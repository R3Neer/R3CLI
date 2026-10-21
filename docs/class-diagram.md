---
type: concept
---

# General Class Diagram

This map summarizes the current public concepts and their ownership. Detailed members and local diagrams belong to their canonical reference documents.

## Responsibilities

Presentation Components describe content; IOutput owns mounted regions. Row/Column support Table, node bases support Tree, and Help composes Sections. Command definitions feed presentation without becoming its renderer.

## Rules

Inheritance indicates API membership. Composition/association lines identify stored or referenced descriptions, not a new inheritance relationship. Symbol is a value, Row/Column are data/view descriptors, and ViewHandle is identity: none becomes inline merely because it contributes to a rendered line.

TreeNodeT below denotes `TreeNode<TData>`; it is abstract and provides typed Value over the same original Data. The diagram omits speculative parser/value/handler classes and adapter transport types.

## Class diagram

```mermaid
classDiagram
    class IComponent { <<interface>> }
    class IInlineContent { <<interface>> }
    class IMessageBody { <<interface>> }
    IComponent <|-- IInlineContent
    IInlineContent <|-- IMessageBody
    class TextBase { <<abstract>> }
    IComponent <|.. TextBase
    TextBase <|-- Text
    TextBase <|-- Subtext
    TextBase <|-- Title
    TextBase <|-- Command
    IMessageBody <|.. Text
    IMessageBody <|.. Subtext
    IInlineContent <|.. Command
    class InlineInput { <<union>> }
    class ComponentInput { <<union>> }
    InlineInput ..> IInlineContent : component case
    InlineInput ..> String : text case
    ComponentInput ..> IComponent : component case
    ComponentInput ..> String : text case
    Line ..> InlineInput : construction
    View ..> ComponentInput : construction
    IComponent <|.. Line
    Line o-- IInlineContent
    IComponent <|.. BlankLine
    class Symbol { <<readonly record struct>> }
    class TabLeader {
        <<readonly record struct>>
        +int Width
        +Symbol? Symbol
    }
    IInlineContent <|.. TabLeader
    TabLeader --> Symbol : optional fill
    IComponent <|.. Separator
    Separator --> Symbol
    class SymbolTextBase { <<abstract>> }
    IComponent <|.. SymbolTextBase
    SymbolTextBase o-- IMessageBody
    SymbolTextBase <|-- Info
    SymbolTextBase <|-- Success
    SymbolTextBase <|-- Warning
    SymbolTextBase <|-- Failure
    SymbolTextBase <|-- Activity
    IComponent <|.. Field
    Field --> TabLeader : optional separator
    IComponent <|.. Section
    Section o-- IComponent
    IComponent <|.. Banner
    Banner o-- Separator
    Banner o-- Title
    IComponent <|.. LiteralBlock
    IComponent <|.. Table
    Table o-- "1..*" Row
    Table o-- Column
    Table ..> Separator : header rule
    class ColumnTData["Column<TData>"]
    Table ..> ColumnTData : source selectors
    Column --> Alignment
    ColumnTData --> Alignment
    Row --> Object : retained source
    Column ..> Row : selects value
    Column ..> IInlineContent : presentation
    IComponent <|.. Tree
    class TreeNode { <<abstract>> }
    class TreeNodeT["TreeNode<TData>"] { <<abstract>> }
    TreeNode <|-- TreeNodeT
    Tree --> "1" TreeNode : Root
    TreeNode o-- TreeNode : Children
    TreeNode --> Line : Presentation
    IComponent <|.. Diagnostic
    Diagnostic --> DiagnosticLevel
    Diagnostic o-- IInlineContent : Recovery
    IComponent <|.. Help
    class HelpSection { <<abstract>> }
    Section <|-- HelpSection
    Help o-- HelpSection
    HelpBuilder ..> HelpSection
    HelpBuilder ..> IComponent
    IInlineContent <|.. OptionName
    IInlineContent <|.. ArgumentName
    IInlineContent <|.. SyntaxSequence
    IInlineContent <|.. Optional
    IInlineContent <|.. Repeated
    IInlineContent <|.. Alternatives
    IComponent <|.. View
    View o-- IComponent
    View --> ViewHandle
    class IOutput { <<interface>> }
    IOutput ..> IComponent : Show
    IOutput ..> ViewHandle : Update Close Remove
    IOutput <|.. StableOutput
    Output ..> IOutput : facade
    Output ..> ViewHandle : original owner
    IInlineContent <|.. Spinner
    Spinner --> Symbol : frames
    Spinner --> FrameSource
    class FrameSource { <<abstract record>> }
    class TimedFrames { <<sealed record>> }
    class SelectedFrame { <<sealed record>> }
    FrameSource <|-- TimedFrames
    FrameSource <|-- SelectedFrame
    IComponent <|.. ProgressBar
    class TaskDisplay { <<abstract>> }
    IComponent <|.. TaskDisplay
    TaskDisplay --> TaskState
    TaskDisplay o-- Spinner
    TaskDisplay o-- Diagnostic
    TaskDisplay <|-- ActivityDisplay
    TaskDisplay <|-- ProgressDisplay
    ProgressDisplay --> TaskProgress
    class TaskProgress { <<readonly record struct>> }
    IComponent <|.. StagesDisplay
    StagesDisplay o-- View : stage regions
    StagesDisplay ..> TaskDisplay : initial stages
    CliNode --> CliNode : declared Parent
    CliNode ..> Help : GetHelp
    CliNode --> CommandActivity : optional override
    class CommandActivity { <<readonly record struct>> }
```

## Example

Follow `Table -> Column -> IInlineContent` to distinguish original data selection from cell presentation. Follow `Tree -> TreeNode -> Line` to distinguish hierarchy from its labels. BlankLine only implements IComponent, so no valid path makes it eligible for Line.

See [[docs/structure]] for a complete composition and [[docs/presentation/README]] for the local contracts and diagrams. The backend availability and the purpose of documentary HTML are explained in [[docs/README]].
