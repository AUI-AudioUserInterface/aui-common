from dataclasses import dataclass
from typing import Mapping, Optional, Sequence

@dataclass(frozen=True)
class AdapterMeta:
    name: str                 # "pc", "ari-simple"
    version: str              # "0.1.0"
    vendor: str               # "AUI" / "Community" / "Acme Inc."
    description: str
    # Technische Hinweise/Fähigkeiten (nur das, was stabil ist)
    sample_rates: Sequence[int] = (16000,)
    channels: int = 1
    sample_format: str = "s16le"      # oder "f32le", ...
    supports_wait: bool = True
    supports_streaming: bool = True
    supports_dtmf: bool = False
    requires_network: bool = False
    estimated_latency_ms: int = 50
    capabilities: Optional[Mapping[str, bool]] = None  # frei erweiterbar
