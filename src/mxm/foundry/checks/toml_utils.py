from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

import tomlkit
from tomlkit.exceptions import ParseError

TomlMapping = Mapping[str, Any]


def load_toml(path: Path) -> tuple[TomlMapping | None, str | None]:
    if not path.is_file():
        return None, f"{path.name} is missing."

    try:
        document = tomlkit.parse(path.read_text())
    except ParseError as exc:
        return None, f"{path.name} is not valid TOML: {exc}"

    return cast(TomlMapping, document), None


def mapping_value(mapping: TomlMapping, key: str) -> TomlMapping | None:
    value = mapping.get(key)
    if isinstance(value, Mapping):
        return cast(TomlMapping, value)
    return None


def nested_mapping(
    mapping: TomlMapping,
    keys: tuple[str, ...],
) -> TomlMapping | None:
    current: TomlMapping | None = mapping

    for key in keys:
        if current is None:
            return None
        current = mapping_value(current, key)

    return current
