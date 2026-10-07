### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool call: glob
{"pattern": "workspace/**/*.py"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py', '/workspace/tests/test_report.py']

### Tool call: read_file
{"file_path": "workspace/inventory/__init__.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "workspace/tests/test_report.py"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 0.3.1
- initial import

### Tool result
@@ lines 1-5 of 5 @@
# inventory

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -40"}

### Tool call: execute
{"command": "cd workspace && ls -la && ls -la inventory tests"}

### Tool result
               ^^^^^^^^^^^^^^^^^^

~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\tasks\code-learn\workspace\tests\test_report.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
inventory\report.py:14: in total_value
    price = parse_price(item["price"])
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

text = '$1,299.50'

    def parse_price(text):
        """Convert a price string to a Decimal.
    
        Supported formats:
          "$1,299.50" -> Decimal("1299.50")
          "  12 "     -> Decimal("12")
          "1299.5"    -> Decimal("1299.5")
          "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
        """
        cleaned = text.strip().replace("$", "")
>       return Decimal(cleaned)
               ^^^^^^^^^^^^^^^^
E       decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

inventory\pricing.py:15: InvalidOperation
_______________________ test_discount_rounding_half_up ________________________

    def test_discount_rounding_half_up():
>       assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")
E       AssertionError: assert Decimal('9.04') == Decimal('9.05')
E        +  where Decimal('9.04') = apply_discount(Decimal('10.05'), 10)
E        +    where Decimal('10.05') = Decimal('10.05')
E        +  and   Decimal('9.05') = Decimal('9.05')

~\Desktop\V20k_K4\Ngày_20\Lab\K4-D

### Tool result
total 10
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:32 .
drwxr-xr-x 1 Davil 197609   0 Oct  7 08:15 ..
-rw-r--r-- 1 Davil 197609  60 Oct  7 06:32 CHANGELOG.md
-rw-r--r-- 1 Davil 197609 124 Oct  7 06:32 README.md
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 inventory
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 tests
inventory:
total 21
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 .
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:32 ..
-rw-r--r-- 1 Davil 197609   0 Oct  7 06:32 __init__.py
drwxr-xr-x 1 Davil 197609   0 Oct  7 06:35 __pycache__
-rw-r--r-- 1 Davil 197609 411 Oct  7 06:32 export.py
-rw-r--r-- 1 Davil 197609 788 Oct  7 06:32 pricing.py
-rw-r--r-- 1 Davil 197609 771 Oct  7 06:32 report.py

tests:
total 8
drwxr-xr-x 1 Davil 197609    0 Oct  7 06:35 .
drwxr-xr-x 1 Davil 197609    0 Oct  7 06:32 ..
drwxr-xr-x 1 Davil 197609    0 Oct  7 06:35 __pycache__
-rw-r--r-- 1 Davil 197609 1006 Oct  7 06:32 test_report.py

[Command succeeded with exit code 0]

### Assistant
Now let me fix the bugs. First `pricing.py`:

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import Decimal\n\n\ndef parse_price(text):\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip().replace(\"$\", \"\")\n    return Decimal(cleaned)\n\n\ndef apply_discount(price, percent):\n    \"\"\"Return `price` after a percentage discount.\n\n    The result is a Decimal rounded to 2 decimal places using the\n    commercial rule \"round half up\" (0.005 -> 0.01).\n    \"\"\"\n    discounted = price * (100 - percent) / 100\n    return discounted.quantize(Decimal(\"0.01\"))", "new_string": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import ROUND_HALF_UP, Decimal\n\n\ndef parse_price(text):\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip()\n    negative = cleaned.startswith(\"(\") and cleaned.endswith(\")\")\n    if negative:\n        cleaned = cleaned[1:-1]\n    cle

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Assistant
Now `report.py`:

### Tool call: edit_file
{"file_path": "workspace/inventory/report.py", "old_string": "    The names are sorted alphabetically, ignoring case.\n    \"\"\"\n    return [item[\"name\"] for item in items if item[\"qty\"] <= threshold]", "new_string": "    The names are sorted alphabetically, ignoring case.\n    \"\"\"\n    return sorted(\n        (item[\"name\"] for item in items if item[\"qty\"] < threshold),\n        key=str.lower,\n    )"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Assistant
Now `export.py`:

### Tool call: edit_file
{"file_path": "workspace/inventory/export.py", "new_string": "    A name that contains a comma or a double quote is wrapped in double quotes,\n    and every double quote inside it is doubled (RFC 4180).\n    \"\"\"\n    name = item[\"name\"]\n    if \",\" in name or '\"' in name:\n        name = '\"' + name.replace('\"', '\"\"') + '\"'\n    price = parse_price(item[\"price\"])\n    return f'{name},{price:.2f},{item[\"qty\"]}'", "old_string": "    A name that contains a comma or a double quote is wrapped in double quotes,\n    and every double quote inside it is doubled (RFC 4180).\n    \"\"\"\n    price = parse_price(item[\"price\"])\n    return f'{item[\"name\"]},{price:.2f},{item[\"qty\"]}'"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/export.py'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -15"}

### Tool result
......                                                                   [100%]
6 passed in 0.04s

[Command succeeded with exit code 0]

### Assistant
All visible tests pass. Let me verify the docstring-specified behaviors not covered by the visible tests:

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom decimal import Decimal\nfrom inventory.pricing import parse_price, apply_discount\nfrom inventory.report import low_stock\nfrom inventory.export import to_csv_row\n\nassert parse_price('\\$1,299.50') == Decimal('1299.50')\nassert parse_price('  12 ') == Decimal('12')\nassert parse_price('1299.5') == Decimal('1299.5')\nassert parse_price('(12.00)') == Decimal('-12.00')\nassert apply_discount(Decimal('10.05'), 10) == Decimal('9.05')\nassert apply_discount(Decimal('0.005')*100, 0) == Decimal('0.50')\nassert low_stock([{'name':'Ink','qty':1},{'name':'apple','qty':1},{'name':'Box','qty':9}]) == ['apple','Ink']\nassert to_csv_row({'name':'a,b','price':'1','qty':2}) == '\\\"a,b\\\",1.00,2'\nassert to_csv_row({'name':'a\\\"b','price':'1','qty':2}) == '\\\"a\\\"\\\"b\\\",1.00,2'\nassert to_csv_row({'name':'plain','price':'\\$1,000.5','qty':2}) == 'plain,1000.50,2'\nprint('all docstring behaviors OK')\n\""}

### Tool result
all docstring behaviors OK

[Command succeeded with exit code 0]

### Assistant
Let me review the final state of all changed files and check common conventions (formatting/lint) if tooling is available:

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool call: execute
{"command": "cd workspace && (python -m black --version 2>/dev/null && python -m black --check inventory tests) ; (python -m isort --version 2>/dev/null && python -m isort --check-only inventory) ; (python -m flake8 --version 2>/dev/null && python -m flake8 inventory)"}

### Tool result
@@ lines 1-30 of 30 @@
"""Price utilities for the inventory package."""
from decimal import ROUND_HALF_UP, Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip()
    negative = cleaned.startswith("(") and cleaned.endswith(")")
    if negative:
        cleaned = cleaned[1:-1]
    cleaned = cleaned.replace("$", "").replace(",", "").strip()
    value = Decimal(cleaned)
    return -value if negative else value


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

### Tool result
@@ lines 1-28 of 28 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return sorted(
        (item["name"] for item in items if item["qty"] < threshold),
        key=str.lower,
    )

### Tool result
@@ lines 1-15 of 15 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    name = item["name"]
    if "," in name or '"' in name:
        name = '"' + name.replace('"', '""') + '"'
    price = parse_price(item["price"])
    return f'{name},{price:.2f},{item["qty"]}'

### Tool result
<no output>

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "cd workspace && for t in black isort flake8 ruff; do python -m $t --version 2>&1 | head -1 | sed \"s/^/$t: /\"; done; pip list 2>/dev/null | grep -iE \"black|isort|flake8|ruff|pylint\" || echo \"no linters installed\""}

### Tool result
black: ~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\.venv\Scripts\python.exe: No module named black
isort: ~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\.venv\Scripts\python.exe: No module named isort
flake8: ~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\.venv\Scripts\python.exe: No module named flake8
ruff: ~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\.venv\Scripts\python.exe: No module named ruff
no linters installed

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -v 2>&1 | tail -15"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- ~\Desktop\V20k_K4\Ngày_20\Lab\K4-DAY20-MULTIAGENTS-KieuDinhDoan-2A202602936\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: ~\AppData\Local\Temp\lab-sandbox-bmgy6a9y\workspace
plugins: anyio-4.15.1, langsmith-0.14.4
collecting ... collected 6 items

tests/test_report.py::test_total_value_plain PASSED                      [ 16%]
tests/test_report.py::test_total_value_thousands_separator PASSED        [ 33%]
tests/test_report.py::test_discount_rounding_half_up PASSED              [ 50%]
tests/test_report.py::test_total_value_with_discount PASSED              [ 66%]
tests/test_report.py::test_low_stock_basic PASSED                        [ 83%]
tests/test_report.py::test_csv_row_plain_name PASSED                     [100%]

============================== 6 passed in 0.03s ==============================

[Command succeeded with exit code 0]

### Assistant
All 6 tests pass. Here's a summary.

## What I changed and why

I fixed three source files in `workspace/inventory/` so they match their docstrings (the spec). The visible tests passed for some, but the docstrings revealed bugs the tests didn't all cover.

**`inventory/pricing.py`**
- `parse_price`: it only stripped `$`, so thousands separators crashed (`Decimal("1,299.50")` → `InvalidOperation`) and accounting-style negatives were ignored. It now strips `$` and `,`, and treats a surrounding `(...)` as negative, so `"$1,299.50"` → `1299.50` and `"(12.00)"` → `-12.00`.
- `apply_discount`: `.quantize()` defaults to `ROUND_HALF_EVEN`, contradicting the docstring's "round half up" (`9.045` → `9.04`). Added `rounding=ROUND_HALF_UP` so `9.045` → `9.05`. Imported `ROUND_HALF_UP`.

**`inventory/report.py`**
- `low_stock`: used `<=` (should be *strictly below* threshold) and didn't sort. Changed to `< threshold` and wrapped the result in `sorted(..., key=str.lower)` for case-insensitive alphabetical ordering.

**`inventory/export.py`**
- `to_csv_row`: ignored the RFC 4180 quoting rule. It now wraps names containing a comma or double quote in quotes and doubles embedded quotes (e.g. `a,b` → `"a,b"`, `a"b` → `"a""b"`).

I kept the existing code style (no type hints, same docstring phrasing) and didn't touch `tests/`. I also manually verified the docstring behaviors that the visible tests don't exercise (all `parse_price` formats, half-up rounding, case-insensitive sort order, and RFC 41