#!/usr/bin/env python3
"""Correct the over-bright liquid card styling while keeping each card's own animated color."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
jsx_path = ROOT / "src" / "Home.jsx"
css_path = ROOT / "src" / "Home.css"
if not jsx_path.exists() or not css_path.exists():
    print("ERROR: Run from ~/shri-shyam-library.")
    sys.exit(1)

jsx = jsx_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")
if "ss-facility-icon-tile" not in jsx or "ss-facility-icon-art" not in jsx:
    print("ERROR: Expected 10-feature icon cards were not found in Home.jsx. No files changed.")
    sys.exit(1)
if "ssLiquidCurrent" not in css or "ss-facility-icon-tile" not in css:
    print("ERROR: Liquid animation patch was not found in Home.css. No files changed.")
    sys.exit(1)

marker = "/* LIQUID PATCH CORRECTION V3 - SATURATED CARD COLOURS */"
if marker in css:
    print("ERROR: This corrective patch is already applied. No files changed.")
    sys.exit(1)

css_fix = r"""

/* LIQUID PATCH CORRECTION V3 - SATURATED CARD COLOURS */
/* The section keeps only a subtle ambient wash; the strong movement stays inside each card. */
.ss-facilities-section{
  background:linear-gradient(180deg,#fffaf0 0%,#f2f7fb 100%)!important;
}
.ss-facilities-section::before{
  opacity:.22!important;
  background:
    radial-gradient(ellipse at 8% 80%,rgba(91,190,224,.13),transparent 33%),
    radial-gradient(ellipse at 87% 18%,rgba(240,197,109,.16),transparent 30%),
    repeating-radial-gradient(ellipse at 10% 104%,transparent 0 27px,rgba(89,174,211,.08) 28px 29px,transparent 30px 48px)!important;
}
.ss-facilities-section::after{opacity:.32!important;filter:blur(9px)!important}

/* Force rich, readable color on every tile instead of the frosted-white wash. */
.ss-facility-icon-grid .ss-facility-icon-tile{
  color:#fff!important;
  border:1px solid rgba(255,255,255,.7)!important;
  box-shadow:0 14px 30px rgba(7,25,46,.18),inset 0 2px 0 rgba(255,255,255,.33),inset 0 -15px 28px rgba(0,0,0,.14)!important;
  background-size:180% 180%!important;
  background-position:0% 48%!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(1){
  --liquid-deep:#003e3e;--liquid-mid:#00a982;--liquid-hot:#67ffcf;
  background:radial-gradient(ellipse at 72% 2%,rgba(92,255,205,.93),transparent 35%),linear-gradient(145deg,#00c99a 0%,#078a7c 48%,#003540 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(2){
  --liquid-deep:#43180d;--liquid-mid:#f87518;--liquid-hot:#ffd07b;
  background:radial-gradient(ellipse at 68% 0%,rgba(255,203,110,.98),transparent 35%),linear-gradient(145deg,#ffb23d 0%,#e36c1b 44%,#482019 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(3){
  --liquid-deep:#062450;--liquid-mid:#0786dc;--liquid-hot:#55f4ff;
  background:radial-gradient(ellipse at 52% -5%,rgba(76,239,255,.9),transparent 33%),linear-gradient(145deg,#079fe9 0%,#075bb6 52%,#062650 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(4){
  --liquid-deep:#17144b;--liquid-mid:#6741dc;--liquid-hot:#f0adff;
  background:radial-gradient(ellipse at 72% 0%,rgba(214,156,255,.96),transparent 35%),linear-gradient(145deg,#7849ed 0%,#3542bc 51%,#151542 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(5){
  --liquid-deep:#4b103a;--liquid-mid:#e12b7b;--liquid-hot:#ffb9e9;
  background:radial-gradient(ellipse at 50% -3%,rgba(255,139,202,.95),transparent 35%),linear-gradient(145deg,#fb4099 0%,#b91d72 50%,#45113e 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(6){
  --liquid-deep:#492408;--liquid-mid:#e39a08;--liquid-hot:#fff37a;
  background:radial-gradient(ellipse at 50% -4%,rgba(255,247,125,.98),transparent 36%),linear-gradient(145deg,#ffda4d 0%,#e79c13 49%,#482309 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(7){
  --liquid-deep:#034574;--liquid-mid:#00afd3;--liquid-hot:#a5ffff;
  background:radial-gradient(ellipse at 50% -2%,rgba(155,255,255,.98),transparent 35%),linear-gradient(145deg,#20d9f4 0%,#008bc9 51%,#043a78 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(8){
  --liquid-deep:#00392e;--liquid-mid:#08b867;--liquid-hot:#a2ff84;
  background:radial-gradient(ellipse at 66% -2%,rgba(144,255,150,.96),transparent 34%),linear-gradient(145deg,#17d56e 0%,#008f57 50%,#00372f 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(9){
  --liquid-deep:#311154;--liquid-mid:#9a31d2;--liquid-hot:#ffbaff;
  background:radial-gradient(ellipse at 50% -1%,rgba(255,185,255,.96),transparent 34%),linear-gradient(145deg,#d457f1 0%,#7f2cba 49%,#29114c 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(10){
  --liquid-deep:#0b2872;--liquid-mid:#187de5;--liquid-hot:#a7ffff;
  background:radial-gradient(ellipse at 88% 0%,rgba(255,105,227,.86),transparent 36%),radial-gradient(ellipse at 30% 0%,rgba(101,255,255,.94),transparent 34%),linear-gradient(145deg,#2cd8f5 0%,#197bdc 47%,#30277d 100%)!important;
}

/* Liquid/flame currents live within their own tile and are less opaque. */
.ss-facility-icon-grid .ss-facility-icon-tile::before{
  inset:-34%!important;
  left:-34%!important;top:-34%!important;
  opacity:.46!important;
  mix-blend-mode:screen!important;
  filter:saturate(1.2)!important;
  background:
    radial-gradient(ellipse at 25% 60%,rgba(255,255,255,.28) 0 2%,transparent 23%),
    radial-gradient(ellipse at 72% 35%,var(--liquid-hot) 0 4%,transparent 28%),
    repeating-radial-gradient(ellipse at 50% 105%,transparent 0 11px,rgba(255,255,255,.25) 12px 13px,rgba(0,0,0,.13) 14px 15px,transparent 16px 27px),
    conic-gradient(from 15deg at 50% 50%,transparent 0 15%,rgba(255,255,255,.12) 21%,transparent 31%,var(--liquid-hot) 39%,transparent 48%,rgba(255,255,255,.14) 57%,transparent 67%,var(--liquid-hot) 76%,transparent 86%,rgba(255,255,255,.12) 94%,transparent 100%)!important;
  animation:ssLiquidCurrent var(--liquid-speed,17s) ease-in-out infinite alternate!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile::after{
  inset:auto 5% -34% 5%!important;
  height:77%!important;
  border:2px solid rgba(255,255,255,.47)!important;
  opacity:.42!important;
  box-shadow:0 0 0 5px rgba(255,255,255,.075),0 0 0 12px rgba(255,255,255,.065),0 0 0 21px rgba(255,255,255,.045),inset 0 0 22px rgba(255,255,255,.09)!important;
  animation:ssLiquidRipple 8s ease-in-out infinite!important;
}

/* Use tinted translucent glass, not a nearly opaque white bubble. */
.ss-facility-icon-grid .ss-facility-icon-art{
  color:#fff!important;
  background:radial-gradient(circle at 28% 18%,rgba(255,255,255,.40),rgba(255,255,255,.14) 27%,rgba(7,24,48,.28) 68%,rgba(0,0,0,.39) 100%)!important;
  border:1px solid rgba(255,255,255,.88)!important;
  box-shadow:0 0 0 2px rgba(255,255,255,.10),0 0 20px var(--liquid-hot),0 12px 28px rgba(0,0,0,.24),inset 0 2px 5px rgba(255,255,255,.45),inset 0 -9px 17px rgba(0,0,0,.22)!important;
}
.ss-facility-icon-grid .ss-facility-icon-art svg{
  color:#fff!important;
  stroke-width:2.15!important;
  filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))!important;
}
.ss-facility-icon-grid .ss-facility-number{
  color:#fff!important;
  text-shadow:0 2px 5px rgba(0,0,0,.45)!important;
  opacity:1!important;
}
.ss-facility-icon-grid .ss-facility-english-copy strong,
.ss-facility-icon-grid .ss-facility-english-copy small{
  color:#fff!important;
  text-shadow:0 1px 2px rgba(0,0,0,.55),0 0 8px rgba(0,0,0,.20)!important;
}
.ss-facility-icon-grid .ss-facility-english-copy small{opacity:.96!important}
.ss-facility-icon-grid .ss-facility-icon-tile:hover{
  filter:saturate(1.12) contrast(1.03)!important;
  transform:translateY(-4px) scale(1.01)!important;
  box-shadow:0 22px 42px rgba(3,18,40,.26),0 0 22px color-mix(in srgb,var(--liquid-hot) 32%,transparent),inset 0 2px 0 rgba(255,255,255,.48)!important;
}

/* Keep the footer's reference-inspired water/champagne waves soft and the text legible. */
.ss-footer{
  background:
    radial-gradient(ellipse at 8% 0%,rgba(255,255,255,.98),transparent 36%),
    radial-gradient(ellipse at 82% 105%,rgba(103,194,225,.28),transparent 40%),
    radial-gradient(ellipse at 98% 3%,rgba(243,202,115,.27),transparent 33%),
    linear-gradient(180deg,#fffdf6 0%,#edf5fb 57%,#fff8e8 100%)!important;
  color:#183349!important;
}
.ss-footer::before{opacity:.45!important;inset:-65% -30%!important}
.ss-footer::after{opacity:.55!important}
.ss-footer .library-brand{--lb-copy:#17374c;--lb-subtle:#506c7e;--lb-gold:#b9822c}
.ss-footer .library-brand__name{color:#17374c!important;text-shadow:0 1px 0 rgba(255,255,255,.9),0 2px 3px rgba(0,0,0,.12)!important}
.ss-footer .library-brand__tagline{color:#526879!important}
@media(max-width:760px){
  .ss-facility-icon-grid .ss-facility-icon-tile{min-height:194px!important}
  .ss-footer::before{opacity:.34!important;inset:-50% -65%!important}
}
@media(prefers-reduced-motion:reduce){
  .ss-facility-icon-grid .ss-facility-icon-tile::before,
  .ss-facility-icon-grid .ss-facility-icon-tile::after{animation:none!important}
}
"""

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"liquid-cards-contrast-fix-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(css_path, backup / "Home.css")
css_path.write_text(css.rstrip() + "\n\n" + css_fix, encoding="utf-8")
print("SUCCESS: Liquid-card contrast correction applied.")
print("Each feature tile now has a stronger individual color; liquid currents are limited to tile interiors.")
print("Footer stays light cream/ice-blue with softer champagne water trails and readable branding.")
print("Changed only: src/Home.css")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Preview locally; do not commit/push until reviewed.")
