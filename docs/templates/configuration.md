---
type: template
---

# Configuration Template

Instances use `type: configuration`. Required: purpose, settings/reference, resolution rules, validation and example. Explicitly distinguish chosen defaults from illustrative colour values. Include accepted values/types and omitted-value behavior. No speculative settings, named-theme architecture or hidden registration requirements.

## Document skeleton

````markdown
---
type: configuration
---

# {{Configuration area}}

{{Purpose}}

## Reference

{{Settings/tokens, accepted values and defaults}}

## Resolution rules

{{Lookup, omission, precedence and scope}}

## Validation

{{Invalid inputs and observable errors}}

## Example

```toml
{{Current schema example}}
```

{{Explanation}}
````
