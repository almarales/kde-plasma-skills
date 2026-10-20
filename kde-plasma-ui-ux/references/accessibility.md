# Accessibility

## Scope

Use this reference as a design and verification requirement for Plasma widgets, KCMs, and KDE applications. Accessibility is a foundational property of the interface, not a final polish phase. It covers keyboard operation, focus, Qt accessibility semantics, screen readers, contrast, scaling, color-independent status, motion, touch targets, and localization. Visual roles are covered in `visual-consistency.md`; interaction behavior in `interaction-patterns.md`.

## Foundational rule

- [Recommendation] Accessibility requirements are inputs to the first design draft. A layout that only works at the default font size, a control with no accessible name, or an interaction that requires hover is structurally incomplete.
- [Official] The HIG states that following its guidance produces an app that is "already quite accessible" and still requires testing against impairments the author may not have.
- [Recommendation] Do not accept "we will add accessibility later" as a plan. Retrospective fixes usually change layout, focus order, and component choice.

## Keyboard-only operation

- [Official] The HIG instructs authors to unplug the mouse or disable the touchpad and interact with every element using only the keyboard.
- [Recommendation] Every action available by pointer must be available by keyboard, including context menus, drag alternatives, and dismissing transient UI.
- [Recommendation] Provide a visible, documented path for Tab/Shift+Tab traversal, arrow-key navigation inside composite widgets, Enter/Space activation, and Escape dismissal.
- [Recommendation] Do not create keyboard traps. A modal surface may contain focus deliberately, but it must offer Escape and restore focus on close.
- [Official] Order names so the distinctive part comes first, which also makes keyboard selection faster — for example "Germany (Europe)" rather than "Europe/Germany".

## Focus

- [Official] The item with default focus must make sense for the task.
- [Official] The focused item must look visibly different from selected items in inactive views.
- [Recommendation] Focus must remain visible against every color scheme and on top of every surface, including popups and overlays.
- [Recommendation] Do not move focus without a user action. When content appears asynchronously, announce it instead of stealing focus.
- [Recommendation] Focus indicators need non-text contrast against adjacent colors; a subtle tint is not sufficient.

## Qt accessibility semantics

- [Official] Qt Quick items expose accessibility through the `Accessible` attached type. Its most important properties are `name`, `description`, and `role`.
- [Official] `Accessible.name` is the short, concise label announced for the control and should reflect visible text. `Accessible.description` adds context that is not already in the name. `Accessible.role` identifies the type of control.
- [Official] Interactive items also expose state such as `focusable`, `checked`, `checkable`, `pressed`, `selected`, `disabled`, `readOnly`, and `passwordEdit`, plus action signals such as `pressAction`, `toggleAction`, and increment/decrement actions.
- [Recommendation] Set `Accessible.name` explicitly when a control has no visible text, when it is icon-only, or when the visible text is ambiguous out of context.
- [Recommendation] Do not override `role` on a standard control that already reports the correct role; verify the reported role instead.
- [Recommendation] Keep `description` supplementary. Do not duplicate the name, and do not put required instructions only in the description.
- [Official] `Accessible.announce(message, politeness)` exists since Qt 6.8 for dynamic announcements. Verify availability for the target Qt version before use.
- [Official] `Accessible.labelledBy` and `Accessible.labelFor` exist since Qt 6.10 for associating labels and controls. Verify availability for the target Qt version.
- [Official] For Qt Widgets and custom C++ widgets, Qt provides the `QAccessible` class and `QAccessibleInterface` for exposing accessibility information. [Recommendation] Native widgets already implement much of this; custom-painted widgets may need an interface.
- [Recommendation] When a custom item changes state without a standard property change, emit an accessibility update so assistive technology notices.

## Screen readers

- [Official] The KDE HIG instructs authors to turn off the screen and use the app with the Orca screen reader, the screen reader it references for Plasma testing. It should announce something intelligible and distinct for all elements.
- [Official] For GUI elements, Orca should announce the label and type, for example "File, Menu" or "Create New Folder, Button".
- [Official] Tooltip text must be read by the screen reader through the `Accessible` attached properties.
- [Official] No label should be used more than once in the same window.
- [Recommendation] Test at least: window and page titles, every button and menu item, icon-only actions, form fields and their errors, list and grid items, tab or page navigation, dialogs, and dynamic status messages.
- [Recommendation] Confirm that a state change is announced once, not repeatedly on every repaint.
- [Recommendation] Test the widget both standalone and in its real host (panel, tray, or System Settings), because the host can change the accessibility tree.

## Contrast

- [Official] Kirigami guidance asks authors to ensure colors have good contrast and are WCAG compliant.
- [Recommendation] Use these as the review baseline, not as a KDE mandate: 4.5:1 for normal text, 3:1 for large text, and 3:1 for UI components and graphical objects needed to understand the interface, per WCAG 2.2 AA.
- [Recommendation] Measure the rendered foreground/background pair, including custom color schemes, accent colors, translucency, and disabled states.
- [Recommendation] Do not treat low opacity as sufficient to communicate disabled state; the result may be unreadable.
- [Recommendation] Focus rings, selection backgrounds, error outlines, and chart series need non-text contrast as well.

## Text and display scaling

