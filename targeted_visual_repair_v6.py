#!/usr/bin/env python3
"""High-specificity fix for the current Siri Library homepage: dark devotional header + rich animated liquid cards + pale water footer."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
home_css_path = ROOT / "src" / "Home.css"
home_jsx_path = ROOT / "src" / "Home.jsx"
if not home_css_path.is_file() or not home_jsx_path.is_file():
    print("ERROR: Run from ~/shri-shyam-library.")
    sys.exit(1)

css = home_css_path.read_text(encoding="utf-8")
jsx = home_jsx_path.read_text(encoding="utf-8")

checks = {
    "header": "ss-navbar" in css and "ss-brand-lockup" in jsx,
    "feature grid": "ss-facility-icon-grid" in jsx and "ss-facility-icon-tile" in jsx,
    "English labels": "ss-facility-english-copy" in jsx,
    "footer": "ss-footer" in jsx and "ss-footer" in css,
}
failed = [k for k, ok in checks.items() if not ok]
if failed:
    print("ERROR: Could not confirm current homepage structure: " + ", ".join(failed))
    print("No files changed.")
    sys.exit(1)

marker = "/* TARGETED REPAIR V6 - HIGH SPECIFICITY LIQUID CARDS */"
if marker in css:
    print("ERROR: V6 targeted repair already exists. No files changed.")
    sys.exit(1)

css_patch = r"""

/* TARGETED REPAIR V6 - HIGH SPECIFICITY LIQUID CARDS */

