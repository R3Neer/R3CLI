# R3CLI Nushell adapter.
#
# Import with:
#   use /path/to/R3CLI *
#
# The adapter keeps human rendering separate from structured pipeline data.

const R3_RESOURCES = path self resources.json


def r3-resources [] {
    open $R3_RESOURCES
}


def r3-field [value: any, name: string, fallback: any = null] {
    $value | get -o $name | default $fallback
}


def r3-nonempty [value: any] {
    let text = ($value | default '' | into string | str trim)
    not ($text | is-empty)
}


def r3-min [a: int, b: int] {
    if $a < $b { $a } else { $b }
}


def r3-max [a: int, b: int] {
    if $a > $b { $a } else { $b }
}


def r3-repeat [text: string, count: int] {
    let n = (r3-max 0 $count)
    if $n == 0 { '' } else { 1..$n | each { $text } | str join }
}


def r3-pad-right [value: any, width: int] {
    $value | into string | fill --alignment left --width $width
}


def r3-visible-length [text: string] {
    $text | ansi strip | str length --grapheme-clusters
}


def r3-role-style [console: record, role: any, bold: bool] {
    if $role != null and $role not-in ($console.theme | columns) {
        error make $"R3CLI.Theme.UnknownRole: '($role)'."
    }

    if not $console.use_colour {
        return {prefix: '', suffix: ''}
    }

    let colour = if $role == null { '' } else { ansi ($console.theme | get $role) }
    let weight = if $bold { ansi bold } else { '' }
    {prefix: $"($weight)($colour)", suffix: (ansi reset)}
}


def r3-render-segment [console: record, segment: any] {
    if ($segment | describe) == 'string' {
        return $segment
    }

    let text = (r3-field $segment text '' | into string)
    let role = (r3-field $segment role null)
    let bold = (r3-field $segment bold false)
    let style = (r3-role-style $console $role $bold)
    $"($style.prefix)($text)($style.suffix)"
}


def r3-render-line [console: record, segments: list<any>] {
    $segments | each {|segment| r3-render-segment $console $segment } | str join
}


def r3-print-line [console: record, segments: list<any>, stream: string = 'stdout'] {
    let text = (r3-render-line $console $segments)
    if $stream == 'stderr' { print --stderr $text } else { print $text }
}


def r3-help-row [console: record, label: string, description: string, width: int] {
    if $console.width < 40 or ($width + 4) >= $console.width {
        r3-print-line $console [{text: $"  ($label)", role: accent}]
        r3-print-line $console [{text: $"    ($description)", role: secondary}]
    } else {
        let left = ('  ' + (r3-pad-right $label $width))
        r3-print-line $console [
            {text: $left, role: accent}
            {text: $description, role: secondary}
        ]
    }
}


def r3-catalogue-groups [catalogue: record] {
    let explicit = (r3-field $catalogue groups null)
    if $explicit != null { return $explicit }
    r3-field $catalogue group-order []
}


def r3-catalogue-help-options [catalogue: record] {
    r3-field $catalogue help-options ['-h' '--help']
}


def r3-catalogue-command [catalogue: record, name: string] {
    let matches = ($catalogue.commands | where {|item| $item.name == $name })
    if ($matches | length) != 1 {
        error make $"R3CLI.Help.UnknownCommand: '($name)'."
    }
    $matches | first
}


export def "r3 console new" [
    --colour: string = 'auto'
    --ascii
    --width: int
    --theme: record = {}
] {
    if $colour not-in ['auto' 'always' 'never'] {
        error make $"R3CLI.Colour.Invalid: '($colour)' must be auto, always or never."
    }

    for entry in ($theme | transpose role colour) {
        if not ($entry.colour =~ '^#[0-9A-Fa-f]{6}$') {
            error make $"R3CLI.Theme.InvalidColours: '($entry.role)' must use #RRGGBB."
        }
    }

    let resources = (r3-resources)
    let terminal_width = if $width == null {
        try { (term size).columns } catch { 80 }
    } else {
        $width
    }
    let no_colour = (($env | get -o NO_COLOR) != null)
    let use_colour = match $colour {
        'always' => true
        'never' => false
        _ => { (is-terminal --stdout) and not $no_colour }
    }

    {
        theme: ($resources.colours | merge $theme)
        symbols: $resources.symbols
        ascii: $ascii
        width: (r3-max 1 $terminal_width)
        use_colour: $use_colour
    }
}


export def "r3 symbol" [console: record, kind: string] {
    if $kind not-in ($console.symbols | columns) {
        error make $"R3CLI.Symbol.Unknown: '($kind)'."
    }
    let index = if $console.ascii { 1 } else { 0 }
    $console.symbols | get $kind | get $index
}


