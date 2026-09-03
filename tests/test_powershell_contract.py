import io
import json
from pathlib import Path
import subprocess
import sys
import shutil

import pytest

from r3_cli import CliError, ConsoleUI, compose_theme, load_theme

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / 'tests/fixtures/console-contract.json').read_text(encoding='utf-8'))


@pytest.mark.parametrize('ascii', [True, False])
def test_shared_console_contract(ascii):
    output = io.StringIO()
    ui = ConsoleUI(colour='never', ascii=ascii, width=FIXTURE['width'], stdout=output)
    for command in FIXTURE['commands']:
        if command['op'] == 'line':
            ui.line(command['segments'])
        else:
            getattr(ui, command['op'])(command['text'])
    assert output.getvalue() == FIXTURE['ascii' if ascii else 'unicode']


def test_theme_extension_inherits_and_validates():
    theme = compose_theme({'client': '#748ffc', 'heading': '#123456'})
    assert theme.colour('client') == '#748FFC'
    assert theme.colour('heading') == '#123456'
    assert theme.colour('value') == load_theme().colour('value')
    with pytest.raises(CliError):
        compose_theme({'client': 'blue'})


def test_powershell_distribution_and_contract(tmp_path):
    pwsh = shutil.which('pwsh')
    if pwsh is None:
        pytest.skip('PowerShell contract also runs in the dedicated Windows CI job')
    output = tmp_path / 'R3CLI'
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_powershell.py'), '--output', str(output)], check=True)
    first = {p.name: p.read_bytes() for p in output.iterdir()}
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_powershell.py'), '--output', str(output)], check=True)
    assert first == {p.name: p.read_bytes() for p in output.iterdir()}
    subprocess.run([pwsh, '-NoProfile', '-File', str(ROOT / 'tests/PowerShell.Contract.ps1'), '-ModulePath', str(output / 'R3CLI.psd1')], check=True)
