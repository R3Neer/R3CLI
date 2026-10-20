---
type: question
---

# Default Output Scope

## Question

How is the default IOutput selected and scoped for facade calls and component.Show()?

## Context

Handle operations always address the original owner. Explicit output instances remain supported. Nested command/adapter sessions must not accidentally share a process-global mutable frame buffer or corrupt structured stdout.

## Alternatives

- An explicitly established lexical/session scope.
- A host-owned contextual default with defined nesting and restoration.
- A process-wide default only where a single-session host can demonstrate safe ownership.

## Resolution criterion

Specify creation, nesting, restoration, disposal, concurrent use and behavior without a configured default. Verify that changing defaults never retargets an existing handle.

## Affected documents

- [[docs/presentation/output]]
- [[docs/presentation/components/view]]
- [[docs/integration/adapter-boundaries]]
