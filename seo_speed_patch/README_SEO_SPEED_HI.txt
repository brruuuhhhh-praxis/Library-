SHRI SHYAM LIBRARY — SEO + SPEED PATCH

क्या करता है:
1. Hindi page language, meaningful title/description, canonical URL, social metadata और LocalBusiness JSON-LD जोड़ता है।
2. Public sitemap बनाता है। Hash-based SPA routes अलग crawlable URLs नहीं होते, इसलिए sitemap में सिर्फ canonical home URL रखा गया है।
3. Registration/Admin/Current Affairs routes को lazy-load करता है ताकि initial bundle छोटा हो सके।
4. नीचे आने वाली study-room और gallery images पर lazy loading/async decoding लगाता है।
5. मौजूदा files का backup बनाता है। Contact/address/registration data को नहीं बदलता।

चलाने का तरीका:
cd ~/shri-shyam-library
unzip -o /sdcard/Download/seo_speed_patch.zip
python seo_speed_patch/apply_seo_speed.py
npm run build
git diff --check

Build पास होने के बाद ही जाँचें:
git diff --stat
git diff -- index.html src/App.jsx src/Home.jsx

फिर केवल संबंधित फाइलें stage करें:
git add index.html src/App.jsx src/Home.jsx public/sitemap.xml
git diff --cached --check
git diff --cached --stat

पिछले colour-theme बदलाव यदि पहले से staged हैं, तो stage किए गए बदलावों को ध्यान से जाँचें। जरूरत हो तो अलग-अलग commits करें। इस patch को चलाने पर GitHub पर अपने-आप push नहीं होगा।

महत्वपूर्ण SEO सीमा:
ऐप #/register, #/current-affairs जैसे hash routes इस्तेमाल करता है। Search engines आम तौर पर इन्हें अलग crawlable pages की तरह नहीं मानते। अलग-अलग पेजों की स्वतंत्र indexing के लिए बाद में path-based routes के साथ static prerender/SSR या अलग HTML pages चाहिए। Google Search Console में sitemap URL submit करना भी उपयोगी है।
