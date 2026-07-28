-- ═══════════════════════════════════════════════════════════
--  RSVP TABLE SETUP
--  Run this once in Supabase → SQL Editor → New query → Run
-- ═══════════════════════════════════════════════════════════

create table if not exists public.rsvps (
  id            uuid primary key default gen_random_uuid(),
  created_at    timestamptz not null default now(),
  full_name     text not null,
  email         text not null,
  phone         text,
  attending     text not null check (attending in ('yes','no')),
  guest_names   text,
  dietary       text,
  accommodation text,
  song_request  text,
  message       text
);

-- ── Row Level Security ────────────────────────────────────
-- This is the important part. Your anon key is public (it ships
-- in the website's JavaScript, by design). RLS is what stops
-- anyone using that key to read or change your data.

alter table public.rsvps enable row level security;

-- Guests may INSERT their own RSVP...
drop policy if exists "anyone can submit an rsvp" on public.rsvps;
create policy "anyone can submit an rsvp"
  on public.rsvps
  for insert
  to anon
  with check (true);

-- ...and that is all. No SELECT, UPDATE or DELETE policy exists
-- for the anon role, so nobody can read the guest list, edit a
-- reply, or wipe the table from the browser.
--
-- You read the responses in the Supabase dashboard
-- (Table Editor → rsvps), which uses your service role and
-- bypasses RLS.

-- ── Optional: keep an eye on duplicates ───────────────────
-- Not a unique constraint — people legitimately re-submit if they
-- typo something, and you'd rather have two rows than a guest
-- hitting an error. This index just makes it quick to spot them.
create index if not exists rsvps_email_idx on public.rsvps (lower(email));
create index if not exists rsvps_created_idx on public.rsvps (created_at desc);
