# Visual Consistency

## Scope

Use this reference for color, typography, icons, spacing, control states, contrast, and theme adaptation in Plasma shell UI, widgets, KCMs, and KDE applications. It defines required behavior, not a frozen token catalog. Exact role names, imports, and available properties must be confirmed for the target KF version.

## Color

- **[Official] Forbidden:** hardcoded color literals in Plasma UI chrome. This includes hex values, named CSS colors, and hardcoded gradients in panels, popups, toolbars, dialogs, headers, and controls.
- [Official] Kirigami's palette follows system colors. Kirigami and QtQuick Controls already follow the palette by default, so custom coloring is usually unnecessary.
- [Official] Primitive items such as `Rectangle` should be colored from `Kirigami.Theme`; hardcoded colors such as `#32b2fa` or `red` should usually be avoided.
- [Official] If custom colors are genuinely required, they belong in an area where only custom colors are used — usually the content area, and never in chrome areas such as toolbars or dialogs.
- [Recommendation] Use semantic roles (`Kirigami.Theme.backgroundColor`, `textColor`, `highlightColor`, `highlightedTextColor`, and other documented roles) instead of literal values. Verify role availability in the target KF version rather than assuming a fixed list.
- [Official] `Kirigami.Theme` is an attached property available to any QML item. Setting `Kirigami.Theme.colorSet` makes children inherit that set unless `Kirigami.Theme.inherit: false` is set explicitly.
- [Official] Documented color sets include `View`, `Window`, `Button`, `Selection`, `Tooltip`, and `Complementary`. Use them to distinguish regions, not to invent a new palette.
- [Official] When overriding theme colors, replace all relevant colors in `Theme`; the Kirigami documentation warns that partial replacement can produce badly contrasting colors.
- [Recommendation] Never encode meaning in color alone. Pair it with text, an icon, or a shape.

## Accent colors

- [Official] The system color scheme and accent color are user-controlled. Components that follow `Kirigami.Theme` inherit them.
- [Recommendation] Use the theme highlight role for selection, focus-adjacent emphasis, and active state. Do not hardcode a brand accent in Plasma chrome.
- [Recommendation] Verify selected, hovered, and focused combinations against the user's accent; an accent that contrasts with the default palette may not contrast with a custom one.

## Typography

- [Official] Use `QtQuick.Controls.Label` for normal-sized text and `Kirigami.Heading` with an appropriate level for larger header text.
- [Official] Do not use `QtQuick.Text` directly for UI labels; it does not respect the system's font settings.
- [Official] `Kirigami.Theme.defaultFont` exposes the theme font; its point size is available as `Kirigami.Theme.defaultFont.pointSize`.
- [Recommendation] Never set a font family in Plasma chrome. Size and weight should come from theme roles or a small documented scale derived from the theme font.
- [Recommendation] Test at the user's default size and at an increased system font size. Layout must reflow, not clip or overlap.
- [Recommendation] Keep line length readable and avoid fixed-width labels for translatable text.

### The heading ladder

[Official] `Kirigami.Heading` multiplies `Theme.defaultFont.pointSize` by its level: L1 ×1.35, L2 ×1.20, L3 ×1.15, L4 ×1.10, L5 ×1.00. `type: Kirigami.Heading.Primary` selects `Font.DemiBold`; the default is `Font.Normal`. The multipliers are Kirigami implementation, not a KDE-approved type scale; verify them for the target KF version.

| Role | Choice |
|---|---|
| Popup or page title | `Heading` L1–L2, only when the shell does not draw a heading |
| Card or list-item title | `Heading` **L4**, `type: Primary`, wraps to at most 3 lines |
| Metadata (app name, timestamp, origin) | `Heading` **L5**, `opacity: 0.9`, elided |
| Section header | `Heading` **L5**, `opacity: 0.75`, followed by a separator |
| Body | `Label` or `Kirigami.SelectableLabel` when the text is selectable |
| Helper or explanation | `PlasmaExtras.DescriptiveLabel`, `opacity: 0.75` (`0.85` when active) |
| Anything smaller | `Kirigami.Theme.smallFont` at `opacity: 0.75` |

- [Recommendation] Build hierarchy from **one size step plus opacity**, not from a bespoke six-size scale. A new size is a new token nobody else honors.
- [Recommendation] Do not invent a "secondary text color". Secondary hierarchy is opacity on the theme text color.
- [Recommendation] Never use a heading level to solve a layout problem; if a level does not fit, the content is too dense for that surface.

### Numeric text

- [Recommendation] Live numeric values set `font.features: { "tnum": 1 }` for tabular figures. Official monitored-data rows do this explicitly; without it the value column jitters on every refresh.
- [Recommendation] Right-align value columns, elide them, and reserve a stable width from the formatter so the row does not reflow as digits change.
- [Recommendation] Keep the unit inside the formatted string and reduce precision before hiding the unit.
- [Recommendation] De-emphasize supporting figures with `opacity: 0.75`, not with a separate muted color role.

## Spacing and metrics

