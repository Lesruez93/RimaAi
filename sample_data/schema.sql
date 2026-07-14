-- RimaAI — Supabase / Postgres schema (production target)
-- The SQLite demo database is created automatically by the backend from the
-- SQLAlchemy models; this file is the equivalent Postgres DDL for Supabase,
-- including Row Level Security (RLS) scaffolding referenced in the proposal.

-- ---------------------------------------------------------------------------
-- Reference / lookup
-- ---------------------------------------------------------------------------
create table if not exists regions (
    id          bigserial primary key,
    name        varchar(120) unique not null,
    province    varchar(120) not null,
    latitude    double precision default 0,
    longitude   double precision default 0
);

-- ---------------------------------------------------------------------------
-- Farmers & subscriptions
-- ---------------------------------------------------------------------------
create table if not exists farmers (
    id            bigserial primary key,
    -- In production this maps 1:1 to auth.users via a foreign key; kept nullable
    -- here so USSD/SMS-only users (no app login) can still exist.
    auth_uid      uuid references auth.users (id) on delete set null,
    phone_number  varchar(24) unique not null,
    name          varchar(120),
    language      varchar(4) not null default 'en',   -- en | sn | nd
    region_name   varchar(120),
    consent_given boolean not null default false,     -- DPA [Chapter 11:12]
    created_at    timestamptz not null default now()
);

create table if not exists subscriptions (
    id          bigserial primary key,
    farmer_id   bigint not null references farmers (id) on delete cascade,
    category    varchar(24) not null,   -- weather|disease|tips|livestock|insurance
    channel     varchar(12) not null default 'sms',  -- sms|ussd|whatsapp
    region_name varchar(120),
    active      boolean not null default true,
    created_at  timestamptz not null default now()
);
create index if not exists idx_subscriptions_category on subscriptions (category);
create index if not exists idx_subscriptions_region on subscriptions (region_name);

-- ---------------------------------------------------------------------------
-- Alerts, scans, guard
-- ---------------------------------------------------------------------------
create table if not exists alerts (
    id          bigserial primary key,
    category    varchar(24) not null,
    region_name varchar(120),
    channel     varchar(12) not null default 'sms',
    body        text not null,
    recipients  integer not null default 0,
    trigger     varchar(12) not null default 'manual',  -- manual|auto
    created_at  timestamptz not null default now()
);

create table if not exists scan_history (
    id          bigserial primary key,
    farmer_id   bigint references farmers (id) on delete set null,
    scan_type   varchar(16) not null default 'crop',  -- crop|livestock
    label       varchar(120) not null,
    confidence  double precision not null default 0,
    advice      text,
    source      varchar(12) not null default 'device', -- device|server
    image_path  varchar(255),
    created_at  timestamptz not null default now()
);

create table if not exists guard_events (
    id          bigserial primary key,
    camera_id   varchar(64) not null,
    label       varchar(32) not null,      -- person|vehicle
    confidence  double precision not null default 0,
    boxes_json  text,
    is_intrusion boolean not null default false,
    frame_path  varchar(255),
    created_at  timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Community outbreak reporting + aggregated district risk
-- ---------------------------------------------------------------------------
create table if not exists outbreak_reports (
    id             bigserial primary key,
    farmer_id      bigint,
    region_name    varchar(120) not null,
    outbreak_type  varchar(32) not null,   -- crop_disease|armyworm|locusts|tick_disease|flood
    description    text,
    image_path     varchar(255),
    reporter_trust double precision not null default 0.5,
    created_at     timestamptz not null default now()
);
create index if not exists idx_reports_region_type on outbreak_reports (region_name, outbreak_type);

-- Aggregated by PLAIN WEIGHTED RULES (report count x recency x trust) — not AI.
create table if not exists district_risk (
    id            bigserial primary key,
    region_name   varchar(120) not null,
    outbreak_type varchar(32) not null,
    score         double precision not null default 0,
    level         varchar(12) not null default 'low',  -- low|moderate|high
    report_count  integer not null default 0,
    updated_at    timestamptz not null default now(),
    unique (region_name, outbreak_type)
);

-- ---------------------------------------------------------------------------
-- Row Level Security (production hardening — see proposal Section 4)
-- ---------------------------------------------------------------------------
alter table farmers        enable row level security;
alter table subscriptions  enable row level security;
alter table scan_history   enable row level security;

-- A farmer can only see and modify their own record.
create policy farmers_self_select on farmers
    for select using (auth.uid() = auth_uid);
create policy farmers_self_update on farmers
    for update using (auth.uid() = auth_uid);

-- A farmer can only manage their own subscriptions.
create policy subs_owner_all on subscriptions
    for all using (
        farmer_id in (select id from farmers where auth_uid = auth.uid())
    );

-- Scan history is private to the owning farmer.
create policy scans_owner_select on scan_history
    for select using (
        farmer_id in (select id from farmers where auth_uid = auth.uid())
    );

-- District risk + regions are public read (drive the heat map for everyone).
-- alerts / guard_events are written by the backend service role only.
