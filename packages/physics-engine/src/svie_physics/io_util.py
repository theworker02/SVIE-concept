"""Shared helpers: repo paths, YAML loading, JSON-friendly results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    """Return monorepo root (…/SVIE-concept)."""
    # packages/physics-engine/src/svie_physics/io_util.py → 4 parents up to repo
    return Path(__file__).resolve().parents[4]


def specs_dir() -> Path:
    return repo_root() / "specs"


def load_yaml(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        candidate = specs_dir() / p.name
        if candidate.is_file():
            p = candidate
        else:
            raise FileNotFoundError(f"Spec not found: {path}")
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {p}")
    return data


def dumps_result(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2, sort_keys=False)
