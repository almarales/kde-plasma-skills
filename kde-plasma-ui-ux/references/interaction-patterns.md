# Interaction Patterns

## Scope

Use this reference for behavior that visual review cannot catch: keyboard paths, focus order, shortcuts, menus, drag and drop, hover versus touch, dialogs, feedback, notifications, undo, configuration, empty/loading/error states, RTL, reduced motion, and localization. It applies to Plasma widgets, KCMs, and KDE applications. Visual treatment is covered in `visual-consistency.md`; accessibility verification in `accessibility.md`.

## Keyboard navigation and focus order

- [Official] The HIG requires that every UI element be usable with the keyboard alone. Test by disabling the pointer.
- [Official] Default focus must make sense, and the focused item must look visibly different from a selected item in an inactive view.
- [Official] Layout order communicates reading order: in left-to-right languages the top-leading item is encountered first, and the bottom-trailing item is perceived as last.
- [Recommendation] Tab order should follow visual reading order and task order, not object-creation order.
- [Recommendation] Define keys per control type: Tab/Shift+Tab for traversal, arrows within lists and grids, Enter or Space for activation, Escape to dismiss, and the Menu key for context menus.
- [Recommendation] Never create a keyboard trap except in a deliberate modal dialog, and always provide Escape.
- [Recommendation] When a popup or dialog closes, return focus to the control that opened it.
- [Recommendation] Do not use focus as the only way to reveal essential information.

## Shortcuts

- [Official] The HIG treats shortcuts as accelerators: never rely exclusively on keyboard shortcuts or context menus to access functionality. Primary workflows must be visible.
- [Official] Assign a shortcut to every action that can have one, or at least make shortcuts user-assignable.
- [Official] Use `KStandardShortcut` for standard actions rather than inventing bindings.
- [Official] Set shortcuts with modifier and alphanumeric keys; the HIG warns against a bare function key because laptop keyboards may make it hard to reach.
- [Recommendation] Display shortcuts consistently in menus and tooltips, and do not reassign a standard shortcut to a different meaning.
- [Recommendation] Check for conflicts with the desktop, the widget host, and common assistive tools.

## Context menus

- [Recommendation] Open context menus from right-click and from the keyboard Menu key.
- [Official] Context menus are accelerators, not the only route to important actions.
- [Recommendation] Group by task, keep the list short, use standard actions where they exist, and separate destructive actions at the end.
- [Recommendation] Do not hide the only copy of an action in a context menu. Surface it in the toolbar, header, or main view.
- [Recommendation] Preserve the target: a context menu must act on the item the user invoked it on, with that item visibly identified.

## Drag and drop

- [Official] The HIG requires every drag-and-drop to show a preview of the dragged item and either succeed or show the "can't drag here" cursor.
- [Recommendation] Provide a non-drag alternative for every drag operation: move up/down, cut/paste, or an explicit action.
- [Recommendation] Make valid drop targets visible during the drag, and do not rely on the cursor alone for meaning.
- [Recommendation] Define what happens on cancel, on drop outside a target, and on multi-item selection.
- [Recommendation] Test drag and drop with keyboard alternatives, because pointer dragging excludes keyboard-only users.

## Hover versus touch

- [Official] Important text must not be visible only in a hover tooltip.
- [Official] Hover tooltips should also appear on press-and-hold for touch.
- [Official] For touchpads and touchscreens, implement only two-finger gestures in apps.
- [Recommendation] Treat hover as enhancement. Every hover-revealed control needs a persistent or keyboard-reachable alternative.
- [Recommendation] Do not place primary actions in controls that appear only on hover.
- [Recommendation] Size interactive targets for touch where the product runs on touch devices, and keep hover-only affordances out of critical paths.

## Dialogs and popups

- [Official] The HIG distinguishes: push a page when content fills the window, use `Kirigami.OverlaySheet` for auxiliary read-only narrow content, and use a dialog for a focused decision.
- [Recommendation] Use modal dialogs only when the user must decide before continuing. Prefer inline messages, sheets, or pages otherwise.
- [Recommendation] Define initial focus, the default action, Escape behavior, and focus return.
- [Recommendation] Do not nest popups or open a dialog from a dialog unless the task genuinely requires it.
- [Recommendation] Keep destructive confirmations specific: name the object and the consequence, and use an action label that states the effect.

## Status and feedback

- [Official] Minimize unnecessary status messages. Indicate success by changing something related to the completed task, not by announcing "Task completed".
- [Official] Long-running tasks are the exception: keep progress visible for work the user may have forgotten.
- [Official] Prefer preventing errors: accept structured input, validate before entry, and recover automatically where possible.
- [Official] Error messages must be actionable and in plain language, stating what happened and what the user can do. Never use technical gibberish or silent failure.
- [Official] Do not rely on color alone to convey meaning or invite action; also use icons, shapes, or text.
- [Recommendation] Choose the lightest feedback channel that fits: inline validation for fields, inline message for page-level state, passive notification for transient confirmation, dialog only for blocking decisions.

## Notifications

