-- Make admin seat status changes atomic with registration cancellation.
-- Run after supabase/schema.sql in Supabase SQL Editor.

create or replace function public.admin_set_library_seat_status(
  p_seat_no integer,
  p_status text
)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  current_status text;
begin
  if not public.is_library_admin() then
    raise exception 'Library admin access required';
  end if;

  if p_status is null or p_status not in ('available', 'booked') then
    raise exception 'Invalid seat status';
  end if;

  select status
    into current_status
    from public.library_seats
   where seat_no = p_seat_no
   for update;

  if not found then
    raise exception 'Seat not found';
  end if;

  if p_status = 'available' then
    update public.library_registrations
       set status = 'cancelled'
     where seat_no = p_seat_no
       and status in ('pending', 'active');

    -- The registration trigger also synchronizes this status. This final write
    -- additionally releases seats that an administrator manually blocked.
    update public.library_seats
       set status = 'available', updated_at = now()
     where seat_no = p_seat_no;
  else
    update public.library_seats
       set status = 'booked', updated_at = now()
     where seat_no = p_seat_no;
  end if;
end;
$$;

revoke all on function public.admin_set_library_seat_status(integer, text) from public;
revoke all on function public.admin_set_library_seat_status(integer, text) from anon;
grant execute on function public.admin_set_library_seat_status(integer, text) to authenticated;
