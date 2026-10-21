---
type: presentation-component
---

# Info

Info is a block message with a fixed indicator and an ordinary textual body.

## Usage

```csharp
new Info("Using the selected project.").Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output/README|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file. The primary constructor preserves the IMessageBody overload and its camelCase body parameter; the string overload delegates through Text. SymbolTextBase validates and retains Body as a get-only property.

```csharp
public sealed class Info(IMessageBody body) : SymbolTextBase(body)
{
    public Info(string body);
    // Body is inherited from SymbolTextBase.
}
```

## Composition

The concrete type supplies its normal and ASCII Symbol indicators. The string overload means a Text body; the IMessageBody overload preserves Text or Subtext. It is not inline and does not accept arbitrary nested components.

## Behavior and validation

Body must be non-null and obey its text contract. No per-instance indicator or colour selector. The message does not change exit status, throw an exception, execute recovery or infer task state.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Indicator | `accent.foreground` |
| Normal body | `text.foreground` |
| Explicit Subtext body | `subtext.foreground` |

### Layout

Messages may form compact consecutive lists and request no lower gap. Wrapped continuations align under the body where width permits.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/info.png]]

[Open interactive preview](../../assets/previews/info.html)

### Preview source

```csharp
new Info("Using the selected project.").Show();
```
