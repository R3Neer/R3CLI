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
public readonly struct Symbol : IEquatable<Symbol>
{
    public Symbol(string value);
    public string Value { get; }
    public bool Equals(Symbol other);
    public override bool Equals(object? obj);
    public override int GetHashCode();
    public static bool operator ==(Symbol left, Symbol right);
    public static bool operator !=(Symbol left, Symbol right);
}
```

## Composition

Symbol stores a pattern, not colour, width, a clock, owning component or fallback. Each owner decides whether it admits a repeating pattern or a single-grapheme indicator.

## Behavior and validation

Value is nonempty, single-line well-formed Unicode. Reject controls, bidi controls, leading spaces, all-space patterns and isolated invisible graphemes. Ordinary spaces inside or after a visible pattern are allowed. Equality is ordinal on the original string. default(Symbol) is invalid: reading Value fails, and consumers reject it at their boundary. Valid construction does not guarantee a font contains every glyph.

## Presentation

The owning component interprets the pattern; Symbol has no independent appearance.

### Colour tokens

This type owns no colour token and has no child components.

### Layout

Owners repeat only whole fitting graphemes. A last pattern cycle may be partial. Remove trailing generated ordinary spaces without changing Value. Width measurement belongs to layout, never string.Length.

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
