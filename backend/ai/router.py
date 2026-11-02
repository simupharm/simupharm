"""Universal AI Provider Router — Supports ANY API key from ANY provider.

Auto-detects which keys are configured in .env and routes through them.
Providers tried in order: Groq → Gemini → OpenRouter → OpenAI.
Falls through to next provider on error/quota. Returns provider name in response.
"""
import asyncio
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Optional
import logging

from backend.config import GEMINI_API_KEY, GROQ_API_KEY, OPENROUTER_API_KEY, OPENAI_API_KEY

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI"])

MAX_RETRIES = 2
RETRY_DELAY = 3


# ---- Provider Definitions ----
def _build_providers():
    """Build list of available providers based on configured keys."""
    providers = []

    if GEMINI_API_KEY and GEMINI_API_KEY != "your-gemini-api-key-here":
        providers.append({
            "name": "gemini",
            "type": "gemini",
            "key": GEMINI_API_KEY,
            "models": ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash-latest"],
            "api_versions": ["v1beta", "v1"],
            "label": "Gemini Flash",
        })

    if GROQ_API_KEY:
        providers.append({
            "name": "groq",
            "type": "openai_compatible",
            "url": "https://api.groq.com/openai/v1/chat/completions",
            "key": GROQ_API_KEY,
            "model": "llama-3.1-8b-instant",
            "label": "Groq (Llama 3.1)",
        })

    if OPENROUTER_API_KEY:
        providers.append({
            "name": "openrouter",
            "type": "openai_compatible",
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "key": OPENROUTER_API_KEY,
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "label": "OpenRouter (Llama 3.1)",
        })

    if OPENAI_API_KEY:
        providers.append({
            "name": "openai",
            "type": "openai_compatible",
            "url": "https://api.openai.com/v1/chat/completions",
            "key": OPENAI_API_KEY,
            "model": "gpt-4o-mini",
            "label": "OpenAI GPT-4o Mini",
        })

    return providers


PROVIDERS = _build_providers()


class ChatRequest(BaseModel):
    """Request body — accepts both Gemini-native and OpenAI-compatible formats."""
    contents: Optional[list[dict[str, Any]]] = None
    messages: Optional[list[dict[str, Any]]] = None  # OpenAI format
    system_instruction: Optional[dict[str, Any]] = None
    tools: Optional[list[dict[str, Any]]] = None
    tool_config: Optional[dict[str, Any]] = None
    generationConfig: Optional[dict[str, Any]] = None


# ---- Status ----
@router.get("/status")
def ai_status():
    """Check which providers are configured."""
    available = [{"name": p["name"], "label": p["label"]} for p in PROVIDERS]
    return {
        "has_key": len(PROVIDERS) > 0,
        "providers": available,
        "primary": PROVIDERS[0]["name"] if PROVIDERS else None,
    }


# ---- Test ----
@router.post("/test")
async def test_providers():
    """Test all configured providers."""
    results = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        for prov in PROVIDERS:
            try:
                if prov["type"] == "openai_compatible":
                    resp = await client.post(
                        prov["url"],
                        headers={"Authorization": f"Bearer {prov['key']}", "Content-Type": "application/json"},
                        json={
                            "model": prov["model"],
                            "messages": [{"role": "user", "content": "Reply with OK"}],
                            "max_tokens": 5,
                        },
                    )
                    working = resp.status_code == 200
                    results.append({"provider": prov["name"], "working": working, "status": resp.status_code})
                    if working:
                        return {"working": True, "provider": prov["name"], "label": prov["label"], "all": results}

                elif prov["type"] == "gemini":
                    for model in prov["models"][:1]:
                        for ver in prov["api_versions"][:1]:
                            url = f"https://generativelanguage.googleapis.com/{ver}/models/{model}:generateContent?key={prov['key']}"
                            resp = await client.post(url, json={
                                "contents": [{"parts": [{"text": "Reply OK"}]}],
                                "generationConfig": {"maxOutputTokens": 5, "temperature": 0},
                            })
                            working = resp.status_code == 200
                            quota = resp.status_code == 429
                            results.append({"provider": "gemini", "working": working or quota, "status": resp.status_code})
                            if working:
                                return {"working": True, "provider": "gemini", "label": prov["label"], "all": results}
            except Exception as e:
                results.append({"provider": prov["name"], "working": False, "error": str(e)})

    return {"working": False, "provider": None, "all": results, "error": "No provider responded"}


