# Tables and data grids

Covers data tables from simple to complex, interactive tables, data grids, responsive
behavior, large/virtualized data, third-party grid libraries and native mobile.
Primary SCs: 1.3.1 Info and Relationships, 1.3.2 Meaningful Sequence, 1.4.10 Reflow,
2.1.1 Keyboard, 2.4.3 Focus Order, 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements,
4.1.2 Name, Role, Value, 4.1.3 Status Messages, 1.4.1 Use of Color, 1.4.11 Non-text Contrast.

Contents: 1 Choose the structure · 2 Simple tables · 3 Complex headers · 4 Content in
cells · 5 Interactive tables · 6 Grid & treegrid · 7 Sticky headers & scrolling ·
8 Responsive tables · 9 Large & virtualized data · 10 States: empty, loading, error,
pagination · 11 Third-party data grids · 12 Native mobile · 13 Testing

---

## 1. Choose the structure first

```
Is it tabular data (values related by row AND column)?
├─ No → not a table. Use headings, lists, <dl>, or cards. Never a layout table.
└─ Yes → native <table> (rule 1: native first)
     ├─ Cells contain links/buttons/checkboxes, Tab moves between them?
     │    → still a plain <table>. Do NOT add role="grid".
     ├─ Users must move cell-to-cell with arrow keys like a spreadsheet
     │  (dense editing, many interactive cells, keyboard power users)?
     │    → <table role="grid"> (§6) — a custom control: rule 1 justification required
     └─ Rows expand into child rows in a hierarchy (files/folders, nested accounts)?
          → role="treegrid" (§6) — custom control; or an expandable-row <table> (§5.3)
```

**Why plain `<table>` is the default:** screen readers give tables dedicated navigation
(jump to table, move by cell, hear headers on every move). `role="grid"` switches many
screen readers into application/focus mode, disabling those commands unless your grid
implements the full keyboard model. A grid done halfway is worse than a table.

Before building a complex table, ask whether it should be **two or more simple tables**
or a table plus a filter. Splitting is usually more accessible than any markup technique.

---

## 2. Simple tables (one header row and/or one header column)

```html
<table>
  <caption>Open invoices, sorted by due date</caption>
  <thead>
    <tr>
      <th scope="col">Invoice</th>
      <th scope="col">Customer</th>
      <th scope="col" class="num">Amount (USD)</th>
      <th scope="col">Due date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">INV-1042</th>
      <td>Northwind Ltd</td>
      <td class="num">420.00</td>
      <td>12 Oct 2026</td>
    </tr>
  </tbody>
  <tfoot>
    <tr><th scope="row" colspan="2">Total</th><td class="num">12,840.00</td><td></td></tr>
  </tfoot>
</table>
```

