---
name: bdd-gherkin
description: Create and maintain executable Gherkin acceptance scenarios when business-readable examples help align product, engineering, and QA. Use for multi-step business workflows or complex acceptance behavior.
---

# BDD and Gherkin Skill

Use BDD/Gherkin when shared business examples provide value. Do not create feature files for every unit test or trivial CRUD operation.

Guidance:

- Express behavior in domain language using Given / When / Then.
- Keep scenarios focused on one outcome and make them independent and deterministic.
- Cover key happy paths, alternate flows, validation failures, permissions, and important business boundaries.
- Avoid UI implementation details unless the UI interaction itself is the behavior under test.
- Reuse domain language and avoid ambiguous steps.
- Connect step definitions to real application behavior; do not hardcode success or mock away the behavior under test.
- Keep lower-level unit and integration tests; Gherkin complements rather than replaces them.
- Ensure the chosen Cucumber implementation and version match the project's language/framework.
- Run the feature suite and report its actual outcome.

Example:

```gherkin
Feature: Customer registration

  Scenario: Register with valid details
    Given the email address is not registered
    When the customer submits valid registration details
    Then a customer account is created
    And a confirmation is requested

  Scenario: Reject an already registered email
    Given the email address is already registered
    When the customer submits registration details
    Then the request is rejected with a duplicate-account error
```
