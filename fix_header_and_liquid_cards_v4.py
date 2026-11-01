#!/usr/bin/env python3
"""Final override: deep devotional black/gold header and saturated liquid/fire facility cards."""
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

if "ss-facility-icon-grid" not in jsx or "ss-facility-icon-tile" not in jsx:
    print("ERROR: The icon-based 10-feature layout was not found. No files changed.")
    sys.exit(1)
if "ss-navbar" not in css or "ss-facility-icon-tile" not in css:
    print("ERROR: Expected homepage header or feature-card styles are missing. No files changed.")
    sys.exit(1)

marker = "/* FINAL FIX — DEVOTIONAL BLACK HEADER + TRUE LIQUID/FIRE FEATURE CARDS V4 */"
if marker in css:
    print("ERROR: This final override is already applied. No files changed.")
    sys.exit(1)

css_addition = r"""

/* FINAL FIX — DEVOTIONAL BLACK HEADER + TRUE LIQUID/FIRE FEATURE CARDS V4 */

/* Black devotional premium header: obsidian/navy, champagne edge and restrained halo. */
.ss-navbar{
  position:sticky!important;
  isolation:isolate;
  overflow:visible!important;
  background:
    radial-gradient(ellipse at 8% 0%,rgba(198,166,107,.15),transparent 37%),
    radial-gradient(ellipse at 78% 120%,rgba(38,93,113,.20),transparent 40%),
    linear-gradient(112deg,#05070c 0%,#090e17 42%,#0c1824 76%,#100f12 100%)!important;
  border-bottom:1px solid rgba(221,184,106,.78)!important;
  box-shadow:0 9px 28px rgba(0,0,0,.45),inset 0 1px rgba(255,255,255,.09)!important;
  color:#fff8e8!important;
}
.ss-navbar::before{
  content:"";
  position:absolute;
  z-index:-1;
  inset:0;
  pointer-events:none;
  opacity:.34;
  background:
    radial-gradient(circle at 14% 55%,rgba(238,201,122,.20) 0 1px,transparent 2px),
    radial-gradient(circle at 18% 25%,rgba(238,201,122,.32) 0 1px,transparent 2px),
    radial-gradient(circle at 75% 72%,rgba(128,219,231,.22) 0 1px,transparent 2px),
    linear-gradient(90deg,transparent,rgba(255,255,255,.025),transparent);
}
.ss-navbar::after{
  content:"";
  position:absolute;
  z-index:0;
  height:1px;
  left:0;right:0;bottom:-1px;
  pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(246,214,145,.85) 18%,rgba(255,245,213,.48) 52%,rgba(246,214,145,.8) 82%,transparent);
}
.ss-navbar>.ss-brand,
.ss-navbar>.ss-menu-toggle,
.ss-navbar>.ss-nav-links{position:relative;z-index:2}
.ss-brand-emblem{
  border-color:rgba(244,211,127,.94)!important;
  background:radial-gradient(circle at 30% 18%,#304a60 0%,#101b27 48%,#03060a 100%)!important;
  box-shadow:inset 0 1px 1px rgba(255,255,255,.28),inset 0 -8px 15px rgba(0,0,0,.46),0 0 0 2px rgba(218,174,85,.10),0 7px 18px rgba(0,0,0,.5),0 0 18px rgba(219,178,91,.10)!important;
}
.ss-brand-words strong span{
  color:#f8d986!important;
  text-shadow:0 1px 0 #fff5cd,0 2px 0 #b7802f,0 4px 0 #70461a,0 7px 13px rgba(0,0,0,.7)!important;
}
.ss-nav-links{color:#f0e7d4!important}
.ss-nav-links>a:not(.ss-nav-cta):hover,
.ss-nav-links>a.active{color:#f4d892!important}
.ss-nav-links>a.active:after{background:linear-gradient(90deg,#a77229,#fff0b3,#a77229)!important}
.ss-nav-cta{
  background:linear-gradient(135deg,#fff0b6 0%,#e5bb5c 45%,#b77e26 100%)!important;
  box-shadow:0 4px 0 #694718,0 8px 18px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,255,255,.95)!important;
  border:1px solid #ffedb1!important;
}
.ss-nav-links.is-open{
  background:linear-gradient(145deg,#080b12,#101d29 70%,#17130d)!important;
  border-color:rgba(226,187,104,.55)!important;
  box-shadow:0 18px 38px rgba(0,0,0,.58)!important;
}
@media(max-width:760px){
  .ss-navbar{background:
    radial-gradient(ellipse at 12% 0%,rgba(198,166,107,.14),transparent 42%),
    linear-gradient(110deg,#04060a,#0a1420 68%,#100f12)!important}
}

/* Give the facility area a clean stage; no giant waves wash over the section or labels. */
.ss-facilities-section{
  position:relative!important;
  isolation:isolate!important;
  background:linear-gradient(180deg,#fffaf0 0%,#f8f7f0 45%,#edf4f8 100%)!important;
}
.ss-facilities-section::before{
  opacity:.12!important;
  filter:none!important;
  background:
    radial-gradient(ellipse at 8% 82%,rgba(79,184,219,.12),transparent 33%),
    radial-gradient(ellipse at 88% 15%,rgba(234,190,97,.15),transparent 30%)!important;
}
.ss-facilities-section::after{opacity:.12!important;filter:blur(18px)!important}

/* Base card: everything animated remains clipped inside the tile. */
.ss-facility-icon-grid .ss-facility-icon-tile{
  --liquid-hot:#adfff0;
  position:relative!important;
  isolation:isolate!important;
  overflow:hidden!important;
  color:#fff!important;
  background-size:100% 100%!important;
  border:1px solid rgba(255,255,255,.72)!important;
  box-shadow:0 14px 29px rgba(3,17,35,.22),inset 0 1px 0 rgba(255,255,255,.46),inset 0 -13px 25px rgba(0,0,0,.23)!important;
  animation:liquidCardFloatV4 9s ease-in-out infinite;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(1){
  --liquid-hot:#72ffe0;
  background:radial-gradient(ellipse at 72% 2%,rgba(101,255,211,.95),transparent 34%),linear-gradient(145deg,#00c99a 0%,#067f78 51%,#00353c 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(2){
  --liquid-hot:#ffd27d;
  background:radial-gradient(ellipse at 70% 0%,rgba(255,217,134,.98),transparent 28%),radial-gradient(ellipse at 25% 85%,rgba(255,90,16,.85),transparent 44%),linear-gradient(145deg,#ffad31 0%,#e65e19 47%,#40160d 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(3){
  --liquid-hot:#6bfbff;
  background:radial-gradient(ellipse at 50% -6%,rgba(79,243,255,.98),transparent 30%),linear-gradient(145deg,#12b9f4 0%,#0663c7 48%,#05234f 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(4){
  --liquid-hot:#f4a4ff;
  background:radial-gradient(ellipse at 75% 0%,rgba(237,148,255,.96),transparent 33%),linear-gradient(145deg,#9b4eee 0%,#4932bb 50%,#17143e 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(5){
  --liquid-hot:#ffb9e6;
  background:radial-gradient(ellipse at 50% -3%,rgba(255,144,203,.95),transparent 32%),linear-gradient(145deg,#fa489d 0%,#b82172 51%,#401039 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(6){
  --liquid-hot:#fff68a;
  background:radial-gradient(ellipse at 50% -4%,rgba(255,248,130,.98),transparent 31%),radial-gradient(ellipse at 80% 90%,rgba(255,102,15,.66),transparent 43%),linear-gradient(145deg,#ffdc44 0%,#e69a0b 49%,#482007 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(7){
  --liquid-hot:#a3ffff;
  background:radial-gradient(ellipse at 52% -2%,rgba(156,255,255,.98),transparent 30%),linear-gradient(145deg,#24d7ef 0%,#008dcb 48%,#04396e 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(8){
  --liquid-hot:#a4ff8d;
  background:radial-gradient(ellipse at 65% -2%,rgba(151,255,143,.95),transparent 32%),linear-gradient(145deg,#1ce27a 0%,#07864e 52%,#00372e 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(9){
  --liquid-hot:#ffb7ff;
  background:radial-gradient(ellipse at 54% -1%,rgba(255,176,255,.97),transparent 30%),linear-gradient(145deg,#d95bfb 0%,#8026bd 48%,#291047 100%)!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile:nth-child(10){
  --liquid-hot:#a9ffff;
  background:radial-gradient(ellipse at 87% 0%,rgba(255,105,224,.91),transparent 32%),radial-gradient(ellipse at 25% -1%,rgba(93,255,255,.9),transparent 31%),linear-gradient(145deg,#27d6ef 0%,#1b70d4 48%,#302579 100%)!important;
}

/* Moving liquid current: soft specular highlights and concentric water lines. */
.ss-facility-icon-grid .ss-facility-icon-tile::before{
  content:""!important;
  position:absolute!important;
  z-index:0!important;
  inset:-43%!important;
  width:auto!important;height:auto!important;left:-43%!important;top:-43%!important;
  pointer-events:none!important;
  opacity:.52!important;
  mix-blend-mode:screen!important;
  transform-origin:50% 50%!important;
  background:
    radial-gradient(ellipse at 23% 43%,rgba(255,255,255,.65) 0 1.2%,transparent 19%),
    radial-gradient(ellipse at 73% 32%,var(--liquid-hot) 0 2%,transparent 25%),
    repeating-radial-gradient(ellipse at 50% 100%,transparent 0 8px,rgba(255,255,255,.32) 9px 10px,rgba(0,0,0,.09) 11px 12px,transparent 13px 22px),
    conic-gradient(from 10deg at 50% 50%,transparent 0 10%,rgba(255,255,255,.14) 18%,transparent 28%,var(--liquid-hot) 37%,transparent 48%,rgba(255,255,255,.17) 58%,transparent 69%,var(--liquid-hot) 80%,transparent 91%,rgba(255,255,255,.14) 100%)!important;
  filter:blur(1.2px) saturate(1.3)!important;
  animation:liquidSurfaceV4 13s ease-in-out infinite alternate!important;
}
.ss-facility-icon-grid .ss-facility-icon-tile::after{
  content:""!important;
  position:absolute!important;
  z-index:0!important;
  inset:auto 4% -37% 4%!important;
  width:auto!important;
  height:80%!important;
  border:1.4px solid rgba(255,255,255,.55)!important;
  border-radius:50%!important;
  opacity:.38!important;
  pointer-events:none!important;
  box-shadow:0 0 0 6px rgba(255,255,255,.07),0 0 0 14px rgba(255,255,255,.06),0 0 0 23px rgba(255,255,255,.045),inset 0 0 24px rgba(255,255,255,.08)!important;
  animation:liquidRippleV4 7s ease-in-out infinite!important;
}
.ss-facility-icon-grid .ss-facility-icon-art{
  position:relative!important;
  z-index:2!important;
  color:#fff!important;
  background:radial-gradient(circle at 28% 20%,rgba(255,255,255,.43),rgba(255,255,255,.15) 27%,rgba(5,24,46,.26) 68%,rgba(0,0,0,.4) 100%)!important;
  border:1px solid rgba(255,255,255,.89)!important;
  box-shadow:0 0 0 2px rgba(255,255,255,.10),0 0 23px var(--liquid-hot),0 12px 28px rgba(0,0,0,.28),inset 0 2px 5px rgba(255,255,255,.45),inset 0 -9px 17px rgba(0,0,0,.25)!important;
  backdrop-filter:blur(4px)!important;
}
.ss-facility-icon-grid .ss-facility-icon-art svg{
  color:#fff!important;stroke-width:2.1!important;
  filter:drop-shadow(0 2px 3px rgba(0,0,0,.55))!important;
}
.ss-facility-icon-grid .ss-facility-number{
  z-index:3!important;color:#fff!important;opacity:1!important;
  text-shadow:0 2px 5px rgba(0,0,0,.55)!important;
}
.ss-facility-icon-grid .ss-facility-english-copy{
  z-index:3!important;
}
.ss-facility-icon-grid .ss-facility-english-copy strong,
.ss-facility-icon-grid .ss-facility-english-copy small{
  color:#fff!important;
  text-shadow:0 1px 2px rgba(0,0,0,.72),0 0 8px rgba(0,0,0,.28)!important;
}
.ss-facility-icon-grid .ss-facility-english-copy strong{font-size:12px!important;line-height:1.4!important}
.ss-facility-icon-grid .ss-facility-english-copy small{font-size:10px!important;line-height:1.5!important;opacity:1!important}
@keyframes liquidSurfaceV4{
  0%{transform:translate3d(-3%,1%,0) rotate(0deg) scale(1)}
  50%{transform:translate3d(2%,-2%,0) rotate(16deg) scale(1.08)}
  100%{transform:translate3d(5%,3%,0) rotate(31deg) scale(1.03)}
}
@keyframes liquidRippleV4{
  0%,100%{transform:scale(.94) translateY(2%);opacity:.23}
  50%{transform:scale(1.05) translateY(-2%);opacity:.48}
}
@keyframes liquidCardFloatV4{
  0%,100%{background-position:0% 50%}
  50%{background-position:100% 50%}
}
@media(hover:hover) and (pointer:fine){
  .ss-facility-icon-grid .ss-facility-icon-tile:hover{
    transform:translateY(-5px) perspective(800px) rotateX(2deg)!important;
    box-shadow:0 23px 42px rgba(2,13,31,.30),0 0 22px color-mix(in srgb,var(--liquid-hot) 24%,transparent),inset 0 1px 0 rgba(255,255,255,.48)!important;
  }
}
@media(max-width:760px){
  .ss-facility-icon-grid .ss-facility-icon-tile{
    min-height:194px!important;
    animation-duration:12s!important;
  }
  .ss-facility-icon-grid .ss-facility-icon-tile::before{animation-duration:15s!important;opacity:.43!important}
  .ss-facility-icon-grid .ss-facility-icon-tile::after{animation-duration:8.5s!important}
  .ss-facility-icon-grid .ss-facility-english-copy strong{font-size:11px!important}
  .ss-facility-icon-grid .ss-facility-english-copy small{font-size:9px!important}
}
@media(prefers-reduced-motion:reduce){
  .ss-facility-icon-grid .ss-facility-icon-tile,
  .ss-facility-icon-grid .ss-facility-icon-tile::before,
  .ss-facility-icon-grid .ss-facility-icon-tile::after{animation:none!important}
}
"""

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"devotional-header-liquid-cards-v4-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(css_path, backup / "Home.css")

css_path.write_text(css.rstrip() + "\n\n" + css_addition, encoding="utf-8")

print("SUCCESS: Black devotional premium header + saturated animated liquid/fire cards applied.")
print("Each tile has an individual color; animation/ripples are clipped inside tile borders.")
print("Text/icons are forced to white with strong shadow for readability.")
print("Changed only: src/Home.css")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Preview locally before committing/pushing.")
