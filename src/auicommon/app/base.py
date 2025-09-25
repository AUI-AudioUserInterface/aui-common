from __future__ import annotations
from typing import Protocol, runtime_checkable
from auicommon.runtime.app_api import AppContext
from auicommon.app.meta import AppMeta

@runtime_checkable
class AppService(Protocol):
    """Contract zwischen Core und App-Plugin."""

    def meta(self) -> AppMeta: ...
    """Leichtgewichtige Metadaten, ohne Nebenwirkungen."""

    def init(self, ctx: AppContext) -> None: ...
    """Context injizieren; hier KEIN I/O, keine Tasks starten."""

    async def start(self) -> None: ...
    """App starten (eigene Loops als Tasks). Zeitnah zurückkehren."""

    async def stop(self) -> None: ...
    """Geordnet stoppen; idempotent."""
