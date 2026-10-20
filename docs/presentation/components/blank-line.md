---
type: presentation-component
---

# BlankLine

One explicit empty block line used to separate content. It is not inline whitespace.

## Usage

```csharp
Output.Show(
    new Text("Before"),
    new BlankLine(),
    new Text("After"));
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public sealed class BlankLine : IComponent
{
    public BlankLine();
}
```

## Composition

BlankLine implements IComponent only. It can be a Show argument or a child of Section/View. It never implements IInlineContent; new Line(new BlankLine()) is invalid.

## Behavior and validation

It represents one explicitly requested empty line. It is distinct from automatic block margins and empty Text. There is no count parameter; repeat descriptions if multiple explicit lines are needed.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

This type owns no colour token and has no child components.

### Layout

Explicit empty lines are retained. They are not silently consumed by the automatic margin-collapse algorithm.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/blank-line.png]]

[Open interactive preview](../../assets/previews/blank-line.html)

### Preview source

```csharp
Output.Show(
    new Text("Before"),
    new BlankLine(),
    new Text("After"));
```
