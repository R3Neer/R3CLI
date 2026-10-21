---
type: presentation-component
---

# Command

A displayed executable invocation. It is literal presentation, not a request to execute or parse a command.

## Usage

```csharp
new Command("modpack project list").Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output/README|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file. The primary constructor preserves the public camelCase value parameter; TextBase validates and retains it through the get-only Value property.

```csharp
public sealed class Command(string value) : TextBase(value), IInlineContent
{
    // Value is inherited from TextBase.
}
```

## Composition

Inherits the non-instantiable TextBase foundation; see [[docs/presentation/composition|Composition]]. Can be placed in Line. Does not implement IMessageBody.

## Behavior and validation

Value is non-null, well-formed Unicode on one logical line. Reject controls and explicit line breaks. Long content can still wrap physically.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Content | `accent.foreground` |

### Layout

No independent lower margin. Content wraps to the available terminal-cell width without adding a heading or separator.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/command.png]]

[Open interactive preview](../../assets/previews/command.html)

### Preview source

```csharp
new Command("modpack project list").Show();
```
