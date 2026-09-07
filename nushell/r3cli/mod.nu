# R3CLI visual-language adapter for Nushell 0.115+.
#
# Use as a module:
#   use ./r3cli
#   let ui = r3cli console
#   r3cli banner $ui 'MY TOOL 1.0'

const MODULE_DIR = path self .

# Load the generated package resources when present. Falling back to the
# canonical repository sources keeps the module usable from a source checkout.
def resources [] -> record {
    let packaged = ($MODULE_DIR | path join 'resources.json')
    if ($packaged | path exists) {
        open $packaged
    } else {
        let root = ($MODULE_DIR | path join '../..')
        {
            colours: ((open ($root | path join 'src/r3_cli/default_theme.toml')).colours)
            symbols: (open ($root | path join 'src/r3_cli/symbols.json'))
        }
    }
}

def fail [message: string] {
    error make { msg: $message }
}

def nonempty [value: any] -> bool {
    if $value == null { false } else { (($value | into string | str trim) != '') }
}

def text-width [text: string] -> int {
    let clean = ($text | ansi strip)
    ($clean | str stats | get 'unicode-width')
}

def clean-text [value: any] -> string {
    ($value | into string | str replace --all "\u{1b}" '' | str replace --all "\r\n" "\n" | str replace --all "\t" '    ')
}

def field [value: any, name: string, default_value: any = null] -> any {
    if (($value | describe) !~ '^record') { return $default_value }
    let result = ($value | get --optional ($name | into cell-path))
    if $result == null { $default_value } else { $result }
}

def role-exists [console: record, role: string] -> bool {
    $role in ($console.theme | columns)
}

def use-colour [console: record] -> bool {
    match $console.colour {
        'always' => true
        'never' => false
        _ => {
            let no_color = (($env | get --optional NO_COLOR) != null)
            let attached = if $console.is_terminal == null {
                # Keep this check in an `if`: `is-terminal` deliberately reports
                # false when its own result is redirected into a pipeline/value.
                if (is-terminal --stdout) { true } else { false }
            } else {
                $console.is_terminal
            }
            $attached and (not $no_color)
        }
    }
}

def styled [console: record, text: string, role: any = null, bold: bool = false] -> string {
    let clean = (clean-text $text)
    if not (use-colour $console) { return $clean }

    if ($role != null) and (not (role-exists $console ($role | into string))) {
        fail $"R3CLI.Theme.UnknownRole: '($role)'."
    }

    let prefix = if $role == null {
        if $bold { ansi bo } else { '' }
    } else {
        let colour = ($console.theme | get (($role | into string) | into cell-path))
        if $bold { ansi { fg: $colour, attr: b } } else { ansi $colour }
    }

    if $prefix == '' { $clean } else { $"($prefix)($clean)(ansi reset)" }
}

def segment-text [segment: any] -> string {
    if (($segment | describe) == 'string') {
        clean-text $segment
    } else {
        clean-text (field $segment 'text' '')
    }
}

def wrap-plain [text: string, width: int] -> list<string> {
    let normalized = (clean-text $text)
    if (text-width $normalized) <= $width { return [$normalized] }

    mut output = []
    for paragraph in ($normalized | split row "\n") {
        if $paragraph == '' {
            $output = ($output | append '')
            continue
        }

        let indent_match = ($paragraph | parse --regex '^(?<indent>\s*)' | first)
        let indent = ($indent_match | get --optional indent | default '')
        let body = ($paragraph | str trim --left)
        let words = ($body | split words)
        mut current = $indent

        for word in $words {
            let candidate = if ($current | str trim) == '' { $"($current)($word)" } else { $"($current) ($word)" }
            if (text-width $candidate) <= $width {
                $current = $candidate
            } else {
                if ($current | str trim) != '' { $output = ($output | append $current) }
                $current = $"($indent)($word)"
            }
        }
        if ($current | str trim) != '' { $output = ($output | append $current) }
    }
    $output
}

