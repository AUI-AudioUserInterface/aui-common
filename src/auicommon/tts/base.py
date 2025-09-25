from __future__ import annotations
from typing import Protocol, runtime_checkable, Optional, AsyncIterator, Any
from auicommon.audio.types import PcmAudio
from auicommon.util.async_utils import CancellationToken
from .meta import TtsMeta

@runtime_checkable
class TtsService(Protocol):
    def meta(self) -> TtsMeta: ...
    """Abstraktion für Text-zu-Audio-Engines (Piper, Coqui, …)."""

    async def init(self, **kwargs: Any) -> None: ...

    async def start(self) -> None: ...
    async def stop(self) -> None: ...

    async def synth(self, text: str,
                    cancel: Optional[CancellationToken] = None) -> PcmAudio: ...
    """Komplette Synthese (voll gepuffert)."""

    async def synth_stream(self, text: str,
                           cancel: Optional[CancellationToken] = None
                           ) -> AsyncIterator[PcmAudio]: ...
    """Gestreamte Synthese (Chunks)."""
