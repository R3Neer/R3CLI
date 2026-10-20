---
type: presentation-component
---

# Text

Primary literal text. Strings in visual-content positions have the semantic shorthand meaning Text; the adapter or C# binding realizes that convenience.

## Usage

```csharp
new Text("Project ready").Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public sealed class Text : TextBase, IMessageBody
{
    public Text(string value);
    // Value is inherited from TextBase.
}
```

## Composition

Inherits the non-instantiable TextBase foundation; see [[docs/presentation/composition|Composition]]. Can be placed in Line. Implements IMessageBody and can be a standard message body.

## Behavior and validation

Value is non-null and well-formed Unicode. Explicit LF/CRLF and internal empty lines are preserved; unsupported controls are rendered visibly rather than interpreted. Empty text does not itself force a blank line.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Content | `text.foreground` |

### Layout

No independent lower margin. Content wraps to the available terminal-cell width without adding a heading or separator.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/text.png]]

[Open interactive preview](../../assets/previews/text.html)

### Preview source

```csharp
new Text("Project ready").Show();
```
