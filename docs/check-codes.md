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

### License (LIC)

- `LIC001` — LICENSE matches canonical license  

### Python / Pyproject (PY)

- `PY001` — pyproject.toml is parseable  
- `PY002` — [tool.poetry] exists  
- `PY003` — Poetry project name starts with mxm-  
- `PY004` — Poetry package uses src/mxm layout  
- `PY031` — [tool.pyright] is absent  
- `PY020` — [tool.black] matches canonical config  
- `PY030` — pyrightconfig.json matches canonical config  

### Makefile

- `MK001` — Makefile defines type target  
- `MK002` — type target invokes pyright  

## Allocation Rules

- Codes must be unique across all families  
- Codes must be added to this document when introduced  
- Codes should be grouped logically within their family  
- Avoid gaps unless reserving space intentionally  

## Notes

This document is authoritative for human-readable structure.

The runtime registry (`checks/registry.py`) is authoritative for enforcement.
