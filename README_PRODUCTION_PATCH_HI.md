# श्री जी लाइब्रेरी — production patch notes

## इस पैच में क्या बदला

- Registration पेज अब डेमो सीटों को वास्तविक उपलब्ध सीट की तरह नहीं दिखाता। Supabase सीट सूची लोड न हो तो बुकिंग रोक दी जाती है।
- Seat availability को जमा करने से ठीक पहले दोबारा जाँचा जाता है; database trigger और unique index अंतिम स्तर पर दोहरी बुकिंग रोकते हैं।
- Joining date और Current Affairs की default event date `Asia/Kolkata` के अनुसार तय होती हैं।
- Current Affairs में किसी खबर को edit करने पर उसके पुराने quiz questions अब सुरक्षित रहते हैं।
- Current Affairs फॉर्म की अधिकतम लंबाइयाँ database constraints से मेल खाती हैं।
- Admin seat status बदलने के लिए एक atomic RPC migration जोड़ी गई है, ताकि cancellation और seat release एक ही database transaction में हों।
- Admin/registration network errors पर loading state अटकी न रहे, इसके लिए error handling मजबूत की गई है।

## Supabase SQL लागू करना

तुम्हारे repository में पहले से मौजूद SQL क्रम यही रखें:

1. `supabase/schema.sql` — library seats, registrations और admin allow-list.
2. `supabase/migrations/202610280001_current_affairs.sql` — Current Affairs table और policies.
3. `supabase/migrations/202611020001_atomic_seat_admin.sql` — नया atomic seat-management RPC.

अगर पहले दो SQL पहले ही Supabase SQL Editor में सफलतापूर्वक चल चुके हैं, तो केवल तीसरा नया migration चलाना है। हर SQL को Supabase Dashboard → SQL Editor में चलाएँ।

## Environment variables

`.env.example` में केवल खाली placeholders हैं। Local testing के लिए इसे `.env.local` की प्रति बनाकर Supabase Project URL और browser-safe anon/publishable key भरें। GitHub Pages deploy में यही values GitHub Actions secrets के रूप में दें:

- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

**कभी भी `service_role` key को `VITE_*` variable, frontend source, GitHub Pages artifact या public repository में न रखें।**

## Build

Project folder में `npm ci` और फिर `npm run build` चलाएँ। इस पैच के source JSX/JS को syntax parser से जाँचा गया है; इस runtime में dependency installation timeout होने के कारण यहाँ पूरा Vite production build execute नहीं हो पाया।

## अभी भी जरूरी production checks

- Supabase में एक वास्तविक admin user को `library_admins` table में allow-list करना।
- Supabase RLS policies live project में लागू हैं, यह verify करना।
- Public registration spam रोकने के लिए CAPTCHA/rate limiting या server-side verification जोड़ना। Frontend-only validation spam protection नहीं है।
- Test registration, duplicate seat booking, admin cancel, manual seat block, Current Affairs draft/publish/unpublish और mobile print flow को live Supabase project पर verify करना।
