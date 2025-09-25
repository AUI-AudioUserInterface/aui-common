from dataclasses import dataclass
from typing import Mapping, Optional, Sequence

@dataclass(frozen=True)
class TtsMeta:
    name: str                 # "piper", "coqui"
    version: str              # "0.3.2"
    vendor: str               # "AUI" / "Community" / "Acme Inc."
    description: str
    languages: Sequence[str] = ()     # ["de-DE", "en-US"]
    voices: Sequence[str] = ()        # ["thorsten", "karl", ...] (optional/Subset)
    sample_rates: Sequence[int] = (16000,)
    channels: int = 1
    sample_format: str = "s16le"
    supports_streaming: bool = True
    requires_network: bool = False
    estimated_latency_ms: int = 120
    capabilities: Optional[Mapping[str, bool]] = None
