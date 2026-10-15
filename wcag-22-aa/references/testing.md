# Testing & verification

Automated tools find only a portion of WCAG issues (roughly a third to a half, depending on
how you count). They cannot judge alt-text quality, reading order, focus behavior, caption
accuracy or whether an error message helps. **A green axe run is necessary, never
sufficient.** Every change needs the relevant manual checks below.

Web automation standard: **axe-core** (Deque). Native: platform tools in `mobile.md` §4.

---

## 1. axe-core configuration (WCAG 2.2 A/AA)

Use these tags so rules match the target exactly:
```js
const WCAG_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22a', 'wcag22aa'];
```
Optional `best-practice` tag for extra checks (report separately; not WCAG failures).

### Playwright (`@axe-core/playwright`) — page and flow scans
```js
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const WCAG_TAGS = ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22a','wcag22aa'];

test('invoices page has no detectable WCAG A/AA violations', async ({ page }) => {
  await page.goto('/invoices');
  const results = await new AxeBuilder({ page }).withTags(WCAG_TAGS).analyze();
  expect(results.violations).toEqual([]);
});

test('dialog state is scanned too', async ({ page }) => {
  await page.goto('/projects');
  await page.getByRole('button', { name: 'Delete project' }).click();
  const results = await new AxeBuilder({ page })
    .include('dialog')            // scan the open state, not just the initial render
    .withTags(WCAG_TAGS).analyze();
  expect(results.violations).toEqual([]);
});
```
- Scan **every state**: open menus, dialogs, error states, empty states, loading, dark mode,
  mobile viewport (`page.setViewportSize({ width: 320, height: 640 })`).
- Use Playwright role locators (`getByRole('button', { name: 'Save' })`) in all tests — if
  a test can't find an element by role and name, neither can a screen reader user.

### Behavioural pass (what axe cannot see)
Axe scans a page at rest; most real failures appear after an action. For every form, async
action, route change and overlay, drive it and record:
- **Where focus lands** after submit, error, success and navigation (`document.activeElement`).
  `<body>` is a failure.
- **Whether the message is announced:** observe DOM insertions (`MutationObserver`) and check
  that each new message is inside a live region that *already existed* before the text.
  A `role="status"` node inserted together with its text is not reliable.
- **Error states:** field has `aria-invalid` and `aria-describedby`; message says how to fix
  it; focus goes to the first invalid field or the summary.
- **Route changes:** `document.title` differs per page; focus or announcement tells the user
  the page changed.
- **Overlays/dialogs:** Tab stays inside, Esc/Cancel/Close dismiss, focus returns to the
  trigger, and `scrollY` does not change when you wheel-scroll behind it.
- **Charts:** render with real data (a mocked payload is fine), then measure gridline/axis/
  fill/label colours against the real background, and check for unnamed focusable SVGs.
- **Long-running states:** put the page in the "in progress" state (fake the DB row) and scan
  and screenshot it.
Run it once keyboard-only and, for announcements, with a real screen reader.

### Component tests (`jest-axe` / `vitest-axe`)
```js
import { axe } from 'jest-axe';
it('IconButton has no violations', async () => {
  const { container } = render(<IconButton label="Delete invoice" icon={<TrashIcon/>} />);
  expect(await axe(container, { runOnly: { type: 'tag', values: WCAG_TAGS } })).toHaveNoViolations();
});
```
Note: jsdom has no layout, so color-contrast and target-size checks don't run here — they
run in the Playwright layer.

### Storybook
`@storybook/addon-a11y` runs axe on every story; configure the same tags and fail CI on
violations via the Storybook test runner.

### Linting (catch issues while typing)
- React/JSX: `eslint-plugin-jsx-a11y` (recommended or strict config).
- Vue: `eslint-plugin-vuejs-accessibility`. Angular: `@angular-eslint` template a11y rules.
  Svelte: built-in compiler a11y warnings.

### CI gate
- Block merges on new axe violations (Playwright + component tests).
- Track known issues in an allow-list **with ticket numbers and owners**, never by disabling
  rules globally.

## 2. Manual checks — run for every UI change (5–10 minutes)

**Keyboard (2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 2.1.4)**
- [ ] Tab/Shift+Tab reaches every interactive element in a logical order
- [ ] Focus is always visible and never fully hidden under sticky bars/banners
- [ ] Enter/Space/arrows/Esc behave per `aria.md` §4
- [ ] Dialogs trap focus, close with Esc, return focus to the trigger
- [ ] No traps; skip link works

