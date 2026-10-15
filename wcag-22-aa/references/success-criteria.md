# WCAG 2.2 Level A + AA — developer reference (55 criteria)

Format per criterion: **Do** (what the build must do) · **Fails** (common failures) ·
**Verify** (A = automatable with axe-core / platform scanners, partly; M = manual).
★ = new in WCAG 2.2. 4.1.1 Parsing is obsolete in 2.2 and is not listed.
Normative source: https://www.w3.org/TR/WCAG22/ — when in doubt, read the
"Understanding" document for the criterion.

---

## 1. Perceivable

### 1.1.1 Non-text Content (A)
- **Do:** Informative images: `alt` describing purpose/content. Decorative: `alt=""` (web),
  `isAccessibilityElement = false` / `.accessibilityHidden(true)` / `contentDescription = null`
  (native). Icon-only controls: name the action ("Delete invoice"), not the icon ("trash").
  Complex images (charts): short alt + adjacent long description or data table. CAPTCHA:
  describe purpose and offer an alternative modality.
- **Fails:** missing alt; filename alt; alt duplicating adjacent text; SVG with no name.
- **Verify:** A (presence) + M (quality).

### 1.2.1 Audio-only and Video-only (Prerecorded) (A)
- **Do:** Audio-only → transcript. Video-only (no audio) → transcript or audio track.
- **Verify:** M.

### 1.2.2 Captions (Prerecorded) (A)
- **Do:** Synchronized captions for all prerecorded audio in video (dialogue, speaker IDs,
  meaningful sounds). Use `<track kind="captions">` or the player's caption support.
- **Fails:** auto-generated captions published unreviewed.
- **Verify:** M.

### 1.2.3 Audio Description or Media Alternative (Prerecorded) (A)
- **Do:** Audio description or full text alternative for visual-only information in video.
- **Verify:** M.

### 1.2.4 Captions (Live) (AA)
- **Do:** Real-time captions for live audio in synchronized media (webinars, streams).
- **Verify:** M.

### 1.2.5 Audio Description (Prerecorded) (AA)
- **Do:** Audio description for prerecorded video where visuals carry info not in audio.
  (Stricter than 1.2.3: a text alternative alone is not enough at AA.)
- **Verify:** M.

### 1.3.1 Info and Relationships (A)
- **Do:** Structure is programmatic: headings (`h1`–`h6`), lists, tables with `th`/`scope`/
  `caption`, `label`/`for`, `fieldset`/`legend` for groups, landmarks (`header`, `nav`,
  `main`, `footer`, `aside`), required state (`required`/`aria-required`). Native: header
  traits, grouping containers, semantic roles.
- **Fails:** styled `div` "headings"; layout tables; data tables without `th`/header
  association; placeholder as only label; visually grouped radios with no group name.
  Tables and grids: see `tables.md`.
- **Verify:** A (partial) + M.

### 1.3.2 Meaningful Sequence (A)
- **Do:** DOM / accessibility-tree order matches reading order. Don't reorder visually with
  CSS `order`, `flex-direction: *-reverse`, grid placement, or absolute positioning in ways
  that change meaning.
- **Verify:** M (screen reader / linearize styles).

### 1.3.3 Sensory Characteristics (A)
- **Do:** Instructions don't rely only on shape, color, size, location, orientation or sound
  ("click the green button on the right" → "select **Continue**").
- **Verify:** M.

### 1.3.4 Orientation (AA)
- **Do:** Don't lock portrait/landscape unless essential (e.g. a piano app). No CSS/JS or
  manifest orientation lock; native: support both orientations.
- **Verify:** M.

### 1.3.5 Identify Input Purpose (AA)
- **Do:** Fields collecting the user's own data use the HTML `autocomplete` tokens (`name`,
  `given-name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`, `bday`,
  `username`, `current-password`, `new-password`, `one-time-code`…). Native:
  `textContentType` (iOS), `autofillHints` / `contentType` (Android/Compose),
  `autoComplete` / `textContentType` (React Native), `autofillHints` (Flutter).
- **Verify:** A (invalid tokens) + M (coverage).

### 1.4.1 Use of Color (A)
- **Do:** Color is never the only cue: add text, icon, pattern, underline or shape. Links in
  body text are underlined, or have 3:1 contrast against surrounding text **plus** a
  non-color cue on hover/focus. Error fields get an icon/text, not just a red border.
- **Verify:** M.

### 1.4.2 Audio Control (A)
- **Do:** Audio that auto-plays > 3 s has pause/stop or independent volume control at the
  top of the page/screen. Best: never autoplay audio.
- **Verify:** M.

