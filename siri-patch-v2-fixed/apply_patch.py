#!/usr/bin/env python3
"""Safely apply the Siri Library liquid-glass home/facilities/seat patch."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
PACKAGE = Path(__file__).resolve().parent / "src"
COPY_FILES = ["Home.jsx", "Home.css", "Booking.css", "CurrentAffairs.css", "libraryConfig.js"]
EXTRA_FILES = ["src/CurrentAffairs.jsx", "src/Registration.jsx", "src/Admin.jsx", "src/LibraryBrand.jsx"]

if not (ROOT / "src" / "Home.jsx").is_file() or not (ROOT / "package.json").is_file():
    print("ERROR: Run from ~/shri-shyam-library (project root). No files changed.")
    sys.exit(1)
missing = [name for name in COPY_FILES if not (PACKAGE / name).is_file()]
if missing:
    print("ERROR: Patch package incomplete: " + ", ".join(missing) + ". No files changed.")
    sys.exit(1)

# Read all proposed files first and validate the actual selectors before touching the project.
staged = {name: (PACKAGE / name).read_text(encoding="utf-8") for name in COPY_FILES}
if "ss-facility-icon-tile" not in staged["Home.jsx"] or "@keyframes ssLiquidDrift" not in staged["Home.css"]:
    print("ERROR: Patch is missing the liquid-glass facility layout. No files changed.")
    sys.exit(1)
if "import LibraryBrand from './LibraryBrand.jsx';" in staged["Home.jsx"]:
    print("ERROR: Home footer still depends on an external LibraryBrand component. No files changed.")
    sys.exit(1)
if "LIBRARY_BRAND_NAME = 'लाइब्रेरी'" not in staged["libraryConfig.js"]:
    print("ERROR: Patch has not removed 'श्याम' from the central library name. No files changed.")
    sys.exit(1)

# Replace old displayed name in the pages not shipped as full-file overlays.
text_changes = {}
for rel in EXTRA_FILES:
    path = ROOT / rel
    if path.is_file():
        content = path.read_text(encoding="utf-8")
        changed = content.replace("श्री श्याम लाइब्रेरी", "श्री लाइब्रेरी")
        if changed != content:
            text_changes[rel] = changed

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"siri-library-liquid-v2-fixed-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
backup_targets = [ROOT / "src" / n for n in COPY_FILES] + [ROOT / rel for rel in text_changes]
for path in backup_targets:
    shutil.copy2(path, backup / path.name)

for name, content in staged.items():
    (ROOT / "src" / name).write_text(content, encoding="utf-8")
for rel, content in text_changes.items():
    (ROOT / rel).write_text(content, encoding="utf-8")

print("SUCCESS: Fixed Siri Library liquid-glass patch applied.")
print("- Corrected validation: checks actual facility class and liquid animation keyframe.")
print("- Home footer uses included inline brand markup; no missing LibraryBrand import.")
print("- Library name is now 'श्री लाइब्रेरी' in central config; old wording updated in existing pages where found.")
print("- Ten colorful liquid-glass feature cards and 3D seat styling applied.")
print("- Registration/seat-selection logic is not replaced by this patch.")
print("Changed: " + ", ".join(["src/" + n for n in COPY_FILES] + list(text_changes)))
print("Backup: " + str(backup))
print("NEXT: npm run build && git diff --check")
print("Do not commit/push until reviewed locally.")