- [Official] Avoid sending system notifications while the app's main window is in the foreground; use in-app feedback instead.
- [Official] Keep notifications and undo actions non-modal and dismissable.
- [Official] `showPassiveNotification` disappears after a few seconds and suits cases where losing the undo option is not catastrophic; `Kirigami.InlineMessage` does not disappear automatically.
- [Recommendation] Make notifications actionable and specific. Do not notify about routine success.
- [Recommendation] Never make a notification the only record of an error or the only path to recovery.

## Undo

- [Official] Offer undo for every action that removes content not trivial to re-add.
- [Official] Move files to the trash instead of deleting immediately.
- [Official] For cases requiring immediate deletion, use deferred deletion that postpones the underlying delete operation.
- [Recommendation] Prefer undo over confirmation dialogs for reversible actions; reserve confirmation for irreversible or high-consequence operations.
- [Recommendation] Keep the undo affordance available long enough to be useful, and state exactly what will be restored.
- [Recommendation] When undo expires, do not silently discard the record if the action was destructive and irreversible; provide a durable recovery path.

## Configuration semantics

- [Official] The primary purpose of settings is to support different valid workflows, not to toggle features on and off.
- [Official] Settings that merely enable or disable a feature are a warning sign of sloppy design.
- [Official] Apply saved settings immediately; do not require relaunching the app.
- [Recommendation] Distinguish instant-apply controls (switch) from controls applied on OK/Apply (checkbox), and never change a control's label or icon when its state changes.
- [Recommendation] Provide defaults and a reset path for every setting, and show the effect of a change where the user can observe it.
- [Recommendation] Do not use customization to work around a design decision or a bug.

## Empty, loading, and error states

- [Official] Use `Kirigami.PlaceholderMessage` for empty views, with an icon, explanation, and ideally a helpful action.
- [Recommendation] Empty states should say what the surface is for and offer the next step. A blank panel with no explanation is a defect.
- [Recommendation] Loading states should preserve layout, avoid indefinite spinners for known durations, and respect the system animation setting.
- [Recommendation] Error states should be local to the failure where possible, name the failed object or action, and offer retry, recovery, or a route to support.
- [Recommendation] Distinguish "empty because there is no data" from "empty because loading failed".

## RTL and localization

- [Official] Layouts reverse automatically for items using anchors and layouts; users of right-to-left languages expect this.
- [Official] Use the reversed icon variants suffixed with `-rtl` for icons that indicate directionality; do not mirror images.
- [Official] Test in right-to-left mode, for example by running with `LANGUAGE=ar_AR`.
- [Recommendation] Never concatenate translated fragments; use complete translatable strings with placeholders.
- [Official] Handle plurals through the translation system, because plural rules differ by language.
- [Recommendation] Avoid fixed widths and heights that assume English text length, and allow labels to wrap or elide with a tooltip.
- [Recommendation] Do not embed text in images or icons.

## Reduced motion

- [Official] When animations are globally disabled, animated UI must transition instantly or show a static image, such as a static loading spinner.
- [Official] Avoid blinking UI elements.
- [Official] Plasma's `BusyIndicator` does not rotate when animation speed is Instant.
- [Recommendation] Respect the platform animation setting rather than adding an app-specific toggle.
- [Recommendation] Never use motion as the only signal that something changed.

## Verification pass

1. Complete the primary task with the pointer disabled.
2. Complete it with only left-clicks and the on-screen keyboard.
3. Open every menu from the keyboard.
4. Tab through every surface; confirm focus order and visible focus.
5. Trigger every drag-and-drop; confirm preview, success, and rejection feedback.
6. Disable animations; confirm instant or static transitions.
7. Switch to a right-to-left language; confirm layout and directional icons.
8. Increase the system font size; confirm no clipping.
9. Trigger empty, loading, error, and offline states.
10. Confirm undo works and remains available for a useful interval.

## Sources

- Accessibility and inclusiveness — https://develop.kde.org/hig/accessibility/ — Accessed: 2026-10-20
- Layout and navigation — https://develop.kde.org/hig/layout_and_nav/ — Accessed: 2026-10-20
- Displaying content — https://develop.kde.org/hig/displaying_content/ — Accessed: 2026-10-20
- Getting input — https://develop.kde.org/hig/getting_input/ — Accessed: 2026-10-20
- Communicating status changes — https://develop.kde.org/hig/status_changes/ — Accessed: 2026-10-20
- Simple by default — https://develop.kde.org/hig/simple_by_default/ — Accessed: 2026-10-20
- Powerful when needed — https://develop.kde.org/hig/powerful_when_needed/ — Accessed: 2026-10-20
- Text and labels — https://develop.kde.org/hig/text_and_labels/ — Accessed: 2026-10-20
- Plasma's QML API (BusyIndicator) — https://develop.kde.org/docs/plasma/widget/plasma-qml-api/ — Accessed: 2026-10-20

## Version notes

Verified against KDE HIG and Plasma documentation as published on 2026-10-20, with a local baseline of Plasma 6.8.0, Qt 6.11.1, and KF6.

- [Recommendation] Key bindings and standard shortcuts can change across Plasma and KF releases. Verify `KStandardShortcut` names for the target version.
- [Unknown] Behavior of hover on hybrid touch devices depends on the compositor and input stack; test on the actual target hardware rather than assuming desktop behavior.
