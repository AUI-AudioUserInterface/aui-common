from typing import Protocol, Optional, AsyncIterator
from auicommon.audio.types import PcmAudio
from auicommon.util.async_utils import CancellationToken
from auicommon.app.meta import AppMeta
'''
AppContext liefert die Schnittstelle / Methoden, die in der App benutzt werden können.
    ctx->say(),
    ctx->play(),
    ...
'''
class AppContext(Protocol):
    # Ausgabe
    async def say(self, text: str, wait: bool = False,
                  cancel: Optional[CancellationToken] = None) -> None: ...
    async def play(self, audio: PcmAudio, wait: bool = False,
                   cancel: Optional[CancellationToken] = None) -> None: ...
    async def stop_audio(self) -> None: ...

    # TTS -> Audio für App zurückgeben
    async def synth(self, text: str,
                    cancel: Optional[CancellationToken] = None) -> PcmAudio: ...
    async def synth_stream(self, text: str,
                           cancel: Optional[CancellationToken] = None
                          ) -> AsyncIterator[PcmAudio]: ...

    # DTMF
    async def get_digit(self, timeout: Optional[float] = None) -> Optional[str]: ...
    async def wait_for_digit(self, digits: str,
                             timeout: Optional[float] = None) -> Optional[str]: ...
