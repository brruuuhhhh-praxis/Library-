श्री श्याम लाइब्रेरी — Hero के नीचे 2 सेक्शन का 3D Glass Redesign

यह patch सिर्फ Home.css में snapshot/current-affairs panels का glassmorphism styling जोड़ता है और Home.jsx के समय-सारिणी label में समय दिखाता है:
“सुबह 6 से रात 12 बजे तक”

यह Hero, Header, YouTube video, सुविधाओं वाले cards, registration या seat-selection logic नहीं बदलता। Script exact classes Home.jsx से पहचानने की कोशिश करता है। अगर पहचान भरोसेमंद न हुई तो बिना कोई file बदले रुक जाएगा।

Termux में चलाएँ:
1) cd ~/shri-shyam-library
2) cp /sdcard/Download/ss_glass_sections_v1.zip .
3) unzip -o ss_glass_sections_v1.zip
4) python apply_ss_glass_sections.py
5) npm run build
6) git diff --check

पहले local website देखें; तुरंत GitHub पर push न करें।
