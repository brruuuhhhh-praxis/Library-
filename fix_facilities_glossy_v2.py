#!/usr/bin/env python3
"""Fix Shri Shyam Library facility cards: premium glossy finish, no Contact edits."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

root = Path.cwd()
home_js = root / 'src/Home.jsx'
home_css = root / 'src/Home.css'
if not home_js.exists() or not home_css.exists():
    print('ERROR: Run from ~/shri-shyam-library; src/Home.jsx and src/Home.css are required.')
    sys.exit(1)

js = home_js.read_text(encoding='utf-8')
css = home_css.read_text(encoding='utf-8')
marker = 'SHRI SHYAM — FACILITIES GLOSS V2'
if marker in css:
    print('ERROR: V2 glossy patch is already present; no changes made.')
    sys.exit(1)

# Translate the facility-card subheadings to concise Hindi. These exact source phrases
# are verified before any file is written so the patch fails safely on code drift.
subs = {
    "subtitle: 'Focus without distractions'": "subtitle: 'ध्यान भटके बिना पढ़ाई'",
    "subtitle: 'Your own space to focus'": "subtitle: 'आपकी अपनी पढ़ने की जगह'",
    "subtitle: 'Stay connected when needed'": "subtitle: 'पढ़ाई के लिए भरोसेमंद कनेक्टिविटी'",
    "subtitle: 'Comfort through study hours'": "subtitle: 'पढ़ाई के समय आरामदायक माहौल'",
    "subtitle: 'A safer study environment'": "subtitle: 'सुरक्षा के लिए निगरानी व्यवस्था'",
    "subtitle: 'Keep your study uninterrupted'": "subtitle: 'बिजली जाने पर पढ़ाई जारी रखने में मदद'",
    "subtitle: 'A refreshment essential'": "subtitle: 'पीने के लिए साफ पानी'",
    "subtitle: 'Clean, comfortable premises'": "subtitle: 'साफ-सुथरा अध्ययन परिसर'",
    "subtitle: 'Organised study resources'": "subtitle: 'किताबों के लिए व्यवस्थित जगह'",
    "subtitle: 'Convenience while you study'": "subtitle: 'आने-जाने में सुविधा'",
}
for old, new in subs.items():
    if old not in js:
        print(f'ERROR: Expected subtitle not found: {old!r}')
        print('No files changed. Inspect src/Home.jsx first.')
        sys.exit(1)
    js = js.replace(old, new, 1)

css_patch = r'''

/* SHRI SHYAM — FACILITIES GLOSS V2
   Corrects the previous cascade conflict: restores distinct card tints and removes
   the flex auto-margin gap that pushed titles too far below the icons. */
.ss-facility-bento{align-items:stretch;gap:15px}
.ss-facility-card{
  min-height:0!important;
  height:100%;
  padding:18px 18px 17px!important;
  display:flex!important;
  flex-direction:column!important;
  justify-content:flex-start!important;
  gap:0!important;
  position:relative;
  isolation:isolate;
  overflow:hidden;
  border:1px solid var(--facility-edge,#e0d4b7)!important;
  border-radius:20px!important;
  background:linear-gradient(145deg,var(--facility-a,#fffdf7) 0%,var(--facility-b,#f1e5cd) 100%)!important;
  box-shadow:0 10px 24px #15283b0b,inset 0 1px 0 #ffffffd9!important;
  transition:transform .24s cubic-bezier(.2,.7,.2,1),box-shadow .24s,border-color .24s!important;
}
.ss-facility-card:before{
  content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;border-radius:inherit;
  background:linear-gradient(118deg,#ffffffbd 0%,#ffffff26 24%,transparent 48%,#ffffff35 76%,#ffffff8a 100%);
  opacity:.78;
}
.ss-facility-card:after{
  content:"";position:absolute;z-index:-1;right:-39px;bottom:-49px;width:130px;height:130px;border-radius:50%;
  border:1px solid var(--facility-glow,#c6a66b52);box-shadow:0 0 0 12px #ffffff16,0 0 0 25px #ffffff12;
  pointer-events:none;opacity:.8;transition:transform .35s ease,opacity .35s ease;
}
.ss-facility-card>*{position:relative;z-index:1}
.ss-facility-card:hover{transform:translateY(-4px)!important;border-color:var(--facility-edge,#c6a66b)!important;box-shadow:0 18px 34px #15283b15,inset 0 1px 0 #ffffffea!important}
.ss-facility-card:hover:after{transform:scale(1.13);opacity:1}
.ss-facility-card.tint-mint{--facility-a:#fbfff9;--facility-b:#e1eee0;--facility-edge:#b9d1b9;--facility-glow:#56805c45;color:#244b3a}
.ss-facility-card.tint-peach{--facility-a:#fffaf4;--facility-b:#f5e2d1;--facility-edge:#e4c3a8;--facility-glow:#b9845d48;color:#69462f}
.ss-facility-card.tint-blue{--facility-a:#fafdff;--facility-b:#dce9f5;--facility-edge:#b4cce1;--facility-glow:#5889b44a;color:#294f70}
.ss-facility-card.tint-lavender{--facility-a:#fffaff;--facility-b:#e8e0f4;--facility-edge:#cdc0e2;--facility-glow:#8d70b748;color:#594777}
.ss-facility-card.tint-rose{--facility-a:#fffafa;--facility-b:#f3dddd;--facility-edge:#e2bfc1;--facility-glow:#b46b7245;color:#783f49}
.ss-facility-card.tint-yellow{--facility-a:#fffdf4;--facility-b:#f5e8bd;--facility-edge:#e4d09b;--facility-glow:#bd984348;color:#72551d}
.ss-facility-card.tint-sky{--facility-a:#f8ffff;--facility-b:#dceef0;--facility-edge:#b5d8dc;--facility-glow:#4c929d45;color:#285e65}
.ss-facility-card.tint-sage{--facility-a:#fcfff6;--facility-b:#e5ead8;--facility-edge:#cbd5b6;--facility-glow:#7d955d45;color:#4c603a}
.ss-facility-card.tint-sand{--facility-a:#fffdf8;--facility-b:#eee1ca;--facility-edge:#dfcda9;--facility-glow:#a9844c45;color:#70502b}
.ss-facility-card.tint-steel{--facility-a:#fcfdff;--facility-b:#e0e6ee;--facility-edge:#c2ccda;--facility-glow:#697f9a45;color:#40566e}
.ss-facility-card-top{min-height:42px;align-items:center;gap:10px}
.ss-facility-card-top>span{font-size:9px!important;letter-spacing:2px!important;font-weight:900!important;color:currentColor;opacity:.62}
.ss-facility-card-top svg{width:42px!important;height:42px!important;flex:0 0 42px;padding:10px!important;border-radius:13px!important;
  color:#ad8439;background:linear-gradient(145deg,#fff8e7,#f1d99e)!important;border:1px solid #d8bd7b!important;
  box-shadow:0 5px 12px #8d68201a,inset 0 1px 0 #ffffffd9!important}
.ss-facility-card h3{
  margin:18px 0 5px!important;padding:0!important;min-height:0!important;align-self:stretch;
  font-family:'Noto Sans Devanagari',sans-serif!important;font-size:15px!important;font-weight:800!important;
  line-height:1.62!important;letter-spacing:-.15px;color:inherit!important;text-wrap:pretty;
}
.ss-facility-card p{
  margin:0!important;padding:0!important;max-width:30ch;font-family:'Noto Sans Devanagari',sans-serif!important;
  font-size:11px!important;line-height:1.75!important;color:inherit!important;opacity:.78;
}
.ss-facility-feature{border:1px solid #c6a66b55;box-shadow:0 18px 40px #102a4020,inset 0 1px 0 #ffffff12}
.ss-facility-feature:before{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(120deg,#ffffff0c,transparent 38%,#e5c77a0d 78%,#ffffff06)}
.ss-facility-feature h3{margin:20px 0 9px!important}
@media(min-width:761px){
  .ss-facility-card{min-height:170px!important}
  .ss-facility-card h3{font-size:15px!important}
}
@media(max-width:760px){
  .ss-facility-bento{grid-template-columns:repeat(2,minmax(0,1fr))!important;grid-template-rows:auto!important;grid-auto-rows:minmax(0,auto)!important;gap:11px!important}
  .ss-facility-feature{grid-column:1/-1;grid-row:auto;min-height:250px;padding:22px!important}
  .ss-facility-card{min-height:166px!important;padding:14px 13px 15px!important;border-radius:17px!important}
  .ss-facility-card-top{min-height:37px;gap:6px}
  .ss-facility-card-top>span{font-size:8px!important;letter-spacing:1.6px!important}
  .ss-facility-card-top svg{width:37px!important;height:37px!important;flex-basis:37px; padding:9px!important;border-radius:12px!important}
  .ss-facility-card h3{margin:17px 0 5px!important;font-size:13px!important;line-height:1.6!important;overflow-wrap:anywhere}
  .ss-facility-card p{font-size:10px!important;line-height:1.65!important}
}
@media(prefers-reduced-motion:reduce){.ss-facility-card,.ss-facility-card:after{transition:none!important}}
'''

stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
backup = Path.home() / '.shri-shyam-library-backups' / f'facilities-gloss-v2-{stamp}'
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(home_js, backup / 'Home.jsx')
shutil.copy2(home_css, backup / 'Home.css')
home_js.write_text(js, encoding='utf-8')
home_css.write_text(css + css_patch, encoding='utf-8')
print('SUCCESS: Facility cards now use a premium glossy navy/champagne-gold visual language.')
print('Fixed: white tint override, excessive title gap, compact mobile spacing, Hindi subtitles.')
print('Contact Us and all other page files were left untouched.')
print('Backup:', backup)
print('NEXT: npm run build && git diff --check')
