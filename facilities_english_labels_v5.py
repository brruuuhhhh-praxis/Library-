#!/usr/bin/env python3
"""Show English names/descriptions under all facility icons; replace parking with newspapers and CA magazine."""
from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

root = Path.cwd()
jsx_path = root / "src" / "Home.jsx"
css_path = root / "src" / "Home.css"
if not jsx_path.exists() or not css_path.exists():
    print("ERROR: Run from ~/shri-shyam-library.")
    sys.exit(1)

jsx = jsx_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")
marker = "/* FACILITY ICONS WITH ENGLISH LABELS V5 */"
if marker in css or marker in jsx:
    print("ERROR: V5 patch already appears to be applied. No files changed.")
    sys.exit(1)

if "facilities.map((item) =>" not in jsx or 'className="ss-facility-accessible-name"' not in jsx:
    print("ERROR: Expected icon-only facility grid not found. No files changed.")
    sys.exit(1)

facility_content = {
    "01": ("BookOpen", "Quiet Study Environment", "A calm space for focused preparation"),
    "02": ("Armchair", "Personal Study Desk", "Your own desk for daily study goals"),
    "03": ("Wifi", "High-Speed Wi-Fi", "Stay connected for digital learning"),
    "04": ("Snowflake", "AC-Cooled Comfort", "A comfortable space through study hours"),
    "05": ("ShieldCheck", "CCTV Security", "A security-focused study environment"),
    "06": ("Zap", "Power Backup", "Keep your study sessions uninterrupted"),
    "07": ("Droplets", "Clean Drinking Water", "Stay refreshed while you study"),
    "08": ("Coffee", "Clean & Hygienic Space", "A clean, comfortable study environment"),
    "09": ("Bookmark", "Personal Bookshelf", "Keep your study materials organized"),
    "10": ("Newspaper", "Daily Newspapers & Monthly CA Magazine", "Daily news and monthly current-affairs revision"),
}

for number, (icon, title, subtitle) in facility_content.items():
    pattern = re.compile(
        r"\{ icon: \w+, title: '[^']*', subtitle: '[^']*', tint: '([^']*)', number: '" + number + r"' \},"
    )
    replacement = (
        "{ icon: " + icon + ", title: '" + title + "', subtitle: '" + subtitle
        + "', tint: '\\1', number: '" + number + "' },"
    )
    jsx_new, count = pattern.subn(replacement, jsx, count=1)
    if count != 1:
        print(f"ERROR: Could not find facility data row {number}. No files changed.")
        sys.exit(1)
    jsx = jsx_new

old_markup = '<span className="ss-facility-accessible-name">{item.title}</span>'
new_markup = "\n".join([
    '<div className="ss-facility-english-copy">',
    '  <strong>{item.title}</strong>',
    '  <small>{item.subtitle}</small>',
    '</div>',
])
if old_markup not in jsx:
    print("ERROR: Could not find the icon-only label markup. No files changed.")
    sys.exit(1)
jsx = jsx.replace(old_markup, new_markup, 1)

jsx = jsx.replace("Monitor, ParkingCircle, ShieldCheck", "Monitor, Newspaper, ShieldCheck", 1)
if "Newspaper" not in jsx.split("from 'lucide-react'")[0]:
    print("ERROR: Could not safely add Newspaper icon import. No files changed.")
    sys.exit(1)

css_addition = r"""

/* FACILITY ICONS WITH ENGLISH LABELS V5 */
.ss-facility-icon-tile{
  min-height:198px!important;
  padding:24px 12px 15px!important;
  flex-direction:column!important;
  justify-content:center!important;
  gap:10px!important;
}
.ss-facility-icon-art{
  flex:0 0 auto;
  width:62px!important;
  height:62px!important;
  border-radius:20px!important;
}
.ss-facility-icon-art svg{width:31px;height:31px}
.ss-facility-english-copy{
  position:relative;
  z-index:2;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:flex-start;
  gap:5px;
  width:100%;
  max-width:100%;
  text-align:center;
}
.ss-facility-english-copy strong{
  display:block;
  font-family:'DM Sans','Noto Sans Devanagari',sans-serif;
  color:#182b3b;
  font-size:12px;
  font-weight:800;
  line-height:1.35;
  letter-spacing:-.1px;
  text-wrap:balance;
  overflow-wrap:anywhere;
}
.ss-facility-english-copy small{
  display:block;
  max-width:27ch;
  font-family:'DM Sans','Noto Sans Devanagari',sans-serif;
  color:#596b78;
  font-size:10px;
  line-height:1.5;
  font-weight:500;
  text-wrap:pretty;
  overflow-wrap:anywhere;
}
@media(min-width:1200px){
  .ss-facility-icon-grid{grid-template-columns:repeat(5,minmax(0,1fr))!important}
  .ss-facility-icon-tile{min-height:202px!important}
  .ss-facility-english-copy strong{font-size:13px}
  .ss-facility-english-copy small{font-size:10px}
}
@media(max-width:1050px){
  .ss-facility-icon-grid{grid-template-columns:repeat(4,minmax(0,1fr))!important}
  .ss-facility-icon-tile{min-height:190px!important}
}
@media(max-width:760px){
  .ss-facility-icon-grid{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
    grid-auto-rows:minmax(194px,auto)!important;
    gap:12px!important;
  }
  .ss-facility-icon-grid .ss-facility-icon-tile:last-child{
    grid-column:auto!important;
    width:auto!important;
    justify-self:stretch!important;
  }
  .ss-facility-icon-tile{
    min-height:194px!important;
    padding:25px 11px 14px!important;
    gap:10px!important;
    border-radius:19px!important;
  }
  .ss-facility-icon-art{width:56px!important;height:56px!important;border-radius:18px!important}
  .ss-facility-icon-art svg{width:28px;height:28px}
  .ss-facility-english-copy{gap:5px}
  .ss-facility-english-copy strong{font-size:11px;line-height:1.4}
  .ss-facility-english-copy small{font-size:9px;line-height:1.45;max-width:24ch}
}
@media(prefers-reduced-motion:reduce){
  .ss-facility-icon-art,.ss-facility-icon-tile{transition:none!important}
}
"""

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"facility-english-labels-v5-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(jsx_path, backup / "Home.jsx")
shutil.copy2(css_path, backup / "Home.css")

jsx_path.write_text(jsx, encoding="utf-8")
css_path.write_text(css + "\n" + css_addition, encoding="utf-8")

print("SUCCESS: English titles and descriptions added to all 10 facility icons.")
print("Facility 10 is now Daily Newspapers & Monthly CA Magazine (replaces parking).")
print("Changed only: src/Home.jsx and src/Home.css.")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Review locally before committing/pushing.")
