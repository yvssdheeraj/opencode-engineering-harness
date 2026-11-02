---
name: spring-boot
description: Use when modifying a Java application that actually uses Spring Boot, Spring MVC, Spring Security, Spring Data, or Spring-managed configuration.
---

# Spring Boot Skill — Starter Guidance

- Detect Java and Spring Boot versions from the build and dependency management before using APIs.
- Follow the repository's package structure, dependency injection style, configuration, and exception conventions.
- Keep controllers/adapters focused on transport concerns; place business rules in the established service/domain layer.
- Validate external input at boundaries and enforce authorization server-side.
- Use transactions intentionally; avoid broad transaction scopes and hidden lazy-loading problems.
- Check JPA query behavior for N+1 access and unbounded fetching.
- Use the project's existing test stack; choose unit tests for business rules and Spring integration/slice tests for framework boundaries.
- Externalize environment-specific configuration and keep secrets out of source.
- Do not add Spring modules or dependencies without a concrete requirement.
- Verify the actual Gradle/Maven commands from the repository. These are starter guidelines, not a substitute for project conventions.
