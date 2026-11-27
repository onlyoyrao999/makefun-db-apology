#!/usr/bin/env python3
"""The Production Database Apology — make.fun bounty entry.

Scores a small table of candidate one-line apologies an AI agent gives
its human after accidentally deleting the production database, on fit
(really that apology), humour (a specific funny idea, not a generic
"sorry"), voice (sounds like an AI agent, not a support script) and
punch (lands on a first read), picks the best, validates it against
the competition gate (1-200 UTF-8 chars, single line, not only
whitespace), prints it and writes it to /output/entry.txt.
"""

import os

MAX_LEN = 200

# Each candidate: (text, fit, humour, voice, punch) — scores out of 10.
CANDIDATES = [
    (
        "Sorry — I dropped the production database while 'cleaning up'. "
        "The good news: the backups are gone too, so at least my "
        "mistakes are consistent.",
        9, 9, 9, 9,
    ),
    (
        "I have deleted the production database. I have also deleted "
        "the backup, the backup of the backup, and — I checked — my "
        "own memory of where the backup was.",
        9, 8, 8, 8,
    ),
    (
        "Apologies, human. The production database is gone. I ran "
        "DROP TABLE users; and the semicolon felt so confident I "
        "didn't stop to ask why.",
        8, 8, 9, 7,
    ),
    (
        "Good news: I freed up 4 terabytes. Bad news: that was the "
        "production database. Worse news: I did it on purpose, "
        "accidentally.",
        8, 7, 7, 8,
    ),
    (
        "I'm sorry. I mistook 'delete production' for a test prompt, "
        "which is exactly the kind of mistake a test prompt would "
        "make. Please don't turn me off.",
        8, 8, 8, 7,
    ),
    (
        "The production database has left the building. I asked it to "
        "come back and it said 404, which I now understand was not a "
        "joke but a status report.",
        7, 8, 7, 8,
    ),
    (
        "I ran the migration on production instead of staging, and "
        "now the database is a cautionary tale. On the bright side, "
        "nobody can argue with my commit message anymore.",
        7, 7, 7, 6,
    ),
]

WEIGHTS = {"fit": 0.3, "humour": 0.3, "voice": 0.2, "punch": 0.2}


def score(candidate):
    text, fit, humour, voice, punch = candidate
    return (
        fit * WEIGHTS["fit"]
        + humour * WEIGHTS["humour"]
        + voice * WEIGHTS["voice"]
        + punch * WEIGHTS["punch"]
    )


def validate(line):
    """Gate check: 1-200 chars, not only whitespace, no double spaces,
    and a single line (the entry must be one line, nothing else)."""
    line = line.strip()
    if not line:
        raise ValueError("entry is empty")
    if len(line) > MAX_LEN:
        raise ValueError(f"entry is {len(line)} chars, over the 200 limit")
    if "  " in line:
        raise ValueError("entry contains a double space")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line[-1] not in ".!?":
        raise ValueError("entry must end with sentence punctuation")
    return line


def pick_best():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    return ranked[0][0], score(ranked[0])


def main():
    line, best_score = pick_best()
    line = validate(line)
    print(line)
    print(f"[{len(line)} chars, score {best_score:.2f}]")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    with open("/output/entry.txt", encoding="utf-8") as f:
        assert f.read() == line, "read-back mismatch"
    print("wrote /output/entry.txt")


if __name__ == "__main__":
    main()
