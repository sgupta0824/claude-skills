# Component patterns (web)

Framework-agnostic recipes in plain HTML/CSS/JS. Translate to your framework and design
system; keep the semantics, keyboard behavior and focus handling identical. Styling is
yours — the constraints in `design-tokens.md` apply to whatever it looks like.
For native mobile equivalents see `mobile.md`. For ARIA details see `aria.md`.

**Native first (SKILL.md rule 1).** Patterns 2–7, 13 and 15 are built on native elements —
keep them native. Patterns that need ARIA (tabs, menu buttons, combobox, carousel,
drag-and-drop) exist only because HTML has no native equivalent; using one of them still
requires the custom-control justification and screen reader pass.

Contents: 1 Page shell · 2 Buttons & links · 3 Images & icons · 4 Forms · 5 Errors ·
6 Dialogs · 7 Disclosure & accordion · 8 Tabs · 9 Navigation & menus · 10 Combobox ·
11 Tooltips & popovers · 12 Toasts & status · 13 Tables · 14 Carousels · 15 Media ·
16 Drag and drop · 17 Authentication · 18 Multi-step flows · 19 SPA routing ·
20 Loading, infinite scroll, timeouts · 21 Charts

---

## 1. Page shell (2.4.1, 2.4.2, 3.1.1, 1.3.1, 3.2.3, 3.2.6)
```html
<html lang="en">
<head><title>Invoices – Billing – Acme</title>
<meta name="viewport" content="width=device-width, initial-scale=1"> <!-- never user-scalable=no -->
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <header>…<nav aria-label="Primary">…</nav></header>
  <main id="main" tabindex="-1"><h1>Invoices</h1>…</main>
  <footer>… help links in a fixed, shared slot (3.2.6) …</footer>
</body></html>
```
- Skip link: first focusable element; visible on focus.
- One `h1` per page; don't skip heading levels (team standard — supports 1.3.1/2.4.6).
- Shared layout guarantees consistent nav order (3.2.3) and help placement (3.2.6).
- Sticky header/footer → set `scroll-padding-top/bottom` to their heights (2.4.11).

## 2. Buttons vs links (2.1.1, 4.1.2, 2.5.3)
- **Link** navigates (`<a href>`). **Button** performs an action (`<button type="button">`).
  Never `<a href="#">` for actions; never `<button>` that only navigates.
- Always set `type` on buttons inside forms (`submit` / `button`).
- Disabled: prefer keeping the control enabled and explaining what's missing; if disabled,
  native `disabled` (exempt from contrast) or `aria-disabled="true"` (stays focusable).
- Links opening a new window: indicate it ("Opens in a new tab" icon + hidden text).
- Minimum 24×24 CSS px target (2.5.8); text links inline in a sentence are exempt.

## 3. Images & icons (1.1.1, 1.4.5, 1.4.11)
```html
<img src="chart.png" alt="Revenue rose 18% from Q1 to Q2, led by subscriptions.">
<img src="divider.svg" alt="">                                   <!-- decorative -->
<svg role="img" aria-labelledby="t1"><title id="t1">Warning</title>…</svg> <!-- meaningful standalone SVG -->
<button aria-label="Delete invoice 1042"><svg aria-hidden="true" focusable="false">…</svg></button>
<span class="icon" aria-hidden="true">✓</span><span>Paid</span>   <!-- icon + text: hide icon -->
```
- CSS background images are invisible to AT — never use them for informative content.
- Informative icons need 3:1 contrast (1.4.11).

## 4. Forms (1.3.1, 1.3.5, 2.4.6, 3.3.2, 3.2.2)
```html
<form novalidate>
  <p id="req-note">Every field is marked Required or Optional.</p>
  <div class="field">
    <label for="email">Email <span>(Required)</span></label>
    <p id="email-hint" class="hint">We'll send the receipt here.</p>
    <input id="email" name="email" type="email" autocomplete="email" required
           aria-describedby="email-hint">
  </div>

  <fieldset>
    <legend>Delivery speed (Required)</legend>
    <input type="radio" id="std" name="speed" value="std"><label for="std">Standard (3–5 days)</label>
    <input type="radio" id="exp" name="speed" value="exp"><label for="exp">Express (1 day)</label>
  </fieldset>

  <button type="submit">Place order</button>
</form>
```
- Team standard: every editable field/group visibly says Required or Optional; conditional requirements must be explicit. Native `required` / supported `aria-required` states must agree with the actual validation.
- Every input has a persistent visible `<label>`. Placeholder is never the label.
  Floating-label patterns must keep the label visible and contrast-compliant.
