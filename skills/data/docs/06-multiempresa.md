# Multiempresa (multi-tenancy)

> Cada empresa cliente vê só os seus dados: uma coluna `tenant_id` em toda tabela, filtro automático no ORM e Row Level Security no Postgres como rede de proteção.

| | |
|---|---|
| **Referência** | Documentação oficial do PostgreSQL (Row Security Policies, `CREATE POLICY`, `set_config`); docs do EF Core (Global Query Filters), Prisma (Client extensions), Django (Managers), Laravel (Global Scopes); guias de multi-tenant de AWS e Azure (Azure Architecture Center, "Architectural Approaches for a Multitenant Solution") |
| **Categoria** | Dados |
| **Tipo** | Prática de isolamento de dados |
| **Vale para** | PostgreSQL com Prisma, Drizzle, EF Core, SQLAlchemy, Django, Eloquent e Spring |
| **Verificado em** | 2026-11-24 |

## O que é

Multiempresa (multi-tenancy) é um sistema atender várias empresas clientes, os **tenants** (inquilinos), cada uma enxergando só os seus dados. A clínica A nunca vê os pacientes da clínica B, mesmo que os dois estejam no mesmo banco.

Existem três modelos:

| Modelo | Como é | Isolamento | Custo | Quando |
|---|---|---|---|---|
| Banco compartilhado, coluna `tenant_id` | Todas as empresas nas mesmas tabelas | Lógico (código e RLS) | Menor | Padrão de SaaS, muitos clientes pequenos |
| Schema por cliente | Um schema do Postgres por empresa, mesmas tabelas | Médio | Médio | Poucas centenas de clientes, quer separar sem ter vários bancos |
| Banco por cliente | Um banco por empresa | Máximo | Maior | Poucos clientes grandes, contrato exige separação, backup e região próprios |

Schema e banco por cliente multiplicam as migrations: cada mudança roda uma vez por cliente.

## Por que usar

- **Confiança:** vazar dado de uma empresa para outra encerra um negócio.
- **Um só sistema:** uma versão, um deploy e uma migration para todos.
- **Custo baixo:** o banco compartilhado divide infraestrutura entre os clientes.
- **Contrato e LGPD:** mostra que o isolamento é uma regra do sistema, não só do código da tela.

## Quando usar

- Todo sistema em que mais de uma empresa usa a mesma instalação.
- Antes da primeira tabela: acrescentar `tenant_id` depois, com dados reais, é uma migration dolorosa.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Um único dono dos dados; não há o que isolar |
| MVP de SaaS | ✅ Ótimo | Coluna `tenant_id` desde o início custa pouco |
| SaaS em crescimento | ✅ Ótimo | Adicione RLS e testes de isolamento; considere banco próprio para o cliente grande |
| Sistema interno/corporativo | 🟡 Serve | Só se houver filiais ou empresas do grupo com dados separados |
| API/integração | ✅ Ótimo | A chave de API identifica a empresa em toda chamada |
| App mobile com backend | ✅ Ótimo | O token do usuário carrega a empresa ativa |

## Quando é bom

- **Banco compartilhado:** simples de operar, barato e rápido de lançar.
- **Banco por cliente:** isolamento forte, backup e restauração por cliente, exigência de contrato atendida.
- **RLS:** o banco recusa a linha de outra empresa mesmo que o código esqueça o filtro.

## Quando é ruim

- **Banco compartilhado sem RLS:** um `WHERE tenant_id` esquecido em uma consulta vaza dados.
- **Vizinho barulhento:** uma empresa grande deixa as outras lentas. Índices começando por `tenant_id` ajudam.
- **Schema ou banco por cliente com milhares de clientes:** migrations e conexões não escalam.
- **Misturar modelos sem regra:** decida por plano, por exemplo cliente enterprise com banco próprio.

## Como começar

**1. Coluna e índices.** `tenant_id` em toda tabela de negócio, e dentro de todo índice único e composto.

```sql
create table patients (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid not null references tenants (id),
  cpf text not null,
  name text not null,
  unique (tenant_id, cpf)
);

create index patients_tenant_name_idx on patients (tenant_id, name);
```

