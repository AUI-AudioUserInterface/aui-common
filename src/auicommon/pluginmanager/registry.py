from __future__ import annotations
import importlib.metadata as md
import logging
from typing import Any, Callable, Dict, Iterable, Optional, Sequence, Type, TypeVar, Generic

T = TypeVar("T")
_log = logging.getLogger("auicommon.pluginmanager")

def _iter_entry_points(groups: Sequence[str]) -> Iterable[Any]:
    for grp in groups:
        try:
            yield from md.entry_points(group=grp)  # py3.10+
        except TypeError:
            eps = md.entry_points()                # py3.8/3.9
            if hasattr(eps, "get"):
                yield from eps.get(grp, [])
            else:
                yield from (ep for ep in eps if getattr(ep, "group", None) == grp)

class PluginRegistry(Generic[T]):
    """Generic, stateless plugin registry (discovery + factories)."""

    def __init__(self, groups: Sequence[str], *, contract: Optional[Type[Any]] = None) -> None:
        self._groups = tuple(groups)
        self._contract = contract
        self._reg: Dict[str, Callable[..., T]] = {}

    def load_entry_points(self, *, refresh: bool = False) -> None:
        if self._reg and not refresh:
            return
        if refresh:
            self._reg.clear()
        for ep in _iter_entry_points(self._groups):
            try:
                obj = ep.load()
                name = ep.name.lower()
                if isinstance(obj, type):
                    self._reg[name] = lambda **kw: obj(**kw)  # per-EP closure
                elif callable(obj):
                    self._reg[name] = obj
                else:
                    _log.warning("EP '%s' ignored (not class/callable)", ep.name)
            except Exception as e:
                _log.warning("EP '%s' failed to load: %s", getattr(ep, "name", "?"), e)

    def register(self, name: str, factory: Callable[..., T]) -> None:
        self._reg[name.lower()] = factory

    def remove(self, name: str) -> bool:
        return self._reg.pop(name.lower(), None) is not None

    def list(self, *, refresh: bool = False) -> list[str]:
        self.load_entry_points(refresh=refresh)
        return sorted(self._reg.keys())

    def make(self, name: str, **kwargs: Any) -> T:
        if not self._reg:
            self.load_entry_points()
        factory = self._reg.get(name.lower())
        if not factory:
            raise KeyError(f"Plugin '{name}' not found")
        inst = factory(**kwargs)
        # optional contract check
        if self._contract is not None:
            try:
                if not isinstance(inst, self._contract):  # type: ignore[arg-type]
                    _log.warning("Plugin '%s' does not satisfy contract %s", name, self._contract)
            except TypeError:
                pass
        return inst
