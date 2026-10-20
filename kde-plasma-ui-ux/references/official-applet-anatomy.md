# Official applet anatomy

## Scope

Use this reference when building or reviewing a Plasma widget that must read as shipped KDE work: the visual grammar, metric envelope, and state model actually used by official applets in Plasma 6.8. It is the evidence base behind the rules in `visual-consistency.md`, `plasma-components.md`, `interaction-patterns.md`, and `accessibility.md`.

It is not a copy-paste recipe. Official applets differ from each other. What follows are patterns observed in more than one official surface, with the exact source cited so you can re-check against your target branch.

Evidence base, inspected on 2026-10-20 against Plasma 6.8.0 / Qt 6.11.1 / KF6:

- `plasma-workspace` branch `Plasma/6.8`, `applets/notifications` and `applets/systemtray` [Official]
- Installed `org.kde.plasma.systemmonitor` with its nine sensor faces, plus `org.kde.plasma.vault` and `org.kde.plasma.kdeconnect` [Observed]
- `PlasmaExtras`, `PlasmaComponents3`, and Kirigami primitives installed on the local system [Observed]

The notifications applet is compiled into plasma-workspace on a normal install (`org.kde.plasma.notifications.so`); read the source from the branch, not from `/usr/share/plasma/plasmoids`.

## The one rule that explains the rest

[Official] Official applets do not paint their own surface. The widget requests the Plasma theme frame:

```qml
Plasmoid.backgroundHints: PlasmaCore.Types.DefaultBackground | PlasmaCore.Types.ConfigurableBackground
```

Surfaces come from Plasma Style elements — `PlasmaExtras.Representation` (page), `PlasmaExtras.PlasmoidHeading` (header over `widgets/plasmoidheading`), `KSvg.FrameSvgItem` with `widgets/listitem` for list hover/focus, `SvgItem widgets/line` for separators. The notifications applet uses **zero explicit surface color roles** and no custom blur, shadow, or gradient [Official, `applets/notifications/contents/ui/**`].

Consequences:

- A translucent, glowing, or gradient card system is not a styling choice inside this grammar; it is a different grammar. It cannot follow the user's Plasma theme or accent reliably and it breaks contrast over arbitrary wallpapers.
- Content may use `Kirigami.Theme.backgroundColor` for an opaque inner card when a card is genuinely needed. Official data UI prefers **separation** (`Kirigami.Separator`, spacing) over a card box.
- Blur belongs to KWin and the theme frame. An alpha tint over `NoBackground` is translucent *without* blur.

## Shell anatomy

| Element | Official pattern | Evidence |
|---|---|---|
| Root | `PlasmoidItem`; `Plasmoid.backgroundHints` as above | `systemmonitor/contents/ui/main.qml:22` [Observed] |
| Compact | `compactRepresentation`; minimum `gridUnit`, preferred width `height * 1.618` in a horizontal panel, maximum `iconSizes.enormous`; `defaultFont → smallFont` is the only collapse step | `faces/CompactSensorFace.qml:17-30`, `textonly/CompactRepresentation.qml:41-42` [Observed] |
| Expanded | `PlasmaExtras.Representation`; typical minimum `gridUnit * 18 × gridUnit * 12`; list shell is `ScrollView { background: null }` + `ListView` with `smallSpacing` and `largeSpacing` edges | `vault/contents/ui/main.qml:59-88` [Observed] |
| Heading | `PlasmoidHeading`/`BasicPlasmoidHeading`, auto-hidden when the containment draws the heading; `Heading level: 1` only when the shell does not | `PlasmaExtras/BasicPlasmoidHeading.qml:35-44` [Observed] |
| Title inside content | `Kirigami.Heading { level: 2 }`, not a custom font | `textonly/FullRepresentation.qml:30-43` [Observed] |
| Background hints | Default + `ConfigurableBackground`; the user can remove the frame | `systemmonitor/main.qml:22` [Observed] |

[Recommendation] Set `switchWidth`/`switchHeight` from the compact and full minimums, as system monitor does, instead of hand-picking pixel values.

