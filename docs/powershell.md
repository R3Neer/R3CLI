# PowerShell adapter

Build the distribution from a clean R3CLI revision:

```console
python scripts/build_powershell.py
```

This development step requires Python 3.11+. The resulting
`dist/powershell/R3CLI` directory contains the PowerShell module, generated
resources, MIT licence and deterministic SHA256 file manifest. It is usable
without Python, Rich, a registry or network access. Consumers should pin the
source commit as well as the package hashes; the adapter API version is `1`.
The module version follows the Python package; source revision distinguishes
unreleased changes from an existing release of the same version.

```powershell
Import-Module ./dist/powershell/R3CLI/R3CLI.psd1
$ui = New-R3Console -Colour auto -ThemeExtension @{ client = '#748FFC' }
Write-R3Banner $ui 'MY TOOL'
Write-R3Status $ui step 'Reading the project'
Write-R3Line $ui @(@{Text='[C] ';Role='client'}, @{Text='Example';Role='value';Bold=$true})
Write-R3Status $ui success 'Ready.'
```

## Context and primitives

Create one context per invocation. `New-R3Console` accepts `Colour`
(`auto`, `always`, `never`), `Ascii`, `Width`, `ThemeExtension`, `Invocation`,
`IsTerminal` and an optional `Sink` scriptblock. `Invocation` may be the caller's
`$MyInvocation`; it suppresses automatic colour for pipelines/redirections.
Without an explicit width, the host width is used, falling back to 80 columns.
Explicit colour modes override environment detection; `NO_COLOR` disables auto.
No preferences or environment variables are changed by the adapter.

`Write-R3Banner`, `Write-R3Heading`, `Write-R3Section`, `Write-R3Status`,
`Write-R3KeyValue` and `Write-R3Table` provide the standard components.
`Write-R3Line` accepts literal strings or segments with `Text`, `Role`, `Bold`.
It validates roles, wraps at word boundaries and splits oversized tokens at grapheme boundaries without losing content.
`-NoNewline` buffers segments until the next completed line, preserving styled
composition while allowing width-aware wrapping. It does not write partial
terminal output. Use `Get-R3Symbol` for shared symbols including status and
inactive badges. `-Ascii` changes those symbols, not user-supplied text.

Human presentation goes to PowerShell's information stream (6), warnings to
stream 3. No objects are written to the success pipeline. `Write-R3Status error`
is visual reporting, not an exception. Applications own termination and error
records. The optional sink receives `(text, stream)` for tests or alternate hosts;
its output is discarded. Standard PowerShell stream capture remains available. `always` produces ANSI in
the information records; the PowerShell host and downstream formatters may still
strip it according to their own `OutputRendering` preference (for example with
`Out-String` or an OS-level pipe). The adapter does not change that session-wide
preference. Capture `InformationRecord.MessageData` to inspect original rendering.

`Format-R3Diagnostic` returns plain text and does not emit it. It accepts
`Message`, optional `Code`, `Details` and `Hint`, so consumers can attach the
result to one native `ErrorRecord` without double-printing. Applications retain
their error identity, category and target. PowerShell owns the host's surrounding
error decoration; R3CLI does not change `ErrorView` or error preferences.

## Help and themes

`Write-R3Help $ui $catalogue [command]` takes a normalised catalogue with
`Product`, `Version`, `Description`, `Invocation`, `Groups`, `Commands`, `Usage`,
`GlobalItems` and `Notes`. Each command has the same fields as Python's
`CommandHelp` (case-insensitive PowerShell property names). Optional collections
may be omitted. `Test-R3HelpCatalogue -ExecutableCommands` detects dispatch drift,
duplicate commands/groups, unknown groups and incomplete documentation. Command
routing and option parsing remain the consumer's responsibility.

The build derives `resources.json` from `default_theme.toml` and `symbols.json` in
the Python package. Generated resources must not be edited. `ThemeExtension`
inherits canonical roles and accepts explicit extra roles or overrides. Python
consumers use `compose_theme(mapping)` for the same behaviour; `load_theme(path)`
continues to load complete themes unchanged.

## Validation

`pytest` validates Python and, when pwsh is available, builds the PowerShell
package twice and exercises it in a fresh process. The dedicated Windows CI job
always executes `tests/PowerShell.Contract.ps1`. Both implementations use the
same JSON fixture for exact plain presentation at a fixed width. Native streams,
ANSI modes, narrow layouts and domain extensions have separate contract checks.
