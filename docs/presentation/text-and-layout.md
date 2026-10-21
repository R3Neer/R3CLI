---
type: concept
---

# Text and layout

All Presentation Components share a terminal-cell layout policy. The human presentation never rewrites the original domain values.

## Responsibilities

Define shared human-presentation behavior for logical line breaks, graphemes, terminal-cell widths, controls and spacing. Component documents specialize these rules; adapters retain original data separately.

## Rules

### Text contract

| Content | Explicit line breaks |
|---|---|
| Text, Subtext, LiteralBlock | Allowed |
| Table cells | Allowed through supported inline content |
| Line | Preserves ordered inline content, including permitted breaks |
| Title, headers, labels, codes, Command, Field values | Rejected; one logical line |
| Symbol | Rejected; stricter printable-pattern validation |

Logical line breaks and physical wrapping are different. A single-line label may wrap when the terminal is narrow. LF and CRLF are equivalent presentation breaks; preserve stored content and explicit internal empty lines. Empty Text does not itself force an empty block line. BlankLine is block-only and cannot be passed to Line.

### Unicode and controls

Reject malformed Unicode. Segment extended grapheme clusters and measure terminal cells, never UTF-16 length. Do not split graphemes or destroy legitimate emoji/joiner sequences.

Text, Subtext and LiteralBlock never interpret embedded ANSI. Unsupported controls and bidi controls render as visible escapes, such as \\u001B. Admitted line breaks keep their layout function. LiteralBlock tabs expand to four-cell stops relative to its content origin; outside it a tab is visible as \\t. Structural single-line fields and Symbol reject controls. There is no raw-terminal escape hatch.

Cell width depends on a supported terminal profile, and valid Unicode is not a guarantee that every font draws connected or identically sized glyphs. Real-terminal verification is required at implementation time.

### Theme and background scope

Colours resolve through [[docs/configuration/built-in-themes|Built-in themes]] and explicit token overrides. General backgrounds are preserved unless output.background explicitly requests a theme fill over the owned region. A theme's reference background is selection metadata, not a mandatory painted surface. LiteralBlock owns its local rectangle. Colour-disabled and structured output receive no coloured fills or background queries. Automatic detection uses the terminal's reported base RGB, not a screenshot or transparency-composited pixel average.

### Wrapping and narrow output

Prefer word breaks, then wrap overlong words at grapheme boundaries. Do not silently truncate or add ellipses. Reduce decoration, indentation and padding before losing content. A grapheme wider than the complete available width gets a visible escapable representation that can itself wrap.

A known zero width emits no presentation. An unknown width uses a reference of 80 cells.

| Component | Width fallback |
|---|---|
| Messages | Wrap continuations under the body where possible |
| Section | Reduce indentation |
| Separator | Emit only whole fitting graphemes |
| LiteralBlock | Reduce padding, then wrap its interior |
| Table | Wrap cells; use labelled vertical records when column minimums do not fit |
| Tree | Compact indentation/connectors; use linear traversal when branch plus content cannot fit |

Table minimum column width is min(natural width, 8 cells); include intercolumn gaps in the fit check. A fallback changes human layout, never row values or hierarchy.

### Spacing

Automatic outer spacing adds one empty line before and after a complete multiline human response when multiline-spacing is enabled. It does not apply independently to every child or update. It never decorates structured values.

| Complete block | Lower margin before following content |
|---|---|
| LiteralBlock, Table, Tree, Diagnostic, Banner, Section, whole progress group | One empty line |
| Text, Subtext, Command, Line, Field, standard messages | None |
| Title, Separator | None independently; enclosing composition decides |
| Tree nodes and individual stages | None inside the group |

Adjacent and nested automatic requests collapse by maximum, not addition. Materialize a lower margin only at a boundary with following content. Coordinate complete-response spacing with those requests. BlankLine is explicit additional content. View updates do not accumulate margins. Stable output does not surround every progress event with blanks.

### Continuous rules and branches

Section root with nested sections uses ═; level two and a flat root use ─; level three and deeper use -. Standalone Separator defaults to ─. No empty line separates a title from its rule. Banner independently defaults to =.

Tree uses one consistent light box-drawing family: │, ─, ├ and └. Each normal level occupies four cells; retain ancestor continuations on wrapped node lines. Unicode/ASCII selection changes characters without changing the underlying structure.

## Alignment padding

[[docs/presentation/components/tab-leader|TabLeader]] measures the complete preceding logical prefix in cells, excluding structural indentation. It fills to a target using spaces or whole fitting pattern graphemes, then fills leftover cells with spaces. Reaching or exceeding the target adds at least one ordinary space. Padding, including trailing spaces, is retained; only Separator uses generated-rule trailing-space trimming. A TabLeader can be inline inside Line or supplied as the separator of Field.

## Configuration boundary

[[docs/configuration/toml|TOML]] owns colour, character and motion preferences and complete-response spacing. There are no per-component margin, indentation, bar-width, padding or frame-cadence settings in the initial schema.

## Example

```csharp
Output.Show(
    new Line("Name: ", new Subtext("demo")),
    new BlankLine(),
    new LiteralBlock("Name    Status\ndemo    ready"));
```

The first argument joins two inline pieces. BlankLine is a separate block, never an item in Line. The literal block retains its explicit line break, shares one background rectangle and requests a lower margin only if later content follows.