**Zoom, reflow, spacing (1.4.4, 1.4.10, 1.4.12, 1.3.4)**
- [ ] Browser zoom 200%: nothing clipped or overlapping
- [ ] 400% zoom at 1280 px (or 320 px viewport): single column, no horizontal scroll (except
      tables/maps/code), sticky bars don't take over the viewport
- [ ] Text-spacing override (paste into the console or a bookmarklet):
```js
const s=document.createElement('style');s.textContent=`*{line-height:1.5!important;
letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}`;
document.head.appendChild(s);
```
- [ ] Rotate device / both orientations work

**Pointer (2.5.1, 2.5.2, 2.5.3, 2.5.7, 2.5.8)**
- [ ] Every drag/swipe/pinch has a single-tap alternative
- [ ] Targets ≥ 24×24 px (inspect hit area, not icon)
- [ ] Voice-control check: visible label = spoken name

**Content (1.1.1, 1.3.3, 1.4.1, 2.4.4, 2.4.6, 3.3.x)**
- [ ] Alt text accurate and concise; decorative images silent
- [ ] Nothing conveyed by color, shape or position alone
- [ ] Headings and labels describe purpose; links make sense in context
- [ ] Submit an invalid form: errors in text, linked to fields, focus to summary, suggestions
- [ ] Previously entered data not requested again in the same flow (3.3.7)
- [ ] Login allows paste and password managers (3.3.8)

**Visual (1.4.3, 1.4.11, 1.4.13)**
- [ ] `scripts/contrast.py` on new color pairs, all themes and states
- [ ] Hover/focus popups: Esc dismisses, pointer can move onto them, they persist

## 3. Screen reader smoke tests (4.1.2, 4.1.3, 1.3.1, 1.3.2)

Run on the pairs your users actually use; at minimum before release:

| Screen reader | Browser / platform | Key commands |
|---|---|---|
| NVDA (free) | Firefox or Chrome on Windows | Insert+Space mode toggle, H headings, D landmarks, F form fields, Tab |
| JAWS | Chrome on Windows (if enterprise users) | similar to NVDA |
| VoiceOver | Safari on macOS | VO (Ctrl+Opt)+U rotor, VO+arrows |
| VoiceOver | Safari on iOS | swipe left/right, rotor (two-finger rotate), double-tap |
| TalkBack | Chrome on Android | swipe left/right, reading controls, double-tap |

Check: page/screen title announced; headings and landmarks navigable; every control
announces name + role + state; state changes announced (expanded, checked); dialogs
announced on open; status messages announced without focus moving; reading order matches
visual order.

## 4. PR checklist (copy into the pull request template)

```markdown
### Accessibility (WCAG 2.2 AA)
- [ ] Native elements/controls used wherever one exists (SKILL.md rule 1)
- [ ] Custom controls (or "None"): ______
      Justification for each: ______
      Screen reader pass (desktop + mobile, which SRs): ______
- [ ] Any ARIA follows references/aria.md
- [ ] Tables/grids (if any): checked against references/tables.md §13; third-party grid
      checklist (§11) on file
- [ ] Keyboard: all functions reachable and operable; focus order logical; no traps
- [ ] Focus visible and not obscured (sticky elements checked)
- [ ] Names, roles, states exposed (icon buttons named; states update)
- [ ] Contrast checked: text 4.5:1 / 3:1 large; UI & graphics 3:1 (all themes/states)
- [ ] Targets ≥ 24×24 px; drag/gesture interactions have single-tap alternatives
- [ ] Works at 320 px width, 200% text, text-spacing override
- [ ] Forms: visible labels, autocomplete tokens, errors in text + linked + announced
- [ ] Status messages announced via live region
- [ ] axe-core (wcag2a…wcag22aa tags) passing for new/changed views and states
- [ ] Screen reader smoke test done on: ______
- [ ] Needs human verification: ______ (alt text, captions, reading order…)
```

## 5. Verification report format (end of every Claude response that changes UI)

```markdown
**Accessibility notes**
- Addressed: 1.3.1 (fieldset/legend for delivery options), 3.3.1 (aria-invalid + linked
  error text), 4.1.3 (polite status on save), 2.5.8 (icon buttons 32×32 px)
- Tests: added Playwright axe scan for /checkout including error state
- Custom controls: address autocomplete combobox (no native element supports async
  search with rich options) — follows APG combobox; NVDA + VoiceOver iOS pass required
- Needs human verification: alt text for product images; NVDA pass on the new combobox
- Design flags: `--text-muted` #8A8A8A on #FFFFFF = 3.45:1, fails 1.4.3 → #767676 (4.54:1)
```
