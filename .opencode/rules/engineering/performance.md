# Engineering Rule — Performance and Scalability (PERF)

Do not optimize blindly. Identify performance expectations, measure important paths, and prioritize bottlenecks that affect user experience, cost, throughput, or reliability.

| ID | Requirement | Agent must enforce |
|---|---|---|
| PERF-01 | Performance awareness | Consider latency, throughput, memory, CPU, storage, and network impact for changed behavior. Avoid obviously wasteful work. |
| PERF-02 | Algorithmic complexity | Consider time/space complexity for large collections, hot paths, and unbounded inputs; choose suitable data structures and algorithms. |
| PERF-03 | Efficient data access | Avoid N+1 queries, repeated fetching, chatty service calls, and unnecessary serialization or transfer. |
| PERF-04 | Resource lifecycle | Close/release files, streams, sockets, connections, locks, and other owned resources reliably. |
| PERF-05 | Caching discipline | Introduce caching only with a clear key, TTL/invalidation, consistency, privacy, and failure strategy. Do not cache sensitive data unsafely. |
| PERF-06 | Pagination and bounded results | Avoid unbounded list responses or scans; paginate, stream, or limit results appropriately. |
| PERF-07 | Lazy loading | Defer expensive resources or computation until they are needed, while avoiding hidden N+1 behavior. |
| PERF-08 | Concurrency | Use concurrency only where beneficial and safe; account for ordering, races, synchronization, cancellation, and resource limits. |
| PERF-09 | Backpressure | Bound queues and work; protect downstream services from overload using throttling, bounded concurrency, or backpressure mechanisms. |
| PERF-10 | Measurement and benchmarking | Benchmark or profile important paths using representative workloads before claiming an optimization. |
| PERF-11 | Resource limits | Set and validate appropriate limits for payloads, uploads, requests, jobs, memory, processing time, and concurrency. |
| PERF-12 | Graceful degradation | Preserve essential functionality when optional or non-critical capabilities are slow or unavailable. |

## Performance review

For material performance-sensitive changes, record the workload, baseline, measurement method, result, and any trade-offs. Do not introduce complex caching or concurrency without evidence and operational visibility.
