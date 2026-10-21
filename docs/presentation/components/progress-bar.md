---
type: presentation-component
---

# ProgressBar

A compact bar for known counts, with the completed and pending portions sharing existing text tokens.

## Usage

```csharp
new ProgressBar(completed: 12, total: 40).Show();
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output/README|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public sealed class ProgressBar : IComponent
{
    public ProgressBar(long completed, long total);
}
```

## Composition

ProgressBar is the standalone known-total bar. Use ProgressDisplay to obtain a ready-made title, state indicator, counts and details. It is a block and does not itself own a ViewHandle.

## Behavior and validation

Counts must be nonnegative and completed must not exceed total. Zero/zero is an empty workload represented as 100 percent; it does not imply execution success. Replacement values can decrease; do not clamp them silently.

## Presentation

The preview shows the semantic arrangement. Browser rendering is illustrative; it does not verify terminal cell measurement.

### Colour tokens

| Part | Token |
|---|---|
| Completed portion | `text.foreground` |
| Pending portion | `subtext.foreground` |

### Layout

Fit the bar to available space without inventing progress. A complete progress block requests one collapsed lower gap. No new bar-specific tokens or TOML width setting.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/progress-bar.png]]

[Open interactive preview](../../assets/previews/progress-bar.html)

### Preview source

```csharp
new ProgressBar(completed: 12, total: 40).Show();
```

## Structured data

Counts remain numbers independent of bar glyphs. Keep the application progress/state model when exporting structured data; do not infer counts from rendered fill.

## Live behavior

Update the owning output handle with a replacement ProgressBar to change counts. Reaching total neither closes the handle nor marks the operation Succeeded.