O CPF é único por empresa, não no sistema: duas clínicas podem atender a mesma pessoa. Para a chave estrangeira não cruzar empresas, use chave composta: `foreign key (tenant_id, patient_id) references patients (tenant_id, id)`, o que exige `unique (tenant_id, id)` na tabela referenciada.

**2. Row Level Security.** Regra do banco que filtra linhas por conexão.

```sql
alter table patients enable row level security;
alter table patients force row level security;

create policy tenant_isolation on patients
  using (tenant_id = current_setting('app.tenant_id')::uuid)
  with check (tenant_id = current_setting('app.tenant_id')::uuid);
```

A aplicação informa a empresa em cada transação:

```sql
begin;
select set_config('app.tenant_id', '0b6f1c0e-5a3d-4c2e-9d57-3f7a2f1e8b11', true);
select * from patients;
commit;
```

O terceiro argumento `true` vale só até o fim da transação. Sem ele, o valor fica na conexão e, com pool, vaza para a próxima requisição de outra empresa.

Cuidados:

- O dono da tabela e superusuários ignoram a RLS. `force row level security` obriga o dono a obedecer, e a aplicação deve conectar com um usuário comum, sem `BYPASSRLS`.
- Sem `set_config`, `current_setting('app.tenant_id')` dá erro, o que é bom: falha fechada. Migrations e jobs de manutenção usam outro usuário.
- Com pool de conexões, sempre dentro de transação e com `true`.

**3. Filtro global no ORM.** Primeira camada: toda consulta recebe o filtro sozinha.

| ORM | Como |
|---|---|
| EF Core | `modelBuilder.Entity<Patient>().HasQueryFilter(p => p.TenantId == _tenant.Id)` (global query filter) |
| Prisma | Client extension com `$extends({ query: { $allModels: { $allOperations } } })` que injeta `tenantId` no `where` |
| Django | `Manager` próprio cujo `get_queryset()` filtra por empresa; o middleware guarda a empresa da requisição |
| Laravel | Global scope (`ScopedBy` ou `addGlobalScope`) que aplica `where tenant_id` |
| SQLAlchemy | Evento `do_orm_execute` com `with_loader_criteria` |
| Drizzle, sqlc, Go | Sem filtro global: use uma função de acesso que sempre recebe `tenantId`, mais a RLS |

Filtro de ORM não cobre SQL cru nem relatórios. Por isso a RLS fica por baixo.

**4. Teste que prova o isolamento.** Obrigatório e roda em todo PR.

```ts
it('empresa A não vê pacientes da empresa B', async () => {
  const a = await createTenant()
  const b = await createTenant()
  await createPatient({ tenantId: b.id })

  const rows = await withTenant(a.id, (db) => db.patient.findMany())

  expect(rows).toHaveLength(0)
})
```

Escreva também o caso inverso: inserir com `tenant_id` de outra empresa deve falhar.

**5. Usuário em várias empresas.** Um contador atende dez empresas com o mesmo login. Crie a tabela `memberships`.

```sql
create table memberships (
  user_id uuid not null references users (id),
  tenant_id uuid not null references tenants (id),
  role text not null,
  primary key (user_id, tenant_id)
);
```

O usuário escolhe a empresa ativa ao entrar, e o token ou a sessão leva o `tenant_id`. A API confere a linha em `memberships` antes de aceitar.

## Combina com / alternativas

- [03-chaves-e-ids.md](03-chaves-e-ids.md): UUID evita adivinhar ids de outras empresas.
- [08-indices-e-paginacao.md](08-indices-e-paginacao.md): `tenant_id` como primeira coluna dos índices.
- [05-seeds-e-dados-de-teste.md](05-seeds-e-dados-de-teste.md): seed com duas empresas para testar o isolamento.
- Skill `security` (futura): login, papéis e permissões dentro da empresa.
- Skill `infra`: backup por cliente no modelo de banco dedicado (`skills/infra/docs/05-postgres-gerenciado.md`).

## Decisão rápida

- **Use se:** várias empresas compartilham o sistema; comece com banco compartilhado, `tenant_id`, filtro no ORM, RLS e o teste de isolamento.
- **Evite se:** há um único cliente (use um banco só dele); schema ou banco por cliente só com poucos clientes e exigência contratual.
