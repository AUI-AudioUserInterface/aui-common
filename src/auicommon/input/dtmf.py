import asyncio
from enum import Enum

class DtmfKey(Enum):
    KEY_0 = 0
    KEY_1 = 1
    KEY_2 = 2
    KEY_3 = 3
    KEY_4 = 4
    KEY_5 = 5
    KEY_6 = 6
    KEY_7 = 7
    KEY_8 = 8
    KEY_9 = 9
    KEY_STAR = 10
    KEY_HASH = 11

class Dtmf:
    valid_keys=set('0123456789*#')
    
    def __init__(self):
        self._queue : asyncio.Queue[DtmfKey] = asyncio.Queue()

    def add(self, key:DtmfKey) -> None:
        self._queue.put_nowait(key)
    
    def get(self) -> DtmfKey | None:
        try:
            return self._queue.get_nowait()
        except:
            return None

    def flush(self) -> None:
        while not self._queue.empty():
            _ = self._queue.get_nowait()
