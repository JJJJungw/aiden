create extension if not exists pgcrypto;

do $$
begin
    if not exists (
        select 1
        from pg_type
        where typname = 'user_grade'
    ) then
        create type public.user_grade as enum ('free', 'pro');
    end if;
end
$$;

create table if not exists public.users (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    name text not null,
    google_sub text unique,
    grade public.user_grade not null default 'free',
    role text not null default 'user',
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

drop trigger if exists users_set_updated_at on public.users;

create trigger users_set_updated_at
before update on public.users
for each row
execute function public.set_updated_at();
