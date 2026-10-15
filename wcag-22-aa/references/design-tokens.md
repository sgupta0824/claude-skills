# Design tokens & visual constraints — for any design system

These are constraints, not a style. Apply them to whatever tokens, theme or design system the
project uses (CSS custom properties, Tailwind config, Style Dictionary, Figma variables,
SwiftUI/Compose themes). Never replace brand values silently — flag failures with the SC,
the measured value and the nearest compliant alternative.

Check pairs with: `python3 scripts/contrast.py <fg> <bg>` or a token file
(`python3 scripts/contrast.py --pairs pairs.json`).

---

## 1. Color contrast

| What | Minimum | SC |
|---|---|---|
| Body/UI text < 24 px (or < 18.66 px bold) | **4.5:1** | 1.4.3 |
| Large text ≥ 24 px, or ≥ 18.66 px bold | **3:1** | 1.4.3 |
| Placeholder text, helper text, captions, timestamps | 4.5:1 (it's still text) | 1.4.3 |
| Input borders, checkbox/radio outlines, toggle tracks, slider tracks — whatever identifies the control | **3:1** vs adjacent background | 1.4.11 |
| State indicators (selected tab underline, checked fill, current-page marker) | 3:1 vs adjacent colors | 1.4.11 |
| Meaningful icons and chart marks | 3:1 vs background | 1.4.11 |
| Focus indicator | visible (2.4.7) — **team standard: ≥ 3:1 vs adjacent colors, ≥ 2 px** | 2.4.7 |
| Links distinguished from body text by color only | 3:1 vs surrounding text **and** non-color cue on hover/focus; team standard: underline | 1.4.1 |
| Disabled controls, decoration, logos | exempt | — |

**Token rules**
- Define contrast-safe **pairs**, not lone colors: `text-primary on surface`,
  `text-on-brand on brand`, `border-input on surface`. Every pair is checked in every theme
  (light, dark, high-contrast) and every state (default, hover, active, focus, selected,
  error).
- "Muted"/"subtle"/"secondary" text tokens are the most common failure — test them first.
- Status colors (error, warning, success): the **text** version must pass 4.5:1; the
  meaning must also be carried by text/icon (1.4.1).
- Text over images/video/gradients: test the lightest/darkest area under the text or add a
  scrim/overlay token with guaranteed contrast.
- Opacity-based tokens (`rgba`, `opacity: .6`): compute against the actual background after
  blending — the script accepts `#RRGGBBAA` and blends over the background.

## 2. Focus indicator
```css
:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {
  outline: var(--focus-width, 2px) solid var(--focus-color);
  outline-offset: var(--focus-offset, 2px);
}
/* Never: *:focus { outline: none } without a replacement */
```
- One shared focus token set (`--focus-color`, `--focus-width`, `--focus-offset`) used by
  every component.
- Must remain visible on every surface the component can sit on (brand-colored buttons, dark
  headers, images). A two-tone ring (e.g. dark outline + light inner box-shadow) works on any
  background.
- Use `outline` (respects Windows High Contrast / forced colors) — `box-shadow`-only focus
  disappears in forced-colors mode; add `outline: 2px solid transparent` as a fallback.
- Don't clip focus rings with `overflow: hidden` on parents.

## 3. Target size & spacing (2.5.8)
- Interactive targets ≥ **24×24 CSS px** (including padding — the hit area, not the icon).
- Undersized targets: ensure ≥ 24 px spacing between target centers so 24 px circles don't
  overlap other targets.
- **Team standard:** 44×44 CSS px for primary touch actions on responsive layouts; native
  44×44 pt (iOS HIG) / 48×48 dp (Material).
- Token suggestion: `--target-min: 24px; --target-touch: 44px;` and component `min-height`/
  `min-width` built on them. Icon buttons: icon 16–20 px + padding to reach the minimum.

## 4. Typography & text resizing (1.4.4, 1.4.12, 1.4.5)
- Font sizes in `rem` (web) / Dynamic Type text styles (iOS) / `sp` (Android) / text scaling
  (Flutter) — never `px` locked sizes that ignore user settings.
- Line-height as a unitless number (≥ 1.5 for body text is a good team standard).
- Containers holding text: no fixed `height`; use `min-height`; avoid `overflow: hidden` and
  single-line truncation for essential content (or provide the full text elsewhere).
- Must survive the text-spacing override (line-height 1.5, paragraph 2em, letter .12em,
  word .16em) — see `testing.md`.
- Body text: team standard ≥ 16 px; avoid long passages of justified or all-caps text.

## 5. Layout & breakpoints (1.4.10, 1.3.4, 1.3.2)
- Must work at **320 CSS px** viewport width without horizontal scrolling (except 2D content
  like data tables, maps, code). That equals desktop at 400% zoom — breakpoints must respond
  to zoom, so define them in `em`/`rem` or test with zoom.
- Sticky/fixed headers and footers: reduce or unstick them at small heights
  (`@media (max-height: 30em)`) so they don't consume the viewport at zoom; set
  `scroll-padding` (2.4.11).
- Never lock orientation (1.3.4).
- Visual order = DOM order. Don't use `order`, `row-reverse`, grid placement or absolute
  positioning to reorder meaningful content.

## 6. Motion & animation (2.2.2, 2.3.1; team standard for reduced motion)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important;
  }
}
```
- Motion tokens (`--duration-*`, `--easing-*`) should collapse to 0 under reduced motion;
  replace parallax/zoom/slide transitions with fades or none.
- Anything that moves for > 5 s needs pause (2.2.2). Never flash > 3 times/second (2.3.1).

## 7. Forced colors / high contrast (supports 1.4.11, 2.4.7)
```css
@media (forced-colors: active) {
  .custom-checkbox { border: 1px solid CanvasText; }
  .icon { forced-color-adjust: auto; }
}
```
- Don't convey state only with background color or `box-shadow` — they're removed in forced
  colors. Use borders/outlines, or system colors (`Highlight`, `CanvasText`, `ButtonText`).
- SVG icons: use `fill="currentColor"` so they follow text color.

## 8. Dark mode & theming
- Every theme is a separate contrast check — a pair passing in light mode says nothing about
  dark mode.
- Pure white text on pure black can cause halation for some users; slightly off-black
  surfaces are fine as long as ratios pass.

## 9. Design review checklist (hand to designers)
- [ ] All text/background pairs ≥ 4.5:1 (3:1 large) in all themes and states
- [ ] Control boundaries, states, icons ≥ 3:1
- [ ] Focus style defined for every interactive component, visible on every surface
- [ ] Targets ≥ 24 px (team standard 44 px touch)
- [ ] No information by color alone (errors, status, charts, links)
- [ ] Layout specified at 320 px width and with 200% text
- [ ] Labels visible for every input (no placeholder-only)
- [ ] Error, empty, loading and success states designed with text
- [ ] Help/contact placement consistent across templates
- [ ] Every drag interaction has a non-drag alternative designed
- [ ] Reduced-motion variant for animations