# Construct a rendering context. `colour` follows R3CLI's auto/always/never
# contract. `is-terminal` exists mainly for deterministic tests and embedding.
export def console [
    --colour: string = 'auto'
    --ascii
    --width: int
    --theme-extension: record = {}
    --is-terminal: any = null
] -> record {
    if $colour not-in ['auto' 'always' 'never'] {
        fail $"R3CLI.Colour.Invalid: '($colour)'."
    }

    for item in ($theme_extension | transpose key value) {
        if (($item.value | describe) != 'string') or ($item.value !~ '^#[0-9A-Fa-f]{6}$') {
            fail $"R3CLI.Theme.InvalidColours: '($item.key)' must use #RRGGBB."
        }
    }

    let loaded = (resources)
    let actual_width = if $width == null {
        let columns = ((term size).columns | default 80)
        if $columns > 0 { $columns } else { 80 }
    } else {
        $width
    }
    if ($actual_width < 1) or ($actual_width > 10000) {
        fail 'R3CLI.Console.InvalidWidth: width must be between 1 and 10000.'
    }

    {
        theme: ($loaded.colours | merge $theme_extension)
        symbols: $loaded.symbols
        ascii: $ascii
        width: $actual_width
        colour: $colour
        is_terminal: $is_terminal
    }
}

export def symbol [console: record, kind: string] -> string {
    if $kind not-in ($console.symbols | columns) {
        fail $"R3CLI.Symbol.Unknown: '($kind)'."
    }
    let values = ($console.symbols | get ($kind | into cell-path))
    if $console.ascii { $values.1 } else { $values.0 }
}

# Print human text without returning it into Nushell's structured pipeline.
export def line [
    console: record
    segments: list<any> = []
    --no-newline
    --stderr
] -> nothing {
    for segment in $segments {
        if (($segment | describe) =~ '^record') {
            let role = (field $segment 'role')
            if ($role != null) and (not (role-exists $console ($role | into string))) {
                fail $"R3CLI.Theme.UnknownRole: '($role)'."
            }
        }
    }

    let plain = ($segments | each {|segment| segment-text $segment } | str join '')
    let wrapped = (wrap-plain $plain $console.width)

    # Preserve per-segment colour on ordinary unwrapped lines. When a line must
    # wrap, use the first segment's role rather than splitting styled tokens;
    # the textual contract remains exact and no content is truncated.
    let rendered = if ($wrapped | length) == 1 and ($plain !~ "\n") {
        $segments | each {|segment|
            if (($segment | describe) == 'string') {
                styled $console ($segment | into string)
            } else {
                styled $console (field $segment 'text' '') (field $segment 'role') (field $segment 'bold' false)
            }
        } | str join '' | wrap
    } else {
        let first_record = ($segments | where {|it| ($it | describe) =~ '^record'} | first | default {})
        let role = (field $first_record 'role')
        let bold = (field $first_record 'bold' false)
        $wrapped | each {|item| styled $console $item $role $bold }
    }

    for item in $rendered {
        if $stderr {
            print --stderr --no-newline=$no_newline $item
        } else {
            print --no-newline=$no_newline $item
        }
    }
}

export def banner [console: record, text: string] -> nothing {
    let rule_width = ([68 $console.width] | math min)
    let rule = ('' | fill --width $rule_width --character (symbol $console banner))
    line $console
    line $console [{ text: $rule, role: secondary }]
    line $console [{ text: $" ($text)", role: heading, bold: true }]
    line $console [{ text: $rule, role: secondary }]
}

export def heading [console: record, text: string] -> nothing {
    line $console
    line $console [{ text: ($text | str upcase), role: heading, bold: true }]
}

export def section [console: record, title: string, count: any = null] -> nothing {
    line $console
    mut segments = [{ text: $"  ($title)", role: heading }]
    if $count != null { $segments = ($segments | append { text: $"  ($count)", role: accent }) }
    line $console $segments
    let rule_width = ([64 ($console.width - 2)] | math min | into int)
    let safe_width = if $rule_width < 0 { 0 } else { $rule_width }
    let rule = ('' | fill --width $safe_width --character (symbol $console rule))
    line $console [{ text: $"  ($rule)", role: secondary }]
}

