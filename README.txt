Shri Shyam Library — Admin security patch

Contents:
- 202611020002_admin_security_hardening.sql: secure database RPC functions and audit log.
- apply_admin_patch.py: adds Confirm / Reject / Membership Cancel buttons to src/Admin.jsx.

Apply:
1. Back up your repository (or commit current working changes).
2. In Supabase Dashboard > SQL Editor, paste and run the SQL migration file.
3. In Termux, cd to the Library repository root.
4. Put apply_admin_patch.py in the repository root and run:
   python apply_admin_patch.py
5. Run:
   npm run build
6. Inspect changes:
   git diff -- src/Admin.jsx
   git status
7. If build succeeds, commit and push.

Important:
- The SQL checks public.is_library_admin() on every action. A logged-in user who is not in library_admins cannot run these actions.
- Do not put Supabase service_role keys in frontend code or .env files committed to GitHub.
- Keep the existing admin_set_library_seat_status migration. This patch adds registration actions; it does not replace seat management.
- The audit log is readable only by allow-listed admins. Do not grant anon access.
