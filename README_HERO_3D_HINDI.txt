SHRI SHYAM LIBRARY — HERO 3D BACKGROUND PATCH

यह patch केवल homepage के Hero section का background बदलता है।
Header, दूसरी sections/cards, YouTube/video, registration और seat-selection logic को नहीं बदलता।

Termux में चलाएँ:
1) ZIP को Download folder में रखें और project root खोलें:
   cd ~/shri-shyam-library
2) ZIP extract करें (ZIP का नाम जैसा डाउनलोड हुआ हो, वही लिखें):
   cp /sdcard/Download/ss_hero_3d_background_v1.zip .
   unzip -o ss_hero_3d_background_v1.zip
3) Patch चलाएँ:
   python apply_ss_hero_3d_background.py
4) Build जाँचें:
   npm run build
   git diff --check
5) लोकल साइट देखने के लिए:
   npm run dev -- --host 0.0.0.0
   फिर terminal में दिखा localhost URL Chrome में खोलें।

जब तक लोकल preview ठीक न दिखे, GitHub पर push न करें।
अगर commit करना हो तो केवल intended files stage करें; `git add .` न चलाएँ।