- [Official] The HIG documents Kirigami units for consistent spacing: `smallSpacing` between directly related items, `mediumSpacing` between toolbar items, `largeSpacing` between groups and at page edges, `cornerRadius` for rounded elements, and `gridUnit` for fixed-size elements.
- [Recommendation] Reference `Kirigami.Units` values. Never copy the numeric value from the HIG table into source; units adapt to display scale and user settings.
- [Recommendation] Group with spacing before adding separators or frames. Proximity communicates relationship more reliably than decoration.
- [Recommendation] Use `QtQuick.Layouts` for resizable composition; avoid anchoring to hardcoded pixel positions in translatable or scalable UI.

## Icons

- [Official] KDE apps respect the FreeDesktop icon theme and naming specification and make extensive use of themable icons. Breeze is KDE's icon theme, and apps should look correct with it.
- [Official] Browse available icons with Icon Explorer from `plasma-sdk`. Request a missing icon rather than shipping a one-off glyph.
- [Recommendation] Use symbolic icons (`*-symbolic` where provided) for toolbar buttons, menu items, and inline actions so they follow the text color. Use colorful icons for application, place, and file-type identity.
- [Official] Prefer universal icons when a text label or surrounding context makes the meaning obvious; use specific icons when items would otherwise share the same icon.
- [Official] Destructive actions must be consistently indicated. Breeze uses red destructive icons such as `edit-delete` and `edit-delete-remove`; do not use red or X symbolism for non-destructive actions.
- [Official] Icon-only buttons are exceptional: only when space is critical, when a related icon group is self-explanatory, or for non-core actions with instantly recognizable imagery. In doubt, show text.
- [Official] Assign text to icon-only buttons anyway so screen readers can announce them, hide it with `AbstractButton.display: IconOnly`, and provide a tooltip for pointer and touch users.
- [Official] The HIG documents icon sizes by context: `IconSizes.small` for menu items and raised buttons, `IconSizes.smallMedium` for flat/toolbar buttons and list items without subtitles, `IconSizes.medium` for list items with subtitles.

## Control states

Every interactive control must define all applicable states. A missing state is a defect, not a styling preference.

| State | Required observable behavior | Check |
|---|---|---|
| Normal | Legible against its color set; clear affordance | Readable without hover |
| Hover | Noticeable but not louder than focus | Does not move layout or change meaning |
| Focus | Visible ring or equivalent, distinct from selection | Keyboard-only pass; visible in light and dark schemes |
| Pressed | Immediate tactile feedback | No double action; state clears correctly |
| Disabled | Clearly unavailable; reason discoverable elsewhere | Not the only signal of why an action is blocked |
| Loading | Progress or busy indication; interaction policy defined | `BusyIndicator`; respects instant-animation setting |
| Error | Text plus icon or shape, not color alone | Actionable message; field-level where possible |

- [Official] The HIG requires each item with active focus to look visibly different from selected items in inactive views.
- [Official] `BusyIndicator` draws from the Plasma Style and does not rotate when the system animation speed is Instant. Test that state.
- [Recommendation] Disabled controls should remain legible. Do not rely on very low contrast to communicate unavailability.
- [Recommendation] Do not use a checkable button for a two-state setting when a switch or checkbox fits; the HIG notes checkability is not obvious.

## Contrast

- [Official] Kirigami guidance asks authors to ensure chosen colors have good contrast and are WCAG compliant.
- [Recommendation] Treat the following as a review baseline, not a KDE mandate: 4.5:1 for normal text, 3:1 for large text, and 3:1 for UI component boundaries and graphical objects required for understanding, following WCAG 2.2 AA.
- [Recommendation] Contrast is a property of the rendered pair, including custom color schemes and accent colors. Sample the actual colors rather than assuming the default theme.
- [Recommendation] Focus indicators, selection highlights, and error outlines need non-text contrast against adjacent colors.
- [Recommendation] Never use opacity alone to create a disabled or secondary style without checking the resulting contrast.

## Dark, light, and custom schemes

- [Recommendation] Test at least Breeze Light, Breeze Dark, and one custom or high-contrast scheme.
- [Recommendation] Do not ship raster assets with baked backgrounds in chrome. Prefer theme-colored primitives, symbolic icons, and Plasma Style SVG elements where applicable.
- [Official] A color set applies recursively to children. Set `Kirigami.Theme.inherit: false` when forcing a different set, and re-check every nested control afterward.
- [Recommendation] Avoid assumptions that "background is light" or "text is dark". Both invert under dark schemes and can invert again under custom schemes.
- [Recommendation] Check translucent or blurred surfaces against multiple wallpapers and color schemes; transparency can destroy contrast even when the base palette is correct.
- [Recommendation] An alpha channel does not blur anything by itself. KWin blurs only the regions a client declares, and for a widget that is the Plasma theme background frame; a translucent surface over `NoBackground` is translucent *without* blur. For the blurred case, keep the theme background hints and let the card supply only a tint. Verify in a real session: desktop widgets and panel popups do not necessarily behave the same.

## Surface ownership

