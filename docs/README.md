---
type: index
---

# R3CLI Reference

This is the current specification for R3CLI's C# backend and language adapters. It defines the new API; it does not claim that the released Python, Nushell or PowerShell implementation already provides it. Documentation previews illustrate the specified appearance without executing R3CLI.

## Contents

| Area | Entry point | Responsibility |
|---|---|---|
| Overall design | [[docs/structure]] | Data, components, output and commands in one worked example |
| General class diagram | [[docs/class-diagram]] | Relationships between the shared API types |
| Presentation | [[docs/presentation/README]] | Components, composition and layout |
| Output | [[docs/presentation/output/README]] | Borrowed .NET writers, scoped sessions, capabilities and handles |
| Presentation architecture | [[docs/presentation/architecture/README]] | Internal design sequence and Spectre.Console delegation |
| Configuration | [[docs/configuration/README]] | Built-in themes, automatic selection, background policy and token overrides |
| Command System | [[docs/command-system/README]] | Parent-defined commands, help, diagnostics and activity |
| Integration | [[docs/integration/README]] | Idiomatic adapters and native structured-data boundaries |
| Questions | [[docs/questions/README]] | Concrete decisions that remain outside the closed visual contracts |
| Documentation rules | [[docs/documentation-rules]] | Current-only content, templates, links and visual evidence |

## Reading guide

Start with Structure and the general diagram. Open the relevant Presentation Component page for its contract, examples and preview. Configuration controls presentation without changing component meaning. Command System integrates definitions and execution with presentation; Integration separates native data from human terminal output.

Use [[docs/presentation/components/tab-leader|TabLeader]] for a shared target width with spaces or a Symbol pattern. [[docs/presentation/components/table|Table]] accepts explicit Columns or header strings followed by at least one data row. Its source-selector factory accepts existing application objects without manual Row conversion.

Documents contain the current contract only. Questions have their own documents and do not silently define reference behavior. Template definitions are under `docs/templates/`; the sole metadata property is `type`.
