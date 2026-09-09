# R3CLI

[![CI](https://github.com/R3Neer/R3CLI/actions/workflows/ci.yml/badge.svg)](https://github.com/R3Neer/R3CLI/actions/workflows/ci.yml)

R3CLI is the shared command-line presentation layer for R3Neer's tools.

It provides one visual language and one help model across Python, PowerShell and Nushell without turning presentation into the source of truth for program data.

```text
product/domain code
       │
       ├── structured data / machine channel
       │
       └── semantic presentation calls
                    │
                    ▼
                  R3CLI
          ┌─────────┼─────────┐
          ▼         ▼         ▼
        Python   PowerShell  Nushell
```

The design originated in ModpackTools and was extracted so other tools can reuse the same hierarchy, colour semantics, symbols, wrapping and help behaviour without copying UI code.

## Design goals

R3CLI is deliberately small. It is responsible for:

- banners, headings, sections and readable spacing;
- semantic status messages;
- key/value layouts and compact tables;
- consistent symbols with ASCII fallbacks;
- colour policy, including `auto`, `always`, `never` and `NO_COLOR`;
- deterministic wrapping against terminal width;
- expected CLI error presentation;
- one validated catalogue model for generated help;
- equivalent PowerShell and Nushell adapters built from the same canonical resources.

R3CLI is **not** a domain framework, command router, persistence layer or machine-output format. Products keep those responsibilities themselves.

Human rendering should remain separable from structured program output.

## Visual language

The default theme uses semantic roles rather than product-specific hard-coded colours:

```text
structure / headings    cyan
process / actions       orange
secondary context       quiet neutral
values                  primary value colour
success                 green + symbol
warning                 orange + symbol
error                   red + symbol
```

Colour is never the only signal. Status meaning is paired with symbols, and every renderer can fall back to ASCII.

See [`docs/design-language.md`](docs/design-language.md) for the full visual contract.

## Python quick start

Install the package in a development checkout:

```console
python -m pip install -e ".[test]"
```

Then use semantic UI operations:

```python
from r3_cli import ConsoleUI

ui = ConsoleUI()
ui.banner("MY TOOL 1.0")
ui.step("Reading the project")
ui.success("Project is ready.")
```

The public Python package also exposes the shared help and error models:

```python
from r3_cli import (
    CliError,
    ColourMode,
    CommandHelp,
    ConsoleUI,
    HelpCatalogue,
    HelpItem,
    HelpRequest,
    R3ArgumentParser,
    Theme,
    add_output_arguments,
    compose_theme,
    load_help_catalogue,
    load_theme,
    resolve_help_request,
    validate_argparse_catalogue,
)
```

`R3ArgumentParser` and `add_output_arguments` integrate the presentation policy with argparse without requiring product code to hand-format standard output controls.

## UI primitives

The adapters expose the same conceptual vocabulary even where host-language syntax differs.

Common primitives include:

- `banner`;
- `heading`;
- `section`;
- `status` / semantic success, warning and error presentation;
- `line` with semantic segments;
- `key-value`;
- `table`;
- symbol lookup;
- help catalogue validation and rendering.

The intent is semantic composition. Product code says what a fragment *means*; the renderer decides how that role is represented in colour, ASCII/Unicode and available terminal width.

## Help from one catalogue

R3CLI can render a ModpackTools-style command overview and focused command pages from one validated catalogue.

A catalogue describes:

- product name and description;
- invocation;
- group order;
- commands and summaries;
- usage forms;
- global and command-specific items;
- notes;
- examples;
- help options.

The same catalogue can therefore drive overview help, focused help and contract tests instead of maintaining separate prose fragments for each renderer.

See:

- [`docs/help-system.md`](docs/help-system.md);
- [`templates/help-catalogue.toml`](templates/help-catalogue.toml).

## Nushell adapter

R3CLI includes an official native Nushell adapter for Nu 0.115+.

```nu
use ./nushell/r3cli

let ui = (r3cli console --colour auto)
r3cli banner $ui 'MY TOOL 1.0'
r3cli status $ui step 'Reading project'
r3cli key-value $ui 'Version' '1.0.0'
```

The adapter does not require Python at runtime. Canonical colours and symbols are packaged into deterministic adapter resources.

Automatic colour detection is evaluated at the final emission boundary so collected intermediate expressions do not accidentally look redirected and disable colour. CI includes pseudo-terminal coverage for that behaviour.

The console can also receive an explicit sink, terminal state, width, ASCII mode and theme extension, making product integration and deterministic tests possible without rewriting rendering code.

See [`docs/nushell.md`](docs/nushell.md).

## PowerShell adapter

The PowerShell adapter exposes the same visual language as a module and likewise requires no Python runtime after packaging.

Products can vendor the generated distribution and import it privately instead of requiring users to install R3CLI as a separate global module.

See [`docs/powershell.md`](docs/powershell.md).

## Building shell distributions

The repository keeps canonical implementation resources under Python source and provides deterministic adapter builders:

```console
python scripts/build_powershell.py --output <directory>
python scripts/build_nushell.py --output <directory>
```

This supports a dependency model used by projects such as ModpackTools and Show-Tree:

```text
R3CLI source revision
       │
       ├── build PowerShell adapter
       ├── build Nushell adapter
       ▼
product/vendor/R3CLI
       │
       └── pin revision + hashes in product dependency manifest
```

Users of the consuming product then install one self-contained tool. They do not need an independent R3CLI checkout.

## Themes

The default theme is canonical. Products may extend it with additional semantic roles for their own domain while preserving the base language.

Python exposes `Theme`, `load_theme` and `compose_theme`. Shell adapters consume the same canonical palette and permit validated extensions appropriate to their host API.

Theme values use semantic names rather than references to a specific command or screen.

## Colour and terminal behaviour

R3CLI follows a small predictable contract:

- `auto` uses terminal detection and respects `NO_COLOR`;
- `always` forces ANSI colour;
- `never` disables it;
- ASCII mode substitutes canonical ASCII symbols;
- wrapping uses visible Unicode width rather than raw byte length;
- non-terminal and captured paths can be controlled explicitly in tests and embedding scenarios.

Machine-readable data belongs outside this renderer. A product that emits JSON should keep that channel clean and route R3CLI's human presentation independently.

## Expected errors

Expected CLI failures should be designed, not dumped as implementation exceptions.

R3CLI provides models such as `CliError` and `Diagnostic` so products can present stable identifiers, concise messages and actionable context while retaining the distinction between expected user-facing failures and unexpected defects.

## Project structure

```text
R3CLI/
├── src/r3_cli/              # canonical Python package and resources
├── powershell/R3CLI/        # PowerShell adapter source/distribution shape
├── nushell/r3cli/           # native Nushell adapter
├── scripts/                 # deterministic adapter builders
├── templates/               # language-neutral catalogue templates
├── docs/                    # design and adapter contracts
└── tests/                   # Python and cross-language regression tests
```

## Development

Install test dependencies in editable mode:

```console
python -m pip install -e ".[test]"
```

Run Python tests:

```console
pytest
```

After changing renderers, resources, help contracts or shell adapters, also build and test the PowerShell and Nushell distributions. CI exercises the cross-language contracts and terminal-specific behaviour.

The project currently supports Python 3.11 through 3.14 and targets PowerShell 7 and Nushell 0.115+ for the official shell adapters.

## Documentation

- [`docs/design-language.md`](docs/design-language.md) — visual semantics and accessibility contract;
- [`docs/help-system.md`](docs/help-system.md) — catalogue-driven help;
- [`docs/powershell.md`](docs/powershell.md) — PowerShell API and packaging;
- [`docs/nushell.md`](docs/nushell.md) — Nushell API, packaging and behaviour.

## Licence

MIT. See [`LICENSE`](LICENSE).
