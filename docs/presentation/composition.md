---
type: concept
---

# Composition

Components are descriptions. Construction neither writes terminal bytes nor starts commands, clocks or tasks.

## Responsibilities

Define which descriptions can be shown, joined inline or used as a message body. Shared layout, output sessions and domain-data conversion belong to their own contracts.

## API contract

```csharp
public interface IComponent { }
public interface IInlineContent : IComponent { }
public interface IMessageBody : IInlineContent
{
    string Value { get; }
}

// Authoring foundations; not direct user-created generic components.
public abstract class TextBase(string value) : IComponent
{
    public string Value { get; }
}

public abstract class SymbolTextBase(IMessageBody body) : IComponent
{
    public IMessageBody Body { get; }
}
```

Primary-constructor parameters are camelCase inputs, not automatically exposed properties. Value and Body remain explicitly declared get-only properties; the actual constructor validates before retaining them. These extracts omit the validation bodies. The foundations identify shared members; their exact protected customization spelling is not a new accepted extension API. Ordinary custom composition reuses supported components. A marker interface alone does not register an arbitrary renderer.

## Rules

| Kind | Members |
|---|---|
| Text message bodies and inline pieces | Text, Subtext |
| Other inline pieces | Command, Spinner, TabLeader, help syntax pieces |
| Block-only descriptions | Title, Line, BlankLine, messages, Field, Section, Banner, LiteralBlock, Table, Tree, Diagnostic, Help, View, progress displays |
| Argument values, not components | Symbol, Row, Column, TreeNode, TaskProgress, FrameSource |
| Output services, not components | IOutput, Output, StableOutput |

BlankLine cannot be placed in Line. Line itself is not inline. A standard message accepts IMessageBody, not an arbitrary IComponent.

## Class diagram

```mermaid
classDiagram
    IComponent <|-- IInlineContent
    IInlineContent <|-- IMessageBody
    IComponent <|.. TextBase
    TextBase <|-- Text
    TextBase <|-- Subtext
    TextBase <|-- Title
    TextBase <|-- Command
    IMessageBody <|.. Text
    IMessageBody <|.. Subtext
    IInlineContent <|.. Command
    IInlineContent <|.. TabLeader
    IComponent <|.. Line
    Line o-- IInlineContent
    IComponent <|.. BlankLine
    IComponent <|.. SymbolTextBase
    SymbolTextBase --> IMessageBody
```

## String convenience and reuse

Strings in visual-content positions mean Text. This is a binding/API convenience, not a claim that a C# implicit conversion to an interface works automatically. Structural strings such as headers, field names, codes and Symbol patterns keep their structural role. Examples use explicit Text at interface positions.

Descriptions normally snapshot their child sequences and are reusable. Explicit View identity has a single placement lifetime; see [[docs/presentation/components/view|View]]. Colours belong to semantic pieces and survive composition, rather than being inherited indiscriminately from a container.

## Example

```csharp
var content = new Section("Project",
    new Line(new Text("Name: "), new Command("demo")),
    new BlankLine(),
    new Info(new Subtext("Local configuration")));
content.Show();
```

## Representation

Small immutable values with useful structural equality use readonly record structs: Symbol, TabLeader and TaskProgress. Validated constructors and get-only properties preserve their invariants; positional init properties are not introduced just to shorten the declaration. Value-type defaults have explicit documented meanings.

Simple text/message descriptors remain classes and use primary constructors where that makes the input clearer. Row, Column, Table, Line, Section, Tree, Help, View, ViewHandle and StagesDisplay remain classes: collections, composition, specialization and placement identity do not become clearer merely by changing their representation. FrameSource is an abstract record, with validated sealed-record source descriptions. IOutput is an interface, Output is a static facade, and StableOutput is a stateful class.

Value semantics do not promise zero allocations: boxing a value through object/interface storage can allocate. Consumer callbacks, terminal ownership and adapter serialization are separate concerns from C# representation.
