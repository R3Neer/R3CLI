---
type: question
---

# Portable Adapter Transport

## Question

Which value profile and protocol preserve native data and presentation requests across adapter/backend boundaries?

## Context

Human text must not replace typed rows, tree data or pipeline values. Strings, numbers, null, lists and named fields need explicit portable mappings. Arbitrary CLR objects, native callbacks and terminal handles cannot be assumed to cross a process boundary unchanged.

## Alternatives

- A versioned structured protocol with explicit type tagging where necessary.
- In-process integration where available, retaining a defined compatible logical value profile.
- A shared logical protocol with different physical transports per adapter.

## Resolution criterion

Specify supported values, precision/null/missing behavior, errors, request/event identity, lifecycle, streaming and metadata. Demonstrate Python/Nushell/PowerShell round trips without reverse-parsing human output.

## Affected documents

- [[docs/integration/adapter-boundaries]]
- [[docs/presentation/components/table]]
- [[docs/presentation/components/tree]]
- [[docs/presentation/output/README]]
