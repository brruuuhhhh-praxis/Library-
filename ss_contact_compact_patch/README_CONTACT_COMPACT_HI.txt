SHRI SHYAM LIBRARY — CONTACT SECTION COMPACT PATCH

What it does:
- Groups the Google Maps location link, English address, Call and WhatsApp cards under one Contact & Location panel.
- Tightens excessive spacing, aligns cards and applies consistent mobile-first styling.
- Keeps the existing address, map URL, phone number and WhatsApp number unchanged.
- Creates a backup before editing.

Apply from the project root (~/shri-shyam-library):
  python ss_contact_compact_patch/apply_ss_contact_compact.py
  npm run build
  git diff --check

If the build is successful, inspect the changes before committing:
  git diff --stat
  git diff -- src/Home.jsx
  git add src/Home.jsx src/Home.css
  git diff --cached --check
  git diff --cached --stat
  git commit -m "Improve contact section layout"
  git push origin main

Do not use `git add .`; there may be unrelated local patch and backup files.
