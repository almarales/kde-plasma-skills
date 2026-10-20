# Qt, QML, and Kirigami UI conventions

Implementation conventions for QML-based KDE Plasma surfaces. This file covers structure, theming, layout, motion, localization, and component choice. It does not cover performance, object lifetime, or threading; those live in the companion engineering skill.

## Scope

- In scope: Plasma 6 plasmoids (desktop widgets, panels, system tray items), Kirigami applications, System Settings KCMs built with QML, and the Qt Widgets configuration dialogs still present in KDE codebases.
- Out of scope: QML engine internals, C++ ownership rules, rendering performance, packaging, and anything that applies to web UI. See the companion skill for implementation-quality rules.
- Target assumptions, verified locally on 2026-10-20: Plasma 6.8.0, Qt 6.11.1, KF6, `qmllint6` (Qt 6.11.1; the unversioned `qmllint` wrapper resolves to Qt 5 on this machine). Treat these as the authoring baseline, not as universal requirements. Always re-verify names and behavior against the branch and version you are changing.

## Evidence labels

Every substantive statement in this file carries one label. Apply the same discipline when you write a review or proposal.

| Label | Meaning |
| --- | --- |
| `[Official]` | Documented by current KDE or Qt documentation, cited in Sources. |
| `[Observed]` | Confirmed directly in the target repository, local build, or running system. Not used here unless a specific inspected artifact is named. |
| `[Recommendation]` | Engineering judgment consistent with official guidance, but not itself a published KDE rule. |
| `[Experimental]` | A proposal under evaluation. Never present it as approved. |
| `[Unknown]` | Not verified. State what evidence would resolve it. |

## 1. Choose the root by target, never by habit

The correct root element depends on what you are building. Inspect the target before editing; a copied root from another surface is the most common structural defect.

| Target | Root element | Basis |
| --- | --- | --- |
| Desktop widget, panel widget, tray item | `PlasmoidItem`; use `ContainmentItem` when the applet is itself a containment | `[Official]` Plasma 6 requires the plasmoid root to be `PlasmoidItem` (or `ContainmentItem`), the QML name for `AppletInterface` |
| Standalone Kirigami application | `Kirigami.ApplicationWindow`, with `pageStack.initialPage` set to a `Kirigami.Page` or subclass | `[Official]` |
| System Settings module (KCM) UI | One of `KCM.SimpleKCM`, `KCM.AbstractKCM`, `KCM.ScrollViewKCM`, `KCM.GridViewKCM` from `org.kde.kcmutils` | `[Official]` |
| Qt Widgets settings dialog in an existing widget application | `KConfigDialog`, with `KPageDialog` page/face types | `[Official]` |

Rules:

- Inspect first: `grep -rn "PlasmoidItem\|Kirigami.ApplicationWindow\|SimpleKCM\|KConfigDialog" <target>` and match the surrounding component. `[Recommendation]`
- A plasmoid's configuration page is a KCM page, not a child of `PlasmoidItem`. Its root must be one of the `org.kde.kcmutils` KCM components. `[Official]`
- Plasma 5 plasmoids used a plain `Item` root with representation properties on the `Plasmoid` attached object. In Plasma 6 the root is `PlasmoidItem`, and `compactRepresentation`, `fullRepresentation`, and `preferredRepresentation` are direct properties of that root. Do not port the old shape forward. `[Official]`
- Do not un-version or re-version QML imports by guesswork. Plasma 6 and Qt 6 imports are generally unversioned; the Plasma 6 porting guidance explicitly recommends dropping version numbers because they can cause bugs. `[Official]`

## 2. Plasmoid structure

```qml
import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasmoid
import org.kde.plasma.components as PlasmaComponents

PlasmoidItem {
    id: root

    toolTipMainText: i18n("Disk usage")
    toolTipSubText: i18np("%1 mounted volume", "%1 mounted volumes", root.volumeCount)
    preferredRepresentation: compactRepresentation

    compactRepresentation: PlasmaComponents.ToolButton {
        icon.name: "drive-harddisk"
        text: i18n("Disk usage")
        onClicked: Plasmoid.expanded = !Plasmoid.expanded
    }

    fullRepresentation: ColumnLayout {
        implicitWidth: Kirigami.Units.gridUnit * 20
        implicitHeight: Kirigami.Units.gridUnit * 12
        spacing: Kirigami.Units.smallSpacing
    }
}
```

