# Engineering Rule — Coding Standards and Clean Code (CODE)

Follow the language-specific conventions loaded from the relevant skill and the repository's formatter/linter configuration.

| ID | Requirement | Agent must enforce |
|---|---|---|
| CODE-01 | Readability | Write code that a maintainer can understand without needing extensive explanation. |
| CODE-02 | Naming | Use descriptive, domain-appropriate names for variables, functions, classes, modules, files, and tests. Follow language conventions. |
| CODE-03 | Focused functions | Keep functions and methods focused on a coherent responsibility; split logic when it improves comprehension, reuse, or testability. |
| CODE-04 | Type safety | Use available static typing, schemas, and compiler checks. Avoid unnecessary untyped values, unsafe casts, and broad escape hatches. |
| CODE-05 | Error handling | Handle expected failures explicitly and consistently; preserve useful context without leaking sensitive details. |
| CODE-06 | No swallowed exceptions | Do not silently catch and ignore failures. Catch only when the code can recover, translate, add context, or deliberately handle the error. |
| CODE-07 | No magic values | Replace meaningful unexplained literals with named constants, enums, configuration, or domain concepts as appropriate. |
| CODE-08 | No dead code | Remove obsolete code, unused imports, unreachable branches, and abandoned implementations introduced by the change. |
| CODE-09 | Useful comments | Comment intent, invariants, non-obvious trade-offs, and constraints; do not narrate code that is already clear. |
| CODE-10 | Interface documentation | Document public APIs, extension points, non-obvious contracts, and complex business rules. |
| CODE-11 | Consistency | Follow existing formatting, naming, lint, and idiomatic language conventions. Do not introduce unrelated formatting churn. |
| CODE-12 | No incomplete placeholders | Do not deliver unexplained TODOs, stubs, dummy responses, hardcoded success paths, or incomplete methods as finished functionality. |
| CODE-13 | Controlled complexity | Avoid needless nesting, long conditional chains, high cyclomatic complexity, and abstractions that make behavior harder to follow. |
| CODE-14 | Immutability and side effects | Prefer immutable data, explicit state transitions, and controlled side effects where appropriate to the language and domain. |
| CODE-15 | Dependency inversion | Keep core business rules from depending unnecessarily on databases, frameworks, UI, or external service implementations. |

## Implementation expectations

- Reuse existing project tooling rather than introducing a competing formatter or linter.
- Do not optimize style at the cost of compatibility with established code conventions.
- Avoid broad refactors inside feature work unless required; scope and verify them separately where practical.
- Make failure behavior and resource ownership explicit.
