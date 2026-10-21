---
type: index
---

# Presentation

Presentation Components describe terminal output without printing during construction. Output actions own placement and lifetime. This is a design specification for the C# backend and its adapters, not a claim that the new API is implemented.

## Contents

### Foundations

- [[docs/presentation/composition|Composition]] — membership, authoring bases and reuse.
- [[docs/presentation/text-and-layout|Text and layout]] — Unicode, wrapping, controls and spacing.
- [[docs/presentation/output/README|Output]] — TextWriter contexts, Show, Update, Close, Remove and stable output.
- [[docs/presentation/architecture/README|Presentation architecture]] — design sequence and Spectre.Console rendering/detection boundary.
- [[docs/presentation/progress-model|Progress model]] — state and counts independent of execution.

### Components

#### Text and composition

[[docs/presentation/components/text|Text]] · [[docs/presentation/components/subtext|Subtext]] · [[docs/presentation/components/title|Title]] · [[docs/presentation/components/command|Command]] · [[docs/presentation/components/line|Line]] · [[docs/presentation/components/blank-line|BlankLine]] · [[docs/presentation/components/symbol|Symbol]] · [[docs/presentation/components/tab-leader|TabLeader]] · [[docs/presentation/components/separator|Separator]]

#### Messages and organization

[[docs/presentation/components/info|Info]] · [[docs/presentation/components/success|Success]] · [[docs/presentation/components/warning|Warning]] · [[docs/presentation/components/failure|Failure]] · [[docs/presentation/components/activity|Activity]] · [[docs/presentation/components/field|Field]] · [[docs/presentation/components/section|Section]] · [[docs/presentation/components/banner|Banner]] · [[docs/presentation/components/literal-block|LiteralBlock]]

#### Data and explanation

[[docs/presentation/components/table|Table, Row and Column]] · [[docs/presentation/components/tree|Tree and node bases]] · [[docs/presentation/components/diagnostic|Diagnostic]] · [[docs/presentation/components/help|Help]]

#### Live feedback

[[docs/presentation/components/view|View and ViewHandle]] · [[docs/presentation/components/spinner|Spinner and frame sources]] · [[docs/presentation/components/progress-bar|ProgressBar]] · [[docs/presentation/components/activity-display|ActivityDisplay]] · [[docs/presentation/components/progress-display|ProgressDisplay]] · [[docs/presentation/components/stages-display|StagesDisplay]]

## Reading guide

Start with Composition and Text and layout, then read the component whose semantics you need. Read Output before using live handles; read Progress model before task displays.

### Related specifications

[[docs/configuration/colour-tokens|Colour tokens]] owns colour names, not the component documents. [[docs/structure|Structure]] contains the integrated example. [[docs/class-diagram|Class diagram]] shows the complete design.