- `[Official]` `PlasmoidItem` keeps `compactRepresentation`, `fullRepresentation`, `preferredRepresentation`, `switchWidth`, `switchHeight`, `activationTogglesExpanded`, the tooltip properties, `toolTipItem`, and `hideOnWindowDeactivate` as direct properties.
- `[Official]` Applet metadata that is not a representation concern stays on the `Plasmoid` attached object: `Plasmoid.title`, `Plasmoid.icon`, contextual actions, and most of the Plasma 5 applet API.
- `[Official]` Plasma 6 plasmoids require JSON metadata with `"X-Plasma-API-Minimum-Version": "6.0"`, and the entry point is fixed at `ui/main.qml`; remove `X-Plasma-MainScript` and `X-Plasma-API`.
- `[Recommendation]` Give the compact representation one obvious action and a translated tooltip. Do not make the compact representation the only place a setting can be reached.

Snippets in this file are illustrative. They assume surrounding properties and models exist; they are not drop-in production code.

## 3. Application structure

```qml
import QtQuick
import QtQuick.Controls as Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: appWindow
    title: i18n("Storage")

    pageStack.initialPage: Kirigami.ScrollablePage {
        title: i18n("Storage")

        ColumnLayout {
            spacing: Kirigami.Units.smallSpacing

            Controls.Label {
                Layout.fillWidth: true
                text: i18n("Mounted volumes")
                wrapMode: Text.WordWrap
            }
        }
    }
}
```

- `[Recommendation]` Use `Kirigami.Page` subclasses for navigation, and keep window-level chrome (title, actions) at the window or page level rather than rebuilding it per view.
- `[Official]` `Kirigami.ScrollablePage` is the standard scroll container for page content; do not nest your own `Flickable` unless the page has a central view that needs one.
- `[Recommendation]` Set `pageStack.initialPage` explicitly. An empty page stack renders an empty window and is not a loading state.

## 4. Theme integration

### 4.1 Colors

- `[Official]` Color every primitive through `Kirigami.Theme` attached properties, for example `Kirigami.Theme.backgroundColor`, `Kirigami.Theme.textColor`, `Kirigami.Theme.disabledTextColor`, `Kirigami.Theme.highlightColor`, `Kirigami.Theme.focusColor`, and `Kirigami.Theme.activeBackgroundColor`.
- `[Official]` Choose the color set by location: `Kirigami.Theme.colorSet` supports `View`, `Window`, `Button`, `Selection`, `Tooltip`, and `Complementary`. Window is the default.
- `[Official]` Color sets inherit down the item tree. Set `Kirigami.Theme.inherit: false` only when you deliberately force a different set for a subtree.
- `[Recommendation]` A literal color in window chrome, panels, popups, toolbars, or dialogs is a defect. Kirigami's own guidance says hardcoded colors should usually be avoided and never used in chrome areas.
- `[Recommendation]` If a content area genuinely needs a custom palette, define all roles in one place with `Kirigami.Theme.inherit: false`, and contrast-check the result with Kontrast. Partial custom palettes produce unreadable combinations in the other color scheme.
- `[Official]` `Kirigami.Theme.colorSet` replaces the Plasma 5 `PlasmaCore.ColorScope.colorGroup`, and `Kirigami.Theme.inherit` replaces `PlasmaCore.ColorScope.inherit`.

### 4.2 Metrics and typography

