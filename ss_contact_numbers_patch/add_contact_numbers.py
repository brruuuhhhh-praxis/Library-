#!/usr/bin/env python3
"""Safely add Call and WhatsApp Business links to the Shri Library footer."""
from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

ROOT = Path.cwd()
HOME_JSX = ROOT / "src" / "Home.jsx"
HOME_CSS = ROOT / "src" / "Home.css"

CONTACT_BLOCK = '''        <div className="ss-footer-contact" aria-label="Contact Shri Library">
          <a className="ss-footer-contact-card ss-footer-call" href="tel:+918306349753" aria-label="Call Shri Library at 8306349753">
            <span className="ss-footer-contact-icon" aria-hidden="true">☎</span>
            <span className="ss-footer-contact-copy"><small>CALL US</small><strong>8306349753</strong><em>कॉल करें</em></span>
            <span className="ss-footer-contact-arrow" aria-hidden="true">↗</span>
          </a>
          <a className="ss-footer-contact-card ss-footer-whatsapp" href="https://wa.me/919664050399" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp Business 9664050399">
            <span className="ss-footer-contact-icon ss-footer-whatsapp-icon" aria-hidden="true">◉</span>
            <span className="ss-footer-contact-copy"><small>WHATSAPP BUSINESS</small><strong>9664050399</strong><em>WhatsApp पर मैसेज करें</em></span>
            <span className="ss-footer-contact-arrow" aria-hidden="true">↗</span>
          </a>
        </div>
'''

CSS_BLOCK = '''

/* Contact actions: phone and WhatsApp Business */
.ss-home .ss-footer .ss-footer-contact {
  width: min(100%, 760px);
  margin: 22px auto 18px !important;
  display: grid !important;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px !important;
}
.ss-home .ss-footer .ss-footer-contact-card {
  position: relative;
  isolation: isolate;
  display: flex !important;
  align-items: center !important;
  gap: 13px !important;
  min-width: 0;
  min-height: 96px;
  padding: 17px 18px !important;
  text-align: left !important;
  text-decoration: none !important;
  color: #fff7e8 !important;
  border: 1px solid rgba(255, 208, 111, .38) !important;
  border-radius: 19px !important;
  background: linear-gradient(145deg, rgba(255,255,255,.105), rgba(255,255,255,.035)), linear-gradient(125deg, #171b25, #080b12 72%) !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.12), 0 12px 28px rgba(0,0,0,.24), 0 0 22px rgba(226,171,67,.07) !important;
  transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
}
.ss-home .ss-footer .ss-footer-contact-card:hover {
  transform: translateY(-3px) !important;
  border-color: rgba(255, 211, 126, .78) !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.16), 0 17px 32px rgba(0,0,0,.32), 0 0 24px rgba(226,171,67,.13) !important;
}
.ss-home .ss-footer .ss-footer-contact-icon {
  flex: 0 0 43px;
  width: 43px;
  height: 43px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  font-size: 25px;
  color: #ffd783 !important;
  background: rgba(255, 204, 105, .12) !important;
  border: 1px solid rgba(255, 211, 126, .25);
}
.ss-home .ss-footer .ss-footer-whatsapp-icon {
  color: #b9f5ce !important;
  background: rgba(37, 211, 102, .12) !important;
  border-color: rgba(90, 227, 143, .28);
}
.ss-home .ss-footer .ss-footer-contact-copy {
  display: flex !important;
  flex: 1 1 auto;
  min-width: 0;
  flex-direction: column !important;
  align-items: flex-start !important;
  gap: 3px !important;
}
.ss-home .ss-footer .ss-footer-contact-copy small {
  color: rgba(255, 222, 163, .78) !important;
  font-size: 9px !important;
  line-height: 1.4;
  letter-spacing: .13em;
  font-weight: 800;
}
.ss-home .ss-footer .ss-footer-contact-copy strong {
  color: #fff8e9 !important;
  font-size: clamp(16px, 2vw, 20px) !important;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: .025em;
}
.ss-home .ss-footer .ss-footer-contact-copy em {
  color: rgba(255, 248, 233, .68) !important;
  font-size: 11px !important;
  line-height: 1.45;
  font-style: normal;
}
.ss-home .ss-footer .ss-footer-contact-arrow {
  flex: 0 0 auto;
  align-self: flex-start;
  color: #ffd783 !important;
  font-size: 19px;
  line-height: 1;
}
@media (max-width: 560px) {
  .ss-home .ss-footer .ss-footer-contact {
    grid-template-columns: minmax(0, 1fr);
    gap: 10px !important;
    margin: 18px auto 14px !important;
  }
  .ss-home .ss-footer .ss-footer-contact-card {
    min-height: 82px;
    padding: 14px 15px !important;
    border-radius: 16px !important;
  }
  .ss-home .ss-footer .ss-footer-contact-icon {
    flex-basis: 39px;
    width: 39px;
    height: 39px;
    border-radius: 12px;
  }
}
'''


def main() -> int:
    if not HOME_JSX.exists() or not HOME_CSS.exists():
        print("ERROR: Run this script from the shri-shyam-library project root; src/Home.jsx and src/Home.css are required.")
        return 2

    jsx = HOME_JSX.read_text(encoding="utf-8")
    css = HOME_CSS.read_text(encoding="utf-8")
    footer_start = jsx.find('<footer id="contact-preview" className="ss-footer">')
    if footer_start < 0:
        print('ERROR: Could not find <footer id="contact-preview" className="ss-footer"> in src/Home.jsx. No files changed.')
        return 2
    footer_end = jsx.find('</footer>', footer_start)
    if footer_end < 0:
        print("ERROR: Could not find the closing footer tag. No files changed.")
        return 2

    current_footer = jsx[footer_start:footer_end]
    if "ss-footer-contact" in current_footer:
        # Replace the existing contact block so the patch is safe to re-run.
        pattern = re.compile(r'\s*<div className="ss-footer-contact"\b.*?</div>\s*', re.DOTALL)
        updated_footer, count = pattern.subn("\n" + CONTACT_BLOCK, current_footer, count=1)
        if count == 0:
            print("ERROR: Contact block exists but its structure was not recognized. No files changed.")
            return 2
        new_jsx = jsx[:footer_start] + updated_footer + jsx[footer_end:]
    else:
        nav_pos = jsx.find("<nav", footer_start, footer_end)
        if nav_pos < 0:
            print("ERROR: Could not find footer navigation insertion point. No files changed.")
            return 2
        new_jsx = jsx[:nav_pos] + CONTACT_BLOCK + "        " + jsx[nav_pos:]

    # Avoid duplicating CSS if this patch is run more than once.
    if ".ss-home .ss-footer .ss-footer-contact" not in css:
        new_css = css.rstrip() + CSS_BLOCK + "\n"
    else:
        new_css = css

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = Path.home() / ".shri-shyam-library-backups" / f"contact-numbers-{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HOME_JSX, backup_dir / "Home.jsx")
    shutil.copy2(HOME_CSS, backup_dir / "Home.css")

    HOME_JSX.write_text(new_jsx, encoding="utf-8")
    HOME_CSS.write_text(new_css, encoding="utf-8")
    print("SUCCESS: Contact phone and WhatsApp Business links added to the footer.")
    print("Call: 8306349753 (tel:+918306349753)")
    print("WhatsApp Business: 9664050399 (https://wa.me/919664050399)")
    print("Updated files: src/Home.jsx, src/Home.css")
    print(f"Backup: {backup_dir}")
    print("NEXT: npm run build && git diff --check")
    return 0

if __name__ == "__main__":
    sys.exit(main())
