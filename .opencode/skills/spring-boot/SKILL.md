---
name: spring-boot
description: Use when modifying a Java application that actually uses Spring Boot, Spring MVC, Spring Security, Spring Data, or Spring-managed configuration.
---

# Spring Boot Skill — Starter Guidance

## Supported scope

- Technology and version range: Spring Boot 2.7.x and 3.x+ on Java 17/21+ (inspect `pom.xml` or `build.gradle(.kts)` to confirm exact Spring Boot, Java, and `javax.*` vs `jakarta.*` namespace versions).
- Last reviewed: 2026-11
- Runtime/build tooling: Maven (`./mvnw`) and Gradle (`./gradlew`).
- Framework modules covered: Spring Web/MVC, Spring Validation, Spring Security, Spring Data JPA/JDBC, Spring Boot Actuator, and `@ConfigurationProperties`.
- Out-of-scope / unsupported versions: Spring Boot 1.x / early 2.0–2.6 without migration guidance, and non-Spring JVM frameworks (Quarkus, Micronaut, Ktor) unless explicitly bridging them.

## When to load

Load when modifying a Java/JVM application that uses Spring Boot, Spring MVC, Spring Security, Spring Data, or Spring-managed configuration. Do not load for non-JVM services or frontend-only changes.

## Before implementation

- Detect Java, Spring Boot, and build-tool versions from `pom.xml`, `build.gradle`, or `gradle/libs.versions.toml` before choosing APIs or annotations.
- Inspect the repository's package structure, constructor injection style, controller error-handling (`@RestControllerAdvice` / `ProblemDetail`), and transaction boundaries.
- Verify the exact Maven or Gradle wrapper commands and active test profiles before running builds or tests.

## Implementation standards

- Use constructor injection for mandatory dependencies; avoid field `@Autowired` injection in application components.
- Keep controllers/adapters focused on transport concerns (request binding, `@Valid` validation, HTTP status codes, response DTOs); keep domain rules in the service/domain layer and avoid exposing JPA entities directly in API responses.
- Enforce authentication and object/method-level authorization (`@PreAuthorize` / security filter chains) at trusted server boundaries.
- Scope `@Transactional` intentionally on service methods; avoid holding open database transactions across remote HTTP calls or message publishing, and guard against hidden lazy-loading (`LazyInitializationException`) and N+1 queries (use fetch joins, `@EntityGraph`, or projections where needed).
- Bind externalized configuration through typed, validated `@ConfigurationProperties` rather than scattered `@Value` strings; never commit secrets in `application*.yml` or `application*.properties`.

## Testing and verification

- Prefer fast JUnit 5 unit tests for isolated domain and service logic without booting the full Spring context.
- Use focused Spring test slices (`@WebMvcTest`, `@DataJpaTest`, `@JsonTest`) or `@SpringBootTest` + Testcontainers for real persistence, serialization, and security filter verification.
- Test validation failures (`400`), unauthenticated/unauthorized access (`401`/`403`), not-found cases (`404`), and transactional rollback behavior.

## Completion checklist

- [ ] Implementation matches the repository's actual Java and Spring Boot version (`jakarta.*` vs `javax.*`).
- [ ] Unit and applicable Spring slice/integration tests executed via `./mvnw` or `./gradlew`.
- [ ] Configuration properties, OpenAPI/API docs, and migrations updated where needed.
- [ ] No unapproved starter dependencies or broad transaction/N+1 regressions introduced.

## References

- Spring Boot reference documentation: https://docs.spring.io/spring-boot/index.html
- Spring Framework reference documentation: https://docs.spring.io/spring-framework/reference/
- Spring Security reference documentation: https://docs.spring.io/spring-security/reference/