- Group related controls (radios, checkbox sets, date parts, address) with
  `fieldset`/`legend`.
- `autocomplete` tokens on all personal-data fields (1.3.5); correct `type`/`inputmode`.
- Selects don't navigate or submit on change (3.2.2).
- Character counters: announce at thresholds via polite live region, not every keystroke.

## 5. Error handling (3.3.1, 3.3.3, 3.3.4, 4.1.3, 1.4.1)
```html
<div id="error-summary" role="alert" tabindex="-1" hidden>
  <h2>There are 2 problems</h2>
  <ul><li><a href="#email">Enter an email address in the format name@example.com</a></li>…</ul>
</div>
<label for="email">Email</label>
<input id="email" aria-invalid="true" aria-describedby="email-hint email-error" autocomplete="email">
<p id="email-error" class="error"><svg aria-hidden="true">…</svg> Enter an email address in the format name@example.com</p>
```
- Team standard: on failed submit, preserve values and focus the first invalid field after rendering all linked inline errors. An optional summary may announce the count/provide field links, but must not move focus away from that field. WCAG requires accessible error identification; first-invalid-field focus is this team’s chosen contract.
- Server-action / re-rendering forms can lose focus when controls are replaced. Restore
  the intended focus explicitly after rendering the result.
- While a request is pending, prevent duplicate submissions and verify focus stays
  logical. If disabling or replacing the focused submit button loses focus in supported
  browsers, keep it focusable with `aria-disabled="true"` and guard repeat activations,
  or move focus deliberately when the result requires it.
- Inline errors: text (not color alone) + icon, `aria-invalid="true"`, referenced in
  `aria-describedby`. Clear both when fixed.
