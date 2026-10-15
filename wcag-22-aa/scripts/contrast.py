#!/usr/bin/env python3
"""WCAG 2.2 contrast checker for color pairs and design tokens (no dependencies).

Usage:
  python3 contrast.py "#767676" "#ffffff"            # one pair, all thresholds
  python3 contrast.py "#8A8A8A" "#fff" --type text   # exit 1 if it fails; suggests a fix
  python3 contrast.py --pairs pairs.json             # batch check token pairs

pairs.json:
  [
    {"name": "text-muted on surface", "fg": "#8A8A8A", "bg": "#FFFFFF", "type": "text"},
    {"name": "heading-xl on brand",   "fg": "#FFFFFF", "bg": "#3B82F6", "type": "large"},
    {"name": "input border",          "fg": "#C4C4C4", "bg": "#FFFFFF", "type": "non-text"}
  ]

Types and minimum ratios:
  text      4.5:1  (SC 1.4.3, text under 24px / under 18.66px bold)
  large     3:1    (SC 1.4.3, text >= 24px or >= 18.66px bold)
  non-text  3:1    (SC 1.4.11, UI component boundaries, states, meaningful graphics;
                    also the team standard for focus indicators)

Colors: #RGB, #RRGGBB, #RRGGBBAA (alpha is blended over the background), rgb()/rgba().
Exit code: 0 if every checked pair passes, 1 otherwise.
"""
import argparse
import json
import re
import sys

THRESHOLDS = {"text": 4.5, "large": 3.0, "non-text": 3.0}
SC = {"text": "1.4.3", "large": "1.4.3", "non-text": "1.4.11"}


def parse(color):
    c = color.strip().lower()
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:[\s,/]+([\d.]+%?))?\s*\)", c)
    if m:
        r, g, b = (float(m.group(i)) for i in range(1, 4))
        a = m.group(4)
        alpha = 1.0 if a is None else (float(a[:-1]) / 100 if a.endswith("%") else float(a))
        return (r, g, b, alpha)
    c = c.lstrip("#")
    if len(c) in (3, 4):
        c = "".join(ch * 2 for ch in c)
    if len(c) not in (6, 8) or not re.fullmatch(r"[0-9a-f]+", c):
        raise ValueError(f"Unrecognized color: {color}")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    alpha = int(c[6:8], 16) / 255 if len(c) == 8 else 1.0
    return (r, g, b, alpha)


def blend(fg, bg):
    """Alpha-composite fg over an opaque bg."""
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3))


def luminance(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg_str, bg_str):
    bg = parse(bg_str)
    if bg[3] < 1:
        raise ValueError(f"Background must be opaque: {bg_str}")
    fg = blend(parse(fg_str), bg)
    l1, l2 = sorted((luminance(fg), luminance(bg[:3])), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05), fg


def to_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(255, v))):02X}" for v in rgb)


def suggest(fg_rgb, bg_str, target):
    """Nearest passing color: move fg toward black or white in small steps, keeping hue."""
    bg = parse(bg_str)[:3]
    best = None
    for end in ((0, 0, 0), (255, 255, 255)):
        for step in range(1, 401):
            t = step / 400
            cand = tuple(fg_rgb[i] + (end[i] - fg_rgb[i]) * t for i in range(3))
            cand = tuple(round(v) for v in cand)
            l1, l2 = sorted((luminance(cand), luminance(bg)), reverse=True)
            r = (l1 + 0.05) / (l2 + 0.05)
            if r >= target:
                if best is None or t < best[0]:
                    best = (t, to_hex(cand), r)
                break
    return best


def check(name, fg, bg, kind):
    r, fg_rgb = ratio(fg, bg)
    need = THRESHOLDS[kind]
    # WCAG: compare unrounded ratio against threshold (4.499 fails)
    ok = r >= need
    line = f"{'PASS' if ok else 'FAIL'}  {r:5.2f}:1  {kind:<8} (SC {SC[kind]}, needs {need}:1)  {name}  [{fg} on {bg}]"
    if not ok:
        s = suggest(fg_rgb, bg, need)
        if s:
            line += f"\n      nearest passing foreground: {s[1]} ({s[2]:.2f}:1)"
    print(line)
    return ok


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fg", nargs="?", help="foreground color (text, border, icon)")
    p.add_argument("bg", nargs="?", help="background color (opaque)")
    p.add_argument("--type", choices=THRESHOLDS, help="check only this threshold")
    p.add_argument("--non-text", action="store_true", help="shorthand for --type non-text")
    p.add_argument("--pairs", help="JSON file with [{name, fg, bg, type}]")
    a = p.parse_args()

    try:
        if a.pairs:
            with open(a.pairs) as f:
                pairs = json.load(f)
            results = [check(x.get("name", ""), x["fg"], x["bg"], x.get("type", "text")) for x in pairs]
            failed = results.count(False)
            print(f"\n{len(results) - failed}/{len(results)} pairs pass")
            sys.exit(0 if failed == 0 else 1)
        if not (a.fg and a.bg):
            p.error("give FG and BG colors, or --pairs FILE")
        kind = "non-text" if a.non_text else a.type
        kinds = [kind] if kind else list(THRESHOLDS)
        results = [check("", a.fg, a.bg, k) for k in kinds]
        sys.exit(0 if all(results) else 1)
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
