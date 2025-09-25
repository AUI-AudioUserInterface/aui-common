from __future__ import annotations
import io, struct, audioop, wave, array
from .types import PcmAudio, AudioFormat

# Kanonisches Zwischenformat für AUI
CANON_FORMAT = AudioFormat(rate=16000, channels=1, width=2)  # s16le, mono, 16kHz

def f32le_to_s16le(buf_f32: bytes) -> bytes:
    """float32 (-1..1) → int16 little endian (mono)."""
    arr = array.array("f")
    arr.frombytes(buf_f32)
    out = bytearray(len(arr) * 2)
    for i, x in enumerate(arr):
        x = max(-1.0, min(1.0, x))
        out[i*2:(i+1)*2] = struct.pack("<h", int(x * 32767.0))
    return bytes(out)

def resample_s16le_mono(pcm_s16: bytes, src_rate: int, dst_rate: int) -> bytes:
    """Resampling mono, s16le → s16le (audioop.ratecv)."""
    if src_rate == dst_rate:
        return pcm_s16
    converted, _ = audioop.ratecv(pcm_s16, 2, 1, src_rate, dst_rate, None)
    return converted

def s16le_to_ulaw(pcm_s16: bytes) -> bytes:
    """PCM → µ-law (8-bit)."""
    return audioop.lin2ulaw(pcm_s16, 2)

def s16le_to_alaw(pcm_s16: bytes) -> bytes:
    """PCM → A-law (8-bit)."""
    return audioop.lin2alaw(pcm_s16, 2)

def wav_frame(pcm: PcmAudio) -> bytes:
    """PCM in WAV kapseln (Header + Daten)."""
    bio = io.BytesIO()
    with wave.open(bio, "wb") as w:
        w.setnchannels(pcm.channels)
        w.setsampwidth(pcm.width)
        w.setframerate(pcm.rate)
        w.writeframes(pcm.data)
    return bio.getvalue()

def normalize_to_canon(pcm: PcmAudio) -> PcmAudio:
    """
    PCM → PcmAudio im kanonischen Format (s16le, mono, 16kHz).
    Wandelt bei Bedarf float32 → s16le, resample, downmix.
    """
    # Sample-Format normalisieren
    if pcm.width == 2:
        s16 = pcm.data
    elif pcm.width == 4:
        s16 = f32le_to_s16le(pcm.data)
    else:
        raise ValueError(f"Unsupported width={pcm.width}")

    # Resample falls nötig
    if pcm.rate != CANON_FORMAT.rate:
        s16 = resample_s16le_mono(s16, pcm.rate, CANON_FORMAT.rate)

    # Downmix falls nötig
    if pcm.channels > 1:
        s16 = audioop.tomono(s16, 2, 0.5, 0.5)

    return PcmAudio(data=s16, rate=CANON_FORMAT.rate,
                    channels=CANON_FORMAT.channels,
                    width=CANON_FORMAT.width)
