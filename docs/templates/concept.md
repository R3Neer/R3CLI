---
type: template
---

# Concept Template

Instances use `type: concept`. Required: purpose, responsibilities, rules and an example. Contracts are conditional on owning an API; a class diagram is required if multiple related types are covered. Related documents and visual evidence are optional except that Structure must include the combined preview/capture/C# source, and Class Diagram must contain the general Mermaid diagram.

## Document skeleton

````markdown
---
type: concept
---

# {{Concept name}}

{{Purpose}}

## Responsibilities

{{Boundaries and collaborating concepts}}

## Rules

{{Current contract}}

%% Conditional: the concept owns API members. %%
## API contract

```csharp
{{API extracts}}
```

%% Conditional: multiple related types. %%
## Class diagram

```mermaid
{{Diagram}}
```

## Example

{{Example and explanation, using fenced code where relevant}}

%% Optional unless this is Structure, where all three are required. %%
## Preview

![[docs/assets/captures/{{slug}}.png]]

[Open interactive preview]({{Relative HTML path}})

```csharp
{{Matching CSharp composition}}
```
````
