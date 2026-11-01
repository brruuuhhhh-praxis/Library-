#!/usr/bin/env python3
"""Apply the screenshot-inspired navy + champagne-gold theme to Shri Shyam Library."""
from pathlib import Path
from datetime import datetime
import re, shutil, sys

root = Path.cwd()
theme = root / "src" / "theme-premium.css"
if not theme.exists():
    print("ERROR: Run this script from ~/shri-shyam-library (src/theme-premium.css not found).")
    sys.exit(1)

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_dir = Path.home() / ".shri-shyam-library-backups" / f"reference-theme-{stamp}"
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(theme, backup_dir / "theme-premium.css")

css = theme.read_text(encoding="utf-8")

# Screenshot palette: midnight navy, warm champagne gold, ivory canvas.
replacements = {
    "#101828": "#06182b",
    "#17243b": "#0b2238",
    "#315efb": "#f2bd4b",
    "#2448d8": "#d99a20",
    "#416cff": "#ffd36a",
    "#527aff": "#ffda7c",
    "#edf2ff": "#fff4d8",
    "#f5f7fb": "#fbf8f1",
    "#ffffff": "#ffffff",
    "#172033": "#101b2d",
    "#68758b": "#667080",
    "#e2e7f0": "#e9e1d3",
    "#9eb4ff": "#ffe09a",
    "#aebfff": "#ffda7c",
    "#b8c7ff": "#ffe09a",
    "#b9c8ff": "#ffe09a",
    "#c3d0ff": "#ffe7b2",
    "#c4d0ff": "#ffe7b2",
    "#c8d4ff": "#ffe7b2",
    "#d7dfec": "#f4ead6",
    "#d0d8e7": "#e8dfcf",
    "#d2dbed": "#eee3cf",
    "#d3dbea": "#e8dfcf",
    "#d0d9e9": "#e8dfcf",
    "#e0e7f5": "#f7eedc",
    "#e3eaff": "#fff1d2",
    "#e2e8f5": "#f7eedc",
    "#f5f7ff": "#fffaf0",
    "#1fa8c9": "#d99a20",
}
for old, new in replacements.items():
    css = css.replace(old, new)

