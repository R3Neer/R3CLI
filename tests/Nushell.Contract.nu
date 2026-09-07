use std/assert

const ADAPTER = path self ../dist/nushell/r3cli
const FIXTURE = path self fixtures/console-contract.json
use $ADAPTER *

def render-fixture [ascii: bool] {
    let fixture = (open $FIXTURE)
    let ui = (console --colour never --ascii=$ascii --width $fixture.width --is-terminal=false)
    for command in $fixture.commands {
        match $command.op {
            banner => { banner $ui $command.text }
            heading => { heading $ui $command.text }
            line => { line $ui $command.segments }
            _ => { status $ui $command.op $command.text }
        }
    }
}

def render-auto-colour [] {
    let ui = (console --colour auto --width 80)
    line $ui [
        { text: 'AUTO ', role: heading, bold: true }
        { text: 'ACCENT', role: accent }
    ]
}

def sample-catalogue []: nothing -> record {
    {
        product: TOOL
        version: '1'
        description: Example
        invocation: tool
        group-order: [CONTENT]
        usage: ['tool <command>']
        global-items: [{ label: '--ascii', description: 'ASCII symbols' }]
        commands: [{
            name: check
            group: CONTENT
            summary: Check
            description: 'Check the project'
            usage: ['tool check']
            items: [{ label: '<long-selector>', description: 'Choose content without truncating this description.' }]
            notes: []
            examples: []
        }]
        notes: []
    }
}

def run-assertions [] {
    let themed = (console --colour never --theme-extension { client: '#123456' } --is-terminal=false)
    assert equal $themed.theme.client '#123456' 'Theme extension was not applied'
    assert equal $themed.theme.heading '#50CDDC' 'Canonical theme inheritance changed'
    assert equal (symbol (console --colour never --ascii --is-terminal=false) success) '+' 'ASCII symbol changed'
    assert equal (symbol (console --colour never --is-terminal=false) success) '✓' 'Unicode symbol changed'

    assert error { console --theme-extension { client: blue } }
    assert error { line $themed [{ text: bad, role: absent }] }
    assert error { symbol $themed absent }

    let diagnostic = (format-diagnostic 'Invalid input' --details 'Missing field' --hint repair --code 'Tool.Invalid')
    assert ($diagnostic =~ '^Invalid input\.') 'Diagnostic message punctuation changed'
    assert ($diagnostic =~ 'Details: Missing field\.') 'Diagnostic details changed'
    assert (not ($diagnostic =~ '\x1b')) 'Diagnostic leaked ANSI escapes'

    let catalogue = (sample-catalogue)
    assert (test-help-catalogue $catalogue --executable-commands [check]) 'Valid help catalogue rejected'
    assert error { test-help-catalogue $catalogue --executable-commands [missing] }

    print 'Nushell contract assertions passed.'
}

def render-width [width: int] {
    let ui = (console --colour never --ascii --width $width --is-terminal=false)
    let catalogue = (sample-catalogue)
    help $ui $catalogue check
    line $ui [{ text: 'Keep complete words when wrapping narrow descriptions', role: value }]
    line $ui [{ text: '[literal] café 漢字', role: accent }]
    table $ui [NAME VALUE] [["Long name with spaces" "Very long value that must be preserved"]]
}

def main [
    --mode: string = 'assertions'
    --width: int = 80
] {
    match $mode {
        'fixture-ascii' => { render-fixture true }
        'fixture-unicode' => { render-fixture false }
        'auto-colour' => { render-auto-colour }
        'width' => { render-width $width }
        'assertions' => { run-assertions }
        _ => { error make { msg: $"Unknown contract mode: ($mode)" } }
    }
}
