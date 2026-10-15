# ARIA — rules, mechanics and pitfalls

ARIA changes only what assistive technology is **told**. It adds no behavior, no focus,
no keyboard support and no styling. Misused ARIA is worse than none: pages using ARIA
routinely show more detected errors than pages without it. Every role you add is a promise
of specific keyboard behavior — keep it or don't add the role.

Primary sources: WAI-ARIA 1.2 (https://www.w3.org/TR/wai-aria-1.2/), ARIA Authoring
Practices Guide (APG, https://www.w3.org/WAI/ARIA/apg/), ARIA in HTML
(https://www.w3.org/TR/html-aria/), Accessible Name Computation
(https://www.w3.org/TR/accname-1.2/).

---

## 1. The five rules of ARIA use

1. **Use native HTML first.** `<button>` beats `<div role="button">`. `<a href>` beats
   `role="link"`. `<input type="checkbox">` beats `role="checkbox"`. `<dialog>` beats
   `role="dialog"`. `<details>/<summary>` beats a scripted disclosure. `<select>` beats a
   custom listbox when it meets the design need. Any custom control needs the written
   justification, full contract and screen reader pass required by SKILL.md rule 1.
2. **Don't change native semantics** unless you must. Not `<h2 role="tab">`; put
   `<div role="tab">` inside the heading, or don't use a heading.
3. **All interactive ARIA controls must be keyboard operable** (see §4).
4. **Never use `role="presentation"`/`role="none"` or `aria-hidden="true"` on a focusable
   element.**
5. **All interactive elements must have an accessible name.**

---

## 2. Accessible name — how it's computed (simplified accname order)

1. `aria-labelledby` (references visible text by id; wins over everything; can reference
   multiple ids and hidden elements)
2. `aria-label` (string; invisible to sighted users — use sparingly)
3. Native labeling: `<label for>`, wrapping `<label>`, `alt`, `<caption>`, `<legend>`,
   `<figcaption>`, `title` attribute on `<svg>` via `<title>` child
4. Element content (for roles that allow name-from-content: button, link, tab, menuitem,
   option, heading, cell…)
5. `title` attribute (last resort; unreliable — don't depend on it)
6. `placeholder` (fallback only in some browsers — never rely on it)

**Rules**
- Visible label text must be **contained** in the accessible name (2.5.3) — preferably at
  the start. `aria-label` that differs from visible text breaks voice control users.
- `aria-label` is ignored on generic elements (`div`, `span` without a role) and is poorly
  supported on non-interactive roles in some AT. Don't put it on `div`/`span`/`p`.
- `aria-describedby` = supplementary description (hints, errors, format), read after the
  name. It is not a substitute for a name.
- Names should be concise and unique in context: "Edit", "Edit" , "Edit" in a table → "Edit
  invoice 1042" (visible "Edit" + visually hidden or `aria-labelledby` row header).
- Don't include the role in the name: `aria-label="Close"` not `"Close button"`.

```html
<!-- Icon button -->
<button type="button" aria-label="Close dialog"><svg aria-hidden="true" focusable="false">…</svg></button>

<!-- Repeated link made unique while keeping visible text first -->
<a href="/invoices/1042" aria-labelledby="edit-1042 inv-1042">
  <span id="edit-1042">Edit</span>
</a> <!-- #inv-1042 is the row header cell text "Invoice 1042" -->

<!-- Visually hidden text utility (keep it in the design system) -->
<style>
.visually-hidden{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;
overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}
</style>
```

---

## 3. States and properties — required per widget

| Widget | Element / role | Required state & props | Notes |
|---|---|---|---|
| Toggle button | `<button>` | `aria-pressed="true\|false"` | Name must not change with state ("Mute" stays "Mute") |
| Disclosure | `<button>` | `aria-expanded`, optional `aria-controls` | Content follows the button in DOM |
| Accordion | heading > `<button>` | `aria-expanded`, `aria-controls`; panel optional `role="region"` + `aria-labelledby` | |
| Tabs | `tablist` > `tab`; `tabpanel` | `aria-selected`, `aria-controls` on tab; `aria-labelledby` on panel | Roving tabindex (§5) |
| Modal dialog | `<dialog>` + `showModal()` or `role="dialog"` | `aria-modal="true"`, `aria-labelledby` (title), optional `aria-describedby` | Background `inert` |
| Alert dialog | `role="alertdialog"` | as dialog + `aria-describedby` message | For confirmations needing a response |
| Checkbox (custom) | `role="checkbox"` | `aria-checked="true\|false\|mixed"` | Space toggles |
| Switch | `role="switch"` | `aria-checked` | Prefer `<button aria-pressed>` or native checkbox |
| Radio group (custom) | `radiogroup` > `radio` | `aria-checked`; group name | Arrows move + select |
| Combobox | `<input role="combobox">` + `listbox` | `aria-expanded`, `aria-controls`, `aria-activedescendant`, `aria-autocomplete` | Follow APG 1.2 pattern exactly |
| Listbox | `listbox` > `option` | `aria-selected`, `aria-multiselectable` if multi | |
| Menu button | `<button aria-haspopup="menu">` | `aria-expanded`, `aria-controls` | Menu: `menu` > `menuitem` |
| Slider | `<input type="range">` or `role="slider"` | `aria-valuenow/min/max`, `aria-valuetext` for human values | Also needs non-drag alternative (2.5.7) |
| Progress | `<progress>` or `role="progressbar"` | `aria-valuenow/min/max` (omit now if indeterminate) | Name it |
| Tree | `tree` > `treeitem` | `aria-expanded`, `aria-selected`, `aria-level` | Complex — prefer a library |
| Grid (interactive) | `grid` > `row` > `gridcell` | roving focus | Only for spreadsheet-like widgets; data tables use `<table>` |
| Current item | links in nav / steps | `aria-current="page\|step\|date\|true"` | Not `aria-selected` |
| Invalid field | input | `aria-invalid="true"` + `aria-describedby` → error | Set only after validation |
| Required field | input | native `required` (or `aria-required="true"`) | Plus visible indicator |
| Busy region | container | `aria-busy="true"` while updating | Remove when done |
| Disabled | native `disabled` or `aria-disabled="true"` | `aria-disabled` keeps it focusable/discoverable | Block activation in JS if using aria-disabled |

States must be **updated in sync** with the visual state on every change.

---

## 4. Keyboard contract implied by roles

| Role | Keys that must work |
|---|---|
| button | Enter, Space |
| link | Enter |
| checkbox / switch | Space |
| radio (in radiogroup) | Arrow keys move and check; Tab enters/leaves the group |
| tablist / tab | Left/Right (or Up/Down if vertical) move; Home/End; Enter/Space activates if manual activation |
| menu / menubar | Arrows, Home/End, Enter/Space, Esc closes and returns focus, type-ahead |
| listbox | Up/Down, Home/End, Space (multi-select), type-ahead |
| combobox | Down opens/moves into list, Up/Down navigate, Enter selects, Esc closes (then clears) |
| dialog | Tab cycles inside, Esc closes, focus returns to trigger |
| slider | Arrows ±step, PageUp/PageDown ±large step, Home/End min/max |
| tree | Up/Down, Right expands/enters, Left collapses/goes to parent, Home/End |
| grid | Arrow keys between cells, Home/End, Ctrl+Home/End |

---

## 5. Focus management techniques

- **Roving tabindex:** in a composite widget (tabs, toolbar, radio group, menu), only the
  active item has `tabindex="0"`; others `tabindex="-1"`. Arrow keys move `tabindex="0"` and
  call `.focus()`. Tab leaves the widget.
- **`aria-activedescendant`:** DOM focus stays on the container/input; the attribute points
  to the id of the visually active option. Used for combobox listboxes. The referenced
  element must be in the DOM and have a visible active style.
- **`tabindex` values:** `0` = in natural order; `-1` = focusable by script only (headings
  or `<main>` as focus targets after route change / skip link); **never positive values**.
- **Programmatic focus on non-interactive elements** (`h1 tabindex="-1"`) is fine for route
  changes and errors; don't give them a focus style that looks interactive; don't leave
  `tabindex="0"` on them.

---

## 6. Hiding content — pick the right tool

| Goal | Use |
|---|---|
| Hidden from everyone | `hidden` attribute, `display:none`, `visibility:hidden` |
| Visible, hidden from AT (decorative) | `aria-hidden="true"` (and no focusable descendants!) |
| Hidden visually, available to AT | `.visually-hidden` class |
| Disable a whole region (behind a modal, off-canvas menu) | `inert` attribute (removes from tab order AND AT) |

**Pitfalls**
- `aria-hidden="true"` on a container with links/buttons → focusable "ghost" elements. Use
  `inert` instead.
- `aria-hidden` on `<body>`'s ancestors of the modal → hides the modal too. With
  `<dialog>.showModal()` the browser handles inertness for you.
- Off-screen menus positioned with `transform` but not `inert`/`hidden` → keyboard users
  tab into invisible links (2.4.3, 2.4.7).

---

## 7. Live regions (4.1.3)

```html
<!-- Present in the DOM at page load, empty -->
<div role="status" aria-live="polite" aria-atomic="true" class="visually-hidden" id="status"></div>
<div role="alert" aria-live="assertive" aria-atomic="true" class="visually-hidden" id="alert"></div>
```
```js
function announce(msg, el = document.getElementById('status')) {
  el.textContent = '';                       // reset so identical messages re-announce
  requestAnimationFrame(() => { el.textContent = msg; });
}
announce('Invoice saved');
```
- Inject the **container** once (layout level); update its **text** later. Containers added
  together with their text are often not announced.
- Framework pitfall: `{done ? <p role="status">Saved</p> : null}` mounts the container with its
  text, so it is often silent. Always render `<p role="status">{done ? 'Saved' : ''}</p>`.
- `polite` for success/status/result counts; `assertive`/`role="alert"` only for urgent
  errors. Don't announce every keystroke — debounce search result counts (~500 ms).
- Visible toasts can double as the live region if the toast container is persistent.
- Don't use live regions to compensate for missing focus management (e.g. route changes →
  move focus to the `h1` instead).

---

## 8. Landmarks

`<header>` (banner, top-level only), `<nav>` (navigation — label each if more than one:
`aria-label="Primary"`, `"Breadcrumb"`), `<main>` (exactly one), `<aside>` (complementary),
`<footer>` (contentinfo, top-level only), `<form>`/`<section>` become landmarks only with an
accessible name, `role="search"` (or `<search>` element). Don't add redundant roles to native
elements (`<nav role="navigation">`).

---

## 9. Common ARIA mistakes → fix

| Mistake | Why it fails | Fix |
|---|---|---|
| `<div onclick>` / `<span role="button">` without key handling | Not focusable / no Enter-Space (2.1.1, 4.1.2) | `<button type="button">` |
| `<a>` without `href` used as button | Not focusable, wrong role | `<button>`; links navigate, buttons act |
| `role="menu"` for site navigation | Promises app-menu keyboard model; SR users get menu mode | `<nav>` + list of links; disclosure buttons for submenus |
| `aria-label` on a `div` / `span` | Ignored or inconsistent | Use visible text or a proper role |
| `aria-label` different from visible text | Breaks voice control (2.5.3) | Start the name with the visible text |
| `aria-hidden="true"` on focusable content | Focusable but silent | `inert`, or remove from tab order |
| Live region injected with its content | Not announced | Persistent empty region, then set text |
| `aria-expanded` on the panel instead of the trigger | Wrong element | Put it on the `<button>` |
| `aria-selected` for current nav page | Wrong state | `aria-current="page"` |
| Redundant role (`<button role="button">`, `<ul role="list">`) | Noise (exception: `role="list"` restores list semantics removed by `list-style:none` in Safari — acceptable) | Remove |
| `role="presentation"` on a `<table>` that holds data | Removes table semantics (1.3.1) | Keep data tables semantic |
| `tabindex="0"` on non-interactive text "for screen readers" | Adds noise tab stops; SR users don't need it | Remove; SRs read text without focus |
| Positive `tabindex` | Breaks order (2.4.3) | Fix DOM order |
| `aria-disabled="true"` without blocking clicks | Control still works | Guard handlers |
| Toggle whose label flips ("Play" → "Pause") **and** uses `aria-pressed` | Double-signals | Either change the label OR use `aria-pressed`, not both |
| Custom select/combobox from scratch | Most-broken widget class | Native `<select>` or a vetted library (verify it with a SR) |

---

## 10. Framework notes

- **React:** ARIA attributes are kebab-case (`aria-expanded={open}`); booleans render as
  `"true"/"false"` strings — good. `useId()` for id references. Fragments/portals: portal
  modals still need focus management and `inert` on the app root.
- **Vue 3:** bind with `:aria-expanded="open"`; `false` renders the string `"false"` (correct
  for ARIA states). Use `null`/`undefined` to remove an attribute entirely (e.g. drop
  `aria-describedby` when there is no error).
- **Angular:** use `[attr.aria-expanded]="open"`; Angular CDK `a11y` (FocusTrap,
  LiveAnnouncer, ListKeyManager) implements several patterns correctly.
- **Svelte:** compiler a11y warnings are useful — don't suppress them without a reason.
- **Component libraries:** Radix UI, React Aria, Headless UI, Angular CDK, Reach-style
  primitives handle most ARIA/keyboard plumbing — still verify name, contrast, target size
  and focus visibility, which are your styling responsibility.