- `[Official]` Use `Kirigami.Units.gridUnit` as the base spatial unit. `Kirigami.Units.gridUnit` replaces `PlasmaCore.Units.mSize(font).height` and `PlasmaCore.Units.largeSpacing`.
- `[Official]` Spacing members verified in Kirigami 6.8.0 `units.h`: `smallSpacing`, `mediumSpacing`, `largeSpacing`, alongside `gridUnit`. Use them instead of literal pixel gaps.
- `[Recommendation]` Do not assume an older Plasma namespace member survived under Kirigami. Check the target branch's `Units` header before adding a name that is not listed here.
- `[Official]` Use `Kirigami.Theme.defaultFont` and `Kirigami.Theme.smallFont` rather than numeric point sizes. `smallFont` replaces `PlasmaCore.Theme.smallestFont`.
- `[Official]` Use `Kirigami.Heading` with `level` for section and page titles instead of manually sizing text.
- `[Recommendation]` Keep the type scale small and semantic: one page title, section headings, body, and a small role for secondary text. Do not introduce intermediate sizes to fix one screen.

### 4.3 Icons

- `[Official]` Set `icon.name` to a name from the installed icon theme; use `Kirigami.Icon` for standalone icons. `Kirigami.Icon` replaces `PlasmaCore.IconItem`.
- `[Recommendation]` Do not ship a bitmap or SVG where a standard icon name exists. A custom icon needs a reason (unique concept, brand mark) and must work on light and dark backgrounds.
- `[Official]` Directional icons must be mirrored for right-to-left layouts. KDE's Plasma 6 guidance shows flipping action icons such as media skip and navigation arrows based on `Qt.application.layoutDirection`.
- `[Recommendation]` Do not encode state in icon color alone; pair it with text, shape, or an accessible description.

## 5. Layout

- `[Official]` Use anchors for parent-relative placement and sizing (`anchors.fill`, `anchors.centerIn`), and Qt Quick Layouts (`ColumnLayout`, `RowLayout`, `GridLayout`) to distribute siblings.
- `[Recommendation]` Do not anchor children of a Layout. The Plasma widget guidance explicitly warns that anchors inside `ColumnLayout` cause undefined behavior. Use `Layout.fillWidth`, `Layout.fillHeight`, and alignment instead.
- `[Official]` Size children with `implicitWidth` / `implicitHeight`, and express constraints with `Layout.preferredWidth`, `Layout.minimumWidth`, `Layout.maximumWidth`. Items default to zero size outside a layout.
- `[Official]` `Layout.*` attached properties have no effect unless the item's parent is a Qt Quick Layout. A representation root directly inside `PlasmoidItem` is not in a layout: set its `implicitWidth`/`implicitHeight` or wrap the content in a Layout instead of expecting `Layout.preferredWidth` to size it.
- `[Recommendation]` Position every sibling explicitly with anchors, a positioner, or a Layout. Siblings that declare only `width`/`height` share the parent's origin and overlap; confirm placement in a rendered capture, not from the source alone.
- `[Recommendation]` Keep one spacing rhythm per surface: derive padding and gaps from `gridUnit` or the named `Kirigami.Units` spacing values. Mixed arbitrary margins read as misalignment even when each value looks reasonable alone.
- `[Official]` Mirror layouts for right-to-left languages with `LayoutMirroring.enabled: Qt.application.layoutDirection === Qt.RightToLeft`, and set `LayoutMirroring.childrenInherit: true` when the whole subtree should mirror.
- `[Official]` Text wraps with `wrapMode` (`Text.Wrap`, `Text.WordWrap`) and truncates with `elide` (`Text.ElideRight`, `Text.ElideMiddle`). Use `maximumLineCount` where a row must stay one line.
- `[Recommendation]` Never clip a label silently. If text must truncate, provide the full value through a tooltip or accessible description, and verify the layout at the largest supported font size.
- `[Recommendation]` Interactive targets should be at least 24×24 px at the current scale, larger (44×44) where the surface is touch-capable. `Kirigami.Units.gridUnit` defaults to 18 px, so one `gridUnit` alone does not meet that minimum; derive the target from the scale factor and verify it at more than 100%.

## 6. State and motion

