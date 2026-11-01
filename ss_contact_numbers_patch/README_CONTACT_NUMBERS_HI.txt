Shri Shyam Library — Contact numbers patch

This patch adds two clickable contact cards in the Contact footer:
- Call: 8306349753
- WhatsApp Business: 9664050399

Run from the project root (~/shri-shyam-library):
  python add_contact_numbers.py
  npm run build
  git diff --check

Only src/Home.jsx and src/Home.css are changed. The script creates a backup first.
Review the local website before committing/pushing. Do not use git add .
