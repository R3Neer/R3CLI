---
type: configuration
---

# Colour tokens

A colour token names the role of a visible part. Standard components select their tokens automatically; composing components preserves each piece's token. Eight tokens do not imply eight different RGB values.

## Reference

| Token | Uses |
|---|---|
| `text.foreground` | Main text, normal message bodies, completed progress and literal-block text |
| `subtext.foreground` | Secondary text, Field labels/default colons, TabLeader fill, Section counters, table headers, separators, tree connectors, pending progress and syntax delimiters |
| `title.foreground` | Title, including Section and Banner titles |
| `accent.foreground` | Command, help option names, Info and Activity indicators, Spinner |
| `success.symbol.foreground` | Success and successful-task indicators |
| `warning.symbol.foreground` | Warning indicator |
| `failure.symbol.foreground` | Failure, error and failed-task indicators |
| `literal-block.background` | LiteralBlock rectangle, including horizontal padding |

Title retains its own colour role. Line, View, whitespace and Symbol itself own no colour tokens. A Symbol acquires its role from the component using it.

[[docs/presentation/components/tab-leader|TabLeader]] reuses `subtext.foreground` for its optional visible fill; it adds no ninth token. An explicit Field separator replaces the normal colon and space, while an omitted separator keeps them.

## Example

```toml
[tokens]
"title.foreground" = "#C7A0FF"
"accent.foreground" = "#75C7F0"
"project.path.foreground" = "#A7D8A0"
```

Values are `#RRGGBB`. Foreground tokens may use `"terminal-default"`; the literal-block background requires explicit RGB. Omitted standard tokens retain built-in defaults. The final built-in RGB selection is addressed in [[docs/questions/default-colours|Default colours]].

## Resolution rules

The `[tokens]` table is a string-to-colour dictionary. A custom piece references a name and obtains the configured value through exact, case-sensitive lookup. No registration, manifest, declaration list or mandatory fallback is required.

- Custom names are allowed even when unused.
- Configured values are validated at load time.
- Referencing a missing custom token fails clearly before that presentation is emitted.
- Standard calls such as `new Warning(...)` do not acquire per-instance token arguments.
- Customization extends the vocabulary without changing the meaning of standard tokens.

The spelling of the adapter authoring API belongs to [[docs/integration/adapter-boundaries|Adapter boundaries]]; a token dictionary does not itself define new rendering behavior.

## Validation

Reject malformed colour values before rendering and report the file, key and cause. A referenced custom name that is not configured is an error; an unused configured name is not. There are no named themes or theme inheritance. Sharing a palette means copying token entries. Version 1 has no aliases between token names, formulas or computed colour expressions. The literal-block background is supplied explicitly; rendering does not assume that the terminal's real background is known.

For the complete file schema and validation, see [[docs/configuration/toml|TOML configuration]].
