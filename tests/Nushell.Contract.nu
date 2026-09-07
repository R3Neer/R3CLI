use std/assert

const ADAPTER = path self ../dist/nushell/r3cli
const FIXTURE = path self fixtures/console-contract.json
use $ADAPTER *

def capture [action: closure]: nothing -> string {
    let path = (mktemp)
    do $action o> $path
    let output = (open --raw $path)
    rm --force $path
    $output
}

def display-width [text: string]: nothing -> int {
    ($text | ansi strip | str stats | get 'unicode-width')
}

def render-fixture [fixture: record, ascii: bool]: nothing -> string {
    capture {
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
}

def main [] {
    let fixture = (open $FIXTURE)

    assert equal (render-fixture $fixture true) $fixture.ascii 'ASCII cross-language output contract changed'
    assert equal (render-fixture $fixture false) $fixture.unicode 'Unicode cross-language output contract changed'

    let themed = (console --colour never --theme-extension { client: '#123456' } --is-terminal=false)
    assert equal $themed.theme.client '#123456' 'Theme extension was not applied'
    assert equal $themed.theme.heading '#50CDDC' 'Canonical theme inheritance changed'

    assert error { console --theme-extension { client: blue } }
    assert error { line $themed [{ text: bad, role: absent }] }
    assert error { symbol $themed absent }

    let diagnostic = (format-diagnostic 'Invalid input' --details 'Missing field' --hint repair --code 'Tool.Invalid')
    assert ($diagnostic =~ '^Invalid input\.') 'Diagnostic message punctuation changed'
    assert ($diagnostic =~ 'Details: Missing field\.') 'Diagnostic details changed'
    assert (not ($diagnostic =~ '\x1b')) 'Diagnostic leaked ANSI escapes'

    let catalogue = {
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

    assert (test-help-catalogue $catalogue --executable-commands [check]) 'Valid help catalogue rejected'
    assert error { test-help-catalogue $catalogue --executable-commands [missing] }

    for width in [30 50 80 120] {
        let output = (capture {
            let ui = (console --colour never --ascii --width $width --is-terminal=false)
            help $ui $catalogue check
            line $ui [{ text: 'Keep complete words when wrapping narrow descriptions', role: value }]
            line $ui [{ text: '[literal] café 漢字', role: accent }]
            table $ui [NAME VALUE] [["Long name with spaces" "Very long value that must be preserved"]]
        })
        let lines = ($output | lines)
        assert (not ($lines | any {|item| (display-width $item) > $width })) $"Help exceeded width ($width)"
        assert ($output | str contains 'Choose content without truncating this description.') 'Help lost content'
        assert (not ($output | lines | any {|item| $item =~ 'wrapp$|descri$' })) 'Words were split despite fitting width'
        assert ($output | str contains '[literal] café 漢字') 'Literal text was interpreted as markup'
        assert ($output | str contains 'Very long value that must be preserved') 'Table truncated a value'
    }

    print 'Nushell contract assertions passed.'
}