- `[Recommendation]` Express visual states declaratively with `states` and `Transition`, and keep the state list small and named after user-visible conditions (`hovered`, `expanded`, `error`). Avoid imperative property writes that fight bindings.
- `[Recommendation]` Bound animation duration to the named duration constants in `Kirigami.Units` (`veryShortDuration`, `shortDuration`, `longDuration`, `veryLongDuration`). Do not hand-pick milliseconds per component; inconsistent durations make unrelated surfaces feel unrelated.
- `[Observed]` Kirigami 6.8.0 `units.h` describes those duration constants as the animation-duration choices and notes that they are scaled according to animation settings, unlike `humanMoment`, which is deliberately not an animation duration. Using the constants therefore honors the system preference.
- `[Recommendation]` Animate only to explain a change of position, hierarchy, or state. No looping decorative motion, no bounce, no animation that delays access to content.
- `[Official]` When animations are disabled system-wide, every animated element must either transition instantly or show a static image; blinking is limited to the text insertion point. Verify this by disabling animations and repeating the flow.
- `[Recommendation]` Never let animation be the only signal that something changed. Pair it with a text, icon, or focus change that survives reduced motion.

## 7. Localization

- `[Official]` Wrap user-visible strings in `i18n("...")` with double quotes. The extraction tool ignores single-quoted calls.
- `[Official]` Use placeholders (`%1`, `%2`) for interpolation: `i18n("%1 unread emails", count)`. Never build a sentence by concatenating translated fragments; word order differs by language.
- `[Official]` Use `i18np` for plurals: `i18np("%1 unread email", "%1 unread emails", count)`. Singular and plural forms cannot be derived by appending a suffix.
- `[Official]` Use `i18nc` with a context comment when a short string is ambiguous (`i18nc("Play previous track", "Previous")`), so translators can disambiguate it.
- `[Official]` Use `xi18n` when the string contains rich text markup, and `i18nd` only to deliberately reuse another translation domain.
- `[Recommendation]` Translate every user-visible string, including accessible names, tooltips, empty states, error messages, and window titles. A translated label with an untranslated accessible name fails screen-reader users in that locale.
- `[Recommendation]` Format numbers, dates, sizes, and durations with `QLocale` conventions rather than hardcoded separators or unit spellings. Keep technical identifiers untranslated.
- `[Recommendation]` Test at least one long translation (for example German) and one right-to-left locale. Layout defects from localization are cheaper to catch than to retrofit.

## 8. Component selection and reuse

| Need | First choice | Notes |
| --- | --- | --- |
| Standard input, button, menu, dialog control | Qt Quick Controls (`import QtQuick.Controls`) | Follows the active style; do not restyle its internals for cosmetics |
| Page, card, form layout, heading, standard icon, prompt dialog | Kirigami | Provides KDE layout conventions and theme integration |
| Plasmoid chrome and containers | Plasma components (`org.kde.plasma.components`, `org.kde.plasma.extras`) | Use the unversioned Plasma 6 imports; verify types in the target branch |
| Settings dialog in an existing Qt Widgets application | `KConfigDialog` / `KPageDialog` | Correct for widget apps; not the recommended path for new KCMs |
| New System Settings module | `org.kde.kcmutils` KCM root plus Kirigami content | QML KCMs are the documented path for Plasma |

- `[Official]` New KCMs should be built with QML and Kirigami. Legacy Qt Widgets KCMs are not recommended for new work and cannot be loaded by `plasma-settings`.
- `[Recommendation]` Prefer the highest-level component that already implements the behavior: Kirigami before Qt Quick Controls before a custom composite. Reuse prevents drift in focus, hover, and disabled behavior.
- `[Recommendation]` Custom controls are allowed only with a documented limitation. Record: which standard control was evaluated, the concrete gap (with `file:line` or screenshot), the keyboard model, the accessible role and name, the theme roles used, and who maintains it. No documented limitation means use the standard control.
- `[Recommendation]` Do not fork a standard control to change spacing or color. Theme roles and `Kirigami.Units` exist for that; a fork silently loses upstream accessibility and style fixes.

## 9. System Settings (KCM) integration