- [Official] The HIG instructs authors to increase the system-wide font size to 14 and verify that visual relationships are preserved and text is not cut off.
- [Official] Qt supports scalable interfaces and, by default, widgets and controls use the fonts and font sizes configured by the operating system.
- [Recommendation] Test at the default size, at 14 pt, and at a substantially larger size. Also test 100%, 125%, 150%, and 200% display scaling where available.
- [Recommendation] Avoid fixed heights for text containers, absolute positioning of labels, and single-line assumptions for translatable text.
- [Recommendation] Icons and controls must scale with the interface; do not ship a single raster size for critical iconography.
- [Recommendation] Verify that popups, panels, and dialogs remain usable when their content grows beyond the initial size.

## Color-independent status

- [Official] The HIG states that color must not be the only means of conveying meaning or inviting action; use icons, shapes, or text as well.
- [Recommendation] Error, warning, success, selection, and busy states each need a non-color signal: an icon, a label, a pattern, or a positional cue.
- [Recommendation] Test with a monochrome or high-contrast scheme and with a color-vision simulation. Status must remain distinguishable.
- [Recommendation] Do not use red/green as the only distinction between destructive and safe actions.

## Reduced motion

- [Official] When animations are globally disabled, animated elements must transition instantly or show a static image, such as a static loading spinner.
- [Official] Avoid blinking UI elements.
- [Official] Plasma's `BusyIndicator` does not rotate when the system animation speed is Instant.
- [Recommendation] Respect the platform setting rather than adding an app-level motion toggle.
- [Recommendation] Do not use animation as the only indication that content changed or that a task completed.

## Touch targets

- [Recommendation] Target at least 24×24 px (the CSS-pixel equivalent at the current scale factor) for pointer targets, and prefer 44×44 for touch, following WCAG 2.2 Target Size (Minimum) and Target Size (Enhanced). These are external accessibility recommendations, not a KDE requirement.
- [Recommendation] Keep spacing between adjacent targets so that a near miss does not trigger the wrong action.
- [Recommendation] Panel and tray items are constrained by the host; verify that the effective hit area still meets the target and that the compact representation is not the only interactive region.
- [Recommendation] Touch targets apply to icon-only buttons, close buttons, list-item trailing actions, and drag handles.

## Localization and RTL

- [Official] The HIG instructs authors to test right-to-left mode, for example with `LANGUAGE=ar_AR`, and confirm that layout reverses and there is enough room for translated text.
- [Official] Use `-rtl` icon variants for directional icons and do not mirror images.
- [Official] Handle plurals through the translation system, because plural rules differ by language.
- [Recommendation] Never concatenate translated fragments. Use complete strings with placeholders and translator context.
- [Recommendation] Avoid text in images, fixed-width labels, and abbreviations that only make sense in English.
- [Recommendation] Check that accessible names are translated too; they are user-facing text.

## Verification checklist

1. Primary task completed with the pointer disabled.
2. Focus order matches reading order; focus is visible in light and dark schemes.
3. Every icon-only control has an accessible name and a tooltip.
4. Every custom interactive item reports a correct role and state.
5. Orca announces label plus type for every control; no duplicate labels in a window.
6. Contrast measured for text, focus, boundaries, and status in three color schemes.
7. Layout survives 14 pt text and 200% scaling.
8. Status is distinguishable without color.
9. Animations respect the system setting; no blinking.
10. Touch targets meet the chosen minimum in panel, tray, and dialog contexts.
11. RTL layout and directional icons verified.
12. Accessible names and messages are translated.

## Sources

- Accessibility and inclusiveness — https://develop.kde.org/hig/accessibility/ — Accessed: 2026-10-20
- Text and labels — https://develop.kde.org/hig/text_and_labels/ — Accessed: 2026-10-20
- Layout and navigation (RTL) — https://develop.kde.org/hig/layout_and_nav/ — Accessed: 2026-10-20
- Communicating status changes (color independence) — https://develop.kde.org/hig/status_changes/ — Accessed: 2026-10-20
- Qt Quick `Accessible` type — https://doc.qt.io/qt-6/qml-qtquick-accessible.html — Accessed: 2026-10-20
- Qt accessibility overview — https://doc.qt.io/qt-6/accessible.html — Accessed: 2026-10-20
- Qt `QAccessible` class — https://doc.qt.io/qt-6/qaccessible.html — Accessed: 2026-10-20
- Qt high-DPI scaling — https://doc.qt.io/qt-6/highdpi.html — Accessed: 2026-10-20
- WCAG 2.2 contrast minimum — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — Accessed: 2026-10-20
- WCAG 2.2 non-text contrast — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — Accessed: 2026-10-20
- WCAG 2.2 target size minimum — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — Accessed: 2026-10-20

## Version notes

Verified against KDE HIG and Qt documentation as published on 2026-10-20, with a local baseline of Plasma 6.8.0, Qt 6.11.1, and KF6.

- [Official] `Accessible.announce` is documented as since Qt 6.8 and `Accessible.labelledBy`/`labelFor` as since Qt 6.10. The target baseline includes both, but older deployments may not.
- [Recommendation] The Qt documentation site defaults to the newest release. Select the target Qt version before copying API details.
- [Recommendation] WCAG 2.2 AA numbers are a review baseline. A project may adopt stricter targets or a different conformance level.
