from pathlib import Path
import re
import shutil
from datetime import datetime

ROOT = Path.cwd()
jsx = ROOT / 'src' / 'Home.jsx'
css = ROOT / 'src' / 'Home.css'
if not jsx.exists() or not css.exists():
    raise SystemExit('ERROR: Run this script from ~/shri-shyam-library (src/Home.jsx and src/Home.css must exist).')

text = jsx.read_text(encoding='utf-8')
css_text = css.read_text(encoding='utf-8')

open_tag = '<section className="ss-contact-panel" aria-labelledby="ss-contact-panel-title">'
if open_tag not in text:
    location_pos = text.find('<a className="ss-contact-location-link"')
    address_pos = text.find('<section className="ss-footer-address-en"')
    contact_pos = text.find('<div className="ss-footer-contact"')
    if min(location_pos, address_pos, contact_pos) < 0 or not (location_pos < address_pos < contact_pos):
        raise SystemExit('ERROR: Could not safely locate the location link, English address card and contact cards. No files changed.')

    # Find beginning of the location link line.
    start = text.rfind('\n', 0, location_pos) + 1
    # Find matching closing div for the ss-footer-contact wrapper using div depth.
    line_start = text.rfind('\n', 0, contact_pos) + 1
    depth = 0
    end = None
    pos = line_start
    for line in text[line_start:].splitlines(keepends=True):
        # Count JSX div opening/closing tags in this wrapper only.
        depth += len(re.findall(r'<div\b', line))
        depth -= len(re.findall(r'</div\s*>', line))
        pos += len(line)
        if depth == 0:
            end = pos
            break
    if end is None:
        raise SystemExit('ERROR: Could not find the end of the contact cards wrapper. No files changed.')

    prefix = '''        <section className="ss-contact-panel" aria-labelledby="ss-contact-panel-title">
          <header className="ss-contact-panel-heading">
            <span className="ss-contact-panel-kicker">CONTACT &amp; LOCATION</span>
            <h2 id="ss-contact-panel-title">हमसे जुड़ें</h2>
            <p>लाइब्रेरी का पता और संपर्क जानकारी</p>
          </header>
'''
    # The location link begins at start; preserve all existing nodes through footer-contact.
    text = text[:start] + prefix + text[start:end] + '        </section>\n' + text[end:]

# Append narrowly-scoped CSS once; avoids disturbing unrelated homepage styles.
css_marker = '/* SS CONTACT COMPACT PANEL PATCH */'
if css_marker not in css_text:
    css_addition = r'''

/* SS CONTACT COMPACT PANEL PATCH */
.ss-contact-panel {
  box-sizing: border-box;
  width: min(100% - 28px, 760px);
  margin: 28px auto 34px;
  padding: clamp(16px, 4vw, 26px);
  display: flex;
  flex-direction: column;
  gap: 14px;
  border: 1px solid rgba(203, 164, 83, 0.68);
  border-radius: 28px;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.78), rgba(244, 239, 222, 0.76));
  box-shadow: 0 18px 42px rgba(24, 31, 40, 0.10), inset 0 1px 0 rgba(255, 255, 255, 0.82);
  -webkit-backdrop-filter: blur(14px);
  backdrop-filter: blur(14px);
}

.ss-contact-panel-heading {
  padding: 2px 3px 4px;
  text-align: left;
}

.ss-contact-panel-kicker {
  display: inline-block;
  color: #8c6b2a;
  font-size: 0.72rem;
  font-weight: 850;
  letter-spacing: 0.16em;
  line-height: 1.4;
}

.ss-contact-panel-heading h2 {
  margin: 5px 0 3px;
  color: #202c37;
  font-size: clamp(1.35rem, 4.3vw, 1.8rem);
  line-height: 1.25;
  font-weight: 850;
}

.ss-contact-panel-heading p {
  margin: 0;
  color: #63717b;
  font-size: 0.94rem;
  line-height: 1.55;
}

.ss-contact-panel > .ss-contact-location-link,
.ss-contact-panel > .ss-footer-address-en,
.ss-contact-panel > .ss-footer-contact {
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  margin: 0 !important;
}

.ss-contact-panel > .ss-contact-location-link {
  align-self: flex-start;
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  padding: 12px 17px;
  border-radius: 15px;
  text-align: center;
  line-height: 1.35;
}

.ss-contact-panel > .ss-footer-address-en {
  padding: clamp(16px, 4vw, 22px);
  border-radius: 20px;
}

.ss-contact-panel > .ss-footer-contact {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 10px;
}

.ss-contact-panel .ss-footer-contact-card {
  box-sizing: border-box;
  min-width: 0;
  min-height: 88px;
  margin: 0 !important;
  padding: 14px 16px;
  border-radius: 18px;
}

.ss-contact-panel .ss-footer-address-copy p {
  overflow-wrap: anywhere;
  line-height: 1.55;
}

.ss-contact-panel .ss-footer-address-copy small {
  display: block;
  line-height: 1.5;
}

@media (min-width: 680px) {
  .ss-contact-panel > .ss-footer-contact {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 420px) {
  .ss-contact-panel {
    width: calc(100% - 24px);
    padding: 14px;
    gap: 12px;
    border-radius: 23px;
  }

  .ss-contact-panel > .ss-contact-location-link {
    align-self: stretch;
    width: 100%;
    font-size: 0.96rem;
  }

  .ss-contact-panel > .ss-footer-address-en {
    gap: 12px;
  }

  .ss-contact-panel .ss-footer-contact-card {
    min-height: 82px;
    padding: 13px 14px;
  }
}
'''
    css_text = css_text.rstrip() + css_addition + '\n'

# Back up before writing so this patch can be rolled back safely.
backup_root = Path.home() / '.shri-shyam-library-backups' / ('contact-compact-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
backup_root.mkdir(parents=True, exist_ok=True)
shutil.copy2(jsx, backup_root / 'Home.jsx')
shutil.copy2(css, backup_root / 'Home.css')
jsx.write_text(text, encoding='utf-8')
css.write_text(css_text.rstrip() + '\n', encoding='utf-8')
print('SUCCESS: Contact & Location section grouped into one responsive panel.')
print('Updated: src/Home.jsx, src/Home.css')
print(f'Backup: {backup_root}')
print('NEXT: npm run build && git diff --check')
