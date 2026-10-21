---
type: presentation-component
---

# Title

A block heading with its own colour and emphasis. It is not inline content and does not create a Section or infer a section level.

## Usage

```csharp
new Title("Project report").Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output/README|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file. The primary constructor preserves the public camelCase value parameter; TextBase validates and retains it through the get-only Value property.

```csharp
public sealed class Title(string value) : TextBase(value)
{
    // Value is inherited from TextBase.
}
```

## Composition

Inherits the non-instantiable TextBase foundation; see [[docs/presentation/composition|Composition]]. Cannot be placed in Line. Does not implement IMessageBody.

## Behavior and validation

Value is non-null, well-formed Unicode on one logical line. Reject controls and explicit line breaks. Long content can still wrap physically.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Content | `title.foreground` |

### Layout

No independent lower margin. Text wraps to the available terminal-cell width; Title retains its heading identity without adding a separator.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/title.png]]

[Open interactive preview](../../assets/previews/title.html)

### Preview source

```csharp
new Title("Project report").Show();
```