Rules:
- **Caption** — every data table has a name. `<caption>` is preferred (visible, and it is
  the table's accessible name). If the design has a heading above the table instead, use
  `aria-labelledby="heading-id"` on the `<table>`. Team standard: names describe content
  and current sort/filter ("Open invoices, sorted by due date").
- **Header cells** are `<th>`, never bold `<td>`. Use `scope="col"` / `scope="row"`.
- **Row headers** — the cell that identifies the row (ID, name) is `<th scope="row">`.
  Screen readers then announce "INV-1042" when moving down a column, giving context.
- **`<thead>`, `<tbody>`, `<tfoot>`** — use them. Totals go in `<tfoot>` with a row header.
- **No empty header cells** where a header is meaningful. The top-left corner cell may be
  empty `<td>` (not `<th>`) when there is genuinely no header.
- **Don't** put `role="presentation"`, `role="none"` or `display:` changes on a data table
  (see §8).
- **Never use tables for layout.** Legacy layout tables: `role="presentation"` and no
  `th`, `caption`, `scope` or `summary`.

---

## 3. Complex headers

### 3.1 Two-level column headers (`colgroup`)
```html
<table>
  <caption>Quarterly revenue by region (USD thousands)</caption>
  <colgroup><col></colgroup>
  <colgroup span="2"></colgroup>
  <colgroup span="2"></colgroup>
  <thead>
    <tr>
      <td rowspan="2"></td>
      <th scope="colgroup" colspan="2">2025</th>
      <th scope="colgroup" colspan="2">2026</th>
    </tr>
    <tr>
      <th scope="col">Q1</th><th scope="col">Q2</th>
      <th scope="col">Q1</th><th scope="col">Q2</th>
    </tr>
  </thead>
  <tbody>
    <tr><th scope="row">North America</th><td>410</td><td>455</td><td>480</td><td>512</td></tr>
  </tbody>
</table>
```
The `<colgroup span>` elements must match the `colspan` of the group headers.

### 3.2 Row groups (`rowgroup`)
```html
<tbody>
  <tr><th scope="rowgroup" colspan="3">Engineering</th></tr>
  <tr><th scope="row">Ana Ruiz</th><td>Platform</td><td>Lead</td></tr>
  <tr><th scope="row">Ben Cole</th><td>Platform</td><td>Engineer</td></tr>
</tbody>
<tbody>
  <tr><th scope="rowgroup" colspan="3">Design</th></tr>
  …
</tbody>
```
One `<tbody>` per group.

### 3.3 Irregular tables (`headers` / `id`)
When a data cell's headers can't be expressed with `scope` (headers in the middle of the
table, cells related to non-adjacent headers, three or more header levels), give every
`th` an `id` and list **all** applicable header ids on each `td`:
```html
<th id="h-2026">2026</th> <th id="h-q1">Q1</th> <th id="h-na">North America</th>
<td headers="h-na h-2026 h-q1">480</td>
```
- Every id referenced must exist in the same table (axe: `td-headers-attr`).
- Support for `headers`/`id` is weaker in some screen readers (VoiceOver especially) than
  `scope`. **If a table needs `headers`/`id`, first try to split or restructure it.**

### 3.4 Spanning cells
- `colspan`/`rowspan` on data cells are fine when the span is meaningful; check that every
  header still associates correctly (screen reader test, §13).
- Never use spans to fake visual layout inside a data table.

### 3.5 Describe complex structure
For tables a sighted user needs a moment to understand, add a short description linked
with `aria-describedby` on the `<table>` ("Columns are grouped by year, then quarter. Rows
are grouped by region."). Do not use the obsolete `summary` attribute.

---

## 4. Content in cells

- **Units and scales in the header, not every cell:** "Amount (USD)", "Revenue (USD
  thousands)".
- **Abbreviations:** expand them in the header text or with visually hidden text. Don't
  rely on `<abbr title>` — `title` is not reliably announced. The `abbr` attribute on `<th>`
  (a short header form) has inconsistent support; don't depend on it either.
- **Meaning not by color alone (1.4.1):** overdue, negative, over-budget, status — add text
  or an icon with a text alternative ("Overdue", a minus sign, "−$40.00").
- **Status pills/badges** contain text; meet 4.5:1 text contrast.
- **Icons in cells:** informative icons need a name; decorative ones `aria-hidden="true"`.
- **Empty cells:** put a meaningful value ("—" with visually hidden "None", or "Not set")
  so screen reader users don't hear "blank" and wonder if it failed to load.
- **Numeric alignment (team standard):** right-align numbers, use tabular figures
  (`font-variant-numeric: tabular-nums`), consistent decimals.
- **Selected / hover row styles:** if selection is shown visually by background color,
  it must also be exposed programmatically (checked checkbox or `aria-selected` in a grid)
  and have a non-color cue or ≥ 3:1 indicator (1.4.1, 1.4.11). Zebra striping must keep
  text at 4.5:1 on both stripe colors.

---

## 5. Interactive tables (still a plain `<table>`)

### 5.1 Sorting
```html
<th scope="col" aria-sort="ascending">
  <button type="button" class="sort">
    Due date <svg aria-hidden="true" focusable="false">…</svg>
  </button>
</th>
<th scope="col">
  <button type="button" class="sort">Amount (USD) <svg aria-hidden="true">…</svg></button>
</th>
```
- `aria-sort` (`ascending` / `descending`) only on the **one** currently sorted header;
  remove it from the others.
- The button's name is the column name — the sort state comes from `aria-sort`. Don't
  write "Sort by…" into the visible label unless the design shows it (2.5.3).
- After sorting, announce politely: "Sorted by due date, ascending" (live region,
  `aria.md` §7). Keep focus on the sort button. Update the caption if it states the sort.
- Sort direction icon ≥ 3:1 (1.4.11). Button target ≥ 24×24 px.

### 5.2 Row selection & bulk actions
```html
<th scope="col">
  <input type="checkbox" id="sel-all" aria-label="Select all invoices on this page">
</th>
…
<td><input type="checkbox" aria-labelledby="inv-1042" /></td> <!-- names it "INV-1042" -->
<th scope="row" id="inv-1042">INV-1042</th>
```
- Each row checkbox is named by the row header (`aria-labelledby`) — never 20 checkboxes
  all named "Select".
- "Select all" uses the native `indeterminate` property when some rows are selected (it is
  announced as "mixed"/"half checked"). State whether it selects the page or all results.
- Announce selection count politely: "3 invoices selected".
- Bulk-action toolbar: place it **before** the table in DOM order; don't move focus to it
  when it appears; keep it in a stable position (don't make it appear on top of the
  focused row — 2.4.11). If it's hidden until selection, the announcement tells users it
  exists ("3 selected. Bulk actions available above the table.").

### 5.3 Row actions and expandable detail rows
```html
<tr>
  <th scope="row" id="r1042">INV-1042</th>
  …
  <td>
    <button type="button" id="det-1042" aria-expanded="false" aria-controls="d1042"
            aria-labelledby="det-1042 r1042">Details</button>
    <button type="button" aria-haspopup="menu" aria-expanded="false"
            aria-labelledby="more-1042 r1042" id="more-1042">More actions</button>
  </td>
</tr>
<tr id="d1042" hidden>
  <td colspan="5">…detail content…</td>
</tr>
```
- Repeated action buttons get unique names that **start** with the visible text: list the
  button's own id first in `aria-labelledby`, then the row header ("Details INV-1042",
  "More actions INV-1042" — 2.5.3, 2.4.6). `aria-describedby` is not enough: it doesn't
  change the name, so a list of buttons would still read "Details, Details, Details".
