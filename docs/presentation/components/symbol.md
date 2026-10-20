---
type: presentation-component
---

# Symbol

An immutable printable pattern value used by owners such as Separator, Banner and Spinner. It is not an IComponent.

## Usage

```csharp
Output.Show(
    new Separator(new Symbol("=")),
    new Separator(new Symbol("=-")),
    new Separator(new Symbol("- ")));
```

Constructing the description does not print. `Show` is the explicit output boundary; see [[docs/presentation/output|Output]].

## API contract

These are API extracts, not implementation bodies or a compiling source file.

```csharp
public readonly record struct Symbol
{
    public Symbol(string value);
    public string Value { get; }
}
```

## Composition

Symbol stores a pattern, not colour, width, a clock, owning component or fallback. Each owner decides whether it admits a repeating pattern or a single-grapheme indicator.

## Behavior and validation

Value is nonempty, single-line well-formed Unicode. Reject controls, bidi controls, leading spaces, all-space patterns and isolated invisible graphemes. Ordinary spaces inside or after a visible pattern are allowed. The readonly record struct supplies generated value equality and hashing, with ordinal equality on the original string. Constructor validation and the get-only property prevent init/with mutation from bypassing validation. default(Symbol) is invalid: reading Value throws InvalidOperationException, and consumers reject it with ArgumentException at their boundary. Two invalid defaults can compare equal without becoming usable. Valid construction does not guarantee a font contains every glyph.

## Presentation

The owning component interprets the pattern; Symbol has no independent appearance.

### Colour tokens

This type owns no colour token and has no child components.

### Layout

Owners repeat only whole fitting graphemes. A last pattern cycle may be partial. Separator removes trailing generated ordinary spaces without changing Value. TabLeader instead preserves its complete padding, including trailing spaces. Width measurement belongs to layout, never string.Length.

Shared wrapping, Unicode and control handling are defined in [[docs/presentation/text-and-layout|Text and layout]]. Automatic margins collapse by maximum; explicit [[docs/presentation/components/blank-line|BlankLine]] remains additional content.

## Preview

![[docs/assets/captures/symbol.png]]

[Open interactive preview](../../assets/previews/symbol.html)

### Preview source

```csharp
Output.Show(
    new Separator(new Symbol("=")),
    new Separator(new Symbol("=-")),
    new Separator(new Symbol("- ")));
```
