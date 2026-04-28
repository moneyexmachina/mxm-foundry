# Plan for `mxm-foundry` v0.1.0
*Construction plan for the first functional release*

## 1. Purpose of this document

This document defines the **implementation plan** for `mxm-foundry` **v0.1.0** — the first release that provides a minimal but fully functional developer-facing tool.  

It translates the principles (`principle_design.md`) and the interface contract (`interface_design.md`) into a concrete execution plan, including scope, architecture, milestones, tasks, and PR structure.

This document is *not* part of the stable interface; it is a construction record and will evolve rapidly.

## 2. Scope of v0.1.0

The goal of v0.1.0 is to produce a tool that can:

### 1. Create new MXM repositories  
Via `mxm-foundry new` with:
- `package` kind  
- `library` template  
- Metadata injection (`name`, `description`, etc.)  
- Writing initial files into a target directory  
- Recording `[tool.mxm-foundry]` metadata (template + version)

### 2. Synchronise existing repositories  
Via `mxm-foundry sync` with:
- Dry-run by default  
- Compare repo state to canonical template  
- Produce a plan of file-level actions (`create`, `update`, `noop`)  
- Apply only when explicitly requested  

### 3. Check policy drift  
Via `mxm-foundry check` with:
- Validation that required files exist  
- Detect divergence in key template-managed sections  
- Return non-zero exit status if issues found  

### 4. Provide minimal internal “template engine”  
Including:
- Reading template files from `mxm-foundry/templates/library/`  
- Variable substitution (very light; probably Jinja2-less for v0.1.0)  
- File-copying with simple logic  
- Support for comparing repo vs template on a per-file basis

### 5. Provide a basic Python API mirroring the CLI  
Functions:
- `scaffold(...)`
- `sync(...)`
- `check(...)`

### 6. Provide minimal documentation  
- README describing how to use v0.1.0  
- Reference to interface design  
- Example commands  

### Out of scope for v0.1.0  
- `upgrade` verb  
- `.mxm-foundry.lock`  
- Multiple templates (only `library`)  
- Template groups (`ci`, `lint`, `docs`, etc.)  
- `show` commands beyond listing available templates  
- Emitting JSON/YAML plan files  
- Schema versioning  
- Multi-level metadata / partial sync  
- Editor integrations  
- Rich diff views  

These will be introduced incrementally in v0.2.x and v0.3.x.

## 3. Architectural structure for v0.1.0

### 3.1. Proposed module layout

```
src/mxm/foundry/
    __init__.py
    cli/
        __init__.py
        main.py
        new_cmd.py
        sync_cmd.py
        check_cmd.py
    api/
        __init__.py
        scaffold.py
        sync.py
        check.py
    core/
        __init__.py
        template_loader.py
        engine_scaffold.py
        engine_sync.py
        engine_check.py
        plan.py
    templates/
        library/
            pyproject.toml
            README.md
            Makefile
            .gitignore
            src/__init__.py
            tests/test_placeholder.py
            docs/index.md
    util/
        fs.py
        diff.py
```

### 3.2. Internal data model

#### Plan object (minimal v0.1.0)
```
Plan = {
    "actions": [
        {
            "type": "create" | "update" | "noop",
            "path": "relative/path/to/file",
            "reason": "string description"
        }
    ],
    "template_version": "0.1.0"
}
```

No delete actions in v0.1.0 (those come later in sync policies).

#### Template resolution
- Template files stored inside the package directory  
- Loading via `importlib.resources`  
- Simple placeholder replacement: `{{ name }}`, `{{ description }}`

#### Sync engine
- Compare file-by-file  
- Use lightweight hash or byte-level comparison  
- No AST-level pyproject merging yet  
- No multi-policy overlays yet  

## 4. Milestones

### **M0 — Repository Bootstrap**
- Create repo structure for `mxm-foundry`
- Set up pyproject, Makefile, ruff, black, pytest, pyright
- Minimal `mxm_foundry` package layout
- Basic documentation skeleton

### **M1 — Template Infrastructure**
- Create `templates/library/` with minimal canonical contents  
- Implement template loader (`core/template_loader.py`)  
- Implement placeholder interpolation  
- Write tests validating template loading  

### **M2 — Scaffolding Engine**
- Implement core scaffolding logic  
- Implement Python API `scaffold(...)`  
- Write `mxm-foundry new` CLI wrapper  
- Ensure correct writing of `[tool.mxm-foundry]` metadata  
- Tests: create a temp directory and ensure correct outputs  

### **M3 — Sync Engine**
- Implement file comparison logic  
- Implement plan construction  
- Implement apply-vs-dry-run mechanism  
- Provide Python API `sync(...)`  
- Implement CLI wrapper `mxm-foundry sync`  
- Tests: compare template vs mutated repo; validate plan  

### **M4 — Check Engine**
- Implement validation rules  
- API `check(...)`  
- CLI `mxm-foundry check`  
- Tests: repo missing files → fail; matching repo → success  

### **M5 — Integrate CLI & API**
- `main.py` dispatch  
- Consistent option handling  
- Standard CLI exit codes  
- Error handling & messaging  

### **M6 — Documentation Pass**
- Update README  
- Add basic usage examples  
- Add link references to interface and principle docs  
- Write minimal architecture section  

### **M7 — Release**
- Final QA on template  
- Tag `v0.1.0`  
- Publish to PyPI  
- Announce internally in MXM ecosystem  
- Mark start of v0.2.0 planning  

## 5. PR Structure

Each milestone should map to 1–3 PRs.

**PR guidelines for v0.1.0**:

- Smallest unit that preserves narrative coherence  
- No giant multi-feature PRs  
- Each PR should update or create tests  
- Each PR should update documentation where applicable  

### Suggested PR breakdown

**PR 1 — Bootstrap repo**  
**PR 2 — Template loader**  
**PR 3 — Template scaffolding engine**  
**PR 4 — CLI for `new`**  
**PR 5 — Sync engine core**  
**PR 6 — CLI for `sync`**  
**PR 7 — Check engine core**  
**PR 8 — CLI for `check`**  
**PR 9 — Documentation + README**  
**PR 10 — Release prep**  

## 6. Out-of-Scope Items for v0.1.0 (Deferred)

To keep the first release minimal and crisp, the following are intentionally deferred:

- Policy-layer logic (ci/lint/docs groups)
- Delete actions in plan  
- Rich diff formatting  
- template inheritance  
- Full Jinja or templating DSL  
- Detailed lockfile  
- Multiple artefact kinds  
- `upgrade` verb  
- `show` beyond bare minimum  
- Error taxonomy  
- Configurable template root overrides  
- Automated project naming validators  

These form the roadmap for v0.2.x and v0.3.x.

## 7. Risks / Open Questions

### File comparison granularity  
For v0.1.0 we accept simple:  
- `hash(template-file) != hash(repo-file)` → `update`  

### Template metadata  
Only minimal `[tool.mxm-foundry]` needed now.

### Future-proofing  
Ensure architecture does not block:  
- Lockfile  
- Complex template graphs  
- Multi-template merge  
- Plugin system  

## 8. Summary

v0.1.0 delivers a foundational, minimal-but-functional `mxm-foundry`:

- It scaffolds new repositories.  
- It detects drift.  
- It synchronises existing repositories.  
- It provides a Python API and CLI aligned with the interface design.  
- It is small, explicit, stable, and testable.  

This release sets the stage for richer template management, versioned migrations, and policy enforcement in subsequent iterations.

