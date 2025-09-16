"""Minimal in-process agent session for the Codespeak MVP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Protocol

from .project_index import ProjectIndex, resolve_project_index
from .planners import Plan, draft_plan


class SupportsToolkit(Protocol):
    def default_toolkit(self) -> Dict[str, object]:
        ...

    def tool_names(self, toolkit: Iterable[object] | None = None) -> Iterable[str]:
        ...


@dataclass
class AgentSession:
    """Tracks the working directory and cached project index."""

    project_root: str
    index: ProjectIndex

    def dict(self) -> Dict[str, object]:
        return {"project_root": self.project_root, "index": self.index.dict()}


@dataclass
class AgentResponse:
    """Container returned by :func:`respond` for CLI serialization."""

    plan: Plan
    tools: Iterable[str]

    def dict(self) -> Dict[str, object]:
        return {"plan": self.plan.dict(), "tools": list(self.tools)}


def session(project: str = ".") -> AgentSession:
    """Initialize an agent session anchored on the provided project path."""

    index = resolve_project_index(project)
    return AgentSession(project_root=str(index.root), index=index)


def respond(state: AgentSession, utterance: str, tools_module: SupportsToolkit) -> AgentResponse:
    """Produce a deterministic response leveraging the supplied tools module."""

    toolkit = tools_module.default_toolkit()
    tool_names = list(tools_module.tool_names(toolkit.values()))
    plan = draft_plan(utterance, state.index, tool_names)
    return AgentResponse(plan=plan, tools=tool_names)
