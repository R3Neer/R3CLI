---
type: index
---

# Output

Output is the public boundary between Presentation Components and a destination supplied as a .NET TextWriter. Construction does not print. Output owns placement and delegates rendering to an internal session using Spectre.Console.

## Contents

- [[docs/presentation/output/sessions-and-handles|Sessions and handles]] owns the facade contract, default-context selection, scope disposal and ViewHandle lifetime.
- [[docs/presentation/output/capabilities|Capabilities and stable output]] owns destination detection, preferences and noninteractive behavior.
- [[docs/presentation/architecture/spectre-console|Spectre.Console integration]] owns the rendering dependency and the boundary of delegation.

## Reading guide

Start with Sessions and handles before using Show or live regions. Read Capabilities before routing human output to stdout, stderr, a file or a custom writer. Component examples assume an enclosing host-established scope unless they create one explicitly. The command executor or adapter establishes that scope for normal application usage; the presentation API also works without the Command System.

Use Console.Out and Console.Error for the two standard channels, StreamWriter for a file, and StringWriter for a captured string. These are .NET destinations, not R3CLI destination subclasses. The caller retains ownership of the writer. See [[docs/presentation/architecture/README|Presentation architecture]] for the internal design order.
