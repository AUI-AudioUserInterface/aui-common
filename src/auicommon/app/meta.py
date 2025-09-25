# auicommon/app/meta.py
from dataclasses import dataclass
from typing import Mapping, Optional

@dataclass(frozen=True)
class AppMeta:
    name: str
    version: str
    category: str
    description: str
    capabilities: Optional[Mapping[str, bool]] = None  # optional
