#!/usr/bin/env python3
"""Repair Shri Shyam Library hero quote placement and portrait glass cards.

Run from ~/shri-shyam-library. Makes timestamped backups before any edits.
Only src/Home.jsx and src/Home.css are edited.
"""
from pathlib import Path
from datetime import datetime
import shutil, sys

ROOT = Path.cwd()
JSX = ROOT / 'src' / 'Home.jsx'
CSS = ROOT / 'src' / 'Home.css'
JSX_MARKER = 'SS HERO LEFT QUOTE GLASS CARDS V3'
CSS_MARKER = 'SS HERO LEFT QUOTE + PORTRAIT CARDS V3'

if not JSX.is_file() or not CSS.is_file():
    print('ERROR: Run this from ~/shri-shyam-library; src/Home.jsx and src/Home.css are required.')
    sys.exit(1)

jsx = JSX.read_text(encoding='utf-8')
css = CSS.read_text(encoding='utf-8')

required = ['className="ss-hero"', 'className="ss-capacity-wrap"', 'className="ss-ca-preview"', 'className="ss-hero-content']
missing = [item for item in required if item not in jsx]
if missing:
    print('ERROR: Home.jsx does not match the expected homepage structure; no files changed.')
    print('Missing:', ', '.join(missing))
    sys.exit(2)

new_jsx = jsx
changed_jsx = False

# Replace the entire hero content area, including old decorative note/bottom-line.
if JSX_MARKER not in new_jsx:
    hero_start = new_jsx.find('<div className="ss-hero-content')
    import re
    hero_close = re.search(r'^\s*</section\s*>', new_jsx[hero_start:], re.M) if hero_start >= 0 else None
    hero_end = hero_start + hero_close.start() if hero_close else -1
    if hero_start < 0 or hero_end < 0:
        print('ERROR: Could not locate the complete hero content block; no files changed.')
        sys.exit(3)
    hero_replacement = '''<div className="ss-hero-content ss-hero-minimal-content" aria-label="Library hero">
          <p className="ss-hero-signature-quote">Success is when your signature becomes an autograph.</p>
          <div className="ss-hero-actions ss-hero-minimal-actions">
            <a className="ss-button ss-button-gold" href="#/register">अपना रजिस्ट्रेशन करें <ArrowRight size={17} /></a>
          </div>
        </div>
        {/* SS HERO LEFT QUOTE GLASS CARDS V3: keep hero text minimal */}
'''
    # Preserve indentation before the existing opening tag.
    line_start = new_jsx.rfind('\n', 0, hero_start) + 1
    indent = new_jsx[line_start:hero_start]
    if indent.strip():
        indent = ''
    new_jsx = new_jsx[:hero_start] + hero_replacement + new_jsx[hero_end:]
    changed_jsx = True

# Group the two sections in a shared row of standing glass cards, with no hero overlap.
if '<div className="ss-hero-followup-cards">' not in new_jsx:
    facilities_marker = '      {/* 4. FACILITIES'
    facilities_start = new_jsx.find(facilities_marker)
    if facilities_start < 0:
        print('ERROR: Could not locate the Facilities section; no files changed.')
        sys.exit(4)
    snapshot_comment_candidates = [
        new_jsx.find('      {/* 3. CAPACITY STRIP'),
        new_jsx.find('      {/* 3. LIBRARY SNAPSHOT'),
        new_jsx.find('        <section className="ss-capacity-wrap"'),
    ]
    valid_candidates = [p for p in snapshot_comment_candidates if p >= 0 and p < facilities_start]
    if not valid_candidates:
        print('ERROR: Could not locate Library Snapshot section; no files changed.')
        sys.exit(5)
    cards_start = min(valid_candidates)
    cards_block = new_jsx[cards_start:facilities_start].rstrip()
    # Remove a stale V2 comment only; preserve all section content and JSX.
    cards_block = cards_block.replace('      {/* SS HERO PORTRAIT GLASS V2: paired vertical glass cards */}\n', '')
    wrapper = ('      {/* SS HERO LEFT QUOTE GLASS CARDS V3 */}\n'
               '      <div className="ss-hero-followup-cards">\n'
               + cards_block + '\n'
               '      </div>\n\n')
    new_jsx = new_jsx[:cards_start] + wrapper + new_jsx[facilities_start:]
    changed_jsx = True

# Real opening hours and exact CTA label requested by the user.
for old in ('लाइब्रेरी के समय के लिए संपर्क करें', 'लाइब्रेरी के समय के लिए संपर्क करें।'):
    if old in new_jsx:
        new_jsx = new_jsx.replace(old, 'सुबह 6:00 बजे से रात 12:00 बजे तक')
