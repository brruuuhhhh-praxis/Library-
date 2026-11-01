#!/usr/bin/env python3
"""Safely apply the Siri Library liquid-glass Home/seat patch in Termux."""
from pathlib import Path
from datetime import datetime
import shutil, sys

ROOT = Path.cwd()
PACKAGE = Path(__file__).resolve().parent / "src"
COPY_FILES = ["Home.jsx", "Home.css", "Booking.css", "CurrentAffairs.css", "libraryConfig.js"]
EXTRA_FILES = ["src/CurrentAffairs.jsx", "src/Registration.jsx", "src/Admin.jsx", "src/LibraryBrand.jsx"]
if not (ROOT / "src" / "Home.jsx").is_file() or not (ROOT / "package.json").is_file():
    print("ERROR: Run from ~/shri-shyam-library (project root). No files changed.")
    sys.exit(1)
missing = [name for name in COPY_FILES if not (PACKAGE / name).is_file()]
if missing:
    print("ERROR: Patch package incomplete: " + ", ".join(missing))
    sys.exit(1)

# Stage the files in memory and validate expected branded header before writing.
staged = {name: (PACKAGE / name).read_text(encoding="utf-8") for name in COPY_FILES}
if 'className="ss-facility-icon-tile' not in staged["Home.jsx"] or "ssLiquidDrift" not in staged["Home.css"]:
    print("ERROR: Patch is missing the liquid-glass facility layout. No files changed.")
    sys.exit(1)
if 'श्याम लाइब्रेरी</strong>' in staged["Home.jsx"] or "LIBRARY_BRAND_NAME = 'श्याम लाइब्रेरी'" in staged["libraryConfig.js"]:
    print("ERROR: Patch still contains old 'Shyam Library' branding. No files changed.")
    sys.exit(1)

# Carefully replace only the library name in existing JSX components not included in the overlay.
text_changes = {}
for rel in EXTRA_FILES:
    path = ROOT / rel
    if path.is_file():
        content = path.read_text(encoding="utf-8")
        changed = content.replace("श्री श्याम लाइब्रेरी", "श्री लाइब्रेरी")
        if changed != content:
            text_changes[rel] = changed

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"siri-library-liquid-v2-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
backup_targets = [ROOT / "src" / n for n in COPY_FILES] + [ROOT / rel for rel in text_changes]
for path in backup_targets:
    shutil.copy2(path, backup / path.name)

for name, content in staged.items():
    (ROOT / "src" / name).write_text(content, encoding="utf-8")
for rel, content in text_changes.items():
    (ROOT / rel).write_text(content, encoding="utf-8")

print("SUCCESS: Corrected Siri Library patch applied.")
print("- Header branding: 'श्री लाइब्रेरी' (removed 'श्याम'), with large 3D gold श्री + AI sparkle.")
print("- All 10 facility cards retain individual liquid-glass/water-motion gradients.")
print("- 3D seat-button styling retained; selection and registration logic untouched.")
print("- Updated old static brand wording in Current Affairs, Registration, Admin, and LibraryBrand files when present.")
print("Changed files: " + ", ".join(["src/" + n for n in COPY_FILES] + list(text_changes)))
print("Backup: " + str(backup))
print("NEXT: npm run build && git diff --check")
print("Do not commit/push until reviewed locally.")
