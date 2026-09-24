# Python package releases

The PyPI distribution is `r3-cli`; the import name is `r3_cli`. The Python
package uses Hatchling and ships its theme and symbols as package resources.

## Check a release locally

Use a fresh virtual environment with a supported Python version:

```console
python -m venv .venv
.venv/Scripts/python -m pip install build twine
.venv/Scripts/python -m pip install -e ".[test]"
.venv/Scripts/python -m pytest
.venv/Scripts/python -m build
.venv/Scripts/python -m twine check dist/*
```

On Unix, replace `.venv/Scripts/python` with `.venv/bin/python`. Install the
generated wheel in a **second** fresh environment and check the public imports
and a render call:

```console
python -m venv .wheel-check
.wheel-check/Scripts/python -m pip install dist/r3_cli-<version>-py3-none-any.whl
.wheel-check/Scripts/python -c "import r3_cli; from r3_cli import ConsoleUI, R3ArgumentParser; print(r3_cli.__version__); ConsoleUI(colour='never').success('Ready')"
```

Check the wheel and source archive contents as well: both should contain the
Python package, `symbols.json`, and `default_theme.toml`, and the source archive
should contain the README and license. Remove the temporary environments after
verification if they are no longer needed.

## Publish deliberately

1. Confirm that `pyproject.toml` and `src/r3_cli/__init__.py` declare the same
   version, tests pass, and the release commit is on the default branch. Use a
   **new** version if the previous version already has a published GitHub
   release or tag. Do not move a published version tag.
2. Configure the `pypi` GitHub Environment. Restrict deployments to version
   tags and, if desired, require a maintainer review before deployment.
3. In PyPI, configure a Trusted Publisher for GitHub owner `R3Neer`, repository
   `R3CLI`, workflow filename `release.yml`, and environment `pypi`. The PyPI
   project name is `r3-cli`. If the project does not exist yet, add a **pending**
   Trusted Publisher from the PyPI account's Publishing page. A pending
   publisher creates the project on first successful upload; it does not reserve
   the name beforehand.
4. Commit and push the release-ready changes, create a new `v<version>` tag on
   that exact commit, and publish a **non-prerelease GitHub Release** for the
   tag. The release event runs `.github/workflows/release.yml`; normal pushes
   and draft releases do not publish to PyPI.
5. Wait for the build and publish jobs to succeed. Check the version and files
   on PyPI, then install `r3-cli` in another fresh environment and verify
   `import r3_cli`.

The build job tests, creates a wheel and source archive, checks metadata, and
tests the installed wheel. It has no OIDC permission. The publish job receives
only those artifacts and requests `id-token: write` to authenticate to PyPI
through Trusted Publishing. No PyPI API token is stored in GitHub secrets.