- Validate on submit or on blur — not on every keystroke while the user is still typing.
- Messages say what's wrong **and** how to fix it (3.3.3): "Enter an email address like
  name@example.com", not "Invalid email". Name the field in summaries. Server/network
  errors explain what happened and what to do next ("We couldn't save your answer.
  Check your connection and try again"). Link field-specific errors to their fields;
  operation-level errors belong in an appropriately announced status/error region.
- Legal/financial/data-deleting actions: review step or confirmation or undo (3.3.4).

## 6. Dialogs (2.1.2, 2.4.3, 2.4.11, 4.1.2)
```html
<button type="button" id="open-del">Delete project</button>
<dialog id="del" aria-labelledby="del-title" aria-describedby="del-desc">
  <h2 id="del-title">Delete project?</h2>
  <p id="del-desc">This permanently removes 14 files.</p>
  <button type="button" value="cancel" autofocus>Cancel</button>
  <button type="button" value="confirm">Delete</button>
</dialog>
<script>
const d = document.getElementById('del'), t = document.getElementById('open-del');
t.addEventListener('click', () => d.showModal());    // native: traps focus, Esc closes, inert background
d.addEventListener('close', () => t.focus());         // return focus to trigger
</script>
```
- Use `<dialog>.showModal()` where possible. If custom: `role="dialog"`, `aria-modal="true"`,
  focus trap, Esc closes, `inert` on the rest of the app, scroll lock.
- Initial focus: first field, or the least destructive action, or the dialog heading
  (`tabindex="-1"`) for long content.
- Always a visible close/cancel control. Return focus to the trigger (or a logical place if
  the trigger was removed).
- Team standard: lock background wheel/touch scrolling for native and custom
  modals, allow internal scrolling, contain overscroll and restore the original
  background scroll position on every close/removal/error path. Retain the lock
  until the last modal closes. Do not equate keyboard trapping with scroll locking.
- Select/listbox popups close when focus exits the entire control/popup; preserve
  selection and normal Tab/Shift+Tab progression. Do not close on internal option
  focus changes. Native selects manage their own popup behavior.
- Non-modal popups must not cover the focused element (2.4.11).

## 7. Disclosure & accordion (4.1.2, 2.1.1)
```html
<h3><button type="button" aria-expanded="false" aria-controls="faq1">Can I cancel anytime?</button></h3>
<div id="faq1" hidden>…</div>
```
- Toggle `aria-expanded` and `hidden` together. Content immediately follows in DOM.
- `<details><summary>` is an acceptable native alternative.

## 8. Tabs (4.1.2, 2.1.1)
```html
<div role="tablist" aria-label="Account settings">
  <button role="tab" id="t-profile" aria-selected="true"  aria-controls="p-profile" tabindex="0">Profile</button>
  <button role="tab" id="t-billing" aria-selected="false" aria-controls="p-billing" tabindex="-1">Billing</button>
</div>
<div role="tabpanel" id="p-profile" aria-labelledby="t-profile" tabindex="0">…</div>
<div role="tabpanel" id="p-billing" aria-labelledby="t-billing" tabindex="0" hidden>…</div>
```
- Left/Right arrows move between tabs (roving tabindex), Home/End to ends; automatic
  activation unless loading a panel is expensive (then Enter/Space activates).
- If "tabs" actually navigate to different URLs, use `<nav>` links with `aria-current="page"`.

## 9. Navigation & menus (2.4.3, 2.1.1, 3.2.3)
```html
<nav aria-label="Primary"><ul>
  <li><a href="/" aria-current="page">Dashboard</a></li>
  <li>
    <button type="button" aria-expanded="false" aria-controls="sub-reports">Reports</button>
    <ul id="sub-reports" hidden><li><a href="/reports/sales">Sales</a></li>…</ul>
  </li>
</ul></nav>
```
- Site navigation = links + disclosure buttons. **Do not** use `role="menu"`/`menubar`
  (reserved for application menus with the full arrow-key model).
- Submenus open on click/Enter/Space, not hover-only; Esc closes and returns focus to the
  button; closing when focus leaves is good practice.
- Mobile "hamburger": a disclosure button (`aria-expanded`, name "Menu"); when open as an
  overlay, treat as a modal (trap + Esc + `inert` background).
- Application menu buttons (`role="menu"`, e.g. row "More actions"): follow APG Menu Button.

## 10. Combobox / autocomplete (4.1.2, 4.1.3, 2.1.1)
- Prefer native `<select>` or `<input list>` + `<datalist>` when acceptable.
- Otherwise follow APG Combobox (1.2) exactly or use a vetted library:
  `<input role="combobox" aria-expanded aria-controls="lb" aria-autocomplete="list"
  aria-activedescendant="opt-3">` + `<ul role="listbox" id="lb">` with `role="option"`.
- Announce result counts politely ("5 suggestions available").
- Keyboard: Down opens/moves, Up/Down navigate, Enter selects, Esc closes then clears.

## 11. Tooltips & popovers (1.4.13, 2.1.1)
```html
<button type="button" aria-describedby="tip-export">Export</button>
<div role="tooltip" id="tip-export" hidden>Downloads a CSV of the current filter</div>
```
- Show on hover **and** focus; hide on Esc, blur, and pointer-out of both trigger and tip
  (with a short delay so the pointer can move onto it — hoverable).
- No interactive content inside tooltips; if it needs links/buttons it's a popover/dialog
  (click-triggered, focus moved into it).
- Never put essential information only in a tooltip (touch users can't hover).
- Native `popover` attribute is fine for click-triggered popovers; still manage names and
  focus.

## 12. Toasts & status messages (4.1.3, 2.2.1)
- Render a persistent live region container at app root (see `aria.md` §7); push toasts into
  it.
- Success: `role="status"`. Errors: `role="alert"`.
- Toasts with actions ("Undo") must not auto-dismiss before users can reach them — keep them
  until dismissed, or provide the action elsewhere; pause timers on hover/focus (2.2.1).
- Don't move focus to a toast.

## 13. Tables & data grids → `references/tables.md`
**Always open `tables.md` for any table, data grid or tabular list work.** Summary of the
non-negotiables:
- Tabular data uses a native `<table>` with a `<caption>` (or `aria-labelledby`), `<th>`
  with `scope`, and a row header per row. Never use tables for layout.
- Interactive cells (links, buttons, checkboxes) do **not** make it a grid. `role="grid"` /
  `treegrid` only for spreadsheet-style arrow-key navigation — a custom control under
  rule 1.
- Complex headers: `colgroup`/`rowgroup` scopes, `headers`/`id` only for irregular tables —
  and try splitting the table first.
- Wide tables scroll inside a focusable, named region; don't restyle table elements into
  cards with CSS `display` changes.
- Sticky headers must not hide focused cells (2.4.11); virtualized tables expose
  `aria-rowcount`/`aria-rowindex`; sort, selection, filter and page changes are announced.
- Third-party data grids get the verification checklist in `tables.md` §11.

## 14. Carousels (2.2.2, 2.1.1, 2.5.1, 4.1.3)
- No autoplay by default (team standard). If it autoplays for more than 5 s: a visible
  Pause/Play button placed before the slides (2.2.2), plus pausing while hovered or focused
  (team standard).
- Previous/Next buttons (single-pointer alternative to swipe, 2.5.1), slide picker buttons
  with names ("Slide 3 of 5").
- Container: `role="region" aria-roledescription="carousel" aria-label="Featured"`; slides
  `role="group" aria-roledescription="slide" aria-label="3 of 5"`; hidden slides `inert`.

## 15. Media (1.2.x, 1.4.2, 2.1.1)
```html
<video controls preload="metadata">
  <source src="intro.mp4" type="video/mp4">
  <track kind="captions" src="intro.en.vtt" srclang="en" label="English" default>
  <track kind="descriptions" src="intro.desc.en.vtt" srclang="en" label="Audio description">
</video>
<a href="intro-transcript.html">Read the transcript</a>
```
- Custom players: every control is a real `<button>` with name and state, keyboard operable,
  focus visible, 24 px targets, caption toggle exposed.
- No autoplay with sound (1.4.2).

## 16. Drag and drop (2.5.7, 2.1.1, 2.5.2, 4.1.3)
- Every drag interaction gets a **single-pointer, non-drag** alternative:
  - Sortable list: "Move up" / "Move down" buttons or a "Move to position…" menu per item.
  - Kanban: "Move to column ▾" menu on each card.
  - Slider: native range input (tap the track) + step buttons or a number input.
  - File drop zone: a visible "Choose file" button (`<input type="file">`).
  - Resizable panels: buttons or a menu with preset sizes.
- Keyboard path too (e.g. Space to pick up, arrows to move, Space to drop, Esc to cancel),
  announcing each move politely: "Invoice 1042 moved to position 3 of 8".
- Dropping outside a valid target cancels (2.5.2).

## 17. Authentication (3.3.8, 1.3.5, 3.3.1, 2.2.1)
```html
<label for="u">Email</label><input id="u" type="email" autocomplete="username">
<label for="p">Password</label><input id="p" type="password" autocomplete="current-password">
<button type="button" aria-pressed="false" aria-controls="p">Show password</button>
<label for="otp">6-digit code</label>
<input id="otp" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]*">
```
- Never block paste (`onpaste` preventDefault) on any credential or code field.
- Single OTP input preferred. If split boxes are mandated: support pasting the full code
  into the first box and auto-distribute, a single group label, and each box named
  ("Digit 1 of 6").
- Offer passkeys/WebAuthn, magic links or OAuth as non-memory alternatives where possible.
- No CAPTCHA requiring transcription/puzzles without an alternative (prefer invisible risk
  checks).
- New-password fields: `autocomplete="new-password"`; state rules up front (3.3.2).
- Session timeouts: warn ≥ 20 s ahead with an accessible "Stay signed in" dialog (2.2.1).

## 18. Multi-step flows / checkout (3.3.7, 3.3.4, 2.4.2, 2.4.3)
- Step indicator as an ordered list with `aria-current="step"`; page title includes
  "Step 2 of 4".
- Carry forward data (3.3.7): "Billing address same as shipping" checkbox, prefill
  previously entered values, review step shows entered data with "Edit" links.
- On step change: update the title and move focus to the step heading.
- Final review + confirm for financial/legal submissions (3.3.4).

## 19. SPA route changes (2.4.2, 2.4.3, 4.1.3)
- On every client-side navigation: update `document.title`, move focus to the new page's
  `h1` (`tabindex="-1"`) or main region, and restore scroll to top. Some frameworks ship a
  route announcer (e.g. Next.js) — keep it, but still manage focus and title.
- Don't move focus on in-page filter/sort updates; announce results politely instead.

## 20. Loading, infinite scroll, timeouts (4.1.3, 2.1.1, 2.4.1)
- Loading: `aria-busy="true"` on the updating region; announce completion ("Results loaded")
  for long waits; spinners have a name ("Loading invoices").
- Skeleton screens are decorative — hide from AT; announce when real content arrives.
- Infinite scroll: provide a "Load more" button instead of (or in addition to) auto-loading,
  and keep the footer reachable. Keep focus position when new items append.

- **Long-running background jobs** (report/plan/export generation, minutes not seconds):
  - The heading and page title describe the *current state* ("Your plan is being built"),
    not the action that started it ("Start a new plan").
  - Show visible progress: an indeterminate indicator with a name (`role="progressbar"` with
    no value, or a labelled spinner). Where useful and known, give the start time and
    expected duration; do not invent estimates.
  - Say where the result will appear and whether the user can leave ("You can leave this
    page; we'll email you and add it to Your plans").
  - Put the status in a **persistent** live region (see `aria.md` §7) and move focus to the
    status heading after submit when needed to orient the user. When the job ends, announce it ("Your plan is ready") and
    offer a link; if the page polls, don't re-render the region in a way that re-announces.
  - Team standard: don't format dates ambiguously (`10/28/2026`); use "28 Oct 2026".
  - Where cancellation is supported, provide Cancel and explain its effect. For a
    stalled job, offer a supported recovery action without implying work was rolled back.
- **Blocking "please wait" overlays** that cannot be dismissed still follow the dialog rules
  in §6: move focus inside (or to the status text), keep it contained, lock page scroll,
  restore focus to the triggering control afterwards. Prefer an inline status for anything
  longer than a few seconds.

## 21. Charts & data visualization (1.1.1, 1.4.1, 1.4.11, 1.3.1)
- Give each chart a name and a text summary of the key takeaway; provide the underlying
  data as a table (visible or toggle).
- Don't encode series by color alone: add direct labels, patterns or marker shapes.
- Lines, bars and markers ≥ 3:1 against the background (1.4.11).
- Interactive charts: tooltips follow 1.4.13; data points reachable by keyboard or the table
  provides equivalent access.
- **Everything needed to read a value is a graphic needing 3:1 (1.4.11):** gridlines, axis
  lines, scale ticks, radar rings and spokes — not only the bars/lines. Faint "decorative"
  grids (`#e5e7eb`-style, about 1.1:1) fail when the scale is the only way to read a value.
  Otherwise label values directly and drop the grid.
- Measure against the **actual page background** (a card, a tinted canvas), not white.
- Text drawn over a data fill (axis labels over a radar polygon, labels on bars) is tested
  against the *blended* colour; avoid overlap or give it a halo/background.
- Team standard: aim for chart text of at least 12 CSS px at the default size; prevent
  label collisions and verify enlargement/reflow. WCAG does not set a universal minimum
  font size; assess the applicable contrast, resize and reflow criteria.
- Inspect the actual DOM and accessibility tree produced by the installed chart library.
  Never leave an unnamed focusable chart surface. If a redundant chart is hidden from
  assistive technology, also remove its focusability and provide equivalent data in a
  table. Use `role="img"` with a name for a static exposed chart; interactive charts need
  appropriate semantics and keyboard behavior, not a blanket role override.
