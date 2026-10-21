---
type: presentation-component
---

# Line

An ordered inline composition represented as one block. A logical line may wrap or contain permitted text line breaks.

## Usage

```csharp
new Line(
    "Project: ",
    new Command("demo"),
    new Subtext("  selected")).Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public sealed class Line : IComponent
{
    public Line(params IEnumerable<InlineInput> items);
    public Line(IEnumerable<IInlineContent> items);
    public IReadOnlyList<IInlineContent> Items { get; }
}
```

## Composition

Items normalize from string or IInlineContent and are stored as IInlineContent. Text, Subtext, Command, Spinner, TabLeader and supported inline syntax pieces qualify. Line itself is not IInlineContent. BlankLine, Title, Section and standard messages cannot be inserted.

## Behavior and validation

Normalize input strings to Text; reject null/default inputs. Existing component sequences use the collection overload without element wrapping. Empty calls select the variadic overload; use a typed collection for explicit empty sequences. Snapshot the ordered input sequence. Null arrays/items are invalid. Preserve item order and do not insert implicit spaces between pieces. An empty sequence has no visible inline content.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

This component owns no colour token; its children retain theirs.

### Layout

No lower margin. Inline pieces share a block and flow in order; do not force one physical terminal row.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/line.png]]

[Open interactive preview](../../assets/previews/line.html)

### Preview source

```csharp
new Line(
    "Project: ",
    new Command("demo"),
    new Subtext("  selected")).Show();
```

## Additional examples

```csharp
IEnumerable<IInlineContent> pieces =
    [new Command("demo"), new Subtext(" selected")];
var fromSequence = new Line(pieces);
var mixed = new Line("Project: ", new Command("demo"));
// Invalid: BlankLine is block-only.
// new Line(new BlankLine());
```
