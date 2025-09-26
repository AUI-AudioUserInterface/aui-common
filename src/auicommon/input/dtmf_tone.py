from __future__ import annotations
import math
from typing import Optional, Tuple

from auicommon.audio.types import PcmAudio, AudioFormat
from auicommon.input.dtmf import DtmfKey


class DtmfTone:
    """
    Erzeugt DTMF-Töne als 16-bit Mono-PCM (little-endian).
    - Frequenzen gemäß ITU-T Q.23
    - Gleichpegel beider Teiltöne (0 dB twist)
    - Kurzer Fade-In/Fade-Out zur Klickvermeidung
    """

    # (row, col) Frequenzen in Hz
    _MAP: dict[DtmfKey, Tuple[float, float]] = {
        DtmfKey.KEY_1: (697.0, 1209.0),
        DtmfKey.KEY_2: (697.0, 1336.0),
        DtmfKey.KEY_3: (697.0, 1477.0),
        DtmfKey.KEY_4: (770.0, 1209.0),
        DtmfKey.KEY_5: (770.0, 1336.0),
        DtmfKey.KEY_6: (770.0, 1477.0),
        DtmfKey.KEY_7: (852.0, 1209.0),
        DtmfKey.KEY_8: (852.0, 1336.0),
        DtmfKey.KEY_9: (852.0, 1477.0),
        DtmfKey.KEY_STAR: (941.0, 1209.0),
        DtmfKey.KEY_0: (941.0, 1336.0),
        DtmfKey.KEY_HASH: (941.0, 1477.0),
        # A/B/C/D wären (697/770/852/941, 1633) – falls du sie später ergänzen willst.
    }

    @staticmethod
    def from_char(ch: str) -> Optional[DtmfKey]:
        ch = (ch or "")[:1]
        return {
            "0": DtmfKey.KEY_0, "1": DtmfKey.KEY_1, "2": DtmfKey.KEY_2, "3": DtmfKey.KEY_3,
            "4": DtmfKey.KEY_4, "5": DtmfKey.KEY_5, "6": DtmfKey.KEY_6, "7": DtmfKey.KEY_7,
            "8": DtmfKey.KEY_8, "9": DtmfKey.KEY_9, "*": DtmfKey.KEY_STAR, "#": DtmfKey.KEY_HASH,
        }.get(ch)

    @classmethod
    def make(
        cls,
        key: DtmfKey,
        duration_s: float = 0.100,
        audio_format: Optional[AudioFormat] = None,
    ) -> PcmAudio:
        """
        Erzeugt einen DTMF-Ton für 'key' mit gegebener Dauer.
        Erwartetes Zielformat: 16-bit signed, mono, rate=audio_format.rate.
        """
        if key not in cls._MAP:
            # Unbekannte Taste -> Stille
            rate = (audio_format.rate if (audio_format and getattr(audio_format, "rate", None)) else 8000)
            return PcmAudio(data=b"", rate=rate)

        rate = (audio_format.rate if (audio_format and getattr(audio_format, "rate", None)) else 8000)
        if rate <= 0:
            rate = 8000
        if duration_s <= 0.0:
            return PcmAudio(data=b"", rate=rate)

        f1, f2 = cls._MAP[key]
        n_samples = int(round(duration_s * rate))
        if n_samples <= 0:
            return PcmAudio(data=b"", rate=rate)

        # Amplituden so wählen, dass Summe sicher nicht clippt
        # Max-Summenpegel 2*A -> A = 0.45 vermeidet Clipping mit Reserve
        a = 0.45
        max_i16 = 32767.0

        # Fade-In/-Out (Hann-Halbwelle) ~5 ms oder bis zur Hälfte der Länge
        ramp_len = min(int(0.005 * rate), n_samples // 2)

        # Schneller ohne numpy: vor-allokieren und in bytearray packen
        buf = bytearray(2 * n_samples)  # 2 bytes pro Sample (int16)

        two_pi_over_rate = 2.0 * math.pi / rate
        for n in range(n_samples):
            t = n * two_pi_over_rate
            s = (math.sin(f1 * t) + math.sin(f2 * t)) * a  # Summe der beiden Sinusse

            # Hüllkurve anwenden
            if ramp_len > 0:
                if n < ramp_len:
                    # Fade-In
                    w = 0.5 * (1.0 - math.cos(math.pi * n / ramp_len))
                    s *= w
                elif n >= (n_samples - ramp_len):
                    # Fade-Out
                    k = n_samples - 1 - n
                    w = 0.5 * (1.0 - math.cos(math.pi * k / ramp_len))
                    s *= w

            # In int16 konvertieren (little-endian)
            v = int(max(-1.0, min(1.0, s)) * max_i16)
            # schnelleres Packen:
            lo = v & 0xFF
            hi = (v >> 8) & 0xFF
            i = 2 * n
            buf[i] = lo
            buf[i + 1] = hi

        return PcmAudio(data=bytes(buf), rate=rate)

    @classmethod
    def make_from_char(
        cls,
        ch: str,
        duration_s: float = 0.100,
        audio_format: Optional[AudioFormat] = None,
    ) -> Optional[PcmAudio]:
        key = cls.from_char(ch)
        return None if key is None else cls.make(key, duration_s, audio_format)