export def status [console: record, kind: string, text: string] -> nothing {
    let role = (match $kind {
        step => process
        success => success
        info => heading
        warning => process
        error => error
        _ => { fail $"R3CLI.Status.Unknown: '($kind)'." }
    })
    let segments = [
        { text: (symbol $console $kind), role: $role }
        { text: $" ($text)", role: value }
    ]
    if $kind == 'warning' { line $console $segments --stderr } else { line $console $segments }
}

export def key-value [console: record, key: string, value: any, --width: int = 16] -> nothing {
    if ($console.width < 40) or (($width + 4) >= $console.width) {
        line $console [{ text: $key, role: secondary }]
        line $console [{ text: $"  ($value)", role: value }]
    } else {
        let padded = ($key | fill --width $width --alignment left)
        line $console [{ text: $"($padded) ", role: secondary } { text: ($value | into string), role: value }]
    }
}

export def table [console: record, headers: list<string>, rows: list<any>] -> nothing {
    let count = ($headers | length)
    for row in $rows {
        if (($row | length) != $count) { fail 'R3CLI.Table.InvalidRow: column count differs.' }
    }
    if $count == 0 { return }

    let raw_width = (($console.width - (2 * ($count - 1))) / $count)
    let width = ([1 ($raw_width | math floor | into int)] | math max)

    if $width < 12 {
        for row in $rows {
            for index in 0..<($count) { key-value $console $headers.($index) $row.($index) }
            line $console
        }
        return
    }

    let header_line = ($headers | each {|item| $item | fill --width $width --alignment left } | str join '  ')
    line $console [{ text: $header_line, role: heading }]

    for row in $rows {
        let has_long = ($row | any {|item| (text-width ($item | into string)) > $width })
        if $has_long {
            for index in 0..<($count) { key-value $console $headers.($index) $row.($index) }
        } else {
            let row_line = ($row | each {|item| ($item | into string) | fill --width $width --alignment left } | str join '  ')
            line $console [{ text: $row_line, role: value }]
        }
    }
}

def normalize-catalogue [catalogue: record] -> record {
    let nested = ($catalogue | get --optional help)
    if $nested == null {
        $catalogue
    } else {
        $nested | merge { commands: ($catalogue | get --optional commands | default []) }
    }
}

def catalogue-groups [catalogue: record] -> list<any> {
    let explicit = ($catalogue | get --optional 'group-order')
    if $explicit == null { $catalogue | get --optional groups | default [] } else { $explicit }
}

export def test-help-catalogue [catalogue: record, --executable-commands: list<string>] -> bool {
    let catalogue = (normalize-catalogue $catalogue)
    for name in [product description invocation] {
        if not (nonempty ($catalogue | get --optional ($name | into cell-path))) {
            fail $"R3CLI.Help.Invalid: ($name) is empty."
        }
    }

    let help_options = ($catalogue | get --optional 'help-options' | default ['-h' '--help'])
    if ('--help' not-in $help_options) or ($help_options | any {|it| not (nonempty $it) }) or (($help_options | uniq | length) != ($help_options | length)) {
        fail 'R3CLI.Help.Invalid: help options must be unique, nonempty and include --help.'
    }

    let groups = (catalogue-groups $catalogue)
    if (($groups | uniq | length) != ($groups | length)) { fail 'R3CLI.Help.Invalid: duplicate groups.' }

    let commands = ($catalogue | get --optional commands | default [])
    mut names = []
    for command in $commands {
        let name = ($command | get --optional name | default '' | into string)
        if (not (nonempty $name)) or ($name == 'help') or ($name in $names) {
            fail $"R3CLI.Help.Invalid: duplicate or invalid command '($name)'."
        }
        $names = ($names | append $name)
        let group = ($command | get --optional group)
        if $group not-in $groups { fail $"R3CLI.Help.Invalid: unknown group for '($name)'." }
        for required in [summary description usage] {
            let values = ($command | get --optional ($required | into cell-path) | default [])
            let values = if (($values | describe) =~ '^list') { $values } else { [$values] }
            if (($values | length) == 0) or ($values | any {|it| not (nonempty $it) }) {
                fail $"R3CLI.Help.Invalid: missing ($required) for '($name)'."
            }
        }
        for item in ($command | get --optional items | default []) {
            if (not (nonempty ($item | get --optional label))) or (not (nonempty ($item | get --optional description))) {
                fail $"R3CLI.Help.Invalid: incomplete item for '($name)'."
            }
        }
    }

    for item in ($catalogue | get --optional 'global-items' | default []) {
        if (not (nonempty ($item | get --optional label))) or (not (nonempty ($item | get --optional description))) {
            fail 'R3CLI.Help.Invalid: incomplete global item.'
        }
    }

    if $executable_commands != null {
        let missing = ($names | where {|it| $it not-in $executable_commands })
        let extra = ($executable_commands | where {|it| $it not-in $names })
        if (($missing | length) > 0) or (($extra | length) > 0) {
            fail 'R3CLI.Help.DispatchMismatch: catalogue differs from executable commands.'
        }
    }
    true
}

