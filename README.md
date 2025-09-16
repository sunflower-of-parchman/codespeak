# codespeak

Repo-aware voice agent MVP.

## What it does
Takes noisy developer utterances and produces a Plan: intent, resolved entities, and a safe command or diff. Uses repo context (files, packages, scripts) for accuracy.

## Quick start
1. `cp .env.example .env` and set `OPENAI_API_KEY`.
2. `pip install -e .`
3. From a repo:  
   `CODESPEAK_PROJECT_ROOT=$(pwd) python -m codespeak.cli plan "run prisma migrate dev name init force"`

## Next steps
- Hook into Realtime API for true speech input/output.
- Add VS Code extension surface.
- Harden normalization and diff workflow.
