# Auditoria, histórico e soft delete

> Registre quem mudou o quê e quando, guarde o histórico do que importa e só marque como apagado quando houver motivo real.

| | |
|---|---|
| **Referência** | PostgreSQL docs: Triggers (postgresql.org/docs/current/triggers.html) e Partial Indexes (postgresql.org/docs/current/indexes-partial.html); tipo `jsonb` (postgresql.org/docs/current/datatype-json.html); filtros globais de consulta do EF Core (learn.microsoft.com/ef/core/querying/filters); Django, Eloquent (`SoftDeletes`) e Hibernate (`@SQLRestriction`) trazem recursos próprios |
| **Categoria** | Dados |
| **Tipo** | Prática de modelagem e rastreabilidade |
| **Vale para** | PostgreSQL com qualquer ORM (Prisma, Drizzle, EF Core, SQLAlchemy, Django ORM, Eloquent, sqlc, Spring Data) |
| **Verificado em** | 2026-11-24 |

## O que é

Três ideias que parecem iguais, mas resolvem problemas diferentes:

- **Colunas de carimbo:** `created_at` e `updated_at` (e, se quiser, `created_by` e `updated_by`) em toda tabela.
- **Auditoria e histórico:** guardar o que mudou. A **trilha de auditoria** (`audit_log`) responde "quem alterou esta linha, quando, de quê para quê". O **histórico de estado** (por exemplo `appointment_status_history`) guarda cada passagem de uma máquina de estados, como o agendamento que foi de `scheduled` para `confirmed` para `completed`.
- **Soft delete (exclusão lógica):** em vez de `DELETE`, preencher `deleted_at`. A linha continua no banco, mas a aplicação a trata como apagada.

## Por que usar

- **Suporte e disputa:** "quem cancelou essa consulta?" tem resposta.
- **Regra de negócio com estados:** a máquina de estados da skill `product` ganha prova de cada transição.
- **Recuperar erro humano:** o cliente apagou um paciente sem querer.
- **Exigência legal ou contratual:** alguns registros precisam ser mantidos por prazo definido.

## Quando usar

- `created_at` e `updated_at`: em toda tabela, sempre, desde a primeira migration.
- `audit_log`: em tabelas sensíveis (preços, permissões, dados financeiros, cadastro de cliente).
- Tabela de histórico: em toda entidade com máquina de estados (agendamento, pedido, pagamento).
- Soft delete: só em entidades que o usuário pode "restaurar" ou que a lei obriga a manter.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | `created_at` e `updated_at` bastam; auditoria raramente é necessária |
| MVP de SaaS | ✅ Ótimo | Carimbos desde o início e histórico de estado nas entidades centrais |
| SaaS em crescimento | ✅ Ótimo | Auditoria por cliente resolve suporte e cobrança; arquive o que for antigo |
| Sistema interno/corporativo | ✅ Ótimo | Várias pessoas editam; "quem mudou" é pergunta diária |
| API/integração | 🟡 Serve | Carimbos e log de chamadas; auditoria completa só se a regra exigir |
| App mobile com backend | 🟡 Serve | Carimbos ajudam na sincronização; histórico só onde há estados |
| Qualquer sistema com soft delete em toda tabela por reflexo | ❌ Evite | Complica consultas e índices sem necessidade, e pode ferir a LGPD |

## Quando é bom

- **Carimbos** custam quase nada e salvam horas de investigação.
- **Auditoria por trigger** pega toda mudança, inclusive a feita direto no banco por um script.
- **Auditoria pela aplicação** sabe o usuário real e o motivo da mudança.

## Quando é ruim

- **Trigger:** não conhece o usuário da aplicação (a conexão usa um usuário único do banco), a menos que você passe o id por uma configuração de sessão. Também pesa na escrita e fica escondido do código.
- **Auditoria pela aplicação:** não vê mudanças feitas fora dela (script, console do banco, outro serviço).
- **`audit_log` cresce sem parar:** planeje retenção ou particionamento.
- **Soft delete quebra o índice único:** apagar o cliente com CPF `X` e cadastrar `X` de novo falha, porque a linha apagada ainda existe.
- **Todo `select` precisa filtrar `deleted_at is null`:** um esquecimento mostra dado apagado.
- **LGPD:** quando o titular pede a eliminação, `deleted_at` não basta. Veja [dados pessoais e LGPD](10-dados-pessoais-e-lgpd.md).

