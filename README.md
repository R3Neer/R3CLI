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

The default theme is canonical, but products may add domain-specific semantic
roles. Machine-readable output remains separate from human rendering and never
contains ANSI escape sequences.

See [`docs/design-language.md`](docs/design-language.md) for the complete
contract.

## Development

```console
python -m pip install -e ".[test]"
pytest
```

## Licence

MIT. See [`LICENSE`](LICENSE).
