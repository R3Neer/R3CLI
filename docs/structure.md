---
type: concept
---

# Structure

R3CLI separates original data, presentation descriptions, output sessions and the Command System. Components can be composed without writing anything; a presentation reaches a terminal only through an output boundary.

## Responsibilities

| Layer | Responsibility |
|---|---|
| Original data | Retain values and relationships without substituting formatted text |
| Presentation Components | Describe semantic text, layout, messages, data views, help and progress |
| Output | Mount descriptions, return handles, update or close owned regions and select stable behavior |
| Configuration | Resolve direct token values and output preferences |
| Command System | Define commands, derive help, coordinate execution/activity and map failures to diagnostics |
| Adapters | Offer idiomatic authoring and preserve native structured values |

The complete type map is [[docs/class-diagram]]. Component contracts are under [[docs/presentation/README]]. [[docs/presentation/output/README|Output]] borrows .NET TextWriter destinations through scoped contexts. [[docs/presentation/architecture/spectre-console|Spectre.Console]] supplies rendering and detection internally; R3CLI retains session and handle ownership.

## Rules

- Construction is side-effect free with respect to output. Show is explicit.
- Original values are independent of labels and formatted cells. A numeric size remains numeric even when presented as a compact string.
- Inline eligibility is explicit. BlankLine, Title, Section, Table, Tree and View are blocks; BlankLine cannot be passed to Line.
- Composition does not recolour children. Eight standard tokens have fixed meanings; custom names resolve against the direct TOML dictionary.
- An ordinary description can be reused; explicit View identity belongs to a mounted region and has a single placement lifetime.
- Human rendering does not become native Nushell/PowerShell data by detecting the shell. Adapters preserve supported values separately.
- The visual Tree has one root and child-defined relationships. The Command System has parent-declared relationships and derives children.
- A live task display describes state; it does not execute work or infer success from 100 percent.

## Example

The combined fixture uses the Catppuccin Mocha preset on its simulated reference background; theme selection does not paint the user's terminal by default. [[docs/configuration/built-in-themes|Built-in themes]] compares the light/dark profiles. The combined fixture exercises every Presentation Component, the eight tokens, shared margins, Unicode rules, tree branches, a real-data table and an editable live region. The interactive preview exposes a theme selector that updates both semantic colours and the simulated terminal background, together with animation and explicit region-update controls. Individual component previews keep a fixed preset. It is a documentation prototype, not the R3CLI backend.

The `command` parameter below is an application-owned CliNode whose generated help describes `modpack project use`: usage `modpack project use <name>`, options `--no-human` and `-h, --help`, and an example `modpack project use demo`. It supplies the usage/options/examples sections selected by this fixture. The CLI parser/typed definition mechanism is not invented by this example.

The input helper Category is an example application record, not an R3CLI type. Categories are retained as original typed source values by Tree.From; the data selector declares their named structured fields.

## Preview

![[docs/assets/captures/structure.png]]

[Open interactive preview](assets/previews/structure.html)

```csharp
// API usage extract. The host supplies its application-owned command.
static ViewHandle ShowPresentation(CliNode command, out ViewHandle metadata)
{
    var categories = new Category("Packages", 12,
    [
        new Category("Client", 8, []),
        new Category("Shared", 4, [])
    ]);

    var table = new Table(
        ["Name", "Files"],
        new Row("demo", 12), new Row("test", 3));

    var leader = new TabLeader(12, new Symbol("."));

    var tree = Tree.From(categories,
        data: category => new Dictionary<string, object?>
        {
            ["name"] = category.Name,
            ["count"] = category.Count
        },
        children: category => category.Children,
        presentation: category => new Line(
            category.Name,
            new Subtext($"  {category.Count}")));

    var metadataView = new View(
        new ActivityDisplay("Reading metadata"));

    var stages = new StagesDisplay("Updating project",
        new ActivityDisplay("Resolve dependencies"),
        new ActivityDisplay("Download files", state: TaskState.Pending),
        new ActivityDisplay("Validate project", state: TaskState.Pending));

    var report = Output.Show(
        new Banner("R3CLI presentation"),
        new Section("Introduction",
            new Line("Primary text. ",
                new Subtext("Additional details.")),
            new Title("Project report"),
            new Command("modpack project use demo"),
            new Line("Project: ", new Subtext("demo selected")),
            new BlankLine(),
            new Separator(new Symbol("=-"))),
        new Section("Messages",
            new Info("Using the selected project."),
            new Success("Configuration saved."),
            new Warning("Optional metadata is missing."),
            new Failure("The operation could not complete."),
            new Activity("Checking package metadata.")),
        new Section("Project",
            new Field("Project", "demo"),
            new Section("Content",
                new Field("Files", 12),
                new Section("Validation", new Success("Checks passed.")))),
        new LiteralBlock("Name    Status\ndemo    ready"),
        new Section("Aligned fields",
            new Field("Name", "demo", leader),
            new Field("Files", 12, leader),
            new Line("Note",
                new TabLeader(12, new Symbol("_-\\_")),
                "Local")),
        table,
        tree,
        new Diagnostic(DiagnosticLevel.Warning,
            "Project.OptionalMetadata",
            "Optional metadata is missing.",
            details: "The project can still be inspected.",
            recovery: new Command("modpack content check")),
        command.GetHelp().SelectSections("usage", "options", "examples"),
        metadataView,
        new Spinner(),
        new ProgressBar(12, 40),
        stages);

    metadata = metadataView.Handle;
    return report;
}

// The host establishes an enclosing Output.Use(Console.Error) scope,
// calls ShowPresentation(command, out var metadata), and keeps the scope
// alive while using the returned handles.
// The preview's update action corresponds to:
static void UpdateMetadata(ViewHandle metadata) =>
    metadata.Update(new ProgressDisplay("Reading metadata",
        new TaskProgress(12, 40, "files")));

public sealed record Category(string Name, int Count, Category[] Children);
```

The code includes literal examples of Info, Success, Warning, Failure and static Activity rather than recolouring arbitrary strings. Title has its own colour. Separator patterns and tree branches use Subtext's token. The LiteralBlock is compact and separated from following content. The nested Section branch demonstrates `═`, `─`, then `-`.

Table places a default continuous Separator below the headers across the full table width, without changing structured data. Table takes columns first, requires at least one data row, centers headers and uses configured Auto cell alignment. The compact Table constructor maps header strings to positional Columns without changing Row or hiding unselected data. TabLeader targets a logical line-prefix width in terminal cells. Explicit Field leaders replace the default colon and gap; the same inline value can align a Line. The underscores/backslash pattern is literal Symbol content, not an escape language interpreted by R3CLI.

Help is generated from the supplied command, not hand-constructed. Its content has no Banner. View updates replace the metadata region without producing new automatic blank lines per frame. Live indicators animate automatically unless reduced motion is requested; pause/play controls remain available. Removing the metadata View leaves unrelated indicators running. Known progress counts change through explicit updates, not elapsed time. The static capture freezes the initial state; the browser fixture can display the explicit progress replacement.
