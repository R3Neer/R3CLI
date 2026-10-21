---
type: index
---

# Configuration

Configuration controls human-output preferences and the colours associated with semantic tokens. Components select their standard tokens automatically; ordinary calls do not pass colours.

## Contents

- [[docs/configuration/toml|TOML configuration]] defines settings, defaults, precedence and validation.
- [[docs/configuration/built-in-themes|Built-in themes]] defines the catalog, exact token values and automatic selection.
- [[docs/configuration/colour-tokens|Colour tokens]] defines the eight standard names and custom-token lookup.

## Reading guide

Start with the file schema, then use the token reference when authoring a component or selecting colours. Select a built-in theme or omit the setting for automatic selection; override individual [tokens] as needed. Custom/imported themes and inheritance are unsupported. Background preservation is the default. Configuration file discovery belongs to the application or adapter rather than an implicit global scan.

See [[docs/presentation/text-and-layout|Text and layout]] for the behavior controlled by the output preferences, and [[docs/command-system/automatic-activity|Automatic activity]] for command-specific overrides.
