---
type: index
---

# Questions

Each document identifies one active design decision. Questions do not define the current API and do not belong as unresolved sections inside component references.

## Contents

| Question | Boundary |
|---|---|
| [[docs/questions/default-colours]] | Exact built-in RGB values for the eight tokens |
| [[docs/questions/dotnet-version]] | Stable SDK and language baseline |
| [[docs/questions/native-aot-or-jit]] | Backend execution and distribution mode |
| [[docs/questions/adapter-transport]] | Portable values and cross-process protocol |
| [[docs/questions/adapter-derivation]] | Native-language reusable contract specializations |
| [[docs/questions/default-output-scope]] | Default output ownership and session scope |
| [[docs/questions/cli-value-types]] | Typed argument/option definitions and conversion |
| [[docs/questions/help-option-parsing]] | Parsing boundaries for variadic help/explain sections |

## Reading guide

Read the affected current reference before considering an alternative. Resolve questions explicitly, integrate the accepted answer in its canonical document, and remove the resolved question and its index entry. No history or resolved-question archive is kept in `docs/`.
