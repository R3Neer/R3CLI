---
type: presentation-component
---

# Field

A compact textual label/value pair. Scalar wrappers are unnecessary for this presentation.

## Usage

```csharp
Output.Show(
    new Field("Project", "demo"),
    new Field("Files", "12"));
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public sealed class Field : IComponent
{
    public Field(string label, string value);
    public string Label { get; }
    public string Value { get; }
}
```

## Composition

Composes a secondary label and colon followed by normal text. Values here are textual; use Table or an application data model to retain typed domain values.

## Behavior and validation

Label and value are non-null single logical lines with well-formed Unicode and no controls. Do not parse values or infer commands. The value is a string, not a new Scalar type.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Label and colon | `subtext.foreground` |
| Value | `text.foreground` |

### Layout

No lower gap between fields. A single logical line may wrap physically; reduce indentation before hiding content.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/field.png]]

[Open interactive preview](../../assets/previews/field.html)

### Preview source

```csharp
Output.Show(
    new Field("Project", "demo"),
    new Field("Files", "12"));
```