export def "r3 line" [
    console: record
    segments: list<any> = []
    --stderr
] {
    r3-print-line $console $segments (if $stderr { 'stderr' } else { 'stdout' })
}


export def "r3 banner" [console: record, text: string] {
    let rule_width = (r3-min 68 $console.width)
    let rule = (r3-repeat (r3 symbol $console banner) $rule_width)
    print ''
    r3-print-line $console [{text: $rule, role: secondary}]
    r3-print-line $console [{text: $" ($text)", role: heading, bold: true}]
    r3-print-line $console [{text: $rule, role: secondary}]
}


export def "r3 heading" [console: record, text: string] {
    print ''
    r3-print-line $console [{text: ($text | str upcase), role: heading, bold: true}]
}


export def "r3 section" [console: record, title: string, count?: int] {
    print ''
    mut segments = [{text: $"  ($title)", role: heading}]
    if $count != null {
        $segments = ($segments | append {text: $"  ($count)", role: accent})
    }
    r3-print-line $console $segments
    let rule_width = (r3-max 0 (r3-min 64 ($console.width - 2)))
    r3-print-line $console [{text: ('  ' + (r3-repeat (r3 symbol $console rule) $rule_width)), role: secondary}]
}


export def "r3 status" [
    console: record
    kind: string
    text: string
] {
    if $kind not-in ['step' 'success' 'info' 'warning' 'error'] {
        error make $"R3CLI.Status.Invalid: '($kind)'."
    }
    let role = ({step: process, success: success, info: heading, warning: process, error: error} | get $kind)
    let stream = if $kind in ['step' 'warning' 'error'] { 'stderr' } else { 'stdout' }
    r3-print-line $console [
        {text: (r3 symbol $console $kind), role: $role}
        {text: $" ($text)", role: value}
    ] $stream
}


export def "r3 key-value" [
    console: record
    key: string
    value: any
    --width: int = 16
] {
    if $console.width < 40 or ($width + 4) >= $console.width {
        r3-print-line $console [{text: $key, role: secondary}]
        r3-print-line $console [{text: $"  ($value)", role: value}]
    } else {
        r3-print-line $console [
            {text: ((r3-pad-right $key $width) + ' '), role: secondary}
            {text: ($value | into string), role: value}
        ]
    }
}


export def "r3 table" [console: record, headers: list<string>, rows: list<any>] {
    let count = ($headers | length)
    if $count == 0 { return }

    for row in $rows {
        if ($row | length) != $count {
            error make 'R3CLI.Table.InvalidRow: column count differs.'
        }
    }

    let available = ($console.width - (2 * ($count - 1)))
    let column_width = (r3-max 1 (($available / $count) | math floor | into int))

    if $column_width < 12 {
        for row in $rows {
            for entry in ($headers | enumerate) {
                r3 key-value $console $entry.item ($row | get $entry.index)
            }
            print ''
        }
        return
    }

    let rendered_headers = ($headers | each {|header| r3-pad-right $header $column_width } | str join '  ')
    r3-print-line $console [{text: $rendered_headers, role: heading}]

    for row in $rows {
        let long = ($row | any {|value| (($value | into string | str length --grapheme-clusters) > $column_width) })
        if $long {
            for entry in ($headers | enumerate) {
                r3 key-value $console $entry.item ($row | get $entry.index)
            }
        } else {
            let rendered = ($row | each {|value| r3-pad-right $value $column_width } | str join '  ')
            r3-print-line $console [{text: $rendered, role: value}]
        }
    }
}


export def "r3 diagnostic format" [
    message: string
    --details: string
    --hint: string
    --code: string
] {
    let clean_message = ($message | ansi strip | str trim)
    let first = if $clean_message =~ '[.!?]$' { $clean_message } else { $clean_message + '.' }
    mut lines = [$first]

    if $code != null and (r3-nonempty $code) {
        $lines = ($lines | append $"  [(($code | ansi strip | str trim))]")
    }
    if $details != null and (r3-nonempty $details) {
        let detail = ($details | ansi strip | str trim)
        let punctuated = if $detail =~ '[.!?]$' { $detail } else { $detail + '.' }
        $lines = ($lines | append $"Details: ($punctuated)")
    }
    if $hint != null and (r3-nonempty $hint) {
        $lines = ($lines | append $"Try: (($hint | ansi strip | str trim))")
    }
    $lines | str join (char nl)
}


export def "r3 help load" [path: path] {
    let raw = (open $path)
    if ('help' not-in ($raw | columns)) {
        error make 'R3CLI.Help.Invalid: TOML catalogue has no [help] table.'
    }

    let help = $raw.help
    {
        product: (r3-field $help product '')
        version: (r3-field $help version '')
        description: (r3-field $help description '')
        invocation: (r3-field $help invocation '')
        group-order: (r3-field $help group-order [])
        usage: (r3-field $help usage [])
        notes: (r3-field $help notes [])
        help-options: (r3-field $help help-options ['-h' '--help'])
        global-items: (r3-field $help global-items [])
        commands: (r3-field $raw commands [])
    }
}


