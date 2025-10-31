[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
# mxm-foundry

**mxm-foundry** is the internal build and maintenance tool for the *Money Ex Machina* ecosystem.  
It provides a unified way to create, configure, and synchronize MXM packages.

---

## Purpose

The package defines a standard structure and toolchain for all MXM Python projects.
It aims to make development fast, safe, and reproducible by enforcing shared conventions for:

- Source layout (`src/mxm/<package_name>/`)
- Dependency and tool configuration (`pyproject.toml`, `pyrightconfig.json`)
- Development tooling (Black, Ruff, Isort, Pyright, Pytest)
- Managed Makefile targets for linting, testing, and publishing
- Template-based scaffolding and synchronization of project configuration

---

## Status

This is an early version (v0.0.1) containing:
- Project scaffold for `mxm-foundry` itself
- Basic CLI stub (`mxm-foundry new` and `mxm-foundry check`)
- Standardized development setup and test suite

Subsequent versions will introduce:
- Template-based package generation (`mxm-foundry new`)
- Repository checks for compliance (`mxm-foundry check`)
- Config synchronization and propagation (`mxm-foundry sync`)
- GitHub integration for automatic repository creation

---

## Development

```bash
# Install dependencies
poetry install

# Run all checks
make check

# Run the CLI
poetry run mxm-foundry --help
```

## License
This project is licensed under the [MIT License](LICENSE).
© 2025 Money Ex Machina

