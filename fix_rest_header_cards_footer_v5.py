#!/usr/bin/env python3
"""Fix the actual homepage CSS: dark devotional header, saturated animated liquid cards, soft water footer.
Does not edit Home.jsx, video/embed markup, registration logic, or other pages.
"""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
css_path = ROOT / "src" / "Home.css"
jsx_path = ROOT / "src" / "Home.jsx"
if not css_path.is_file() or not jsx_path.is_file():
    print("ERROR: Run from ~/shri-shyam-library.")
    sys.exit(1)

css = css_path.read_text(encoding="utf-8")
jsx = jsx_path.read_text(encoding="utf-8")
required = [
    "ss-navbar", "ss-facility-icon-tile", "ss-facility-icon-art",
    "ss-facility-english-copy", "ss-footer"
]
missing = [token for token in required if token not in css]
if missing:
    print("ERROR: Missing expected Home.css selectors: " + ", ".join(missing))
    print("No files changed.")
    sys.exit(1)
if "ss-facility-icon-tile" not in jsx or "ss-facility-icon-grid" not in jsx:
    print("ERROR: The expected 10-feature card markup is not in Home.jsx. No files changed.")
    sys.exit(1)

marker = "/* FINAL VISUAL REPAIR V5: DEVOTIONAL HEADER + VIVID LIQUID CARDS + WATER FOOTER */"
if marker in css:
    print("ERROR: V5 repair has already been applied. No files changed.")
    sys.exit(1)

