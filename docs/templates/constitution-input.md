# Input Guide for `/speckit.constitution`

Use this guide to write the actual project constitution. Do not copy every row of the generic engineering catalog into it.

## Candidate durable principles

Choose and tailor principles that genuinely apply:

1. **User and requirement integrity:** Implement only behavior traceable to approved requirements and acceptance criteria.
2. **Architecture:** Preserve explicit module boundaries, dependency direction, and domain ownership.
3. **Maintainability:** Prefer simple, readable, cohesive changes; avoid speculative abstractions.
4. **Testing:** Verify behavior at appropriate test levels; use TDD by default where practical.
5. **Security and privacy:** Validate untrusted input, enforce server-side authorization, protect secrets and sensitive data.
6. **Reliability:** Define failure behavior, timeouts, retry/idempotency rules, and data integrity for relevant operations.
7. **Accessibility and UX:** Follow the project's accessibility target and established design system for user-facing work.
8. **Operability:** Make production-relevant behavior observable and support safe deployment/recovery.
9. **Compatibility:** Evolve APIs, schemas, and dependencies deliberately; document approved breaking changes.
10. **Evidence:** Do not mark work complete without actual implementation and verification evidence.

## Project-specific decisions to supply

- Product/domain and critical user journeys.
- Architectural style and explicit module/service boundaries.
- Supported language/framework/runtime versions.
- Data classification and security/compliance constraints.
- Availability/performance expectations where known.
- Accessibility target.
- API compatibility and deprecation policy.
- Required CI checks and release controls.
- Definition of done and approval boundaries.

Keep the final constitution concise, durable, and testable. Put detailed technology rules into skills and repository-specific build commands into `AGENTS.md`.
