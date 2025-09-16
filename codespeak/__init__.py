"""Codespeak package init for repo-aware voice agent MVP."""

from .agent import AgentResponse, AgentSession, respond, session
from .checker import CheckResult, Edit, normalize_utterance

__all__ = [
    "AgentResponse",
    "AgentSession",
    "CheckResult",
    "Edit",
    "normalize_utterance",
    "respond",
    "session",
]

__version__ = "0.1.0"
