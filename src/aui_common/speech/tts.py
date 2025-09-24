from typing import Protocol, Optional, Iterable, AsyncIterator
from aui_common.audio.types import PcmAudio
from aui_common.util.async_utils import CancellationToken

class SpeechProvider(Protocol):
    async def preload(self) -> None: ...
    async def synth(self, text: str,
                    cancel: Optional[CancellationToken]=None) -> PcmAudio: ...
    # optional: Streaming für niedrige Latenz
    async def stream(self, text: str, 
                     cancel: Optional[CancellationToken]=None) -> AsyncIterator[bytes]: ...
