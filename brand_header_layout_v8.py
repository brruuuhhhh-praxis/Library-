#!/usr/bin/env python3
"""V8: make the real homepage header visibly premium and prevent phone desktop-mode shrinking."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
css_path = ROOT / "src" / "Home.css"
jsx_path = ROOT / "src" / "Home.jsx"

if not css_path.is_file() or not jsx_path.is_file():
    print("ERROR: Run this script from ~/shri-shyam-library.")
    sys.exit(1)

css = css_path.read_text(encoding="utf-8")
jsx = jsx_path.read_text(encoding="utf-8")

required_jsx = [
    'className="ss-navbar"',
    'className="ss-brand-lockup"',
    'className="ss-brand-emblem"',
    'ss-nav-links',
    'is-open',
    'className="ss-menu-toggle"',
]
required_css = [".ss-navbar", ".ss-brand-lockup", ".ss-brand-emblem", ".ss-nav-links", ".ss-menu-toggle", ".ss-facility-icon-grid"]
missing = [x for x in required_jsx if x not in jsx] + [x for x in required_css if x not in css]
if missing:
    print("ERROR: Current header/grid differs from the expected version: " + ", ".join(missing))
    print("No files changed.")
    sys.exit(1)

marker = "/* V8 BRAND REDESIGN: OBSIDIAN DEVOTIONAL HEADER + COARSE-POINTER RESPONSIVENESS */"
if marker in css:
    print("ERROR: V8 is already applied. No files changed.")
    sys.exit(1)

patch = r"""

/* V8 BRAND REDESIGN: OBSIDIAN DEVOTIONAL HEADER + COARSE-POINTER RESPONSIVENESS */