- Prefer one "Actions" menu button per row over many icon buttons; if icons are used,
  each has a name and a 24 px target.
- Detail row immediately follows its parent row; `aria-expanded` on the button.
- Whole-row click targets: keep a real link or button inside the row as the keyboard and
  screen reader path; the row click is a pointer convenience only. Don't put
  `tabindex="0"` or `role="button"` on `<tr>`.

### 5.4 Inline editing
- Prefer an explicit "Edit" button per row (opens an edit form or a dialog). A dialog
  sidesteps most table-editing complexity and is usually the better choice.
- If editing in place: the input is labeled from row + column headers
  (`aria-labelledby="r1042 h-amount"` → "INV-1042 Amount (USD)"), Enter saves, Esc
  cancels, focus returns to the Edit button, the result is announced ("Saved" / error
  text linked with `aria-describedby`, 3.3.1).
- Validation errors appear in the cell as text and are announced.

### 5.5 Column controls
- Column resize and reorder by drag need a non-drag alternative (2.5.7): a column menu
  with "Move left / Move right", "Width: narrow / default / wide", or a "Columns" settings
  dialog with up/down buttons.
- Column show/hide: a "Columns" button opening a checkbox list; announce the change.
- Column header menus (filter, pin, hide) are menu buttons — keyboard reachable, Esc
  closes and returns focus.

---

## 6. Grid and treegrid (custom controls — rule 1 applies)

Use only when §1 says so. Build on `<table>` where possible so structure survives:
```html
<table role="grid" aria-labelledby="grid-title" aria-rowcount="250">
```

