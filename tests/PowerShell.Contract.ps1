param([Parameter(Mandatory)][string]$ModulePath)
$ErrorActionPreference = 'Stop'
Import-Module $ModulePath -Force
$script:assertions = 0
function Assert-Contract($Condition, [string]$Message) {
    $script:assertions++
    if (-not $Condition) { throw $Message }
}
function Assert-Throws([scriptblock]$Action, [string]$Message) {
    $thrown = $false
    try { & $Action | Out-Null } catch { $thrown = $true }
    Assert-Contract $thrown $Message
}
$fixture = Get-Content (Join-Path $PSScriptRoot 'fixtures/console-contract.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($ascii in @($true,$false)) {
    $script:lines = [Collections.Generic.List[string]]::new()
    $console = New-R3Console -Colour never -Ascii:$ascii -Width $fixture.width -Sink { param($line,$stream) $script:lines.Add($line) }
    foreach ($command in $fixture.commands) {
        switch ($command.op) {
            banner { Write-R3Banner $console $command.text }
            heading { Write-R3Heading $console $command.text }
            line { Write-R3Line $console $command.segments }
            default { Write-R3Status $console $command.op $command.text }
        }
    }
    $expected = if ($ascii) { $fixture.ascii } else { $fixture.unicode }
    Assert-Contract (($script:lines -join "`n") + "`n" -ceq $expected) 'Cross-language output contract changed'
}
$originalNoColor = [Environment]::GetEnvironmentVariable('NO_COLOR')
try {
    [Environment]::SetEnvironmentVariable('NO_COLOR','1')
    Assert-Contract (-not (New-R3Console -IsTerminal $true).UseColour) 'NO_COLOR was ignored'
    Assert-Contract ((New-R3Console -Colour always -IsTerminal $false).UseColour) 'Explicit always must override NO_COLOR'
    [Environment]::SetEnvironmentVariable('NO_COLOR',[NullString]::Value)
    Assert-Contract (-not (New-R3Console -IsTerminal $false).UseColour) 'Redirected output must be plain in auto'
    Assert-Contract ((New-R3Console -IsTerminal $true).UseColour) 'Terminal colour detection failed'
} finally { [Environment]::SetEnvironmentVariable('NO_COLOR',$(if ($null -eq $originalNoColor) { [NullString]::Value } else { $originalNoColor })) }
$console = New-R3Console -Colour never -ThemeExtension @{client='#123456'}
Assert-Contract ($console.Theme.client -eq '#123456' -and $console.Theme.heading -eq '#50CDDC') 'Theme inheritance failed'
Assert-Throws { New-R3Console -ThemeExtension @{client='blue'} } 'Invalid theme accepted'
Assert-Throws { Write-R3Line $console @(@{Text='bad';Role='absent'}) } 'Unknown role accepted'
Assert-Contract ($console.Pending.Count -eq 0) 'Failed write polluted the next response'
$console = New-R3Console -Colour always -Width 50
$information = @(); $pipeline = @(Write-R3Status $console success 'Ready.' -InformationVariable information 6>$null)
Assert-Contract ($pipeline.Count -eq 0 -and $information.Count -eq 1) 'Human text leaked into the object pipeline'
Assert-Contract ([string]$information[0] -match '\x1b\[') 'Forced colour is missing'
$warnings = @(); Write-R3Status $console warning 'Review.' -WarningVariable warnings -WarningAction SilentlyContinue
Assert-Contract ($warnings.Count -eq 1) 'Warning stream was not preserved'
$diagnostic = Format-R3Diagnostic -Message 'Invalid input' -Details 'Missing field' -Hint 'repair' -Code 'Tool.Invalid'
Assert-Contract ($diagnostic -match '^Invalid input\.' -and $diagnostic -match 'Details: Missing field\.' -and $diagnostic -notmatch '\x1b') 'Diagnostic formatting failed'
$catalogue = @{
    Product='TOOL'; Version='1'; Description='Example'; Invocation='tool'; Groups=@('CONTENT')
    Usage=@('tool <command>'); GlobalItems=@(@{Label='--ascii';Description='ASCII symbols'})
    Commands=@(@{Name='check';Group='CONTENT';Summary='Check';Description='Check the project';Usage=@('tool check');Items=@(@{Label='<long-selector>';Description='Choose content without truncating this description.'});Notes=@();Examples=@()})
    Notes=@()
}
Assert-Contract (Test-R3HelpCatalogue $catalogue -ExecutableCommands @('check')) 'Valid catalogue rejected'
Assert-Throws { Test-R3HelpCatalogue $catalogue -ExecutableCommands @('missing') } 'Dispatch drift was accepted'
$invalid = $catalogue.Clone(); $invalid.Commands = @($catalogue.Commands[0],$catalogue.Commands[0])
Assert-Throws { Test-R3HelpCatalogue $invalid } 'Duplicate command was accepted'
foreach ($width in @(30,50,80,120)) {
    $script:lines = [Collections.Generic.List[string]]::new()
    $console = New-R3Console -Colour never -Ascii -Width $width -Sink { param($line,$stream) $script:lines.Add($line) }
    Write-R3Help $console $catalogue check
    Assert-Contract (@($script:lines | Where-Object Length -gt $width).Count -eq 0) "Help exceeded width $width"
    Assert-Contract (($script:lines -join '') -match 'Choose content without truncating this description\.') 'Help lost content'
    Write-R3Line $console @(@{Text='Keep complete words when wrapping narrow descriptions';Role='value'})
    Assert-Contract (-not @($script:lines | Where-Object { $_ -match 'wrapp$|descri$' }).Count) 'Words were split despite fitting the terminal width'
    Write-R3Line $console @(@{Text='[literal] café 漢字';Role='accent'})
    Assert-Contract ($script:lines[-1] -ceq '[literal] café 漢字') 'Literal text was interpreted as markup'
    Write-R3Table $console @('NAME','VALUE') @(,@('Long name with spaces','Very long value that must be preserved'))
    Assert-Contract (($script:lines -join '') -match 'Very long value that must be preserved') 'Table truncated a value'
}
Write-Output "$script:assertions PowerShell contract assertions passed."
