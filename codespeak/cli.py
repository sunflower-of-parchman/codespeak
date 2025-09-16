"""Typer entrypoint exposing the Codespeak planning command."""

from __future__ import annotations

import typer
from rich import print

from . import tools as tools_mod
from .agent import respond, session
from .checker import normalize_utterance

app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    text: str = typer.Argument(None, help="Raw voice transcript or text"),
    project: str = typer.Option(".", "--project", "-p"),
    with_plan: bool = typer.Option(
        False, "--with-plan", help="Also run planner on cleaned text"
    ),
):
    if text is None:
        typer.echo(app.get_help(ctx=typer.get_current_context()))
        raise typer.Exit(0)

    st = session(project)
    chk = normalize_utterance(text, st.index)
    output = {"checker": chk.dict()}

    if with_plan:
        planned = respond(st, chk.cleaned, tools_mod)
        output["plan"] = planned.dict()

    print(output)


@app.command()
def plan(text: str, project: str = "."):
    st = session(project)
    res = respond(st, text, tools_mod)
    print({"raw": res.dict() if hasattr(res, "dict") else str(res)})


if __name__ == "__main__":
    app()
