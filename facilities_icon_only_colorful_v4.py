#!/usr/bin/env python3
"""Switch all 10 homepage facilities to colorful, glossy icon-only cards."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

root = Path.cwd()
jsx_path = root / "src" / "Home.jsx"
css_path = root / "src" / "Home.css"

if not jsx_path.exists() or not css_path.exists():
    print("ERROR: Run this script from ~/shri-shyam-library.")
    sys.exit(1)

jsx = jsx_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")
marker = "/* FACILITY ICON GALLERY V4 - COLORFUL GLOSSY TILES */"

if marker in css:
    print("ERROR: V4 icon-gallery styling is already present. No files changed.")
    sys.exit(1)

if "facilities.slice(1)" not in jsx:
    print("ERROR: Home.jsx does not currently match the expected pre-V4 facility grid. No files changed.")
    sys.exit(1)

start = jsx.find('        <div className="ss-facility-bento')
end = jsx.find('        <div className="ss-facility-footnote">', start)
if start < 0 or end < 0:
    print("ERROR: Could not safely locate the facilities grid in src/Home.jsx. No files changed.")
    sys.exit(1)

new_grid = """        <div className="ss-facility-bento ss-facility-icon-grid">
          {facilities.map((item) => {
            const Icon = item.icon;
            return (
              <article
                className={`ss-facility-card ss-facility-icon-tile tint-${item.tint}`}
                key={item.number}
                title={item.title}
                aria-label={item.title}
              >
                <span className="ss-facility-number">{item.number}</span>
                <span className="ss-facility-icon-art" aria-hidden="true">
                  <Icon size={43} strokeWidth={1.7} />
                </span>
                <span className="ss-facility-accessible-name">{item.title}</span>
              </article>
            );
          })}
        </div>
"""
new_jsx = jsx[:start] + new_grid + jsx[end:]

css_addition = r"""

