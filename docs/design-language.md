# R3CLI design language

## Hierarchy

- **Heading** establishes structure and product identity.
- **Accent** marks commands, selectors and values the user can act on.
- **Secondary** carries descriptions, paths and supporting context.
- **Value** carries primary content.
- **Success**, **process** and **error** communicate state together with a
  symbol or explicit word; colour is never the only signal.

The canonical palette is stored in `default_theme.toml`. Product-only roles
belong in consumer themes rather than the universal palette.

## Composition

- A banner uses a double horizontal rule and one bold product title.
- Help uses uppercase section names, indented command rows and aligned labels.
- Work in progress uses `→`; success uses `✓`; information uses `•`; warnings
  use `!`; failures use `✗`. ASCII fallbacks are `>`, `+`, `*`, `!` and `x`.
- Tables avoid ornamental borders unless a border materially improves reading.
- Output ends cleanly and does not depend on a particular background colour.

## Errors

Expected failures follow this order:

```text
What failed and, when useful, which value caused it.
Details: Technical or upstream context.
Try: One concrete recovery action
```

The first sentence names the subject. Commands appear only in `Try:`. Each
application attaches a stable error code. Unexpected programming exceptions
retain their traceback.

## Terminal and automation contract

`--colour` overrides environment detection. `NO_COLOR` disables colour.
Automatic mode emits colour only to a terminal. Unicode has an ASCII fallback,
layouts contract to the available width, and JSON or redirected data never
contains presentation escape sequences. Human progress and diagnostics use
stderr whenever stdout carries data.
