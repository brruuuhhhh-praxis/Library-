-- Shri Shyam Library: admin-only registration actions + audit log
-- Apply in Supabase Dashboard > SQL Editor after the existing schema/migrations.
-- Safe to re-run.

create table if not exists public.library_admin_audit_log (
  id bigint generated always as identity primary key,
  actor_user_id uuid not null default auth.uid() references auth.users(id),
  action text not null check (action in (
    'registration_confirmed', 'registration_rejected',
    'membership_cancelled', 'seat_status_changed'
  )),
  registration_id uuid,
  seat_no integer,
  old_status text,
  new_status text,
  created_at timestamptz not null default now()
);

alter table public.library_admin_audit_log enable row level security;
revoke all on public.library_admin_audit_log from public, anon, authenticated;
grant select on public.library_admin_audit_log to authenticated;

drop policy if exists "Library admins can read audit log" on public.library_admin_audit_log;
create policy "Library admins can read audit log"
  on public.library_admin_audit_log for select to authenticated
  using (public.is_library_admin());

create or replace function public.admin_confirm_library_registration(p_registration_id uuid)
returns void language plpgsql security definer set search_path = public
as $$
declare r public.library_registrations%rowtype;
begin
  if auth.uid() is null or not public.is_library_admin() then
    raise exception 'Library admin access required';
  end if;

  select * into r from public.library_registrations
   where id = p_registration_id for update;
  if not found then raise exception 'Registration not found'; end if;
  if r.status <> 'pending' then
    raise exception 'Only pending registrations can be confirmed';
  end if;

  update public.library_registrations set status = 'active'
   where id = p_registration_id and status = 'pending';

  insert into public.library_admin_audit_log
    (action, registration_id, seat_no, old_status, new_status)
  values ('registration_confirmed', r.id, r.seat_no, r.status, 'active');
end;
$$;

create or replace function public.admin_reject_library_registration(p_registration_id uuid)
returns void language plpgsql security definer set search_path = public
as $$
declare r public.library_registrations%rowtype;
begin
  if auth.uid() is null or not public.is_library_admin() then
    raise exception 'Library admin access required';
  end if;

  select * into r from public.library_registrations
   where id = p_registration_id for update;
  if not found then raise exception 'Registration not found'; end if;
  if r.status <> 'pending' then
    raise exception 'Only pending registrations can be rejected';
  end if;

  update public.library_registrations set status = 'cancelled'
   where id = p_registration_id and status = 'pending';

  insert into public.library_admin_audit_log
    (action, registration_id, seat_no, old_status, new_status)
  values ('registration_rejected', r.id, r.seat_no, r.status, 'cancelled');
end;
$$;

create or replace function public.admin_cancel_library_membership(p_registration_id uuid)
returns void language plpgsql security definer set search_path = public
as $$
declare r public.library_registrations%rowtype;
begin
  if auth.uid() is null or not public.is_library_admin() then
    raise exception 'Library admin access required';
  end if;

  select * into r from public.library_registrations
   where id = p_registration_id for update;
  if not found then raise exception 'Registration not found'; end if;
  if r.status <> 'active' then
    raise exception 'Only active memberships can be cancelled';
  end if;

  update public.library_registrations set status = 'cancelled'
   where id = p_registration_id and status = 'active';

  insert into public.library_admin_audit_log
    (action, registration_id, seat_no, old_status, new_status)
  values ('membership_cancelled', r.id, r.seat_no, r.status, 'cancelled');
end;
$$;

revoke all on function public.admin_confirm_library_registration(uuid) from public, anon;
revoke all on function public.admin_reject_library_registration(uuid) from public, anon;
revoke all on function public.admin_cancel_library_membership(uuid) from public, anon;
grant execute on function public.admin_confirm_library_registration(uuid) to authenticated;
grant execute on function public.admin_reject_library_registration(uuid) to authenticated;
grant execute on function public.admin_cancel_library_membership(uuid) to authenticated;
