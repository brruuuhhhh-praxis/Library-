#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re, shutil, sys

root = Path.cwd()
home = root / 'src' / 'Home.jsx'
css = root / 'src' / 'Home.css'
asset = root / 'src' / 'assets' / 'ss-hero-library-3d.webp'
if not home.exists() or not css.exists():
    print('ERROR: Run this script from ~/shri-shyam-library (src/Home.jsx and src/Home.css required).')
    sys.exit(1)
jsx = home.read_text(encoding='utf-8')
styles = css.read_text(encoding='utf-8')
checks = ['<section className="ss-hero">', 'className="ss-capacity-wrap"', 'className="ss-ca-preview"', 'className="ss-hero-content"', 'अपनी सीट बुक करें']
missing = [x for x in checks if x not in jsx]
if missing:
    print('ERROR: Home.jsx does not match expected structure; no files changed.')
    print('Missing:', missing)
    sys.exit(2)
if 'SS HERO PORTRAIT GLASS V2' in styles or 'SS HERO PORTRAIT GLASS V2' in jsx:
    print('Already applied: SS HERO PORTRAIT GLASS V2')
    sys.exit(0)
backup_dir = Path.home() / '.shri-shyam-library-backups' / ('hero-portrait-glass-v2-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(home, backup_dir / 'Home.jsx')
shutil.copy2(css, backup_dir / 'Home.css')
if asset.exists():
    shutil.copy2(asset, backup_dir / asset.name)

# Replace only the hero copy: quote + registration CTA, retaining the existing hero background.
start = jsx.index('        <div className="ss-hero-content">')
end_marker = '      </section>\n\n      {/* 3. CAPACITY STRIP'
end = jsx.index(end_marker, start)
hero = '''        <div className="ss-hero-content ss-hero-minimal-content">
          <p className="ss-hero-signature-quote">Success is when your signature becomes an autograph.</p>
          <div className="ss-hero-actions ss-hero-minimal-actions">
            <a className="ss-button ss-button-gold" href="#/register">अपना रजिस्ट्रेशन करें <ArrowRight size={17} /></a>
          </div>
        </div>
'''
jsx = jsx[:start] + hero + jsx[end:]
# Remove the old decorative quote and bottomline if present.
jsx = re.sub(r'\n        <div className="ss-hero-note">.*?</div>\n        <div className="ss-hero-bottomline">.*?</div>', '', jsx, count=1, flags=re.S)
# Group the two existing sections so they can render as portrait cards side by side.
jsx = jsx.replace('      {/* 3. CAPACITY STRIP — separate overlapping horizontal dashboard */}\n      <section className="ss-capacity-wrap"',
                  '      {/* SS HERO PORTRAIT GLASS V2: paired vertical glass cards */}\n      <div className="ss-hero-followup-cards">\n      {/* 3. LIBRARY SNAPSHOT */}\n      <section className="ss-capacity-wrap"', 1)
jsx = jsx.replace('      {/* 4. FACILITIES — colourful bento grid, different from other sections */}',
                  '      </div>\n\n      {/* 4. FACILITIES — colourful bento grid, different from other sections */}', 1)
jsx = jsx.replace('लाइब्रेरी के समय के लिए संपर्क करें', 'सुबह 6:00 बजे – रात 12:00 बजे')
home.write_text(jsx, encoding='utf-8')

css_patch = r'''

/* SS HERO PORTRAIT GLASS V2 — only hero + the two cards below it */
.ss-hero {
  min-height: clamp(650px, 82svh, 940px) !important;
  height: auto !important;
  position: relative;
  display: flex;
  align-items: center;
  overflow: hidden;
}
.ss-hero-image,
.ss-hero-shade { position: absolute; inset: 0; }
.ss-hero-image { background-size: cover !important; background-position: center right !important; transform: scale(1.015); }
.ss-hero-shade {
  background: linear-gradient(90deg, rgba(3,8,15,.94) 0%, rgba(3,8,15,.78) 40%, rgba(3,8,15,.20) 100%),
              linear-gradient(0deg, rgba(3,8,15,.42), transparent 38%) !important;
  pointer-events: none;
}
.ss-hero-minimal-content {
  position: relative !important;
  z-index: 2;
  width: min(100%, 1000px) !important;
  max-width: 1000px !important;
  padding: clamp(34px, 6vw, 76px) clamp(24px, 5vw, 70px) !important;
  margin: 0 !important;
}
.ss-hero-signature-quote {
  max-width: 780px;
  margin: 0 0 30px !important;
  color: #fff8e9 !important;
  font-family: Georgia, 'Times New Roman', serif !important;
  font-size: clamp(32px, 5.2vw, 66px) !important;
  font-weight: 700 !important;
  line-height: 1.16 !important;
  letter-spacing: -.035em !important;
  text-wrap: balance;
  text-shadow: 0 4px 30px rgba(0,0,0,.72), 0 0 30px rgba(246,183,65,.15);
}
.ss-hero-minimal-actions { margin-top: 0 !important; }
.ss-hero-minimal-actions .ss-button { min-height: 54px; padding: 15px 24px !important; font-size: 15px !important; }
.ss-hero-followup-cards {
  position: relative;
  z-index: 3;
  width: min(1120px, calc(100% - 36px));
  margin: -24px auto 70px;
  display: grid;
  grid-template-columns: minmax(0, .92fr) minmax(0, 1.08fr);
  gap: 22px;
  align-items: stretch;
}
.ss-hero-followup-cards .ss-capacity-wrap,
.ss-hero-followup-cards .ss-ca-preview {
  width: 100% !important;
  min-width: 0;
  min-height: 330px;
  height: 100%;
  margin: 0 !important;
  padding: 24px !important;
  border: 1px solid rgba(255, 211, 125, .48) !important;
  border-radius: 28px !important;
  background: linear-gradient(145deg, rgba(13,22,34,.96), rgba(4,10,19,.88)) !important;
  box-shadow: 0 22px 55px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.12), 0 0 24px rgba(244,181,63,.08) !important;
  backdrop-filter: blur(22px) saturate(130%);
  -webkit-backdrop-filter: blur(22px) saturate(130%);
  overflow: hidden;
  position: relative;
}
.ss-hero-followup-cards .ss-capacity-wrap::before,
.ss-hero-followup-cards .ss-ca-preview::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(circle at 85% 8%, rgba(255,194,74,.22), transparent 38%), linear-gradient(135deg, rgba(255,255,255,.08), transparent 42%);
  pointer-events: none;
}
.ss-hero-followup-cards .ss-capacity-card {
  position: relative;
  z-index: 1;
  width: 100%; height: 100%; min-height: 280px;
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  justify-content: space-between !important;
  gap: 22px !important;
  padding: 4px !important;
  border: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}
.ss-hero-followup-cards .ss-capacity-intro,
.ss-hero-followup-cards .ss-capacity-item,
.ss-hero-followup-cards .ss-capacity-link { position: relative; z-index: 1; }
.ss-hero-followup-cards .ss-capacity-intro { display: grid !important; grid-template-columns: auto 1fr; align-items: center; column-gap: 9px; row-gap: 7px; }
.ss-hero-followup-cards .ss-capacity-intro small { grid-column: 2; }
.ss-hero-followup-cards .ss-capacity-item { display: flex !important; flex-direction: column !important; align-items: flex-start !important; gap: 7px !important; border: 0 !important; }
.ss-hero-followup-cards .ss-capacity-item strong { color: #ffe0a0 !important; font-size: clamp(30px, 4vw, 44px) !important; line-height: 1 !important; }
.ss-hero-followup-cards .ss-capacity-item .ss-time { font-family: inherit; font-size: 20px !important; }
.ss-hero-followup-cards .ss-capacity-divider { display: none !important; }
.ss-hero-followup-cards .ss-capacity-link { margin-top: auto; display: inline-flex; align-items: center; gap: 8px; color: #ffce68 !important; }
.ss-hero-followup-cards .ss-ca-preview { display: flex !important; flex-direction: column !important; justify-content: space-between !important; align-items: stretch !important; gap: 22px !important; }
.ss-hero-followup-cards .ss-ca-preview-copy { position: relative; z-index: 1; max-width: none !important; }
.ss-hero-followup-cards .ss-ca-preview h2 { margin: 18px 0 14px !important; color: #fff7e7 !important; font-size: clamp(25px, 3vw, 36px) !important; line-height: 1.28 !important; }
.ss-hero-followup-cards .ss-ca-preview h2 em { color: #ffd16d !important; }
.ss-hero-followup-cards .ss-ca-preview p { color: rgba(255,248,233,.78) !important; }
.ss-hero-followup-cards .ss-ca-preview-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.ss-hero-followup-cards .ss-ca-preview-cta { position: relative; z-index: 1; align-self: flex-start; margin-top: auto; }
@media (max-width: 680px) {
  .ss-hero { min-height: max(600px, 78svh) !important; }
  .ss-hero-image { background-position: 62% center !important; }
  .ss-hero-shade { background: linear-gradient(90deg, rgba(3,8,15,.90), rgba(3,8,15,.42)), linear-gradient(0deg, rgba(3,8,15,.4), transparent 55%) !important; }
  .ss-hero-minimal-content { padding: 34px 22px !important; }
  .ss-hero-signature-quote { font-size: clamp(31px, 8.2vw, 46px) !important; line-height: 1.2 !important; }
  .ss-hero-followup-cards { width: calc(100% - 24px); grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin: -16px auto 52px; }
  .ss-hero-followup-cards .ss-capacity-wrap,
  .ss-hero-followup-cards .ss-ca-preview { min-height: 310px; padding: 16px 13px !important; border-radius: 22px !important; }
  .ss-hero-followup-cards .ss-capacity-card { min-height: 276px; gap: 17px !important; }
  .ss-hero-followup-cards .ss-capacity-intro > span:not(.ss-live-dot) { font-size: 9px !important; letter-spacing: .08em; }
  .ss-hero-followup-cards .ss-capacity-intro small { font-size: 10px !important; }
  .ss-hero-followup-cards .ss-capacity-item strong { font-size: 34px !important; }
  .ss-hero-followup-cards .ss-capacity-item .ss-time { font-size: 16px !important; }
  .ss-hero-followup-cards .ss-capacity-item span { font-size: 11px !important; line-height: 1.45; }
  .ss-hero-followup-cards .ss-capacity-link { font-size: 11px !important; gap: 4px; }
  .ss-hero-followup-cards .ss-ca-preview-kicker { font-size: 8px !important; line-height: 1.5; }
  .ss-hero-followup-cards .ss-ca-preview h2 { font-size: clamp(20px, 5.3vw, 27px) !important; margin: 14px 0 10px !important; }
  .ss-hero-followup-cards .ss-ca-preview p { font-size: 11px !important; line-height: 1.55; }
  .ss-hero-followup-cards .ss-ca-preview-tags span { font-size: 9px !important; padding: 5px 7px !important; }
  .ss-hero-followup-cards .ss-ca-preview-cta { font-size: 11px !important; padding: 10px 11px !important; }
}
@media (max-width: 380px) {
  .ss-hero-followup-cards { grid-template-columns: 1fr; }
  .ss-hero-followup-cards .ss-capacity-wrap,
  .ss-hero-followup-cards .ss-ca-preview { min-height: 270px; }
}
'''
css.write_text(styles + css_patch, encoding='utf-8')
print('SUCCESS: Hero simplified and enlarged; both sections converted to portrait 3D glass cards.')
print('Changed: src/Home.jsx, src/Home.css')
print('Preserved: facilities cards, header/nav, gallery, video/registration/seat logic outside hero CTA.')
print('Backup:', backup_dir)
print('NEXT: npm run build && git diff --check; inspect locally before committing.')
