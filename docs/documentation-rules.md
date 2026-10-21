---
type: concept
---

# Documentation Rules

The documentation describes the current R3CLI specification. A contract is not a claim that the released implementation already provides it. Implementation availability is explained in [[docs/README]], without repeating release archaeology in individual reference pages.

## Responsibilities

Templates define document contracts; reference pages instantiate them; questions hold unresolved decisions; previews demonstrate the same cases as their C# examples.

## Rules

The following conventions apply to every current document and asset.

## Language and Markdown

Write documentation, identifiers, comments and default examples in English. Use Obsidian Markdown: YAML properties, repository-root-qualified wikilinks, image embeds, callouts, Mermaid and fenced blocks with a language. Understanding a contract must not require an Obsidian plugin. Use ordinary relative Markdown links for executable HTML previews.

Treat the repository root as the vault root. A link such as `[[docs/presentation/components/table]]` identifies a unique document. Do not use ambiguous bare `[[README]]` links.

## Document types

Each Markdown file has exactly one YAML property, `type`. It identifies its document contract:

| Type | Template |
|---|---|
| index | [[docs/templates/index]] |
| presentation-component | [[docs/templates/presentation-component]] |
| concept | [[docs/templates/concept]] |
| configuration | [[docs/templates/configuration]] |
| command-system | [[docs/templates/command-system]] |
| question | [[docs/templates/question]] |
| template | Template definitions in `docs/templates/` |

The H1 is the title; do not duplicate it in metadata. Do not add status, date, author, tags, version, dependency or question lists to YAML. Relationships belong in the content.

## Templates and ownership

Define the relevant template before instantiating a document. Required sections are always present; conditional sections are present only when their condition applies; optional sections need useful content. Remove template instructions and placeholders from instances. Never leave empty sections.

Presentation authoring contracts live in `docs/presentation/components/`. Public output contracts live in `docs/presentation/output/`; internal responsibility and dependency design lives in `docs/presentation/architecture/`. Use the existing concept and index templates for both folders, without adding metadata types. Keep internal design prose separate from public API declarations and link to the canonical owner instead of duplicating contracts.

A document owns one public concept, including its supporting types: Table owns Row/Column; Tree owns its node bases. Link to other concepts instead of maintaining duplicate contract definitions. Include a class diagram whenever the document covers several related types. The general diagram is [[docs/class-diagram]].

API extracts may omit method bodies; identify them as contract extracts rather than a compiling project. Use C# 15 preview as specified in [[docs/integration/build-baseline|Build baseline]] where useful. Do not introduce methods, inheritance, defaults or transport guarantees that have not been decided. C# examples must follow the declared composition memberships; in particular BlankLine is block-only and cannot be supplied to Line.

Use primary constructors to reduce syntax without silently changing named arguments, public properties, identity or validation. A class primary parameter is not automatically a property. Use records for specified value equality, not as a universal shorthand for every class. Get-only record properties retain validated values; positional notation must not expose an `init`/`with` route around invariants. Arrays, lists and delegates do not acquire deep semantic equality merely by belonging to a record. Preserve positional deconstruction where it is already part of the contract.

## Visual evidence

Each presentation-component document has exactly one representative capture, one current offline HTML preview and the C# composition represented by that preview. Use matching stems under `docs/assets/captures/` and `docs/assets/previews/`. A preview may offer several cases, content edits or live controls; its capture is deterministic. Live indicators start automatically unless reduced motion is requested. Capture tooling uses the documentary capture query to freeze the first frame; ordinary page loads animate. Abstract/value concepts are demonstrated through their owners or consumers rather than being given invented visual chrome.

The combined example belongs to [[docs/structure]], with its own HTML, capture and complete composition source. Previews are documentation fixtures, not a runtime or an implementation of R3CLI. They must preserve the specified tokens, line characters, spacing and structure. Do not link obsolete prototypes.

## Current state and questions

`docs/` contains current reference, current templates, active questions and current visual assets. Do not keep draft alternatives, old versions, historical appendices, release chronicles or supersession notices here. Replace the canonical wording when a decision changes. Source-control history preserves changes after commits are authorized.

An unresolved decision has one document under `docs/questions/`, using the question template. Reference it at the affected boundary when useful, without adding an Open Questions section to the reference page. A question does not define accepted behavior. Once answered, integrate the decision in its canonical location and remove the resolved question from active documentation.

## Publication checks

Check input-union normalization, string -> Text only, nonempty table rows, columns-first signatures and concrete TOML alignment values. Check metadata, required sections, unique H1 titles, local links and image targets, balanced code fences, related-type diagrams, exactly eight standard tokens, ten complete built-in presets and SDK pin consistency, current HTML/capture pairs and absence of template placeholders. Verify HTML with a real browser, including interaction and overflow. Review API/examples against the accepted contract. Documentation checks do not imply library compilation, native-shell tests or runtime implementation.

Run the standard-library checker from the repository root:

```console
python scripts/validate-docs.py
```

Recheck and recapture browser fixtures using an existing Playwright installation and Chromium executable:

```console
node scripts/capture-doc-previews.cjs --playwright-module <existing-playwright-module> --browser-executable <existing-chromium-executable>
```

The browser checker tests normal and narrow widths and explicit interaction before reporting failures. TabLeader probes cover spaces, symbols, partial pattern cycles, a segmented prefix, exhausted targets, zero width and reset. It writes captures and does not install dependencies or run R3CLI. An optional `--report <file>` writes machine-readable results outside the reference pages.

## Example

`docs/presentation/components/table.md` uses `type: presentation-component`, owns Row/Column/Table in one diagram, embeds `docs/assets/captures/table.png`, links the matching offline HTML, and includes the C# source of that same example. An unresolved transport choice belongs in its own question, not a speculative addition to the Table API.