### 1.4.3 Contrast (Minimum) (AA)
- **Do:** Text and images of text ≥ 4.5:1; large text (≥ 24 CSS px regular, or ≥ 18.66 CSS
  px / 14 pt bold) ≥ 3:1. Applies to placeholder text, text in all states (hover, focus,
  disabled is exempt), text over images/gradients (check worst case).
  Exempt: disabled controls, pure decoration, logos.
- **Verify:** A (solid backgrounds) + M (images/gradients). Use `scripts/contrast.py`.

### 1.4.4 Resize Text (AA)
- **Do:** Text resizes to 200% without loss of content/function. Use relative units
  (`rem`/`em`) for font sizes; never `maximum-scale=1` or `user-scalable=no`; no fixed-height
  text containers that clip. Native: Dynamic Type / `sp` units.
- **Verify:** M (browser zoom 200%, text-only zoom).

### 1.4.5 Images of Text (AA)
- **Do:** Use real text styled with CSS, not images of text (logos exempt).
- **Verify:** M.

### 1.4.10 Reflow (AA)
- **Do:** At 320 CSS px width (= 1280 px at 400% zoom) content reflows to one column with no
  horizontal scrolling; vertical-scrolling content at 256 px height has no vertical scroll in
  2 dimensions. Exceptions: data tables, maps, diagrams, toolbars, video, code that need 2D
  layout. Use fluid layouts, `min-width: 0`, `overflow-wrap: anywhere` for long strings.
- **Fails:** fixed-width containers; sticky headers that eat the viewport at 400%; off-screen
  content reachable only by horizontal scroll.
- **Verify:** M (viewport 320 px or 400% zoom at 1280 px).

### 1.4.11 Non-text Contrast (AA)
- **Do:** ≥ 3:1 against adjacent colors for: UI component boundaries needed to identify the
  control (input borders, checkbox outlines, toggle tracks), state indicators (selected tab,
  checked state, focus indicator), and meaningful graphics (chart lines, icons conveying
  info). Text-only buttons without borders are fine if the text itself meets 1.4.3.
- **Verify:** M + `scripts/contrast.py --non-text`.

### 1.4.12 Text Spacing (AA)
- **Do:** No loss of content/function when users set line-height 1.5×, paragraph spacing 2×,
  letter-spacing 0.12×, word-spacing 0.16× font size. Avoid fixed heights on text
  containers; let them grow; avoid `overflow: hidden` on text boxes.
- **Verify:** M (text-spacing bookmarklet / test CSS in `testing.md`).

### 1.4.13 Content on Hover or Focus (AA)
- **Do:** Tooltips, popovers, hover cards triggered by hover/focus are:
  **Dismissible** (Esc closes without moving focus/pointer), **Hoverable** (pointer can move
  onto the popup without it disappearing), **Persistent** (stays until hover/focus leaves,
  dismissed, or no longer valid). Native `title` tooltips are exempt (user agent).
- **Verify:** M.

---

## 2. Operable

### 2.1.1 Keyboard (A)
- **Do:** All functionality via keyboard (Tab, Shift+Tab, Enter, Space, arrows, Esc) with no
  timing requirement. Use native controls; custom widgets need `tabindex="0"` + key handlers
  per `aria.md`. Click handlers on `div`/`span` are a failure. Hover-only menus need a
  keyboard path.
- **Verify:** M (unplug the mouse) + A (partial).

### 2.1.2 No Keyboard Trap (A)
- **Do:** Focus can always move away using standard keys. Modal dialogs intentionally
  contain focus but must close with Esc / a close button. Embedded widgets (maps, editors,
  iframes) must have a documented way out.
- **Verify:** M.

### 2.1.4 Character Key Shortcuts (A)
- **Do:** Single-character shortcuts (letters, numbers, punctuation without a modifier) can be
  turned off, remapped to include a modifier, or are only active when the component has
  focus.
- **Verify:** M.

### 2.2.1 Timing Adjustable (A)
- **Do:** For any time limit: user can turn off, adjust (≥ 10×), or extend (warned ≥ 20 s
  before expiry, extend with a simple action, at least 10 times). Exceptions: real-time
  events, essential, > 20 hours. Session-timeout dialogs must be keyboard and SR accessible.
- **Verify:** M.

### 2.2.2 Pause, Stop, Hide (A)
- **Do:** Moving/blinking/scrolling content that starts automatically, lasts > 5 s and sits
  alongside other content: provide pause/stop/hide (carousels, marquees, animated
  backgrounds). Auto-updating content (feeds, tickers): pause/stop/hide or control frequency.
- **Verify:** M.

### 2.3.1 Three Flashes or Below Threshold (A)
- **Do:** Nothing flashes more than 3 times per second (unless below general/red flash
  thresholds). Watch animations, video, loading effects.