# ---- Chat ----
@router.post("/chat")
async def chat_proxy(req: ChatRequest):
    """Route chat through available providers with automatic failover."""
    if not PROVIDERS:
        raise HTTPException(status_code=503, detail="No AI API keys configured. Add GROQ_API_KEY or GEMINI_API_KEY to .env")

    # Convert Gemini format to messages if needed
    messages = _to_openai_messages(req)
    gemini_body = _to_gemini_body(req)

    last_error = None

    for prov in PROVIDERS:
        for attempt in range(MAX_RETRIES):
            try:
                result = await _call_provider(prov, messages, gemini_body)
                if result:
                    # Normalize response to Gemini format (frontend expects it)
                    return _normalize_response(result, prov)

            except QuotaError:
                logger.warning(f"[{prov['name']}] Quota exceeded (attempt {attempt + 1})")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                break  # Move to next provider

            except ProviderError as e:
                logger.warning(f"[{prov['name']}] Error: {e}")
                last_error = str(e)
                break  # Move to next provider

            except Exception as e:
                logger.error(f"[{prov['name']}] Unexpected: {e}")
                last_error = str(e)
                break

    raise HTTPException(
        status_code=429,
        detail=f"All AI providers exhausted. Last error: {last_error}. "
               "Add more API keys in .env or wait 1-2 minutes for quota to reset. "
               "Get a free Groq key at https://console.groq.com"
    )


class QuotaError(Exception):
    pass


class ProviderError(Exception):
    pass


