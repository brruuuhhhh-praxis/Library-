# Shri Shyam Library: Registration Upgrade

## Added to the current Vite website
- Premium midnight-navy, deep-teal, champagne-gold and ivory theme.
- GitHub Pages-safe hash routes: `#/register` and `#/admin`.
- Registration form with personal details, selected seat (1–50), explicit offline ID-copy note, and A4 print stylesheet.
- Shared seat availability/booking backed by Supabase (not browser local storage).
- Admin email/password login, seat status controls, private registration records and print action.
- Supabase schema with RLS; public clients can see seat status and submit a request but cannot read personal registration records.

## Required one-time setup
1. Create a Supabase project.
2. In Supabase Dashboard -> SQL Editor, run the complete `supabase/schema.sql`.
3. In Supabase Dashboard -> Project Settings -> API, copy the Project URL and the publishable/anon key. Do not use a service-role/secret key in the website.
4. In GitHub repository Settings -> Secrets and variables -> Actions, add repository secrets named exactly `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`. Their values are the URL and publishable/anon key above.
5. In Supabase Dashboard -> Authentication -> Users, create the library administrator user with an email and strong password. Copy that user's UUID.
6. In Supabase SQL Editor, run this one-line query after replacing the UUID:

   `insert into public.library_admins (user_id) values ('PASTE-ADMIN-USER-UUID-HERE');`

7. Push code to `main` to trigger GitHub Actions. Once deployed, the public form is the homepage URL followed by `#/register`, and the admin panel is the homepage URL followed by `#/admin`.

For local development only, copy `.env.example` to `.env` and fill in the same Project URL and publishable/anon key. The real `.env` is gitignored. Never store Supabase service-role keys in frontend code, environment variables exposed to Vite, GitHub Pages, or a public repository.

## Behavior and privacy
- ID document is not uploaded or stored by this application. User submits a physical photocopy at the library.
- Full Aadhaar number is not collected by the form.
- Public users can read seat statuses, but RLS prevents them from reading registration names, addresses, or phone numbers.
- Public form submissions create `pending` applications and reserve the chosen seat. The unique index blocks two active/pending records for the same seat.
- Admin must set up a trusted user in Supabase Auth and explicitly add its UUID to `library_admins`.
- Before using this for real applicants, test a sample booking and cancellation with non-sensitive test data.
