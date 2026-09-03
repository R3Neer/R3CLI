from __future__ import annotations

import io
import json
import re

import pytest

from r3_cli import CliError, ConsoleUI, Diagnostic, R3ArgumentParser


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


def test_multiline_response_has_a_blank_margin_at_both_ends() -> None:
    output = io.StringIO()
    ui = ConsoleUI(colour="never", stdout=output)
    ui.response("usage: r3tool [options]\n\noptions:\n  --help\n")
    assert output.getvalue() == "\nusage: r3tool [options]\n\noptions:\n  --help\n\n"


def test_single_line_response_stays_compact() -> None:
    output = io.StringIO()
    ui = ConsoleUI(colour="never", stdout=output)
    ui.response("0.4.0")
    assert output.getvalue() == "0.4.0\n"


def test_argparse_adapter_wraps_multiline_help_but_not_version(capsys) -> None:
    parser = R3ArgumentParser(prog="r3tool")
    parser.add_argument("--version", action="version", version="r3tool 0.4.0")
    parser.add_argument("--check", action="store_true")
    with pytest.raises(SystemExit, match="0"):
        parser.parse_args(["--help"])
    assert capsys.readouterr().out.startswith("\nusage: r3tool")
    with pytest.raises(SystemExit, match="0"):
        parser.parse_args(["--version"])
    assert capsys.readouterr().out == "r3tool 0.4.0\n"


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
