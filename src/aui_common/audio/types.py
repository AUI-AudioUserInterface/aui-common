from dataclasses import dataclass

@dataclass
class PcmAudio:
    data: bytes
    rate: int
    channels: int = 1
    width: int = 2

@dataclass
class AudioFormat:
    rate: int
    channels: int = 1
    width: int = 2
