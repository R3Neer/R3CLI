---
type: presentation-component
---

# Subtext

Secondary literal text, used for supporting detail without changing the meaning of the data.

## Usage

```csharp
new Line("demo", new Subtext("  local project")).Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file. TextBase captures the original value, runtime type and textual representation through get-only properties; conversion and validation bodies are omitted.

```csharp
public sealed class Subtext(object? value) : TextBase(value), IMessageBody
{
    // OriginalValue, OriginalType and Value are inherited from TextBase.
}
```

## Composition

Inherits the non-instantiable TextBase foundation; see [[docs/presentation/composition|Composition]]. Can be placed in Line. Implements IMessageBody and can be a standard message body.

## Behavior and validation

Use the shared value-to-text policy in [[docs/presentation/composition|Composition]]. There is no implicit conversion from string to Subtext. Value is non-null and well-formed Unicode. Explicit LF/CRLF and internal empty lines are preserved; unsupported controls are rendered visibly rather than interpreted. Empty text does not itself force a blank line.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Content | `subtext.foreground` |

### Layout

No independent lower margin. Content wraps to the available terminal-cell width without adding a heading or separator.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/subtext.png]]

[Open interactive preview](../../assets/previews/subtext.html)

### Preview source

```csharp
new Line("demo", new Subtext("  local project")).Show();
```
