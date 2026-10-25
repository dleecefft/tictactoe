---
paths: ["tictactoe/**/*.py", "tests/**/*.py"]
---

# Review criteria

What an automated review of this repository reports, and what it leaves alone.

## Reportable categories

| Category | Report | Do not report |
|---|---|---|
| security | Untrusted or personal data reaching a log, a file path, a shell or a query | A dependency whose advisory you cannot see |
| correctness | A result that is wrong for an input the function accepts, or a docstring that claims behaviour the code does not have | A design you would have written differently |
| testing | A branch this change adds or alters that no test exercises | A module with fewer tests than you would like |
| convention | A documented convention in CLAUDE.md that this change does not follow | A convention you are inferring rather than reading |

Anything outside these four categories is not a finding here, however true it is.

## Severity, anchored

Severity is about the consequence, not about your confidence. Not being sure is a reason to
say nothing, not a reason to file the same finding one rung lower.

**high**: it loses data, corrupts a file, or puts something personal somewhere it does not
belong.

    Path(destination).write_text(line)     # write_text truncates, an append needs "a"

**medium**: it is wrong in a corner of the input space, or the code contradicts itself.

    # the docstring says "returns the winning mark or the string draw"
    return winner(board)           # returns None on a full board

**low**: it costs a reader a moment, or leaves a documented convention half done.

    print(f"wrote {path}")                 # printing from a module that is not cli.py

## Do not flag

These are conventions this repository has chosen, written down in CLAUDE.md. They are not
defects, and reporting them is the noise that gets a reviewer switched off.

- `place()` copying the board rather than mutating it and undoing the move. The copy is
  what lets the opponent search ahead, and it is cheap on nine cells.
- `lru_cache(maxsize=None)` on `_score`. The game tree is bounded and so is the cache.
- The absence of type annotations. This package does not use them.
- Anything a formatter would fix on its own.
- Anything you would phrase as "consider reviewing this logic". A finding carries a fix
  that could be applied as written.

## Temporarily disabled

None at present. A category whose findings are wrong more often than they are right is
listed here and stops being reported, rather than being tolerated, because its noise is
charged against every other category's credibility. Refine its rules with a reported and a
not-reported example, then put it back.

## The id on every finding

Give each finding an id of `category:path:symbol`, where the symbol is the enclosing
function, class or constant.

    correctness:tictactoe/cli.py:main

Not the line number. The line moves when anything above it changes, and a finding whose
identity moves is reported again as new on the next commit.

## On a rerun

When you are given the findings from an earlier commit, report only what is new in this
change or was reported before and is still unaddressed. Do not repeat a finding this change
resolved, and do not file the same defect twice.