/* Desktop header redesign — visually distinct from the previous flat navy strip. */
body .ss-home > header.ss-navbar{
  box-sizing:border-box!important;
  position:sticky!important;top:0!important;z-index:100!important;
  display:flex!important;align-items:center!important;justify-content:space-between!important;
  flex-wrap:nowrap!important;
  width:100%!important;min-height:120px!important;height:auto!important;
  padding:16px clamp(26px,3.2vw,60px)!important;
  gap:clamp(20px,2.3vw,36px)!important;
  color:#fff4dc!important;
  background:
    radial-gradient(ellipse at 8% 0%,rgba(225,177,79,.28) 0%,transparent 28%),
    radial-gradient(ellipse at 87% 110%,rgba(43,121,150,.23) 0%,transparent 35%),
    radial-gradient(ellipse at 52% -75%,rgba(255,232,164,.09) 0%,transparent 53%),
    linear-gradient(112deg,#020307 0%,#060a12 32%,#0a1925 67%,#08090d 100%)!important;
  border-bottom:1px solid rgba(237,197,111,.92)!important;
  box-shadow:0 10px 30px rgba(0,0,0,.48),inset 0 1px 0 rgba(255,255,255,.13)!important;
  backdrop-filter:blur(18px)!important;
}
body .ss-home > header.ss-navbar::before{
  content:""!important;position:absolute!important;z-index:0!important;inset:0!important;
  pointer-events:none!important;opacity:.64!important;
  background:
    radial-gradient(circle at 7% 26%,rgba(255,231,162,.88) 0 1px,transparent 2px),
    radial-gradient(circle at 14% 72%,rgba(255,221,145,.7) 0 1px,transparent 2px),
    radial-gradient(circle at 27% 17%,rgba(143,228,238,.6) 0 1px,transparent 2px),
    radial-gradient(circle at 72% 29%,rgba(255,223,145,.62) 0 1px,transparent 2px),
    radial-gradient(circle at 92% 65%,rgba(151,234,238,.65) 0 1px,transparent 2px),
    linear-gradient(105deg,transparent 20%,rgba(255,246,220,.055) 43%,rgba(111,207,223,.055) 57%,transparent 78%)!important;
}
body .ss-home > header.ss-navbar::after{
  content:""!important;position:absolute!important;left:0!important;right:0!important;bottom:-1px!important;
  height:2px!important;pointer-events:none!important;
  background:linear-gradient(90deg,transparent 0%,#986a26 11%,#f0d38c 27%,#fff4c8 50%,#e3b75e 73%,#9d6e28 89%,transparent 100%)!important;
  box-shadow:0 0 10px rgba(238,195,104,.42)!important;
}
body .ss-home > header.ss-navbar > .ss-brand,
body .ss-home > header.ss-navbar > .ss-menu-toggle,
body .ss-home > header.ss-navbar > .ss-nav-links{position:relative!important;z-index:2!important}
body .ss-home > header.ss-navbar > .ss-brand{
  display:inline-flex!important;flex:0 0 auto!important;min-width:max-content!important;max-width:none!important;
}
body .ss-home > header.ss-navbar .ss-brand-lockup{
  display:inline-flex!important;align-items:center!important;gap:15px!important;min-width:0!important;
}
body .ss-home > header.ss-navbar .ss-brand-emblem{
  flex:0 0 68px!important;width:68px!important;height:68px!important;border-radius:20px!important;
  display:grid!important;place-items:center!important;position:relative!important;overflow:visible!important;
  border:1px solid rgba(255,223,146,.98)!important;
  background:
    radial-gradient(circle at 29% 17%,rgba(76,126,148,.66),transparent 42%),
    linear-gradient(145deg,#122335 0%,#080d15 60%,#020306 100%)!important;
  box-shadow:
    inset 0 1px 2px rgba(255,255,255,.32),
    inset 0 -10px 16px rgba(0,0,0,.58),
    0 0 0 3px rgba(214,174,91,.13),
    0 0 24px rgba(225,181,88,.20),
    0 10px 24px rgba(0,0,0,.55)!important;
}
body .ss-home > header.ss-navbar .ss-brand-emblem::before{
  content:""!important;position:absolute!important;inset:4px!important;border-radius:15px!important;
  border:1px solid rgba(252,220,139,.3)!important;pointer-events:none!important;
}
body .ss-home > header.ss-navbar .ss-brand-shri{
  position:relative!important;font-size:36px!important;font-weight:900!important;line-height:1!important;
  color:#ffe3a0!important;
  text-shadow:0 1px 0 #fff6d8,0 2px 0 #c08b30,0 4px 0 #76491a,0 7px 0 #3d2815,0 9px 14px rgba(0,0,0,.8)!important;
}
body .ss-home > header.ss-navbar .ss-brand-ai{
  position:absolute!important;right:7px!important;bottom:6px!important;
  color:#9af1e7!important;filter:drop-shadow(0 0 5px rgba(98,237,226,.9))!important;
}
body .ss-home > header.ss-navbar .ss-brand-words{
  display:flex!important;flex-direction:column!important;justify-content:center!important;
  min-width:0!important;gap:6px!important;
}
body .ss-home > header.ss-navbar .ss-brand-words strong{
  display:block!important;white-space:nowrap!important;
  color:#fff4de!important;font-size:25px!important;line-height:1.22!important;font-weight:850!important;
  letter-spacing:-.4px!important;text-shadow:0 2px 2px rgba(0,0,0,.68),0 4px 10px rgba(0,0,0,.34)!important;
}
body .ss-home > header.ss-navbar .ss-brand-words strong span{
  color:#f4d17d!important;font-size:1.32em!important;font-weight:950!important;
  text-shadow:0 1px 0 #fff2c7,0 2px 0 #c18a2c,0 4px 0 #714318,0 7px 11px rgba(0,0,0,.75)!important;
}
body .ss-home > header.ss-navbar .ss-brand-words small{
  display:block!important;white-space:nowrap!important;
  color:#c4d5df!important;font-size:8px!important;line-height:1.35!important;
  font-weight:800!important;letter-spacing:1.1px!important;
}
body .ss-home > header.ss-navbar .ss-nav-links{
  display:flex!important;flex:0 1 auto!important;align-items:center!important;justify-content:flex-end!important;
  gap:clamp(12px,1.35vw,22px)!important;min-width:0!important;
  color:#eee3cc!important;font-size:13px!important;font-weight:750!important;
}
body .ss-home > header.ss-navbar .ss-nav-links>a:not(.ss-nav-cta){
  color:#eee5d5!important;font-size:13px!important;white-space:nowrap!important;
  padding:13px 0!important;transition:color .2s ease,text-shadow .2s ease!important;
}
body .ss-home > header.ss-navbar .ss-nav-links>a:not(.ss-nav-cta):hover,
body .ss-home > header.ss-navbar .ss-nav-links>a.active{
  color:#ffdc8a!important;text-shadow:0 0 13px rgba(235,190,94,.28)!important;
}
body .ss-home > header.ss-navbar .ss-nav-links>a.active:after{
  height:2px!important;background:linear-gradient(90deg,#a77228,#fff0b2,#a77228)!important;
  box-shadow:0 0 8px rgba(241,197,101,.5)!important;
}
body .ss-home > header.ss-navbar .ss-nav-cta{
  display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:9px!important;
  min-height:48px!important;padding:0 19px!important;border-radius:14px!important;
  white-space:nowrap!important;font-size:13px!important;font-weight:850!important;color:#1a2734!important;
  background:linear-gradient(135deg,#fff2be 0%,#f0ce78 42%,#d6a13b 78%,#b87c23 100%)!important;
  border:1px solid #fff0b1!important;
  box-shadow:0 4px 0 #78501b,0 9px 22px rgba(0,0,0,.38),inset 0 1px 0 rgba(255,255,255,.96)!important;
}
body .ss-home > header.ss-navbar .ss-nav-cta:hover{transform:translateY(-2px)!important;filter:brightness(1.04)!important}
body .ss-home > header.ss-navbar .ss-menu-toggle{
  display:none!important;color:#f6dfaa!important;border:1px solid rgba(231,192,109,.72)!important;
  border-radius:12px!important;background:rgba(255,255,255,.04)!important;
}

/* Medium desktop / narrow tablets use a clean dropdown rather than squashing the wordmark. */
@media(max-width:1280px){
  body .ss-home > header.ss-navbar{min-height:98px!important;padding:12px 24px!important;gap:16px!important}
  body .ss-home > header.ss-navbar .ss-brand-emblem{width:58px!important;height:58px!important;flex-basis:58px!important}
  body .ss-home > header.ss-navbar .ss-brand-shri{font-size:31px!important}
  body .ss-home > header.ss-navbar .ss-brand-words strong{font-size:22px!important}
  body .ss-home > header.ss-navbar .ss-brand-words small{font-size:7px!important;letter-spacing:.8px!important}
  body .ss-home > header.ss-navbar .ss-menu-toggle{
    display:grid!important;place-items:center!important;flex:0 0 45px!important;
    width:45px!important;height:45px!important;position:relative!important;z-index:5!important;
  }
  body .ss-home > header.ss-navbar .ss-nav-links{
    display:none!important;position:absolute!important;left:14px!important;right:14px!important;top:calc(100% + 8px)!important;
    flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;gap:0!important;
    padding:13px!important;border:1px solid rgba(230,191,109,.68)!important;border-radius:17px!important;
    background:linear-gradient(145deg,#03060b 0%,#0b1824 70%,#171207 100%)!important;
    box-shadow:0 20px 44px rgba(0,0,0,.68)!important;
  }
  body .ss-home > header.ss-navbar .ss-nav-links.is-open{display:flex!important}
  body .ss-home > header.ss-navbar .ss-nav-links>a:not(.ss-nav-cta){
    display:block!important;padding:14px 10px!important;border-bottom:1px solid rgba(255,255,255,.09)!important;font-size:14px!important;
  }
  body .ss-home > header.ss-navbar .ss-nav-links>a.active:after{display:none!important}
  body .ss-home > header.ss-navbar .ss-nav-links .ss-nav-cta{display:flex!important;margin-top:10px!important}
}

/* Critical: phone browsers can use a desktop-width layout viewport. Coarse pointer
   switches to the mobile menu + two-column facilities regardless of that width. */
@media(pointer:coarse){
  body .ss-home > header.ss-navbar{
    min-height:96px!important;height:auto!important;padding:10px 14px!important;gap:10px!important;
  }
  body .ss-home > header.ss-navbar > .ss-brand{
    flex:1 1 auto!important;min-width:0!important;max-width:calc(100% - 58px)!important;
  }
  body .ss-home > header.ss-navbar .ss-brand-lockup{gap:9px!important}
  body .ss-home > header.ss-navbar .ss-brand-emblem{width:55px!important;height:55px!important;flex-basis:55px!important;border-radius:16px!important}
  body .ss-home > header.ss-navbar .ss-brand-shri{font-size:30px!important}
  body .ss-home > header.ss-navbar .ss-brand-words strong{font-size:20px!important}
  body .ss-home > header.ss-navbar .ss-brand-words small{
    max-width:100%!important;white-space:normal!important;font-size:6px!important;letter-spacing:.45px!important;line-height:1.3!important;
  }
  body .ss-home > header.ss-navbar .ss-menu-toggle{
    display:grid!important;place-items:center!important;flex:0 0 44px!important;width:44px!important;height:44px!important;
    position:relative!important;z-index:6!important;
  }
  body .ss-home > header.ss-navbar .ss-nav-links{
    display:none!important;position:absolute!important;left:10px!important;right:10px!important;top:calc(100% + 7px)!important;
    flex-direction:column!important;align-items:stretch!important;gap:0!important;padding:12px!important;
    border:1px solid rgba(236,196,114,.68)!important;border-radius:16px!important;
    background:linear-gradient(145deg,#03060b,#0b1824 72%,#171207)!important;
    box-shadow:0 18px 42px rgba(0,0,0,.68)!important;
  }
  body .ss-home > header.ss-navbar .ss-nav-links.is-open{display:flex!important}
  body .ss-home > header.ss-navbar .ss-nav-links>a:not(.ss-nav-cta){
    padding:13px 10px!important;font-size:14px!important;border-bottom:1px solid rgba(255,255,255,.10)!important;
  }
  body .ss-home > header.ss-navbar .ss-nav-links>a.active:after{display:none!important}
  body .ss-home > header.ss-navbar .ss-nav-links .ss-nav-cta{display:flex!important;margin-top:9px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;grid-auto-rows:minmax(215px,auto)!important;gap:12px!important;
  }
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{
    min-height:215px!important;padding:23px 13px 15px!important;gap:11px!important;
  }
}
@media(max-width:520px) and (pointer:coarse){
  body .ss-home > header.ss-navbar{min-height:88px!important;padding:9px 11px!important}
  body .ss-home > header.ss-navbar .ss-brand-emblem{width:49px!important;height:49px!important;flex-basis:49px!important}
  body .ss-home > header.ss-navbar .ss-brand-shri{font-size:26px!important}
  body .ss-home > header.ss-navbar .ss-brand-words strong{font-size:17px!important}
  body .ss-home > header.ss-navbar .ss-brand-words small{font-size:5.2px!important;letter-spacing:.25px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid{grid-auto-rows:minmax(205px,auto)!important;gap:10px!important}
  body .ss-home section.ss-facilities-section .ss-facility-icon-grid .ss-facility-icon-tile{min-height:205px!important;padding:21px 11px 13px!important}
}
"""

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"brand-header-layout-v8-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(css_path, backup / "Home.css")
css_path.write_text(css.rstrip() + "\n\n" + marker + "\n" + patch, encoding="utf-8")

print("SUCCESS: V8 header redesign and touch-device responsive layout applied.")
print("Header: larger wordmark/emblem, obsidian devotional glow, gold edge, clearer nav/CTA.")
print("Touchscreens: hamburger menu is enabled even when Chrome uses a desktop-width viewport.")
print("Feature cards: vivid palette preserved; touch layout forced to two readable columns.")
print("Changed only: src/Home.css. YouTube video, Home.jsx, forms, seats, other pages untouched.")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
