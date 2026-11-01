from pathlib import Path
from datetime import datetime
import shutil
import sys

root = Path.cwd()
src = root / 'src'
if not (root / 'package.json').exists() or not src.exists():
    sys.exit('ERROR: Run this script from the project root (the folder containing package.json and src/).')

# Pick the likely application entry point without touching page component files.
candidates = [
    src / 'main.jsx', src / 'main.tsx', src / 'main.js', src / 'main.ts',
    src / 'index.jsx', src / 'index.tsx', src / 'index.js', src / 'index.ts',
]
entry = next((p for p in candidates if p.exists()), None)
if entry is None:
    # Fallback: locate the first source file that mounts React.
    for p in sorted(src.rglob('*')):
        if p.suffix not in {'.jsx', '.tsx', '.js', '.ts'} or p.name.endswith('.backup'):
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        if 'createRoot(' in text or 'ReactDOM.render(' in text:
            entry = p
            break
if entry is None:
    sys.exit('ERROR: Could not find the app entry point (main.jsx/main.tsx or a React mount). No files changed.')

css_path = src / 'theme-cohesion.css'
css = r'''/* Shri Shyam Library — shared visual theme
   Palette: warm ivory · deep navy · muted gold · restrained sage
   This layer harmonizes colors across routes without changing page content. */
:root {
  --ss-theme-ivory: #F7F5EF;
  --ss-theme-ivory-deep: #EFE9DC;
  --ss-theme-navy: #17263A;
  --ss-theme-navy-2: #24384D;
  --ss-theme-gold: #C6A15A;
  --ss-theme-gold-light: #E8D39D;
  --ss-theme-sage: #6E887B;
  --ss-theme-ink: #263547;
  --ss-theme-muted: #687584;
  --ss-theme-border: rgba(198, 161, 90, 0.34);
  --ss-theme-shadow: 0 16px 42px rgba(23, 38, 58, 0.10);
  color-scheme: light;
}

html { scroll-behavior: smooth; }
body {
  background-color: var(--ss-theme-ivory);
  color: var(--ss-theme-ink);
  accent-color: var(--ss-theme-gold);
}
::selection { background: rgba(198, 161, 90, 0.28); color: var(--ss-theme-navy); }
:where(a, button, input, select, textarea, [role="button"]):focus-visible {
  outline: 3px solid rgba(198, 161, 90, 0.82);
  outline-offset: 3px;
}

/* Consistent borders/shadows across cards without forcing their text/background colors. */
:where(
  [class*="-card"], [class*="_card"], [class*="-panel"], [class*="_panel"],
  [class*="glass-card"], [class*="facility-card"], [class*="membership-card"],
  [class*="feature-card"], [class*="info-card"], [class*="service-card"]
) {
  border-color: var(--ss-theme-border);
  box-shadow: var(--ss-theme-shadow);
}

/* Match the library's dark-glass + gold identity in the existing contact area. */
:where(.ss-contact-panel, .ss-footer-address-en, .ss-footer-contact-card, .ss-capacity-card) {
  border-color: var(--ss-theme-border) !important;
  box-shadow: 0 18px 42px rgba(23, 38, 58, 0.16), 0 2px 8px rgba(198, 161, 90, 0.08);
}
:where(.ss-contact-panel, .ss-footer-address-en, .ss-footer-contact-card, .ss-capacity-card) {
  background-color: var(--ss-theme-navy) !important;
}

/* Primary actions share one navy-and-gold treatment; WhatsApp retains its green identity. */
:where(.ss-button-gold, .ss-contact-location-link, .ss-ca-preview-cta) {
  border-color: var(--ss-theme-gold) !important;
  background: linear-gradient(135deg, var(--ss-theme-navy), var(--ss-theme-navy-2)) !important;
  color: var(--ss-theme-gold-light) !important;
}
:where(.ss-button-gold, .ss-contact-location-link, .ss-ca-preview-cta) svg { color: currentColor; }
:where(.ss-footer-contact-card, .ss-footer-contact-card *) { color: inherit; }
:where(.ss-footer-contact-card a, .ss-footer-contact-card strong, .ss-footer-contact-card p, .ss-footer-contact-card small) {
  color: #F7F5EF;
}
:where(.ss-footer-contact-card .ss-footer-contact-arrow) { color: var(--ss-theme-gold-light); }

/* Keep links and controls polished on every route. */
:where(input, select, textarea) {
  border-color: rgba(23, 38, 58, 0.22);
}
:where(input, select, textarea):focus {
  border-color: var(--ss-theme-gold);
  box-shadow: 0 0 0 3px rgba(198, 161, 90, 0.15);
}
@media (prefers-reduced-motion: no-preference) {
  :where(a, button, [role="button"]) { transition: color 180ms ease, background-color 180ms ease, border-color 180ms ease, box-shadow 180ms ease; }
}
'''

# Save a timestamped backup if overwriting a previous run.
backup_dir = root / '.theme-cohesion-backups'
if css_path.exists():
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = backup_dir / f'theme-cohesion-{stamp}.css'
    shutil.copy2(css_path, backup)
css_path.write_text(css, encoding='utf-8')

entry_text = entry.read_text(encoding='utf-8')
import_line = "import './theme-cohesion.css';"
# If entry isn't at src root, path should still be relative to its parent.
relative_css = './' + css_path.relative_to(entry.parent).as_posix()
import_line = f"import '{relative_css}';"
if 'theme-cohesion.css' not in entry_text:
    # Put the CSS import first; Vite safely handles CSS imports before JS imports.
    entry.write_text(import_line + '\n' + entry_text, encoding='utf-8')

print('SUCCESS: Shared warm-ivory, deep-navy and muted-gold theme added.')
print(f'Entry point: {entry.relative_to(root)}')
print(f'Created: {css_path.relative_to(root)}')
print('Only the app entry point and the new theme CSS were changed.')
print('NEXT: npm run build && git diff --check')
