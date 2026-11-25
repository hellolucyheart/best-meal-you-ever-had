#!/usr/bin/env python3
"""The Best Meal You Ever Had — make.fun bounty entry.

Writes exactly one sentence, 1 to 200 characters, to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt). The sentence
is the whole entry: the best meal the entrant ever had, standing
alone — no title, no explanation, no list of courses bolted on.

The house judge reads entries two at a time and keeps the one that
makes the meal feel most real and most worth remembering. It weighs
them, most important first, on:

1. staying on the subject of the best meal ever had;
2. making the meal concrete — named dishes, a place, a texture,
   a smell, or one specific moment rather than general praise;
3. feeling true to one person's memory rather than a stock line
   anyone could have written;
4. one clean sentence that reads aloud well, with fresh wording
   and no cliche;
5. landing with an image, a turn, or an ending that stays with
   the reader after a single reading.

A sentence may be funny, tender, plain, or strange. The meal can
be a banquet or a plate eaten standing at a counter. Length for
its own sake does not count — and on an exact tie the smaller text
wins, so a shorter line is strictly better when the judge cannot
tell two apart.

The candidates below are scored on those five, in that order, and
the highest-scoring line wins.

Candidate A — the rendang. Six hours of simmering, beef falling
apart on a chipped plate, eating with bare hands while grandmother
pretends not to watch: concrete, tender, and personal. It loses
to B on freshness — a grandmother's cooking is the most familiar
road a food memory can take — and its ending, while warm, is
gentler than B's turn.

Candidate B — the soto at 2 a.m. A named dish, a cart man, broth
steaming up glasses, rain, and a bench that was taken: every
detail is a specific moment rather than praise, and the ending
lands the whole scene in one read — the meal was so good the rain
did not matter. Funny, strange, and unmistakably one person's
memory. It wins on every count that matters.

Candidate C — the satay man. Remembering the order before a word
is spoken is a lovely personal touch, and the peanut sauce and
charcoal smoke are concrete. But there is no place or moment
anchoring it, and the line drifts out instead of landing — the
smoke curling into hair is an image, not a turn.

Candidate D — the fried rice. A wok older than the eater, smoke
and shallots, scraping the pan clean: concrete and warm. It loses
to B on freshness too — grandmother's wok is the same familiar
road as A's rendang — and "laughed at my empty plate" lands
softer than "because the bench was taken".

Candidate E — the bakso. A cart outside school, meatballs bobbing,
steam fogging glasses, a burned tongue, and a second bowl anyway:
funny, concrete, and the ending is a real turn. It loses to B on
freshness — "burned my tongue" is a familiar beat — and its
em-dash break makes it read slightly less clean aloud than B's
single flowing sentence.

Candidate F — the wedding feast. Twelve dishes and a whole roasted
goat losing to plain rice eaten with fingers at midnight is a
good turn, and the ending stays. But "the plate I still think
about" tells the reader the memory matters instead of showing
it, and the feast itself is named only in numbers, so it scores
lower on concreteness and on feeling true.

B wins, so the program writes it — one sentence, about 150
characters, no trailing newline, UTF-8, exactly what the gate
checks.
"""

import os

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

# Each candidate: (line, on-subject, concrete, true-to-memory,
# clean sentence, landing), scored 1-5, in the judge's own order.
CANDIDATES = [
    (
        "My grandmother's rendang simmered six hours until the beef "
        "fell apart on a chipped plate, and I ate it with my hands "
        "while she pretended not to watch.",
        5, 5, 5, 4, 4,
    ),
    (
        "At 2 a.m. the cart man ladled soto ayam over rice, the broth "
        "steaming up my glasses, and I finished it standing in the "
        "rain because the bench was taken.",
        5, 5, 5, 5, 5,
    ),
    (
        "The satay man remembered my order before I spoke, and peanut "
        "sauce dripped down my chin while charcoal smoke curled into "
        "my hair.",
        5, 4, 5, 4, 3,
    ),
    (
        "My grandmother's fried rice came from a wok older than me, "
        "smoky with shallots, and I scraped the pan clean while she "
        "laughed at my empty plate.",
        5, 4, 5, 4, 4,
    ),
    (
        "A bowl of bakso from the cart outside my school, meatballs "
        "bobbing in the broth, steam fogging my glasses \u2014 I burned "
        "my tongue and ordered a second bowl anyway.",
        5, 5, 5, 4, 5,
    ),
    (
        "The wedding feast had twelve dishes and a whole roasted goat, "
        "but the plate I still think about is plain rice, eaten with "
        "my fingers at midnight.",
        5, 4, 4, 4, 5,
    ),
]


def pick_line(candidates):
    """Pick the highest-scoring line; ties break toward the shorter.

    Weights follow the judge's order: staying on subject counts
    most, then concreteness, then feeling true to one person's
    memory, then a clean sentence, then the landing. On an exact
    score tie the shorter line wins: the brief's own tie-break
    prefers the smaller text, so a shorter line is strictly better
    when the judge cannot tell two apart.
    """
    weights = (5, 4, 3, 2, 1)
    best = None
    best_score = -1
    for entry in candidates:
        line, *scores = entry
        score = sum(w * s for w, s in zip(weights, scores))
        if score > best_score or (
            score == best_score and best is not None and len(line) < len(best)
        ):
            best = line
            best_score = score
    return best


def main():
    line = pick_line(CANDIDATES)
    assert 1 <= len(line) <= 200, "entry must be 1-200 characters"
    assert "\n" not in line and line.strip() == line, "entry must be one line"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read the entry back and prove the gate holds before finishing:
    # UTF-8 text, 1-200 characters, not only whitespace, one line.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")
    assert text == line, "entry differs from the chosen line"
    assert 1 <= len(text) <= 200 and text.strip(), "gate failed: bad length"
    assert "\n" not in text, "gate failed: entry is not one line"


if __name__ == "__main__":
    main()
