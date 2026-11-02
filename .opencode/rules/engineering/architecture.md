# Engineering Rule — Architecture and Design (ARCH)

Apply these standards pragmatically. Preserve an established architecture unless there is a justified, reviewed reason to change it. Avoid architecture astronautics and speculative abstractions.

| ID | Requirement | Agent must enforce |
|---|---|---|
| ARCH-01 | Separation of concerns | Keep presentation, business rules, persistence, integration, and infrastructure responsibilities appropriately separated. |
| ARCH-02 | High cohesion, low coupling | Keep closely related responsibilities together and minimize unnecessary dependencies between unrelated components. |
| ARCH-03 | Modularity | Organize code into components/modules with clear responsibilities, boundaries, and interfaces. |
| ARCH-04 | SOLID principles | Apply SRP, OCP, LSP, ISP, and DIP where they improve design; do not force patterns mechanically. |
| ARCH-05 | DRY | Remove meaningful duplication, but do not abstract coincidentally similar code when the abstraction would obscure different domain behavior. |
| ARCH-06 | KISS | Prefer the simplest design that satisfies functional, non-functional, and operational requirements. |
| ARCH-07 | YAGNI | Do not implement hypothetical features or extension points without a demonstrated requirement or justified near-term need. |
| ARCH-08 | Extensibility | Provide extension points where actual or reasonably anticipated variation exists; explain their intended variation point. |
| ARCH-09 | Reusability | Reuse genuinely shared behavior where doing so improves consistency and maintenance; avoid premature generic frameworks. |
| ARCH-10 | Dependency management | Avoid circular dependencies, uncontrolled transitive coupling, unnecessary dependencies, and incorrect dependency direction. |
| ARCH-11 | Architecture consistency | Follow existing architecture and ADRs; propose material deviations with rationale and migration impact. |
| ARCH-12 | Design patterns | Use established patterns only when they solve a concrete problem and fit the project's idioms. |
| ARCH-13 | Interface-driven design | Define clear contracts between components that need independent evolution, testing, or substitution. |
| ARCH-14 | Configuration management | Externalize environment-specific and operational configuration; validate it and provide safe defaults where appropriate. |
| ARCH-15 | Technical debt management | Identify material debt introduced or encountered; document impact, risk, and a practical remediation path without creating unrelated cleanup scope. |

## Design decision guidance

- Evaluate the simplest viable design before introducing layers, factories, registries, event buses, or plugin mechanisms.
- Keep domain rules independent of frameworks and infrastructure where project complexity justifies that boundary.
- Consider migration and compatibility costs before reorganizing modules or changing shared contracts.
- Add or update an ADR for consequential architectural decisions.
- Treat extensibility as a response to a real variation point, not a goal to maximize in isolation.
