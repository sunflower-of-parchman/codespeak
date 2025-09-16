"""Typer entrypoint exposing the Codespeak planning command."""

import typer
from rich import print

from . import tools as tools_mod
from .agent import respond, session

app = typer.Typer(add_completion=False)


@app.command()
def plan(text: str, project: str = "."):
    """Resolve a high-level utterance into a deterministic plan."""

    st = session(project)
    res = respond(st, text, tools_mod)
    print({"raw": res.dict() if hasattr(res, "dict") else str(res)})


if __name__ == "__main__":
    app()
