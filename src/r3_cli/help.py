from __future__ import annotations

import tomllib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import CliError


@dataclass(frozen=True)
class HelpItem:
    label: str
    description: str


@dataclass(frozen=True)
class CommandHelp:
    name: str
    group: str
    summary: str
    description: str
    usage: Sequence[str]
    items: Sequence[HelpItem] = field(default_factory=tuple)
    notes: Sequence[str] = field(default_factory=tuple)
    examples: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "usage", tuple(self.usage))
        object.__setattr__(self, "items", tuple(self.items))
        object.__setattr__(self, "notes", tuple(self.notes))
        object.__setattr__(self, "examples", tuple(self.examples))


@dataclass(frozen=True)
class HelpCatalogue:
    product: str
    version: str
    description: str
    invocation: str
    groups: Sequence[str]
    commands: Sequence[CommandHelp]
    usage: Sequence[str] = field(default_factory=tuple)
    notes: Sequence[str] = field(default_factory=tuple)
    show_help_on_empty: bool = True
    help_options: Sequence[str] = ("-h", "--help")

    def __post_init__(self) -> None:
        object.__setattr__(self, "groups", tuple(self.groups))
        object.__setattr__(self, "commands", tuple(self.commands))
        object.__setattr__(self, "usage", tuple(self.usage))
        object.__setattr__(self, "notes", tuple(self.notes))
        object.__setattr__(self, "help_options", tuple(self.help_options))

    @property
    def title(self) -> str:
        return f"{self.product} {self.version}" if self.version else self.product

    def validate(self, executable_commands: Iterable[str] | None = None) -> None:
        errors: list[str] = []
        required = {
            "product": self.product,
            "description": self.description,
            "invocation": self.invocation,
        }
        errors.extend(f"{name} is empty" for name, value in required.items() if not value.strip())

        folded_groups = [group.casefold() for group in self.groups]
        if len(folded_groups) != len(set(folded_groups)):
            errors.append("group names are not unique")
        if "--help" not in self.help_options:
            errors.append("help options must include '--help'")
        if any(not option.strip() for option in self.help_options):
            errors.append("help options contain an empty value")
        if len(self.help_options) != len(set(self.help_options)):
            errors.append("help options are not unique")

        command_names: list[str] = []
        known_groups = set(self.groups)
        for command in self.commands:
            command_names.append(command.name.casefold())
            if not command.name.strip():
                errors.append("a command name is empty")
            if command.name.casefold() == "help":
                errors.append("'help' must not be declared as a command")
            if command.group not in known_groups:
                errors.append(f"command '{command.name}' uses unknown group '{command.group}'")
            if not command.summary.strip():
                errors.append(f"command '{command.name}' has no summary")
            if not command.description.strip():
                errors.append(f"command '{command.name}' has no description")
            if not command.usage or any(not value.strip() for value in command.usage):
                errors.append(f"command '{command.name}' has no valid usage line")
            for item in command.items:
                if not item.label.strip() or not item.description.strip():
                    errors.append(f"command '{command.name}' has an incomplete help item")
        if len(command_names) != len(set(command_names)):
            errors.append("command names are not unique")

        if executable_commands is not None:
            documented = set(command_names)
            executable = {str(name).casefold() for name in executable_commands}
            missing = sorted(executable - documented)
            extra = sorted(documented - executable)
            if missing:
                errors.append("undocumented executable commands: " + ", ".join(missing))
            if extra:
                errors.append("documented commands without an executable: " + ", ".join(extra))

        if errors:
            raise CliError(
                "The help catalogue is invalid.",
                code="R3CLI.Help.InvalidCatalogue",
                details="; ".join(errors),
                hint="repair the catalogue and keep it aligned with command dispatch",
            )

    def command(self, name: str) -> CommandHelp:
        self.validate()
        folded = name.casefold()
        for command in self.commands:
            if command.name.casefold() == folded:
                return command
        raise CliError(
            f"Command '{name}' does not have a help page.",
            code="R3CLI.Help.UnknownTopic",
            hint=f"{self.invocation} --help",
        )


