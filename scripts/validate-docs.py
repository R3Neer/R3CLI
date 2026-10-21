"""Validate the current Obsidian reference without importing or executing R3CLI.

Uses only the Python standard library. --root selects a checkout or a staging
tree containing docs/. Browser rendering is a separate preview check.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import struct
import sys
from urllib.parse import unquote, urlsplit

REQUIRED = {
    "index": {"Contents", "Reading guide"},
    "presentation-component": {"Usage", "API contract", "Composition", "Behavior and validation", "Presentation", "Preview"},
    "concept": {"Responsibilities", "Rules", "Example"},
    "configuration": {"Reference", "Resolution rules", "Validation", "Example"},
    "command-system": {"Responsibilities", "Rules", "Example"},
    "question": {"Question", "Context", "Alternatives", "Resolution criterion", "Affected documents"},
    "template": set(),
}
TOKENS = {
    "text.foreground", "subtext.foreground", "title.foreground",
    "accent.foreground", "success.symbol.foreground",
    "warning.symbol.foreground", "failure.symbol.foreground",
    "literal-block.background",
}


class LocalResources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "img", "link"}:
            value = attrs.get("src") or attrs.get("href")
            if value:
                self.resources.append(value)


def check(root: Path) -> dict:
    docs = root / "docs"
    errors = []
    markdown = sorted(docs.rglob("*.md"))
    components = []
    diagrams = 0

    def fail(path, message):
        errors.append(f"{path.relative_to(root)}: {message}")

    def local_link(path, target, wiki=False):
        target = unquote(target.strip().split("|", 1)[0])
        if not target or target.startswith("#") or urlsplit(target).scheme:
            return
        target = target.split("#", 1)[0]
        if not target:
            return
        resolved = (root / target) if wiki else (path.parent / target)
        if wiki and not resolved.suffix:
            resolved = resolved.with_suffix(".md")
        try:
            resolved.resolve().relative_to(root.resolve())
        except ValueError:
            fail(path, f"link leaves the checkout: {target}")
            return
        if not resolved.exists():
            fail(path, f"missing local target: {target}")

    for path in markdown:
        text = path.read_text(encoding="utf-8-sig")
        front = re.match(r"\A---\r?\ntype: ([a-z-]+)\r?\n---(?:\r?\n|$)", text)
        if not front or front.group(1) not in REQUIRED:
            fail(path, "frontmatter must contain only a recognized type")
            continue
        kind = front.group(1)
        body = text[front.end():]
        lines = body.splitlines()
        fence = None
        visible = []
        code_blocks = []
        block = []
        for line in lines:
            marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
            if fence:
                if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():
                    code_blocks.append("\n".join(block))
                    block = []
                    fence = None
                else:
                    block.append(line)
            elif marker:
                fence = marker.group(1)
                if marker.group(2).strip() == "mermaid":
                    diagrams += 1
            else:
                visible.append(line)
        if fence:
            fail(path, "unclosed code fence")
        plain = "\n".join(visible)
        if kind == "template":
            continue
        if len(re.findall(r"^# .+", plain, re.M)) != 1:
            fail(path, "expected exactly one H1")
        headings = set(re.findall(r"^## (.+)$", plain, re.M))
        for missing in REQUIRED[kind] - headings:
            fail(path, f"missing required section: {missing}")
        if re.search(r"\{\{[^}]+\}\}", body):
            fail(path, "uninstantiated template placeholder")
        if re.search(r"^#{1,3} (?:Open questions|History|Historical material|Pending decisions)\s*$", plain, re.I | re.M):
            fail(path, "historical/open-question section in current reference")
        link_text = re.sub(r"`[^`\n]+`", "", plain)
        for link in re.findall(r"!?\[\[([^\]]+)\]\]", link_text):
            local_link(path, link, wiki=True)
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", link_text):
            local_link(path, target)
        if kind == "presentation-component":
            components.append(path.stem)
            captures = re.findall(r"!\[\[([^\]]+\.png)\]\]", plain)
            html_links = re.findall(r"\[[^\]]+\]\(([^)]+\.html)\)", plain)
            if len(captures) != 1 or len(html_links) != 1:
                fail(path, "expected exactly one PNG embed and one HTML preview link")
            elif Path(captures[0]).stem != path.stem or Path(html_links[0]).stem != path.stem:
                fail(path, "preview/capture stem differs from component")
            if "### Preview source" not in plain or "```csharp" not in body.split("### Preview source")[-1]:
                fail(path, "missing C# preview source")
            declarations = re.findall(r"\b(?:class|struct|interface|enum)\s+([A-Za-z_]\w*)", "\n".join(code_blocks))
            if len(set(declarations)) > 1 and "```mermaid" not in body:
                fail(path, "multiple related types without a class diagram")

    expected = set(components) | {"structure"}
    previews = {p.stem for p in (docs / "assets/previews").glob("*.html")}
    captures = {p.stem for p in (docs / "assets/captures").glob("*.png")}
    if previews != expected:
        errors.append(f"HTML set mismatch: missing {sorted(expected-previews)}, extra {sorted(previews-expected)}")
    if captures != expected:
        errors.append(f"PNG set mismatch: missing {sorted(expected-captures)}, extra {sorted(captures-expected)}")
    for path in (docs / "assets/previews").glob("*.html"):
        parser = LocalResources()
        parser.feed(path.read_text(encoding="utf-8"))
        for resource in parser.resources:
            if urlsplit(resource).scheme or resource.startswith("//"):
                fail(path, f"preview requires nonlocal resource: {resource}")
            else:
                local_link(path, resource)
    for path in (docs / "assets/captures").glob("*.png"):
        data = path.read_bytes()
        if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 24:
            fail(path, "invalid PNG capture")
        else:
            width, height = struct.unpack(">II", data[16:24])
            if width < 1 or height < 1:
                fail(path, "empty capture dimensions")
    config = docs / "configuration/toml.md"
    if config.exists():
        source = config.read_text(encoding="utf-8-sig")
        examples = re.findall(r"```toml\n(.*?)\n```", source, re.S)
        if not examples:
            fail(config, "missing TOML schema example")
        else:
            import tomllib
            try:
                parsed = tomllib.loads(examples[0])
                if set(parsed.get("tokens", {})) != TOKENS:
                    fail(config, "example must contain exactly the eight standard tokens")
                alignment = parsed.get("presentation", {}).get("table", {}).get("alignment", {})
                expected_alignment = {"headers", "number", "text", "boolean", "date-time", "duration", "other", "mixed"}
                if set(alignment) != expected_alignment or any(value not in {"left", "center", "right"} for value in alignment.values()):
                    fail(config, "table alignment must define the accepted categories with concrete left/center/right values")
                if alignment.get("headers") != "center" or alignment.get("number") != "right":
                    fail(config, "schema example must show centered headers and right-aligned numbers")
                if "theme" in parsed:
                    fail(config, "named themes are outside the current schema")
            except tomllib.TOMLDecodeError as error:
                fail(config, f"invalid TOML example: {error}")
    # Cross-document API invariants: these check the specification, not a backend.
    invariant_files = {
        "presentation/components/tab-leader.md": (
            r"public\s+readonly\s+record\s+struct\s+TabLeader\s*:\s*IInlineContent",
            r"public\s+int\s+Width\s*\{\s*get;\s*\}",
            r"public\s+Symbol\?\s+Symbol\s*\{\s*get;\s*\}",
        ),
        "presentation/components/field.md": (
            r"public\s+Field\(string\s+label,\s*object\?\s+value,\s*TabLeader\?\s+separator\s*=\s*null\)",
        ),
        "presentation/components/table.md": (
            r"public\s+Table\(IEnumerable<Column>\s+columns,\s*Row\s+firstRow,\s*params\s+IEnumerable<Row>\s+remainingRows\)",
            r"public\s+Table\(IEnumerable<string>\s+columns,\s*IEnumerable<Row>\s+rows\)",
        ),
        "presentation/composition.md": (
            r"public\s+union\s+InlineInput\(IInlineContent,\s*string\)",
            r"public\s+union\s+ComponentInput\(IComponent,\s*string\)",
            r"public\s+object\?\s+OriginalValue\s*\{\s*get;\s*\}",
            r"public\s+Type\?\s+OriginalType\s*\{\s*get;\s*\}",
        ),
        "presentation/components/text.md": (
            r"public\s+static\s+implicit\s+operator\s+Text\(string\s+value\)",
        ),
        "presentation/components/line.md": (
            r"public\s+Line\(params\s+IEnumerable<InlineInput>\s+items\)",
            r"public\s+Line\(IEnumerable<IInlineContent>\s+items\)",
        ),
        "presentation/components/view.md": (
            r"public\s+View\(params\s+IEnumerable<ComponentInput>\s+content\)",
            r"public\s+View\(IEnumerable<IComponent>\s+content\)",
        ),
        "presentation/components/symbol.md": (
            r"public\s+readonly\s+record\s+struct\s+Symbol\b",
            r"public\s+string\s+Value\s*\{\s*get;\s*\}",
        ),
        "presentation/progress-model.md": (
            r"public\s+readonly\s+record\s+struct\s+TaskProgress\b",
            r"public\s+long\s+Completed\s*\{\s*get;\s*\}",
            r"public\s+long\?\s+Total\s*\{\s*get;\s*\}",
        ),
        "presentation/components/spinner.md": (
            r"public\s+sealed\s+record\s+SelectedFrame\(int\s+Index\)\s*:\s*FrameSource",
            r"public\s+int\s+Index\s*\{\s*get;\s*\}",
            r"public\s+int\s+IntervalMs\s*\{\s*get;\s*\}",
        ),
        "command-system/automatic-activity.md": (
            r"public\s+readonly\s+record\s+struct\s+CommandActivity\(\s*int\?\s+AfterMs,\s*string\?\s+Message\s*=\s*null\)",
            r"public\s+int\?\s+AfterMs\s*\{\s*get;\s*\}",
            r"public\s+string\?\s+Message\s*\{\s*get;\s*\}",
        ),
        "presentation/components/blank-line.md": (
            r"public\s+sealed\s+class\s+BlankLine\s*:\s*IComponent",
        ),
    }
    for relative, patterns in invariant_files.items():
        path = docs / relative
        if not path.exists():
            fail(path, "missing invariant-owning reference")
            continue
        source = path.read_text(encoding="utf-8-sig")
        api = "\n".join(re.findall(r"```csharp\n(.*?)\n```", source, re.S))
        for pattern in patterns:
            if not re.search(pattern, api):
                fail(path, f"API invariant not represented: {pattern}")
    subtext = (docs / "presentation/components/subtext.md").read_text(encoding="utf-8-sig")
    if re.search(r"implicit\s+operator\s+Subtext", subtext):
        fail(docs / "presentation/components/subtext.md", "Subtext must require explicit construction")
    table_api = (docs / "presentation/components/table.md").read_text(encoding="utf-8-sig")
    if re.search(r"public\s+Table\(IEnumerable<Row>\s+rows", table_api):
        fail(docs / "presentation/components/table.md", "Table construction must put columns first")
    if (docs / "questions/dotnet-version.md").exists():
        fail(docs / "questions/dotnet-version.md", "the C# 15 preview baseline is resolved")
    for relative in ("presentation/components/view.md", "presentation/components/tree.md", "presentation/components/stages-display.md", "presentation/output.md"):
        path = docs / relative
        if path.exists():
            source = path.read_text(encoding="utf-8-sig")
            if re.search(r"\brecord\s+(?:struct\s+)?(?:View|ViewHandle|Tree|TreeNode|StagesDisplay|StableOutput)\b", source):
                fail(path, "identity-bearing type represented as a record")
    return {"markdown": len(markdown), "components": len(components), "html_previews": len(previews), "captures": len(captures), "mermaid_diagrams": diagrams, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = check(args.root.resolve())
    print(json.dumps(result, indent=2))
    return bool(result["errors"])


if __name__ == "__main__":
    sys.exit(main())
