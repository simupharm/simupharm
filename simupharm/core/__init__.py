"""
SimuPharm Core Types and Abstractions.
"""
from pydantic import BaseModel, Field

class SpectrumResult(BaseModel):
    """Base class for spectral simulation results."""
    instrument: str
    metadata: dict = Field(default_factory=dict)
