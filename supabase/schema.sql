-- Shri Shyam Library registration + seat inventory
-- Run this entire file in Supabase Dashboard > SQL Editor > New query.
create extension if not exists pgcrypto;

create table if not exists public.library_seats (
  seat_no integer primary key check (seat_no between 1 and 50),
  status text not null default 'available' check (status in ('available','booked')),
  updated_at timestamptz not null default now()
);
insert into public.library_seats (seat_no, status)
select n, 'available' from generate_series(1,50) as n
on conflict (seat_no) do nothing;

create table if not exists public.library_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

create table if not exists public.library_registrations (
  id uuid primary key default gen_random_uuid(),
  full_name text not null check (length(trim(full_name)) between 2 and 100),
  father_name text not null check (length(trim(father_name)) between 2 and 100),
  date_of_birth date not null check (date_of_birth <= current_date),
  mobile text not null check (length(trim(mobile)) between 10 and 16),
  alternate_mobile text,
  address text not null check (length(trim(address)) between 8 and 500),
  emergency_contact text not null check (length(trim(emergency_contact)) between 10 and 16),
  id_type text not null check (id_type in ('Aadhaar Card','Voter ID','PAN Card','Driving Licence','Other Government ID')),
  joining_date date not null default current_date,
  seat_no integer not null references public.library_seats(seat_no),
  status text not null default 'pending' check (status in ('pending','active','cancelled')),
  created_at timestamptz not null default now()
);

-- A seat can have only one pending/active registration at any time.
create unique index if not exists library_registrations_one_live_booking_per_seat
  on public.library_registrations(seat_no) where status in ('pending','active');
create index if not exists library_registrations_created_at_idx on public.library_registrations(created_at desc);
create index if not exists library_registrations_mobile_idx on public.library_registrations(mobile);

create or replace function public.is_library_admin()
returns boolean language sql stable security definer set search_path = public
as $$ select exists (select 1 from public.library_admins where user_id = auth.uid()); $$;
revoke all on function public.is_library_admin() from public;
grant execute on function public.is_library_admin() to anon, authenticated;

create or replace function public.reserve_library_seat()
returns trigger language plpgsql security definer set search_path = public
as $$
declare changed_rows integer;
begin
  update public.library_seats set status='booked', updated_at=now()
  where seat_no=NEW.seat_no and status='available';
  get diagnostics changed_rows = row_count;
  if changed_rows <> 1 then
    raise exception 'Selected seat is no longer available';
  end if;
  return NEW;
end; $$;

drop trigger if exists trg_reserve_library_seat on public.library_registrations;
create trigger trg_reserve_library_seat after insert on public.library_registrations
for each row when (NEW.status in ('pending','active')) execute function public.reserve_library_seat();

create or replace function public.sync_library_seat_after_registration_update()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if NEW.status in ('pending','active') then
    update public.library_seats set status='booked', updated_at=now() where seat_no=NEW.seat_no;
  elsif OLD.status in ('pending','active') and NEW.status not in ('pending','active') then
    if not exists (select 1 from public.library_registrations r where r.seat_no=NEW.seat_no and r.status in ('pending','active')) then
      update public.library_seats set status='available', updated_at=now() where seat_no=NEW.seat_no;
    end if;
  end if;
  return NEW;
end; $$;
drop trigger if exists trg_sync_library_seat_after_registration_update on public.library_registrations;
create trigger trg_sync_library_seat_after_registration_update after update of status on public.library_registrations
for each row execute function public.sync_library_seat_after_registration_update();

alter table public.library_seats enable row level security;
alter table public.library_registrations enable row level security;
alter table public.library_admins enable row level security;

drop policy if exists "Public can view seat availability" on public.library_seats;
create policy "Public can view seat availability" on public.library_seats for select to anon, authenticated using (true);
drop policy if exists "Library admins can update seats" on public.library_seats;
create policy "Library admins can update seats" on public.library_seats for update to authenticated using (public.is_library_admin()) with check (public.is_library_admin());
drop policy if exists "Library admins can insert seats" on public.library_seats;
create policy "Library admins can insert seats" on public.library_seats for insert to authenticated with check (public.is_library_admin());

drop policy if exists "Visitors can submit registration requests" on public.library_registrations;
create policy "Visitors can submit registration requests" on public.library_registrations for insert to anon, authenticated
with check (status='pending' and length(trim(full_name)) between 2 and 100 and length(trim(mobile)) between 10 and 16);
drop policy if exists "Library admins can read registrations" on public.library_registrations;
create policy "Library admins can read registrations" on public.library_registrations for select to authenticated using (public.is_library_admin());
drop policy if exists "Library admins can update registrations" on public.library_registrations;
create policy "Library admins can update registrations" on public.library_registrations for update to authenticated using (public.is_library_admin()) with check (public.is_library_admin());
drop policy if exists "Library admins can delete registrations" on public.library_registrations;
create policy "Library admins can delete registrations" on public.library_registrations for delete to authenticated using (public.is_library_admin());

-- No public access is granted to the admin allow-list.
drop policy if exists "Admins can view their own allow-list row" on public.library_admins;
create policy "Admins can view their own allow-list row" on public.library_admins for select to authenticated using (user_id=auth.uid());

grant select on public.library_seats to anon, authenticated;
grant insert on public.library_registrations to anon, authenticated;
grant select, update, delete on public.library_registrations to authenticated;
grant select, update, insert on public.library_seats to authenticated;
grant select on public.library_admins to authenticated;
