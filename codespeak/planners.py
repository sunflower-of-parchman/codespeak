"""Planning heuristics for translating utterances into executable actions."""

from __future__ import annotations

import shlex
from dataclasses import dataclass, asdict
from typing import Dict, Iterable

from .project_index import ProjectIndex


@dataclass
class Plan:
    """Simple planning result exposed through the agent response."""

    intent: str
    utterance: str
    command: str
    tool: str
    confidence: float

    def dict(self) -> Dict[str, object]:
        return asdict(self)


def draft_plan(
    utterance: str, index: ProjectIndex, tools: Iterable[str]
) -> Plan:
    """Produce a deterministic plan using repository metadata and available tools."""

    tool_choice = next(iter(tools), "shell_command")
    command = f"echo {shlex.quote(utterance)}"
    return Plan(
        intent="analyze_repo_request",
        utterance=utterance,
        command=command,
        tool=tool_choice,
        confidence=0.2,
    )
