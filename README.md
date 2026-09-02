# R3CLI

R3CLI is the shared visual language for command-line tools created by R3Neer.
It turns the hierarchy first developed in ModpackTools into a small,
accessible Python library: cyan structure, orange actions, quiet secondary
context, clear values and status colours that are always paired with symbols.

```python
from r3_cli import ConsoleUI

ui = ConsoleUI()
ui.banner("MY TOOL 1.0")
ui.step("Reading the project")
ui.success("Project is ready.")
```

R3CLI also provides the catalogue and renderer behind ModpackTools-style help:
grouped command overviews, focused command pages, usage, notes and examples
from one validated source of truth. See
[`docs/help-system.md`](docs/help-system.md) and the language-neutral
[`templates/help-catalogue.toml`](templates/help-catalogue.toml).

The default theme is canonical, but products may add domain-specific semantic
roles. Machine-readable output remains separate from human rendering and never
contains ANSI escape sequences.

See [`docs/design-language.md`](docs/design-language.md) for the complete visual
contract.

## Maintaining R3CLI

These commands are for contributors changing R3CLI itself, not for tools that
use it as a dependency. From a local clone, install the library together with
its test dependencies in editable mode:

```console
python -m pip install -e ".[test]"
```

Editable installation means changes under `src/r3_cli/` are used immediately;
there is no need to reinstall the package after each change.

Run the test suite after changing the renderer, theme, help system or public
API:

```console
pytest
```

## Licence

MIT. See [`LICENSE`](LICENSE).