**Grid keyboard contract** (APG Grid pattern):
| Key | Action |
|---|---|
| Tab / Shift+Tab | Enters/leaves the grid — the grid is **one** tab stop (roving tabindex on cells) |
| Arrow keys | Move one cell |
| Home / End | First / last cell in row |
| Ctrl+Home / Ctrl+End | First / last cell in grid |
| Page Up / Page Down | Move by visible page of rows |
| Enter or F2 | Enter the cell's widget / start editing |
| Esc | Leave cell widget / cancel editing, focus returns to the cell |
| Space (optional) | Select row; Shift+Space / Ctrl+Space for row / column selection |

- Focusable element in each cell (the cell itself or its single widget); only one
  `tabindex="0"` in the grid at a time.
- Selection: `aria-selected` on rows or cells; `aria-multiselectable="true"` on the grid if
  multiple.
- Read-only grids: `aria-readonly="true"`.
- Header cells keep `role="columnheader"` / `"rowheader"` (native `<th>` does this).

**Treegrid** adds to each row: `aria-level`, `aria-expanded` (parent rows only),
`aria-setsize`, `aria-posinset`. Right arrow expands / moves to first child; Left collapses
/ moves to parent. Follow the APG Treegrid pattern exactly or use a vetted library.

Grids and treegrids require the rule 1 justification and the screen reader pass recorded
in the PR.

---

## 7. Sticky headers, frozen columns and scrolling

```css
.table-scroll { overflow: auto; max-height: 70vh;
  scroll-padding-top: var(--table-header-h);      /* 2.4.11: focused cell not hidden */
  scroll-padding-inline-start: var(--frozen-col-w); }
thead th { position: sticky; top: 0; z-index: 1; }
tbody th[scope="row"] { position: sticky; inset-inline-start: 0; }
```
```html
<div class="table-scroll" role="region" aria-labelledby="inv-caption" tabindex="0">
  <table><caption id="inv-caption">…</caption>…</table>
</div>
```
- A scroll container with no focusable content must itself be focusable so keyboard users
  can scroll it (axe: `scrollable-region-focusable`) — `tabindex="0"`, a role and a name.
- Sticky headers and frozen columns must not hide the focused cell or control
  (scroll-padding above). Test by tabbing through every interactive cell while scrolled.
- At 400% zoom a sticky header plus a sticky page header can fill the viewport — unstick
  the table header at small heights (`@media (max-height: 30em)`).
- Frozen columns implemented as a **separate table** overlaid on the main one break
  header association and double-read content — check library output (§11).
- Visible focus ring must not be clipped by `overflow` — use `outline-offset` inward
  (negative) on cells if needed.

---

## 8. Responsive tables (1.4.10 Reflow)

Data tables are an allowed 1.4.10 exception for two-dimensional scrolling — **the table
itself** may scroll horizontally, the rest of the page must not. Options, safest first:

1. **Horizontal scroll inside a labeled, focusable region** (§7). Keeps full semantics.
   Add a visual hint that more columns exist; freeze the row-header column.
2. **Fewer columns at small widths** — a "Columns" chooser or a priority set of columns,
   with each row linking to a full detail view. Never silently drop information with no
   way to reach it.
3. **Different markup for small screens** — render a list of cards (`<ul>` of `<article>`
   or `<dl>` per record) at the small breakpoint and hide the table with `display:none`
   (and vice versa). Each card has a heading (the row header value) and real text labels
   for every value.

**Avoid restyling the table itself into cards with CSS.** Setting `display: block`, `flex`
or `grid` on `table`, `tr`, `td` has removed table semantics in some browser and screen
reader combinations, and labels injected with CSS `::before { content: attr(data-label) }`
are read inconsistently. If you must do it:
- Restore semantics explicitly: `role="table"`, `role="rowgroup"`, `role="row"`,
  `role="columnheader"`, `role="rowheader"`, `role="cell"` on the corresponding elements.
- Put the labels in the DOM as real text, not generated content.
- Test with VoiceOver (Safari) and NVDA (Chrome/Firefox) at both breakpoints.

