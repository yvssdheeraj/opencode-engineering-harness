# Engineering Rule — API and Integration Design (API)

Apply the HTTP-specific rules to HTTP APIs and the contract/evolution rules to other service, event, and message interfaces as appropriate.

| ID | Requirement | Agent must enforce |
|---|---|---|
| API-01 | Clear contracts | Define request, response, error, event, and compatibility contracts for integration boundaries. |
| API-02 | Consistent response shapes | Use consistent success and error representations within the existing API conventions. |
| API-03 | Correct HTTP semantics | Use HTTP methods, status codes, caching semantics, and headers appropriately for HTTP APIs. |
| API-04 | Versioning strategy | Define how externally consumed contracts evolve and when versioning or compatibility windows are needed. |
| API-05 | Schema validation | Define and validate payload schemas, types, required fields, constraints, and size limits. |
| API-06 | Stable error contracts | Return machine-readable, stable error codes and safe messages; do not make clients parse arbitrary exception text. |
| API-07 | Endpoint security | Apply authentication, authorization, tenant isolation, and input/output protections at the trusted boundary. |
| API-08 | Rate limiting and abuse controls | Protect exposed or expensive operations with suitable throttling, quotas, and abuse detection. |
| API-09 | Idempotency | Support idempotency keys or equivalent safeguards for operations where retries or duplicate requests can cause duplicate effects. |
| API-10 | API documentation | Keep OpenAPI or equivalent docs, examples, schemas, and usage guidance aligned with actual behavior. |
| API-11 | Backward compatibility | Assess existing consumers before changing fields, semantics, error codes, ordering, defaults, or endpoint behavior. |
| API-12 | Integration isolation | Encapsulate external provider behavior behind suitable adapters/clients; avoid leaking provider-specific models throughout the domain. |
| API-13 | Contract validation | Test provider/consumer assumptions, schemas, compatibility, and relevant failure behavior. |
| API-14 | Schema evolution | Plan safe evolution for events, messages, payloads, and persisted contracts, including old/new producer-consumer coexistence where relevant. |

## Integration behavior

- Define timeout, retry, idempotency, authentication, observability, and failure behavior for external calls.
- Avoid logging full request/response payloads when they may contain secrets or personal data.
- Document ownership and compatibility expectations for shared contracts.
