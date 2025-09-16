# codespeak

Repo-aware voice agent MVP.

## What it does
- Checker: cleans voice-y text (spell/grammar/context) using repo terms; outputs original+cleaned+edits.
- Planner: optional; run with `--with-plan` to plan on the cleaned text.

## Quick start
1. `cp .env.example .env` and set `OPENAI_API_KEY`.
2. `pip install -e .`
3. From a repo:  
   `CODESPEAK_PROJECT_ROOT=$(pwd) python -m codespeak.cli plan "run prisma migrate dev name init force"`

## Next steps
- Hook into Realtime API for true speech input/output.
- Add VS Code extension surface.
- Harden normalization and diff workflow.