- **Verify:** M (PEAT for video).

### 2.4.1 Bypass Blocks (A)
- **Do:** "Skip to main content" link as first focusable element, targeting `<main id>`
  (with `tabindex="-1"` if needed); plus landmarks and headings.
- **Verify:** A (partial) + M.

### 2.4.2 Page Titled (A)
- **Do:** Unique, descriptive `<title>` per page/route: "Page – Section – Product". Update on
  SPA route change. Native: screen/navigation titles.
- **Verify:** A (presence) + M (quality).

### 2.4.3 Focus Order (A)
- **Do:** Focus order preserves meaning. Avoid positive `tabindex`. When opening a dialog,
  move focus in; when closing, return to the trigger. Inserted content (expanded section,
  inline error) follows its trigger in DOM order.
- **Verify:** M.

### 2.4.4 Link Purpose (In Context) (A)
- **Do:** Link purpose clear from text alone or with its sentence/list item/table cell/
  heading. Avoid bare "Read more" / "Click here"; if visually required, extend the name with
  visually hidden text or `aria-labelledby` (keep visible text in the name — 2.5.3).
- **Verify:** M.

### 2.4.5 Multiple Ways (AA)
- **Do:** More than one way to find a page in a set: navigation + search, sitemap, or index.
  Exempt: steps in a process.
- **Verify:** M.

### 2.4.6 Headings and Labels (AA)
- **Do:** Headings and labels describe topic or purpose ("Shipping address", not "Section 2").
- **Verify:** M.

### 2.4.7 Focus Visible (AA)
- **Do:** Every keyboard-focusable element has a visible focus indicator. Never
  `outline: none` without a replacement. Use `:focus-visible`.
  **Team standard:** indicator ≥ 2 CSS px thick and ≥ 3:1 against adjacent colors (aligns
  with AAA 2.4.13).
- **Verify:** M.

### 2.4.11 Focus Not Obscured (Minimum) (AA) ★
- **Do:** A focused element is not **entirely** hidden by author-created content (sticky
  headers/footers, cookie banners, chat widgets, non-modal dialogs). Use
  `scroll-padding-top/bottom` equal to sticky bar heights; make banners dismissible or
  non-overlapping; ensure non-modal popups don't cover the next focus target.
  **Team standard:** aim for no partial obscuring either (AAA 2.4.12).
- **Verify:** M (Tab through the whole page with sticky elements active).

### 2.5.1 Pointer Gestures (A)
- **Do:** Multipoint (pinch, two-finger) or path-based (swipe, draw) gestures have a
  single-pointer, non-path alternative (buttons for next/prev, zoom +/-). Exempt: essential
  (signature).
- **Verify:** M.

### 2.5.2 Pointer Cancellation (A)
- **Do:** Single-pointer actions complete on the up-event (`click`), not `pointerdown`/
  `mousedown`/`touchstart`; or can be aborted (move off before release) or undone.
  Drag-and-drop dropping outside a target cancels.
- **Verify:** M + code review for down-event handlers.

### 2.5.3 Label in Name (A)
- **Do:** Accessible name contains the visible label text, ideally starting with it.
  Visible "Search" → name "Search" or "Search products", never "Find". Don't override visible
  text with a different `aria-label`.
- **Verify:** A (partial) + M (voice control test: "click Search").

### 2.5.4 Motion Actuation (A)
- **Do:** Functions triggered by device motion (shake to undo, tilt) also available through
  UI controls, and motion response can be disabled.
- **Verify:** M.

### 2.5.7 Dragging Movements (AA) ★
- **Do:** Every drag operation (reorder lists, sliders, kanban, map pan, file drop, resize
  handles) has a single-pointer alternative without dragging: move up/down buttons, "Move
  to…" menu, click-to-place, step buttons, a file picker. Keyboard support alone does not
  satisfy this — the alternative must work with a single pointer (tap/click).
- **Verify:** M.

### 2.5.8 Target Size (Minimum) (AA) ★
- **Do:** Pointer targets ≥ 24×24 CSS px, OR undersized targets are spaced so a 24 px
  diameter circle centered on each doesn't intersect another target or circle. Exceptions:
  an equivalent control elsewhere on the page meets it, inline targets in text, user-agent
  default controls, essential presentation (e.g. map pins).
  **Team standard:** 44×44 CSS px for primary touch actions; 44 pt iOS / 48 dp Android native.
- **Verify:** A (axe `target-size`) + M.

---

## 3. Understandable

### 3.1.1 Language of Page (A)
- **Do:** `<html lang="en">` (correct BCP 47 code, set dynamically for localized builds).
  Native: app localization / `accessibilityLanguage` / `LocaleSpan` where needed.
- **Verify:** A.

