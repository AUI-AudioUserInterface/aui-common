from __future__ import annotations
from typing import Protocol, runtime_checkable, Optional, Any
from auicommon.audio.types import PcmAudio  # bei dir bereits vorhanden
from auicommon.util.async_utils import CancellationToken  # bei dir vorhanden
from .meta import AdapterMeta

@runtime_checkable
class AdapterService(Protocol):
    def meta(self) -> AdapterMeta: ...
    """Abstraktion für Audio-Ausgabe/Transporte (z. B. PC, ARI, SIP…)."""

    async def init(self, **kwargs: Any) -> None: ...

    async def start(self) -> None: ...
    async def stop(self) -> None: ...

    async def play(self, audio: PcmAudio, *, wait: bool = False,
                   cancel: Optional[CancellationToken] = None) -> None: ...
    """Audio wiedergeben. Falls `wait=True`, erst zurückkehren, wenn Ausgabe beendet."""

    async def stop_audio(self) -> None: ...
    """Laufende Audioausgabe umgehend abbrechen (Not-Aus)."""
