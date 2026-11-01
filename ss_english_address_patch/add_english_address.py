#!/usr/bin/env python3
"""Add an English address card to Shri Shyam Library's Contact footer."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
HOME_JSX = ROOT / "src" / "Home.jsx"
HOME_CSS = ROOT / "src" / "Home.css"
MARKER = "ss-footer-address-en"

ADDRESS_BLOCK = '''
        <section className="ss-footer-address-en" aria-label="Library address in English">
          <div className="ss-footer-address-pin" aria-hidden="true">📍</div>
          <div className="ss-footer-address-copy">
            <span className="ss-footer-address-kicker">VISIT US</span>
            <strong>Shri Shyam Library</strong>
            <p>Ward No. 3, Gurudwara Road, Bishnoi Mohalla, Suratgarh, Rajasthan – 335804</p>
            <small><span aria-hidden="true">⌖</span> Landmark: 100 metres from Paras Hyundai</small>
          </div>
        </section>
'''

CSS_BLOCK = '''

/* English address card — ss-footer-address-en */
.ss-home .ss-footer .ss-footer-address-en {
  position: relative;
  isolation: isolate;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  width: min(100%, 760px);
  box-sizing: border-box;
  margin: 20px auto 18px;
  padding: 19px 21px;
  text-align: left;
  border: 1px solid rgba(255, 208, 111, .34);
  border-radius: 20px;
  background: linear-gradient(145deg, rgba(255,255,255,.09), rgba(255,255,255,.025)), linear-gradient(125deg, rgba(25,29,39,.96), rgba(7,10,16,.96));
  box-shadow: inset 0 1px 0 rgba(255,255,255,.10), 0 12px 28px rgba(0,0,0,.22);
}
.ss-home .ss-footer .ss-footer-address-pin {
  display: grid;
  place-items: center;
  flex: 0 0 42px;
  width: 42px;
  height: 42px;
  border: 1px solid rgba(255,211,126,.25);
  border-radius: 14px;
  background: rgba(255,204,105,.11);
  font-size: 21px;
}
.ss-home .ss-footer .ss-footer-address-copy {
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
}
.ss-home .ss-footer .ss-footer-address-kicker {
  color: rgba(255,222,163,.78);
  font-size: 9px;
  line-height: 1.4;
  letter-spacing: .15em;
  font-weight: 800;
}
.ss-home .ss-footer .ss-footer-address-copy strong {
  color: #fff7e8;
  font-size: 17px;
  line-height: 1.35;
  font-weight: 800;
}
.ss-home .ss-footer .ss-footer-address-copy p {
  margin: 0;
  color: rgba(255,248,233,.84);
  font-size: 13px;
  line-height: 1.7;
  overflow-wrap: anywhere;
}
.ss-home .ss-footer .ss-footer-address-copy small {
  color: #ffd783;
  font-size: 11px;
  line-height: 1.55;
}
@media (max-width: 560px) {
  .ss-home .ss-footer .ss-footer-address-en {
    gap: 11px;
    margin: 17px auto 14px;
    padding: 15px 14px;
    border-radius: 17px;
  }
  .ss-home .ss-footer .ss-footer-address-pin {
    flex-basis: 36px;
    width: 36px;
    height: 36px;
    border-radius: 12px;
    font-size: 18px;
  }
  .ss-home .ss-footer .ss-footer-address-copy strong { font-size: 15px; }
  .ss-home .ss-footer .ss-footer-address-copy p { font-size: 12px; }
}
'''

def main() -> int:
    if not HOME_JSX.exists() or not HOME_CSS.exists():
        print("ERROR: Run this script from ~/shri-shyam-library; src/Home.jsx and src/Home.css are required.")
        return 2

    jsx = HOME_JSX.read_text(encoding="utf-8")
    css = HOME_CSS.read_text(encoding="utf-8")
    if MARKER in jsx:
        print("ALREADY APPLIED: English address card is already present; no changes made.")
        return 0

    footer_start = jsx.find('<footer id="contact-preview"')
    if footer_start < 0:
        print('ERROR: Could not find <footer id="contact-preview" in src/Home.jsx. No files changed.')
        return 2
    footer_end = jsx.find('</footer>', footer_start)
    if footer_end < 0:
        print("ERROR: Could not find the Contact footer closing tag. No files changed.")
        return 2

    footer = jsx[footer_start:footer_end]
    # Put the address before phone/WhatsApp cards when present; otherwise, before footer navigation.
    insert_rel = footer.find('<div className="ss-footer-contact"')
    if insert_rel < 0:
        insert_rel = footer.find('<nav')
    if insert_rel < 0:
        insert_rel = len(footer)
    insert_at = footer_start + insert_rel
    new_jsx = jsx[:insert_at] + ADDRESS_BLOCK + "\n        " + jsx[insert_at:]
    new_css = css if MARKER in css else css.rstrip() + CSS_BLOCK + "\n"

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = Path.home() / ".shri-shyam-library-backups" / f"english-address-{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HOME_JSX, backup_dir / "Home.jsx")
    shutil.copy2(HOME_CSS, backup_dir / "Home.css")
    HOME_JSX.write_text(new_jsx, encoding="utf-8")
    HOME_CSS.write_text(new_css, encoding="utf-8")

    print("SUCCESS: English address added to the Contact footer.")
    print("Address: Ward No. 3, Gurudwara Road, Bishnoi Mohalla, Suratgarh, Rajasthan – 335804")
    print("Landmark: 100 metres from Paras Hyundai")
    print("Updated: src/Home.jsx, src/Home.css")
    print(f"Backup: {backup_dir}")
    print("NEXT: npm run build && git diff --check")
    return 0

if __name__ == "__main__":
    sys.exit(main())
