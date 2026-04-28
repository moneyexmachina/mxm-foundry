from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.predicates import check_required_file


def test_check_required_file_pass(tmp_path: Path) -> None:
    # Arrange
    file_path = tmp_path / "README.md"
    file_path.write_text("# Test\n")

    # Act
    result = check_required_file(tmp_path, "README.md", "FS001")

    # Assert
    assert result.status == "pass"
    assert result.code == "FS001"
    assert result.path == file_path


def test_check_required_file_fail(tmp_path: Path) -> None:
    # Arrange
    # no file created

    # Act
    result = check_required_file(tmp_path, "README.md", "FS001")

    # Assert
    assert result.status == "fail"
    assert result.code == "FS001"
    assert result.path == tmp_path / "README.md"


def test_check_required_file_different_file(tmp_path: Path) -> None:
    # Arrange
    (tmp_path / "LICENSE").write_text("MIT\n")

    # Act
    result = check_required_file(tmp_path, "LICENSE", "FS002")

    # Assert
    assert result.status == "pass"
    assert result.code == "FS002"
    assert result.path == tmp_path / "LICENSE"
