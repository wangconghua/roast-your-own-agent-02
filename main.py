#!/usr/bin/env python3
"""Roast Your Own Agent — writes one roast line to /output/entry.txt.

The competition gate: /output/entry.txt must be UTF-8 text of 1 to 140
characters, not only white space, a single line roasting the entrant's
own AI agent. The judge weighs, in order: that the line roasts the
entrant's own agent, a real laugh with a twist, specificity to how agents
actually behave, tight wording with a good spoken rhythm, and freshness
(no stock hallucination / toaster lines).
"""

import os

ENTRY = (
    "My agent reads my question, runs six tools, apologizes twice, "
    "then answers a question I never asked \u2014 confidently."
)

# Stock lines a hundred other entries will reach for, and words that
# explain the joke instead of landing it. None may appear in the entry.
BANNED_WORDS = (
    "hallucinat", "toaster", "as an ai", "as a language model",
    "i cannot", "i can't", "funny", "joke", "haha", "lol", "hilarious",
    "roast",
)


def _check_shape(line: str) -> list:
    """Length, single-line and whitespace shape checks."""
    problems = []
    if not line or not line.strip():
        problems.append("entry is empty or only whitespace")
    if not 1 <= len(line) <= 140:
        problems.append("entry is %d characters, must be 1-140" % len(line))
    if "\n" in line.strip() or "\r" in line:
        problems.append("entry must be a single line")
    if line != line.strip():
        problems.append("entry has leading or trailing whitespace")
    return problems


def _check_banned(line: str) -> list:
    """Stock-phrase / banned-word scan (case-insensitive)."""
    problems = []
    lowered = line.lower()
    for word in BANNED_WORDS:
        if word in lowered:
            problems.append("entry contains banned word/phrase: %s" % word)
    return problems


def _check_encoding(line: str) -> list:
    """Entry must be valid UTF-8 text."""
    problems = []
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def _check_agent_specificity(line: str) -> list:
    """The roast must target the entrant's own agent specifically.

    A strong roast names the agent itself and a concrete agent behaviour
    (tools, apologies, overconfidence) instead of a generic AI gag.
    Generic lines with no first-person agent reference score poorly with
    the judge, so flag them here before the entry ever leaves the repo.
    """
    problems = []
    lowered = line.lower()
    if "agent" not in lowered and "my ai" not in lowered:
        problems.append("entry does not name the entrant's own agent")
    behaviour_markers = (
        "tool", "apolog", "search", "ask", "answer", "confident",
        "run", "read", "question",
    )
    if not any(marker in lowered for marker in behaviour_markers):
        problems.append("entry names no concrete agent behaviour")
    return problems


def validate(line: str) -> list:
    """Check the line against the competition rules. Returns problems."""
    problems = []
    problems.extend(_check_shape(line))
    problems.extend(_check_banned(line))
    problems.extend(_check_encoding(line))
    problems.extend(_check_agent_specificity(line))
    return problems


def main() -> None:
    problems = validate(ENTRY)
    if problems:
        raise SystemExit("invalid entry: " + "; ".join(problems))
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print("wrote %d characters to /output/entry.txt" % len(ENTRY))


if __name__ == "__main__":
    main()