css_fix = r"""

/* FINAL VISUAL REPAIR V5: DEVOTIONAL HEADER + VIVID LIQUID CARDS + WATER FOOTER */

/* WIDE devotional header: obsidian-black, midnight navy and a subtle gold diya glow. */
.ss-navbar{
  width:100%!important;
  min-height:92px!important;
  height:auto!important;
  padding:11px clamp(14px,3.5vw,58px)!important;
  gap:clamp(12px,2vw,28px)!important;
  isolation:isolate!important;
  background:
    radial-gradient(ellipse at 8% 0%,rgba(211,171,83,.17),transparent 30%),
    radial-gradient(ellipse at 78% 115%,rgba(39,100,125,.18),transparent 38%),
    linear-gradient(112deg,#030509 0%,#070c14 42%,#0b1722 76%,#0e0d0d 100%)!important;
  color:#fff5d8!important;
  border-bottom:1px solid rgba(229,192,111,.82)!important;
  box-shadow:0 8px 27px rgba(0,0,0,.42),inset 0 1px rgba(255,255,255,.10)!important;
}
.ss-navbar::before{
  content:""!important;
  position:absolute!important;
  inset:0!important;
  z-index:-1!important;
  pointer-events:none!important;
  opacity:.3!important;
  background:
    radial-gradient(circle at 12% 25%,rgba(246,218,147,.72) 0 1px,transparent 2px),
    radial-gradient(circle at 30% 72%,rgba(246,218,147,.5) 0 1px,transparent 2px),
    radial-gradient(circle at 82% 32%,rgba(145,228,239,.52) 0 1px,transparent 2px),
    linear-gradient(90deg,transparent,rgba(255,255,255,.045),transparent)!important;
}
.ss-navbar .ss-brand-lockup{gap:11px!important;min-width:0!important}
.ss-navbar .ss-brand-emblem{
  flex:0 0 54px!important;
  width:54px!important;height:54px!important;
  border-radius:17px!important;
  background:radial-gradient(circle at 30% 18%,#29485f 0%,#0e1a26 52%,#020407 100%)!important;
  border:1px solid rgba(245,215,137,.9)!important;
  box-shadow:inset 0 1px 2px rgba(255,255,255,.28),inset 0 -8px 15px rgba(0,0,0,.48),0 0 0 3px rgba(212,169,84,.10),0 7px 17px rgba(0,0,0,.48)!important;
}
.ss-navbar .ss-brand-shri{
  font-size:28px!important;
  color:#ffe8a5!important;
  text-shadow:0 1px 0 #fff7d5,0 2px 0 #bf8b32,0 4px 0 #704719,0 7px 12px rgba(0,0,0,.72)!important;
}
.ss-navbar .ss-brand-words{gap:4px!important;min-width:0}
.ss-navbar .ss-brand-words strong{
  color:#fbf2db!important;
  font-size:clamp(16px,1.45vw,22px)!important;
  text-shadow:0 1px 0 rgba(255,255,255,.10),0 3px 7px rgba(0,0,0,.64)!important;
}
.ss-navbar .ss-brand-words strong span{
  color:#f9d783!important;
  text-shadow:0 1px 0 #fff0c0,0 2px 0 #b7812d,0 4px 0 #654016,0 7px 12px rgba(0,0,0,.68)!important;
}
.ss-navbar .ss-brand-words small{color:#c7d0d7!important;font-size:7px!important;letter-spacing:1px!important}
.ss-navbar .ss-nav-links{color:#f1e7d2!important;gap:clamp(9px,1.35vw,20px)!important}
.ss-navbar .ss-nav-links>a:not(.ss-nav-cta){color:#eee4d1!important}
.ss-navbar .ss-nav-links>a:not(.ss-nav-cta):hover,
.ss-navbar .ss-nav-links>a.active{color:#f3d48a!important}
.ss-navbar .ss-nav-links>a.active:after{background:linear-gradient(90deg,#aa782d,#fff0b5,#aa782d)!important}
.ss-navbar .ss-nav-cta{
  background:linear-gradient(135deg,#fff0b6 0%,#e6bb5c 44%,#b67c24 100%)!important;
  border:1px solid #ffedb2!important;
  box-shadow:0 4px 0 #624218,0 8px 18px rgba(0,0,0,.34),inset 0 1px rgba(255,255,255,.93)!important;
}
.ss-navbar .ss-menu-toggle{
  color:#f7dfab!important;border:1px solid rgba(236,201,125,.55)!important;
  background:rgba(255,255,255,.035)!important;
}
@media(max-width:1050px){
 .ss-navbar{padding:10px 16px!important;gap:10px!important}
 .ss-navbar .ss-nav-links{gap:9px!important}
}
@media(max-width:760px){
 .ss-navbar{min-height:78px!important;height:auto!important;padding:9px 12px!important;gap:8px!important}
 .ss-navbar .ss-brand-lockup{gap:7px!important}
 .ss-navbar .ss-brand-emblem{width:43px!important;height:43px!important;flex-basis:43px!important;border-radius:14px!important}
 .ss-navbar .ss-brand-shri{font-size:23px!important}
 .ss-navbar .ss-brand-words strong{font-size:14px!important}
 .ss-navbar .ss-brand-words small{font-size:5px!important;letter-spacing:.55px!important;white-space:normal!important}
 .ss-navbar .ss-menu-toggle{width:39px!important;height:39px!important;flex:0 0 39px!important}
 .ss-navbar .ss-nav-links.is-open{
   background:linear-gradient(145deg,#05070c,#0b1722 72%,#17120b)!important;
   border:1px solid rgba(229,192,111,.6)!important;
   box-shadow:0 18px 38px rgba(0,0,0,.65)!important;
 }
}

/* The facilities stage stays quiet. Animated light stays CLIPPED inside each tile. */
.ss-facilities-section{
  position:relative!important;
  isolation:isolate!important;
  background:linear-gradient(180deg,#fffaf1 0%,#f8f7f1 50%,#edf5fa 100%)!important;
}
.ss-facilities-section::before{opacity:.11!important;filter:none!important}
.ss-facilities-section::after{opacity:.09!important;filter:blur(18px)!important}

.ss-facility-icon-grid .ss-facility-icon-tile{
  position:relative!important;
  isolation:isolate!important;
  overflow:hidden!important;
  color:#fff!important;
  border:1px solid rgba(255,255,255,.72)!important;
  background-size:140% 140%!important;
  box-shadow:0 14px 29px rgba(5,18,38,.24),inset 0 1px 0 rgba(255,255,255,.4),inset 0 -16px 26px rgba(0,0,0,.24)!important;
  animation:featureColorBreatheV5 11s ease-in-out infinite alternate!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(1){
  --liquid-hot:#70ffe0;
  background:radial-gradient(ellipse at 70% 0%,rgba(106,255,211,.95),transparent 34%),linear-gradient(145deg,#00bd91 0%,#067c72 52%,#00353b 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(2){
  --liquid-hot:#ffd17a;
  background:radial-gradient(ellipse at 64% 0%,rgba(255,209,112,.95),transparent 32%),radial-gradient(ellipse at 30% 100%,rgba(255,76,12,.72),transparent 43%),linear-gradient(145deg,#ffae36 0%,#d95317 52%,#40160d 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(3){
  --liquid-hot:#62f7ff;
  background:radial-gradient(ellipse at 50% 0%,rgba(92,244,255,.94),transparent 32%),linear-gradient(145deg,#12b9f3 0%,#075bb6 51%,#05234f 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(4){
  --liquid-hot:#efa9ff;
  background:radial-gradient(ellipse at 74% 0%,rgba(232,145,255,.95),transparent 33%),linear-gradient(145deg,#8d4be5 0%,#4430b8 51%,#17143e 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(5){
  --liquid-hot:#ffb9e7;
  background:radial-gradient(ellipse at 48% 0%,rgba(255,143,202,.94),transparent 33%),linear-gradient(145deg,#f83f98 0%,#b31e70 50%,#421039 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(6){
  --liquid-hot:#fff487;
  background:radial-gradient(ellipse at 50% 0%,rgba(255,248,133,.98),transparent 33%),radial-gradient(ellipse at 82% 92%,rgba(255,100,14,.69),transparent 40%),linear-gradient(145deg,#ffda45 0%,#e59a0b 50%,#482008 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(7){
  --liquid-hot:#a3ffff;
  background:radial-gradient(ellipse at 50% 0%,rgba(156,255,255,.95),transparent 32%),linear-gradient(145deg,#20d5ef 0%,#0089c8 50%,#04396e 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(8){
  --liquid-hot:#adff86;
  background:radial-gradient(ellipse at 65% 0%,rgba(155,255,146,.95),transparent 34%),linear-gradient(145deg,#1bd66d 0%,#078550 50%,#00372d 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(9){
  --liquid-hot:#ffb8ff;
  background:radial-gradient(ellipse at 53% 0%,rgba(255,178,255,.96),transparent 32%),linear-gradient(145deg,#d753f5 0%,#8028bc 50%,#291047 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(10){
  --liquid-hot:#a6ffff;
  background:radial-gradient(ellipse at 85% 0%,rgba(255,104,224,.88),transparent 33%),radial-gradient(ellipse at 25% 0%,rgba(99,255,255,.92),transparent 32%),linear-gradient(145deg,#27d4f0 0%,#1a70d2 49%,#302579 100%)!important;
}

/* This is the moving-water/flame surface; it has no white veil over the text. */
.ss-facility-icon-grid .ss-facility-icon-tile::before{
  content:""!important;
  position:absolute!important;z-index:0!important;
  inset:-38%!important;left:-38%!important;top:-38%!important;
  width:auto!important;height:auto!important;
  pointer-events:none!important;
  opacity:.48!important;
  mix-blend-mode:screen!important;
  filter:saturate(1.45) blur(1.4px)!important;
  background:
    radial-gradient(ellipse at 24% 40%,rgba(255,255,255,.58) 0 1.2%,transparent 20%),
    radial-gradient(ellipse at 72% 31%,var(--liquid-hot) 0 2.4%,transparent 27%),
    repeating-radial-gradient(ellipse at 50% 105%,transparent 0 8px,rgba(255,255,255,.35) 9px 10px,rgba(0,0,0,.12) 11px 12px,transparent 13px 22px),
    conic-gradient(from 0deg at 50% 50%,transparent 0 12%,rgba(255,255,255,.17) 19%,transparent 29%,var(--liquid-hot) 38%,transparent 48%,rgba(255,255,255,.19) 58%,transparent 69%,var(--liquid-hot) 79%,transparent 90%,rgba(255,255,255,.15) 100%)!important;
  animation:featureLiquidFlowV5 12s ease-in-out infinite alternate!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile::after{
  content:""!important;
  position:absolute!important;z-index:0!important;
  width:130px!important;height:88px!important;
  left:50%!important;right:auto!important;top:auto!important;bottom:-45px!important;
  transform:translateX(-50%) rotate(-7deg)!important;
  border:1.5px solid rgba(255,255,255,.58)!important;
  border-radius:50%!important;
  opacity:.42!important;
  pointer-events:none!important;
  box-shadow:0 0 0 7px rgba(255,255,255,.075),0 0 0 15px rgba(255,255,255,.055),0 0 0 25px rgba(255,255,255,.035),inset 0 0 22px rgba(255,255,255,.08)!important;
  animation:featureRippleV5 6.5s ease-in-out infinite!important;
}

/* Keep icon glass tinted and translucent rather than opaque white. */
.ss-facility-icon-grid .ss-facility-icon-art{
  position:relative!important;z-index:2!important;
  color:#fff!important;
  background:radial-gradient(circle at 28% 18%,rgba(255,255,255,.45),rgba(255,255,255,.17) 25%,rgba(4,19,38,.30) 70%,rgba(0,0,0,.43) 100%)!important;
  border:1px solid rgba(255,255,255,.87)!important;
  box-shadow:0 0 0 2px rgba(255,255,255,.12),0 0 21px var(--liquid-hot),0 12px 25px rgba(0,0,0,.30),inset 0 2px 5px rgba(255,255,255,.46),inset 0 -9px 17px rgba(0,0,0,.25)!important;
  backdrop-filter:blur(2px)!important;
}
.ss-facility-icon-grid .ss-facility-icon-art svg{
  color:#fff!important;stroke-width:2.1!important;
  filter:drop-shadow(0 2px 3px rgba(0,0,0,.62))!important;
}
.ss-facility-icon-grid .ss-facility-number{
  z-index:3!important;color:#fff!important;opacity:1!important;
  text-shadow:0 2px 6px rgba(0,0,0,.72)!important;
}
.ss-facility-icon-grid .ss-facility-english-copy{position:relative!important;z-index:3!important}
.ss-facility-icon-grid .ss-facility-english-copy strong,
.ss-facility-icon-grid .ss-facility-english-copy small{
  color:#fff!important;
  text-shadow:0 1px 2px rgba(0,0,0,.78),0 0 7px rgba(0,0,0,.32)!important;
}
.ss-facility-icon-grid .ss-facility-english-copy strong{font-size:12px!important;line-height:1.4!important}
.ss-facility-icon-grid .ss-facility-english-copy small{font-size:10px!important;line-height:1.5!important;opacity:1!important}

@keyframes featureLiquidFlowV5{
  0%{transform:translate3d(-4%,2%,0) rotate(-10deg) scale(1)}
  50%{transform:translate3d(2%,-3%,0) rotate(13deg) scale(1.08)}
  100%{transform:translate3d(5%,2%,0) rotate(28deg) scale(1.03)}
}
@keyframes featureRippleV5{
  0%,100%{opacity:.22;width:112px;bottom:-49px}
  50%{opacity:.48;width:154px;bottom:-42px}
}
@keyframes featureColorBreatheV5{
  0%,100%{background-position:0% 42%}
  50%{background-position:100% 58%}
}
@media(hover:hover) and (pointer:fine){
  .ss-facility-icon-grid .ss-facility-icon-tile:hover{
    transform:translateY(-4px) perspective(800px) rotateX(2deg)!important;
    box-shadow:0 23px 42px rgba(2,13,31,.32),0 0 20px color-mix(in srgb,var(--liquid-hot) 26%,transparent),inset 0 1px 0 rgba(255,255,255,.52)!important;
  }
}
@media(max-width:760px){
  .ss-facility-icon-grid .ss-facility-icon-tile{min-height:194px!important;animation-duration:13s!important}
  .ss-facility-icon-grid .ss-facility-icon-tile::before{opacity:.43!important;animation-duration:15s!important}
  .ss-facility-icon-grid .ss-facility-icon-tile::after{animation-duration:8s!important}
  .ss-facility-icon-grid .ss-facility-english-copy strong{font-size:11px!important}
  .ss-facility-icon-grid .ss-facility-english-copy small{font-size:9px!important}
}

/* Footer: pale ivory/ice-blue water field, matching the reference without darkening copy. */
.ss-footer{
  position:relative!important;
  isolation:isolate!important;
  overflow:hidden!important;
  background:
    radial-gradient(ellipse at 7% 5%,rgba(255,255,255,.98),transparent 38%),
    radial-gradient(ellipse at 86% 100%,rgba(110,204,233,.27),transparent 42%),
    radial-gradient(ellipse at 98% 0%,rgba(239,195,106,.25),transparent 32%),
    linear-gradient(180deg,#fffdf5 0%,#edf5fa 56%,#fff8e9 100%)!important;
  color:#20384a!important;
  border-top:1px solid rgba(198,166,107,.45)!important;
}
.ss-footer::before{
  opacity:.43!important;
  background:repeating-radial-gradient(ellipse at 4% 115%,transparent 0 23px,rgba(95,177,211,.13) 24px 25px,transparent 26px 43px)!important;
  animation:footerWaterDriftV5 18s ease-in-out infinite alternate!important;
  pointer-events:none!important;
}
.ss-footer::after{
  opacity:.55!important;
  background:radial-gradient(ellipse at 85% 8%,rgba(255,255,255,.75),transparent 32%),linear-gradient(105deg,transparent 20%,rgba(234,196,116,.12) 46%,transparent 68%)!important;
  pointer-events:none!important;
}
.ss-footer .library-brand{--lb-copy:#17364a;--lb-subtle:#526d7c;--lb-gold:#a9772d}
.ss-footer .library-brand__name{color:#17364a!important;text-shadow:0 1px 0 white,0 2px 3px rgba(0,0,0,.12)!important}
.ss-footer .library-brand__tagline{color:#526d7c!important}
.ss-footer>p,.ss-footer>nav,.ss-footer .ss-copyright{position:relative;z-index:2;color:#425e70!important}
.ss-footer>nav a:hover{color:#a7772b!important}
@keyframes footerWaterDriftV5{
  0%{transform:translate3d(-2%,0,0) rotate(-2deg)}
  100%{transform:translate3d(2%,-1%,0) rotate(2deg)}
}
@media(prefers-reduced-motion:reduce){
  .ss-facility-icon-grid .ss-facility-icon-tile,
  .ss-facility-icon-grid .ss-facility-icon-tile::before,
  .ss-facility-icon-grid .ss-facility-icon-tile::after,
  .ss-footer::before{animation:none!important}
}
"""

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"home-visual-repair-v5-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(css_path, backup / "Home.css")
css_path.write_text(css.rstrip() + "\n\n" + css_fix, encoding="utf-8")

print("SUCCESS: visual repair V5 applied.")
print("Updated: black devotional header, all 10 saturated liquid/fire feature cards, pale water-wave footer.")
print("YouTube/video markup was not edited. Registration and seat-selection logic untouched.")
print("Changed only: src/Home.css")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Check the local page after a hard refresh. Do not commit/push until it is reviewed.")
