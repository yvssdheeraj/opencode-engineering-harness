# Engineering Rule — Reliability and Resilience (REL)

Apply these controls according to service criticality, failure modes, and recovery objectives.

| ID | Requirement | Agent must enforce |
|---|---|---|
| REL-01 | Predictable failure | Define and handle expected failure modes consistently; avoid ambiguous partial success. |
| REL-02 | Timeouts | Set bounded timeouts for network calls, database operations, and other potentially blocking external work. |
| REL-03 | Retry strategy | Retry only transient, safe-to-retry failures; use bounded attempts, backoff, jitter where appropriate, and an overall deadline. |
| REL-04 | Idempotency | Make retryable or externally retried operations idempotent where duplicate execution could cause harm. |
| REL-05 | Circuit breaking | Consider circuit breakers or equivalent load-shedding when repeated dependency failures can amplify outages. |
| REL-06 | Fault isolation | Prevent a failure in one component, tenant, or optional dependency from unnecessarily cascading into unrelated functionality. |
| REL-07 | Transaction integrity | Preserve atomicity and consistency across operations; document and test distributed consistency where a single transaction is not possible. |
| REL-08 | Recovery | Provide recovery paths for failed jobs, interrupted operations, and corrupted or unavailable dependencies where relevant. |
| REL-09 | Health checks | Expose meaningful liveness/readiness/dependency health signals without disclosing sensitive internal details. |
| REL-10 | Graceful shutdown | Stop accepting work, finish or safely cancel in-flight work, and release resources appropriately. |
| REL-11 | Failure testing | Test relevant timeouts, dependency outages, partial failures, retries, duplicate delivery, and recovery. |
| REL-12 | Disaster recovery | Define and validate backup, restore, failover, RTO, and RPO expectations for systems where business continuity requires them. |

## Reliability cautions

- Avoid retry storms and retrying non-idempotent operations without protection.
- Do not treat health-check success as proof of end-to-end business correctness.
- Document consistency trade-offs for asynchronous and distributed operations.