export def "r3 help validate" [
    catalogue: record
    --commands: list<string>
] {
    for field in ['product' 'description' 'invocation'] {
        if not (r3-nonempty (r3-field $catalogue $field '')) {
            error make $"R3CLI.Help.Invalid: ($field) is empty."
        }
    }

    let help_options = (r3-catalogue-help-options $catalogue)
    if '--help' not-in $help_options or ($help_options | any {|item| not (r3-nonempty $item) }) or (($help_options | uniq | length) != ($help_options | length)) {
        error make 'R3CLI.Help.Invalid: help options must be unique, nonempty and include --help.'
    }

    let groups = (r3-catalogue-groups $catalogue)
    if ($groups | uniq | length) != ($groups | length) {
        error make 'R3CLI.Help.Invalid: duplicate groups.'
    }

    mut names = []
    for command in (r3-field $catalogue commands []) {
        let name = (r3-field $command name '' | into string)
        if not (r3-nonempty $name) or $name == 'help' or $name in $names {
            error make $"R3CLI.Help.Invalid: duplicate or invalid command '($name)'."
        }
        $names = ($names | append $name)
        if (r3-field $command group '') not-in $groups {
            error make $"R3CLI.Help.Invalid: unknown group for '($name)'."
        }
        for field in ['summary' 'description' 'usage'] {
            let values = (r3-field $command $field [])
            if ($values | length) == 0 or ($values | any {|item| not (r3-nonempty $item) }) {
                error make $"R3CLI.Help.Invalid: missing ($field) for '($name)'."
            }
        }
        for item in (r3-field $command items []) {
            if not (r3-nonempty (r3-field $item label '')) or not (r3-nonempty (r3-field $item description '')) {
                error make $"R3CLI.Help.Invalid: incomplete item for '($name)'."
            }
        }
    }

    for item in (r3-field $catalogue global-items []) {
        if not (r3-nonempty (r3-field $item label '')) or not (r3-nonempty (r3-field $item description '')) {
            error make 'R3CLI.Help.Invalid: incomplete global item.'
        }
    }

    if $commands != null {
        if (($names | where {|name| $name not-in $commands } | length) > 0) or (($commands | where {|name| $name not-in $names } | length) > 0) {
            error make 'R3CLI.Help.DispatchMismatch: catalogue differs from executable commands.'
        }
    }
    true
}


export def "r3 help" [console: record, catalogue: record, command?: string] {
    r3 help validate $catalogue | ignore
    let commands = (r3-field $catalogue commands [])
    let groups = (r3-catalogue-groups $catalogue)

    let entry = if $command == null { $catalogue } else { r3-catalogue-command $catalogue $command }
    let title = if $command == null {
        $"((r3-field $catalogue product '')) ((r3-field $catalogue version ''))" | str trim
    } else {
        $command | str upcase
    }

    r3 banner $console $title
    r3-print-line $console [{text: (r3-field $entry description ''), role: value}]
    r3 heading $console USAGE
    for usage in (r3-field $entry usage []) {
        r3-print-line $console [{text: $"  ($usage)", role: accent}]
    }

    let items = if $command == null { r3-field $entry global-items [] } else { r3-field $entry items [] }
    if ($items | length) > 0 {
        r3 heading $console (if $command == null { 'GLOBAL OPTIONS' } else { 'ARGUMENTS AND OPTIONS' })
        let widest = ($items | each {|item| (r3-field $item label '' | str length --grapheme-clusters) } | math max)
        let width = (r3-min 28 ($widest + 2))
        for item in $items {
            r3-help-row $console (r3-field $item label '') (r3-field $item description '') $width
        }
    }

    if $command == null {
        let widest = if ($commands | length) == 0 { 0 } else { $commands | each {|item| ($item.name | str length --grapheme-clusters) } | math max }
        let width = (r3-min 24 ($widest + 2))
        for group in $groups {
            let members = ($commands | where {|item| $item.group == $group })
            if ($members | length) == 0 { continue }
            r3 heading $console $group
            for member in $members {
                r3-help-row $console $member.name $member.summary $width
            }
        }
    }

    let notes = (r3-field $entry notes [])
    if ($notes | length) > 0 {
        if $command == null { print '' } else { r3 heading $console NOTES }
        for note in $notes { r3 status $console info $note }
    }

    let examples = (r3-field $entry examples [])
    if ($examples | length) > 0 {
        r3 heading $console EXAMPLES
        for example in $examples {
            r3-print-line $console [{text: $"  ($example)", role: accent}]
        }
    }
    print ''
}
