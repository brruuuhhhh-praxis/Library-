#!/usr/bin/env python3
"""V7 responsive layout repair: bigger devotional header + legible colorful liquid cards."""
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
checks = {
    "header": "ss-navbar" in css and "ss-brand-lockup" in jsx,
    "feature grid": "ss-facility-icon-grid" in jsx and "ss-facility-icon-tile" in jsx,
    "feature copy": "ss-facility-english-copy" in jsx,
    "menu toggle": "ss-menu-toggle" in jsx and "ss-nav-links" in jsx,
}
missing = [key for key, ok in checks.items() if not ok]
if missing:
    print("ERROR: Expected homepage structure not found: " + ", ".join(missing))
    print("No files changed.")
    sys.exit(1)

marker = "/* V7 RESPONSIVE PREMIUM REPAIR: HEADER + 2-COLUMN LIQUID CARDS */"
if marker in css:
    print("ERROR: V7 patch already applied. No files changed.")
    sys.exit(1)

patch = r"""

/* V7 RESPONSIVE PREMIUM REPAIR: HEADER + 2-COLUMN LIQUID CARDS */

/* Preserve the rich rainbow-liquid palette, but restore an intentional premium layout. */
.ss-navbar{
  position:relative!important;
  z-index:50!important;
  min-height:98px!important;
  height:auto!important;
  width:100%!important;
  padding:12px clamp(18px,3.5vw,58px)!important;
  gap:clamp(18px,2.6vw,38px)!important;
  background:
    radial-gradient(ellipse at 8% 0%,rgba(238,194,105,.22),transparent 31%),
    radial-gradient(ellipse at 78% 118%,rgba(53,125,148,.22),transparent 40%),
    linear-gradient(112deg,#020307 0%,#080d16 42%,#0b1925 76%,#100d0c 100%)!important;
  border-bottom:1px solid #e0ba6b!important;
  box-shadow:0 8px 28px rgba(0,0,0,.42),inset 0 1px rgba(255,255,255,.12)!important;
  color:#fff3d2!important;
}
.ss-navbar::before{
  opacity:.32!important;
  pointer-events:none!important;
  background:
    radial-gradient(circle at 12% 26%,rgba(255,225,145,.7) 0 1px,transparent 2px),
    radial-gradient(circle at 24% 76%,rgba(255,225,145,.55) 0 1px,transparent 2px),
    radial-gradient(circle at 82% 31%,rgba(128,229,239,.68) 0 1px,transparent 2px),
    linear-gradient(90deg,transparent,rgba(255,255,255,.035),transparent)!important;
}
.ss-navbar::after{
  content:""!important;position:absolute!important;bottom:-1px!important;left:0!important;right:0!important;height:1px!important;
  background:linear-gradient(90deg,transparent,#b98734 15%,#fff0b5 50%,#b98734 85%,transparent)!important;
  pointer-events:none!important;
}
.ss-navbar .ss-brand{flex:0 0 auto!important;min-width:0!important;max-width:100%!important;position:relative!important;z-index:2!important}
.ss-navbar .ss-brand-lockup{display:flex!important;align-items:center!important;gap:13px!important;min-width:0!important}
.ss-navbar .ss-brand-emblem{
  flex:0 0 58px!important;width:58px!important;height:58px!important;border-radius:18px!important;
  border:1px solid rgba(248,218,143,.94)!important;
  background:radial-gradient(circle at 28% 18%,#2c4e63 0%,#101a27 50%,#020407 100%)!important;
  box-shadow:inset 0 1px 2px rgba(255,255,255,.30),inset 0 -8px 15px rgba(0,0,0,.5),0 0 0 3px rgba(220,176,86,.11),0 8px 20px rgba(0,0,0,.5)!important;
}
.ss-navbar .ss-brand-shri{
  font-size:30px!important;color:#ffdfa0!important;
  text-shadow:0 1px 0 #fff5d5,0 2px 0 #b9822f,0 4px 0 #704719,0 7px 12px rgba(0,0,0,.75)!important;
}
.ss-navbar .ss-brand-ai{color:#9af0e8!important;filter:drop-shadow(0 0 5px #5ee4da)!important}
.ss-navbar .ss-brand-words{display:flex!important;flex-direction:column!important;gap:5px!important;min-width:0!important}
.ss-navbar .ss-brand-words strong{
  font-size:clamp(19px,1.65vw,25px)!important;line-height:1.25!important;
  color:#fff5df!important;letter-spacing:-.3px!important;
  text-shadow:0 2px 6px rgba(0,0,0,.68)!important;
}
.ss-navbar .ss-brand-words strong span{
  font-size:1.35em!important;color:#f6d486!important;
  text-shadow:0 1px 0 #fff0bd,0 2px 0 #b7832c,0 4px 0 #6e4518,0 7px 12px rgba(0,0,0,.68)!important;
}
.ss-navbar .ss-brand-words small{
  color:#cbd6df!important;font-size:8px!important;line-height:1.35!important;
  letter-spacing:1.15px!important;white-space:nowrap!important;
}
.ss-navbar .ss-nav-links{position:relative!important;z-index:2!important;gap:clamp(10px,1.25vw,19px)!important;color:#f2e8d1!important}
.ss-navbar .ss-nav-links>a:not(.ss-nav-cta){color:#eee5d2!important}
.ss-navbar .ss-nav-links>a.active,.ss-navbar .ss-nav-links>a:not(.ss-nav-cta):hover{color:#f5d892!important}
.ss-navbar .ss-nav-links>a.active:after{background:linear-gradient(90deg,#a7762a,#fff0b5,#a7762a)!important}
.ss-navbar .ss-nav-cta{
  padding:12px 18px!important;border-radius:12px!important;
  color:#172637!important;background:linear-gradient(135deg,#fff0b9 0%,#e7bd61 48%,#b57a22 100%)!important;
  border:1px solid #ffecb0!important;
  box-shadow:0 4px 0 #674719,0 8px 17px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.95)!important;
}
.ss-navbar .ss-menu-toggle{display:none!important;color:#f6dfaa!important;border:1px solid #e2bd6e77!important;background:#ffffff08!important}

/* When Chrome uses a desktop-width viewport on a phone, switch to a real mobile nav/grid. */
@media(max-width:1050px){
  .ss-navbar{min-height:88px!important;padding:10px 17px!important;gap:12px!important}
  .ss-navbar .ss-brand{max-width:calc(100% - 54px)!important;flex:1 1 auto!important}
  .ss-navbar .ss-brand-lockup{gap:10px!important}
  .ss-navbar .ss-brand-emblem{width:51px!important;height:51px!important;flex-basis:51px!important}
  .ss-navbar .ss-brand-shri{font-size:27px!important}
  .ss-navbar .ss-brand-words strong{font-size:20px!important}
  .ss-navbar .ss-brand-words small{font-size:7px!important;letter-spacing:.8px!important}
  .ss-navbar .ss-menu-toggle{
    display:grid!important;place-items:center!important;position:relative!important;z-index:5!important;
    flex:0 0 43px!important;width:43px!important;height:43px!important;border-radius:12px!important;
  }
  .ss-navbar .ss-nav-links{
    display:none!important;position:absolute!important;left:12px!important;right:12px!important;top:calc(100% + 7px)!important;
    flex-direction:column!important;align-items:stretch!important;gap:0!important;
    padding:12px!important;border:1px solid rgba(233,196,115,.62)!important;border-radius:17px!important;
    background:linear-gradient(145deg,#03060b 0%,#0c1925 72%,#181208 100%)!important;
    box-shadow:0 20px 42px rgba(0,0,0,.64)!important;
  }
  .ss-navbar .ss-nav-links.is-open{display:flex!important}
  .ss-navbar .ss-nav-links>a:not(.ss-nav-cta){padding:13px 10px!important;border-bottom:1px solid rgba(255,255,255,.09)!important;font-size:13px!important}
  .ss-navbar .ss-nav-links>a.active:after{display:none!important}
  .ss-navbar .ss-nav-links .ss-nav-cta{display:flex!important;justify-content:center!important;margin-top:10px!important}
  .ss-facilities-section .ss-facility-icon-grid{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
    grid-auto-rows:minmax(218px,auto)!important;
    gap:13px!important;
  }
}

/* Make the ten cards read like the reference: full-color liquid surfaces, strong titles, ample space. */
.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{
  min-width:0!important;min-height:218px!important;
  padding:24px 17px 17px!important;
  display:flex!important;flex-direction:column!important;
  align-items:stretch!important;justify-content:flex-start!important;gap:13px!important;
  border-radius:22px!important;overflow:hidden!important;isolation:isolate!important;
  color:#fff!important;
  box-shadow:0 15px 30px rgba(4,18,36,.20),inset 0 1px rgba(255,255,255,.44),inset 0 -14px 26px rgba(0,0,0,.18)!important;
}
.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art{
  align-self:center!important;flex:0 0 auto!important;
  width:78px!important;height:78px!important;border-radius:50%!important;
  color:#fff!important;
  background:radial-gradient(circle at 28% 17%,rgba(255,255,255,.55),rgba(255,255,255,.17) 27%,rgba(4,20,40,.25) 68%,rgba(0,0,0,.38) 100%)!important;
  border:1px solid rgba(255,255,255,.92)!important;
  box-shadow:0 0 0 3px rgba(255,255,255,.10),0 0 24px var(--liquid-hot),0 12px 24px rgba(0,0,0,.28),inset 0 2px 6px rgba(255,255,255,.48),inset 0 -9px 15px rgba(0,0,0,.23)!important;
}
.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art svg{
  width:39px!important;height:39px!important;color:#fff!important;stroke-width:2.05!important;
  filter:drop-shadow(0 2px 3px rgba(0,0,0,.6))!important;
}
.ss-facilities-section .ss-facility-icon-grid .ss-facility-number{
  position:absolute!important;left:16px!important;top:13px!important;z-index:4!important;
  font-size:10px!important;font-weight:900!important;letter-spacing:1.6px!important;
  color:#fff!important;opacity:1!important;text-shadow:0 2px 5px rgba(0,0,0,.8)!important;
}
.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy{
  position:relative!important;z-index:4!important;display:flex!important;flex-direction:column!important;
  align-items:flex-start!important;text-align:left!important;gap:6px!important;width:100%!important;
}
.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy strong{
  color:#fff!important;font-size:14px!important;font-weight:800!important;line-height:1.35!important;
  text-shadow:0 1px 2px rgba(0,0,0,.70),0 0 8px rgba(0,0,0,.18)!important;
}
.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy small{
  color:rgba(255,255,255,.96)!important;font-size:11px!important;line-height:1.55!important;
  text-shadow:0 1px 2px rgba(0,0,0,.72)!important;opacity:1!important;max-width:34ch!important;
}

/* Desktop/tablet 4-wide and phone/desktop-mode 2-wide layout. */
@media(min-width:1051px){
  .ss-facilities-section .ss-facility-icon-grid{
    grid-template-columns:repeat(4,minmax(0,1fr))!important;
    grid-auto-rows:minmax(230px,auto)!important;gap:16px!important;
  }
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{min-height:230px!important}
}
@media(max-width:1050px){
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{min-height:218px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art{width:72px!important;height:72px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art svg{width:36px!important;height:36px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy strong{font-size:13px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy small{font-size:10px!important}
}
@media(max-width:520px){
  .ss-navbar{min-height:80px!important;padding:8px 11px!important}
  .ss-navbar .ss-brand-emblem{width:44px!important;height:44px!important;flex-basis:44px!important}
  .ss-navbar .ss-brand-shri{font-size:24px!important}
  .ss-navbar .ss-brand-words strong{font-size:16px!important}
  .ss-navbar .ss-brand-words small{font-size:5.5px!important;letter-spacing:.4px!important}
  .ss-facilities-section .ss-facility-icon-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px!important;grid-auto-rows:minmax(202px,auto)!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{min-height:202px!important;padding:22px 12px 14px!important;gap:10px!important;border-radius:18px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art{width:62px!important;height:62px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art svg{width:31px!important;height:31px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-number{left:12px!important;top:10px!important;font-size:9px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy strong{font-size:11px!important}
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy small{font-size:9px!important}
}

/* Keep the liquid/fire motion clipped to each card, not across the section. */
.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::before{
  z-index:1!important;opacity:.50!important;mix-blend-mode:screen!important;filter:saturate(1.35) blur(1px)!important;
}
.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::after{
  z-index:1!important;opacity:.42!important;
}
.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(2)::before,
.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(6)::before{
  opacity:.60!important;filter:saturate(1.6) blur(1.5px)!important;
}

/* Reference-style footer: bright ivory + ice-blue/champagne water trails, readable text. */
.ss-footer{
  position:relative!important;isolation:isolate!important;overflow:hidden!important;
  background:
    radial-gradient(ellipse at 7% 0%,rgba(255,255,255,.99),transparent 38%),
    radial-gradient(ellipse at 85% 105%,rgba(93,194,230,.31),transparent 43%),
    radial-gradient(ellipse at 98% 0%,rgba(242,196,106,.30),transparent 33%),
    linear-gradient(180deg,#fffdf6 0%,#edf5fb 56%,#fff8e9 100%)!important;
  color:#17384d!important;border-top:1px solid rgba(198,166,107,.52)!important;
}
.ss-footer::before{
  opacity:.40!important;
  background:repeating-radial-gradient(ellipse at 4% 116%,transparent 0 23px,rgba(79,171,210,.15) 24px 25px,transparent 26px 43px)!important;
}
.ss-footer .ss-brand-words strong{color:#17384d!important;text-shadow:0 1px 0 #fff,0 2px 3px rgba(0,0,0,.12)!important}
.ss-footer .ss-brand-words small{color:#526d7e!important}
.ss-footer>p,.ss-footer>nav,.ss-footer>.ss-copyright{position:relative;z-index:2;color:#425f71!important}
.ss-footer>nav a:hover{color:#a7772b!important}
@media(prefers-reduced-motion:reduce){
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile,
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::before,
  .ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::after{animation:none!important}
}
"""


