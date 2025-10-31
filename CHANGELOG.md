# Changelog
All notable changes to this project will be documented in this file.

This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] — 2025-10-31
### Added
- Initial repository scaffold with `src/mxm/foundry/` namespace layout.
- `pyproject.toml` with Poetry, dev toolchain (Ruff, Black, Isort, Pyright, Pytest).
- `pyrightconfig.json` (Python 3.13, strict mode).
- `Makefile` with standard targets (`fmt`, `lint`, `type`, `test`, `check`, etc.).
- `README.md` and `LICENSE` (MIT).
- `.gitignore` for Python, Poetry, and tool caches.
- `py.typed` marker and inclusion in packaging.
- Minimal CLI stub (`mxm-foundry`) with `new` and `check` placeholders.
- `tests/test_smoke.py` covering version import and CLI basics.
