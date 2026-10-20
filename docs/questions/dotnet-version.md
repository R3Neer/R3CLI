---
type: question
---

# Stable .NET Baseline

## Question

Which stable .NET SDK and C# language version define the supported build baseline?

## Context

C# is the backend language. Contracts may use primary constructors and modern stable extension syntax where useful. No preview feature or exact installed SDK has been made a requirement by the visual contracts.

## Alternatives

- Select a supported stable baseline that directly supports the preferred extension-block spelling.
- Select another supported stable baseline and express equivalent extension behavior using the available syntax.

## Resolution criterion

Select the baseline after checking required language features, platform support and the deployment decision, without changing public semantics merely for syntactic convenience.

## Affected documents

- [[docs/presentation/output]]
- [[docs/integration/adapter-boundaries]]
