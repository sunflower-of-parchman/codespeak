# Codespeak

Repo-aware voice agent MVP that cleans noisy developer utterances and turns them into deterministic plans.

Codespeak now ships with a **checker** front-end that normalizes voice transcripts before they reach the planner. This makes the downstream automation far more reliable when users mumble repository names, pronounce CLI flags, or mix frameworks mid-sentence.

## Architecture at a Glance
- **Checker (`codespeak/checker.py`)** &mdash; Builds a lexicon from the project tree, package manifests, and common developer jargon. It rewrites transcripts, records edits with confidence scores, and can prompt for clarification when two options look similar.
- **Planner (`codespeak/agent.py`)** &mdash; Optional follow-up step that takes the cleaned utterance and resolves intents/tool calls. Enable it with `--with-plan` when you want the end-to-end flow.
- **CLI (`codespeak/cli.py`)** &mdash; Minimal Typer app that exposes both flows. Invoking `codespeak` runs the checker (and the planner when requested). The legacy `codespeak plan` subcommand stays available for direct planning on raw text.

## Getting Started

### Prerequisites
- Python 3.11+
- OpenAI API key with `model.request` scope exported as `OPENAI_API_KEY`
- (Optional) Virtual environment: `python -m venv .venv && source .venv/bin/activate`

### Installation
```bash
pip install -e .[dev]
```
This installs Codespeak along with formatter/lint/test tooling.

### Pointing at a Repository
The checker builds its lexicon from a project root. Pass the path with `-p/--project` (defaults to the current directory).

## Usage

### 1. Run the Checker
```bash
codespeak "set up prisma migraiton dash dash force" -p /path/to/repo
```
Example output:
```json
{
  "checker": {
    "original": "set up prisma migraiton dash dash force",
    "cleaned": "set up prisma migration --force",
    "edits": [
      {"src": "migraiton", "dst": "migration", "reason": "repo_lexicon_match", "confidence": 0.84}
    ],
    "needs_clarification": false,
    "clarifier": null
  }
}
```

### 2. Checker + Planner
```bash
codespeak "generate nuxt page for pricing" -p /path/to/repo --with-plan
```
Returns the checker block plus a planner payload (intent, arguments, safety metadata). Planner execution requires network access to OpenAI.

### 3. Direct Planner (legacy)
```bash
codespeak plan "run prisma migrate dev name init force" -p /path/to/repo
```
Skips normalization and feeds the raw string to the planner.

## Project Layout
- `codespeak/checker.py` &mdash; Transcript normalization with repo-aware lexicon matching.
- `codespeak/agent.py` &mdash; Planner interface returning structured actions.
- `codespeak/cli.py` &mdash; Typer entrypoint exposing checker-only and checker+planner flows.
- `codespeak/project_index.py` &mdash; Lightweight file/dependency index used by the checker.
- `README.md`, `AGENTS.md` &mdash; Repository documentation and operating guidelines.

## Development Workflow
- Format: `ruff check .` and `black .`
- Tests: `pytest` (add coverage for every checker/planner branch)
- Type checking: optional but recommended via `ruff --select TID`
- Commit style: Conventional Commits (`feat:`, `fix:`, etc.)

## Roadmap
- Hook into the Realtime API for speech in/out.
- Add an editor surface (VS Code extension prototype).
- Harden normalization heuristics and diff generation.

Share feedback with the OpenAI Codex team&mdash;this repo now demonstrates how the checker stabilizes voice inputs before agents execute plans.
