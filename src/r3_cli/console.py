from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Iterable, Sequence
from typing import Any, TextIO

from rich.console import Console
from rich.table import Table
from rich.text import Text

from .help import HelpCatalogue
from .models import CliError, ColourMode, Diagnostic
from .theme import Theme, load_theme


def add_output_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--colour",
        choices=[mode.value for mode in ColourMode],
        default=ColourMode.AUTO.value,
        help="Colour output: auto, always, or never.",
    )
    parser.add_argument("--ascii", action="store_true", help="Use ASCII status symbols.")


class ConsoleUI:
    def __init__(
        self,
        *,
        theme: Theme | None = None,
        colour: ColourMode | str = ColourMode.AUTO,
        ascii: bool = False,
        stdout: TextIO | None = None,
        stderr: TextIO | None = None,
        width: int | None = None,
    ) -> None:
        self.theme = theme or load_theme()
        self.ascii = ascii
        self.stdout_stream = stdout or sys.stdout
        self.stderr_stream = stderr or sys.stderr
        mode = ColourMode(colour)
        force_terminal: bool | None
        no_colour = False
        if mode is ColourMode.ALWAYS:
            force_terminal = True
            color_system: str | None = "truecolor"
        elif mode is ColourMode.NEVER or "NO_COLOR" in os.environ:
            force_terminal = False
            no_colour = True
            color_system = None
        else:
            force_terminal = None
            color_system = "auto"
        options = {
            "color_system": color_system,
            "force_terminal": force_terminal,
            "no_color": no_colour,
            "highlight": False,
            "soft_wrap": True,
            "width": width,
        }
        self.out = Console(file=self.stdout_stream, **options)
        self.err = Console(file=self.stderr_stream, **options)

    def _text(self, value: object, role: str | None = None, *, bold: bool = False) -> Text:
        style = None
        if role:
            style = self.theme.colour(role)
        if bold:
            style = f"bold {style}" if style else "bold"
        return Text(str(value), style=style)

    def _symbol(self, kind: str) -> str:
        symbols = {
            "step": ("→", ">"),
            "success": ("✓", "+"),
            "info": ("•", "*"),
            "warning": ("!", "!"),
            "error": ("✗", "x"),
        }
        unicode_symbol, ascii_symbol = symbols[kind]
        return ascii_symbol if self.ascii else unicode_symbol

    def banner(self, text: str) -> None:
        width = max(24, min(68, self.out.width))
        rule = ("=" if self.ascii else "═") * width
        self.out.print()
        self.out.print(self._text(rule, "secondary"))
        title = Text(" ")
        title.append(str(text), style=f"bold {self.theme.colour('heading')}")
        self.out.print(title)
        self.out.print(self._text(rule, "secondary"))

    def heading(self, text: str) -> None:
        self.out.print()
        self.out.print(self._text(text.upper(), "heading", bold=True))

    def section(self, title: str, count: int | None = None) -> None:
        self.out.print()
        line = Text("  ")
        line.append(title, style=self.theme.colour("heading"))
        if count is not None:
            line.append("  ")
            line.append(str(count), style=self.theme.colour("accent"))
        self.out.print(line)
        self.out.print(self._text("  " + ("-" if self.ascii else "─") * max(20, min(64, self.out.width - 2)), "secondary"))

    def _status(self, kind: str, text: str, *, error: bool = False) -> None:
        role = {"step": "process", "success": "success", "info": "heading", "warning": "process", "error": "error"}[kind]
        line = Text()
        line.append(self._symbol(kind), style=self.theme.colour(role))
        line.append(" " + text, style=self.theme.colour("value") if kind == "info" else None)
        (self.err if error else self.out).print(line)

    def step(self, text: str) -> None:
        self._status("step", text, error=True)

    def success(self, text: str) -> None:
        self._status("success", text)

    def result(self, text: str) -> None:
        """Write a final human-readable result to stdout."""
        self._status("success", text)

    def info(self, text: str) -> None:
        self._status("info", text)

    def warning(self, text: str) -> None:
        self._status("warning", text, error=True)

    def failure(self, text: str) -> None:
        self._status("error", text, error=True)

    def key_value(self, key: str, value: object, *, width: int = 16) -> None:
        line = Text()
        line.append(key.ljust(width), style=self.theme.colour("secondary"))
        line.append(" ")
        line.append(str(value), style=self.theme.colour("value"))
        self.out.print(line)

    def command(self, command: str, description: str | None = None) -> None:
        line = Text("  ")
        line.append(command, style=self.theme.colour("accent"))
        if description:
            line.append("  " + description, style=self.theme.colour("secondary"))
        self.out.print(line)

    def help_row(self, label: str, description: str, *, width: int = 24) -> None:
        if self.out.width < 40 or width + 4 >= self.out.width:
            self.out.print(self._text("  " + label, "accent"))
            self.out.print(self._text("    " + description, "secondary"))
            return
        line = Text("  ")
        line.append(label.ljust(width), style=self.theme.colour("accent"))
        line.append(description, style=self.theme.colour("secondary"))
        self.out.print(line)

    def help_text(self, text: str) -> None:
        self.out.print(self._text(text, "value"))

    def help_overview(self, catalogue: HelpCatalogue) -> None:
        catalogue.validate()
        self.banner(catalogue.title)
        self.help_text(catalogue.description)
        self.heading("usage")
        usage = catalogue.usage or (
            f"{catalogue.invocation} <command> [arguments] [options]",
            f"{catalogue.invocation} <command> --help",
        )
        for line in usage:
            self.command(line)
        row_width = min(24, max((len(command.name) for command in catalogue.commands), default=0) + 2)
        for group in catalogue.groups:
            commands = [command for command in catalogue.commands if command.group == group]
            if not commands:
                continue
            self.heading(group)
            for command in commands:
                self.help_row(command.name, command.summary, width=row_width)
        if catalogue.notes:
            self.out.print()
        for note in catalogue.notes:
            self.info(note)
        self.out.print()

    def help_command(self, catalogue: HelpCatalogue, command_name: str) -> None:
        command = catalogue.command(command_name)
        self.banner(command.name.upper())
        self.help_text(command.description)
        self.heading("usage")
        for line in command.usage:
            self.command(line)
        if command.items:
            self.heading("arguments and options")
            row_width = min(28, max(len(item.label) for item in command.items) + 2)
            for item in command.items:
                self.help_row(item.label, item.description, width=row_width)
        if command.notes:
            self.heading("notes")
            for note in command.notes:
                self.info(note)
        if command.examples:
            self.heading("examples")
            for example in command.examples:
                self.command(example)
        self.out.print()

    def help(self, catalogue: HelpCatalogue, command: str | None = None) -> None:
        if command is None:
            self.help_overview(catalogue)
        else:
            self.help_command(catalogue, command)

    def response(self, text: str, *, error: bool = False) -> None:
        """Write plain human text, separating a multiline response from the shell prompt.

        Use this for help or reports produced by an external renderer such as
        ``argparse``. Structured output belongs to :meth:`json` instead.
        """
        if not text:
            return
        stream = self.stderr_stream if error else self.stdout_stream
        multiline = "\n" in text.rstrip("\n")
        if multiline:
            stream.write("\n")
        stream.write(text)
        if not text.endswith("\n"):
            stream.write("\n")
        if multiline:
            stream.write("\n")
        stream.flush()

    def table(self, headers: Sequence[str], rows: Iterable[Sequence[object]]) -> None:
        table = Table(show_header=True, box=None, pad_edge=False)
        for header in headers:
            table.add_column(header, style=self.theme.colour("secondary"), header_style=self.theme.colour("heading"))
        for row in rows:
            table.add_row(*(str(value) for value in row), style=self.theme.colour("value"))
        self.out.print(table)

    def diagnostic(self, diagnostic: Diagnostic) -> None:
        level = str(diagnostic.level)
        kind = "warning" if level == "warning" else "info" if level == "info" else "success" if level == "success" else "error"
        self._status(kind, diagnostic.message, error=kind in {"warning", "error"})
        target = self.err if kind in {"warning", "error"} else self.out
        target.print(self._text(f"  [{diagnostic.code}]", "secondary"))
        if diagnostic.details:
            target.print(self._text(f"Details: {diagnostic.details}", "secondary"))
        if diagnostic.hint:
            line = Text("Try: ", style=self.theme.colour("secondary"))
            line.append(diagnostic.hint, style=self.theme.colour("accent"))
            target.print(line)

    def error(self, error: CliError) -> None:
        self.diagnostic(error.as_diagnostic())

    def json(self, value: Any) -> None:
        self.stdout_stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")
        self.stdout_stream.flush()


class R3ArgumentParser(argparse.ArgumentParser):
    """An ``argparse`` parser that applies R3CLI's human-response spacing."""

    def _print_message(self, message: str | None, file: TextIO | None = None) -> None:
        if not message:
            return
        target = file or sys.stdout
        ConsoleUI(colour=ColourMode.NEVER, stdout=target, stderr=target).response(message)
