"""Disk-backed JSON cache keyed by (module_name, domain)."""

import json
import hashlib
from pathlib import Path

_CACHE_ROOT = Path("cache")


def _path(module: str, domain: str) -> Path:
    safe = hashlib.sha1(domain.encode()).hexdigest()[:12]
    return _CACHE_ROOT / module / f"{safe}_{domain.replace('/', '_')}.json"


def load(module: str, domain: str):
    p = _path(module, domain)
    if p.exists():
        return json.loads(p.read_text())
    return None


def save(module: str, domain: str, data) -> None:
    p = _path(module, domain)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, default=str, indent=2))
