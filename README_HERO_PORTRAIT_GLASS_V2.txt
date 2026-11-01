SHRI SHYAM LIBRARY — HERO + PORTRAIT GLASS CARDS V2

Run from the project root (~/shri-shyam-library):
  python apply_ss_hero_portrait_glass_v2.py
  npm run build
  git diff --check

This patch changes only src/Home.jsx and src/Home.css. It keeps the existing hero background asset,
leaves the header and facilities grid intact, simplifies hero copy to the requested quote + registration
button, and turns Library Snapshot and Current Affairs into tall glassmorphism cards. Opening hours are
shown as 6:00 AM–12:00 AM. A timestamped backup is created before any change.
Do not git add .; inspect the local page before committing.
