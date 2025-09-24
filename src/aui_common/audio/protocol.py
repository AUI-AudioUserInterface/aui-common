from typing import Protocol
from aui_common.audio.types import PcmAudio

class AudioSink(Protocol):
    async def play(self, audio: PcmAudio, wait: bool = False) -> None: ...

class AudioSource(Protocol):
    async def record(self, duration: float) -> PcmAudio: ...
