---
type: question
---

# Built-in Colour Values

## Question

What exact built-in RGB values should supply the eight standard tokens?

## Context

Token names and ownership are fixed. The previews use a coherent illustrative palette, including a distinct Title colour and soft LiteralBlock background. Those RGB choices have not been selected as final built-in defaults. There is no named-theme system.

## Alternatives

- Adopt the illustrated values after checking contrast and common terminals.
- Adjust individual defaults after visual comparison, keeping the same eight tokens and TOML surface.

## Recommendation

Use the current preview values as the starting specimen and compare dark/light terminal backgrounds before fixing defaults. Do not add token names to compensate for a poorly chosen palette.

## Resolution criterion

Approve exact values and verify representative text, symbols, separators, progress and literal content in colour and no-colour presentations.

## Affected documents

- [[docs/configuration/colour-tokens]]
- [[docs/configuration/toml]]
- [[docs/structure]]
