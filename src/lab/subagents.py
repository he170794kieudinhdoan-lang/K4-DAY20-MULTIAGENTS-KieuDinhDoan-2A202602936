"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use to explore the workspace, inspect files, check logs, "
                "read docstrings, data schemas, or documentation. Do not modify files."
            ),
            "system_prompt": (
                "You are an exploratory research assistant. Your task is to read and investigate "
                "files, directory structures, schemas, and logs. Report factual findings clearly "
                "and do not make changes to any files."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use to perform concrete code or data modifications, execute Python scripts, "
                "and run tests. Report exact execution outputs and changes made."
            ),
            "system_prompt": (
                "You are an implementation assistant. Your task is to write or edit code/data files "
                "carefully according to instructions, run execution commands or tests, and report results."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use to independently review modified files, verify edge cases against specifications, "
                "and ensure tests pass. Do not modify files."
            ),
            "system_prompt": (
                "You are an independent reviewer. Verify outputs and code against the task requirements, "
                "check edge cases, and run tests without modifying any files."
            ),
        },
    ]
