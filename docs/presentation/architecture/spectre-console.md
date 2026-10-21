---
type: concept
---

# Spectre.Console integration

Use Spectre.Console internally for rendering and terminal detection, with R3CLI-owned sessions and ViewHandles. The dependency does not alter public component contracts or require consumers and adapters to construct Spectre objects.

## Responsibilities

| Responsibility | Owner |
|---|---|
| ANSI/colour capabilities, environment and CI evidence | Spectre.Console detection, interpreted by R3CLI policy |
| Styled segments, ANSI generation and supported layout primitives | Spectre.Console |
| Component validation, original values and callback capture | R3CLI |
| Tokens, built-in theme selection, local background and spacing policy | R3CLI |
| Component-specific layout/fallback guarantees | R3CLI, reusing compatible Spectre primitives |
| Output scopes, nested handles and editable-region ownership | R3CLI |
| Motion/state coordination and stable event history | R3CLI |
| Native structured values and adapter boundaries | R3CLI and its adapters |

## Rules

### Rendering boundary

Project accepted descriptions into internal Spectre IRenderable objects or styled segments. Public IComponent does not inherit IRenderable. Spectre types remain absent from public signatures and portable adapter values. Use an instance configured for the borrowed TextWriter, rather than relying on Spectre's process-wide static console. Do not transfer writer ownership to the rendering session.

Prefer existing text/layout primitives when they satisfy the documented result. Adapt or supply custom renderables for pattern separators, TabLeader, local LiteralBlock geometry, table rules/alignment, narrow-width fallbacks and collapsed margins. Preserve literal text: do not send arbitrary strings through markup overloads. For example, Spectre 0.57.2's string TableColumn constructor creates Markup with ellipsis, which is not our literal-header/wrapping contract.

Capture conversions and consumer callback results at their specified boundary. Measurement and repaint may traverse the internal renderable repeatedly without rerunning consumer callbacks or converting original values again. Retain original domain values separately; styled segments are not a serialization model. Spectre's cell measurement is reusable infrastructure, not a substitute for verifying grapheme handling, terminal/font behavior and all shared layout invariants.

### Sessions and live regions

Use R3CLI coordination for Show, Update, Close and Remove. Do not create a concurrent Spectre LiveDisplay/Status/Progress operation per ViewHandle. A group may freeze independently of other active groups, and child identities follow the View contract. Spectre's high-level live callbacks do not supply those semantics directly.

Do not delegate owned-region management directly to LiveDisplay. In the reviewed stable version 0.57.2, LiveRenderable.PositionCursor may call EraseInDisplay(2), ClearScrollback and CursorHome when its previous shape exceeds the resized terminal dimensions. That behavior violates the contract against clearing unrelated screen content/history. Use compatible static rendering and ANSI operations under R3CLI's region coordinator; do not depend on private Spectre live classes or fork them into the public model.

Coordinate frame selection, refresh, physical terminal ownership and stable fallback in R3CLI. Disabling colour does not disable all cursor capability, and enabling colour does not grant it. [[docs/presentation/output/capabilities|Capabilities]] owns effective policy. Background queries and theme matching require our separate bounded, input-coordinated mechanism.

### Dependency and verification boundary

The source audit baseline is Spectre.Console 0.57.2, not a declaration that a package is installed or a runtime project now exists. Choose and pin the actual package version with the implementation baseline, then recheck the relevant behavior on upgrades. The selected dependency is the full Spectre.Console rendering/detection package; its separate ANSI package supplies low-level functionality underneath it. No CLI-parser dependency is selected by this decision.

The reviewed project declares IsAotCompatible for modern target frameworks and uses the MIT license. Those facts do not prove our own Native AOT publication, startup cost, package size or rendering performance. Validate those on the implementation, alongside Windows and supported native shells.

Before accepting the integration, verify independently redirected stdout/stderr, files/strings/wrapped writers, plain strings containing markup-like text, Unicode/control handling, exact table/tree layout, narrow/zero widths, nested handles, partial Close/Remove, resize and overflow, concurrent updates, cancellation/disposal, stable logs and clean structured output. Compare rendered behavior against our contracts, not merely a Spectre snapshot.

## Example

```csharp
using var scope = Output.Use(Console.Error);
var details = new View(new Field("Files", 12));
var report = Output.Show(new Title("Project report"), details);
details.Handle.Update(new Field("Files", 25));
details.Handle.Close();
report.Remove();
```

The caller uses only R3CLI and .NET types. Internally, R3CLI retains the view identities and selects the compatible Spectre rendering operations. No internal renderer class or registration API is introduced by this example.

## Sources

- [Spectre.Console 0.57.2 package](https://www.nuget.org/packages/Spectre.Console/0.57.2).
- [IRenderable measurement and segment contract](https://github.com/spectreconsole/spectre.console/blob/0.57.2/src/Spectre.Console/Rendering/IRenderable.cs).
- [TableColumn string handling](https://github.com/spectreconsole/spectre.console/blob/0.57.2/src/Spectre.Console/Widgets/Table/TableColumn.cs).
- [LiveDisplay behavior and concurrency limits](https://spectreconsole.net/console/live/live-display/).
- [LiveRenderable resize behavior](https://github.com/spectreconsole/spectre.console/blob/0.57.2/src/Spectre.Console/Live/LiveRenderable.cs).
- [ANSI writer](https://github.com/spectreconsole/spectre.console/blob/0.57.2/src/Spectre.Console.Ansi/AnsiWriter.cs).
- [AOT project settings](https://github.com/spectreconsole/spectre.console/blob/0.57.2/src/Spectre.Console/Spectre.Console.csproj) and [MIT license](https://github.com/spectreconsole/spectre.console/blob/0.57.2/LICENSE.md).