---

## 9. Large and virtualized data

- When only some rows are in the DOM (virtual scrolling, server pagination presented as one
  list, lazy loading), tell assistive technology the real size:
  - `aria-rowcount` on the `table`/`grid` = total rows **including header rows**
    (`-1` if unknown).
  - `aria-rowindex` on every rendered `tr`/`row` = its 1-based position in the full set,
    including the header row as 1.
  - Column virtualization: `aria-colcount` on the table, `aria-colindex` on cells.
- Without these, screen readers say "table with 20 rows" for a 5,000-row dataset and users
  cannot tell where they are.
- Keep focus stable when rows recycle: don't destroy the focused row's DOM node; restore
  focus to the same logical cell after re-render.
- `Ctrl+F` and screen reader search can't find unrendered rows — provide a search/filter
  control.
- Prefer real pagination or a "Load more" button over infinite scroll for tables
  (`component-patterns.md` §20). Infinite scroll must not make the footer unreachable.

---

## 10. States: empty, loading, error, pagination, filtering

- **Loading:** `aria-busy="true"` on the table (or its region) while fetching; announce
  "Loading invoices" for waits over ~1 s and "25 invoices loaded" on completion. Skeleton
  rows are `aria-hidden="true"`.
- **Empty:** keep the caption and headers and render one row:
  `<tr><td colspan="5">No invoices match your filters. <button>Clear filters</button></td></tr>`
  — or replace the table with a heading + message. Announce the result count.
- **Error:** text message with a retry button, announced (`role="alert"`), not an empty
  table.
- **Filtering / searching:** filter controls sit before the table; results update in place
  (not a context change, 3.2.2) and the count is announced politely after a short
  debounce: "12 of 240 invoices shown". Update the caption if it describes the filter.
- **Pagination:**
  ```html
  <nav aria-label="Invoices pagination">
    <ul>
      <li><a href="?page=1">Previous<span class="visually-hidden"> page</span></a></li>
      <li><a href="?page=1">1</a></li>
      <li><a href="?page=2" aria-current="page">2</a></li> …
    </ul>
  </nav>
  ```
  Page links named in context ("Page 3" via visually hidden text); targets ≥ 24 px; after a
  client-side page change, move focus to the table caption/heading (`tabindex="-1"`) or
  announce "Page 2 of 10" — never leave focus on a removed element. "Rows per page"
  selects don't auto-navigate unexpectedly.

---

## 11. Third-party data grids (AG Grid, MUI DataGrid, TanStack Table, Kendo, etc.)

A data-grid library is a custom control under rule 1. Its vendor accessibility claims
are not verification. Before adopting or upgrading one, check and record:

- [ ] Renders `table`/`grid` roles with correct row, column header and row header
      association (inspect the accessibility tree, not the DOM classes)
- [ ] Frozen/pinned columns don't split the grid into separate tables that break header
      association or duplicate content
- [ ] Full keyboard model (§6) or plain-table behavior — not a mix; single tab stop if grid
- [ ] Visible focus on cells and in-cell widgets; not obscured by pinned headers/columns
- [ ] Sort, filter, column menus and pagination keyboard operable and announced
- [ ] Column resize/reorder and row drag have non-drag alternatives (2.5.7)
- [ ] Virtualization exposes `aria-rowcount` / `aria-rowindex` (§9)
- [ ] Selection exposed (`aria-selected` / checked) and named per row
- [ ] Editing: inputs labeled, Esc/Enter behavior, errors announced
- [ ] Contrast of headers, gridlines that convey structure, selection and focus states
- [ ] Works at 400% zoom / 320 px and with text spacing overrides
- [ ] NVDA + VoiceOver pass reading headers while moving by cell
- [ ] Vendor's accessibility documentation / conformance report (ACR/VPAT) reviewed, and
      which accessibility options must be switched on (some libraries ship them off by
      default)

Keep the completed checklist with the component's documentation; re-run it on major
version upgrades.

---

## 12. Native mobile

