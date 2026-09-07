# Nushell adapter

R3CLI provides a native Nushell adapter for Nu 0.115 or newer. It implements the
same canonical palette, symbols, responsive wrapping, status hierarchy and help
contract as the Python and PowerShell implementations without requiring Python or
PowerShell at runtime.

## Build the distribution

From a clean R3CLI checkout:

```console
python scripts/build_nushell.py
```

The resulting module is written to `dist/nushell/r3cli/`. The build copies the
Nu module and MIT licence, generates `resources.json` from the canonical R3CLI
theme and symbols, and records deterministic SHA-256 hashes.

## Use the module

Point `use` at the built `r3cli` directory. A directory module exposes its
commands under the `r3cli` namespace:

```nu
use ./dist/nushell/r3cli

let ui = (r3cli console)
r3cli banner $ui 'MY TOOL 1.0'
r3cli status $ui step 'Reading the project'
r3cli status $ui success 'Project is ready.'
```

Import `*` when an unqualified API is more convenient:

```nu
use ./dist/nushell/r3cli *
let ui = (console --colour auto)
status $ui info 'Run with --help.'
```

## Public commands

| Command | Purpose |
|---|---|
| `console` | Create a rendering context with colour, ASCII and width policy. |
| `symbol` | Resolve a canonical status/rule symbol. |
| `line` | Print styled human text without returning it into the Nu pipeline. |
| `banner` | Render a product or command banner. |
| `heading` | Render an uppercase section heading. |
| `section` | Render a counted visual section. |
| `status` | Render `step`, `success`, `info`, `warning` or `error`. |
| `key-value` | Render a responsive key/value pair. |
| `table` | Render a compact table without truncating values. |
| `test-help-catalogue` | Validate the language-neutral help catalogue. |
| `help` | Render overview or command help from a catalogue. |
| `format-diagnostic` | Return plain, ANSI-free diagnostic text. |

Human rendering uses `print`, whose output type is `nothing`, so R3CLI text does
not become structured pipeline data. Warnings are written to stderr. Machine
output should remain a separate command/application concern and must not be fed
through the R3CLI renderer.

## Colour policy

`console` accepts `--colour auto|always|never`, `--ascii`, `--width`, and a
`--theme-extension` record. In `auto` mode rendering honours `NO_COLOR` and the
current stdout terminal. `always` explicitly overrides `NO_COLOR`.

```nu
let ui = (console --theme-extension { client: '#123456' })
```

Theme extensions must use `#RRGGBB`. Canonical roles cannot disappear; matching
keys may be overridden by the consumer.

For deterministic tests or embedding, `console` also accepts `--is-terminal` to
override terminal detection and `--sink` to receive rendered `(text, stream)`
values through a closure instead of printing them. Normal CLI consumers should
usually leave both unset.

## Help catalogue

The adapter accepts the language-neutral TOML shape directly:

```nu
let source = (open help.toml)
help $ui $source
help $ui $source check
```

It also accepts an already-flattened record containing `product`, `version`,
`description`, `invocation`, `group-order`, `usage`, `global-items`, `commands`,
`notes` and the corresponding per-command fields. `test-help-catalogue` rejects
duplicate commands/groups, incomplete items, unknown groups and optional dispatch
drift.

## Contract testing

The cross-language fixture in `tests/fixtures/console-contract.json` is shared
with the PowerShell contract. CI builds the packaged module, parses it with
`nu-check`, then runs `tests/run_nushell_contract.py`. The harness executes
`tests/Nushell.Contract.nu` under Nu 0.115.1, captures the process output and
checks exact ASCII/Unicode parity plus responsive rendering at several terminal
widths.
