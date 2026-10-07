### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
I'll start by exploring the workspace structure.

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
{"command": "cd workspace && ls -la && ls -la .. 2>/dev/null | head -50"}

### Tool call: glob
{"pattern": "**/*.{toml,cfg,ini,txt,md,json,yaml,yml}"}

### Tool result
total 6
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:32 .
drwxr-xr-x 1 Davil 197609   0 Oct  7 08:35 ..
-rw-r--r-- 1 Davil 197609  60 Oct  7 06:32 CHANGELOG.md
-rw-r--r-- 1 Davil 197609 123 Oct  7 06:32 README.md
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 bookings
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 tests
total 512
drwxr-xr-x 1 Davil 197609 0 Oct  7 08:35 .
drwxr-xr-x 1 Davil 197609 0 Oct  7 08:35 ..
drwxr-xr-x 1 Davil 197609 0 Oct  7 06:32 workspace

[Command succeeded with exit code 0]

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md']

### Tool call: execute
{"command": "cd workspace && python --version && python -m pytest tests -q 2>&1 | tail -20"}

### Tool result
Python 3.11.9
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

~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\tasks\code-eval\workspace\tests\test_bookings.py:10: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_bookings.py::test_total_minutes_mixed_formats - ValueError:...
FAILED tests/test_bookings.py::test_billable_blocks_rounds_up - assert 1 == 2
2 failed, 1 passed in 0.43s

[Command succeeded with exit code 0]

### Assistant
Now let me fix the three source files.

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n_HOURS_MINUTES_RE = re.compile(r\"(\\d+)h(\\d+)m\")\n_HOURS_RE = re.compile(r\"(\\d+)h\")\n_MINUTES_RE = re.compile(r\"(\\d+)m\")\n_CLOCK_RE = re.compile(r\"(\\d+):(\\d+)\")\n_PLAIN_MINUTES_RE = re.compile(r\"(\\d+)\")\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    value = text.strip()\n\n    match = _HOURS_MINUTES_RE.fullmatch(value)\n    if match:\n        return int(match.group(1)) * 60 + int(match.group(2))\n\n    match = _HOURS_RE.fullmatch(value)\n    if match:\n        return int(match.group(1)) * 60\n\n    match = _MINUTES_RE.fullmatch(value)\n    if match:\n        return int(match.group(1))\n\n    match = _CLOCK_RE.fullmatch(value)\n    if match:\n        return int(match.group(1)) * 60 + int(match.group(2))\n\n    match = _PLAIN_MINUTES_RE.fullmatch(value)\n    if match:\n        return int(match.group(1))\n\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool call: write_file
{"file_path": "workspace/bookings/billing.py", "content": "\"\"\"Billing rules.\"\"\"\nimport math\n\n\ndef billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    return math.ceil(minutes / block)\n"}

### Tool call: write_file
{"file_path": "workspace/bookings/schedule.py", "content": "\"\"\"Schedule helpers.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations):\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return [*(slots or []), slot]\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool result
Updated file /workspace/bookings/billing.py

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5 && python - <<'EOF'\nfrom bookings.timeutil import parse_duration\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\n\ncases = {\"1h30m\":90,\"2h\":120,\"45m\":45,\"1:30\":90,\"45\":45,\"  2h  \":120,\"0\":0,\"10h5m\":605,\"1:05\":65}\nfor k,v in cases.items():\n    got = parse_duration(k)\n    assert got == v, (k, got, v)\nfor bad in [\"\", \"abc\", \"1h30\", \"h30\", \"1.5h\", \"1:2:3\", \"-5m\", \"1 2\"]:\n    try:\n        parse_duration(bad)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(f\"expected ValueError for {bad!r}\")\nprint(\"parse_duration ok\")\n\nassert add_slot(\"a\") == [\"a\"]\nassert add_slot(\"b\") == [\"b\"]\nassert add_slot(\"c\", [\"a\",\"b\"]) == [\"a\",\"b\",\"c\"]\nbase = [\"x\"]\nout = add_slot(\"y\", base)\nassert out == [\"x\",\"y\"] and base == [\"x\"], (out, base)\nassert add_slot(\"a\") == [\"a\"]\nprint(\"add_slot ok\")\n\nassert billable_blocks(20) == 2 and billable_blocks(45) == 3\nassert billable_blocks(0) == 0\nassert billable_blocks(15) == 1\nassert billable_blocks(16) == 2\nassert billable_blocks(30, 30) == 1\nassert billable_blocks(31, 30) == 2\nfor bad in (-1, -100):\n    try:\n        billable_blocks(bad)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(\"expected ValueError\")\nprint(\"billable_blocks ok\")

### Tool result
...                                                                      [100%]
3 passed in 0.04s
parse_duration ok
add_slot ok
billable_blocks ok
all docstring checks ok

[Command succeeded with exit code 0]

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "old_string": "    return [*(slots or []), slot]", "new_string": "    if slots is None:\n        slots = []\n    return [*slots, slot]"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- Fix `parse_duration` to accept all documented formats (\"1h30m\", \"2h\", \"45m\", \"1:30\", \"45\").\n- Fix `add_slot` so calls no longer share state and the input list is left untouched.\n- Fix `billable_blocks` to always round up and to reject negative minutes.\n"}

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -3 && (python -m flake8 bookings 2>&1 | head -20; python -m pycodestyle bookings 2>&1 | head -20) "}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool result
...                                                                      [100%]
3 passed in 0.03s
~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\.venv\Scripts\python.exe: No module named flake8
~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\.venv\Scripts\python.exe: No module named pycodestyle

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python - <<'EOF'\nfrom bookings.schedule import add_slot\nassert add_slot(\"a\") == [\"a\"] and add_slot(\"b\") == [\"b\"]\nbase = [\"x\"]; assert add_slot(\"y\", base) == [\"x\",\"y\"] and base == [\"x\"]\nassert add_slot(\"c\", [\"a\",\"b\"]) == [\"a\",\"b\",\"c\"]\nprint(\"ok\")\nEOF"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
ok

[Command succeeded with exit code 0]

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

### Assistant
The whole suite passes (`3 passed`) and my extra spec-derived checks (all documented duration formats, negative/edge cases, no shared or mutated state) pass too.

Changes made:

- **`bookings/timeutil.py`** — `parse_duration` only handled `"1h30m"`. It now accepts every documented format via anchored full-match patterns: `"1h30m"`, `"2h"`, `"45m"`, `"1:30"` (h:mm) and bare minutes `"45"`, after stripping surrounding whitespace, and still raises `ValueError` for anything else (e.g. `""`, `"abc"`, `"1h30"`, `"-5m"`).
- **`bookings/schedule.py`** — `add_slot` used a mutable default (`slots=[]`), so calls shared state and it mutated the caller's list. It now takes `slots=None`, builds a fresh list, and returns a new list without touching the input.
- **`bookings/billing.py`** — `billable_blocks` used `round()` (so 20 min → 1 block, and 20 vs 45 were banker's-rounded). It now rounds up with `math.ceil`, matching the "partial block billed as a full block" rule, and raises `ValueError` for negative `minutes` as the docstring specifies.
- **`CHANGELOG.md`** — added entries under `## Unreleased` describing the three fixes.

No files in `tests/` were touched.