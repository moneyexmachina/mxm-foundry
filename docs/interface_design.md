# Interface Design for `mxm-foundry`
*Developer-facing architecture, CLI surface, and API contract*

## 1. Overview

`mxm-foundry` is the entry point through which ideas become structured artefacts inside the Money Ex Machina ecosystem.  
Where `purpose.md` defines *why* the tool exists, and `principle_design.md` defines *how* it should behave, this document specifies *what the developer interacts with* — the CLI and the Python API.

The interface is deliberately minimal, explicit, and shaped by the design principles of clarity, reproducibility, and orthogonality.  
All developer interactions fall under five verbs:

- `new` – create a structured repository from an intention  
- `sync` – apply policies and templates to bring a repo into alignment  
- `check` – detect drift from the canonical template  
- `show` – inspect policies, templates, and tool metadata  
- `upgrade` – controlled migration from an older template to a newer one  

These verbs form the stable external contract of the tool.

## 2. Interaction Model

### 2.1. Intent crystallisation
Developers begin with a conceptual intention: *“I need an MXM Python library for configuration handling”*.  
`mxm-foundry` converts that abstract intention into a concrete repository with:

- Correct directory layout  
- Standard `pyproject.toml` metadata  
- Build, lint, and test scaffolding  
- A minimal documentation skeleton  
- CI workflows  
- A recorded template version  

### 2.2. Continuous alignment
Once a repository exists, the developer periodically synchronises it with evolving MXM policies using `sync`.  
This preserves:

- Reproducible foundations  
- Stability of interface  
- Visibility of changes via explicit plans and diffs  

### 2.3. Inspection and pedagogy
`show` exposes the templates and rules clearly, fulfilling the “tool and textbook” principle.  
Templates are intentionally readable and inspectable.

### 2.4. Migration over time
Policies evolve but do not break the interface.  
Repositories record which version of the template they were generated with; `upgrade` computes and applies a precise migration plan.

## 3. CLI Design

### 3.1. General philosophy
The CLI follows three constraints:

1. **Few verbs, many options** — avoid command sprawl  
2. **Dry-runs by default** — no silent mutations  
3. **Plan visibility** — all actions represented as explicit plan objects  

Each command supports:

- `--dry-run`  
- `--apply`  
- `--emit-plan` (export JSON/YAML for automation)

### 3.2. Command: `new`

Create a new MXM artefact.

Example:

```
mxm-foundry new package \
  --name mxm-config \
  --template library \
  --description "Config layer for MXM" \
  --dest ~/dev/mxm-config
```

This writes only what is necessary; everything is Git-diffable.

Supported artefact kinds (initially):

- `package` — a standard Python library  
- `cli-tool` — a package providing an entrypoint  
- `service` — long-running operational tools (later)  
- `analysis` — notebooks + script scaffolds (later)

### 3.3. Command: `sync`

Synchronise an existing repository with the active template.

```
cd ~/dev/mxm-config
mxm-foundry sync repo --profile library --apply
```

`sync`:

- Compares current state with the canonical template  
- Produces a plan of file-level changes  
- Applies changes only when `--apply` is set  

Supports template groups:

- `ci`  
- `lint`  
- `docs`  
- `structure`  
- `labels`  

### 3.4. Command: `check`

Non-destructive consistency check.

```
mxm-foundry check repo --profile library
```

Reports:

- Missing required files  
- Deviations from canonical config sections  
- Policy drift relative to recorded template version  

Exits non-zero for CI integration.

### 3.5. Command: `show`

Introspect policies and templates.

```
mxm-foundry show templates
mxm-foundry show template library
mxm-foundry show policy linting
mxm-foundry show version
```

This command anchors the pedagogical role of the tool.

### 3.6. Command: `upgrade`

Upgrade a repository between template versions.

```
mxm-foundry upgrade repo \
  --from 0.2.1 \
  --to   0.3.0 \
  --apply
```

Produces:

- A migration plan  
- Diffs per changed template component  
- Migration notes extracted from an internal changelog  

## 4. Python API

### 4.1. Principles

The API mirrors the CLI exactly.  
No hidden global state.  
No side effects without explicit apply.

### 4.2. Functions

```
from mxm_foundry import api as foundry

foundry.scaffold(...)
foundry.sync(...)
foundry.check(...)
foundry.describe_template(...)
foundry.upgrade_plan(...)
```

### 4.3. Plan objects

Sync and upgrade operations return pure, explicit “plan” objects:

```
{
  "actions": [
    { "type": "create", "path": "Makefile", "reason": "template missing" },
    { "type": "update", "path": "pyproject.toml", "reason": "policy drift" },
    { "type": "noop", "path": "README.md" }
  ],
  "template_version_from": "0.2.1",
  "template_version_to": "0.3.0"
}
```

Plans are:

- Serializable  
- Stable  
- Testable  
- Independent of execution  

### 4.4. Repository metadata

Every template-generated repo contains:

```
[tool.mxm-foundry]
template = "library"
profile  = "default"
version  = "0.3.0"
```

Optionally:

- `.mxm-foundry.lock` — file-level hashes for full reproducibility.

## 5. Template & Policy Versioning

### 5.1. Template version
Each release of `mxm-foundry` includes:

- Template files  
- Policy documents  
- A structured changelog describing differences  

### 5.2. Version recorded locally
Repos track the template version they were created with.  
This enables:

- Accurate sync  
- Safe upgrade  
- Predictable migrations  

### 5.3. Controlled evolution
Older repos do not break when templates change.  
Repository owners choose when to run `upgrade`.

## 6. Alignment with Design Principles

`interface_design.md` is the binding layer connecting the design principles to concrete interface choices.

| Design Principle | Interface Reflection |
|------------------|-----------------------|
| **Explicitness** | Verb-based CLI; explicit profiles; recorded template version |
| **Minimalism** | Five core commands; no magic; minimal flags |
| **Reproducibility** | Templates + lockfiles + version metadata |
| **Policy as artefact** | `show` exposes templates and rules |
| **Orthogonality** | Separate verbs for create/sync/check/inspect/upgrade |
| **Visibility** | Dry-runs; plan emission; Git-diff clarity |
| **Pedagogy** | CLI + API + documentation form a cohesive textbook |
| **Stability** | Commands are stable; templates evolve through versioning |

## 7. Roadmap

### Minimal v0

- `new`, `sync`, `check`  
- One template: `library`  
- `show templates`  
- Recording `[tool.mxm-foundry]` metadata  

### v0.2 – Template evolution

- Add `upgrade`  
- Add template groups  
- Add `emit-plan`  
- Introduce `.mxm-foundry.lock`  

### v0.3 – Developer UX maturity

- More templates (CLI tool, analysis)  
- Extended `show` functionality  
- Richer plan diffs  

## 8. Summary

`interface_design.md` defines the stable external contract of `mxm-foundry`.  
It translates design principles into concrete interactions and ensures that the tool remains transparent, predictable, and aligned with the aesthetic and operational philosophy of Money Ex Machina.

