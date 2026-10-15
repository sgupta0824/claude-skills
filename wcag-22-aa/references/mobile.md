# Native mobile — applying WCAG 2.2 AA to iOS, Android, React Native and Flutter

WCAG is written for web content, but it is the accepted standard for native apps too (and
is what EN 301 549, Section 508 and most procurement contracts reference). W3C's **WCAG2ICT**
guidance (https://www.w3.org/TR/wcag2ict-22/) explains how each criterion maps to non-web
software. Practical translation used here:

- "Web page" → **screen / view**. "Set of web pages" → the **app**.
- "CSS pixel" → **pt** (iOS) / **dp** (Android) / logical pixels (Flutter, RN).
- "Keyboard" → hardware keyboard **and** switch access / Full Keyboard Access, plus screen
  reader gestures (VoiceOver, TalkBack), which all use the accessibility focus.
- "Accessible name/role/state" → the platform accessibility API (UIAccessibility,
  AccessibilityNodeInfo, Compose semantics, Flutter Semantics).

Webviews and hybrid screens (Capacitor, Cordova, embedded web) follow the web references —
plus the native shell must expose the webview correctly and pass through text scaling.

---

## 0. Native platform controls first (SKILL.md rule 1)

Platform controls ship with correct roles, states, focus, keyboard/switch support, Dynamic
Type / font scaling and voice-control names. Build from them; restyle them through themes
rather than replacing them.

| Need | iOS (UIKit / SwiftUI) | Android (Views / Compose) | React Native | Flutter |
|---|---|---|---|---|
| Button | `UIButton` / `Button` | `Button`, `MaterialButton` / `Button`, `IconButton` | `Button`, or `Pressable` **with** `accessibilityRole="button"` + label | `ElevatedButton`, `TextButton`, `IconButton`, `CupertinoButton` |
| Toggle | `UISwitch` / `Toggle` | `MaterialSwitch` / `Switch` | `Switch` | `Switch`, `CupertinoSwitch` |
| Checkbox / radio | `Toggle(.checkbox)` on macOS; iOS: list row + checkmark with `.isSelected` trait | `CheckBox`, `RadioButton` / `Checkbox`, `RadioButton` + `Modifier.selectable` | community checkbox with roles, or `Pressable` with `accessibilityRole="checkbox"` + state | `Checkbox`, `Radio`, `CheckboxListTile`, `RadioListTile` |
| Text input | `UITextField` / `TextField`, `SecureField` | `TextInputLayout` + `TextInputEditText` / `TextField`, `OutlinedTextField` | `TextInput` | `TextField`, `TextFormField` |
| Picker / select | `UIPickerView`, `UIMenu` / `Picker`, `Menu` | `Spinner`, `ExposedDropdownMenu` / `ExposedDropdownMenuBox` | platform picker libraries | `DropdownMenu`, `DropdownButton`, `CupertinoPicker` |
| Slider / stepper | `UISlider`, `UIStepper` / `Slider`, `Stepper` | `Slider` (Material) / `Slider` | community slider exposing `adjustable` role | `Slider`, `CupertinoSlider` |
| Date / time | `UIDatePicker` / `DatePicker` | `MaterialDatePicker` / `DatePicker` | platform date-picker libraries | `showDatePicker`, `CupertinoDatePicker` |
| Segmented / tabs | `UISegmentedControl`, `UITabBarController` / `Picker(.segmented)`, `TabView` | `TabLayout`, `BottomNavigationView` / `TabRow`, `NavigationBar` | navigation library tab bars | `TabBar`, `NavigationBar`, `CupertinoSegmentedControl` |
| Dialog / sheet | `UIAlertController`, sheets / `.alert`, `.sheet` | `MaterialAlertDialog`, `BottomSheetDialog` / `AlertDialog`, `ModalBottomSheet` | `Modal`, `Alert` | `showDialog`, `AlertDialog`, `showModalBottomSheet` |

**Custom-control red flags on mobile** (each needs the rule 1 justification, full
semantics from §1, and a VoiceOver + TalkBack pass):
- `onTapGesture` on a `Text`/`Image`/`VStack` (SwiftUI); `UITapGestureRecognizer` on a
  `UIView`/`UILabel`.
- `setOnClickListener` on a `TextView`/`LinearLayout`; `Modifier.clickable` on a
  `Box`/`Row` without `role` and state (use `toggleable`/`selectable` for state).
- `TouchableOpacity`/`Pressable` without `accessibilityRole` and label (React Native).
- `GestureDetector`/`InkWell` around a custom widget without a `Semantics` wrapper (Flutter).

---

## 1. API mapping

| Need | iOS UIKit | SwiftUI | Android Views | Jetpack Compose | React Native | Flutter |
|---|---|---|---|---|---|---|
| Name | `accessibilityLabel` | `.accessibilityLabel()` | `contentDescription`, `labelFor`, `TextInputLayout` hint | `semantics { contentDescription }`; text content | `accessibilityLabel` / `aria-label` | `Semantics(label:)`, `tooltip:` on IconButton |
| Hint / description | `accessibilityHint` | `.accessibilityHint()` | `tooltipText`, `hint` | `semantics { stateDescription }`, supporting text | `accessibilityHint` | `Semantics(hint:)` |
| Role | `accessibilityTraits` (`.button`, `.link`, `.header`, `.adjustable`, `.image`) | `.accessibilityAddTraits(.isButton/.isHeader/.isLink)` | Use native widget; `AccessibilityDelegate` `className`; `setAccessibilityHeading` | `semantics { role = Role.Button }`, `heading()` | `accessibilityRole` / `role` | `Semantics(button:/header:/link:/image:)` |
| State | traits `.selected`, `.notEnabled`; `accessibilityValue` | `.isSelected` trait, `.accessibilityValue()` | `setStateDescription`, checked/selected on native widgets | `stateDescription`, `selected`, `toggleableState`, `disabled()` | `accessibilityState={{checked, selected, expanded, disabled}}` | `Semantics(checked:, selected:, enabled:, expanded:)` |
| Hide decorative | `isAccessibilityElement = false`, `accessibilityElementsHidden` | `.accessibilityHidden(true)` | `importantForAccessibility="no"`; `contentDescription=null` on images | `Icon(contentDescription = null)`, `clearAndSetSemantics {}` | `accessible={false}`, `importantForAccessibility="no"`, `aria-hidden` | `ExcludeSemantics` |
| Group as one element | container `isAccessibilityElement = true` + label | `.accessibilityElement(children: .combine)` | `focusable`/`screenReaderFocusable` container | `Modifier.semantics(mergeDescendants = true)` | `accessible={true}` on container | `MergeSemantics` |
| Modal | `accessibilityViewIsModal = true` | `.accessibilityAddTraits(.isModal)` | Dialog / `setAccessibilityPaneTitle` | `Dialog`, `paneTitle` | `accessibilityViewIsModal` (iOS), `Modal` | `BlockSemantics`, `showDialog` |
| Announce (4.1.3) | `UIAccessibility.post(notification: .announcement, argument:)` | `AccessibilityNotification.Announcement(…).post()` | `accessibilityLiveRegion="polite"` | `semantics { liveRegion = LiveRegionMode.Polite }` | `accessibilityLiveRegion` (Android), `AccessibilityInfo.announceForAccessibility` | `Semantics(liveRegion: true)`, `SemanticsService.announce` |
| Screen change focus | `.post(notification: .screenChanged, argument: view)` | `@AccessibilityFocusState` | `sendAccessibilityEvent`, pane title | `FocusRequester`, `paneTitle` | `AccessibilityInfo.setAccessibilityFocus` | `FocusNode.requestFocus`, route semantics |
| Custom actions (swipe/drag alternatives) | `accessibilityCustomActions` | `.accessibilityAction(named:)` | `ViewCompat.addAccessibilityAction` | `semantics { customActions = … }` | `accessibilityActions` + `onAccessibilityAction` | `Semantics(customSemanticsActions:)` |
| Adjustable (slider/stepper) | `.adjustable` + `accessibilityIncrement/Decrement` | `.accessibilityAdjustableAction` | `SeekBar` / range info | `Slider` / `progressSemantics`, `setProgress` | `accessibilityRole="adjustable"` + `accessibilityActions` increment/decrement | `Slider` / `Semantics(increasedValue:, onIncrease:)` |
| Reading order | element order / `accessibilityElements` | `.accessibilitySortPriority()` | layout order / `accessibilityTraversalBefore/After` | layout order / `isTraversalGroup`, `traversalIndex` | layout order | `FocusTraversalGroup`, `OrdinalSortKey` |
| Autofill (1.3.5, 3.3.8) | `textContentType` (`.username`, `.password`, `.oneTimeCode`, `.emailAddress`) | `.textContentType()` | `android:autofillHints` | `semantics { contentType = ContentType.Username }` (recent Compose) / autofill APIs | `autoComplete`, `textContentType` | `autofillHints` + `AutofillGroup` |
| Text scaling (1.4.4) | `UIFont.preferredFont(forTextStyle:)` + `adjustsFontForContentSizeCategory = true` | built-in `.font(.body)` styles; avoid fixed `.system(size:)` without `relativeTo:` | `sp` units | `sp` units / `MaterialTheme.typography` | default `allowFontScaling` (never set false globally) | don't clamp `MediaQuery.textScaler` to 1.0 |
| Reduced motion | `UIAccessibility.isReduceMotionEnabled` | `@Environment(\.accessibilityReduceMotion)` | `Settings.Global.ANIMATOR_DURATION_SCALE` / `ValueAnimator.areAnimatorsEnabled()` | same | `AccessibilityInfo.isReduceMotionEnabled()` | `MediaQuery.disableAnimationsOf(context)` |
| Min target (2.5.8; team std) | 44×44 pt frame / `contentShape` | `.frame(minWidth: 44, minHeight: 44)` | `minHeight/minWidth="48dp"`, `TouchDelegate` | `minimumInteractiveComponentSize()` (48 dp) | `minHeight: 44`, `hitSlop` | `kMinInteractiveDimension` (48), `MaterialTapTargetSize.padded` |

## 2. Criterion notes specific to native

- **1.1.1 / 4.1.2:** Image buttons and icon-only toolbar items always need a label. Don't
  include the control type in the label ("Delete", not "Delete button") — the role is
  announced separately.
- **1.3.1:** Mark section titles as headers (`.header` trait / `heading()` / `header: true`) —
  screen reader users navigate by headings with the rotor / reading controls.
- **1.3.2 / 2.4.3:** Verify swipe order with VoiceOver/TalkBack; custom layouts (overlapping
  views, `ZStack`, `Box`, `Stack`) often produce wrong order.
- **1.3.4:** Support portrait and landscape on phones and tablets unless essential.
- **1.4.3 / 1.4.11:** Same ratios as web; check both light and dark appearance and the
  increased-contrast settings.
- **1.4.4 / 1.4.10:** At the largest accessibility text sizes (iOS AX5, Android 200% font
  scale), text must not truncate or overlap; layouts switch from horizontal to vertical
  stacks; content scrolls. Never set `numberOfLines = 1` / `maxLines = 1` on essential text
  without an alternative.
- **2.1.1 / 2.1.2:** Test with a Bluetooth keyboard (iOS Full Keyboard Access, Android
  keyboard navigation) and Switch Control / Switch Access. Custom gestures need an
  accessibility action or a visible control.
- **2.4.2:** Every screen has a title (navigation title, `paneTitle`, `Semantics(namesRoute:)`
  / route title) that VoiceOver/TalkBack announce on arrival.
- **2.4.7 / 2.4.11:** Keyboard focus must be visible (system focus effects work if you don't
  suppress them); bottom sheets, snackbars and keyboards must not cover the focused field —
  scroll it into view.
- **2.5.1 / 2.5.7:** Swipe-to-delete, swipe between pages, pull-to-refresh, drag-to-reorder,
  pinch-to-zoom → each needs a tap alternative (visible button or menu) **and** a custom
  accessibility action.
- **2.5.3:** For voice control (Voice Control on iOS, Voice Access on Android), the spoken
  name must match the visible text; iOS `accessibilityInputLabels` can add alternatives.
- **2.5.4:** Shake-to-undo / shake-to-report must have a UI alternative and be disableable.
- **2.5.8:** Undersized hit areas are the #1 mobile failure — expand the touch area without
  changing visuals (`contentShape`, `hitSlop`, `TouchDelegate`, padding).
- **3.2.3 / 3.2.4 / 3.2.6:** Tab bars and navigation stay in the same order on every screen;
  help/support entry in a consistent location.
- **3.3.1–3.3.3:** Attach errors to fields (`TextInputLayout.setError`,
  `semantics { error("…") }`, `Semantics` label update + announcement) and announce on submit.
- **3.3.8:** Allow paste in password/OTP fields; support password managers through autofill
  hints; support biometrics/passkeys as non-memory alternatives; SMS code autofill.
- **Tables and grids:** no native table control exists on phones — see `tables.md` §12 for
  list vs. data-table semantics per platform.
- **4.1.3:** Snackbars/toasts must be announced; on Android a `Snackbar` is announced by
  TalkBack; custom banners need a live region or announcement.

## 3. Cross-platform specifics

**React Native**
- Every `Pressable`/`Touchable*` needs `accessibilityRole` and a label if not text-only.
- `aria-*` and `role` props are supported in recent versions; pick one style per codebase.
- `accessibilityState` must update with every state change (expanded, checked, selected).
- Modal: `accessibilityViewIsModal` (iOS) and `importantForAccessibility="no-hide-descendants"`
  on the background (Android).
- Lint: `eslint-plugin-react-native-a11y`.

**Flutter**
- Prefer Material/Cupertino widgets — they ship semantics. Custom `GestureDetector`
  widgets need a `Semantics` wrapper with `button: true`, `label`, `onTap`.
- Flutter **web** builds the semantics tree only when enabled — call
  `SemanticsBinding.instance.ensureSemantics()` at startup so assistive tech gets it without
  the user activating a hidden toggle.
- Don't clamp text scaling to 1.0 in `MediaQuery`/`textScaler`; test at 200%.
- Widget-test guidelines: `meetsGuideline(androidTapTargetGuideline)`,
  `iOSTapTargetGuideline`, `labeledTapTargetGuideline`, `textContrastGuideline`.

## 4. Native testing tools (axe-core does not cover native screens)

| Platform | Automated | Manual |
|---|---|---|
| iOS | XCUITest `app.performAccessibilityAudit()` (Xcode 15+/iOS 17+); Accessibility Inspector audit | VoiceOver, Full Keyboard Access, Voice Control, Switch Control, largest Dynamic Type, Increase Contrast, Reduce Motion |
| Android | Espresso `AccessibilityChecks.enable()` (Accessibility Test Framework); Compose UI test accessibility checks (recent `ui-test` versions); Accessibility Scanner app; Android Lint | TalkBack, Switch Access, Voice Access, keyboard, font size + display size at max |
| React Native | `eslint-plugin-react-native-a11y`; Testing Library role/label queries; then the platform tools above on device | as iOS + Android |
| Flutter | `meetsGuideline(...)` widget tests; platform tools on device | as iOS + Android |
| Webviews / hybrid | axe-core injected into the webview content | screen reader inside the app shell |
