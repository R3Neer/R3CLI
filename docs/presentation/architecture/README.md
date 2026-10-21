---
type: index
---

# Presentation architecture

The presentation backend fulfills the accepted component and output contracts independently of the Command System. This folder owns internal responsibilities and dependency choices; component reference pages own public authoring contracts. These documents specify design, not implemented runtime behavior.

## Contents

- [[docs/presentation/architecture/model-and-construction|Model and construction]] defines the accepted phase 1 capture model and internal contracts.
- [[docs/presentation/architecture/spectre-console|Spectre.Console integration]] defines the accepted rendering/detection dependency and delegation limits.
- [[docs/presentation/output/README|Output]] defines the public boundary, session lifetime, capabilities and handles.
- [[docs/presentation/composition|Composition]] defines the current description model and original-value retention.
- [[docs/presentation/text-and-layout|Text and layout]] defines the shared observable layout guarantees.

## Reading guide

Design in the following order. These are responsibility boundaries to examine, not a declaration of seven new classes or an already completed internal architecture.

| Step | Design responsibility | Evidence to use |
|---|---|---|
| 1 | [[docs/presentation/architecture/model-and-construction|Component construction, data capture and validation]] | Closed design: node-owned captures, CapturedTable and shared normalization; no runtime implementation |
| 2 | Presentation context | Borrowed writer, configuration, capabilities, theme and dimensions |
| 3 | Measurement and composition | Terminal cells, wrapping, alignment, margins and children |
| 4 | Static rendering | Components to styled output; exact Spectre reuse |
| 5 | Sessions and views | Placement identity, nested handles, lifetime and safe editable regions |
| 6 | Motion | Monotonic time, selected frames, refresh and serialized updates |
| 7 | Integration | Stable output, native structured values and language adapters |

For each boundary, identify logical responsibilities, define black-box contracts and exercise complete scenarios before choosing internal classes. Start with construction through first static write. Then test a table in a file, a nested View updated beside an active spinner, a narrower window, structured stdout with human stderr, and disposal while animations are active. Extend the internal design only as those scenarios require; do not infer new public APIs from a responsibility name.

Develop the Command System after these presentation boundaries: help, diagnostics and automatic command activity consume presentation without becoming its renderer. Open deployment and adapter transport decisions remain in [[docs/questions/README|Questions]].