There is no native table control on iOS or Android phones. Choose by data shape:

- **Few columns:** a list where each row is one accessibility element whose label reads
  as a sentence with the column names: "INV-1042, Northwind Ltd, amount 420 dollars, due
  12 October". Group with `.accessibilityElement(children: .combine)` (SwiftUI),
  `Modifier.semantics(mergeDescendants = true)` (Compose), `MergeSemantics` (Flutter),
  `accessible={true}` on the row (React Native) — and add the column names, which merging
  alone doesn't provide.
- **Real two-dimensional grid** (comparisons, schedules, spreadsheets): expose row/column
  position and headers:
  - **iOS UIKit:** container adopts `UIAccessibilityContainerDataTable`
    (`accessibilityRowCount`, `accessibilityColumnCount`,
    `accessibilityDataTableCellElement(forRow:column:)`,
    `accessibilityHeaderElements(forColumn:)` / `(forRow:)`); cells adopt
    `UIAccessibilityContainerDataTableCell` (`accessibilityRowRange`,
    `accessibilityColumnRange`); set `accessibilityContainerType = .dataTable`.
  - **SwiftUI:** `Table` (iOS 16+) — on compact-width iPhone it shows only the first
    column, so that column must carry the essential information or provide a detail
    view. For custom grids, label each cell with its row and column header.
  - **Android Views:** `AccessibilityNodeInfo.CollectionInfo` on the container and
    `CollectionItemInfo` (row/column index and span, `isHeading`) on cells;
    `RecyclerView` with `GridLayoutManager` provides much of this.
  - **Jetpack Compose:** `Modifier.semantics { collectionInfo = CollectionInfo(rows, cols) }`
    on the container and `collectionItemInfo = CollectionItemInfo(rowIndex, rowSpan,
    colIndex, colSpan)` on cells (lazy lists/grids set some of this automatically —
    verify with TalkBack).
  - **Flutter:** the `Table` widget conveys little structure by default; check whether your
    Flutter version provides table semantics roles, otherwise give each cell a `Semantics`
    label that includes its row and column header.
  - **React Native:** no table semantics; use the list approach or a native module.
- Horizontal-scrolling grids need a non-swipe way to reach columns (2.5.1) and must keep
  Dynamic Type / font scaling working without truncating values.
- Swipe-to-delete or swipe actions on rows need visible buttons or accessibility custom
  actions (`mobile.md` §2).

---

## 13. Testing tables

**Automated (axe-core):** relevant rules include `td-headers-attr`, `th-has-data-cells`,
`td-has-header`, `scope-attr-valid`, `table-duplicate-name`, `table-fake-caption`,
`scrollable-region-focusable`, `aria-required-children` / `aria-required-parent` (for
grid/table roles). Some are tagged best-practice or experimental — enable them
explicitly in your axe configuration; they pass silently otherwise. Scan sorted, filtered,
selected, expanded, editing, empty and loading states, and small viewport.

**Screen reader (required for complex tables, grids and third-party grids):**
| Screen reader | How to check |
|---|---|
| NVDA / JAWS (Windows) | `T` jumps to the table; table name and size announced; `Ctrl+Alt+Arrow` moves by cell; column header announced when changing column, row header when changing row |
| VoiceOver (macOS, Safari) | Table name and size announced; `VO+Arrow` moves by cell; headers announced on movement |
| VoiceOver (iOS) / TalkBack (Android) | Swipe through cells/rows; each cell or row announces its value with header context; row/column position where exposed |

Check for every table: name announced; correct row/column counts (real totals for
virtualized data); headers announced on cell movement, including both levels of grouped
headers; sort state announced after sorting; selection count announced; expanded state
of detail rows; empty/loading/error states announced.

**Keyboard:** plain tables — Tab reaches each interactive cell in reading order; grids —
the §6 contract, single tab stop, Esc always returns from in-cell widgets.

**Visual:** 400% zoom (table scrolls inside its region, page does not), sticky headers don't
hide focus, selection and status not shown by color alone.
