#!/usr/bin/env python3
"""Add a subtle premium gloss sweep to all home facility cards and center card 10 on mobile."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

root = Path.cwd()
css_path = root / "src" / "Home.css"
jsx_path = root / "src" / "Home.jsx"
if not css_path.exists() or not jsx_path.exists():
    print("ERROR: Run this script from ~/shri-shyam-library.")
    sys.exit(1)

css = css_path.read_text(encoding="utf-8")
jsx = jsx_path.read_text(encoding="utf-8")

marker = "/* FACILITY CARDS - GLOSS SWEEP & MOBILE BALANCE V3 */"
if marker in css:
    print("ERROR: V3 gloss styling is already present; no files changed.")
    sys.exit(1)

if "facilities.slice(1)" not in jsx:
    print("ERROR: Home.jsx does not currently render all facility cards. No files changed.")
    sys.exit(1)

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"facility-gloss-v3-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(css_path, backup / "Home.css")
shutil.copy2(jsx_path, backup / "Home.jsx")

css += r"""

/* FACILITY CARDS - GLOSS SWEEP & MOBILE BALANCE V3 */
.ss-facility-card,
.ss-facility-feature{
  position:relative;
  isolation:isolate;
  overflow:hidden;
}
.ss-facility-card::before,
.ss-facility-feature::before{
  content:"";
  position:absolute;
  z-index:-1;
  inset:-2px;
  pointer-events:none;
  opacity:0;
  transform:translateX(-115%) skewX(-16deg);
  background:linear-gradient(
    112deg,
    transparent 0%,
    rgba(255,255,255,0) 34%,
    rgba(255,255,255,.13) 45%,
    rgba(255,244,207,.34) 50%,
    rgba(255,255,255,.10) 56%,
    rgba(255,255,255,0) 68%,
    transparent 100%
  );
  transition:transform .75s cubic-bezier(.2,.7,.2,1),opacity .22s ease;
}
.ss-facility-card{
  border-color:rgba(198,166,107,.25);
  box-shadow:0 9px 24px rgba(18,40,59,.08),inset 0 1px 0 rgba(255,255,255,.95);
}
.ss-facility-card-top svg{
  border:1px solid rgba(198,166,107,.30);
  box-shadow:0 5px 14px rgba(18,40,59,.08),inset 0 1px rgba(255,255,255,.95);
}
.ss-facility-card:focus-within::before,
.ss-facility-card:active::before,
.ss-facility-feature:focus-within::before,
.ss-facility-feature:active::before{
  opacity:1;
  transform:translateX(115%) skewX(-16deg);
}
@media (hover:hover) and (pointer:fine){
  .ss-facility-card:hover::before,
  .ss-facility-feature:hover::before{
    opacity:1;
    transform:translateX(115%) skewX(-16deg);
  }
  .ss-facility-card:hover,
  .ss-facility-feature:hover{
    box-shadow:0 18px 36px rgba(18,40,59,.15),inset 0 1px 0 rgba(255,255,255,.9);
  }
}
@media(max-width:760px){
  /* Facility 10 (parking) is centered on its own final row. */
  .ss-facility-card:last-child{
    grid-column:1/-1;
    width:calc(50% - 5px);
    justify-self:center;
  }
}
@media(prefers-reduced-motion:reduce){
  .ss-facility-card::before,
  .ss-facility-feature::before{
    transition:none!important;
  }
}
"""
css_path.write_text(css, encoding="utf-8")
print("SUCCESS: Gloss sweep added to feature + all 9 facility cards.")
print("Mobile: facility 10 (parking) is centered on the final row.")
print("Changed: src/Home.css only.")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Review locally before committing/pushing.")
