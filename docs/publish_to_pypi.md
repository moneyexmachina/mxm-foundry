# Publishing to PyPI (MXM Packages)

This document describes how to set up and use **automated publishing to PyPI via GitHub Actions (Trusted Publishing / OIDC)** for an MXM package.

It is written as an explicit step-by-step guide for first-time setup and subsequent releases.

# Overview

We use:

- **Poetry** for packaging
- **GitHub Actions** for CI and release automation
- **PyPI Trusted Publishing (OIDC)** for secure, tokenless publishing

Publishing is triggered by pushing a **version tag**:

```bash
git tag v0.1.0
git push origin v0.1.0
```

# Preconditions

You should already have:

- A GitHub repository (e.g. `moneyexmachina/mxm-foundry`)
- A valid `pyproject.toml`
- A working CI (`make check` passes locally)
- Accounts:
  - Logged into GitHub (mxm)
  - Logged into PyPI (mxm)

# Step 1 — Ensure release workflow exists

Create:

```
.github/workflows/release.yml
```

Canonical version:

```yaml
name: Publish to PyPI

on:
  push:
    tags: ["v*"]

permissions:
  id-token: write
  contents: read

jobs:
  publish:
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/project/<PACKAGE_NAME>/

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Build
        run: |
          python -m pip install --upgrade pip
          pip install build twine

          TAG="${GITHUB_REF_NAME#v}"

          python - <<'PY' "$TAG"
          import sys, tomllib
          want = sys.argv[1]
          with open("pyproject.toml", "rb") as f:
              got = tomllib.load(f)["tool"]["poetry"]["version"]
          assert want == got, f"Tag v{want} != pyproject {got}"
          PY

          python -m build
          python -m twine check dist/*

      - name: Publish to PyPI via OIDC
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          print-hash: true
```

Replace:

```
<PACKAGE_NAME>
```

Example:

```
mxm-foundry
```

# Step 2 — Configure PyPI Trusted Publisher (ONE-TIME SETUP)

This is the critical step.

## 2.1 Go to PyPI

- Open: https://pypi.org
- Log in with mxm account

## 2.2 Create project OR prepare for creation

Two cases:

### Case A — Project already exists

- Open project page
- Go to:
  ```
  Manage → Publishing
  ```

### Case B — Project does not exist yet

- Go to:
  ```
  Account Settings → Publishing
  ```
- Add a **new Trusted Publisher**

## 2.3 Add Trusted Publisher

Fill in:

| Field | Value |
|------|------|
| Owner | `moneyexmachina` |
| Repository | `<repo-name>` (e.g. `mxm-foundry`) |
| Workflow | `release.yml` |
| Environment | `pypi` |

Important:

- Workflow name must match file name exactly
- Environment must match GitHub Actions job

## 2.4 Save

At this point:

- PyPI trusts GitHub Actions from this repo
- No API token is required

# Step 3 — Verify package metadata

Before releasing:

## 3.1 Version

Ensure:

```toml
[tool.poetry]
version = "0.1.0"
```

Matches intended tag.

## 3.2 Build works locally

```bash
poetry install
make check

python -m build
python -m twine check dist/*
```

## 3.3 Changelog updated

Ensure:

```
CHANGELOG.md
```

Contains:

```
## [0.1.0] – YYYY-MM-DD
```

# Step 4 — Create release

## 4.1 Commit everything

```bash
git add .
git commit -m "Release v0.1.0"
git push
```

## 4.2 Create tag

```bash
git tag v0.1.0
git push origin v0.1.0
```

# Step 5 — Observe GitHub Actions

- Go to:
  ```
  GitHub → Actions → Publish to PyPI
  ```

Expected steps:

1. Checkout
2. Build
3. Version check (tag vs pyproject)
4. Upload to PyPI

If successful:

- Package appears on PyPI immediately

# Step 6 — Verify release

```bash
pip install mxm-foundry
```

or:

```bash
pip install mxm-foundry==0.1.0
```

# Common Failure Modes

## 1. Version mismatch

Error:

```
Tag v0.1.0 != pyproject 0.0.1
```

Fix:

- Update `pyproject.toml`
- Commit
- Re-tag

## 2. Trusted publisher not configured

Error:

```
403 Forbidden / authentication failed
```

Fix:

- Re-check PyPI → Publishing settings
- Ensure repo / workflow / environment match exactly

## 3. Wrong workflow name

PyPI requires exact match:

```
release.yml
```

## 4. Environment mismatch

Must match:

```yaml
environment:
  name: pypi
```

# Optional Enhancements (Later)

- Add GitHub Release creation step
- Add changelog extraction into release notes
- Add TestPyPI staging flow
- Add version bump automation

# Minimal Mental Model

Publishing is:

```
git tag → GitHub Actions → OIDC → PyPI
```

No API keys, no manual upload.

# Final Checklist

Before tagging:

- [ ] `make check` passes
- [ ] version updated in `pyproject.toml`
- [ ] CHANGELOG updated
- [ ] CI passing on main
- [ ] Trusted Publisher configured

Then:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

This is the standard MXM publishing workflow.