if 'लाइब्रेरी के समय के लिए संपर्क करें' in new_jsx:
    new_jsx = new_jsx.replace('लाइब्रेरी के समय के लिए संपर्क करें', 'सुबह 6:00 बजे से रात 12:00 बजे तक')
if 'अपनी सीट बुक करें' in new_jsx:
    # Only replace the hero CTA; other booking CTAs remain untouched.
    start = new_jsx.find('className="ss-hero-actions ss-hero-minimal-actions"')
    if start >= 0:
        end = new_jsx.find('</div>', start)
        segment = new_jsx[start:end]
        segment_new = segment.replace('अपनी सीट बुक करें', 'अपना रजिस्ट्रेशन करें')
        if segment_new != segment:
            new_jsx = new_jsx[:start] + segment_new + new_jsx[end:]

# Append a high-specificity override, deliberately AFTER old V2 CSS so it wins.
css_patch = r'''

/* SS HERO LEFT QUOTE + PORTRAIT CARDS V3 */
.ss-home > .ss-hero {
  position: relative !important;
  isolation: isolate;
  min-height: clamp(660px, 86svh, 900px) !important;
  height: auto !important;
  overflow: hidden !important;
  display: block !important;
}
.ss-home > .ss-hero .ss-hero-image {
  position: absolute !important;
  inset: 0 !important;
  z-index: 0 !important;
  background-size: cover !important;
  background-position: center right !important;
  transform: scale(1.012) !important;
}
.ss-home > .ss-hero .ss-hero-shade {
  position: absolute !important;
  inset: 0 !important;
  z-index: 1 !important;
  pointer-events: none !important;
  background: linear-gradient(90deg, rgba(3,8,15,.60) 0%, rgba(3,8,15,.28) 38%, rgba(3,8,15,.05) 100%),
              linear-gradient(0deg, rgba(3,8,15,.28), transparent 42%) !important;
}
.ss-home .ss-hero .ss-hero-minimal-content {
  position: absolute !important;
  inset: 0 !important;
  z-index: 3 !important;
  display: block !important;
  width: 100% !important;
  max-width: none !important;
  min-height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}
.ss-home .ss-hero .ss-hero-signature-quote {
  position: absolute !important;
  top: clamp(22px, 4.2svh, 48px) !important;
  left: clamp(18px, 4.2vw, 58px) !important;
  width: min(285px, 53vw) !important;
  max-width: 285px !important;
  margin: 0 !important;
  color: #ffe1a0 !important;
  font-family: Georgia, 'Times New Roman', serif !important;
  font-size: clamp(13px, 1.45vw, 18px) !important;
  font-weight: 500 !important;
  line-height: 1.45 !important;
  letter-spacing: .015em !important;
  text-wrap: pretty;
  text-shadow: 0 2px 14px rgba(0,0,0,.85), 0 0 20px rgba(255,186,65,.14) !important;
}
.ss-home .ss-hero .ss-hero-minimal-actions {
  position: absolute !important;
  top: 43% !important;
  left: clamp(18px, 4.2vw, 58px) !important;
  margin: 0 !important;
  z-index: 4 !important;
}
.ss-home .ss-hero .ss-hero-minimal-actions .ss-button {
  min-height: 48px !important;
  padding: 12px 20px !important;
  font-size: 14px !important;
  box-shadow: 0 8px 28px rgba(247,181,54,.24) !important;
}

/* Independent portrait cards below the hero — deliberately no negative margin. */
.ss-home .ss-hero-followup-cards {
  position: relative !important;
  z-index: 2 !important;
  isolation: isolate;
  display: grid !important;
  grid-template-columns: minmax(0, .92fr) minmax(0, 1.08fr) !important;
  align-items: stretch !important;
  gap: clamp(14px, 2.3vw, 26px) !important;
  width: min(1000px, calc(100% - 40px)) !important;
  margin: 30px auto 64px !important;
}
.ss-home .ss-hero-followup-cards > .ss-capacity-wrap,
.ss-home .ss-hero-followup-cards > .ss-ca-preview {
  position: relative !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  align-items: stretch !important;
  width: 100% !important;
  min-width: 0 !important;
  min-height: 390px !important;
  height: auto !important;
  margin: 0 !important;
  padding: clamp(18px, 2.5vw, 28px) !important;
  overflow: hidden !important;
  border: 1px solid rgba(255,207,112,.62) !important;
  border-radius: 25px !important;
  background:
    radial-gradient(ellipse at 88% 5%, rgba(255,190,65,.22), transparent 40%),
    radial-gradient(ellipse at 10% 100%, rgba(30,108,157,.24), transparent 48%),
    linear-gradient(145deg, rgba(9,18,29,.97), rgba(4,9,17,.94)) !important;
  color: #fff7e7 !important;
  box-shadow: 0 18px 38px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.16), inset 0 -1px 0 rgba(255,194,74,.18), 0 0 24px rgba(247,183,63,.11) !important;
  backdrop-filter: blur(20px) saturate(135%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(135%) !important;
  transform: perspective(1000px) rotateY(-.4deg) !important;
}
.ss-home .ss-hero-followup-cards > .ss-ca-preview {
  transform: perspective(1000px) rotateY(.4deg) !important;
}
.ss-home .ss-hero-followup-cards > .ss-capacity-wrap::before,
.ss-home .ss-hero-followup-cards > .ss-ca-preview::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  z-index: 0 !important;
  border-radius: inherit !important;
  pointer-events: none !important;
  background: linear-gradient(128deg, rgba(255,255,255,.10), transparent 28%, transparent 66%, rgba(255,196,82,.12)) !important;
}
.ss-home .ss-hero-followup-cards > .ss-capacity-wrap::after,
.ss-home .ss-hero-followup-cards > .ss-ca-preview::after {
  content: '' !important;
  position: absolute !important;
  inset: 1px !important;
  z-index: 0 !important;
  border-radius: inherit !important;
  pointer-events: none !important;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.035), inset 0 0 36px rgba(255,181,48,.035) !important;
}
.ss-home .ss-hero-followup-cards > .ss-capacity-wrap * ,
.ss-home .ss-hero-followup-cards > .ss-ca-preview * { position: relative; z-index: 1; }
.ss-home .ss-hero-followup-cards .ss-capacity-card {
  display: flex !important;
  flex: 1 1 auto !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  justify-content: space-between !important;
  gap: 20px !important;
  width: 100% !important;
  min-height: 335px !important;
  height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  border: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}
.ss-home .ss-hero-followup-cards .ss-capacity-intro {
  display: grid !important;
  grid-template-columns: auto minmax(0, 1fr) !important;
  align-items: center !important;
  column-gap: 9px !important;
  row-gap: 6px !important;
}
.ss-home .ss-hero-followup-cards .ss-capacity-intro small { grid-column: 2 !important; }
.ss-home .ss-hero-followup-cards .ss-capacity-intro > span:not(.ss-live-dot) { color: #ffe1a0 !important; letter-spacing: .13em !important; font-size: 10px !important; }
.ss-home .ss-hero-followup-cards .ss-capacity-intro small,
.ss-home .ss-hero-followup-cards .ss-capacity-item span { color: rgba(255,247,231,.76) !important; }
.ss-home .ss-hero-followup-cards .ss-capacity-item {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  gap: 7px !important;
  margin: 0 !important;
  padding: 0 !important;
  border: 0 !important;
  color: #fff7e7 !important;
}
.ss-home .ss-hero-followup-cards .ss-capacity-item strong { color: #ffe0a0 !important; font-size: 36px !important; line-height: 1.05 !important; }
.ss-home .ss-hero-followup-cards .ss-capacity-item .ss-time { color: #ffe0a0 !important; font-size: 18px !important; }
.ss-home .ss-hero-followup-cards .ss-capacity-divider { display: none !important; }
.ss-home .ss-hero-followup-cards .ss-capacity-link { display: inline-flex !important; align-items: center !important; gap: 8px !important; margin-top: auto !important; color: #ffcf69 !important; }
.ss-home .ss-hero-followup-cards .ss-ca-preview-copy { width: 100% !important; max-width: none !important; margin: 0 !important; }
.ss-home .ss-hero-followup-cards .ss-ca-preview-kicker { color: #ffce69 !important; font-size: 10px !important; letter-spacing: .12em !important; line-height: 1.5 !important; }
.ss-home .ss-hero-followup-cards .ss-ca-preview h2 { margin: 20px 0 14px !important; color: #fff8e9 !important; font-size: clamp(22px, 2.6vw, 30px) !important; line-height: 1.3 !important; }
.ss-home .ss-hero-followup-cards .ss-ca-preview h2 em { color: #ffd16d !important; }
.ss-home .ss-hero-followup-cards .ss-ca-preview p { color: rgba(255,248,233,.78) !important; font-size: 14px !important; line-height: 1.65 !important; }
.ss-home .ss-hero-followup-cards .ss-ca-preview-tags { display: flex !important; flex-wrap: wrap !important; gap: 7px !important; }
.ss-home .ss-hero-followup-cards .ss-ca-preview-tags span { border: 1px solid rgba(255,212,124,.25) !important; background: rgba(255,255,255,.045) !important; color: #fff2d2 !important; }
.ss-home .ss-hero-followup-cards .ss-ca-preview-cta { align-self: flex-start !important; margin-top: auto !important; color: #201505 !important; }
@media (max-width: 680px), (pointer: coarse) {
  .ss-home > .ss-hero { min-height: max(660px, 84svh) !important; }
  .ss-home .ss-hero .ss-hero-image { background-position: 62% center !important; }
  .ss-home .ss-hero .ss-hero-signature-quote { top: 24px !important; left: 18px !important; width: min(235px, 65vw) !important; max-width: 235px !important; font-size: 14px !important; line-height: 1.45 !important; }
  .ss-home .ss-hero .ss-hero-minimal-actions { top: 44% !important; left: 18px !important; }
  .ss-home .ss-hero .ss-hero-minimal-actions .ss-button { min-height: 45px !important; padding: 11px 14px !important; font-size: 12px !important; }
  .ss-home .ss-hero-followup-cards { width: calc(100% - 24px) !important; grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 10px !important; margin: 22px auto 48px !important; }
  .ss-home .ss-hero-followup-cards > .ss-capacity-wrap,
  .ss-home .ss-hero-followup-cards > .ss-ca-preview { min-height: 375px !important; padding: 15px 12px !important; border-radius: 20px !important; }
  .ss-home .ss-hero-followup-cards .ss-capacity-card { min-height: 340px !important; gap: 15px !important; }
  .ss-home .ss-hero-followup-cards .ss-capacity-intro > span:not(.ss-live-dot) { font-size: 8px !important; letter-spacing: .07em !important; }
  .ss-home .ss-hero-followup-cards .ss-capacity-intro small { font-size: 9px !important; }
  .ss-home .ss-hero-followup-cards .ss-capacity-item strong { font-size: 30px !important; }
  .ss-home .ss-hero-followup-cards .ss-capacity-item .ss-time { font-size: 14px !important; }
  .ss-home .ss-hero-followup-cards .ss-capacity-item span { font-size: 10px !important; line-height: 1.45 !important; }
  .ss-home .ss-hero-followup-cards .ss-capacity-link { font-size: 10px !important; gap: 3px !important; }
  .ss-home .ss-hero-followup-cards .ss-ca-preview-kicker { font-size: 8px !important; letter-spacing: .07em !important; }
  .ss-home .ss-hero-followup-cards .ss-ca-preview h2 { font-size: 19px !important; margin: 15px 0 10px !important; line-height: 1.32 !important; }
  .ss-home .ss-hero-followup-cards .ss-ca-preview p { font-size: 10px !important; line-height: 1.5 !important; }
  .ss-home .ss-hero-followup-cards .ss-ca-preview-tags { gap: 4px !important; }
  .ss-home .ss-hero-followup-cards .ss-ca-preview-tags span { font-size: 8px !important; padding: 4px 5px !important; }
  .ss-home .ss-hero-followup-cards .ss-ca-preview-cta { font-size: 10px !important; padding: 9px 9px !important; gap: 4px !important; }
}
@media (max-width: 380px) {
  .ss-home .ss-hero-followup-cards { grid-template-columns: 1fr !important; }
  .ss-home .ss-hero-followup-cards > .ss-capacity-wrap,
  .ss-home .ss-hero-followup-cards > .ss-ca-preview { min-height: 310px !important; }
  .ss-home .ss-hero-followup-cards .ss-capacity-card { min-height: 275px !important; }
}
@media (prefers-reduced-motion: reduce) {
  .ss-home .ss-hero-image { animation: none !important; }
}
'''

