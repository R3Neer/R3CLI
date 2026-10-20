---
type: question
---

# Typed CLI Values

## Question

What public definitions describe argument/option value types and conversion consistently across consumers?

## Context

Names, requiredness, cardinality, defaults and choices drive parsing and generated help. String-only type identifiers are not a sufficient typed C# API, and unrestricted object payloads do not define portable semantics.

## Alternatives

- A closed portable set with explicit extension points.
- Typed descriptors normalized by adapters to a shared logical model.
- A combination that preserves common native ergonomics without permitting unspecified conversions.

## Resolution criterion

Define conversion, repetition, defaults, choices, missing/null, diagnostics and adapter mappings; demonstrate several commands without requiring duplicated help metadata.

## Affected documents

- [[docs/command-system/arguments-and-options]]
- [[docs/command-system/help-routing]]
- [[docs/presentation/components/help]]
