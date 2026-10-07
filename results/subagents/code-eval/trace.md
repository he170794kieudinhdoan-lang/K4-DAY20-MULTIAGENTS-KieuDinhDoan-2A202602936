### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
I'll start by exploring the workspace to understand the structure.

### Tool call: ls
{"path": "workspace"}

### Tool call: glob
{"pattern": "workspace/**/*.py"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py"}

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: execute
{"command": "cd workspace && ls -la && ls -la bookings tests && python -m pytest tests -q 2>&1 | tail -20"}

### Tool call: glob
{"pattern": "workspace/**/*"}

### Tool result
total 6
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:32 .
drwxr-xr-x 1 Davil 197609   0 Oct  7 08:37 ..
-rw-r--r-- 1 Davil 197609  60 Oct  7 06:32 CHANGELOG.md
-rw-r--r-- 1 Davil 197609 123 Oct  7 06:32 README.md
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 bookings
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 tests
bookings:
total 13
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 .
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:32 ..
-rw-r--r-- 1 Davil 197609  23 Oct  7 06:32 __init__.py
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 __pycache__
-rw-r--r-- 1 Davil 197609 344 Oct  7 06:32 billing.py
-rw-r--r-- 1 Davil 197609 218 Oct  7 06:32 calendar_export.py
-rw-r--r-- 1 Davil 197609 484 Oct  7 06:32 schedule.py
-rw-r--r-- 1 Davil 197609 532 Oct  7 06:32 timeutil.py

tests:
total 1
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 .
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:32 ..
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 __pycache__
-rw-r--r-- 1 Davil 197609 386 Oct  7 06:32 test_bookings.py
        Surrounding whitespace is ignored.
        """
        m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
        if not m:
>           raise ValueError(f"bad duration: {text!r}")
E           ValueError: bad duration: '2h'

bookings\timeutil.py:18: ValueError
_______________________ test_billable_blocks_rounds_up ________________________

    def test_billable_blocks_rounds_up():
>       assert billable_blocks(20) == 2
E       assert 1 == 2
E        +  where 1 = billable_blocks(20)

~\Desktop\V20k_K4\Ngày_20\Lab\

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-311.pyc', '/workspace/bookings/__pycache__/billing.cpython-311.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-311.pyc', '/workspace/bookings/__pycache__/schedule.cpython-311.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-311.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-311-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: execute
{"command": "ls -la . ; ls -la .. 2>/dev/null | head -30"}

### Tool result
total 516
drwxr-xr-x 1 Davil 197609 0 Oct  7 08:37 .
drwxr-xr-x 1 Davil 197609 0 Oct  7 08:38 ..
drwxr-xr-x 1 Davil 197609 0 Oct  7 08:38 workspace
total 207266
drwxr-xr-x 1 Davil 197609        0 Oct  7 08:38 .
drwxr-xr-x 1 Davil 197609        0 Sep  2 17:53 ..
drwxr-xr-x 1 Davil 197609        0 Sep 23 10:48 .opera
-rw-r--r-- 1 Davil 197609       53 Oct  7 00:32 .ses
-rw-r--r-- 1 Davil 197609  4353263 Oct  7 06:01 014b9564-2364-4ff3-a64c-310370471b78.tmp
-rw-r--r-- 1 Davil 197609   161196 Sep 19 02:33 03a9a814-831e-4102-a8e1-2af06c9d48a4.tmp
-rw-r--r-- 1 Davil 197609  2127654 Oct  4 20:58 0796cf7b-7a49-457a-ae90-9097559b4a97.tmp.ico
-rw-r--r-- 1 Davil 197609   161196 Sep 19 10:45 0d23a1ca-8ced-4cd8-93f5-02db649507c3.tmp
-rw-r--r-- 1 Davil 197609    45247 Oct  7 04:11 0da6b64e-a7d9-40e0-95a4-bece7141bd0e.png
-rw-r--r-- 1 Davil 197609        0 Oct  7 08:37 0dd4dc2d-de40-4813-b0d5-c8f4fb214df6.tmp
-rw-r--r-- 1 Davil 197609   516133 Oct  7 06:21 0e94b06d-d0cd-4aba-908e-52b9f4906845.tmp
-rw-r--r-- 1 Davil 197609        0 Oct  3 01:34 0ed20a08-8a79-4cfb-8ed4-d6b2ce42953b.tmp
-rw-r--r-- 1 Davil 197609     1630 Oct  7 06:07 0f057874-0136-487a-94a3-3191343eb1c0.tmp
-rw-r--r-- 1 Davil 197609   161196 Sep 18 10:01 0f1cbcd0-c4d8-46e8-8a56-3824ff3a32bd.tmp
-rw-r--r-- 1 Davil 197609   828908 Oct  7 08:17 0fd9e578-0b70-48d4-a613-1fab5ce475d6.tmp
-rw-r--r-- 1 Davil 197609   248531 Sep 19 10:46 11b269b4-0e70-41c8-9e14-b0da0ba6febd.tmp
-rw-r--r-- 1 Davil 197609   161196 Sep 19 02:34 12a0db13-1

### Assistant
Now I understand the bugs. Let me fix the three problematic modules.

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n# Accepted duration formats:\n#   \"1h30m\" -> hours and minutes\n#   \"2h\"    -> hours only\n#   \"45m\"   -> minutes only\n#   \"1:30\"  -> hours:minutes\n#   \"45\"    -> bare number, meaning minutes\n_DURATION_RE = re.compile(\n    r\"(?:(?P<hours>\\d+)h(?:(?P<minutes>\\d+)m)?\"\n    r\"|(?P<only_minutes>\\d+)m\"\n    r\"|(?P<clock_hours>\\d+):(?P<clock_minutes>\\d+)\"\n    r\"|(?P<bare_minutes>\\d+))\"\n)\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    if not isinstance(text, str):\n        raise ValueError(f\"bad duration: {text!r}\")\n    match = _DURATION_RE.fullmatch(text.strip())\n    if match is None:\n        raise ValueError(f\"bad duration: {text!r}\")\n    hours = match[\"hours\"] or match[\"clock_hours\"] or 0\n    minutes = (\n        match[\"minutes\"]\n        or match[\"only_minutes\"]\n        or match[\"clock_minutes\"]\n        or match[\"bare_minutes\"]\n        or 0\n    )\n    return int(hours) * 60 + int(minutes)\n"}

### Tool call: write_file
{"file_path": "workspace/bookings/billing.py", "content": "\"\"\"Billing rules.\"\"\"\nimport math\n\n\ndef billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    if block <= 0:\n        raise ValueError(f\"block must be > 0, got {block!r}\")\n    return math.ceil(minutes / block)\n"}

### Tool call: write_file
{"file_path": "workspace/bookings/schedule.py", "content": "\"\"\"Schedule helpers.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations):\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        slots = []\n    return [*slots, slot]\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool result
Updated file /workspace/bookings/billing.py

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- `parse_duration` now supports every documented format (\"1h30m\", \"2h\", \"45m\", \"1:30\", \"45\") and still rejects invalid input with `ValueError`.\n- `billable_blocks` rounds up to a full block and raises `ValueError` for negative minutes.\n- `add_slot` no longer shares state between calls and never mutates the list it is given.\n"}

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool result
...                                                                      [100%]
3 passed in 0.02s

[Command succeeded with exit code 0]

### Tool call: task
{"description": "Independently review the fixed `bookings` package in the sandbox folder `workspace/` (relative to the sandbox root; do NOT modify any files). Task context: the test suite of this package was failing; I fixed the source in `workspace/bookings/timeutil.py`, `workspace/bookings/billing.py`, `workspace/bookings/schedule.py` and added a CHANGELOG entry in `workspace/CHANGELOG.md`. `workspace/tests/test_bookings.py` must not be modified, and hidden tests will exercise edge cases described only by the docstrings.\n\nThe docstrings are the specification:\n- `bookings.timeutil.parse_duration(text)`: convert a duration string to whole minutes (int). Formats: \"1h30m\"->90, \"2h\"->120, \"45m\"->45, \"1:30\"->90, \"45\"->45 (bare number = minutes). Surrounding whitespace ignored. Invalid input must raise ValueError.\n- `bookings.schedule.total_minutes(durations)`: total minutes of a list of duration strings.\n- `bookings.schedule.add_slot(slot, slots=[])`: return a NEW list containing the given slots plus `slot`; separate calls must not share state (add_slot(\"a\") then add_slot(\"b\") -> [\"a\"] then [\"b\"]).\n- `bookings.billing.billable_blocks(minutes, block=15)`: number of billable blocks, always rounding UP (16 min / 15 -> 2 blocks); minutes must be >= 0, negative raises ValueError.\n- `bookings.calendar_export.slot_end(start_minute, duration_text)`: minute of the day at which a slot ends = start +/- parsed duration.\n\nPlease do all of the following and report re

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom bookings.timeutil import parse_duration\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.calendar_export import slot_end\nprint([parse_duration(t) for t in ['1h30m','2h','45m','1:30','45',' 1h30m ','0m','0h0m']])\nprint(total_minutes(['1h30m','2h','45','1:30']), total_minutes([]))\nprint(add_slot('a'), add_slot('b'), add_slot('a'))\nb=['x']; r=add_slot('y', b); print(r, b, r is b, add_slot('y',()))\nprint([billable_blocks(m) for m in (0,1,15,16,20,45,100)])\nfor bad in ['', 'abc', '1h30', '1:30:00', '1h 30m', '-5']:\n    try:\n        parse_duration(bad); print('NO RAISE', repr(bad))\n    except ValueError: pass\ntry: parse_duration(None); print('NO RAISE None')\nexcept ValueError: pass\ntry: billable_blocks(-1); print('NO RAISE -1')\nexcept ValueError: pass\ntry: billable_blocks(10, 0); print('NO RAISE block0')\nexcept ValueError: pass\nprint(slot_end(600,'1h30m'), slot_end(0,'45'))\n\""}

### Tool result
Verification complete. Here is my independent review report.

## 1. Test suite result

```
$ cd workspace && python -m pytest tests -q
...                                                                      [100%]
3 passed in 0.05s
```
Exit code 0 — all 3 visible tests pass.

## 2. Line-by-line review vs docstrings

I read every source file and re-checked each function against its spec. **No deviation from any docstring was found.**

| Function | File:lines | Verdict |
|---|---|---|
| `parse_duration` | `bookings/timeutil.py:18-42` | ✅ Matches. `fullmatch` on `text.strip()` enforces whole-string match, so all 5 formats work and everything else (including `"1h30"`, `"1:30:00"`, `"1h 30m"`) raises `ValueError`. Zero components handled (`"0h0m"`→0). |
| `total_minutes` | `bookings/schedule.py:5-7` | ✅ Matches. Returns `int`; `[]`→0. |
| `add_slot` | `bookings/schedule.py:10-18` | ✅ Matches. Uses `slots=None` sentinel (safer than the `[]` in the task text) then `[*slots, slot]` → always a fresh list, never mutates input, no cross-call state. |
| `billable_blocks` | `bookings/billing.py:5-16` | ✅ Matches. `math.ceil(minutes/block)` rounds up; `minutes < 0` raises `ValueError`. |
| `slot_end` | `bookings/calendar_export.py:5-7` | ✅ Matches. `start + parse_duration(...)`. |

Two **defensive extras** (not deviations, no documented case affected):
- `timeutil.py:29-30` — non-`str` input raises `ValueError` (spec only says "invalid input must raise `ValueError`", so this is consistent

### Tool result
[90, 120, 45, 90, 45, 90, 0, 0]
345 0
['a'] ['b'] ['a']
['x', 'y'] ['x'] False ['y']
[0, 1, 1, 2, 2, 3, 7]
690 45

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "ls -la tmp 2>/dev/null"}

### Tool result
total 8
drwxr-xr-x 1 Davil 197609    0 Oct  7 08:39 .
drwxr-xr-x 1 Davil 197609    0 Oct  7 08:38 ..
-rw-r--r-- 1 Davil 197609 3192 Oct  7 08:38 check_bookings.py
-rw-r--r-- 1 Davil 197609 2011 Oct  7 08:39 extra.py

[Command succeeded with exit code 0]

### Tool call: delete
{"file_path": "tmp"}

### Tool result
Deleted /tmp

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -3 && ls -la . && ls"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool result
...                                                                      [100%]
3 passed in 0.01s
total 10
drwxr-xr-x 1 Davil 197609   0 Oct  7 08:38 .
drwxr-xr-x 1 Davil 197609   0 Oct  7 08:39 ..
drwxr-xr-x 1 Davil 197609   0 Oct  7 08:38 .pytest_cache
-rw-r--r-- 1 Davil 197609 380 Oct  7 08:38 CHANGELOG.md
-rw-r--r-- 1 Davil 197609 123 Oct  7 06:32 README.md
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 bookings
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 tests
CHANGELOG.md
README.md
bookings
tests

[Command succeeded with exit code 0]

### Tool result
@@ lines 1-9 of 9 @@
# Changelog

## Unreleased
- `parse_duration` now supports every documented format ("1h30m", "2h", "45m", "1:30", "45") and still rejects invalid input with `ValueError`.
- `billable_blocks` rounds up to a full block and raises `ValueError` for negative minutes.
- `add_slot` no longer shares state between calls and never mutates the list it is given.

## 1.4.2
- initial import

### Tool call: delete
{"file_path": "workspace/.pytest_cache"}

### Tool result
Deleted /workspace/.pytest_cache

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool result
@@ lines 1-42 of 42 @@
"""Time helpers for the bookings package."""
import re

# Accepted duration formats:
#   "1h30m" -> hours and minutes
#   "2h"    -> hours only
#   "45m"   -> minutes only
#   "1:30"  -> hours:minutes
#   "45"    -> bare number, meaning minutes
_DURATION_RE = re.compile(
    r"(?:(?P<hours>\d+)h(?:(?P<minutes>\d+)m)?"
    r"|(?P<only_minutes>\d+)m"
    r"|(?P<clock_hours>\d+):(?P<clock_minutes>\d+)"
    r"|(?P<bare_minutes>\d+))"
)


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    if not isinstance(text, str):
        raise ValueError(f"bad duration: {text!r}")
    match = _DURATION_RE.fullmatch(text.strip())
    if match is None:
        raise ValueError(f"bad duration: {text!r}")
    hours = match["hours"] or match["clock_hours"] or 0
    minutes = (
        match["minutes"]
        or match["only_minutes"]
        or match["clock_minutes"]
        or match["bare_minutes"]
        or 0
    )
    return int(hours) * 60 + int(minutes)

### Tool result
@@ lines 1-18 of 18 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=None):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    if slots is None:
        slots = []
    return [*slots, slot]

### Tool result
@@ lines 1-16 of 16 @@
"""Billing rules."""
import math


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    if minutes < 0:
        raise ValueError(f"minutes must be >= 0, got {minutes!r}")
    if block <= 0:
        raise ValueError(f"block must be > 0, got {block!r}")
    return math.ceil(minutes / block)

### Assistant
All fixed and verified. Summary of changes:

**`workspace/bookings/timeutil.py`** — `parse_duration` only handled `"1h30m"`, so `"2h"`, `"45m"`, `"1:30"` and `"45"` all raised `ValueError`. Replaced the single regex with one documented-format regex (module-level compiled constant, named groups) that accepts all five formats, ignores surrounding whitespace, and still raises `ValueError` on anything else.

**`workspace/bookings/billing.py`** — `billable_blocks` used `round()`, which rounds to nearest (20 min → 1 block). Changed to `math.ceil` so partial blocks always round up, added the documented `ValueError` for negative `minutes`, plus a guard for a non-positive `block` (avoids an internal `ZeroDivisionError`).

**`workspace/bookings/schedule.py`** — `add_slot` had a mutable default (`slots=[]`), so calls shared state and mutated the caller's list. Now uses `None` as the sentinel and returns a fresh list (`[*slots, slot]`), so separate calls never share state and the passed-in list is untouched.

**`workspace/CHANGELOG.md`** — added entries under `## Unreleased` describing the three fixes.

`workspace/bookings/calendar_export.py` and everything in `workspace/tests/` were left unchanged. `python -m pytest tests -q` → **3 passed**; an independent review of all docstring-specified behaviour plus 70+ edge cases (whitespace, zero values, invalid inputs, no shared/mutated state, block rounding boundaries) passed with no deviations.