# Correct palette variables and button treatments after global color mapping.
css = re.sub(
    r":root\s*\{.*?\}",
    """:root {
  --lux-night: #06182b;
  --lux-night-2: #0b2238;
  --lux-blue: #f2bd4b;
  --lux-blue-dark: #c88a16;
  --lux-blue-light: #fff4d8;
  --lux-cyan: #d99a20;
  --lux-canvas: #fbf8f1;
  --lux-paper: #ffffff;
  --lux-ink: #101b2d;
  --lux-muted: #667080;
  --lux-line: #e9e1d3;
  --lux-shadow: 0 16px 42px rgba(6, 24, 43, .09);
  --lux-shadow-blue: 0 10px 26px rgba(200, 138, 22, .22);
}""",
    css, count=1, flags=re.S
)
# Make all key calls-to-action champagne gold with dark navy text, matching the supplied reference.
css = re.sub(
    r"background:\s*linear-gradient\(135deg,\s*#ffd36a 0%,\s*#f2bd4b 52%,\s*#d99a20 100%\)\s*!important;",
    "background: linear-gradient(135deg, #ffe08a 0%, #f2bd4b 52%, #dfa52c 100%) !important;",
    css
)
# Handle values if original replacements changed the exact declaration differently.
css = re.sub(
    r"background:\s*linear-gradient\(135deg,\s*#[0-9a-fA-F]{6}\s*0%,\s*#[0-9a-fA-F]{6}\s*52%,\s*#[0-9a-fA-F]{6}\s*100%\)\s*!important;",
    "background: linear-gradient(135deg, #ffe08a 0%, #f2bd4b 52%, #dfa52c 100%) !important;",
    css
)
# The gold CTA should have dark navy lettering for the crisp high-end reference look.
css = css.replace("color: #fff !important;\n  font-family: 'DM Sans'", "color: #06182b !important;\n  font-family: 'DM Sans'")
css = css.replace("color: #fff !important;\n  box-shadow: 0 9px 20px", "color: #06182b !important;\n  box-shadow: 0 9px 20px")
css = css.replace("rgba(49,94,251,.23)", "rgba(200,138,22,.24)")
css = css.replace("rgba(49,94,251,.3)", "rgba(200,138,22,.30)")
css = css.replace("rgba(49,94,251,.2)", "rgba(200,138,22,.20)")
# Keep outline button dark/transparent and white text over the hero.
css = css.replace("background: rgba(255,255,255,.045) !important;", "background: rgba(6,24,43,.32) !important;")
css = css.replace("border: 1px solid rgba(255,255,255,.48) !important;", "border: 1px solid rgba(255,255,255,.72) !important;")
css = css.replace("color: #06182b !important;\n  box-shadow: inset 0 1px 0 rgba(255,255,255,.08);", "color: #fff !important;\n  box-shadow: inset 0 1px 0 rgba(255,255,255,.08);")
# Set gold accent lines/icons and warm off-white surfaces consistently.
css += r"""

/* Reference-match finishing pass: navy + champagne gold + warm ivory */
.ss-home .ss-overline,
.ss-home .ss-eyebrow,
.ss-home .ss-hero-kicker,
.ss-home .ss-intro-signature,
.ss-home .ss-text-link,
.ss-home .ss-capacity-link { color: #c88a16 !important; }
.ss-home .ss-eyebrow span,
.ss-home .ss-hero-bottomline i,
.ss-home .ss-gold-rule,
.ss-home .ss-gold-rule:after { background: #f2bd4b !important; }
.ss-home .ss-hero h1 em,
.ss-home .ss-section h2 em,
.ss-home .ss-intro-copy h2 em,
.ss-home .ss-gallery-header h2 em,
.ss-home .ss-closing-cta h2 em { color: #ffd978 !important; }
.ss-home .ss-navbar,
.ss-home .ss-gallery-section,
.ss-home .ss-footer { background-color: #06182b !important; }
.ss-home .ss-facilities-section,
.ss-home .ss-capacity-wrap,
.ss-home { background-color: #fbf8f1 !important; }
.ss-home .ss-facility-card[class*="tint-"] {
  border-color: #eee5d6 !important;
  box-shadow: 0 8px 24px rgba(6,24,43,.055), 0 2px 5px rgba(6,24,43,.025) !important;
}
.ss-home .ss-button:not(.ss-button-outline),
.ss-home .ss-nav-cta,
.ss-home .ss-ca-preview-cta,
.ca-page .ca-primary-button,
.booking-page .booking-submit {
  background: linear-gradient(135deg, #ffe08a 0%, #f2bd4b 55%, #dfa52c 100%) !important;
  color: #06182b !important;
  border: 1px solid rgba(255,255,255,.58) !important;
  border-radius: 12px !important;
  box-shadow: 0 7px 0 rgba(151,99,10,.13), 0 12px 24px rgba(151,99,10,.20), inset 0 1px 0 rgba(255,255,255,.65) !important;
  font-weight: 800 !important;
  letter-spacing: .01em;
  transition: transform .2s ease, box-shadow .2s ease, filter .2s ease !important;
}
.ss-home .ss-button:not(.ss-button-outline):hover,
.ss-home .ss-nav-cta:hover,
.ss-home .ss-ca-preview-cta:hover,
.ca-page .ca-primary-button:hover,
.booking-page .booking-submit:hover {
  transform: translateY(-2px) !important;
  filter: saturate(1.06) brightness(1.025);
  box-shadow: 0 9px 0 rgba(151,99,10,.10), 0 17px 30px rgba(151,99,10,.25), inset 0 1px 0 rgba(255,255,255,.72) !important;
}
.ss-home .ss-button:not(.ss-button-outline):active,
.ss-home .ss-nav-cta:active,
.ss-home .ss-ca-preview-cta:active,
.ca-page .ca-primary-button:active,
.booking-page .booking-submit:active {
  transform: translateY(1px) scale(.99) !important;
  box-shadow: 0 3px 0 rgba(151,99,10,.12), 0 5px 12px rgba(151,99,10,.14) !important;
}
.ss-home .ss-button-outline {
  background: rgba(6,24,43,.40) !important;
  color: #fff !important;
  border: 1px solid rgba(255,255,255,.76) !important;
  border-radius: 12px !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.14), 0 8px 20px rgba(0,0,0,.12) !important;
}
.ss-home .ss-button-outline:hover { background: rgba(255,255,255,.12) !important; border-color: #ffd978 !important; }
.ca-page, .booking-page { background: #fbf8f1 !important; }
.ca-category-tabs button.is-active,
.booking-seat.is-selected { background: linear-gradient(135deg,#ffe08a,#f2bd4b 55%,#dfa52c) !important; color: #06182b !important; border-color: #dfa52c !important; }
.ca-quiz-panel, .ss-home .ss-ca-preview, .booking-hero {
  background: radial-gradient(circle at 86% 10%, #193b58 0, transparent 38%), linear-gradient(120deg,#0b2238,#06182b) !important;
}
.ca-primary-button { color: #06182b !important; }
@media (max-width: 760px) {
  .ss-home .ss-nav-links { background: #06182b !important; }
  .ss-home .ss-button, .ss-home .ss-nav-cta, .ss-home .ss-ca-preview-cta,
  .ca-page .ca-primary-button, .booking-page .booking-submit { min-height: 49px; }
}
"""
theme.write_text(css, encoding="utf-8")
print("SUCCESS: Applied screenshot-inspired midnight navy + champagne gold + warm ivory theme.")
print("Backup:", backup_dir / "theme-premium.css")
print("Only src/theme-premium.css changed. Now run: npm run build")
