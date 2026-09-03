# R3CLI help system

R3CLI adopts the help hierarchy first developed in ModpackTools. A catalogue
holds product identity and command documentation; `ConsoleUI` renders the same
catalogue as a grouped overview or a focused command page.

## Behaviour contract

- A discoverable command suite may show its overview both with no arguments
  and with global `--help`. Validators that perform useful default work should
  set `show_help_on_empty` to `false`.
- `-h` may be accepted as a platform-friendly alias, but examples use
  `--help` consistently.
- `<command> --help` is resolved before project, configuration, filesystem or
  network state. Asking for help must not fail because application state is
  unavailable.
- Global `--help` rejects additional arguments. Command help takes precedence
  over the command's required arguments, like conventional argument parsers.
- `help` is not a pseudo-command. Unknown commands point to `<tool> --help`.
- `--version` is a global option and prints one undecorated line.
- Every executable command appears exactly once in the catalogue. CI should
  call `catalogue.validate(executable_commands)` to detect drift.
- Every operational positional argument and option has one help item. Its
  description says what it accepts, what it changes and any meaningful default
  or restriction. Standard `-h` and `--help` are the only intentional
  exception.
- Global inputs such as `--version`, output format and presentation options
  live in `global_items`; command-specific inputs live in `CommandHelp.items`.
  Use `NOTES` for safety, incompatibility, environment and stateful behaviour,
  and add examples for non-obvious or writing commands.

The routing helper recognises these rules without taking ownership of command
parsing:

```python
import sys

from r3_cli import ConsoleUI, resolve_help_request

request = resolve_help_request(sys.argv[1:], catalogue)
if request is not None:
    ConsoleUI().help(catalogue, request.command)
    raise SystemExit(0)
```

Applications remain free to use `argparse`, Click, Typer or their own parser.
R3CLI owns the visual and behavioural help contract, not execution semantics.
When an application must retain a parser's plain multiline help, it should pass
`parser.format_help()` to `ConsoleUI.response()` rather than print it directly.
For `argparse`, use `R3ArgumentParser` instead: it applies the same rule to
global and command help while preserving compact one-line `--version` output.

For `argparse` applications, validate the documentation against the parser at
startup and in tests:

```python
from r3_cli import validate_argparse_catalogue

validate_argparse_catalogue(parser, catalogue)
```

It rejects a root option missing from `global_items`, or a command input
missing from that command's `items`. Other parser ecosystems can use the same
catalogue contract and provide an equivalent adapter.

## Catalogue API

Catalogues can be constructed in Python:

```python
from r3_cli import CommandHelp, HelpCatalogue, HelpItem

catalogue = HelpCatalogue(
    product="MY TOOL",
    version="1.0.0",
    description="Manage example projects.",
    invocation="mytool",
    groups=("PROJECTS",),
    usage=("mytool <command> [arguments] [options]", "mytool <command> --help"),
    notes=("Run mytool <command> --help for detailed help.",),
    global_items=(
        HelpItem("--version", "Print the installed version and exit."),
        HelpItem("--colour auto|always|never", "Control colour output."),
    ),
    commands=(
        CommandHelp(
            name="check",
            group="PROJECTS",
            summary="Check a project",
            description="Check project structure and report findings.",
            usage=("mytool check <project>",),
            items=(HelpItem("<project>", "Stable project ID."),),
            examples=("mytool check example",),
        ),
    ),
)
```

Or loaded from [`templates/help-catalogue.toml`](../templates/help-catalogue.toml):

```python
from pathlib import Path
from r3_cli import load_help_catalogue

catalogue = load_help_catalogue(Path("help.toml"))
```

The TOML form is the language-neutral template for PowerShell, Node and other
adapters. Those adapters should preserve the same field meanings, ordering and
validation even when they cannot reuse the Python renderer directly.

## Presentation

The overview contains, in order: product banner, description, `USAGE`, optional
`GLOBAL OPTIONS`, grouped commands and short closing guidance. A command page contains its command
banner, description, `USAGE`, optional `ARGUMENTS AND OPTIONS`, optional
`NOTES`, and optional `EXAMPLES`.

Structure uses the heading colour, commands and selectors use the accent
colour, descriptions use the secondary colour and body text uses the value
colour. Narrow terminals place descriptions below labels instead of truncating
either. Redirected output remains plain text; colour is never required to
understand the hierarchy.
