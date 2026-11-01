#!/usr/bin/env python3
"""Apply only a cinematic 3D-style background to Shri Shyam Library's hero section."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

root = Path.cwd()
css_path = root / 'src' / 'Home.css'
jsx_path = root / 'src' / 'Home.jsx'
source_image = Path(__file__).with_name('ss-hero-library-3d.webp')
asset_dir = root / 'src' / 'assets'
asset_path = asset_dir / 'ss-hero-library-3d.webp'
marker = 'SHRI SHYAM HERO BACKGROUND 3D V1'

if not css_path.is_file() or not jsx_path.is_file():
    print('ERROR: Run this script from the project root: ~/shri-shyam-library')
    print('Required files: src/Home.css and src/Home.jsx')
    sys.exit(1)
if not source_image.is_file():
    print('ERROR: ss-hero-library-3d.webp must be beside this script. Re-extract the ZIP.')
    sys.exit(1)

css = css_path.read_text(encoding='utf-8')
jsx = jsx_path.read_text(encoding='utf-8')
checks = [
    ('hero section in JSX', 'ss-hero' in jsx),
    ('hero image layer in JSX and CSS', 'ss-hero-image' in jsx and '.ss-hero-image' in css),
    ('hero shade layer in JSX and CSS', 'ss-hero-shade' in jsx and '.ss-hero-shade' in css),
]
failed = [name for name, ok in checks if not ok]
if failed:
    print('ERROR: Expected hero structure was not found; no files changed.')
    for name in failed:
        print(' - Missing:', name)
    print('Send this output so the patch can be matched to your current project.')
    sys.exit(1)
if marker in css:
    print('INFO: 3D hero background patch is already installed. No changes made.')
    sys.exit(0)

stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
backup_dir = Path.home() / '.shri-shyam-library-backups' / f'hero-3d-background-{stamp}'
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(css_path, backup_dir / 'Home.css')
if asset_path.exists():
    shutil.copy2(asset_path, backup_dir / 'ss-hero-library-3d.webp')

asset_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(source_image, asset_path)

patch = r'''

/* SHRI SHYAM HERO BACKGROUND 3D V1
   Visual-only: changes the hero background/image treatment only.
   Home.jsx, header, other sections, YouTube/video, registration and seat logic are untouched. */
.ss-hero{
  background:#07080a!important;
  isolation:isolate;
}
.ss-hero-image{
  inset:0!important;
  left:0!important;
  right:0!important;
  background-image:url('./assets/ss-hero-library-3d.webp')!important;
  background-size:cover!important;
  background-repeat:no-repeat!important;
  background-position:center 52%!important;
  transform:scale(1.04);
  filter:saturate(1.07) contrast(1.06) brightness(1.02);
  will-change:transform;
}
.ss-hero-shade{
  background:
    radial-gradient(ellipse at 80% 28%,rgba(235,164,66,.13) 0%,rgba(235,164,66,0) 41%),
    linear-gradient(90deg,rgba(5,6,9,.99) 0%,rgba(5,6,9,.96) 27%,rgba(5,6,9,.82) 48%,rgba(5,6,9,.42) 72%,rgba(5,6,9,.13) 100%),
    linear-gradient(0deg,rgba(5,6,9,.70) 0%,rgba(5,6,9,0) 40%)!important;
}
@keyframes ssHero3DDepthMotion{
  from{transform:scale(1.04) translate3d(0,0,0)}
  to{transform:scale(1.075) translate3d(-.35%,-.2%,0)}
}
@media(prefers-reduced-motion:no-preference){
  .ss-hero-image{animation:ssHero3DDepthMotion 28s ease-in-out infinite alternate}
}
@media(max-width:760px){
  .ss-hero-image{
    background-position:25% center!important;
    transform:scale(1.06);
    filter:saturate(1.05) contrast(1.05) brightness(.98);
  }
  .ss-hero-shade{
    background:
      radial-gradient(ellipse at 80% 22%,rgba(235,164,66,.09),rgba(235,164,66,0) 43%),
      linear-gradient(90deg,rgba(5,6,9,.90) 0%,rgba(5,6,9,.78) 58%,rgba(5,6,9,.55) 100%),
      linear-gradient(0deg,rgba(5,6,9,.82) 0%,rgba(5,6,9,.13) 68%,rgba(5,6,9,.18) 100%)!important;
  }
}
@media(prefers-reduced-motion:reduce){.ss-hero-image{animation:none!important;transform:scale(1.04)}}
'''

css_path.write_text(css + patch, encoding='utf-8')
print('SUCCESS: 3D hero background applied.')
print('Changed files: src/Home.css, src/assets/ss-hero-library-3d.webp')
print('Untouched: Home.jsx, header, all other sections, video, registration and seat-selection logic.')
print('Backup:', backup_dir)
print('NEXT: npm run build && git diff --check')
print('Review locally before committing/pushing; do not use git add .')