/* 1) Header: devotional obsidian / midnight navy with champagne light. */
body .ss-home header.ss-navbar{
  min-height:94px!important;
  height:auto!important;
  width:100%!important;
  padding:10px clamp(14px,3.5vw,56px)!important;
  gap:clamp(12px,2vw,25px)!important;
  color:#fdf4db!important;
  background:
    radial-gradient(ellipse at 8% -15%,rgba(223,180,91,.23),transparent 32%),
    radial-gradient(ellipse at 78% 120%,rgba(46,118,142,.20),transparent 39%),
    linear-gradient(110deg,#020409 0%,#080d16 43%,#0b1925 75%,#0c0b0a 100%)!important;
  border-bottom:1px solid #d8b66c!important;
  box-shadow:0 9px 28px rgba(0,0,0,.48),inset 0 1px rgba(255,255,255,.1)!important;
}
body .ss-home header.ss-navbar::before{
  opacity:.22!important;
  background:
    radial-gradient(circle at 13% 28%,rgba(255,230,162,.85) 0 1px,transparent 2px),
    radial-gradient(circle at 27% 73%,rgba(255,230,162,.55) 0 1px,transparent 2px),
    radial-gradient(circle at 84% 30%,rgba(143,235,239,.7) 0 1px,transparent 2px)!important;
}
body .ss-home header.ss-navbar .ss-brand-emblem{
  border:1px solid rgba(244,214,136,.95)!important;
  background:radial-gradient(circle at 28% 18%,#2b4d62 0%,#101b27 48%,#020408 100%)!important;
  box-shadow:inset 0 1px 2px rgba(255,255,255,.3),inset 0 -8px 15px rgba(0,0,0,.5),0 0 0 3px rgba(221,177,90,.10),0 8px 17px rgba(0,0,0,.48)!important;
}
body .ss-home header.ss-navbar .ss-brand-shri,
body .ss-home header.ss-navbar .ss-brand-words strong span{
  color:#ffdf8c!important;
  text-shadow:0 1px 0 #fff4c6,0 2px 0 #b7832c,0 4px 0 #704517,0 7px 12px rgba(0,0,0,.72)!important;
}
body .ss-home header.ss-navbar .ss-brand-words strong{
  color:#fff4df!important;
  text-shadow:0 2px 5px rgba(0,0,0,.7)!important;
}
body .ss-home header.ss-navbar .ss-brand-words small{color:#c7d5df!important}
body .ss-home header.ss-navbar .ss-nav-links{color:#f1e7d2!important}
body .ss-home header.ss-navbar .ss-nav-links>a:not(.ss-nav-cta){color:#eee5d2!important}
body .ss-home header.ss-navbar .ss-nav-links>a.active,
body .ss-home header.ss-navbar .ss-nav-links>a:not(.ss-nav-cta):hover{color:#f4d58b!important}
body .ss-home header.ss-navbar .ss-nav-links>a.active:after{background:linear-gradient(90deg,#a8792b,#fff0b4,#a8792b)!important}
body .ss-home header.ss-navbar .ss-nav-cta{
  color:#1c2934!important;
  background:linear-gradient(135deg,#fff0b8,#e5b954 53%,#b77a20)!important;
  border:1px solid #ffedb6!important;
  box-shadow:0 4px 0 #69471b,0 8px 18px rgba(0,0,0,.38),inset 0 1px rgba(255,255,255,.95)!important;
}
@media(max-width:760px){
  body .ss-home header.ss-navbar{min-height:76px!important;padding:8px 12px!important;gap:8px!important}
  body .ss-home header.ss-navbar .ss-brand-emblem{width:43px;height:43px;flex-basis:43px}
  body .ss-home header.ss-navbar .ss-brand-words strong{font-size:14px!important}
  body .ss-home header.ss-navbar .ss-brand-words small{font-size:5px!important;letter-spacing:.55px!important}
  body .ss-home header.ss-navbar .ss-nav-links.is-open{
    background:linear-gradient(145deg,#03060a,#0b1824 76%,#171108)!important;
    border:1px solid rgba(230,193,111,.62)!important;
  }
}

/* 2) Keep the section background calm; saturated animation is contained in each card. */
body .ss-home section.ss-facilities-section{
  position:relative!important;
  isolation:isolate!important;
  background:linear-gradient(180deg,#fffaf0 0%,#f8f8f2 48%,#edf5fa 100%)!important;
}
body .ss-home section.ss-facilities-section::before{opacity:.10!important;filter:none!important}
body .ss-home section.ss-facilities-section::after{opacity:.08!important;filter:blur(16px)!important}

body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{
  position:relative!important;
  isolation:isolate!important;
  overflow:hidden!important;
  color:#fff!important;
  border:1px solid rgba(255,255,255,.82)!important;
  background-size:150% 150%!important;
  box-shadow:0 15px 31px rgba(3,18,39,.24),inset 0 1px rgba(255,255,255,.4),inset 0 -16px 27px rgba(0,0,0,.25)!important;
  animation:targetLiquidColorV6 12s ease-in-out infinite alternate!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(1){
  --liquid-hot:#70ffe0;
  background:radial-gradient(ellipse at 68% 0%,rgba(92,255,207,.96),transparent 34%),linear-gradient(145deg,#00c99a 0%,#067d73 52%,#00343a 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(2){
  --liquid-hot:#ffd27d;
  background:radial-gradient(ellipse at 68% 0%,rgba(255,218,132,.98),transparent 30%),radial-gradient(ellipse at 32% 100%,rgba(255,74,8,.72),transparent 43%),linear-gradient(145deg,#ffb236 0%,#df5c18 50%,#43170d 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(3){
  --liquid-hot:#65f8ff;
  background:radial-gradient(ellipse at 50% 0%,rgba(83,244,255,.97),transparent 32%),linear-gradient(145deg,#13baf5 0%,#075cb8 50%,#05244f 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(4){
  --liquid-hot:#f0aaff;
  background:radial-gradient(ellipse at 72% 0%,rgba(231,147,255,.98),transparent 33%),linear-gradient(145deg,#944ceb 0%,#4530bb 50%,#17133f 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(5){
  --liquid-hot:#ffbce8;
  background:radial-gradient(ellipse at 50% 0%,rgba(255,146,205,.97),transparent 32%),linear-gradient(145deg,#f9419a 0%,#b41e70 52%,#401039 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(6){
  --liquid-hot:#fff48a;
  background:radial-gradient(ellipse at 50% 0%,rgba(255,248,129,.98),transparent 33%),radial-gradient(ellipse at 80% 95%,rgba(255,97,12,.7),transparent 41%),linear-gradient(145deg,#ffdc43 0%,#df9309 49%,#482008 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(7){
  --liquid-hot:#a5ffff;
  background:radial-gradient(ellipse at 50% 0%,rgba(158,255,255,.97),transparent 33%),linear-gradient(145deg,#25d7f1 0%,#008bca 51%,#04396e 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(8){
  --liquid-hot:#a5ff8b;
  background:radial-gradient(ellipse at 66% 0%,rgba(154,255,146,.97),transparent 34%),linear-gradient(145deg,#1cdd78 0%,#078651 51%,#00372e 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(9){
  --liquid-hot:#ffb6ff;
  background:radial-gradient(ellipse at 52% 0%,rgba(255,177,255,.98),transparent 32%),linear-gradient(145deg,#d956f5 0%,#8129bf 51%,#291049 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(10){
  --liquid-hot:#a5ffff;
  background:radial-gradient(ellipse at 86% 0%,rgba(255,102,223,.88),transparent 32%),radial-gradient(ellipse at 25% 0%,rgba(96,255,255,.94),transparent 31%),linear-gradient(145deg,#2ad7f1 0%,#1b70d2 48%,#302578 100%)!important;
}

/* Rippling water + flame-like highlights; no blanket white overlay. */
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::before{
  content:""!important;
  position:absolute!important;
  z-index:0!important;
  inset:-42%!important;
  top:-42%!important;left:-42%!important;
  width:auto!important;height:auto!important;
  opacity:.55!important;
  pointer-events:none!important;
  mix-blend-mode:screen!important;
  transform-origin:center!important;
  filter:blur(1.3px) saturate(1.4)!important;
  background:
    radial-gradient(ellipse at 22% 42%,rgba(255,255,255,.6) 0 1.4%,transparent 20%),
    radial-gradient(ellipse at 72% 29%,var(--liquid-hot) 0 2.2%,transparent 27%),
    repeating-radial-gradient(ellipse at 50% 103%,transparent 0 8px,rgba(255,255,255,.34) 9px 10px,rgba(0,0,0,.14) 11px 12px,transparent 13px 21px),
    conic-gradient(from 0deg at 50% 50%,transparent 0 12%,rgba(255,255,255,.17) 19%,transparent 29%,var(--liquid-hot) 38%,transparent 48%,rgba(255,255,255,.18) 58%,transparent 68%,var(--liquid-hot) 79%,transparent 90%,rgba(255,255,255,.15) 100%)!important;
  animation:targetLiquidSurfaceV6 12s ease-in-out infinite alternate!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::after{
  content:""!important;
  position:absolute!important;
  z-index:0!important;
  top:auto!important;left:50%!important;right:auto!important;bottom:-47px!important;
  width:136px!important;height:88px!important;
  transform:translateX(-50%) rotate(-7deg)!important;
  border:1.5px solid rgba(255,255,255,.60)!important;
  border-radius:50%!important;
  opacity:.45!important;
  pointer-events:none!important;
  box-shadow:0 0 0 7px rgba(255,255,255,.08),0 0 0 15px rgba(255,255,255,.055),0 0 0 25px rgba(255,255,255,.04),inset 0 0 21px rgba(255,255,255,.08)!important;
  animation:targetLiquidRippleV6 7s ease-in-out infinite!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art{
  position:relative!important;z-index:2!important;
  color:#fff!important;
  background:radial-gradient(circle at 28% 18%,rgba(255,255,255,.43),rgba(255,255,255,.15) 26%,rgba(4,19,38,.28) 70%,rgba(0,0,0,.43) 100%)!important;
  border:1px solid rgba(255,255,255,.9)!important;
  box-shadow:0 0 0 2px rgba(255,255,255,.12),0 0 22px var(--liquid-hot),0 12px 25px rgba(0,0,0,.31),inset 0 2px 5px rgba(255,255,255,.45),inset 0 -9px 17px rgba(0,0,0,.25)!important;
  backdrop-filter:blur(2px)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art svg{
  color:#fff!important;stroke-width:2.1!important;filter:drop-shadow(0 2px 3px rgba(0,0,0,.6))!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-number{
  z-index:3!important;color:#fff!important;opacity:1!important;text-shadow:0 2px 5px rgba(0,0,0,.72)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy{position:relative!important;z-index:3!important}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy strong,
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy small{
  color:#fff!important;text-shadow:0 1px 2px rgba(0,0,0,.76),0 0 8px rgba(0,0,0,.30)!important;opacity:1!important;
}
@keyframes targetLiquidSurfaceV6{
  0%{transform:translate3d(-4%,2%,0) rotate(-12deg) scale(1)}
  50%{transform:translate3d(2%,-3%,0) rotate(12deg) scale(1.07)}
  100%{transform:translate3d(5%,2%,0) rotate(28deg) scale(1.03)}
}
@keyframes targetLiquidRippleV6{
  0%,100%{opacity:.22;width:112px;bottom:-50px}
  50%{opacity:.5;width:158px;bottom:-42px}
}
@keyframes targetLiquidColorV6{
  0%,100%{background-position:0% 42%}
  50%{background-position:100% 58%}
}
@media(hover:hover) and (pointer:fine){
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:hover{
    transform:translateY(-5px) perspective(800px) rotateX(2deg)!important;
    box-shadow:0 22px 40px rgba(2,13,31,.3),0 0 18px color-mix(in srgb,var(--liquid-hot) 24%,transparent),inset 0 1px rgba(255,255,255,.5)!important;
  }
}
@media(max-width:760px){
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{min-height:194px!important;animation-duration:13s!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::before{opacity:.43!important;animation-duration:15s!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::after{animation-duration:8s!important}
}

/* Footer: reference-style ivory/ice-blue luminous waves instead of solid black. */
body .ss-home footer.ss-footer{
  position:relative!important;isolation:isolate!important;overflow:hidden!important;
  background:
    radial-gradient(ellipse at 7% 0%,rgba(255,255,255,.98),transparent 38%),
    radial-gradient(ellipse at 85% 105%,rgba(98,196,227,.30),transparent 42%),
    radial-gradient(ellipse at 98% 3%,rgba(240,194,104,.28),transparent 32%),
    linear-gradient(180deg,#fffdf6 0%,#edf5fb 56%,#fff8e9 100%)!important;
  color:#17384d!important;border-top:1px solid rgba(198,166,107,.5)!important;
}
body .ss-home footer.ss-footer::before{
  opacity:.42!important;
  background:repeating-radial-gradient(ellipse at 4% 116%,transparent 0 23px,rgba(79,171,210,.15) 24px 25px,transparent 26px 43px)!important;
  animation:targetFooterWaterV6 18s ease-in-out infinite alternate!important;pointer-events:none!important;
}
body .ss-home footer.ss-footer::after{
  opacity:.52!important;
  background:radial-gradient(ellipse at 84% 8%,rgba(255,255,255,.78),transparent 32%),linear-gradient(105deg,transparent 20%,rgba(234,196,116,.14) 46%,transparent 68%)!important;
  pointer-events:none!important;
}
body .ss-home footer.ss-footer .ss-brand-words strong{color:#17384d!important;text-shadow:0 1px 0 #fff,0 2px 3px rgba(0,0,0,.12)!important}
body .ss-home footer.ss-footer .ss-brand-words small{color:#526d7e!important}
body .ss-home footer.ss-footer>p,
body .ss-home footer.ss-footer>nav,
body .ss-home footer.ss-footer>.ss-copyright{position:relative;z-index:2;color:#425f71!important}
body .ss-home footer.ss-footer>nav a:hover{color:#a7772b!important}
@keyframes targetFooterWaterV6{
  0%{transform:translate3d(-2%,0,0) rotate(-2deg)}
  100%{transform:translate3d(2%,-1%,0) rotate(2deg)}
}
@media(prefers-reduced-motion:reduce){
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile,
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::before,
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::after,
  body .ss-home footer.ss-footer::before{animation:none!important}
}
"""

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"targeted-visual-repair-v6-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(home_css_path, backup / "Home.css")
home_css_path.write_text(css.rstrip() + "\n\n" + css_patch, encoding="utf-8")
print("SUCCESS: V6 targeted visual repair applied to src/Home.css.")
print("Header: obsidian black / midnight navy devotional style with gold edge.")
print("Cards: 10 high-specificity saturated liquid/fire gradients + moving ripple layers; no white haze overlay.")
print("Footer: light ice-blue/champagne water-wave finish.")
print("Untouched: Home.jsx, YouTube video, feature labels, Contact Us, registration and seat-selection logic.")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Hard-refresh the local browser to verify.")
