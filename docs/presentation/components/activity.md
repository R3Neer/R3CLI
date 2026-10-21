---
type: presentation-component
---

# Activity

Activity is a block message with a fixed indicator and an ordinary textual body. Activity describes ongoing work but is static; use Spinner or ActivityDisplay for animation.

## Usage

```csharp
new Activity("Checking package metadata.").Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output/README|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file. The primary constructor preserves the IMessageBody overload and its camelCase body parameter; the string overload delegates through Text. SymbolTextBase validates and retains Body as a get-only property.

```csharp
public sealed class Activity(IMessageBody body) : SymbolTextBase(body)
{
    public Activity(string body);
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

![[docs/assets/captures/activity.png]]

[Open interactive preview](../../assets/previews/activity.html)

### Preview source

```csharp
new Activity("Checking package metadata.").Show();
```
