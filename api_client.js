/* ================================================================
   SimuPharma API Client — Frontend ↔ Backend Bridge
   
   Connects the existing HTML/JS frontend to the FastAPI backend.
   Handles: auth, simulation requests, experiment logging, analytics.
   
   Falls back gracefully when backend is unavailable (offline mode).
   ================================================================ */
(function () {
    'use strict';

    const API_BASE = 'http://localhost:8000';
    const TOKEN_KEY = 'simupharma_token';
    const USER_KEY = 'simupharma_user';

    // ---- State ----
    let authToken = localStorage.getItem(TOKEN_KEY) || null;
    let currentUser = JSON.parse(localStorage.getItem(USER_KEY) || 'null');
    let backendAvailable = false;

    // ---- HTTP Helper ----
    async function apiFetch(path, options = {}) {
        const url = `${API_BASE}${path}`;
        const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
        if (authToken) {
            headers['Authorization'] = `Bearer ${authToken}`;
        }
        try {
            const resp = await fetch(url, { ...options, headers });
            if (!resp.ok) {
                const err = await resp.json().catch(() => ({ detail: resp.statusText }));
                throw new Error(err.detail || `HTTP ${resp.status}`);
            }
            return await resp.json();
        } catch (e) {
            if (e.message === 'Failed to fetch' || e.name === 'TypeError') {
                backendAvailable = false;
                console.warn('[SimuPharma API] Backend unavailable — running in offline mode');
                return null;
            }
            throw e;
        }
    }

    // ---- Health Check ----
    async function checkBackend() {
        try {
            const data = await apiFetch('/api/health');
            if (data && data.status === 'healthy') {
                backendAvailable = true;
                console.log(`%c[SimuPharma API] Connected — v${data.version} with ${data.engines.length} engines`, 'color:#22c55e;font-weight:bold');
                updateBackendBadge(true);
                return true;
            }
        } catch (e) { /* silent */ }
        backendAvailable = false;
        updateBackendBadge(false);
        return false;
    }

    // ---- Auth ----
    async function register(email, name, password, institution) {
        const data = await apiFetch('/api/v1/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, name, password, institution })
        });
        if (data) {
            authToken = data.access_token;
            currentUser = data.user;
            localStorage.setItem(TOKEN_KEY, authToken);
            localStorage.setItem(USER_KEY, JSON.stringify(currentUser));
            updateAuthUI();
        }
        return data;
    }

    async function login(email, password) {
        const data = await apiFetch('/api/v1/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        if (data) {
            authToken = data.access_token;
            currentUser = data.user;
            localStorage.setItem(TOKEN_KEY, authToken);
            localStorage.setItem(USER_KEY, JSON.stringify(currentUser));
            updateAuthUI();
        }
        return data;
    }

    async function verifyEmail(token) {
        return apiFetch('/api/v1/auth/verify-email', {
            method: 'POST', body: JSON.stringify({ token })
        });
    }

    async function resendVerification(email) {
        return apiFetch('/api/v1/auth/resend-verification', {
            method: 'POST', body: JSON.stringify({ email })
        });
    }

    async function forgotPassword(email) {
        return apiFetch('/api/v1/auth/forgot-password', {
            method: 'POST', body: JSON.stringify({ email })
        });
    }

    async function resetPassword(token, newPassword) {
        return apiFetch('/api/v1/auth/reset-password', {
            method: 'POST', body: JSON.stringify({ token, new_password: newPassword })
        });
    }

    function logout() {
        authToken = null;
        currentUser = null;
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        updateAuthUI();
    }

    function isLoggedIn() { return !!authToken && !!currentUser; }
    function getUser() { return currentUser; }

    // ---- Simulation APIs ----
    const simulate = {
        uvvis: (params) => apiFetch('/api/v1/simulate/uvvis', { method: 'POST', body: JSON.stringify(params) }),
        uvvisCalibration: (params) => apiFetch('/api/v1/simulate/uvvis/calibration', { method: 'POST', body: JSON.stringify(params) }),
        ftir: (params) => apiFetch('/api/v1/simulate/ftir', { method: 'POST', body: JSON.stringify(params) }),
        hplc: (params) => apiFetch('/api/v1/simulate/hplc', { method: 'POST', body: JSON.stringify(params) }),
        gc: (params) => apiFetch('/api/v1/simulate/gc', { method: 'POST', body: JSON.stringify(params) }),
        massSpec: (params) => apiFetch('/api/v1/simulate/mass-spec', { method: 'POST', body: JSON.stringify(params) }),
        massSpecCompound: (params) => apiFetch('/api/v1/simulate/mass-spec/compound', { method: 'POST', body: JSON.stringify(params) }),
        polarimeter: (params) => apiFetch('/api/v1/simulate/polarimeter', { method: 'POST', body: JSON.stringify(params) }),
        psa: (params) => apiFetch('/api/v1/simulate/psa', { method: 'POST', body: JSON.stringify(params) }),
    };

    // ---- Compounds ----
    const compounds = {
        search: (query, category) => apiFetch(`/api/v1/compounds?q=${encodeURIComponent(query || '')}&category=${encodeURIComponent(category || '')}`),
        get: (id) => apiFetch(`/api/v1/compounds/${id}`),
        spectrum: (id, instrument) => apiFetch(`/api/v1/compounds/${id}/spectrum/${instrument}`),
    };

    // ---- ML Analysis ----
    const analyze = {
        identify: (params) => apiFetch('/api/v1/analyze/identify', { method: 'POST', body: JSON.stringify(params) }),
    };

    // ---- Experiments ----
    const experiments = {
        log: (data) => apiFetch('/api/v1/experiments', { method: 'POST', body: JSON.stringify(data) }),
        list: (instrument) => apiFetch(`/api/v1/experiments?instrument=${instrument || ''}`),
        get: (id) => apiFetch(`/api/v1/experiments/${id}`),
    };

    // ---- Analytics ----
    const analytics = {
        submitQuiz: (data) => apiFetch('/api/v1/analytics/quiz-result', { method: 'POST', body: JSON.stringify(data) }),
        updateProgress: (data) => apiFetch('/api/v1/analytics/progress', { method: 'POST', body: JSON.stringify(data) }),
        getProgress: () => apiFetch('/api/v1/analytics/progress'),
        getStats: () => apiFetch('/api/v1/analytics/stats'),
        getLeaderboard: () => apiFetch('/api/v1/analytics/leaderboard'),
    };

    // ---- Billing ----
    const billing = {
        getPlans: () => apiFetch('/api/v1/billing/plans'),
        createSubscription: (plan, billingPeriod) => apiFetch('/api/v1/billing/create-subscription', {
            method: 'POST', body: JSON.stringify({ plan, billing_period: billingPeriod })
        }),
        verifyPayment: (paymentData) => apiFetch('/api/v1/billing/verify-payment', {
            method: 'POST', body: JSON.stringify(paymentData)
        }),
        getSubscription: () => apiFetch('/api/v1/billing/subscription'),
        cancelSubscription: () => apiFetch('/api/v1/billing/cancel', { method: 'POST' }),
        getInvoices: () => apiFetch('/api/v1/billing/invoices'),
    };

    // ---- UI: Backend Status Badge ----
    function updateBackendBadge(connected) {
        let badge = document.getElementById('api-status-badge');
        if (!badge) {
            badge = document.createElement('div');
            badge.id = 'api-status-badge';
            badge.style.cssText = `
                position:fixed; bottom:20px; left:20px; z-index:8000;
                padding:8px 16px; border-radius:20px; font-size:12px;
                font-family:Inter,system-ui,sans-serif; font-weight:600;
                display:flex; align-items:center; gap:8px;
                box-shadow:0 4px 20px rgba(0,0,0,0.15);
                cursor:pointer; transition:all 0.3s ease;
                backdrop-filter:blur(10px);
            `;
            badge.addEventListener('click', () => {
                if (!backendAvailable) {
                    showAuthModal();
                } else if (!isLoggedIn()) {
                    showAuthModal();
                } else {
                    badge.title = `Logged in as ${currentUser.name}`;
                }
            });
            document.body.appendChild(badge);
        }

        if (connected) {
            badge.style.background = 'rgba(34,197,94,0.15)';
            badge.style.border = '1px solid rgba(34,197,94,0.3)';
            badge.style.color = '#16a34a';
            const userText = isLoggedIn() ? ` · ${currentUser.name}` : '';
            badge.innerHTML = `<span style="width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block"></span>API Connected${userText}`;
        } else {
            badge.style.background = 'rgba(239,68,68,0.1)';
            badge.style.border = '1px solid rgba(239,68,68,0.2)';
            badge.style.color = '#dc2626';
            badge.innerHTML = `<span style="width:8px;height:8px;border-radius:50%;background:#ef4444;display:inline-block"></span>Offline Mode`;
        }
    }

    function updateAuthUI() {
        updateBackendBadge(backendAvailable);
        // Dispatch event for other scripts to react
        window.dispatchEvent(new CustomEvent('simupharma:auth', { detail: { user: currentUser, loggedIn: isLoggedIn() } }));
    }

    // ---- UI: Auth Modal ----
    function showAuthModal() {
        if (document.getElementById('sp-auth-modal')) return;

        const overlay = document.createElement('div');
        overlay.id = 'sp-auth-modal';
        overlay.style.cssText = `
            position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;
            background:rgba(0,0,0,0.6);backdrop-filter:blur(5px);animation:spFadeIn 0.2s ease;
        `;

        const card = document.createElement('div');
        card.style.cssText = `
            background:#0f172a;border:1px solid rgba(37,99,235,0.3);border-radius:16px;
            padding:32px;width:380px;max-width:90vw;color:#e2e8f0;
            font-family:Inter,system-ui,sans-serif;box-shadow:0 25px 60px rgba(0,0,0,0.5);
        `;

        card.innerHTML = `
            <div style="text-align:center;margin-bottom:24px">
                <div style="font-size:28px;margin-bottom:8px">🔬</div>
                <h2 style="font-size:20px;font-weight:700;color:#fff;margin:0">SimuPharma Account</h2>
                <p style="font-size:13px;color:#94a3b8;margin:4px 0 0">Sign in to save experiments & track progress</p>
            </div>
            <div id="sp-auth-tabs" style="display:flex;gap:4px;margin-bottom:20px;background:#1e293b;padding:4px;border-radius:10px">
                <button data-tab="login" class="sp-tab-active"
                    style="flex:1;padding:8px;border:none;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;
                    background:#2563eb;color:#fff;transition:all 0.2s">Sign In</button>
                <button data-tab="register"
                    style="flex:1;padding:8px;border:none;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;
                    background:transparent;color:#94a3b8;transition:all 0.2s">Register</button>
            </div>
            <form id="sp-auth-form">
                <div id="sp-name-field" style="display:none;margin-bottom:12px">
                    <input name="name" placeholder="Full Name" style="${inputStyle()}" />
                </div>
                <div style="margin-bottom:12px">
                    <input name="email" type="email" placeholder="Email" required style="${inputStyle()}" />
                </div>
                <div style="margin-bottom:12px">
                    <input name="password" type="password" placeholder="Password" required style="${inputStyle()}" />
                </div>
                <div id="sp-inst-field" style="display:none;margin-bottom:12px">
                    <input name="institution" placeholder="Institution (optional)" style="${inputStyle()}" />
                </div>
                <div id="sp-auth-error" style="color:#ef4444;font-size:12px;margin-bottom:8px;display:none"></div>
                <button type="submit" style="
                    width:100%;padding:12px;border:none;border-radius:10px;
                    background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;
                    font-size:14px;font-weight:700;cursor:pointer;transition:all 0.2s;
                ">Sign In</button>
            </form>
            <button id="sp-auth-close" style="
                position:absolute;top:12px;right:16px;background:none;border:none;
                color:#64748b;font-size:20px;cursor:pointer;
            ">✕</button>
        `;

        overlay.appendChild(card);
        document.body.appendChild(overlay);

        let mode = 'login';
        const form = card.querySelector('#sp-auth-form');
        const tabs = card.querySelectorAll('[data-tab]');
        const nameField = card.querySelector('#sp-name-field');
        const instField = card.querySelector('#sp-inst-field');
        const submitBtn = form.querySelector('button[type=submit]');
        const errorDiv = card.querySelector('#sp-auth-error');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                mode = tab.dataset.tab;
                tabs.forEach(t => { t.style.background = 'transparent'; t.style.color = '#94a3b8'; });
                tab.style.background = '#2563eb'; tab.style.color = '#fff';
                nameField.style.display = mode === 'register' ? 'block' : 'none';
                instField.style.display = mode === 'register' ? 'block' : 'none';
                submitBtn.textContent = mode === 'register' ? 'Create Account' : 'Sign In';
                errorDiv.style.display = 'none';
            });
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            errorDiv.style.display = 'none';
            submitBtn.disabled = true;
            submitBtn.textContent = 'Please wait...';
            try {
                const fd = new FormData(form);
                if (mode === 'register') {
                    await register(fd.get('email'), fd.get('name'), fd.get('password'), fd.get('institution'));
                } else {
                    await login(fd.get('email'), fd.get('password'));
                }
                overlay.remove();
            } catch (err) {
                errorDiv.textContent = err.message;
                errorDiv.style.display = 'block';
                submitBtn.disabled = false;
                submitBtn.textContent = mode === 'register' ? 'Create Account' : 'Sign In';
            }
        });

        card.querySelector('#sp-auth-close').addEventListener('click', () => overlay.remove());
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
    }

    function inputStyle() {
        return `width:100%;padding:10px 14px;border:1px solid #334155;border-radius:8px;
                background:#1e293b;color:#e2e8f0;font-size:14px;font-family:inherit;
                outline:none;box-sizing:border-box;transition:border 0.2s;`;
    }

    // ---- Add CSS animation ----
    const style = document.createElement('style');
    style.textContent = `@keyframes spFadeIn{from{opacity:0}to{opacity:1}}
        #sp-auth-modal input:focus{border-color:#2563eb !important}`;
    document.head.appendChild(style);

    // ---- Expose Global API ----
    window.SimuPharmaAPI = {
        checkBackend,
        isAvailable: () => backendAvailable,

        // Auth
        register, login, logout,
        isLoggedIn, getUser,
        showAuthModal,
        verifyEmail, resendVerification,
        forgotPassword, resetPassword,

        // Simulation
        simulate,

        // Compounds
        compounds,

        // ML Analysis
        analyze,

        // Experiments
        experiments,

        // Analytics
        analytics,

        // Billing
        billing,
    };

    // Auto-check backend on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', checkBackend);
    } else {
        checkBackend();
    }
})();