def help-row [console: record, label: string, description: string, width: int] -> nothing {
    if ($console.width < 40) or (($width + 4) >= $console.width) {
        line $console [{ text: $"  ($label)", role: accent }]
        line $console [{ text: $"    ($description)", role: secondary }]
    } else {
        let padded = ($label | fill --width $width --alignment left)
        line $console [{ text: $"  ($padded)", role: accent } { text: $description, role: secondary }]
    }
}

export def help [console: record, catalogue: record, command: string = ''] -> nothing {
    let catalogue = (normalize-catalogue $catalogue)
    test-help-catalogue $catalogue | ignore
    let commands = ($catalogue | get --optional commands | default [])

    let entry = if $command != '' {
        let matches = ($commands | where name == $command)
        if (($matches | length) != 1) { fail $"R3CLI.Help.UnknownCommand: '($command)'." }
        banner $console ($command | str upcase)
        $matches | first
    } else {
        let version = ($catalogue | get --optional version | default '')
        banner $console ($"($catalogue.product) ($version)" | str trim)
        $catalogue
    }

    line $console [{ text: ($entry | get description), role: value }]
    heading $console USAGE
    for usage in ($entry | get usage) { line $console [{ text: $"  ($usage)", role: accent }] }

    let items = if $command != '' {
        $entry | get --optional items | default []
    } else {
        $entry | get --optional 'global-items' | default []
    }
    if ($items | length) > 0 {
        heading $console (if $command != '' { 'ARGUMENTS AND OPTIONS' } else { 'GLOBAL OPTIONS' })
        let max_label = ($items | get label | each {|it| text-width ($it | into string) } | math max)
        let width = ([28 ($max_label + 2)] | math min)
        for item in $items { help-row $console $item.label $item.description $width }
    }

    if $command == '' {
        let names = ($commands | get name)
        let width = if (($names | length) == 0) { 2 } else {
            [24 (($names | each {|it| text-width $it } | math max) + 2)] | math min
        }
        for group in (catalogue-groups $catalogue) {
            let members = ($commands | where group == $group)
            if ($members | length) == 0 { continue }
            heading $console $group
            for member in $members { help-row $console $member.name $member.summary $width }
        }
    }

    let notes = ($entry | get --optional notes | default [])
    if ($notes | length) > 0 {
        if $command != '' { heading $console NOTES } else { line $console }
        for note in $notes { status $console info $note }
    }

    let examples = ($entry | get --optional examples | default [])
    if ($examples | length) > 0 {
        heading $console EXAMPLES
        for example in $examples { line $console [{ text: $"  ($example)", role: accent }] }
    }
    line $console
}

export def format-diagnostic [
    message: string
    --details: string = ''
    --hint: string = ''
    --code: string = ''
] -> string {
    def sentence [value: string] -> string {
        let text = ($value | ansi strip | str trim)
        if $text =~ '[.!?]$' { $text } else { $"($text)." }
    }

    mut lines = [(sentence $message)]
    if $code != '' { $lines = ($lines | append $"  [(($code | ansi strip | str trim))]") }
    if $details != '' { $lines = ($lines | append $"Details: (sentence $details)") }
    if $hint != '' { $lines = ($lines | append $"Try: (($hint | ansi strip | str trim))") }
    $lines | str join (char newline)
}
