SHRI SHYAM LIBRARY — DAILY CURRENT AFFAIRS PIPELINE PATCH

Daily target:
- National: 15
- Rajasthan: 10
- International: 5
- Total: 30

What the patch changes:
1. Expands RSS discovery sources for national, Rajasthan and international stories.
2. Changes the editorial target to 15/10/5.
3. Logs a clear shortfall for any category that does not have enough eligible, source-backed stories.
4. Preserves the existing Asia/Kolkata daily GitHub Actions schedule, Supabase publishing, duplicate checks, date checks, source links and quiz validation.
5. Leaves the website UI and Supabase schema unchanged.

IMPORTANT:
The quota is a target, not permission to invent news. If the feeds do not contain enough relevant, verifiable stories for the previous India calendar day, the pipeline deliberately publishes fewer and logs the shortfall.

APPLY IN TERMUX:
1. Extract this ZIP into the repository root.
2. Run:
   cd ~/shri-shyam-library
   python apply_daily_current_affairs_pipeline.py
   python -m py_compile automation/publish_current_affairs.py
   git diff --check
   git diff -- automation/publish_current_affairs.py
3. If the diff looks correct, commit and push:
   git add automation/publish_current_affairs.py
   git commit -m "Expand daily current affairs feeds and set 15-10-5 targets"
   git push origin main

Existing GitHub Actions secrets required by the current workflow:
- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY
- GEMINI_API_KEY

The existing workflow is scheduled for 8:00 AM Asia/Kolkata and also supports manual runs through Actions > Publish Daily Current Affairs > Run workflow.

SOURCE / FEED TERMS:
RSS feeds are used for discovery and source linking. Publisher terms may restrict redistribution; review each provider's terms before publicly republishing summaries on a commercial website. Keep summaries factual, brief and attributed with original source links.
