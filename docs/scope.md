# Scope of `mxm-foundry`

This document defines the functional scope of `mxm-foundry`. It clarifies what the tool provides, what responsibilities it holds within the MXM ecosystem, and how it interacts with related packages such as `mxm-style`. The scope is derived from the purpose and design principles of the project, and will evolve through versioned revisions.

## 1. Overview

`mxm-foundry` is responsible for establishing, maintaining, and enforcing the structural, stylistic, and procedural foundations of all MXM software components. It is the tool that translates conceptual intent into an initial working artefact, and ensures that all subsequent MXM packages remain aligned with shared policies, standards, and style definitions.

The scope of `mxm-foundry` has two layers:

1. **Artefact creation** – scaffolding new packages, repositories, and documentation.
2. **Artefact enforcement** – checking and synchronising packages to maintain compliance with MXM-wide standards.

It does not implement runtime features, domain-specific logic, or user-facing interfaces. It is a construction tool, not an operational tool.

## 2. Scaffolding Responsibilities

Scaffolding is a core function of `mxm-foundry`. It includes:

### 2.1 Package Creation
- Creating directory structures for new MXM packages.
- Initialising Poetry configurations.
- Initialising Git repositories.
- Creating and populating common files:
  - `README.md`
  - `CHANGELOG.md`
  - `LICENSE`
  - `.gitignore`
  - `py.typed`
  - `Makefile`
  - base test structure
  - `docs/` folder with MXM-standard documents

### 2.2 Repository Initialization
- Adding GitHub Actions CI workflows.
- Adding PR & issue templates.
- Adding default GitHub labels.
- Applying MXM-wide development and release conventions.
- Preparing semantic versioning integration.

### 2.3 Template Registry
- Maintaining canonical MXM templates (e.g. `mxm-package`, `cli-tool`, `data-package`).
- Supporting local and user-defined templates.
- Ensuring template evolution is versioned and reproducible.

These scaffolding outputs reflect explicit MXM design and development policies.

## 3. Standards and Configuration Responsibilities

`mxm-foundry` provides and enforces the shared configuration layer of the MXM ecosystem. This includes:

### 3.1 Coding Standards
- `pyproject.toml` configuration for:
  - ruff
  - black
  - isort
  - pyright
  - pytest
  - Poetry metadata
- `.editorconfig`
- Standardised Makefile targets
- Test scaffolding conventions

### 3.2 Documentation Standards
- Templates for:
  - README structure
  - CHANGELOG format (conventional commits + semantic versioning)
  - Development sequence & PR requirements
  - Architecture documentation layout
- Scaffolding for policy and philosophy documents inside each package.

### 3.3 Policy Enforcement
Scaffolding is not the end state. `mxm-foundry` must also ensure long-term adherence to standards by providing:

- `mxm-foundry check` — detect divergence from MXM standards.
- `mxm-foundry sync` — apply corrections and update specifications in-place.

This dual function ensures that both new and existing packages remain aligned with the evolving MXM framework.

## 4. Style Responsibilities

### 4.1 Separation of Source-of-Truth vs Enforcement
`mxm-style` is the **authoritative repository of MXM visual, textual, and stylistic rules**.

`mxm-foundry` **consumes and enforces** those rules.

This division is intentional:

- `mxm-style` = defines **what MXM looks and feels like**
- `mxm-foundry` = ensures all packages **adhere to those stylistic rules**

### 4.2 Style Enforcement (Within Scope)
`mxm-foundry` enforces:
- GitHub label colour palette
- Standardised badge styling
- Makefile output conventions
- Terminal colour coding for tools (if defined in `mxm-style`)
- Documentation tone and structure (as rules, not as prose)
- Layout and ordering of sections in standard files
- Any style guidelines defined in `mxm-style` that apply to developers or code artefacts

### 4.3 Style Definition (Out of Scope)
`mxm-foundry` does **not** define:
- Aesthetic themes for visualisations, plots, or UI.
- User-facing branding (typography, logos, imagery).
- Website or publication styling.
- Aesthetic frameworks for mxm-operator or mxm-brain.

These belong in `mxm-style`.

## 5. Out of Scope (Explicit)

The following are outside the responsibility of `mxm-foundry`:

- Runtime execution tools and operator interfaces.
- Data ingestion, configuration interpretation, pipeline execution.
- Simulation or modelling utilities.
- Test execution frameworks.
- Public-facing aesthetic or branding tools.
- Runtime policy management.

`mxm-foundry` is concerned solely with the construction, consistency, and coherence of MXM components.

## 6. Summary

`mxm-foundry` is the construction tool of the Money Ex Machina ecosystem.  
Its responsibilities include:

- Creating new packages and repositories.
- Applying MXM standards and configurations.
- Enforcing consistency across the entire ecosystem.
- Consuming and applying style rules defined in `mxm-style`.

It is not a runtime or operational tool, but the mechanism by which MXM’s architecture, conventions, and identity become concrete across all code repositories.


## 7. Architecture as Code

Money Ex Machina treats architecture as a first-class component of the system. Architectural intent is not an informal side-layer or commentary; it is part of the constructed artefact. `mxm-foundry` therefore includes explicit support for representing architecture in code and for ensuring that every MXM package expresses its structural intent in a consistent, reproducible, and inspectable way.

Architecture in MXM is expressed across three layers:

### 7.1 The Code Layer
This is the structural implementation: modules, functions, classes, and internal logic. It expresses behaviour and structure. It is governed by coding standards, directory conventions, and type-checked APIs. `mxm-foundry` ensures this layer begins from a clear, consistent foundation through scaffolding and synchronisation.

### 7.2 The Architectural Intent Layer
This layer is captured through Architectural Decision Records (ADRs). ADRs encode the rationale behind architectural choices, the alternatives considered, and the long-term design principles that guide package boundaries and system evolution. They ensure that architectural intent does not remain implicit or dependent on personal memory.

`mxm-foundry` supports this layer by:
- Providing ADR templates,
- Enforcing naming and structural conventions,
- Initialising a `docs/decisions/` directory,
- Offering commands to create, index, and manage ADRs,
- Ensuring ADRs remain consistent with repository structure.

### 7.3 The System Policy Layer
Beyond individual decisions, MXM maintains global architectural policies: naming ontologies, data model conventions, configuration standards, and cross-package integration rules. These policies operate above both code and ADRs. They define the governing principles of the ecosystem.

`mxm-foundry` acts as the mechanism through which these policies become enforceable across all repositories. It applies shared templates, synchronises common files, validates structure, and ensures that all components of the system align with the global architectural framework.

### 7.4 Integration of Layers
Treating architecture as code means that:

- architectural decisions are versioned,
- system-wide policies are codified and inspectable,
- structure and intent evolve together,
- deviations are detectable and correctable,
- tooling (human or automated) can reason over architecture.

`mxm-foundry` is the tool that binds these layers. It translates architectural thinking into concrete artefacts, keeps architectural records coherent, and enforces the connection between code, intent, and policy.

This three-layer model ensures that MXM grows coherently, remains explainable, and retains a stable conceptual spine as new components are added or existing components evolve.

