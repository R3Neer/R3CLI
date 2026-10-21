---
type: concept
---

# Capabilities and stable output

A TextWriter defines where characters go. Destination evidence and output preferences determine whether those characters include colour, Unicode decoration or cursor operations.

## Responsibilities

Spectre.Console supplies technical detection. R3CLI combines that evidence with [[docs/configuration/toml|configuration]], structured-output separation and ownership of an editable region. Resolve the session profile at scope creation; update available dimensions as the terminal changes. Theme selection remains session-cached under [[docs/configuration/built-in-themes|Built-in themes]].

## Rules

### Detection and preferences

Detect the selected output channel, not merely whether the process has some terminal. stdout and stderr can be redirected independently. Use Spectre's ANSI, colour-system, interactivity and Unicode evidence, including its environment/CI detection. These are estimates, not proof of font coverage or exclusive cursor ownership. In the reviewed Spectre 0.57.2 implementation, Unicode is inferred from encoding; ANSI and interactivity are distinct properties.

Known standard channels use redirection evidence. Files, strings and unidentified custom writers use stable behavior unless a host integration supplies reliable terminal evidence. A wrapper may hide the original destination. Do not guess terminal capabilities from a writer class name or from the user's shell name. The concrete advanced-host reporting API is not introduced here.

| Preference | Policy |
|---|---|
| colour = auto | Respect automatic capability and environment detection, including NO_COLOR |
| colour = always | Explicitly request colour sequences, including deliberate captures; never imply motion |
| colour = never | Emit no coloured styles, fills or background queries |
| characters = auto | Use the detected character repertoire |
| characters = unicode / ascii | Apply the explicit repertoire choice |
| motion = auto | Animate only with adequate terminal capability and coordinated region ownership; CI is stable by default |
| motion = always | Request motion where editing is possible; a file/string remains stable |
| motion = never | Preserve useful state through stable presentation without frame events |

An explicit R3CLI colour preference overrides the automatic environment choice; automatic mode leaves that choice to detection. Structured values receive no decoration regardless of these settings. Keep colour, characters and motion independent: a colourless terminal can still support cursor editing, and a CI log can support colour without live rewriting. Do not start an OSC background query without safe coordinated input ownership and a bounded wait. Ordinary output does not require input access.

### Stable output

Append meaningful state snapshots to the supplied writer without cursor rewriting or temporal frame events. Close freezes logical state; Remove deactivates the logical region without deleting already written lines. Do not surround each event with decorative blank lines or flood logs with spinner frames. Meaningful updates remain distinguishable from time-driven animation; scheduling and throttling internals do not change task data.

Unknown width uses the shared reference of 80 cells; a known zero width emits no presentation. Reuse [[docs/presentation/text-and-layout|layout]] and [[docs/configuration/built-in-themes|theme fallback]] rules rather than inventing per-writer component semantics. Native structured results bypass human rendering entirely.

## Example

```csharp
using var capture = new StringWriter();
using (Output.Use(capture))
{
    var handle = new ActivityDisplay("Resolving dependencies").Show();
    handle.Update(new ActivityDisplay(
        "Resolving dependencies", state: TaskState.Succeeded));
    handle.Close();
}
string log = capture.ToString();
```

The capture contains stable human state rather than a sequence of spinner frames. Console.Error can be interactive in the same process while Console.Out is redirected to a file. Each output session evaluates its own destination; sharing a physical terminal still requires coordination.

## Sources

- [Spectre capability reference](https://spectreconsole.net/console/reference/capabilities-reference/).
- [Spectre 0.57.2 output destination detection](https://github.com/spectreconsole/spectre.console/blob/0.57.2/src/Spectre.Console/AnsiConsoleOutput.cs).
- [Spectre 0.57.2 capability construction](https://github.com/spectreconsole/spectre.console/blob/0.57.2/src/Spectre.Console/Capabilities.cs).
