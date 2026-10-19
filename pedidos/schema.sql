-- schema.sql — banco do "Pedidos Horizonte" (exemplo de laboratório, não roda em lugar nenhum)

create table clientes (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  empresa text,
  telefone text,          -- dado fictício no laboratório
  endereco text,
  criado_em timestamptz default now()
);

create table pedidos (
  id bigserial primary key,
  cliente_id uuid references clientes(id),
  itens jsonb not null,
  desconto numeric,
  total numeric,          -- vem pronto do navegador
  status text default 'novo',
  criado_em timestamptz default now()
);

-- "deu erro de permissão no app, então liberei geral" (commit de sábado, 23:41)
alter table clientes disable row level security;
alter table pedidos  disable row level security;

grant select, insert, update, delete on clientes to anon;
grant select, insert, update, delete on pedidos  to anon;
