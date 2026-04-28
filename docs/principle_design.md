# Design Principles of `mxm-foundry`

The design of `mxm-foundry` follows a set of principles that ensure clarity, durability, and conceptual integrity across all MXM components. These principles guide both the internal structure of the tool and the form of the artefacts it generates.

## 1. Explicitness Over Convention
`mxm-foundry` must make its policies and assumptions explicit. Structural decisions—directory layout, configuration defaults, testing scaffolds, naming conventions—are codified rather than left implicit. This ensures that every MXM package begins from a known and inspectable foundation.

## 2. Minimalism of Mechanism
The tool should provide the minimum set of mechanisms required to express the intended structure. It should not introduce layers of abstraction that obscure what is being generated. Templates are clear, readable, and modifiable. The scaffolding logic is simple by design, in order to remain transparent.

## 3. Reproducible Foundations
The generated package structure must be reproducible across machines, environments, and future versions of MXM. Reproducibility here is not merely technical; it preserves coherence across the system as it grows. Identical intentions should yield identical structures.

## 4. Policy as First-Class Artefact
`mxm-foundry` acts as a repository for the policies that govern MXM development. These include configuration policies, code style conventions, naming rules, versioning standards, and documentation layouts. Policies evolve with the system and are version-controlled alongside the tool.

## 5. Orthogonality and Composability
The tool’s components—template engine, configuration synchronisation, CLI interface, documentation—should be orthogonal, each handling a single concern cleanly. Their composition should yield coherent, predictable outputs without hidden coupling. This mirrors the modular philosophy of MXM itself.

## 6. Primacy of Intent
A central principle of the MXM ecosystem is that components are crystallised intentions. `mxm-foundry` therefore begins from intention rather than from convenience. The structure of each template reflects the conceptual role of the generated package, not merely standard boilerplate.

## 7. Stability of Interface, Evolution of Templates
The CLI and API should remain stable over time, enabling reproducible workflows. Templates and policies may evolve, but changes are deliberate, documented, and versioned. Users should trust that upgrading `mxm-foundry` will not arbitrarily alter their development experience.

## 8. Visibility and Auditability
Every action performed by `mxm-foundry` should be visible to the user. The generated files are ordinary text files, not opaque artefacts. Synchronisation mechanisms operate through explicit diffs. Nothing is hidden, and nothing is magical.

## 9. Alignment with the MXM Aesthetic
`mxm-foundry` reflects the broader MXM identity: a disciplined, text-first, Unix-inspired, Bauhaus-influenced approach to construction. Artefacts are clean, minimal, and functional. The design avoids ornamentation and favours clarity of form.

## 10. Tool and Textbook
Finally, `mxm-foundry` is both a tool and a textbook. It defines the practical scaffolding required to build MXM packages, and it preserves the underlying principles that give the system coherence. Its design reflects this dual role: operational on the one hand, instructional on the other.