@dataclass(frozen=True)
class HelpRequest:
    command: str | None = None


def resolve_help_request(argv: Sequence[str], catalogue: HelpCatalogue) -> HelpRequest | None:
    """Recognise the ModpackTools help routes before application state is loaded."""
    catalogue.validate()
    values = tuple(argv)
    help_options = set(catalogue.help_options)
    if not values:
        return HelpRequest() if catalogue.show_help_on_empty else None
    if values[0] in help_options:
        if len(values) != 1:
            raise CliError(
                "The global help option does not accept additional arguments.",
                code="R3CLI.Help.InvalidArguments",
                hint=f"{catalogue.invocation} --help",
            )
        return HelpRequest()
    if any(value in help_options for value in values[1:]):
        command = catalogue.command(values[0])
        return HelpRequest(command.name)
    return None


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    return value


def _strings(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be an array of strings")
    return tuple(value)


def load_help_catalogue(path: Path) -> HelpCatalogue:
    try:
        parsed = tomllib.loads(path.read_text(encoding="utf-8-sig"))
        metadata = parsed["help"]
        raw_commands = parsed.get("commands", [])
        if not isinstance(metadata, dict) or not isinstance(raw_commands, list):
            raise ValueError("[help] must be a table and commands must be an array")
        commands: list[CommandHelp] = []
        for index, raw in enumerate(raw_commands):
            if not isinstance(raw, dict):
                raise ValueError(f"commands[{index}] must be a table")
            raw_items = raw.get("items", [])
            if not isinstance(raw_items, list):
                raise ValueError(f"commands[{index}].items must be an array")
            items = tuple(
                HelpItem(
                    _string(item["label"], f"commands[{index}].items.label"),
                    _string(item["description"], f"commands[{index}].items.description"),
                )
                for item in raw_items
                if isinstance(item, dict)
            )
            if len(items) != len(raw_items):
                raise ValueError(f"commands[{index}].items must contain tables")
            commands.append(
                CommandHelp(
                    name=_string(raw["name"], f"commands[{index}].name"),
                    group=_string(raw["group"], f"commands[{index}].group"),
                    summary=_string(raw["summary"], f"commands[{index}].summary"),
                    description=_string(raw["description"], f"commands[{index}].description"),
                    usage=_strings(raw["usage"], f"commands[{index}].usage"),
                    items=items,
                    notes=_strings(raw.get("notes", []), f"commands[{index}].notes"),
                    examples=_strings(raw.get("examples", []), f"commands[{index}].examples"),
                )
            )
        catalogue = HelpCatalogue(
            product=_string(metadata["product"], "help.product"),
            version=_string(metadata.get("version", ""), "help.version"),
            description=_string(metadata["description"], "help.description"),
            invocation=_string(metadata["invocation"], "help.invocation"),
            groups=_strings(metadata["group-order"], "help.group-order"),
            commands=commands,
            usage=_strings(metadata.get("usage", []), "help.usage"),
            notes=_strings(metadata.get("notes", []), "help.notes"),
            show_help_on_empty=metadata.get("show-help-on-empty", True),
            help_options=_strings(metadata.get("help-options", ["-h", "--help"]), "help.help-options"),
        )
        if not isinstance(catalogue.show_help_on_empty, bool):
            raise ValueError("help.show-help-on-empty must be a Boolean")
        catalogue.validate()
        return catalogue
    except (OSError, KeyError, UnicodeError, ValueError, tomllib.TOMLDecodeError) as exc:
        raise CliError(
            f"Help catalogue '{path}' could not be loaded.",
            code="R3CLI.Help.UnreadableCatalogue",
            details=str(exc),
            hint="repair the TOML catalogue using the R3CLI help template",
        ) from exc
