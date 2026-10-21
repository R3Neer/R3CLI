---
type: index
---

# Integration

R3CLI has a shared C# backend and idiomatic language-facing adapters. Integration preserves the distinction between data, presentation and output lifetime.

## Contents

- [[docs/integration/build-baseline|Build baseline]] defines C# 15 preview and compiler verification.

- [[docs/integration/adapter-boundaries|Adapter boundaries]] — supported responsibilities, customization and structured data.

## Reading guide

Read Adapter boundaries alongside the component whose values or callbacks an adapter exposes. Backend deployment is addressed in [[docs/questions/native-aot-or-jit|Native AOT or JIT]]. The exact transport and reusable adapter specializations are addressed in [[docs/questions/adapter-transport|Adapter transport]] and [[docs/questions/adapter-derivation|Adapter derivation]].
