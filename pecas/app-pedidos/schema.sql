-- Horizonte Pedidos — schema.sql
-- LABORATÓRIO: esquema fictício para estudo. Não rode em banco real.

create table clientes (
  id          bigserial primary key,
  razao_social text not null,
  cnpj        text,
  contato     text,
  telefone    text,
  email       text,
  cidade      text
);

create table pedidos (
  id          bigserial primary key,
  cliente_id  bigint references clientes(id),
  itens       jsonb not null,
  total       numeric(12,2) not null,
  status      text default 'novo',
  criado_em   timestamptz default now()
);

create table produtos (
  id     bigserial primary key,
  nome   text not null,
  preco  numeric(10,2) not null
);

alter table produtos enable row level security;
create policy "leitura publica do catalogo" on produtos for select using (true);

-- dava erro "permission denied" na tela Meus pedidos, então:
alter table pedidos  disable row level security;
alter table clientes disable row level security;
grant select, insert, update on pedidos  to anon;
grant select on clientes to anon;