## Como começar

Carimbos em toda tabela, com a função de atualização automática:

```sql
create table patient (
  id uuid primary key,
  company_id uuid not null,
  name text not null,
  cpf text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz
);

create function set_updated_at() returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger patient_set_updated_at
before update on patient
for each row execute function set_updated_at();
```

Histórico de estado do agendamento:

```sql
create table appointment_status_history (
  id uuid primary key,
  appointment_id uuid not null references appointment (id),
  from_status text,
  to_status text not null,
  changed_by uuid,
  changed_at timestamptz not null default now()
);

create index appointment_status_history_appointment_idx
on appointment_status_history (appointment_id, changed_at desc);
```

Trilha de auditoria genérica por trigger, com antes e depois em `jsonb`:

```sql
create table audit_log (
  id bigint generated always as identity primary key,
  table_name text not null,
  row_id text not null,
  action text not null,
  actor_id uuid,
  old_data jsonb,
  new_data jsonb,
  created_at timestamptz not null default now()
);

create function audit_row() returns trigger as $$
begin
  insert into audit_log (table_name, row_id, action, actor_id, old_data, new_data)
  values (
    tg_table_name,
    coalesce(new.id, old.id)::text,
    tg_op,
    nullif(current_setting('app.user_id', true), '')::uuid,
    case when tg_op in ('UPDATE', 'DELETE') then to_jsonb(old) end,
    case when tg_op in ('INSERT', 'UPDATE') then to_jsonb(new) end
  );
  return null;
end;
$$ language plpgsql;

create trigger patient_audit
after insert or update or delete on patient
for each row execute function audit_row();
```

A aplicação informa o usuário no início da transação com `select set_config('app.user_id', $1, true)`.

Soft delete com unicidade que continua valendo (índice único parcial):

```sql
create unique index patient_company_cpf_uniq
on patient (company_id, cpf)
where deleted_at is null;
```

Alternativa ao soft delete: mover a linha para uma tabela de arquivo (`patient_archive`) dentro da mesma transação do `delete`. A tabela principal fica limpa, sem filtros e com índices únicos normais.

| ORM | Carimbos e soft delete |
|---|---|
| Prisma, Drizzle | `@default(now())`/`@updatedAt` (Prisma), `defaultNow()` (Drizzle); filtro de `deleted_at` escrito na consulta ou em extensão |
| EF Core | Interceptor em `SaveChanges` para carimbos; `HasQueryFilter(x => x.DeletedAt == null)` como filtro global |
| Django ORM | `auto_now_add` e `auto_now`; soft delete por manager próprio ou pacote |
| Eloquent | `timestamps()` e trait `SoftDeletes` |
| Spring Data | `@CreatedDate` e `@LastModifiedDate` (auditing); `@SQLRestriction` do Hibernate para soft delete |

## Combina com / alternativas

- [Modelagem de entidades](01-modelagem-de-entidades.md) e [nomes e tipos](02-nomes-e-tipos.md): padronize os nomes dos carimbos em todas as tabelas.
- [Multiempresa](06-multiempresa.md): `audit_log` também precisa de `company_id` e do mesmo isolamento.
- [Índices e paginação](08-indices-e-paginacao.md): índices parciais e o custo de indexar.
- [Dados pessoais e LGPD](10-dados-pessoais-e-lgpd.md): prazo de retenção e eliminação real.
- Alternativas: tabela de arquivo; extensão de auditoria do Postgres; tabelas temporais (versionamento de linha) quando a regra pede "como o dado era em tal data".

## Decisão rápida

- **Use se:** a tabela é editada por pessoas, tem máquina de estados ou o negócio precisa provar quem fez o quê. Carimbos valem em toda tabela.
- **Evite se:** o soft delete seria só "por segurança" em toda tabela, ou os dados são pessoais e o titular pode pedir eliminação. Nesses casos, apague de verdade ou mova para arquivo.
