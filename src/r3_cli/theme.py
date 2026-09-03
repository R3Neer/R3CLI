from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Mapping

from .models import CliError


REQUIRED_ROLES = ("heading", "accent", "secondary", "value", "success", "error", "process")
HEX_COLOUR = re.compile(r"^#[0-9A-Fa-f]{6}$")


@dataclass(frozen=True)
class Theme:
    colours: Mapping[str, str]

    def colour(self, role: str) -> str:
        try:
            return self.colours[role]
        except KeyError as exc:
            raise CliError(
                f"Theme role '{role}' is not defined.",
                code="R3CLI.Theme.UnknownRole",
                hint="add the role to the product theme",
            ) from exc


def _load(data: bytes, source: str) -> Theme:
    try:
        parsed = tomllib.loads(data.decode("utf-8-sig"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise CliError(
            f"Theme '{source}' is not valid TOML.",
            code="R3CLI.Theme.Invalid",
            details=str(exc),
            hint="repair the theme or restore the canonical file",
        ) from exc
    colours = parsed.get("colours")
    if not isinstance(colours, dict):
        raise CliError(
            f"Theme '{source}' has no [colours] table.",
            code="R3CLI.Theme.MissingColours",
            hint="add the required [colours] table",
        )
    missing = [role for role in REQUIRED_ROLES if role not in colours]
    invalid = [name for name, value in colours.items() if not isinstance(value, str) or not HEX_COLOUR.fullmatch(value)]
    if missing or invalid:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if invalid:
            details.append("invalid #RRGGBB values: " + ", ".join(invalid))
        raise CliError(
            f"Theme '{source}' is incomplete or malformed.",
            code="R3CLI.Theme.InvalidColours",
            details="; ".join(details),
            hint="define every required colour as #RRGGBB",
        )
    return Theme({name: value.upper() for name, value in colours.items()})


def load_theme(path: Path | None = None) -> Theme:
    if path is None:
        resource = files("r3_cli").joinpath("default_theme.toml")
        return _load(resource.read_bytes(), "default_theme.toml")
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise CliError(
            f"Theme '{path}' could not be read.",
            code="R3CLI.Theme.Unreadable",
            details=str(exc),
            hint="provide a readable TOML theme path",
        ) from exc
    return _load(data, str(path))


def compose_theme(extension: Mapping[str, str], base: Theme | None = None) -> Theme:
    """Inherit the canonical palette and apply explicit product roles/overrides."""
    colours = dict((base or load_theme()).colours)
    for role, value in extension.items():
        if not isinstance(value, str) or not HEX_COLOUR.fullmatch(value):
            raise CliError(f"Theme role '{role}' must use #RRGGBB.", code="R3CLI.Theme.InvalidColours")
        colours[role] = value.upper()
    return Theme(colours)
