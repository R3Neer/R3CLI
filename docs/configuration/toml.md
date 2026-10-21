---
type: configuration
---

# TOML configuration

The configuration file controls output preferences and token colours. It does not define components, execute callbacks or choose where applications install their data.

## Example

The RGB values below illustrate a valid palette; they do not select the built-in colours. Palette selection is documented in [[docs/questions/default-colours|Default colours]].

```toml
schema-version = 1

[output]
colour = "auto"
characters = "auto"
motion = "auto"
multiline-spacing = true
auto-activity-after-ms = 500

[presentation.table.alignment]
headers = "center"
number = "right"
text = "left"
boolean = "left"
date-time = "left"
duration = "left"
other = "left"
mixed = "left"

[tokens]
"text.foreground" = "#E8ECF2"
"subtext.foreground" = "#99A3B2"
"title.foreground" = "#C7A0FF"
"accent.foreground" = "#75C7F0"
"success.symbol.foreground" = "#7BD99A"
"warning.symbol.foreground" = "#F1C66D"
"failure.symbol.foreground" = "#FF8C9B"
"literal-block.background" = "#252B36"
```

## Reference

| Key | Accepted values | Default | Meaning |
|---|---|---|---|
| `schema-version` | Supported integer version | `1` when omitted | Configuration schema |
| `output.colour` | `"auto"`, `"always"`, `"never"` | `"auto"` | Whether human presentation emits colours |
| `output.characters` | `"auto"`, `"unicode"`, `"ascii"` | `"auto"` | Character repertoire |
| `output.motion` | `"auto"`, `"always"`, `"never"` | `"auto"` | Dynamic presentation preference |
| `output.multiline-spacing` | Boolean | `true` | Outer spacing for a complete multiline human response |
| `output.auto-activity-after-ms` | Nonnegative integer or `false` | `500` | Automatic command activity delay; `false` disables it |
| `presentation.table.alignment.headers` | `"left"`, `"center"`, `"right"` | `"center"` | Header alignment within each measured column |
| `presentation.table.alignment.number` | `"left"`, `"center"`, `"right"` | `"right"` | Auto alignment for numeric columns |
| `presentation.table.alignment.text`, `.boolean`, `.date-time`, `.duration`, `.other`, `.mixed` | `"left"`, `"center"`, `"right"` | `"left"` | Auto alignment for each original-value category |
| `tokens` | String-to-colour table | Built-in standard values | Partial standard overrides and custom token values |

Zero activity delay means immediate display. `true` and negative delays are invalid. There is no separate enabled switch and no configurable spinner frame interval here. A deliberately different cadence belongs to `TimedFrames` in code.

Colour, character repertoire and motion are independent. Disabling motion uses stable output rather than dropping useful results or errors. `"always"` cannot make cursor editing possible in a file and never adds decoration to structured output. Exact capability detection must be verified by the terminal implementation.

### Table alignment

Column Alignment.Auto consults the configured original-value category. Ignore null while classifying; all-null columns use other. Numbers represented by strings remain text. Headers align independently inside each calculated column width. Only left, center and right are valid configuration values: neither auto nor column is a TOML alignment. Explicit Column alignment overrides the configured cell default but not the independent header policy. Cell formatting never changes original values or their classification. [[docs/presentation/components/table|Table]] owns measurement, wrapping and fallback behavior.

### Spacing

With `multiline-spacing = true`, a complete multiline human response requests one blank line before and after itself. Children and animation frames do not each receive that spacing. Automatic margins collapse by maximum rather than addition. Explicit `BlankLine` remains additional block content, and structured values receive no decorative whitespace.

See [[docs/presentation/text-and-layout|Text and layout]] for the component-specific lower margins and narrow-width behavior.

## Resolution rules

1. Built-in defaults establish output preferences and standard token values.
2. The loaded TOML overrides those values.
3. Explicit Column alignment overrides its configured cell-category default.
4. An explicit node policy overrides the general automatic-activity setting.

An omitted command policy inherits configuration; there is no additional parent-command policy chain. See [[docs/command-system/automatic-activity|Automatic activity]].

The application or adapter chooses the configuration path. R3CLI does not implicitly search globally for another application's TOML. No named-theme loader, colour expression engine, palette aliases or theme inheritance is part of this schema.

## Validation

- Unknown structural keys, unsupported schema versions and incorrect setting types are errors.
- Reject unknown alignment categories, wrong types and values outside left/center/right.
- Arbitrary keys under `[tokens]` are allowed, including unused custom names.
- RGB colours use `#RRGGBB`; foregrounds also accept `"terminal-default"`.
- `literal-block.background` requires explicit RGB.
- Report the configuration file, key and cause when validation fails.
- Help and configuration-error explanations remain available through a basic default presentation when configuration is invalid.

```toml
[output]
auto-activity-after-ms = false

[tokens]
"project.path.foreground" = "#A7D8A0"
```

This disables automatic command activity and defines a custom colour without registration. Standard omitted tokens retain their defaults. See [[docs/configuration/colour-tokens|Colour tokens]] for lookup rules.
