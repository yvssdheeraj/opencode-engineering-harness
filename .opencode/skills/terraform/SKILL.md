---
name: terraform
description: Use when the repository uses Terraform/OpenTofu and a task changes providers, modules, resources, state, variables, or infrastructure plans.
---

# Terraform Skill — Starter Guidance

## Supported scope

- Technology and version range: Terraform 1.5+ and OpenTofu 1.6+ (inspect `required_version`, `.terraform.lock.hcl`, and CI workflows for exact CLI and provider versions).
- Last reviewed: 2026-11
- Runtime/build tooling: `terraform` / `tofu`, `tflint`, `trivy` / `checkov`, and repository wrapper scripts.
- Framework modules covered: root configurations, reusable modules, providers, state backends, variables/outputs, IAM/network resources, and plan inspection.
- Out-of-scope / unsupported versions: Legacy Terraform (< 0.15) syntax, imperative cloud CLIs, Pulumi, CloudFormation/CDK, or Kubernetes application manifests unless managed via Terraform.

## When to load

Load when the repository uses Terraform or OpenTofu and a task changes providers, modules, resources, state configuration, variables, outputs, or infrastructure plans. Do not load for application-only code changes.

## Before implementation

- Detect whether the project uses `terraform` or `tofu`, required CLI/provider versions, state backend configuration, workspace/environment layout, and module structure.
- Inspect state and variable boundaries without printing or exposing secret values.
- Confirm which validation commands (`fmt -check`, `validate`, `tflint`, security scanners) can run locally without cloud credentials or state mutations.

## Implementation standards

- Constrain `required_version` and provider version ranges explicitly; keep reusable modules focused with typed `variable` definitions, `validation` blocks where helpful, and clear `description` fields.
- Keep environment-specific values out of reusable module code; pass them via root-module variables or approved secret references.
- Mark sensitive inputs and outputs with `sensitive = true`, and remember that Terraform/OpenTofu state still stores plaintext values—never commit `.tfstate` files, `.tfvars` containing secrets, or unencrypted plan files.
- Apply least privilege to IAM policies, security groups, and network ingress/egress rules; use `lifecycle` blocks (`prevent_destroy`, `create_before_destroy`) deliberately for stateful resources.
- Review any resource address rename carefully and use `moved` blocks where supported to avoid unintended destroy/recreate operations.

## Testing and verification

- Run `terraform fmt -check` (or `tofu fmt -check`) and `validate` (with `-backend=false` when remote state access is unavailable or unapproved).
- Run configured linters/policy checks (`tflint`, `trivy config`, `checkov`, `terraform test` / `tofu test`) when present in the repository.
- Always inspect `plan` output for unexpected replacements (`-/+` or `destroy`), IAM broadening, network exposure, or stateful data loss before any apply; never run `apply` or `destroy` against shared/production environments without explicit user authorization (`INFRA-20`, `AUTO-06`).

## Completion checklist

- [ ] Implementation matches the project's Terraform/OpenTofu and provider version constraints.
- [ ] Formatting, validation, and applicable static/security checks executed.
- [ ] Resource replacement, state migration (`moved`), IAM, and cost/availability impacts reviewed.
- [ ] No secrets, `.tfstate` artifacts, or unapproved `apply`/`destroy` actions executed.

## References

- Terraform language documentation: https://developer.hashicorp.com/terraform/language
- OpenTofu documentation: https://opentofu.org/docs/