/* FACILITY ICON GALLERY V4 - COLORFUL GLOSSY TILES */
.ss-facility-icon-grid{
  display:grid!important;
  grid-template-columns:repeat(5,minmax(0,1fr))!important;
  grid-auto-rows:minmax(158px,auto)!important;
  gap:16px!important;
}
.ss-facility-icon-tile{
  min-width:0;
  min-height:158px;
  padding:17px 16px!important;
  display:flex!important;
  align-items:center;
  justify-content:center;
  position:relative;
  isolation:isolate;
  overflow:hidden;
  border-radius:22px!important;
  border:1px solid rgba(255,255,255,.8)!important;
  box-shadow:0 13px 27px rgba(18,40,59,.09),inset 0 1px rgba(255,255,255,.9)!important;
  transform:translateZ(0);
  transition:transform .24s ease,box-shadow .24s ease,border-color .24s ease;
}
.ss-facility-icon-tile::after{
  content:"";
  position:absolute;
  z-index:0;
  width:130px;
  height:130px;
  right:-40px;
  bottom:-65px;
  border:1px solid currentColor;
  border-radius:50%;
  opacity:.17;
  box-shadow:0 0 0 14px rgba(255,255,255,.08),0 0 0 29px rgba(255,255,255,.06);
  pointer-events:none;
}
.ss-facility-icon-tile::before{
  content:"";
  position:absolute;
  z-index:0!important;
  top:-30%;
  left:-120%;
  width:80%;
  height:170%;
  opacity:0;
  transform:skewX(-22deg);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.13),rgba(255,255,255,.56),rgba(255,255,255,.12),transparent);
  transition:left .75s cubic-bezier(.2,.7,.2,1),opacity .25s ease;
  pointer-events:none;
}
.ss-facility-number{
  position:absolute;
  left:15px;
  top:13px;
  z-index:2;
  font-size:9px!important;
  font-weight:900!important;
  letter-spacing:1.8px;
  opacity:.68;
}
.ss-facility-icon-art{
  position:relative;
  z-index:1;
  width:83px;
  height:83px;
  display:grid;
  place-items:center;
  border-radius:27px;
  color:var(--tile-ink);
  background:linear-gradient(145deg,rgba(255,255,255,.93),rgba(255,255,255,.34));
  border:1px solid rgba(255,255,255,.94);
  box-shadow:0 12px 24px rgba(24,40,55,.12),inset 0 1px 0 rgba(255,255,255,.95),inset 0 -5px 12px rgba(255,255,255,.15);
  transition:transform .28s ease,box-shadow .28s ease;
}
.ss-facility-icon-art svg{filter:drop-shadow(0 2px 1px rgba(20,35,48,.10))}
.ss-facility-accessible-name{
  position:absolute!important;
  width:1px!important;
  height:1px!important;
  padding:0!important;
  margin:-1px!important;
  overflow:hidden!important;
  clip:rect(0,0,0,0)!important;
  white-space:nowrap!important;
  border:0!important;
}
.ss-facility-icon-tile.tint-mint{--tile-ink:#246447;background:linear-gradient(145deg,#e7f6e9 0%,#b6dec1 100%)!important;color:#246447}
.ss-facility-icon-tile.tint-peach{--tile-ink:#9a542d;background:linear-gradient(145deg,#fff0df 0%,#f0c49c 100%)!important;color:#8b4d2b}
.ss-facility-icon-tile.tint-blue{--tile-ink:#24658e;background:linear-gradient(145deg,#e5f4ff 0%,#afd8f1 100%)!important;color:#245d7d}
.ss-facility-icon-tile.tint-lavender{--tile-ink:#6c4da0;background:linear-gradient(145deg,#f1eaff 0%,#d1bdf4 100%)!important;color:#664b95}
.ss-facility-icon-tile.tint-rose{--tile-ink:#a33f5c;background:linear-gradient(145deg,#fff0f2 0%,#efbeca 100%)!important;color:#963e57}
.ss-facility-icon-tile.tint-yellow{--tile-ink:#946112;background:linear-gradient(145deg,#fff8dc 0%,#f0d483 100%)!important;color:#8c6116}
.ss-facility-icon-tile.tint-sky{--tile-ink:#24717a;background:linear-gradient(145deg,#e6fcff 0%,#addfe5 100%)!important;color:#286d76}
.ss-facility-icon-tile.tint-sage{--tile-ink:#536b36;background:linear-gradient(145deg,#f0f6df 0%,#ccdba7 100%)!important;color:#54683a}
.ss-facility-icon-tile.tint-sand{--tile-ink:#85552a;background:linear-gradient(145deg,#fbf0df 0%,#dfc29c 100%)!important;color:#80552e}
.ss-facility-icon-tile.tint-steel{--tile-ink:#3b5b7b;background:linear-gradient(145deg,#e9f2fb 0%,#bed0e3 100%)!important;color:#3b5875}
@media(hover:hover) and (pointer:fine){
 .ss-facility-icon-tile:hover{
   transform:translateY(-5px) perspective(700px) rotateX(2deg);
   box-shadow:0 20px 36px rgba(18,40,59,.15),inset 0 1px rgba(255,255,255,.95)!important;
   border-color:rgba(198,166,107,.8)!important;
 }
 .ss-facility-icon-tile:hover::before{left:135%;opacity:1}
 .ss-facility-icon-tile:hover .ss-facility-icon-art{
   transform:translateY(-2px) scale(1.045);
   box-shadow:0 17px 28px rgba(24,40,55,.16),inset 0 1px 0 rgba(255,255,255,.98);
 }
}
@media(max-width:1050px){
 .ss-facility-icon-grid{grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:13px!important}
}
@media(max-width:760px){
 .ss-facility-icon-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;grid-auto-rows:minmax(145px,auto)!important;gap:12px!important}
 .ss-facility-icon-tile{min-height:145px;padding:14px!important;border-radius:19px!important}
 .ss-facility-icon-art{width:75px;height:75px;border-radius:24px}
 .ss-facility-number{left:13px;top:11px;font-size:8px!important}
}
@media(prefers-reduced-motion:reduce){
 .ss-facility-icon-tile,.ss-facility-icon-tile::before,.ss-facility-icon-art{transition:none!important}
}
"""

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"facility-icon-gallery-v4-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(jsx_path, backup / "Home.jsx")
shutil.copy2(css_path, backup / "Home.css")

jsx_path.write_text(new_jsx, encoding="utf-8")
css_path.write_text(css + "\n" + css_addition, encoding="utf-8")

print("SUCCESS: All 10 facilities are now icon-only cards with distinct colors.")
print("Visual labels are hidden but remain available to screen readers and title tooltips.")
print("Changed only: src/Home.jsx and src/Home.css.")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Review locally before committing/pushing.")
