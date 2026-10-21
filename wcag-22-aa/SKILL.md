---
name: wcag-22-aa
description: Build and review UI that conforms to WCAG 2.2 Level AA from the first line of code, on web (any framework or design system) and native mobile (iOS, Android, React Native, Flutter). Use for any work that creates, changes or reviews user-facing UI, components, forms, styles, design tokens, navigation, media or authentication flows, and whenever ARIA, accessibility, a11y, WCAG or screen readers come up.
---

# WCAG 2.2 AA by default

Every piece of UI produced with this skill must conform to WCAG 2.2 Level A and AA
(55 success criteria; 4.1.1 Parsing was removed in 2.2). Accessibility is part of
"done", not a later pass. This skill is design-agnostic: it never dictates brand,
layout or visual style, only the constraints any design must satisfy.

## Reference files — load only what the task needs

| File | Open it when |
|---|---|
| `references/component-patterns.md` | Building or changing any component (buttons, forms, dialogs, tabs, menus, combobox, tables, carousels, toasts, drag-and-drop, auth, multi-step flows, SPA routing, media) |
| `references/tables.md` | Building or reviewing any table, data grid, treegrid, tabular list, sortable/filterable/paginated data, or a third-party grid library (web and mobile) |
| `references/aria.md` | Writing or reviewing ANY `role`, `aria-*` attribute, `tabindex`, `inert`, or a custom widget |
| `references/design-tokens.md` | Touching colors, focus styles, typography, spacing, sizing, motion, breakpoints, or a design system / theme |
| `references/mobile.md` | Working on iOS (UIKit/SwiftUI), Android (Views/Compose), React Native, Flutter, or a webview |
| `references/success-criteria.md` | Mapping work to specific SC numbers, writing a review, or when unsure what a criterion requires |
| `references/testing.md` | Writing tests, setting up CI checks, or producing the verification report |
| `scripts/contrast.py` | Checking any color pair or token set (`python3 scripts/contrast.py "#767676" "#ffffff"`) |

## Workflow

### 1. Before writing UI
- List the component types and user flows involved; open the matching sections of
  `component-patterns.md` (and `mobile.md` for native).
- For each component, decide **native or custom** under rule 1 below before writing any
  markup. If custom, write the justification first — it goes into the Accessibility notes.
- If design tokens or mockups are provided, check them with `scripts/contrast.py`
  and the rules in `design-tokens.md` before building.

### 2. While writing — non-negotiables
1. **Native controls first — custom controls must earn their place.** Use the native
   HTML element or platform control whenever one exists for the job: `<button>`,
   `<a href>`, `<input>` (all types), `<select>`, `<textarea>`, `<fieldset>`/`<legend>`,
   `<dialog>`, `<details>`/`<summary>`, `<table>`, `<progress>`, `<input type="range">`;
   on mobile, the platform's own buttons, switches, pickers, sliders and text fields
   (`mobile.md` §0). Native controls provide name, role, state, keyboard and focus
   behavior for free; custom controls must rebuild all of it.
   A custom control (a hand-built widget, a `div`/`span` with a role or click handler,
   or a gesture-detector on mobile) is allowed only when:
   - **no native element exists** for the pattern (tabs, tree, menu button, carousel,
     toolbar, combobox with async search, drag-and-drop), **or**
   - a **documented product requirement** cannot be met by the native control even after
     styling it.
   Appearance alone is **not** a valid reason — native controls can be styled
   (`appearance: none`, `accent-color`, custom checkbox/radio visuals over a real input,
   themed platform controls). "Our component library renders divs" is not a reason
   either; fix or wrap the library component.
   When a custom control is used, all three are mandatory:
   a. **Justification** — one or two sentences stating which condition above applies,
      included under "Custom controls" in the Accessibility notes and the PR.
   b. **Full contract** — the role, accessible name, every state, the complete keyboard
      model and focus management from `aria.md` §3–§5 (web) or the semantics and custom
      actions from `mobile.md` §1 (native). Prefer a vetted accessible library (React
      Aria, Radix, Angular CDK, Headless UI) over writing it from scratch.
   c. **Screen reader verification before merge** — at least one desktop and one mobile
      screen reader pass (`testing.md` §3), recorded in the PR.
2. **Name, role, state** — every interactive element exposes an accessible name, the
   correct role, and current state (expanded, selected, checked, pressed, disabled,
   invalid). Visible label text is contained in the accessible name (2.5.3).
3. **Keyboard** — everything operable by pointer is operable by keyboard (or switch /
   screen-reader gestures on mobile), with no traps, in a logical order.
4. **Focus** — focus is always visible, never removed without a replacement, never
   fully hidden behind sticky headers, footers, banners or overlays (2.4.11), and is
   moved deliberately when content opens, closes or the route changes.
   **Team standard:** dismiss select/listbox popups when focus leaves the whole
   control/popup without stealing focus or changing selection. Preserve option
   navigation inside the popup; prefer native selects.
5. **Structure** — real headings, lists, landmarks, tables and label associations;
   DOM/reading order matches visual order.
