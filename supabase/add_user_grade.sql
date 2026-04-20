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

alter table public.users
add column if not exists grade public.user_grade not null default 'free';
