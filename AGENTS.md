# Repository Guidelines

This repository hosts modular autonomous agents and their shared tooling. Keep contributions focused, deterministic, and easy to test so agents remain composable.

## Project Structure & Module Organization
- Place production code in `src/codespeak/` with one directory per agent (`planner/`, `executor/`, etc.) and shared utilities in `src/codespeak/core/`.
- Mirror each module in `tests/` (e.g., `tests/test_planner.py`) and keep fixtures in `tests/fixtures/`.
- Store prompts, sample transcripts, and configuration defaults under `assets/`; large datasets belong in external storage referenced via `.env` keys.

## Build, Test, and Development Commands
- Create a virtual env with `python -m venv .venv && source .venv/bin/activate`.
- Install dependencies using `pip install -e .[dev]` once the `pyproject.toml` baseline is pulled; re-run after editing dependencies.
- Run the fast feedback suite with `pytest`; use `pytest -m "not slow"` while iterating and `pytest --maxfail=1 --disable-warnings` before submitting.
- Enforce style with `ruff check src tests` and `black src tests`.

## Coding Style & Naming Conventions
- Target Python 3.11, use four-space indentation, and prefer dataclasses for structured payloads.
- Use snake_case for functions, PascalCase for classes, and kebab-case for CLI entry points in `pyproject.toml`.
- Keep prompt templates in `.txt` files and name them `<agent>_prompt.txt`.
- Run `ruff format` only for auto-generated code; otherwise rely on `black`.

## Testing Guidelines
- Write `pytest` unit tests for every agent behavior branch; integration tests live under `tests/integration/` and must mock external APIs.
- Mark slow or network-bound tests with `@pytest.mark.slow` so they can be skipped locally.
- Maintain ≥90% coverage for core planners; add regression tests for every production incident.

## Commit & Pull Request Guidelines
- Follow Conventional Commit prefixes (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`) and keep messages under 72 characters.
- Reference Jira tickets or GitHub issues in the PR description and list blocking dependencies explicitly.
- Include before/after behavior notes, CLI invocations, and screenshots or trace snippets when UI or telemetry changes.