- `[Official]` The QML root must be `SimpleKCM` for arbitrary form/column content, `ScrollViewKCM` for a central scrollable view, `GridViewKCM` for a grid, or `AbstractKCM` when you need to control the scroll container yourself.
- `[Official]` The C++ backend derives from `KQuickConfigModule`, is built with `kcmutils_add_qml_kcm`, and declares its buttons in the constructor (for example `setButtons(Help | Apply | Default)`).
- `[Official]` For KConfigXT-managed settings, derive from `KQuickManagedConfigModule` instead and expose a settings object generated from the `*.kcfg`/`*.kcfgc` pair as a constant property. The base class discovers it and maintains `saveNeeded` and `defaults`; do not manage those properties yourself.
- `[Official]` Export the C++ module with `K_PLUGIN_FACTORY_WITH_JSON` pointing at the metadata JSON, and register the QML module through `kcmutils_add_qml_kcm()`.
- `[Recommendation]` State the apply model: instant-apply commits each change, while Apply/Reset keeps pending values and restores them on Reset. Do not mix both; neither model requires an application restart.
- `[Official]` Module metadata in the JSON file uses `Name`, `Description`, `Icon`, `FormFactors`, `X-KDE-Keywords`, and `X-KDE-System-Settings-Parent-Category`.
- `[Recommendation]` Build forms with `Kirigami.FormLayout` and `Kirigami.FormData.label` so labels, controls, and grouping match other modules. Do not hand-place label/control pairs with anchors.
- `[Recommendation]` Test the module standalone with `kcmshell6 <module-name>` before testing it inside System Settings; this isolates loading errors from navigation errors.
- `[Recommendation]` The Plasma 5 type was `KQuickAddons.ConfigModule`. It is not evidence for the KF6 API name. Check the target branch and the KF6 KCM porting guidance before reusing an old snippet.

## 10. Qt Widgets configuration dialogs

- `[Official]` `KConfigDialog` creates the dialog, manages the Apply/Defaults/Cancel button state, restores and saves settings, and deletes pages. Widget names must correspond to configuration entries with a `kcfg_` prefix (for example `kcfg_MyOption` for `MyOption`).
- `[Official]` `KPageDialog` provides the page/face model; `setFaceType(KPageDialog::List)` is the common settings shape.
- `[Recommendation]` Use this path only in an existing Qt Widgets application. Mixing Qt Widgets and QML in one settings surface adds two styling and accessibility stacks for no user benefit.
- `[Recommendation]` Keep page titles short and stable; they are navigation labels, not descriptions.

## 11. Cross-skill boundary

This file defines what the interface should be. Binding preservation, delegate efficiency, `Loader` use, object lifetime, threading, and profiling belong to the companion engineering skill: [`../../kde-plasma-best-practices/SKILL.md`](../../kde-plasma-best-practices/SKILL.md).

- `[Recommendation]` When a visual requirement and an engineering constraint conflict, record both, choose with evidence, and state which one was traded away. Neither skill silently overrides the target repository's requirements.

## Sources

