---
type: question
---

# Help Selection Parsing

## Question

How does the parser delimit variadic section selections for --help/-h and --explain?

## Context

Zero section names means a full help page; --explain first requires a diagnostic code. Help must remain available without operational required arguments and must not execute operational work. Section selection preserves page order and rejects unknown/unavailable identifiers.

## Alternatives

- Treat help/explain as dedicated terminal routes with an explicit termination rule.
- Keep them in ordinary option parsing with a specified boundary at subsequent options and command tokens.

## Resolution criterion

Approve examples with missing command arguments, repeated help, multiple section IDs, subsequent flags, diagnostic codes, delimiters and unknown sections. Specify precedence without introducing an extra --sections option.

## Affected documents

- [[docs/command-system/help-routing]]
- [[docs/command-system/arguments-and-options]]
