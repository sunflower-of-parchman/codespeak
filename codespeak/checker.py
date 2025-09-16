"""Lightweight checker that cleans raw voice transcripts before planning."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .project_index import ProjectIndex

_COMMON_DEV = {
    "nuxt",
    "next",
    "vite",
    "prisma",
    "eslint",
    "prettier",
    "vitest",
    "jest",
    "webpack",
    "tsconfig",
    "pnpm",
    "yarn",
    "npm",
    "tsx",
    "typescript",
    "node",
}

_CODE_LIKE = re.compile(r"^[-/_.a-zA-Z0-9]+$")


@dataclass
class Edit:
    src: str
    dst: str
    reason: str
    confidence: float

    def dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass
class CheckResult:
    original: str
    cleaned: str
    edits: List[Edit]
    needs_clarification: bool
    clarifier: Optional[str]

    def dict(self) -> Dict[str, object]:
        return {
            "original": self.original,
            "cleaned": self.cleaned,
            "edits": [edit.dict() for edit in self.edits],
            "needs_clarification": self.needs_clarification,
            "clarifier": self.clarifier,
        }


def _read_pkg_deps(root: Path) -> List[str]:
    pkg = root / "package.json"
    if not pkg.exists():
        return []
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except Exception:
        return []
    deps: List[str] = []
    for key in ("dependencies", "devDependencies"):
        section = data.get(key) or {}
        if isinstance(section, dict):
            deps.extend(section.keys())
    return [dep.lower() for dep in deps]


def _build_lexicon(index: ProjectIndex) -> Tuple[List[str], set[str]]:
    tokens = set(_COMMON_DEV)
    repo_tokens: set[str] = set()
    for file_path in index.files:
        for token in re.split(r"[^a-zA-Z0-9_.-]+", file_path.lower()):
            if len(token) >= 2:
                repo_tokens.add(token)
                tokens.add(token)
    deps = set(_read_pkg_deps(Path(index.root)))
    repo_tokens.update(deps)
    tokens.update(deps)
    return sorted(tokens), repo_tokens


MATCH_THRESHOLD = 0.74


def _best_two(token: str, lexicon: List[str]) -> Tuple[str, float, Optional[str], float]:
    best, best_score = token, 0.0
    second, second_score = None, 0.0
    lowered = token.lower()
    for candidate in lexicon:
        score = SequenceMatcher(None, lowered, candidate).ratio()
        if score > best_score:
            second, second_score = best, best_score
            best, best_score = candidate, score
        elif score > second_score:
            second, second_score = candidate, score
    return best, best_score, second, second_score


def _pre_rules(words: List[str]) -> List[str]:
    rewritten: List[str] = []
    index = 0
    while index < len(words):
        current = words[index].lower()
        if (
            index + 1 < len(words)
            and current in {"dash", "minus"}
            and words[index + 1].lower() in {"dash", "minus"}
        ):
            rewritten.append("--")
            index += 2
            continue
        if current == "slash":
            rewritten.append("/")
            index += 1
            continue
        rewritten.append(words[index])
        index += 1
    return rewritten


_COMMON_FIXES = {
    "grammer": "grammar",
    "chexked": "checked",
    "cann't": "can't",
    "wanna": "want to",
}


def normalize_utterance(text: str, index: ProjectIndex) -> CheckResult:
    original = text
    words = text.strip().split()
    words = _pre_rules(words)

    lexicon, repo_tokens = _build_lexicon(index)
    lexicon_set = set(lexicon)

    cleaned_words: List[str] = []
    edits: List[Edit] = []
    needs_clarification = False
    clarifier: Optional[str] = None

    for word in words:
        lowered = word.lower()
        if (_CODE_LIKE.match(word) and not word.isalpha()) or lowered in lexicon_set:
            cleaned_words.append(word)
            continue

        if lowered in _COMMON_FIXES:
            replacement = _COMMON_FIXES[lowered]
            cleaned_words.append(replacement)
            edits.append(
                Edit(src=word, dst=replacement, reason="common_fix", confidence=0.99)
            )
            continue

        best, best_score, second, second_score = _best_two(lowered, lexicon)
        if best_score >= MATCH_THRESHOLD and best != lowered:
            if best in _COMMON_DEV and best not in repo_tokens:
                cleaned_words.append(word)
                continue
            if second and second_score >= MATCH_THRESHOLD and (best_score - second_score) < 0.02:
                needs_clarification = True
                clarifier = f"Did you mean {best} or {second}?"
                cleaned_words.append(word)
            else:
                cleaned_words.append(best)
                edits.append(
                    Edit(
                        src=word,
                        dst=best,
                        reason="repo_lexicon_match",
                        confidence=round(best_score, 3),
                    )
                )
        else:
            cleaned_words.append(word)

    cleaned = " ".join(cleaned_words)
    return CheckResult(
        original=original,
        cleaned=cleaned,
        edits=edits,
        needs_clarification=needs_clarification,
        clarifier=clarifier,
    )
