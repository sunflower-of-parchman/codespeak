"""Minimal project indexer that inspects the active repository."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List


@dataclass
class ProjectIndex:
    """Structured view of repository metadata consumed by planners."""

    root: Path
    files: List[str] = field(default_factory=list)
    scripts: Dict[str, str] = field(default_factory=dict)

    def dict(self) -> Dict[str, object]:
        return {
            "root": str(self.root),
            "files": list(self.files),
            "scripts": dict(self.scripts),
        }


def _discover_scripts(pyproject_path: Path) -> Dict[str, str]:
    try:
        raw = pyproject_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}

    try:
        data = json.loads(raw)  # fallback if file already json encoded
    except json.JSONDecodeError:
        data = None

    if isinstance(data, dict):
        scripts = data.get("project", {}).get("scripts", {})
        if isinstance(scripts, dict):
            return {str(k): str(v) for k, v in scripts.items()}
        return {}

    # Naive parse for simple TOML-like key/value pairs
    scripts: Dict[str, str] = {}
    capture = False
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("[project.scripts]"):
            capture = True
            continue
        if capture and stripped.startswith("["):
            break
        if capture and "=" in stripped:
            key, value = stripped.split("=", 1)
            scripts[key.strip()] = value.strip().strip('"')
    return scripts


def resolve_project_index(project_root: str | None = None) -> ProjectIndex:
    """Build a deterministic project inventory suitable for downstream planning."""

    root = Path(project_root or os.environ.get("CODESPEAK_PROJECT_ROOT", os.getcwd()))
    root = root.resolve()
    files = sorted(
        str(path.relative_to(root))
        for path in root.glob("**/*")
        if path.is_file() and not path.name.startswith(".")
    )

    scripts = _discover_scripts(root / "pyproject.toml")
    return ProjectIndex(root=root, files=files, scripts=scripts)
