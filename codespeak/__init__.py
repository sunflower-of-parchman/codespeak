"""Codespeak package init for repo-aware voice agent MVP."""

from .agent import AgentResponse, AgentSession, respond, session

__all__ = [
    "AgentResponse",
    "AgentSession",
    "respond",
    "session",
]

__version__ = "0.1.0"