## List and section anatomy

- [Observed] Section header: `PlasmaExtras.ListSectionHeader` — `topPadding: largeSpacing + smallSpacing`, `Heading level: 5`, `opacity: 0.75`, `elide: ElideRight`, followed by a `widgets/line` hairline.
- [Observed] Delegate padding: `largeSpacing` left/right in the notifications list; `smallSpacing` between icon and text.
- [Observed] Separator: `Kirigami.Separator`, one pixel, interpolating background→text at the frame contrast. Do not fake it with a 1 px `Rectangle` of arbitrary alpha.
- [Observed] Group/relationship rails: 3 px `Rectangle` at `textColor`, `opacity: 0.2`, used in notification groups. This is a legitimate, official way to show grouping.
- [Observed] Delegate structure: fixed leading icon, then a content column, then a trailing state element. The trailing element is text or an icon, not a colored dot alone.

## Typography ladder

[Official] `Kirigami.Heading` multiplies `Theme.defaultFont.pointSize` by level: L1 ×1.35, L2 ×1.20, L3 ×1.15, L4 ×1.10, L5 ×1.00. `type: Kirigami.Heading.Primary` selects `Font.DemiBold`; the default is `Font.Normal` [Kirigami `Heading.qml`, `units.cpp`].

| Role | Official choice |
|---|---|
| Notification title / card title | `Kirigami.Heading` **level 4**, `type: Primary`, max 3 lines, `elide: ElideRight` |
| App or origin name, timestamp | `Kirigami.Heading` **level 5**, `opacity: 0.9`, `elide: ElideMiddle` for names |
| Body | `Kirigami.SelectableLabel`, default font, `TextEdit.Wrap` |
| Explanation / helper | `PlasmaExtras.DescriptiveLabel`, `opacity: 0.75` (`0.85` when active) |
| Section header | `Heading level: 5`, `opacity: 0.75` |
| Empty-state title | `Heading`, `type: Primary`, whole block at `opacity: 0.75` when informational |

[Recommendation] The hierarchy is created by **one step of size plus opacity**, not by inventing a six-size scale. Anything below `Heading` level 5 belongs in `smallFont` at 0.75, not at another arbitrary size.

## Numeric presentation

The canonical monitored-value row is `ChartsControls.LegendDelegate` [Observed]:

```qml
Label {
    Layout.fillWidth: true
    horizontalAlignment: Text.AlignRight
    elide: Text.ElideRight
    font.features: { "tnum": 1 }
}
```

- [Observed] `font.features: { "tnum": 1 }` is explicit in official code. Without tabular figures a live value column jitters on every update.
- [Observed] Reserve the value column with a formatter width (`Formatter.maximumLength(unit, font)`) so the row does not reflow when digits change.
- [Observed] The unit lives inside the formatted value; there is no separate unit widget. Reduce precision before hiding the unit.
- [Observed] Hero value: centre it, `fontSizeMode: Text.HorizontalFit` with `minimumPointSize: smallFont.pointSize * 0.8`, `wrapMode: Wrap`, `maximumLineCount: 1`, so the unit disappears before the number wraps (`UsedTotalDisplay.qml:86-96`).
- [Observed] De-emphasis is `opacity: 0.75`, never a separate "secondary text color".
- [Observed] Series color is one **flat** color per series, derived from `highlightColor`. Gradients inside a data mark are not part of this grammar.

Charts: [Observed] `lineWidth: 1`, fill opacity `0.1`, grid `1 px` at a 0.2 background→text interpolation, 3 major grid lines, no minor grid, axis labels in `smallFont` at 0.75–0.8 alpha on a background pill (`LineChartCard.qml:89-121`, `barchart/FullRepresentation.qml:107-111`).

## States

[Observed] Empty, loading, error, and unavailable share one component: `PlasmaExtras.PlaceholderMessage` / `Kirigami.PlaceholderMessage`.

- icon `round(iconSizes.huge * 1.5)` (96 px at defaults)
- `spacing: gridUnit`
- `Heading { type: Primary }` plus optional `explanation`
- optional `helpfulAction` with `Layout.topMargin: gridUnit`
- whole block at `opacity: 0.75` when `type: Informational`
- width usually `parent.width - gridUnit * 4`

