from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tests/Nushell.Contract.nu"
CONFIG = ROOT / "tests/Nushell.CI.Config.nu"
FIXTURE = ROOT / "tests/fixtures/console-contract.json"
ANSI_RE = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))")


def run_nu(*args: str) -> str:
    process = subprocess.run(
        ["nu", "--config", str(CONFIG), str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    if process.returncode:
        raise AssertionError(
            f"Nushell contract command failed ({process.returncode})\n"
            f"stdout:\n{process.stdout}\n"
            f"stderr:\n{process.stderr}"
        )
    return process.stdout


def display_width(text: str) -> int:
    text = ANSI_RE.sub("", text)
    width = 0
    for char in text:
        if unicodedata.combining(char):
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
    return width


def normalized_words(text: str) -> str:
    return " ".join(ANSI_RE.sub("", text).split())


def main() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    ascii_output = run_nu("--mode", "fixture-ascii")
    assert ascii_output == fixture["ascii"], (
        "ASCII cross-language output contract changed\n"
        f"expected={fixture['ascii']!r}\nactual={ascii_output!r}"
    )

    unicode_output = run_nu("--mode", "fixture-unicode")
    assert unicode_output == fixture["unicode"], (
        "Unicode cross-language output contract changed\n"
        f"expected={fixture['unicode']!r}\nactual={unicode_output!r}"
    )

    assertions = run_nu("--mode", "assertions")
    assert "Nushell contract assertions passed." in assertions

    for width in (30, 50, 80, 120):
        output = run_nu("--mode", "width", "--width", str(width))
        for line in output.splitlines():
            assert display_width(line) <= width, (
                f"Nushell help exceeded width {width}: {line!r}\n{output!r}"
            )
        normalized = normalized_words(output)
        assert "Choose content without truncating this description." in normalized, (
            f"Help lost item description at width {width}: {output!r}"
        )
        assert not re.search(r"wrapp$|descri$", output, flags=re.MULTILINE), (
            f"Help split a complete word at width {width}: {output!r}"
        )
        assert "[literal] café 漢字" in normalized, (
            f"Literal text changed at width {width}: {output!r}"
        )
        assert "Very long value that must be preserved" in normalized, (
            f"Table lost content at width {width}: {output!r}"
        )

    print("Nushell adapter contract passed.")


if __name__ == "__main__":
    main()
