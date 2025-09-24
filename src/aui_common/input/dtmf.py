from enum import Enum
from dataclasses import dataclass
from typing import Optional

class DtmfDigit(str, Enum):
    D0="0"; D1="1"; D2="2"; D3="3"; D4="4"; D5="5"; D6="6"; D7="7"; D8="8"; D9="9"
    STAR="*"; HASH="#"; A="A"; B="B"; C="C"; D="D"

@dataclass
class DtmfEvent:
    digit: DtmfDigit
    ts: float                 # monotonic timestamp (seconds)
    source: Optional[str]=None  # z.B. "pc", "ari", "sip"
