श्री लाइब्रेरी — Hero + Portrait Glass Cards V3

इस patch को ~/shri-shyam-library में चलाएँ:

1. unzip -o ss_hero_left_quote_cards_v3.zip
2. python apply_ss_hero_left_quote_cards_v3.py
3. npm run build
4. git diff --check

क्या बदलेगा:
- Hero के ऊपरी-बाएँ कोने में छोटे अक्षरों में:
  “Success is when your signature becomes an autograph.”
- Hero में केवल “अपना रजिस्ट्रेशन करें” वाला बटन रहेगा।
- Hero की 3D background image साफ दिखाई देगी।
- Library Snapshot और Daily Current Affairs खड़े 3D glass cards होंगे।
- Cards Hero के ऊपर overlap नहीं करेंगे; दोनों नीचे positive gap के साथ आएँगे।
- लाइब्रेरी का समय सुबह 6:00 बजे से रात 12:00 बजे तक दिखेगा।
- Header, facilities cards, gallery, video, registration/seat-selection logic नहीं बदलेगा।

Script src/Home.jsx और src/Home.css का timestamped backup अपने-आप बनाएगी।
पहले local website पर देख लें; जब तक जाँच न हो, git push न करें।
