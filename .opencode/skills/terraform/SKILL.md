---
name: terraform
description: Use when the repository uses Terraform/OpenTofu and a task changes providers, modules, resources, state, variables, or infrastructure plans.
---

# Terraform Skill — Starter Guidance

- Detect Terraform/OpenTofu and provider versions, backend, workspace/environment model, and module conventions.
- Inspect state/configuration boundaries without exposing secrets.
- Keep modules focused, inputs/outputs typed, names stable, and provider versions constrained.
- Treat state as sensitive; never commit it or print secret-bearing outputs.
- Run formatting and validation, then inspect a plan before any apply.
- Review replacements, deletions, IAM/network exposure, cost, drift, and data-loss implications.
- Do not run apply/destroy against production without explicit authorization.
- Keep environment-specific values outside reusable module code and use the approved secret mechanism.
