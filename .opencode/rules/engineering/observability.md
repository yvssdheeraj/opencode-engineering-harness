# Engineering Rule — Observability and Monitoring (OBS)

Observability should help operators understand system behavior and diagnose failures without exposing sensitive data.

| ID | Requirement | Agent must enforce |
|---|---|---|
| OBS-01 | Structured logging | Use consistent structured logs with appropriate severity, timestamp, service, and contextual fields. |
| OBS-02 | Meaningful events | Log important state transitions, errors, and operationally relevant business events without noisy or redundant messages. |
| OBS-03 | Metrics | Expose meaningful service, resource, dependency, and business metrics where useful. Avoid unbounded/high-cardinality labels. |
| OBS-04 | Distributed tracing | Propagate trace context across service and asynchronous boundaries where distributed diagnosis is required. |
| OBS-05 | Correlation IDs | Correlate requests, jobs, and related operations across logs and telemetry. Do not trust arbitrary incoming IDs without validation. |
| OBS-06 | Error monitoring | Make unexpected failures and significant error rates discoverable with actionable context. |
| OBS-07 | Health information | Provide appropriate liveness, readiness, and dependency health indicators. |
| OBS-08 | Alertability | Ensure critical failure modes can trigger meaningful alerts with ownership and runbook guidance. |
| OBS-09 | Sensitive data filtering | Redact or omit secrets, tokens, credentials, personal data, and sensitive payloads from logs and telemetry. |
| OBS-10 | Business observability | Measure important business outcomes and workflow states when those metrics help diagnose or operate the product. |

## Telemetry guidance

- Prefer OpenTelemetry-compatible instrumentation when it fits the stack.
- Add observability proportionate to operational importance; do not add telemetry noise for every trivial helper.
- Document new metrics, dashboards, alerts, and runbook implications when material.
