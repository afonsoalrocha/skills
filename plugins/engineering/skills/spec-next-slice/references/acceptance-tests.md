# Acceptance tests in natural language

A contract with the system owner, who does not read code (source: Uncle Bob, Gherkin reviewed by a human).

```text
Feature: Discount for a VIP customer
  Scenario: A VIP pays 10% less
    Given a VIP customer
    When they buy 100.00
    Then the total is 90.00
```

- Write in plain language, using glossary terms, one behavior per scenario.
- Include the edge cases the owner would recognize (a zero amount, a customer with no record, a failed payment).
- The owner reads and approves them before implementation. A changed scenario needs approval again.
- The scenarios become executable tests, and they have to pass before any delivery.