async def _call_provider(prov, messages, gemini_body):
    """Call a single provider. Returns parsed response or raises an exception."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        if prov["type"] == "openai_compatible":
            body = {
                "model": prov["model"],
                "messages": messages,
                "max_tokens": 2048,
                "temperature": 0.7,
            }
            resp = await client.post(
                prov["url"],
                headers={
                    "Authorization": f"Bearer {prov['key']}",
                    "Content-Type": "application/json",
                },
                json=body,
            )

            if resp.status_code == 200:
                logger.info(f"[{prov['name']}] ✅ Success")
                return {"raw": resp.json(), "format": "openai"}
            if resp.status_code == 429:
                raise QuotaError(f"{prov['name']} rate limited")
            if resp.status_code == 403 or resp.status_code == 401:
                raise ProviderError(f"{prov['name']} auth failed ({resp.status_code})")
            raise ProviderError(f"{prov['name']} returned {resp.status_code}")

        elif prov["type"] == "gemini":
            for model in prov["models"]:
                for api_ver in prov["api_versions"]:
                    url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{model}:generateContent?key={prov['key']}"
                    resp = await client.post(url, json=gemini_body)

                    if resp.status_code == 200:
                        logger.info(f"[gemini] ✅ {model}/{api_ver}")
                        return {"raw": resp.json(), "format": "gemini"}
                    if resp.status_code == 429:
                        raise QuotaError("gemini rate limited")
                    if resp.status_code == 403:
                        raise ProviderError("gemini key invalid")
                    if resp.status_code == 404:
                        continue
                    if resp.status_code == 400:
                        continue

            raise ProviderError("gemini: no model worked")

    return None


def _to_openai_messages(req: ChatRequest) -> list:
    """Convert Gemini-format contents to OpenAI-format messages."""
    if req.messages:
        return req.messages

    messages = []

    # System instruction
    if req.system_instruction:
        parts = req.system_instruction.get("parts", [])
        sys_text = " ".join(p.get("text", "") for p in parts if "text" in p)
        if sys_text:
            messages.append({"role": "system", "content": sys_text})

    # Contents
    if req.contents:
        for item in req.contents:
            role = item.get("role", "user")
            parts = item.get("parts", [])
            text_parts = [p.get("text", "") for p in parts if "text" in p]
            if text_parts:
                oai_role = "assistant" if role == "model" else "user"
                messages.append({"role": oai_role, "content": " ".join(text_parts)})

    return messages or [{"role": "user", "content": "Hello"}]


def _to_gemini_body(req: ChatRequest) -> dict:
    """Build Gemini-format request body."""
    body = {}
    if req.contents:
        body["contents"] = req.contents
    if req.system_instruction:
        body["system_instruction"] = req.system_instruction
    if req.tools:
        body["tools"] = req.tools
    if req.tool_config:
        body["tool_config"] = req.tool_config
    if req.generationConfig:
        body["generationConfig"] = req.generationConfig
    return body


def _normalize_response(result: dict, prov: dict) -> dict:
    """Normalize any provider response to Gemini-compatible format."""
    raw = result["raw"]

    if result["format"] == "gemini":
        # Already Gemini format, just add provider info
        raw["_provider"] = prov["name"]
        raw["_provider_label"] = prov["label"]
        return raw

    if result["format"] == "openai":
        # Convert OpenAI format → Gemini format
        choices = raw.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content", "")
        else:
            content = "No response generated."

        return {
            "candidates": [{
                "content": {
                    "parts": [{"text": content}],
                    "role": "model"
                },
                "finishReason": "STOP"
            }],
            "_provider": prov["name"],
            "_provider_label": prov["label"],
        }

    return raw


# ─────────────────────────────────────────────────────────
# TEXT-TO-SPEECH  — 3-tier: OpenAI nova → edge-tts → error
# ─────────────────────────────────────────────────────────
from fastapi.responses import StreamingResponse
import io

class TTSRequest(BaseModel):
    text: str
    voice: str = "nova"
    model: str = "tts-1"   # tts-1 is faster with higher rate limits than tts-1-hd
    speed: float = 1.0

async def _tts_openai(text: str, voice: str, model: str, speed: float) -> bytes | None:
    """Try OpenAI TTS. Returns audio bytes or None on failure."""
    if not OPENAI_API_KEY:
        return None
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/audio/speech",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
                json={"model": model, "voice": voice, "input": text, "speed": speed, "response_format": "mp3"},
            )
        if resp.status_code == 200:
            return resp.content
        logger.warning(f"[TTS] OpenAI returned {resp.status_code}")
    except Exception as e:
        logger.warning(f"[TTS] OpenAI failed: {e}")
    return None

async def _tts_edge(text: str) -> bytes | None:
    """Use Microsoft Edge TTS (free, neural Aria voice). Returns mp3 bytes or None."""
    try:
        import edge_tts, tempfile, os, asyncio
        voice = "en-US-AriaNeural"   # Warm, natural female voice
        communicate = edge_tts.Communicate(text, voice, rate="+5%", volume="+0%")
        # edge_tts writes to a file; collect via streaming
        buf = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])
        audio = buf.getvalue()
        return audio if audio else None
    except Exception as e:
        logger.warning(f"[TTS] edge-tts failed: {e}")
    return None

@router.post("/tts")
async def text_to_speech(req: TTSRequest):
    """
    Human-quality TTS with automatic fallback chain:
      1. OpenAI tts-1 nova  (premium, fast)
      2. edge-tts Aria       (Microsoft neural voice, free, always available)
    """
    text = req.text.strip()[:4096]
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")

    # Tier 1 — OpenAI
    audio = await _tts_openai(text, req.voice, req.model, req.speed)

    # Tier 2 — edge-tts (Microsoft neural, free)
    if not audio:
        audio = await _tts_edge(text)

    if not audio:
        raise HTTPException(status_code=503, detail="All TTS providers unavailable")

    return StreamingResponse(
        io.BytesIO(audio),
        media_type="audio/mpeg",
        headers={"Cache-Control": "no-cache"},
    )