6. **Text alternatives** — informative images have meaningful alt text; decorative
   ones are hidden from assistive technology; icon-only controls have a name.
7. **Color** — text contrast ≥ 4.5:1 (≥ 3:1 for large text); UI component boundaries,
   states and meaningful graphics ≥ 3:1; color is never the only signal.
8. **Targets** — pointer targets ≥ 24×24 CSS px or adequately spaced (2.5.8). Team
   standard on mobile: 44×44 pt (iOS) / 48×48 dp (Android).
9. **Reflow & resize** — works at 320 CSS px width and 200% text size, and survives the
   text-spacing overrides, with no loss of content or function. Native: supports
   Dynamic Type / font scaling and both orientations. Never disable user zoom.
   For extensions, verify zoom in/out in actual side-panel and bottom/side/
   undocked DevTools hosts; see `references/testing.md`. An ordinary extension
   tab is not native-host zoom evidence.
10. **Forms** — persistent visible labels, programmatic hints and errors, `autocomplete`
   / content-type tokens for personal data, errors identified in text with
   suggestions, no re-entry of already provided data (3.3.7).
   **Team standard:** every editable field/group says Required or Optional,
   matching the actual rule, including conditional requirements. On failed
   submit, preserve values, render linked inline errors next to invalid fields,
   and focus the first invalid field. An optional summary must not compete for
   focus; this focus rule is the team's contract, not a universal WCAG mandate.
11. **Authentication** — allow paste and password managers; no puzzles, transcription
    or memory tests unless an alternative exists (3.3.8).
12. **Pointer** — no path-based or multi-point gesture without a single-pointer
    alternative; no drag without a non-drag alternative (2.5.7); actions fire on
    up-event / are cancellable.
13. **Dynamic content** — status messages (toasts, "saved", result counts, loading
    complete) are announced without moving focus (4.1.3); hover/focus popups are
    dismissible, hoverable and persistent (1.4.13). Verify by driving the action: where focus lands,
    and that the live region existed before the text (`testing.md` behavioural pass).
14. **Time & motion** — time limits adjustable; anything auto-moving > 5 s can be
    paused; nothing flashes > 3×/s; respect reduced-motion preferences (team standard).
15. **Consistency** — navigation, component naming and help mechanisms stay consistent
    and in the same relative order across screens (3.2.3, 3.2.4, 3.2.6).
16. **Language & titles** — page/screen language set; unique, descriptive page titles
    or screen titles.

### Modal scroll isolation (team standard)
Native `<dialog>` inertness does not guarantee scroll isolation. While any
modal is open, block background mouse/touch scrolling, preserve internal
scrolling and stop scroll chaining at its boundaries. Preserve background
position and restore scrolling on all close/error/removal paths, including
nested dialogs; closing a child must not unlock the parent's background.
Do not lock the background for an inline, non-modal picker. Keep keyboard
focus containment, dismissal, focus restoration and browser zoom usable.
Verify real wheel/touch input as well as keyboard; see `references/testing.md`.

### 3. Design-agnostic rule
Never invent brand colors, fonts or layouts. If a supplied token, color pair or design
fails a criterion, **flag it** with the SC number, the measured value, and the nearest
compliant alternative (e.g. "`--text-muted` #8A8A8A on #FFFFFF is 3.45:1, fails 1.4.3;
#767676 passes at 4.54:1"). Do not silently override the design.

### 4. After writing — verify and report
- Self-check the code against every SC the change touches (`success-criteria.md`).
- Add or update automated checks (axe-core for web; platform scanners for native — see
  `testing.md`) for the changed views.
- End the response with a short **Accessibility notes** block:
  - Criteria addressed and how (one line each, with SC numbers).
  - **Needs human verification** — anything automation and code reading cannot
    confirm: alt-text accuracy, caption/transcript quality, reading order with a
    screen reader, focus behavior in the real app, contrast over images/gradients.
  - **Custom controls** — each custom control with its rule 1 justification and the
    screen reader pass still required; or "None — native controls only".
  - Any design or token conflicts flagged under step 3.

### 5. When reviewing existing code
Report each finding as: **SC number + name · severity (Blocker / Major / Minor) ·
location · what fails · concrete fix (code)**. Blocker = a user cannot complete the
task with keyboard or assistive technology. Flag every custom control that duplicates a
native one (e.g. `div` button, custom checkbox, hand-rolled select) — as a WCAG failure
when it breaks an SC (usually 2.1.1 or 4.1.2), otherwise as a **team standard** finding
under rule 1, with the native replacement as the fix. Never claim a product "is WCAG conformant"
based on code review or automated scans alone; conformance requires the manual checks
in `testing.md`.

## Labels used in this skill
- **Required (SC x.y.z)** — normative WCAG 2.2 A/AA requirement.
- **Team standard** — deliberately exceeds AA (e.g. 3:1 focus indicator contrast,
  reduced motion, 44/48 mobile targets). Apply by default; mark as such in reviews,
  and never report a team-standard gap as a WCAG failure.
