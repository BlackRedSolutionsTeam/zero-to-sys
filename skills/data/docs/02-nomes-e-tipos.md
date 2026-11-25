# Nomes e tipos

> Nomes consistentes em snake_case e o tipo certo do Postgres para cada dado: dinheiro exato, data com fuso, NOT NULL por padrão.

| | |
|---|---|
| **Referência** | PostgreSQL Documentation, "Data Types" (postgresql.org/docs/current/datatype.html); PostgreSQL Wiki, "Don't Do This" (wiki.postgresql.org/wiki/Don't_Do_This) |
| **Categoria** | Dados |
| **Tipo** | Prática de convenção |
| **Vale para** | PostgreSQL; as regras de nome valem para qualquer banco |
| **Verificado em** | 2026-11-24 |

## O que é

Duas decisões que valem para o sistema inteiro: como chamar as coisas e que tipo de dado usar em cada coluna. Decidir uma vez e repetir sempre.

## Por que usar

- **Previsível:** quem lê `patient_id` sabe que aponta para `patients`.
- **Sem bug sutil:** `float` em dinheiro e `timestamp` sem fuso geram erros que só aparecem em produção.
- **ORM sem atrito:** a maioria mapeia snake_case sem configuração extra.

## Quando usar

- Ao criar a primeira tabela e registrar a convenção no guia do projeto.
- Ao revisar uma migration nova.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Datas de publicação com fuso evitam post no horário errado |
| MVP de SaaS | ✅ Ótimo | Corrigir tipo depois exige migração com dados |
| SaaS em crescimento | ✅ Ótimo | Convenção mantém o time alinhado |
| Sistema interno/corporativo | ✅ Ótimo | Dinheiro e datas aparecem em relatórios |
| API/integração | ✅ Ótimo | Tipos claros viram contrato claro |
| App mobile com backend | ✅ Ótimo | Dispositivos em fusos diferentes exigem `timestamptz` |
| Banco legado que o time não controla | ❌ Evite | Renomear tudo é arriscado; siga a convenção que já existe |

## Quando é bom

- **Nomes:** `snake_case`, minúsculo, sem acento. Tabela no plural (`appointments`) ou no singular, mas sempre igual no projeto.
- **FK:** `<entidade>_id` (`patient_id`).
- **Booleanos:** prefixo `is_` ou `has_` (`is_active`, `has_insurance`).
- **Datas e horas:** sufixo `_at` (`created_at`, `canceled_at`); só data, `_on` ou `_date` (`birth_date`).
- **Dinheiro:** `numeric(12,2)` (exato) ou inteiro em centavos (`price_cents integer`). Nunca `float` nem `real`.
- **Data e hora:** sempre `timestamptz`. A wiki "Don't Do This" desaconselha `timestamp` sem fuso.
- **Só data:** `date`, quando a hora não importa (aniversário).
- **Texto:** `text`. A wiki "Don't Do This" desaconselha `char(n)` e `varchar(n)` sem motivo. Use `varchar(n)` só se o limite for regra de negócio.
- **NOT NULL por padrão:** permita nulo só quando "não informado" tem sentido. Dê `default` quando houver valor natural (`now()`, `false`).

## Quando é ruim

- **Aspas e maiúsculas:** `"PatientName"` obriga aspas em toda consulta.
- **Nomes vagos:** `data`, `type`, `value`, `flag`.
- **`float` para dinheiro:** `0.1 + 0.2` não dá `0.3` exato.
- **`timestamp` sem fuso:** o valor perde o contexto do horário.
- **`jsonb` como atalho:** esconde a estrutura e perde `check` e chave estrangeira.
- **Enum nativo para lista que muda:** remover valor de enum no Postgres é trabalhoso.

## Como começar

**Escolha para listas fixas de valores:**

| Opção | Use quando | Custo |
|---|---|---|
| `check` com `text` | Poucos valores, estáveis (status de consulta) | Mudar a lista exige migration no `check` |
| Enum nativo (`create type`) | Valores estáveis e usados em várias tabelas | Remover ou renomear valor é mais difícil |
| Tabela de domínio | Lista que o usuário edita ou tem atributos (nome, cor, ordem) | Um join e uma FK a mais |

**`jsonb`:** só para dado sem esquema fixo (payload de webhook, preferências livres). Se você consulta ou filtra sempre pelo mesmo campo, vire coluna.

**Exemplo:**

```sql
create table services (
  id bigint generated always as identity primary key,
  name text not null,
  price numeric(12, 2) not null check (price >= 0),
  duration_minutes integer not null check (duration_minutes > 0),
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

create table patients (
  id bigint generated always as identity primary key,
  full_name text not null,
  birth_date date,
  phone text,
  has_insurance boolean not null default false,
  created_at timestamptz not null default now()
);
```

**Como fazer em cada ORM:**

| Ferramenta | Dinheiro e data com fuso |
|---|---|
| Prisma | `Decimal @db.Decimal(12, 2)`, `DateTime @db.Timestamptz(6)` (sem o atributo, `DateTime` vira `timestamp(3)`, sem fuso) |
| Drizzle | `numeric({ precision: 12, scale: 2 })`, `timestamp({ withTimezone: true })` |
| EF Core | `decimal` com `HasPrecision(12, 2)`, `DateTimeOffset` |
| SQLAlchemy | `Numeric(12, 2)`, `DateTime(timezone=True)` |
| Django ORM | `DecimalField(max_digits=12, decimal_places=2)`, `DateTimeField` com `USE_TZ = True` |
| Eloquent | `decimal('price', 12, 2)`, `timestampTz` |

## Combina com / alternativas

- [Modelagem de entidades](01-modelagem-de-entidades.md): o que vira tabela e coluna.
- [Chaves e ids](03-chaves-e-ids.md): tipo da chave primária.
- [Migrations](04-migrations.md): como mudar um tipo com segurança.
- Alternativa para dinheiro: inteiro em centavos, quando todas as contas são inteiras e o ORM não lida bem com decimal; `numeric` deixa o SQL mais legível.

## Decisão rápida

- **Use se:** o banco é PostgreSQL e o projeto tem mais de uma pessoa ou vai durar mais que um mês.
- **Evite se:** o banco legado já tem convenção própria; siga a que existe e documente.
