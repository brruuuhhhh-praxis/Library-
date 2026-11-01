श्री श्याम लाइब्रेरी — Contact Us में Google Maps Location जोड़ने का Patch

इस patch से Home.jsx के Contact footer (id="contact-preview") में “लाइब्रेरी की लोकेशन देखें” लिंक जुड़ता है। क्लिक करने पर उपयोगकर्ता के दिए गए Google Maps URL को नया टैब में खोला जाएगा।

क्या बदलेगा:
- src/Home.jsx: Contact/footer में location link
- src/Home.css: उसी link की responsive gold-glass styling

बाकी Header, Hero, features, YouTube/video और registration/seat-selection logic को नहीं छूता।
पहले दोनों फाइलों का backup बनाया जाता है। Link पहले से मौजूद हुआ तो script कोई बदलाव नहीं करेगी।

चलाने के बाद:
  npm run build
  git diff --check

सही दिखने की पुष्टि के बाद केवल ये दो files stage करें:
  git add src/Home.jsx src/Home.css