priority_patch = r"""

/* V7 HIGH-PRIORITY OVERRIDES: beat earlier appended CSS and restore legibility */

/* Header override intentionally matches the prior high-specificity selector. */
body .ss-home header.ss-navbar{
  min-height:108px!important;height:auto!important;
  padding:12px clamp(18px,3.5vw,58px)!important;
  gap:clamp(18px,2.6vw,38px)!important;
  background:
    radial-gradient(ellipse at 8% 0%,rgba(238,194,105,.23),transparent 31%),
    radial-gradient(ellipse at 78% 118%,rgba(53,125,148,.21),transparent 40%),
    linear-gradient(112deg,#020307 0%,#080d16 42%,#0b1925 76%,#100d0c 100%)!important;
  border-bottom:1px solid #e0ba6b!important;
  box-shadow:0 8px 28px rgba(0,0,0,.46),inset 0 1px rgba(255,255,255,.12)!important;
}
body .ss-home header.ss-navbar .ss-brand-emblem{
  width:62px!important;height:62px!important;flex-basis:62px!important;border-radius:19px!important;
  background:radial-gradient(circle at 28% 18%,#2c4e63 0%,#101a27 50%,#020407 100%)!important;
  border:1px solid rgba(248,218,143,.96)!important;
  box-shadow:inset 0 1px 2px rgba(255,255,255,.3),inset 0 -8px 15px rgba(0,0,0,.5),0 0 0 3px rgba(220,176,86,.12),0 8px 20px rgba(0,0,0,.5)!important;
}
body .ss-home header.ss-navbar .ss-brand-shri{
  font-size:32px!important;color:#ffdfa0!important;
  text-shadow:0 1px 0 #fff5d5,0 2px 0 #b9822f,0 4px 0 #704719,0 7px 12px rgba(0,0,0,.75)!important;
}
body .ss-home header.ss-navbar .ss-brand-words strong{font-size:25px!important;color:#fff5df!important}
body .ss-home header.ss-navbar .ss-brand-words strong span{font-size:1.35em!important;color:#f6d486!important}
body .ss-home header.ss-navbar .ss-brand-words small{font-size:8px!important;letter-spacing:1px!important;color:#cbd6df!important}
body .ss-home header.ss-navbar .ss-nav-links{gap:clamp(10px,1.25vw,19px)!important}
body .ss-home header.ss-navbar .ss-nav-cta{
  padding:13px 19px!important;border-radius:12px!important;
  background:linear-gradient(135deg,#fff0b9 0%,#e7bd61 48%,#b57a22 100%)!important;
  border:1px solid #ffecb0!important;color:#172637!important;
  box-shadow:0 4px 0 #674719,0 8px 17px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.95)!important;
}

/* At desktop-width Android viewports, keep brand readable and collapse links into a menu. */
@media(max-width:1050px){
  body .ss-home header.ss-navbar{min-height:91px!important;padding:10px 16px!important;gap:12px!important}
  body .ss-home header.ss-navbar .ss-brand{flex:1 1 auto!important;max-width:calc(100% - 55px)!important}
  body .ss-home header.ss-navbar .ss-brand-lockup{gap:10px!important}
  body .ss-home header.ss-navbar .ss-brand-emblem{width:52px!important;height:52px!important;flex-basis:52px!important}
  body .ss-home header.ss-navbar .ss-brand-shri{font-size:27px!important}
  body .ss-home header.ss-navbar .ss-brand-words strong{font-size:20px!important}
  body .ss-home header.ss-navbar .ss-brand-words small{font-size:6.5px!important;letter-spacing:.7px!important}
  body .ss-home header.ss-navbar .ss-menu-toggle{
    display:grid!important;place-items:center!important;position:relative!important;z-index:5!important;
    flex:0 0 43px!important;width:43px!important;height:43px!important;border-radius:12px!important;
    color:#f6dfaa!important;border:1px solid #e2bd6e88!important;background:#ffffff08!important;
  }
  body .ss-home header.ss-navbar .ss-nav-links{
    display:none!important;position:absolute!important;left:12px!important;right:12px!important;top:calc(100% + 7px)!important;
    flex-direction:column!important;align-items:stretch!important;gap:0!important;padding:12px!important;
    border:1px solid rgba(233,196,115,.65)!important;border-radius:17px!important;
    background:linear-gradient(145deg,#03060b 0%,#0c1925 72%,#181208 100%)!important;
    box-shadow:0 20px 42px rgba(0,0,0,.64)!important;
  }
  body .ss-home header.ss-navbar .ss-nav-links.is-open{display:flex!important}
  body .ss-home header.ss-navbar .ss-nav-links>a:not(.ss-nav-cta){padding:13px 10px!important;border-bottom:1px solid rgba(255,255,255,.09)!important;font-size:13px!important}
  body .ss-home header.ss-navbar .ss-nav-links>a.active:after{display:none!important}
  body .ss-home header.ss-navbar .ss-nav-links .ss-nav-cta{display:flex!important;justify-content:center!important;margin-top:10px!important}
}

/* 10 cards: high-specificity background/color rules replace previous pastel rules. */
body .ss-home section.ss-facilities-section .ss-facility-icon-grid{
  grid-template-columns:repeat(4,minmax(0,1fr))!important;
  grid-auto-rows:minmax(232px,auto)!important;gap:16px!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{
  min-height:232px!important;padding:24px 17px 17px!important;
  display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;gap:13px!important;
  overflow:hidden!important;isolation:isolate!important;border-radius:22px!important;
  color:#fff!important;background-size:150% 150%!important;
  border:1px solid rgba(255,255,255,.8)!important;
  box-shadow:0 15px 31px rgba(3,18,39,.24),inset 0 1px rgba(255,255,255,.4),inset 0 -16px 27px rgba(0,0,0,.22)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(1){
 --liquid-hot:#70ffe0;
 background:radial-gradient(ellipse at 68% 0%,rgba(92,255,207,.9),transparent 34%),linear-gradient(145deg,#00c99a 0%,#067d73 52%,#00343a 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(2){
 --liquid-hot:#ffd27d;
 background:radial-gradient(ellipse at 68% 0%,rgba(255,218,132,.9),transparent 30%),radial-gradient(ellipse at 32% 100%,rgba(255,74,8,.65),transparent 43%),linear-gradient(145deg,#ffb236 0%,#df5c18 50%,#43170d 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(3){
 --liquid-hot:#65f8ff;
 background:radial-gradient(ellipse at 50% 0%,rgba(83,244,255,.9),transparent 32%),linear-gradient(145deg,#13baf5 0%,#075cb8 50%,#05244f 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(4){
 --liquid-hot:#f0aaff;
 background:radial-gradient(ellipse at 72% 0%,rgba(231,147,255,.9),transparent 33%),linear-gradient(145deg,#944ceb 0%,#4530bb 50%,#17133f 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(5){
 --liquid-hot:#ffbce8;
 background:radial-gradient(ellipse at 50% 0%,rgba(255,146,205,.9),transparent 32%),linear-gradient(145deg,#f9419a 0%,#b41e70 52%,#401039 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(6){
 --liquid-hot:#fff48a;
 background:radial-gradient(ellipse at 50% 0%,rgba(255,248,129,.91),transparent 33%),radial-gradient(ellipse at 80% 95%,rgba(255,97,12,.66),transparent 41%),linear-gradient(145deg,#ffdc43 0%,#df9309 49%,#482008 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(7){
 --liquid-hot:#a5ffff;
 background:radial-gradient(ellipse at 50% 0%,rgba(158,255,255,.9),transparent 33%),linear-gradient(145deg,#25d7f1 0%,#008bca 51%,#04396e 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(8){
 --liquid-hot:#a5ff8b;
 background:radial-gradient(ellipse at 66% 0%,rgba(154,255,146,.9),transparent 34%),linear-gradient(145deg,#1cdd78 0%,#078651 51%,#00372e 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(9){
 --liquid-hot:#ffb6ff;
 background:radial-gradient(ellipse at 52% 0%,rgba(255,177,255,.9),transparent 32%),linear-gradient(145deg,#d956f5 0%,#8129bf 51%,#291049 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile:nth-child(10){
 --liquid-hot:#a5ffff;
 background:radial-gradient(ellipse at 86% 0%,rgba(255,102,223,.8),transparent 32%),radial-gradient(ellipse at 25% 0%,rgba(96,255,255,.9),transparent 31%),linear-gradient(145deg,#2ad7f1 0%,#1b70d2 48%,#302578 100%)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::before{
  z-index:1!important;opacity:.45!important;mix-blend-mode:screen!important;filter:blur(1.4px) saturate(1.35)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::after{
  z-index:1!important;opacity:.38!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art{
  align-self:center!important;flex:0 0 auto!important;width:76px!important;height:76px!important;border-radius:50%!important;
  color:#fff!important;background:radial-gradient(circle at 28% 17%,rgba(255,255,255,.43),rgba(255,255,255,.15) 27%,rgba(4,20,40,.25) 68%,rgba(0,0,0,.38) 100%)!important;
  border:1px solid rgba(255,255,255,.92)!important;
  box-shadow:0 0 0 3px rgba(255,255,255,.1),0 0 23px var(--liquid-hot),0 12px 24px rgba(0,0,0,.28),inset 0 2px 6px rgba(255,255,255,.48)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art svg{
  width:38px!important;height:38px!important;color:#fff!important;stroke-width:2.05!important;filter:drop-shadow(0 2px 3px rgba(0,0,0,.6))!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-number{
  position:absolute!important;left:16px!important;top:13px!important;z-index:4!important;color:#fff!important;opacity:1!important;
  font-size:10px!important;letter-spacing:1.5px!important;text-shadow:0 2px 5px rgba(0,0,0,.75)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy{
  position:relative!important;z-index:4!important;display:flex!important;flex-direction:column!important;
  align-items:flex-start!important;text-align:left!important;gap:6px!important;width:100%!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy strong{
  color:#fff!important;font-size:14px!important;font-weight:800!important;line-height:1.35!important;text-shadow:0 1px 3px rgba(0,0,0,.75)!important;
}
body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy small{
  color:#fff!important;font-size:11px!important;line-height:1.5!important;opacity:1!important;text-shadow:0 1px 3px rgba(0,0,0,.78)!important;max-width:34ch!important;
}
@media(max-width:1050px){
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;grid-auto-rows:minmax(218px,auto)!important;gap:13px!important;
  }
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{min-height:218px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art{width:70px!important;height:70px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art svg{width:35px!important;height:35px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy strong{font-size:13px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy small{font-size:10px!important}
}
@media(max-width:520px){
  body .ss-home header.ss-navbar{min-height:82px!important;padding:8px 11px!important}
  body .ss-home header.ss-navbar .ss-brand-emblem{width:45px!important;height:45px!important;flex-basis:45px!important}
  body .ss-home header.ss-navbar .ss-brand-shri{font-size:24px!important}
  body .ss-home header.ss-navbar .ss-brand-words strong{font-size:16px!important}
  body .ss-home header.ss-navbar .ss-brand-words small{font-size:5px!important;letter-spacing:.4px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid{gap:10px!important;grid-auto-rows:minmax(204px,auto)!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{min-height:204px!important;padding:22px 12px 14px!important;gap:10px!important;border-radius:18px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art{width:62px!important;height:62px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-art svg{width:31px!important;height:31px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy strong{font-size:11px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-english-copy small{font-size:9px!important}
}

/* Footer high-specificity override: pale water/aurora, not a dark solid block. */
body .ss-home footer.ss-footer{
  position:relative!important;isolation:isolate!important;overflow:hidden!important;
  background:
    radial-gradient(ellipse at 7% 0%,rgba(255,255,255,.98),transparent 38%),
    radial-gradient(ellipse at 85% 105%,rgba(93,194,230,.28),transparent 43%),
    radial-gradient(ellipse at 98% 0%,rgba(242,196,106,.27),transparent 33%),
    linear-gradient(180deg,#fffdf6 0%,#edf5fb 56%,#fff8e9 100%)!important;
  color:#17384d!important;border-top:1px solid rgba(198,166,107,.52)!important;
}
body .ss-home footer.ss-footer::before{
  opacity:.40!important;
  background:repeating-radial-gradient(ellipse at 4% 116%,transparent 0 23px,rgba(79,171,210,.15) 24px 25px,transparent 26px 43px)!important;
  pointer-events:none!important;
}
body .ss-home footer.ss-footer .ss-brand-words strong{color:#17384d!important;text-shadow:0 1px 0 #fff,0 2px 3px rgba(0,0,0,.12)!important}
body .ss-home footer.ss-footer .ss-brand-words small{color:#526d7e!important}
body .ss-home footer.ss-footer>p,
body .ss-home footer.ss-footer>nav,
body .ss-home footer.ss-footer>.ss-copyright{position:relative;z-index:2;color:#425f71!important}
@media(prefers-reduced-motion:reduce){
 body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile,
 body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::before,
 body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile::after{animation:none!important}
}
"""

patch += priority_patch

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"responsive-premium-layout-v7-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(css_path, backup / "Home.css")
css_path.write_text(css.rstrip() + "\n\n" + patch, encoding="utf-8")

print("SUCCESS: V7 responsive premium repair appended to src/Home.css.")
print("Header: taller, clearer devotional black/navy/gold; smaller screens use a dropdown hamburger menu.")
print("Features: 4 columns on desktop, 2 large columns on <=1050px; stronger labels, larger glass icons, distinct liquid colors.")
print("Footer: light ice-blue/ivory with champagne water styling.")
print("Only Home.css changed; YouTube, Home.jsx, Contact, registration and seat logic untouched.")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Hard-refresh local Chrome after build.")
