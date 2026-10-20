---
type: template
---

# Command System Template

Instances use `type: command-system`. Required: purpose, responsibilities, rules and example. Include API contracts only where accepted. A class diagram is required if several related types are covered. Arguments, execution and error behavior are conditional on the subject. Never fill undecided handler/parser/portable-type contracts with invented members; link to the specific question at the relevant boundary.

## Document skeleton

````markdown
---
type: command-system
---

# {{Command system concept}}

{{Purpose}}

## Responsibilities

{{Definition, parsing, execution or presentation boundary}}

## Rules

{{Accepted behavior and validation}}

%% Conditional: accepted API is owned here. %%
## API contract

```csharp
{{Accepted API extracts}}
```

%% Conditional: several related types. %%
## Class diagram

```mermaid
{{Diagram}}
```

## Example

{{Invocation or CSharp example and explanation}}
````
