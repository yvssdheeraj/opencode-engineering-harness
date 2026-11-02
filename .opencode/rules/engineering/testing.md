# Engineering Rule — Testing Strategy and TDD (TEST)

Testing must be risk-based and layered. TDD is the default for new or changed behavior when practical; it is not a reason to write low-value tests or fake a red phase. Use the project's frameworks and test conventions.

| ID | Requirement | Agent must enforce |
|---|---|---|
| TEST-01 | Test-first development | Prefer Red → Green → Refactor: add a behavior test, observe the expected failure, implement the smallest passing change, then refactor and rerun. Record justified exceptions. |
| TEST-02 | Unit testing | Test focused business rules, algorithms, transformations, and validation without unnecessary external dependencies. |
| TEST-03 | Integration testing | Test interactions across real component boundaries such as database, framework wiring, queues, filesystem, and service clients. |
| TEST-04 | End-to-end testing | Verify critical user journeys through the running application or representative deployed system where appropriate. |
| TEST-05 | Regression testing | Add a test for a defect or previously broken behavior so it does not silently return. |
| TEST-06 | Acceptance testing | Map acceptance criteria to observable tests or documented verification evidence. |
| TEST-07 | Negative testing | Test invalid inputs, missing records, permission denial, timeouts, unavailable dependencies, and expected failures. |
| TEST-08 | Boundary testing | Test empty, null, minimum, maximum, out-of-range, oversized, duplicate, and unusual inputs where relevant. |
| TEST-09 | Concurrency testing | Test races, simultaneous updates, ordering, and concurrent access when the behavior or data integrity requires it. |
| TEST-10 | Contract testing | Verify consumer/provider contracts, schemas, message formats, and compatibility across independently released components. |
| TEST-11 | Test isolation | Tests must not depend on execution order, shared mutable state, or uncontrolled external state. |
| TEST-12 | Determinism | Avoid flaky timing, random, network, locale, clock, and environment dependencies; control or inject them. |
| TEST-13 | Coverage interpretation | Use coverage to find untested code, not as a standalone measure of quality or a target that encourages meaningless assertions. |
| TEST-14 | Mutation testing | Consider mutation testing for critical business rules, security-sensitive logic, or high-assurance components. |
| TEST-15 | Test data management | Use reproducible, minimal, non-sensitive fixtures and controlled data setup/teardown. Never copy production personal data into tests without approved safeguards. |
| TEST-16 | Test pyramid and balance | Prefer fast unit tests and focused integration/contract tests; keep E2E coverage centered on critical journeys rather than making the suite unnecessarily brittle. |
| TEST-17 | Independent verification | Execute the relevant tests after implementation, inspect final status and failures, and report exact results. |
| TEST-18 | Failure diagnosis | Investigate whether code, test assumptions, fixtures, environment, or contract is wrong. Never delete or weaken a valid test merely to obtain a pass. |

## BDD and Cucumber / Gherkin

- Use Gherkin when concrete business examples need to be shared among product, domain, testing, and engineering stakeholders or when executable acceptance scenarios provide durable value.
- Write scenarios in business language and observable outcomes. Keep UI mechanics and implementation details out of business scenarios unless they are part of the requirement.
- Implement step definitions against real application behavior and execute them in the intended test environment.
- Do not create Gherkin for every unit test or duplicate all lower-level assertions in feature files.
- Use Given/When/Then to express initial context, an event/action, and an observable outcome. Include alternate and failure scenarios where they matter.

## Test selection guide

- Unit: isolated logic and domain rules.
- Integration: persistence, framework wiring, messaging, adapters, and boundaries.
- Contract: independently developed or deployed consumers/providers.
- E2E: a small set of critical end-user flows.
- BDD/Gherkin: shared business acceptance examples when collaboration benefits.
