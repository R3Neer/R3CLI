---
type: presentation-component
---

# Separator

A repeated pattern spanning available space, normally a continuous light horizontal line.

## Usage

```csharp
Output.Show(
    new Title("Project report"),
    new Separator());
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output/README|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public sealed class Separator : IComponent
{
    public Separator();
    public Separator(Symbol symbol);
}
```

## Composition

Uses Symbol as a pattern value. It is a block, not inline content. Section computes its own depth-specific patterns rather than changing a standalone Separator.

## Behavior and validation

Default Unicode pattern is ─ (U+2500), with ASCII - fallback. An explicit valid Symbol overrides the pattern. In ASCII mode preserve ASCII patterns and replace an unsupported non-ASCII pattern with the owner fallback. No per-call width or repeat count.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Rule | `subtext.foreground` |

### Layout

No independent lower gap and no blank line between a title and its rule. Use whole fitting graphemes; zero available cells emits no rule glyph.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/separator.png]]

[Open interactive preview](../../assets/previews/separator.html)

### Preview source

```csharp
Output.Show(
    new Title("Project report"),
    new Separator());
```
