---
name: tdd
description: Use test-driven development for behavior changes: formulate failing tests, implement the smallest change, refactor, and verify. Use when adding features or fixing bugs where tests can express expected behavior.
---

# Test-Driven Development Skill

1. Identify the behavior and acceptance criteria before writing code.
2. Choose the narrowest meaningful test level first (usually unit or component; integration/contract/E2E where boundaries require it).
3. Write a test for one behavior or scenario.
4. Run it and confirm it fails for the expected reason—not because of broken setup or syntax.
5. Implement the smallest change that satisfies the test.
6. Run the test and confirm it passes.
7. Refactor for clarity/design while keeping tests green.
8. Add negative, boundary, and regression cases based on risk.
9. Run the relevant broader test suite and record exact commands/results.
10. Do not change a failing test merely to match an incorrect implementation.

TDD is the default, not dogma. For mechanical changes, exploratory spikes, external-system constraints, or code where a meaningful test cannot precede implementation, use a justified alternative and add verification as early as possible.