- [Official] A Plasma applet does not paint its own chrome. It requests the theme frame with `Plasmoid.backgroundHints: PlasmaCore.Types.DefaultBackground | PlasmaCore.Types.ConfigurableBackground` and lets the Plasma Style supply the surface.
- [Observed] Official applets use **no explicit surface color roles** in their popup content: `PlasmaExtras.Representation` supplies the page, `PlasmaExtras.PlasmoidHeading` supplies the header over `widgets/plasmoidheading`, `KSvg.FrameSvgItem widgets/listitem` supplies the list highlight, `SvgItem widgets/line` supplies separators, and list `ScrollView` sets `background: null`.
- [Recommendation] Do not paint the popup background, do not stack a full-bleed `Rectangle` as the representation root, and do not reimplement a header the shell already draws.
- [Recommendation] When content genuinely needs a distinct region, prefer separation first: spacing, `Kirigami.Separator`, or an opaque `Kirigami.Theme.backgroundColor` panel. A card is a last resort, not the default composition unit.
- [Recommendation] Custom glow, gradient, and drop-shadow effects are incompatible with this grammar. They cannot follow the user's accent or Plasma theme, they encode state in color alone, and they destroy contrast over arbitrary wallpapers. Express emphasis with size, spacing, weight, and opacity instead.
- [Unknown] Whether a given Plasma theme frame provides blur for a given surface depends on KWin, the containment, and the theme. Verify in a real session; never assume a tint will be blurred.

## Visual hierarchy

- [Recommendation] Establish one primary action per view, then secondary actions, then destructive actions separated by position and styling.
- [Recommendation] Use type scale, spacing, and alignment before color or decoration to create hierarchy.
- [Recommendation] Keep chrome quiet and give content the strongest contrast and largest area.
- [Recommendation] Align to a consistent grid and reuse the same spacing rhythm across panels, popups, and settings pages.

## Review checklist

1. No hardcoded color, font family, or pixel metric in chrome.
2. Every color resolves through `Kirigami.Theme`; role availability verified for the target KF version.
3. Typography uses `Label` and `Kirigami.Heading`, not raw `Text`.
4. Symbolic icons in actions; colorful icons only for identity.
5. Icon-only buttons have text, an accessible name, and a tooltip.
6. All seven control states are defined where applicable.
7. Contrast checked on rendered colors in light, dark, and one custom scheme.
8. Focus is visible and distinct from selection.
9. No meaning conveyed by color alone.
10. Layout survives increased font size and display scaling.
11. The applet requests the theme background and paints no popup surface of its own.
12. No custom gradient, glow, blur, or drop shadow anywhere in chrome or content cards.
13. Hierarchy uses the heading ladder plus opacity; no ad-hoc point sizes and no invented muted color.
14. Live numeric values use tabular figures, right alignment, and a reserved width.

## Sources

- Layout and navigation (Kirigami units and icon sizes) — https://develop.kde.org/hig/layout_and_nav/ — Accessed: 2026-10-20
- Text and labels — https://develop.kde.org/hig/text_and_labels/ — Accessed: 2026-10-20
- Icons — https://develop.kde.org/hig/icons/ — Accessed: 2026-10-20
- Communicating status changes — https://develop.kde.org/hig/status_changes/ — Accessed: 2026-10-20
- Colors and themes in Kirigami — https://develop.kde.org/docs/getting-started/kirigami/style-colors/ — Accessed: 2026-10-20
- Typography in Kirigami — https://develop.kde.org/docs/getting-started/kirigami/style-typography/ — Accessed: 2026-10-20
- Plasma's QML API (BusyIndicator behavior) — https://develop.kde.org/docs/plasma/widget/plasma-qml-api/ — Accessed: 2026-10-20
- WCAG 2.2 contrast minimum — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — Accessed: 2026-10-20
- WCAG 2.2 non-text contrast — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — Accessed: 2026-10-20
- plasma-workspace notifications applet, branch `Plasma/6.8` (surface, typography, numeric rows) — https://invent.kde.org/plasma/plasma-workspace/-/tree/Plasma/6.8/applets/notifications — Accessed: 2026-10-20
- Installed `org.kde.plasma.systemmonitor` faces and `PlasmaExtras` primitives, Plasma 6.8.0 — local, Accessed: 2026-10-20
- KDE API reference (verify roles and imports) — https://api.kde.org/ — Accessed: 2026-10-20

## Version notes

Verified against Kirigami documentation and KDE HIG pages as published on 2026-10-20, with a local baseline of Plasma 6.8.0, Qt 6.11.1, and KF6.

- [Recommendation] Color role names and color-set names have changed across KF major versions. Confirm each name in `https://api.kde.org/` for the target version before writing code.
- [Official] PlasmaComponents 2 was removed in Plasma 6.0; do not copy imports from Plasma 5 material.
- [Recommendation] WCAG thresholds are external accessibility guidance, not a KDE requirement. A project may adopt stricter targets.
- [Recommendation] Heading multipliers are Kirigami implementation details read from source, not a published KDE type scale. Re-read `Heading.qml` for the target KF version before treating the table as fixed.
