"""Utility hooks for registering lightweight tool metadata."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Iterable


@dataclass(frozen=True)
class ToolDescription:
    """Lightweight descriptor capturing what an automation tool can do."""

    name: str
    description: str

    def dict(self) -> Dict[str, str]:
        return asdict(self)


def default_toolkit() -> Dict[str, ToolDescription]:
    """Return a deterministic baseline tool registry used for planning."""

    return {
        "shell_command": ToolDescription(
            name="shell_command",
            description="Execute a safe command within the target repository context.",
        ),
        "apply_diff": ToolDescription(
            name="apply_diff",
            description="Prepare a patch or diff that can be inspected before applying.",
        ),
    }


def tool_names(toolkit: Iterable[ToolDescription] | None = None) -> Iterable[str]:
    """Convenience to surface tool names for ranking or inspection."""

    if toolkit is None:
        toolkit = default_toolkit().values()
    return (tool.name for tool in toolkit)