### 3.1.2 Language of Parts (AA)
- **Do:** Passages in another language carry `lang` (`<span lang="fr">`). Language switcher
  items in their own language with `lang`. Exempt: proper names, technical terms, loanwords.
- **Verify:** M.

### 3.2.1 On Focus (A)
- **Do:** Receiving focus never triggers a change of context (navigation, submission, opening
  a new window, moving focus elsewhere).
- **Verify:** M.

### 3.2.2 On Input (A)
- **Do:** Changing a setting (select, radio, checkbox, typing) doesn't automatically change
  context unless the user was warned beforehand. Use an explicit "Apply/Go" button for
  select-to-navigate. Filtering results in place is fine (not a context change) — announce it
  (4.1.3).
- **Verify:** M.

### 3.2.3 Consistent Navigation (AA)
- **Do:** Navigation repeated across pages stays in the same relative order. Implement via
  shared layout components.
- **Verify:** M.

### 3.2.4 Consistent Identification (AA)
- **Do:** Same function = same label/icon/name across the product (don't call it "Search" on
  one page and "Find" on another). Centralize labels in the component library / i18n keys.
- **Verify:** M.

### 3.2.6 Consistent Help (A) ★
- **Do:** If help mechanisms (contact details, human contact method, self-help/FAQ link,
  chatbot) repeat across pages, they appear in the same relative order each time. Put them in
  a shared layout slot.
- **Verify:** M.

### 3.3.1 Error Identification (A)
- **Do:** Errors detected automatically are identified in **text** and the field is
  indicated: `aria-invalid="true"`, error text linked via `aria-describedby`, error summary
  for multi-error submits with links to fields. Native: error announced and attached to the
  field (`TextInputLayout.setError`, `Modifier.semantics { error(...) }`).
- **Verify:** M + A (partial).

### 3.3.2 Labels or Instructions (A)
- **Do:** Visible labels for inputs; required fields marked (text or `*` with a legend);
  formats explained up front ("DD/MM/YYYY"). Placeholders are not labels.
- **Verify:** A (partial) + M.

### 3.3.3 Error Suggestion (AA)
- **Do:** When a correction is known, suggest it ("Enter a date in the format DD/MM/YYYY",
  "Password needs at least 12 characters"), unless that jeopardizes security.
- **Verify:** M.

### 3.3.4 Error Prevention (Legal, Financial, Data) (AA)
- **Do:** For legal commitments, financial transactions, modifying/deleting user data, or
  test submissions: submissions are reversible, OR checked with a chance to correct, OR
  reviewed and confirmed before final submission.
- **Verify:** M.

### 3.3.7 Redundant Entry (A) ★
- **Do:** In one process, information the user already entered is auto-populated or
  selectable (e.g. "Billing same as shipping" checkbox, prefilled review step). Exceptions:
  re-entry essential (games, memory), security (confirm password is allowed), info no longer
  valid.
- **Verify:** M.

### 3.3.8 Accessible Authentication (Minimum) (AA) ★
- **Do:** No cognitive function test (remembering a password, solving a puzzle, transcribing
  characters) in any login step unless one of: an alternative method without one; a
  mechanism to assist (**allow paste**, support password managers via correct `autocomplete`,
  copy-paste of OTP codes); object recognition; recognizing the user's own content.
  Passkeys/WebAuthn, magic links, OAuth and OTP with `autocomplete="one-time-code"` all pass.
- **Fails:** `onpaste` blocked on password or code fields; split OTP inputs that break paste;
  text-transcription CAPTCHA with no alternative.
- **Verify:** M.

---

## 4. Robust

### 4.1.2 Name, Role, Value (A)
- **Do:** Every UI component exposes name, role, states, properties and value to assistive
  technology, and changes are notified. Native controls do this; custom widgets must follow
  `aria.md` (web) or platform semantics (`mobile.md`).
- **Fails:** `div onClick`; custom toggles without `aria-pressed`/`aria-checked`; disclosure
  without `aria-expanded`; icon button without a name.
- **Verify:** A (partial) + M (screen reader).

### 4.1.3 Status Messages (AA)
- **Do:** Status messages that don't take focus are announced via live regions: `role="status"`
  (polite: "Saved", "12 results"), `role="alert"` (assertive: errors needing attention),
  `role="log"` (chat). The live region must exist in the DOM **before** the text is inserted.
  Native: `UIAccessibility.post(notification: .announcement)` / `AccessibilityNotification`,
  Compose `liveRegion`, Android `accessibilityLiveRegion` / pane titles (prefer these over
  `announceForAccessibility`, which recent Android versions deprecate), Flutter
  `SemanticsService.announce`. See `mobile.md`.
- **Verify:** M (screen reader).
