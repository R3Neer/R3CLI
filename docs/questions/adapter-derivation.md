---
type: question
---

# Adapter Contract Derivation

## Question

How does an adapter declare reusable specializations of supported authoring contracts?

## Context

Ordinary custom sections, nodes and compositions should not require writing C#. The intended direction normalizes native declarations to compiled backend representations; arbitrary runtime CLR subclass generation is not promised. There is no CustomHelpSection fallback class.

## Alternatives

- Declarative specializations with supported properties and callback slots.
- Native-language wrapper types that produce the same validated descriptions.
- A small combination where declarations describe reusable structure and callbacks remain local.

## Resolution criterion

Define supported bases, constructor/instance semantics, override points, validation and callback lifetime, then express a custom help section and a typed tree node idiomatically in each adapter.

## Affected documents

- [[docs/integration/adapter-boundaries]]
- [[docs/presentation/components/help]]
- [[docs/presentation/components/tree]]
