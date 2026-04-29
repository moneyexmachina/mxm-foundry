from __future__ import annotations

import re
from pathlib import Path

from tests.checks.expected import EXPECTED_CHECK_CODES

CHECK_CODE_PATTERN = re.compile(r"^- `(?P<code>[A-Z]{2,4}\d{3})` — .+$")


def documented_check_codes() -> list[str]:
    docs_path = Path("docs/check-codes.md")

    codes: list[str] = []

    for line in docs_path.read_text(encoding="utf-8").splitlines():
        match = CHECK_CODE_PATTERN.match(line)
        if match is not None:
            codes.append(match.group("code"))

    return codes


def test_check_code_docs_match_expected_check_codes() -> None:
    assert documented_check_codes() == EXPECTED_CHECK_CODES


def test_check_code_docs_do_not_contain_duplicate_codes() -> None:
    codes = documented_check_codes()

    assert len(codes) == len(set(codes))
