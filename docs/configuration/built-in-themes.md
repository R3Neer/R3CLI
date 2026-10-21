---
type: configuration
---

# Built-in themes

Themes are a closed catalog of complete values for the eight semantic tokens. Applications select a built-in identifier or let the output session choose automatically; users may override individual tokens without defining theme files.

## Reference

Each reference background is metadata describing the intended environment, not a ninth token or an instruction to paint the terminal. These are fixed R3CLI adaptations of published palettes. Source updates are not downloaded or applied at runtime. Catppuccin is the preferred family for automatic-selection ties.

| Family | Dark identifier | Light identifier | Source |
|---|---|---|---|
| Catppuccin | `catppuccin-mocha` | `catppuccin-latte` | [Published palette](https://catppuccin.com/palette/) |
| Gruvbox | `gruvbox-dark` | `gruvbox-light` | [Published palette](https://github.com/morhetz/gruvbox/blob/master/colors/gruvbox.vim) |
| Solarized | `solarized-dark` | `solarized-light` | [Published palette](https://ethanschoonover.com/solarized/) |
| Nord | `nord-dark` | `nord-light` | [Published palette](https://www.nordtheme.com/docs/colors-and-palettes/) |
| Tokyo Night | `tokyo-night` | `tokyo-day` | [Published palette](https://github.com/folke/tokyonight.nvim) |

### Exact token values

The following values, also recorded in [the documentary preset data](built-in-themes.json), define the presets. Role mapping belongs to R3CLI. Changes from published RGB values were baked into these presets to target 4.5:1 foreground contrast on the stated opaque reference backgrounds; primary text was also checked on its LiteralBlock background. This is not runtime colour adjustment or a guarantee for arbitrary terminal backgrounds, fonts or transparency.

### catppuccin-mocha

Reference background: `#1e1e2e`.

| Token | RGB |
|---|---|
| `text.foreground` | `#CDD6F4` |
| `subtext.foreground` | `#A6ADC8` |
| `title.foreground` | `#CBA6F7` |
| `accent.foreground` | `#89B4FA` |
| `success.symbol.foreground` | `#A6E3A1` |
| `warning.symbol.foreground` | `#F9E2AF` |
| `failure.symbol.foreground` | `#F38BA8` |
| `literal-block.background` | `#313244` |
### catppuccin-latte

Reference background: `#eff1f5`.

| Token | RGB |
|---|---|
| `text.foreground` | `#4C4F69` |
| `subtext.foreground` | `#5C5F77` |
| `title.foreground` | `#8839EF` |
| `accent.foreground` | `#1D64EF` |
| `success.symbol.foreground` | `#327D22` |
| `warning.symbol.foreground` | `#996214` |
| `failure.symbol.foreground` | `#D20F39` |
| `literal-block.background` | `#E6E9EF` |

Adapted foregrounds: `accent.foreground` (#1e66f5 → #1d64ef), `success.symbol.foreground` (#40a02b → #327d22), `warning.symbol.foreground` (#df8e1d → #996214).
### gruvbox-dark

Reference background: `#282828`.

| Token | RGB |
|---|---|
| `text.foreground` | `#EBDBB2` |
| `subtext.foreground` | `#BDAE93` |
| `title.foreground` | `#D3869B` |
| `accent.foreground` | `#83A598` |
| `success.symbol.foreground` | `#B8BB26` |
| `warning.symbol.foreground` | `#FABD2F` |
| `failure.symbol.foreground` | `#FB533F` |
| `literal-block.background` | `#3C3836` |

Adapted foregrounds: `failure.symbol.foreground` (#fb4934 → #fb533f).
### gruvbox-light

Reference background: `#fbf1c7`.

| Token | RGB |
|---|---|
| `text.foreground` | `#3C3836` |
| `subtext.foreground` | `#665C54` |
| `title.foreground` | `#8F3F71` |
| `accent.foreground` | `#076678` |
| `success.symbol.foreground` | `#75700E` |
| `warning.symbol.foreground` | `#976311` |
| `failure.symbol.foreground` | `#9D0006` |
| `literal-block.background` | `#EBDBB2` |

Adapted foregrounds: `success.symbol.foreground` (#79740e → #75700e), `warning.symbol.foreground` (#b57614 → #976311).
### solarized-dark

Reference background: `#002b36`.

| Token | RGB |
|---|---|
| `text.foreground` | `#8B9B9D` |
| `subtext.foreground` | `#7D9096` |
| `title.foreground` | `#8287CD` |
| `accent.foreground` | `#3694D5` |
| `success.symbol.foreground` | `#859900` |
| `warning.symbol.foreground` | `#B58900` |
| `failure.symbol.foreground` | `#E56462` |
| `literal-block.background` | `#073642` |

Adapted foregrounds: `text.foreground` (#839496 → #8b9b9d), `subtext.foreground` (#657b83 → #7d9096), `title.foreground` (#6c71c4 → #8287cd), `accent.foreground` (#268bd2 → #3694d5), `failure.symbol.foreground` (#dc322f → #e56462).
### solarized-light

Reference background: `#fdf6e3`.

| Token | RGB |
|---|---|
| `text.foreground` | `#586C73` |
| `subtext.foreground` | `#586E75` |
| `title.foreground` | `#666AB8` |
| `accent.foreground` | `#2076B3` |
| `success.symbol.foreground` | `#697800` |
| `warning.symbol.foreground` | `#8F6C00` |
| `failure.symbol.foreground` | `#D5302E` |
| `literal-block.background` | `#EEE8D5` |

Adapted foregrounds: `text.foreground` (#657b83 → #586c73), `title.foreground` (#6c71c4 → #666ab8), `accent.foreground` (#268bd2 → #2076b3), `success.symbol.foreground` (#859900 → #697800), `warning.symbol.foreground` (#b58900 → #8f6c00), `failure.symbol.foreground` (#dc322f → #d5302e).
### nord-dark

Reference background: `#2e3440`.

| Token | RGB |
|---|---|
| `text.foreground` | `#ECEFF4` |
| `subtext.foreground` | `#D8DEE9` |
| `title.foreground` | `#B590AF` |
| `accent.foreground` | `#88C0D0` |
| `success.symbol.foreground` | `#A3BE8C` |
| `warning.symbol.foreground` | `#EBCB8B` |
| `failure.symbol.foreground` | `#CF888F` |
| `literal-block.background` | `#3B4252` |

Adapted foregrounds: `title.foreground` (#b48ead → #b590af), `failure.symbol.foreground` (#bf616a → #cf888f).
### nord-light

Reference background: `#eceff4`.

| Token | RGB |
|---|---|
| `text.foreground` | `#2E3440` |
| `subtext.foreground` | `#4C566A` |
| `title.foreground` | `#7F657A` |
| `accent.foreground` | `#516F93` |
| `success.symbol.foreground` | `#617254` |
| `warning.symbol.foreground` | `#7B6B49` |
| `failure.symbol.foreground` | `#A6545C` |
| `literal-block.background` | `#E5E9F0` |

Adapted foregrounds: `title.foreground` (#b48ead → #7f657a), `accent.foreground` (#5e81ac → #516f93), `success.symbol.foreground` (#a3be8c → #617254), `warning.symbol.foreground` (#ebcb8b → #7b6b49), `failure.symbol.foreground` (#bf616a → #a6545c).
### tokyo-night

Reference background: `#1a1b26`.

| Token | RGB |
|---|---|
| `text.foreground` | `#C0CAF5` |
| `subtext.foreground` | `#A9B1D6` |
| `title.foreground` | `#BB9AF7` |
| `accent.foreground` | `#7AA2F7` |
| `success.symbol.foreground` | `#9ECE6A` |
| `warning.symbol.foreground` | `#E0AF68` |
| `failure.symbol.foreground` | `#F7768E` |
| `literal-block.background` | `#292E42` |
### tokyo-day

Reference background: `#e1e2e7`.

| Token | RGB |
|---|---|
| `text.foreground` | `#2E51A0` |
| `subtext.foreground` | `#546298` |
| `title.foreground` | `#7E46C9` |
| `accent.foreground` | `#2564B9` |
| `success.symbol.foreground` | `#526D35` |
| `warning.symbol.foreground` | `#7D6037` |
| `failure.symbol.foreground` | `#C12150` |
| `literal-block.background` | `#C4C8DA` |

Adapted foregrounds: `text.foreground` (#3760bf → #2e51a0), `subtext.foreground` (#6172b0 → #546298), `title.foreground` (#9854f1 → #7e46c9), `accent.foreground` (#2e7de9 → #2564b9), `success.symbol.foreground` (#587539 → #526d35), `warning.symbol.foreground` (#8c6c3e → #7d6037), `failure.symbol.foreground` (#f52a65 → #c12150).

## Resolution rules

1. An explicit output.theme selects its exact preset. Unknown identifiers fail; a path or URL is not a theme identifier.
2. When theme is omitted, obtain the current default background RGB from the host or a supported terminal query, then evaluate all built-in light/dark profiles. Never infer it from the shell name or the operating-system appearance.
3. Prioritize foreground contrast against the detected background and text contrast within LiteralBlock. Among candidates meeting the comparison target, prefer the perceptually nearest reference background; use a perceptual space such as OKLab rather than raw RGB channel distance. Deterministic ties prefer Catppuccin. Numerical tuning is an implementation detail to verify against representative backgrounds, not user-configurable weights.
4. If background information is unavailable, or no candidate is suitable, use the terminal's default foreground/background as a neutral fallback. Do not silently assume a dark background. Preserve component structure, messages and explicit user token overrides. Without a colour preset, LiteralBlock retains padding/spacing and uses the terminal background unless explicitly overridden; its foreground follows the same neutral fallback.
5. Apply explicit [tokens] overrides after preset selection. A deliberate override is not rewritten by automatic contrast adjustment. Retain the selection for the output session.

### Background ownership

output.background = "terminal" preserves the surrounding/default background and is the default. The theme's reference background remains selection metadata. output.background = "theme" fills only the application's owned output region with the selected preset's reference colour, including any owned blank cells; it never changes the terminal-wide default or the user's profile. A fullscreen terminal application can fill its complete owned surface. Neutral fallback has no theme fill. LiteralBlock is a local background-bearing component independently of this general setting.

### Detection

The queried value is the terminal's current default background RGB. For an opaque solid background it is that base colour. With transparency it remains the base colour used with opacity, not the desktop-composited pixel colour or an alpha value. Background images are not sampled. Windows Terminal's [OSC resource implementation](https://github.com/microsoft/terminal/blob/main/src/terminal/adapter/adaptDispatch.cpp) reports the RGB colour-table entry; [appearance settings](https://learn.microsoft.com/en-us/windows/terminal/customize-settings/profile-appearance) configure opacity and images separately.

Only query through an output session/host that can coordinate terminal input and consume the response without stealing keystrokes or pipeline stdin. Use bounded waiting and cache the result for the session. Do not query redirected output, structured streams, or colour-disabled presentation. If safe querying is unavailable, use the fallback. Capability detection, timeouts and response handling require real-terminal tests during implementation.

## Validation

- Every preset supplies exactly the eight standard tokens and one valid reference RGB.
- User-defined/imported themes, inheritance and runtime theme downloads are unsupported.
- Only terminal/theme are general background-policy values. Explicit token values retain their normal validation.
- Theme selection does not affect domain values, table alignment, semantic roles or output routing.
- Plain/structured output receives no background fill or probing sequences. Colour-disabled output removes local coloured backgrounds as well as foreground colour.

## Example

```toml
[output]
theme = "catppuccin-mocha"
background = "terminal"

[tokens]
"title.foreground" = "#B4BEFE"
```

Omit theme to enable automatic selection. Custom token names remain supported separately from custom theme definitions; see [[docs/configuration/colour-tokens|Colour tokens]].

## Preview

![[docs/assets/theme-comparison/comparison.png]]

[Compare all five families on light and dark backgrounds](../assets/theme-comparison/index.html)

The specimen demonstrates the eight tokens through descriptions corresponding to [[docs/structure|the combined C# example]]. Its solid backdrops simulate terminal environments; they do not imply that ordinary output paints those backgrounds. Individual component previews use fixed Catppuccin Mocha. The combined C# example preview exposes a built-in-profile selector that changes tokens and the complete simulated terminal backdrop together; this is an environment comparison, not the production background policy.
