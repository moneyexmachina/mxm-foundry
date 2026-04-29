from __future__ import annotations

from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch

from mxm.foundry.checks.predicates import license
from mxm.foundry.checks.predicates.golden import load_text
from mxm.foundry.checks.predicates.license import (
    LICENSE_CHECKS,
    check_license_matches_canonical,
)


def canonical_license() -> str:
    policy_text, error = load_text(license.POLICY_LICENSE_PATH)

    assert policy_text is not None, error

    return policy_text


def test_license_check_passes_when_project_matches_canonical(
    tmp_path: Path,
) -> None:
    (tmp_path / "LICENSE").write_text(canonical_license(), encoding="utf-8")

    result = check_license_matches_canonical(tmp_path, "FS003")

    assert result.status == "pass"
    assert result.code == "FS003"
    assert result.path == tmp_path / "LICENSE"
    assert result.message == "LICENSE matches canonical MXM license."


def test_license_check_fails_when_project_differs_from_canonical(
    tmp_path: Path,
) -> None:
    (tmp_path / "LICENSE").write_text(
        canonical_license() + "\nmodified\n",
        encoding="utf-8",
    )

    result = check_license_matches_canonical(tmp_path, "FS003")

    assert result.status == "fail"
    assert result.code == "FS003"
    assert result.path == tmp_path / "LICENSE"
    assert result.message == "LICENSE does not match canonical MXM license."


def test_license_check_uses_policy_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    policy_path = tmp_path / "policy" / "LICENSE"
    policy_path.parent.mkdir()

    canonical_text = "canonical license\n"

    (tmp_path / "LICENSE").write_text(canonical_text, encoding="utf-8")
    policy_path.write_text(canonical_text, encoding="utf-8")

    monkeypatch.setattr(
        license,
        "POLICY_LICENSE_PATH",
        policy_path,
    )

    result = check_license_matches_canonical(tmp_path, "FS003")

    assert result.status == "pass"
    assert result.path == tmp_path / "LICENSE"


def test_license_check_fails_when_policy_path_is_missing(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    (tmp_path / "LICENSE").write_text(canonical_license(), encoding="utf-8")

    policy_path = tmp_path / "missing_policy" / "LICENSE"

    monkeypatch.setattr(
        license,
        "POLICY_LICENSE_PATH",
        policy_path,
    )

    result = check_license_matches_canonical(tmp_path, "FS003")

    assert result.status == "fail"
    assert result.code == "FS003"
    assert result.path == policy_path
    assert "File not found" in result.message


def test_license_checks_tuple_contains_fs003() -> None:
    assert len(LICENSE_CHECKS) == 1

    check = LICENSE_CHECKS[0]

    assert check.code == "FS003"
    assert check.name == "LICENSE matches canonical license"