Concrete official uses: `action-unavailable-symbolic` for unsupported platforms, a create action for an empty vault list, and "select an item" for an empty detail pane.

Loading is `Plasmoid.busy` plus `BusyIndicator`. There is no skeleton-card pattern in official applets [Observed].

Status is `Plasmoid.status` (`ActiveStatus`/`PassiveStatus`) plus a symbolic icon variant plus tooltip text. Never a color-only dot [Observed in the notifications applet; type documented in Plasma's QML API].

## Motion

[Observed] Durations come only from `Kirigami.Units`:

| Transition | Value |
|---|---|
| State change on the compact icon | `longDuration`, `Easing.InOutQuad`, on `opacity`/`scale` |
| Stack push | `InQuad`, fade 0→1 |
| Stack pop | `OutQuad`, fade 1→0 |
| List item entrance | `PropertyAction opacity 0` → `PauseAnimation longDuration` → `NumberAnimation longDuration` |
| List highlight movement | `highlightMoveDuration: 0` (instant) |
| Appear animation | `longDuration`-class, `Easing.InExpo`, opacity 0→1, scale 0.8→1.0 |

- [Observed] When a delegate resizes, official code compensates the vertical shift with a manual `Translate` + `NumberAnimation` because `ListView` add/remove transitions misbehave (source cites bug 427894 / QTBUG-110366).
- [Observed] Reduced motion is handled by gating decorative animation on `Kirigami.Units.longDuration > 1`, which collapses when the system animation speed is Instant.
- [Observed] Official applets never animate values, chart data, gauge fill, or anything looping. Progress is `BusyIndicator`, which is static under Instant animations.

## Interaction contract

- [Observed] Compact: left click toggles expanded; middle click performs the secondary action; hover only changes the icon's `active` state.
- [Observed] Expanded: `Down` from the header control into the list, `Home`/`End`, `Delete` to dismiss, `Enter`/`Return` for the default action, `Left`/`Right` for hierarchy, mirrored under `LayoutMirroring`.
- [Observed] Keyboard focus uses the Plasma Style `widgets/listitem` `"pressed"` frame, deliberately distinct from `PlasmaExtras.Highlight`. Focus and selection must not look the same.
- [Observed] Icon-only buttons still set `text` (used by the accessibility layer), a `ToolTip`, and `Accessible.description`.
- [Observed] Context menus open from right-click and the Menu key; destructive items are separated last.

## Popup sizing envelope

[Observed] From the notifications applet `Globals.qml` and `NotificationPopup.qml`, useful as a starting envelope for any panel popup:

- content width `gridUnit * 18`, or `gridUnit * 22` when centred; clamp to at most `3 ×` that width
- minimum edge distance `2 * gridUnit`
- maximum vertical use `0.8` of the screen
- concurrent popup limit `ceil(screenHeight / (gridUnit * 4))`
- body text cap of 8 lines inside a popup, with a scrollbar only when overflowing

[Recommendation] A panel popup sized from these numbers behaves like a popup. A popup sized as a phone-app viewport behaves like a window smuggled into a panel.

## Tray and "Status and Notifications"

- [Observed] "Status and Notifications" is the **system tray applet's popup title** (`applets/systemtray/qml/ExpandedRepresentation.qml:76`), not a separate applet.
- [Observed] In Plasma 6.8 the tray satisfies discovery using `X-Plasma-NotificationAreaCategory` only; `applets/systemtray/plasmoidregistry.cpp` skips any plugin whose category is empty. Set `X-Plasma-NotificationArea` too, but do not rely on it alone.
- [Observed] The tray merges a third-party applet's header and footer with its own chrome only when `fullRepresentation` is a `PlasmaComponents3.Page` or a `PlasmaExtras.Representation` whose header is a `PlasmaExtras.PlasmoidHeading` (`PlasmoidPopupsContainer.qml`). This is the highest-value native seam available to third-party widgets.
- [Official] The notifications applet exposes no provider or page-injection API. External progress can appear only through the D-Bus `org.kde.JobViewServer` / `org.kde.JobViewV2` protocol or through a real `KNotification`. Do not design around content injection; it does not exist.

## Identity without breaking the grammar

[Recommendation] Official applets are identical in **material** and distinct in **composition**. Put a product's identity in what it composes, never in a custom material:

- distinctive data marks are allowed if they are flat, theme-colored, and encode magnitude by geometry (arc, bar, rail);
- distinctive navigation is allowed if it is a standard control (`TabBar`, `ToolButton` + `ModelContextMenu`) with keyboard support;
- distinctive grouping is allowed if it uses spacing, separators, or the 0.2-opacity rail;
- identity is never carried by glow, gradient, translucency, custom shadows, or a custom header.

## Testable rules

Express these as repository tests or `grep` gates; they are the cheapest way to keep a codebase inside the grammar. The checker in `../kde-plasma-best-practices/scripts/lint_qml.py` automates gates 1, 2, 4, 6 and 8, and reports the role-plus-alpha form of gate 1 as informational, because only the project knows whether that surface is on its documented allowlist.

1. No literal colors in `contents/ui`: `grep -rnE '#[0-9A-Fa-f]{3,8}|Qt\.rgba?\('` returns nothing outside a documented allowlist.
2. No custom material: `grep -rnE 'Gradient|MultiEffect|DropShadow|FastBlur|layer\.effect'` returns nothing.
3. The applet requests the theme background: `backgroundHints` contains `DefaultBackground | ConfigurableBackground`, and no representation root is a self-painted `Rectangle`.
4. No numeric spacing or radius literals: `grep -rnE '(spacing|Padding|Margin|radius):\s*[0-9]+'` returns nothing except `0`.
5. Values are tabular and right-aligned: every live-value `Label` sets `font.features` with `"tnum": 1`.
6. Typography comes from the ladder: no `font.pointSize` literals, no raw `Text` for UI labels.
7. Every model surface has empty/error states: one `PlaceholderMessage` per collection, and loading is `Plasmoid.busy`.
8. Motion is bounded and sourced: every `NumberAnimation`/`Behavior` uses `Kirigami.Units.*Duration`; no `loops: Animation.Infinite`.
9. Panel identity is symbolic: compact/action icons use `-symbolic` variants and follow the theme text color.
10. Actions are reachable without a pointer: every icon-only control has `text`, `ToolTip`, and `Accessible.name`.

## Sources

- plasma-workspace, `applets/notifications` (branch `Plasma/6.8`) — https://invent.kde.org/plasma/plasma-workspace/-/tree/Plasma/6.8/applets/notifications — Accessed: 2026-10-20
- plasma-workspace, `applets/systemtray` (branch `Plasma/6.8`) — https://invent.kde.org/plasma/plasma-workspace/-/tree/Plasma/6.8/applets/systemtray — Accessed: 2026-10-20
- Kirigami `Heading.qml` and `units.cpp` — https://invent.kde.org/frameworks/kirigami — Accessed: 2026-10-20
- Installed `org.kde.plasma.systemmonitor` faces and PlasmaExtras primitives on Plasma 6.8.0 — local, Accessed: 2026-10-20
- KDE HIG, layout and navigation — https://develop.kde.org/hig/layout_and_nav/ — Accessed: 2026-10-20

## Version notes

- Verified against the Plasma/6.8 branch and a local Plasma 6.8.0 / Qt 6.11.1 / KF6 install on 2026-10-20.
- [Unknown] Exact `smallSpacing`, `largeSpacing`, `cornerRadius`, and duration constants are computed in C++ from font metrics and the animation-speed setting; they are not readable from installed QML. Reference the roles, never the numbers.
- [Recommendation] The notifications applet is compiled on normal installs. Re-read the branch for your target release instead of assuming the file layout is installed.
- [Unknown] Tray discovery behavior is version-specific. The category-only filter was observed on `Plasma/6.8`; confirm on the branch you target.
