---
type: template
---

# Question Template

Instances use `type: question`. One file represents one actionable uncertainty. Required: question, context, alternatives, resolution criterion and affected documents. Recommendation is optional. The filename identifies the question; do not add ID/status/date/priority metadata. Keep only active questions; integrate accepted answers into reference documents and remove the resolved question.

## Document skeleton

```markdown
---
type: question
---

# {{Question title}}

## Question

{{One concrete decision to make}}

## Context

{{Accepted constraints and why the decision matters}}

## Alternatives

{{Credible choices and tradeoffs}}

%% Optional: a preference, not accepted behavior. %%
## Recommendation

{{Preferred alternative and reasoning}}

## Resolution criterion

{{Evidence/choice needed to close the question}}

## Affected documents

{{Links to the canonical reference pages to update}}
```
