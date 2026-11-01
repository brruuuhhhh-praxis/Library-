SHRI SHYAM LIBRARY — OVERALL COLOR THEME PATCH

Palette:
- Warm ivory background
- Deep navy for core/primary surfaces
- Muted gold for borders, focus, and premium accents
- Restrained sage as a secondary accent

What it does:
- Adds src/theme-cohesion.css
- Imports it from the React/Vite app entry point
- Harmonizes shared cards, contact cards, location/primary buttons, forms, focus states, and shadows
- Does not change page copy, address, phone number, or WhatsApp number

Apply from the project root (the folder containing package.json):
  unzip -o /sdcard/Download/theme_cohesion_patch.zip
  python theme_cohesion_patch/apply_theme_cohesion.py
  npm run build
  git diff --check

If the build succeeds, inspect the changes before committing:
  git status --short
  git diff --stat
  git diff -- src/main.jsx

NOTE:
- The script locates the React entry point automatically.
- It is safe to rerun; it will not add the import twice.
- The patch has not been applied to the live site automatically.
