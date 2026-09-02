from __future__ import annotations

import io
from pathlib import Path

import pytest

from r3_cli import (
    CliError,
    CommandHelp,
    ConsoleUI,
    HelpCatalogue,
    HelpItem,
    HelpRequest,
    load_help_catalogue,
    resolve_help_request,
)


def catalogue() -> HelpCatalogue:
    return HelpCatalogue(
        product="R3 TOOL",
        version="0.2",
        description="Manage example projects.",
        invocation="r3tool",
        groups=("PROJECTS", "MAINTENANCE"),
        usage=(
            "r3tool <command> [arguments] [options]",
            "r3tool <command> --help",
            "r3tool --version",
        ),
        notes=("Run r3tool <command> --help for detailed help.",),
        commands=(
            CommandHelp(
                "list",
                "PROJECTS",
                "Show projects",
                "Show every registered project.",
                ("r3tool list",),
            ),
            CommandHelp(
                "check",
                "MAINTENANCE",
                "Check a project",
                "Check project structure without modifying it.",
                ("r3tool check <project> [options]",),
                (HelpItem("<project>", "Stable project ID."), HelpItem("--strict", "Fail on incomplete metadata.")),
                ("Checking never modifies the project.",),
                ("r3tool check example",),
            ),
        ),
    )


def test_overview_snapshot() -> None:
    output = io.StringIO()
    ConsoleUI(colour="never", ascii=True, stdout=output, width=54).help(catalogue())
    assert output.getvalue() == (
        "\n"
        + "=" * 54
        + "\n R3 TOOL 0.2\n"
        + "=" * 54
        + "\nManage example projects.\n"
        "\nUSAGE\n"
        "  r3tool <command> [arguments] [options]\n"
        "  r3tool <command> --help\n"
        "  r3tool --version\n"
        "\nPROJECTS\n"
        "  list   Show projects\n"
        "\nMAINTENANCE\n"
        "  check  Check a project\n"
        "\n* Run r3tool <command> --help for detailed help.\n\n"
    )


def test_command_help_snapshot() -> None:
    output = io.StringIO()
    ConsoleUI(colour="never", ascii=True, stdout=output, width=54).help(catalogue(), "check")
    assert output.getvalue() == (
        "\n"
        + "=" * 54
        + "\n CHECK\n"
        + "=" * 54
        + "\nCheck project structure without modifying it.\n"
        "\nUSAGE\n"
        "  r3tool check <project> [options]\n"
        "\nARGUMENTS AND OPTIONS\n"
        "  <project>  Stable project ID.\n"
        "  --strict   Fail on incomplete metadata.\n"
        "\nNOTES\n"
        "* Checking never modifies the project.\n"
        "\nEXAMPLES\n"
        "  r3tool check example\n\n"
    )


def test_narrow_help_rows_stack_without_truncation() -> None:
    output = io.StringIO()
    ConsoleUI(colour="never", ascii=True, stdout=output, width=24).help(catalogue(), "check")
    rendered = output.getvalue()
    assert "  <project>\n    Stable project ID.\n" in rendered
    assert "  --strict\n    Fail on incomplete metadata.\n" in rendered


def test_help_routing_matches_modpacktools_contract() -> None:
    help_catalogue = catalogue()
    assert resolve_help_request((), help_catalogue) == HelpRequest()
    assert resolve_help_request(("--help",), help_catalogue) == HelpRequest()
    assert resolve_help_request(("-h",), help_catalogue) == HelpRequest()
    assert resolve_help_request(("check", "--help"), help_catalogue) == HelpRequest("check")
    assert resolve_help_request(("check", "example"), help_catalogue) is None
    assert resolve_help_request(("help",), help_catalogue) is None


def test_empty_arguments_can_continue_to_a_validator_default() -> None:
    source = catalogue()
    validator = HelpCatalogue(
        product=source.product,
        version=source.version,
        description=source.description,
        invocation=source.invocation,
        groups=source.groups,
        commands=source.commands,
        show_help_on_empty=False,
    )
    assert resolve_help_request((), validator) is None


def test_redirected_help_has_no_ansi() -> None:
    output = io.StringIO()
    ConsoleUI(colour="auto", stdout=output).help(catalogue())
    assert "\x1b[" not in output.getvalue()


def test_command_help_wins_before_required_arguments() -> None:
    assert resolve_help_request(("check", "--strict", "--help"), catalogue()) == HelpRequest("check")


def test_global_help_rejects_additional_arguments() -> None:
    with pytest.raises(CliError, match="does not accept additional arguments") as caught:
        resolve_help_request(("--help", "check"), catalogue())
    assert caught.value.code == "R3CLI.Help.InvalidArguments"
    assert caught.value.hint == "r3tool --help"


def test_unknown_help_topic_is_actionable() -> None:
    with pytest.raises(CliError, match="does not have a help page") as caught:
        resolve_help_request(("missing", "--help"), catalogue())
    assert caught.value.code == "R3CLI.Help.UnknownTopic"
    assert caught.value.hint == "r3tool --help"


def test_catalogue_detects_dispatch_drift() -> None:
    catalogue().validate(("list", "check"))
    with pytest.raises(CliError) as caught:
        catalogue().validate(("list", "build"))
    assert "undocumented executable commands: build" in (caught.value.details or "")
    assert "documented commands without an executable: check" in (caught.value.details or "")


def test_toml_template_loads() -> None:
    path = Path(__file__).resolve().parents[1] / "templates" / "help-catalogue.toml"
    loaded = load_help_catalogue(path)
    loaded.validate(("list", "check"))
    assert loaded.command("check").items[1].label == "--strict"


def test_invalid_toml_is_reported_as_cli_error(tmp_path: Path) -> None:
    path = tmp_path / "help.toml"
    path.write_text("[help\n", encoding="utf-8")
    with pytest.raises(CliError) as caught:
        load_help_catalogue(path)
    assert caught.value.code == "R3CLI.Help.UnreadableCatalogue"
