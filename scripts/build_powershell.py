"""Build an unmodified, deterministic PowerShell distribution. No runtime Python."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def build(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    sources = sorted((ROOT / "powershell/R3CLI").glob("*.ps*"))
    allowed = {p.name for p in sources} | {'LICENSE', 'resources.json', 'hashes.json'}
    unexpected = [p.name for p in destination.iterdir() if not p.is_file() or p.name not in allowed]
    if unexpected:
        raise ValueError(f"Build destination has unexpected content: {unexpected}")
    for source in sources:
        (destination / source.name).write_bytes(source.read_bytes().replace(b"\r\n", b"\n"))
    (destination / "LICENSE").write_bytes((ROOT / "LICENSE").read_bytes().replace(b"\r\n", b"\n"))
    resources = {
        "colours": tomllib.loads((ROOT / "src/r3_cli/default_theme.toml").read_text())['colours'],
        "symbols": json.loads((ROOT / "src/r3_cli/symbols.json").read_text(encoding="utf-8")),
    }
    (destination / "resources.json").write_bytes((json.dumps(resources, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode())
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.iterdir()) if p.is_file() and p.name != 'hashes.json'}
    (destination / "hashes.json").write_bytes((json.dumps(hashes, sort_keys=True, indent=2) + "\n").encode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/powershell/R3CLI')
    build(parser.parse_args().output)
