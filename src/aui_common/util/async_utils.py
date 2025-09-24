import asyncio
from typing import Callable, Any

class CancellationToken:
    def __init__(self) -> None:
        self._cancelled = False
    def cancel(self) -> None:
        self._cancelled = True
    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

class Debouncer:
    def __init__(self, delay: float) -> None:
        self._delay = delay
        self._task: asyncio.Task | None = None

    async def __call__(self, fn: Callable[[], Any]) -> None:
        if self._task:
            self._task.cancel()
        async def _run():
            await asyncio.sleep(self._delay)
            fn()
        self._task = asyncio.create_task(_run())

class RateLimiter:
    def __init__(self, rate: float) -> None:
        self._rate = rate
        self._last = 0.0

    async def wait(self) -> None:
        now = asyncio.get_event_loop().time()
        elapsed = now - self._last
        wait = max(0.0, (1.0 / self._rate) - elapsed)
        if wait:
            await asyncio.sleep(wait)
        self._last = asyncio.get_event_loop().time()
