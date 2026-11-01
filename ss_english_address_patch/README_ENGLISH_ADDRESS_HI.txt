SHRI SHYAM LIBRARY — ENGLISH ADDRESS PATCH

This patch adds an English address card to the Contact footer and keeps the existing Hindi address/content.

Address displayed:
Ward No. 3, Gurudwara Road, Bishnoi Mohalla, Suratgarh, Rajasthan – 335804
Landmark: 100 metres from Paras Hyundai

INSTALL IN TERMUX
1. Copy/extract add_english_address.py into your Termux project folder.
2. Run:
   cd ~/shri-shyam-library
   python /path/to/add_english_address.py

   Replace /path/to/add_english_address.py with the actual path where you saved the script.
   If the script is already in the project folder, run:
   python add_english_address.py

3. Validate:
   npm run build
   git diff --check

4. Review just the changed files:
   git diff -- src/Home.jsx src/Home.css

5. If the result looks correct, stage only these files and push:
   git add src/Home.jsx src/Home.css
   git diff --cached --stat
   git commit -m "Add English library address"
   git push origin main

A timestamped backup of Home.jsx and Home.css is created automatically before changes.
