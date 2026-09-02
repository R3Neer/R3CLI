from __future__ import annotations

import io
import json
import re

from r3_cli import CliError, ConsoleUI, Diagnostic


def test_plain_help_hierarchy() -> None:
    output = io.StringIO()
    ui = ConsoleUI(colour="never", ascii=True, stdout=output, width=50)
    ui.banner("R3 TOOL 0.1")
    ui.heading("usage")
    ui.command("r3tool check", "Check a project")
    ui.info("Run with --help for details.")
    assert output.getvalue() == (
        "\n"
        + "=" * 50
        + "\n R3 TOOL 0.1\n"
        + "=" * 50
        + "\n\nUSAGE\n  r3tool check  Check a project\n* Run with --help for details.\n"
    )


def test_forced_colour_contains_ansi() -> None:
    output = io.StringIO()
    ui = ConsoleUI(colour="always", stdout=output, width=40)
    ui.success("Ready.")
    assert "\x1b[" in output.getvalue()
    assert re.sub(r"\x1b\[[0-9;]*m", "", output.getvalue()) == "✓ Ready.\n"


def test_step_is_progress_on_stderr() -> None:
    output = io.StringIO()
    error_output = io.StringIO()
    ui = ConsoleUI(colour="never", ascii=True, stdout=output, stderr=error_output)
    ui.step("Loading profile.")
    assert output.getvalue() == ""
    assert error_output.getvalue() == "> Loading profile.\n"


def test_json_is_never_styled() -> None:
    output = io.StringIO()
    ui = ConsoleUI(colour="always", stdout=output)
    ui.json({"status": "ok"})
    assert json.loads(output.getvalue()) == {"status": "ok"}
    assert "\x1b[" not in output.getvalue()


def test_diagnostic_contract_uses_stderr() -> None:
    error_output = io.StringIO()
    ui = ConsoleUI(colour="never", ascii=True, stderr=error_output)
    ui.error(CliError("Profile 'x' is invalid.", code="Tool.Profile.Invalid", details="Missing language.", hint="repair profile.toml"))
    rendered = error_output.getvalue()
    assert "x Profile 'x' is invalid." in rendered
    assert "[Tool.Profile.Invalid]" in rendered
    assert "Details: Missing language." in rendered
    assert "Try: repair profile.toml" in rendered


def test_structured_diagnostic() -> None:
    value = Diagnostic("warning", "Tool.Warning", "Review this.", data={"line": 2})
    assert value.as_dict()["data"] == {"line": 2}
