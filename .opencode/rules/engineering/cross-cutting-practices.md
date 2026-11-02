# Engineering Rule — Cross-Cutting Methods and Design Practices

These are recognized approaches, not universal mandates. Apply them only when they address a real problem in the current domain and stack.

| Practice ID | Practice | When to apply |
|---|---|---|
| XENG-01 | Design by Contract | Define preconditions, postconditions, and invariants for important operations, public interfaces, and domain rules. |
| XENG-02 | Domain-Driven Design | Use ubiquitous language, bounded contexts, aggregates, and domain models when business complexity and domain boundaries justify them. |
| XENG-03 | Clean Architecture / Ports and Adapters | Separate core business policy from frameworks and external adapters when dependency isolation improves testability and evolution. |
| XENG-04 | Functional programming | Use pure functions, immutability, explicit effects, and composable transformations where the language and problem benefit. |
| XENG-05 | Twelve-Factor principles | Apply relevant principles to cloud-native services, especially config, backing services, build/release/run separation, logs, and disposability. |
| XENG-06 | Secure SDLC | Integrate threat assessment, secure implementation, testing, and security review across the lifecycle. |
| XENG-07 | Shift-left quality | Catch requirement, design, security, and test defects as early as practical. |
| XENG-08 | Continuous refactoring | Improve structure in small, behavior-preserving increments when touching code; avoid unrelated broad rewrites. |
| XENG-09 | Observability-driven development | Decide how important new behavior and failure modes will be diagnosed before production. |
| XENG-10 | Backward compatibility | Consider consumers, old application versions, persisted data, and rolling releases before changing contracts. |
| XENG-11 | Evolutionary architecture | Prefer designs that can evolve through small controlled changes over premature irreversible choices. |
| XENG-12 | Chaos and fault testing | Use controlled fault injection for critical distributed systems where it validates meaningful resilience assumptions. |
| XENG-13 | Testability by design | Structure dependencies and side effects so behavior can be verified without excessive environment setup or brittle mocking. |
| XENG-14 | Documentation as code | Version important technical documentation alongside implementation and validate examples where practical. |
| XENG-15 | Everything as Code | Version-control appropriate infrastructure, configuration, policies, pipelines, and operational definitions. |

Do not force a methodology, architecture style, or pattern solely because it appears in this list. Record why a practice is relevant when it materially changes system design.
