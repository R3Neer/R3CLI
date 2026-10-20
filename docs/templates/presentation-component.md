---
type: template
---

# Presentation Component Template

Instances use `type: presentation-component`. Required fields: name, purpose, minimal usage, API contract, API explanation, composition, behavior/validation, visual structure, tokens, layout, one capture, one HTML link and corresponding C# preview source. A class diagram is required when several related types are documented. Structured data, live behavior and customization are conditional; additional examples are optional. Remove instructions and nonapplicable sections in instances.

## Document skeleton

````markdown
---
type: presentation-component
---

# {{Component name}}

{{Purpose and meaning}}

## Usage

```csharp
{{Minimal usage example}}
```

{{Explanation}}

## API contract

These are API extracts; method bodies are omitted.

```csharp
{{Public and relevant protected/internal contracts}}
```

{{Member responsibilities}}

## Composition

{{Accepted children, supporting types and reused components}}

%% Required if multiple related types are covered. %%
```mermaid
{{Class diagram}}
```

## Behavior and validation

{{Defaults, valid/invalid inputs, absence, ordering and errors}}

## Presentation

{{Visible structure}}

### Colour tokens

| Part | Token |
|---|---|
| {{Part}} | `{{Token}}` |

%% State explicitly if no visible token is owned. %%

### Layout

{{Component-specific application of shared layout rules}}

## Preview

![[docs/assets/captures/{{slug}}.png]]

[Open interactive preview](../../assets/previews/{{slug}}.html)

### Preview source

```csharp
{{Complete composition represented by the preview}}
```

{{What the preview demonstrates}}

%% Conditional: retains/exposes domain data or structured projection. %%
## Structured data

{{Data preservation and projection rules}}

%% Conditional: identity, updates, animation or lifecycle. %%
## Live behavior

{{Live contract}}

%% Conditional: supported specialization or callbacks. %%
## Customization

{{Extension points and constraints}}

%% Optional: distinct additional cases. %%
## Additional examples

```csharp
{{Additional example}}
```

{{Explanation}}
````
