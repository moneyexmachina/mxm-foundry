# Code and Architectural Decision Records (ADRs) in Money Ex Machina

This document explains why Money Ex Machina uses Architectural Decision Records (ADRs), how they complement code, and what conceptual role they serve in the construction of the MXM ecosystem. It defines the boundary between what belongs in code and what belongs in an ADR, so that the development process remains intentional, light, and aligned with the principles of the system.

## 1. Background

Software architecture is shaped by decisions: which patterns to use, how responsibilities are divided, what constraints exist, and what principles guide the system’s evolution. In a small or short-lived codebase, these decisions may be implicit. However, the Money Ex Machina ecosystem is:

- long-term,
- multi-package,
- conceptually structured,
- philosophically grounded,
- and intended to support both human collaborators and automated assistants.

In such a system, architectural decisions cannot be left implicit. They must be made visible and durable.

## 2. Why Code Alone Is Not Sufficient

There exists a school of thought that “clean code documents itself” and that architecture should be discoverable directly from the code. While this is partially true for implementation details, it breaks down at the architectural level.

Code can express *what* exists.  
Code cannot express:

- alternatives that were considered,
- the reasoning behind a structural decision,
- the intended constraints,
- long-term principles,
- cross-package relationships,
- naming ontologies,
- or why a particular boundary was chosen.

Architecture is defined by choices among viable alternatives.  
Code is only the final expression of one choice.

Therefore, code alone cannot preserve architectural intent.

## 3. Why ADRs Are Needed in MXM

Money Ex Machina requires:

- conceptual clarity,
- aligned modularity,
- reproducibility across years and packages,
- interoperability between components,
- a consistent architectural philosophy,
- and support for future collaborators and coding assistants.

ADRs serve these needs by capturing the *intention* behind structural choices. They do not document code. They document the rationale that leads to code. They make architectural thinking explicit, traceable, and inspectable.

ADRs serve several purposes:

1. **Preservation of intent:** decisions do not disappear over time.
2. **Clarity across packages:** shared architecture remains coherent.
3. **Support for AI-based development:** assistants cannot infer intent from code alone.
4. **Structured evolution:** future changes can reference, revise, or supersede earlier decisions.
5. **Lightweight governance:** ADRs encode principles that guide consistent implementation without heavy process.

For MXM, ADRs act as part of the system’s backbone.

## 4. The Boundary Between Code and ADRs

To avoid overhead or duplication, the boundary must be clear and sharp.

### ADRs document:

- architectural principles,
- module boundaries,
- package responsibilities,
- data models and schemas,
- naming ontologies,
- configuration structure,
- cross-package conventions,
- and long-term design constraints.

These are “load-bearing” decisions that shape code but are not visible in code.

### Code documents:

- behaviour,
- algorithms,
- implementation details,
- small refactors,
- performance optimisations,
- internal structure of functions and classes.

These are implementation-level decisions that should remain in code.

This boundary ensures that ADRs do not become bureaucratic or self-serving.

## 5. ADRs as Operational Artefacts

ADRs in MXM are not passive documentation. They are operational inputs:

- collaborators use them to understand system intent,
- coding assistants use them to generate consistent structure,
- mxm-foundry uses them to enforce standards,
- future refactors use them to avoid architectural drift.

ADRs encode the decision layer above the code layer. They are part of the construction process, not commentary after the fact.

## 6. Lightweight Process

MXM adopts a minimal ADR process that meets two criteria:

- **structurally explicit**, so that decisions are formal and traceable;
- **cognitively light**, so that the process does not burden development.

ADRs follow a simple, fixed five-section template and are created at the moment a meaningful architectural choice is made. Creating an ADR is intended to take only a few minutes, not become a separate project.

This balance preserves intentional design without adding friction.

## 7. Summary

Money Ex Machina uses ADRs because the system’s architectural intent must remain:

- explicit,
- durable,
- traceable,
- reproducible,
- and aligned across multiple packages and authors.

Code expresses structure and behaviour.  
ADRs express intention and rationale.

Both are necessary.  
Together they ensure that MXM grows coherently and remains faithful to its design philosophy of explicitness, clarity, and crystallised intention.

