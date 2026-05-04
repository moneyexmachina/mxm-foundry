# MXM Foundry Check Codes

## Purpose

This document defines the namespace and allocation of all check codes used in `mxm-foundry`.

It serves two roles:

1. **Namespace discipline** — preventing arbitrary or inconsistent code usage  
2. **Allocation ledger** — recording all assigned codes and their meaning  

The runtime registry enforces uniqueness.  
This document enforces **intentional structure**.

## Code Families

- `FSxxx` — filesystem structure and required files  
- `LICxxx` — license policy and license content  
- `PYxxx` — Python, pyproject, and pyright configuration  
- `DEPxxx` — dependency declaration and version constraints *(planned)*  
- `MKxxx` — Makefile and task runner checks *(planned)*  

## Allocated Codes

### Filesystem (FS)

- `FS001` — README.md exists  
- `FS002` — LICENSE exists  
- `FS003` — pyproject.toml exists  
- `FS004` — pyrightconfig.json exists  
- `FS005` — Makefile exists  
- `FS006` — tests directory exists  
- `FS007` — src/mxm directory exists  
- `FS008` — single MXM package directory exists  
- `FS009` — package py.typed exists  
- `FS010` — CHANGELOG.md exists  

### License (LIC)

- `LIC001` — LICENSE matches canonical license  

### Python / Pyproject (PY)

- `PY001` — pyproject.toml is parseable  
- `PY002` — [tool.poetry] exists  
- `PY003` — Poetry project name starts with mxm-  
- `PY004` — Poetry package uses src/mxm layout  
- `PY005` — [tool.poetry.dependencies] exists  
- `PY006` — [tool.poetry.group.dev.dependencies] exists  
- `PY007` — [build-system] exists  
- `PY008` — [tool.pytest.ini_options] exists  
- `PY009` — Poetry include contains package py.typed  
- `PY031` — [tool.pyright] is absent  
- `PY020` — [tool.black] matches canonical config  
- `PY021` — [tool.ruff] matches canonical config  
- `PY022` — [tool.ruff.lint] matches canonical config  
- `PY023` — [tool.ruff.lint.isort] matches canonical config  
- `PY024` — [tool.isort] matches canonical config  
- `PY030` — pyrightconfig.json matches canonical config  

### Makefile

- `MK001` — Makefile defines canonical type target  
- `MK002` — type target matches canonical commands  
- `MK003` — Makefile defines canonical lint target  
- `MK004` — lint target matches canonical commands  
- `MK005` — Makefile defines canonical fmt target  
- `MK006` — fmt target matches canonical commands  
- `MK007` — Makefile defines canonical test target  
- `MK008` — test target matches canonical commands  
- `MK009` — Makefile defines canonical check target  
- `MK010` — check target matches canonical commands  
- `MK011` — Makefile defines canonical ci target  
- `MK012` — ci target matches canonical commands  

### Documentation
- `DOC001` — README.md has required sections  
- `DOC002` — CHANGELOG.md has minimal structure  
## Allocation Rules

- Codes must be unique across all families  
- Codes must be added to this document when introduced  
- Codes should be grouped logically within their family  
- Avoid gaps unless reserving space intentionally  

## Notes

This document is authoritative for human-readable structure.

The runtime registry (`checks/registry.py`) is authoritative for enforcement.
