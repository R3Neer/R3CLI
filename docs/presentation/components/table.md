---
type: presentation-component
---

# Table

A row-oriented data view. Row preserves values; Column selects and presents a value from each row. Human formatting never replaces original data.

## Usage

```csharp
var table = new Table(
    [new Row("README.md", 2048L), new Row("main.cs", 1024L)],
    new Column("Name", index: 0),
    Column.For<long>("Size", index: 1,
        presentation: bytes => new Subtext($"{bytes / 1024} KiB")));
table.Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public sealed class Row
{
    public Row(params object?[] values);
    public static Row FromFields(IReadOnlyDictionary<string, object?> fields);
    public int Count { get; }
    public IReadOnlyList<object?> Values { get; }
    public IReadOnlyList<string>? FieldNames { get; }
    public object? this[int index] { get; }
    public object? this[string field] { get; }
    public bool TryGetValue(string field, out object? value);
}

public sealed class Column
{
    public Column(string header, int index,
        Func<object?, IInlineContent>? presentation = null);
    public Column(string header, string field,
        Func<object?, IInlineContent>? presentation = null);
    public static Column For<TValue>(string header, int index,
        Func<TValue, IInlineContent> presentation);
    public static Column For<TValue>(string header, string field,
        Func<TValue, IInlineContent> presentation);
    public string Header { get; }
    public int? Index { get; }
    public string? Field { get; }
    public Func<object?, IInlineContent>? Presentation { get; }
    internal object? ReadValue(Row row);
    internal IInlineContent CreateCell(Row row);
}

public sealed class Table : IComponent
{
    public Table(IEnumerable<Row> rows, params Column[] columns);
    public IReadOnlyList<Row> Rows { get; }
    public IReadOnlyList<Column> Columns { get; }
    internal void Validate();
    internal IInlineContent GetCell(int rowIndex, int columnIndex);
}
```

## Composition

Rows are data and columns are selectors, not separate lists of cells. Header is mandatory. A column selects exactly one field or index, established by its constructor. The internal ReadValue and CreateCell seams separate lookup from visual representation; sealed types require no protected API.

```mermaid
classDiagram
    IComponent <|.. Table
    Table o-- "0..*" Row : rows
    Table o-- "0..*" Column : columns
    Column ..> Row : reads
    Column ..> IInlineContent : presents
```

## Behavior and validation

Snapshot input containers without promising arbitrary deep cloning. Named fields compare exactly; missing differs from null. Validate absent fields/indices and type compatibility before output, reporting row and column. For<TValue> returns an ordinary Column. Do not parse numeric strings or silently convert types. Nullable value types allow null; reference annotations do not create a distinct runtime type. Evaluate presentation once per cell snapshot and reuse it for layout.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Default headers | `subtext.foreground` |
| Default values | `text.foreground` |
| Custom cells | `Tokens of their inline components` |

### Layout

Cells can wrap or contain permitted explicit breaks; row height is the tallest cell. Column minimum is min(natural width, 8 cells). If minimums plus gaps do not fit, render labelled vertical records, preserving labels and order. Request one lower gap after the complete table.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/table.png]]

[Open interactive preview](../../assets/previews/table.html)

### Preview source

```csharp
var table = new Table(
    [new Row("README.md", 2048L), new Row("main.cs", 1024L)],
    new Column("Name", index: 0),
    Column.For<long>("Size", index: 1,
        presentation: bytes => new Subtext($"{bytes / 1024} KiB")));
table.Show();
```

## Structured data

Rows retain supported original values and field names independently of headers and presentation. The numeric value 2048L stays numeric when its cell reads 2 KiB. Displayed columns do not implicitly project away unselected fields. Adapters accept native rows/records and build these descriptions internally. See [[docs/integration/adapter-boundaries|Adapter boundaries]].

## Customization

Column presentation accepts an inline descriptor. Use For<TValue> in C# to avoid casts; foreign adapters evaluate their own callbacks. A callback does not cross processes as an arbitrary CLR delegate.

```csharp
var row = Row.FromFields(new Dictionary<string, object?>
{
    ["name"] = "demo",
    ["files"] = 12
});
var namedTable = new Table([row],
    new Column("Name", field: "name"),
    new Column("Files", field: "files"));
```
