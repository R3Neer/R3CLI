---
type: presentation-component
---

# LiteralBlock

Literal text displayed on one compact, soft-background rectangle. It neither executes examples nor interprets terminal markup.

## Usage

```csharp
Output.Show(
    new LiteralBlock("Name    Status\ndemo    ready"),
    "The project is ready.");
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public sealed class LiteralBlock : IComponent
{
    public LiteralBlock(string content);
}
```

## Composition

Contains literal text, not a nested component tree. The foreground remains ordinary Text; the background covers content and padding.

## Behavior and validation

Content is non-null well-formed Unicode. Preserve internal line breaks and empty lines. Empty content retains one empty padded row. ANSI and unsupported controls become visible escapes; tabs expand to four-cell stops relative to content origin.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Content | `text.foreground` |
| Rectangle including padding | `literal-block.background` |

### Layout

Use one rectangle sized to the widest displayed line plus one cell of padding on each side, capped by available width. Short lines share the rectangle. Reduce padding and wrap when necessary. Request one collapsed lower gap before following content.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/literal-block.png]]

[Open interactive preview](../../assets/previews/literal-block.html)

### Preview source

```csharp
Output.Show(
    new LiteralBlock("Name    Status\ndemo    ready"),
    "The project is ready.");
```
