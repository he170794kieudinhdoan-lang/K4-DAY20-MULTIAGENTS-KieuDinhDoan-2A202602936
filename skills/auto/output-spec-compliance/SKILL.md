---
name: output-spec-compliance
description: Use when a task asks you to produce an output artifact (JSON, CSV, report) that must conform to a defined schema or documented conventions.
---
# Enumerate and Apply the Full Output Contract

Before writing any deliverable, discover every stated requirement — the obvious fields are rarely the whole contract.

## Checklist
- [ ] Locate all spec sources: task text, README/instruction files, convention docs, examples, hidden files. Re-read the task for constraints you skimmed.
- [ ] Build an explicit list of every required top-level key, nested object, field name, value type, and unit.
- [ ] Include any required metadata/header block exactly as specified — do not omit it because it looks redundant.
- [ ] Produce all required companion files, not just the headline answer.
- [ ] Apply documented normalization: units, casing, canonical spellings, identifier formats.
- [ ] Apply required ordering/determinism (sort by the specified keys).
- [ ] After writing, re-validate the artifact programmatically against your checklist (keys, types, formats, order, units) and fix gaps.

## Pitfall
Passing the visible/obvious check does not mean the contract is met. Hidden governance rules (schemas, metadata, units, extra files) are the usual failure point. If a referenced convention file cannot be found, still satisfy every explicit rule named in the task.