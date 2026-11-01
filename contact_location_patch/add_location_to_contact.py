#!/usr/bin/env python3
"""Safely add a Google Maps location link to Shri Shyam Library's Contact footer."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
HOME = ROOT / 'src' / 'Home.jsx'
CSS = ROOT / 'src' / 'Home.css'
MAP_URL = 'https://maps.app.goo.gl/92QvGfjMJF5mAWTL7?g_st=ac'
LINK_MARKER = 'ss-contact-location-link'

if not (ROOT / 'package.json').exists():
    sys.exit('ERROR: package.json not found. Run this script from ~/shri-shyam-library.')
if not HOME.exists() or not CSS.exists():
    sys.exit('ERROR: expected src/Home.jsx and src/Home.css; no files were changed.')

jsx = HOME.read_text(encoding='utf-8')
css = CSS.read_text(encoding='utf-8')
if LINK_MARKER in jsx:
    print('ALREADY APPLIED: Contact location link already exists; no changes made.')
    sys.exit(0)

footer_start = jsx.find('<footer id="contact-preview"')
if footer_start < 0:
    sys.exit('ERROR: could not find the Contact footer anchor in src/Home.jsx; no files were changed.')
footer_end = jsx.find('</footer>', footer_start)
if footer_end < 0:
    sys.exit('ERROR: Contact footer closing tag not found; no files were changed.')
footer = jsx[footer_start:footer_end]
anchor = '<p>एकाग्रता से तैयारी, तैयारी से सफलता।</p>'
anchor_pos = footer.find(anchor)
if anchor_pos < 0:
    sys.exit('ERROR: expected footer tagline was not found; no files were changed. Please share the current footer code.')

insert = '''\n        <a className="ss-contact-location-link" href="https://maps.app.goo.gl/92QvGfjMJF5mAWTL7?g_st=ac" target="_blank" rel="noopener noreferrer" aria-label="Google Maps पर लाइब्रेरी की लोकेशन खोलें">\n          <span aria-hidden="true">📍</span> लाइब्रेरी की लोकेशन देखें <ArrowUpRight size={16} />\n        </a>'''
insert_at = footer_start + anchor_pos + len(anchor)
new_jsx = jsx[:insert_at] + insert + jsx[insert_at:]

css_addition = '''\n\n/* Contact footer: Google Maps location CTA */\n.ss-contact-location-link {\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  gap: 10px;\n  width: fit-content;\n  max-width: 100%;\n  margin: 14px auto 18px;\n  padding: 12px 18px;\n  border: 1px solid rgba(255, 207, 112, .58);\n  border-radius: 999px;\n  color: #ffe2a5 !important;\n  background: linear-gradient(135deg, rgba(255, 207, 112, .14), rgba(14, 28, 45, .82));\n  box-shadow: 0 8px 24px rgba(0, 0, 0, .18), inset 0 1px 0 rgba(255, 255, 255, .12);\n  font-size: 14px;\n  font-weight: 700;\n  text-decoration: none !important;\n  transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;\n}\n.ss-contact-location-link:hover {\n  transform: translateY(-2px);\n  border-color: rgba(255, 220, 150, .95);\n  box-shadow: 0 12px 28px rgba(0, 0, 0, .25), 0 0 18px rgba(255, 194, 83, .12);\n}\n.ss-contact-location-link:focus-visible { outline: 2px solid #ffcf70; outline-offset: 4px; }\n@media (max-width: 600px) {\n  .ss-contact-location-link { margin: 12px auto 16px; padding: 11px 15px; font-size: 13px; }\n}\n'''
new_css = css if LINK_MARKER in css else css + css_addition.replace('/* Contact footer: Google Maps location CTA */', '/* Contact footer: Google Maps location CTA — ss-contact-location-link */')

backup_root = Path.home() / '.shri-shyam-library-backups' / f'contact-location-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
backup_root.mkdir(parents=True, exist_ok=True)
shutil.copy2(HOME, backup_root / 'Home.jsx')
shutil.copy2(CSS, backup_root / 'Home.css')
HOME.write_text(new_jsx, encoding='utf-8')
CSS.write_text(new_css, encoding='utf-8')
print('SUCCESS: Google Maps location link added to the Contact footer.')
print('Updated files: src/Home.jsx, src/Home.css')
print('Link opens in a new tab: ' + MAP_URL)
print('Backup: ' + str(backup_root))
print('NEXT: npm run build && git diff --check')
