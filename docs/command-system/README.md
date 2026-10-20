---
type: index
---

# Command System

The Command System describes commands, generates their help and coordinates execution-facing behavior. It is distinct from the visual `Command` component and from the presentation `Tree`.

## Contents

- [[docs/command-system/command-tree|Command tree]] — parent declarations and command identity.
- [[docs/command-system/arguments-and-options|Arguments and options]] — one source of command syntax and value metadata.
- [[docs/command-system/help-routing|Help routing]] — command help, section selection and diagnostic explanations.
- [[docs/command-system/diagnostics|Diagnostics]] — error boundaries and documented diagnostic codes.
- [[docs/command-system/automatic-activity|Automatic activity]] — delayed indicators and command overrides.

## Reading guide

Read Command tree first, then Arguments and options. Help routing and Diagnostics explain metadata and failure presentation; Automatic activity covers the execution feedback policy. The C# contracts describe the shared backend. Python, Nushell and PowerShell provide idiomatic authoring and consumption through [[docs/integration/adapter-boundaries|Adapter boundaries]]. The documents specify design contracts rather than a claim that a parser or native runtime has already been implemented.