changed_css = False
if CSS_MARKER not in css:
    css = css.rstrip() + css_patch + '\n'
    changed_css = True

if not changed_jsx and not changed_css:
    print('Already applied: V3 hero quote + portrait cards. No files changed.')
    sys.exit(0)

stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
backup_dir = Path.home() / '.shri-shyam-library-backups' / f'hero-left-quote-cards-v3-{stamp}'
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(JSX, backup_dir / 'Home.jsx')
shutil.copy2(CSS, backup_dir / 'Home.css')
if changed_jsx:
    JSX.write_text(new_jsx, encoding='utf-8')
if changed_css:
    CSS.write_text(css, encoding='utf-8')

print('SUCCESS: Hero quote placement and portrait glass cards updated.')
print('Hero: small quote at upper-left; registration button retained; old hero copy removed.')
print('Cards: two vertical glass cards now sit BELOW the hero with positive spacing (no overlap).')
print('Library hours: 6:00 AM to 12:00 midnight.')
print('Changed:', ', '.join(name for name, changed in [('src/Home.jsx', changed_jsx), ('src/Home.css', changed_css)] if changed))
print('Untouched: header, facilities card markup/colors, gallery, video, registration flow and seat-selection logic.')
print(f'Backup: {backup_dir}')
print('NEXT: npm run build && git diff --check')
