#!/usr/bin/env python3
"""Apply reference-style moving liquid/fire backgrounds to 10 facility cards and the footer."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

root = Path.cwd()
home_jsx = root / "src" / "Home.jsx"
home_css = root / "src" / "Home.css"
patch_css = Path(__file__).resolve().parent / "src" / "liquid_aurora_reference.css"
if not home_jsx.is_file() or not home_css.is_file() or not patch_css.is_file():
    print("ERROR: Run from ~/shri-shyam-library and keep the extracted ZIP folder intact.")
    sys.exit(1)
jsx = home_jsx.read_text(encoding="utf-8")
css = home_css.read_text(encoding="utf-8")
patch = patch_css.read_text(encoding="utf-8")
marker = "/* REFERENCE-MATCH LIQUID WATER / FIRE / AURORA BACKGROUNDS"
if marker in css:
    print("ERROR: Reference liquid/aurora styling is already appended. No files changed.")
    sys.exit(1)
if "ss-facility-icon-tile" not in jsx or "ss-facility-icon-art" not in jsx:
    print("ERROR: Current Home.jsx does not contain the expected 10-feature icon tile markup. No files changed.")
    sys.exit(1)
if ".ss-footer" not in css:
    print("ERROR: Home.css has no .ss-footer selector. No files changed.")
    sys.exit(1)
stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"liquid-aurora-reference-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(home_css, backup / "Home.css")
home_css.write_text(css.rstrip() + "\n\n" + patch, encoding="utf-8")
print("SUCCESS: Reference-style moving liquid/fire backgrounds applied to the 10 feature cards.")
print("Footer now uses pale cream/ice-blue aurora waves with champagne-gold light trails.")
print("Changed only: src/Home.css. No React, registration, or seat logic was changed.")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Preview locally before commit/push.")
