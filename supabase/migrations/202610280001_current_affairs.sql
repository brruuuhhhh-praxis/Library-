-- Shri Shyam Library: Current Affairs content + quiz payloads.
-- Run in Supabase Dashboard > SQL Editor after the existing library schema.sql.

create table if not exists public.current_affairs (
  id uuid primary key default gen_random_uuid(),
  edition_date date not null,
  event_date date not null,
  category text not null check (category in ('national','international','rajasthan')),
  headline text not null check (length(trim(headline)) between 5 and 220),
  one_liner text not null check (length(trim(one_liner)) between 10 and 700),
  source_name text not null check (length(trim(source_name)) between 2 and 100),
  source_url text not null check (source_url ~* '^https?://[^[:space:]]+$'),
  quiz_questions jsonb not null default '[]'::jsonb check (jsonb_typeof(quiz_questions) = 'array'),
  priority integer not null default 100 check (priority between 0 and 10000),
  status text not null default 'draft' check (status in ('draft','published')),
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint current_affairs_unique_story_per_edition unique (edition_date, category, headline, source_url)
);

create index if not exists current_affairs_published_edition_idx
  on public.current_affairs (edition_date desc, category, priority, created_at desc)
  where status = 'published';
create index if not exists current_affairs_event_date_idx
  on public.current_affairs (event_date desc);

create or replace function public.set_current_affairs_updated_at()
returns trigger language plpgsql set search_path = public
as $$
begin
  new.updated_at = now();
  if new.status = 'published' and old.status is distinct from 'published' then
    new.published_at = coalesce(new.published_at, now());
  end if;
  return new;
end; $$;

drop trigger if exists trg_current_affairs_updated_at on public.current_affairs;
create trigger trg_current_affairs_updated_at
before update on public.current_affairs
for each row execute function public.set_current_affairs_updated_at();

alter table public.current_affairs enable row level security;

drop policy if exists "Public can read published current affairs" on public.current_affairs;
create policy "Public can read published current affairs"
on public.current_affairs for select to anon, authenticated
using (status = 'published' or (auth.role() = 'authenticated' and public.is_library_admin()));

drop policy if exists "Library admins can insert current affairs" on public.current_affairs;
create policy "Library admins can insert current affairs"
on public.current_affairs for insert to authenticated
with check (public.is_library_admin());

drop policy if exists "Library admins can update current affairs" on public.current_affairs;
create policy "Library admins can update current affairs"
on public.current_affairs for update to authenticated
using (public.is_library_admin()) with check (public.is_library_admin());

drop policy if exists "Library admins can delete current affairs" on public.current_affairs;
create policy "Library admins can delete current affairs"
on public.current_affairs for delete to authenticated
using (public.is_library_admin());

grant select on public.current_affairs to anon, authenticated;
grant insert, update, delete on public.current_affairs to authenticated;

-- Example quiz_questions structure (add to each story when curated):
-- [{"question":"प्रश्न?","options":["विकल्प A","विकल्प B","विकल्प C","विकल्प D"],"answer_index":1,"explanation":"संक्षिप्त तथ्य और संदर्भ"}]
-- Each edition D should contain facts from the previous calendar day in Asia/Kolkata.
