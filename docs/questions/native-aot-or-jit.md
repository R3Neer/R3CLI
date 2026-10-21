---
type: question
---

# Backend Deployment Mode

## Question

Should the backend use Native AOT, JIT deployment, or separately justified artifacts for different consumption paths?

## Context

The language is C#. R3CLI has multiple language consumers, live presentation, customization and startup-sensitive commands. ModpackTools' deployment decision does not automatically select R3CLI's deployment mode.

## Alternatives

- Native AOT artifacts: evaluate startup, distribution size, platform builds and supported customization.
- JIT deployment: evaluate runtime prerequisites, startup and integration.
- Multiple artifacts only if their distinct consumers justify the maintenance cost.

## Resolution criterion

Compare representative startup, rendering, adapter communication and distribution requirements; explicitly choose supported artifacts without promising arbitrary reflection/runtime subclass generation.

## Affected documents

- [[docs/integration/adapter-boundaries]]
- [[docs/presentation/output/README]]