- KDE Human Interface Guidelines: https://develop.kde.org/hig/ (Accessed: 2026-10-20)
- KDE HIG, Accessibility and inclusiveness: https://develop.kde.org/hig/accessibility/ (Accessed: 2026-10-20)
- KDE HIG, Text and labels: https://develop.kde.org/hig/text_and_labels/ (Accessed: 2026-10-20)
- Kirigami tutorial, Colors and themes: https://develop.kde.org/docs/getting-started/kirigami/style-colors/ (Accessed: 2026-10-20)
- Kirigami tutorial, Typography: https://develop.kde.org/docs/getting-started/kirigami/style-typography/ (Accessed: 2026-10-20)
- Kirigami tutorial, Scrollable pages and list views: https://develop.kde.org/docs/getting-started/kirigami/components-scrollablepages_listviews/ (Accessed: 2026-10-20)
- Kirigami API, Theme attached property: https://api.kde.org/qml-org-kde-kirigami-platform-theme.html (Accessed: 2026-10-20)
- Kirigami API index: https://api.kde.org/kirigami-index.html (Accessed: 2026-10-20)
- Kirigami 6.8.0 `units.h` source (spacing and duration members): https://invent.kde.org/frameworks/kirigami/-/raw/v6.8.0/src/platform/units.h (Accessed: 2026-10-20)
- Plasma widget tutorial, QML: https://develop.kde.org/docs/plasma/widget/qml/ (Accessed: 2026-10-20)
- Porting Plasmoids to KF6: https://develop.kde.org/docs/plasma/widget/porting_kf6/ (Accessed: 2026-10-20)
- Plasma widget tutorial, Translations / i18n: https://develop.kde.org/docs/plasma/widget/translations-i18n/ (Accessed: 2026-10-20)
- Ki18n programmer's guide: https://invent.kde.org/frameworks/ki18n/-/blob/master/docs/programmers-guide.md (Accessed: 2026-10-20)
- Settings module (KCM) development: https://develop.kde.org/docs/features/configuration/kcm/ (Accessed: 2026-10-20)
- KDE Frameworks 6 porting guide for KCMs: https://develop.kde.org/docs/features/configuration/porting_kf6/ (Accessed: 2026-10-20)
- KConfigDialog: https://develop.kde.org/docs/features/configuration/configdialog/ (Accessed: 2026-10-20)
- KQuickConfigModule API: https://api.kde.org/kquickconfigmodule.html (Accessed: 2026-10-20)
- KCMUtils SimpleKCM API: https://api.kde.org/qml-org-kde-kcmutils-simplekcm.html (Accessed: 2026-10-20)
- KPageDialog API: https://api.kde.org/kpagedialog.html (Accessed: 2026-10-20)
- KConfigDialog API: https://api.kde.org/kconfigdialog.html (Accessed: 2026-10-20)
- Qt QML coding conventions: https://doc.qt.io/qt-6/qml-codingconventions.html (Accessed: 2026-10-20)
- Qt Quick positioning and layouts: https://doc.qt.io/qt-6/qtquick-positioning-topic.html (Accessed: 2026-10-20)
- Qt Quick Layouts: https://doc.qt.io/qt-6/qtquick-positioning-layouts.html (Accessed: 2026-10-20)
- Qt Quick Text: https://doc.qt.io/qt-6/qml-qtquick-text.html (Accessed: 2026-10-20)
- Qt Quick LayoutMirroring: https://doc.qt.io/qt-6/qml-qtquick-layoutmirroring.html (Accessed: 2026-10-20)
- Qt Quick states and transitions: https://doc.qt.io/qt-6/qtquick-statesanimations-states.html (Accessed: 2026-10-20)
- Qt Quick Transition: https://doc.qt.io/qt-6/qml-qtquick-transition.html (Accessed: 2026-10-20)
- Qt Quick Behavior: https://doc.qt.io/qt-6/qml-qtquick-behavior.html (Accessed: 2026-10-20)
- Qt Quick Controls QML types: https://doc.qt.io/qt-6/qtquick-controls-qmlmodule.html (Accessed: 2026-10-20)
- Qt Quick accessibility: https://doc.qt.io/qt-6/qml-qtquick-accessible.html (Accessed: 2026-10-20)
- Qt accessibility overview: https://doc.qt.io/qt-6/accessible.html (Accessed: 2026-10-20)
- Qt.application layoutDirection: https://doc.qt.io/qt-6/qml-qtqml-qt.html (Accessed: 2026-10-20)

## Version notes

- Authoring baseline: Plasma 6.8.0, Qt 6.11.1, KF6, verified 2026-10-20.
- Plasma 5 names that must not be carried forward unverified: `PlasmaCore.ColorScope`, `PlasmaCore.Theme.smallestFont`, `PlasmaCore.IconItem`, `PlasmaCore.Units.mSize`, `KQuickAddons.ConfigModule`, and a plain `Item` plasmoid root.
- `Kirigami.Units` spacing (`gridUnit`, `smallSpacing`, `mediumSpacing`, `largeSpacing`) and duration (`veryShortDuration`, `shortDuration`, `longDuration`, `veryLongDuration`) members were verified in the Kirigami 6.8.0 `units.h` source on 2026-10-20. Other members still require a target-branch check.
- Plasma 6 requires JSON metadata for plasmoids and fixes the entry point at `ui/main.qml`; a Plasma 5 `.desktop` metadata file is not a valid baseline.
