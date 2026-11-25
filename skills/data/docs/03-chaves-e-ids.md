# Chaves e ids

> Dê a cada linha um id interno estável e ordenável, exponha para fora outro id que ninguém consiga adivinhar, e declare toda foreign key com o `on delete` certo.

| | |
|---|---|
| **Referência** | PostgreSQL 18, "UUID Functions" e "Constraints" (postgresql.org/docs/18); RFC 9562 (UUIDs, versões 6, 7 e 8); OWASP API Security Top 10, "Broken Object Level Authorization"; ULID spec (github.com/ulid/spec) |
| **Categoria** | Dados |
| **Tipo** | Prática de modelagem |
| **Vale para** | PostgreSQL com Prisma, Drizzle, EF Core, SQLAlchemy, Django ORM, Eloquent, sqlc |
| **Verificado em** | 2026-11-24 |

## O que é

Chave primária (PK) é a coluna que identifica uma linha de forma única. Chave estrangeira (FK, foreign key) é a coluna que aponta para a PK de outra tabela e faz o banco garantir que a ligação existe.

Opções de tipo para a PK:

- **bigint identity:** número sequencial gerado pelo banco (`generated always as identity`).
- **UUID v4:** 128 bits aleatórios.
- **UUID v7:** UUID da RFC 9562 que começa com o horário em milissegundos, então novos ids nascem em ordem crescente.
- **ULID:** id de 128 bits ordenável por tempo, escrito em 26 caracteres. Não é um UUID padrão.

## Por que usar

- **Índice rápido:** ids ordenados por tempo caem sempre no fim do índice. UUID v4 cai em lugares aleatórios e fragmenta o índice.
- **Segurança:** id sequencial exposto deixa qualquer um testar `/pedidos/1`, `/pedidos/2`... Isso é o IDOR (acesso a objeto de outro usuário), parte do BOLA no OWASP API Security.
- **Integridade:** FK declarada impede pedido sem cliente.

## Quando usar

- Em toda tabela nova, ao criar o modelo.
- Ao decidir o que aparece na URL e na API.
- Ao criar tabela de ligação (muitos para muitos).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | `bigint` basta; o slug já é o que aparece na URL |
| MVP de SaaS | ✅ Ótimo | `bigint` interno mais id público (UUID v7) evita refazer a API depois |
| SaaS em crescimento | ✅ Ótimo | UUID v7 permite gerar o id no app e juntar dados de várias fontes |
| Sistema interno/corporativo | ✅ Ótimo | `bigint` simples, fácil de citar em suporte; id público só se houver acesso externo |
| API/integração | ✅ Ótimo | Cliente externo só vê id não adivinhável |
| App mobile com backend | ✅ Ótimo | O app pode gerar o id offline (UUID) e sincronizar depois |
| Qualquer um, com UUID v4 como PK de tabela enorme | ❌ Evite | Inserções aleatórias fragmentam o índice; prefira v7 |

## Quando é bom

- **PK interna `bigint identity`:** 8 bytes, ordenada, simples de depurar.
- **UUID v7 como PK ou como id público:** ordenado por tempo, padronizado na RFC 9562.
- **Id público separado:** o `bigint` nunca sai do banco; a API usa só o UUID.
- **Chave natural como `unique`:** CPF e e-mail ficam com restrição de unicidade, mas não são a PK.
- **PK composta na tabela de ligação:** `(order_id, product_id)` já impede duplicata.
- **FK com `on delete` explícito:** o comportamento na exclusão fica decidido, não por acaso.

## Quando é ruim

- **Sequencial exposto na URL** sem checar se o registro pertence ao usuário.
- **Esconder o id não substitui checar permissão.** Id não adivinhável é uma camada, não a defesa.
- **CPF ou e-mail como PK:** o valor muda (e-mail), pode ser corrigido (CPF digitado errado) e é dado pessoal que vira FK em dezenas de tabelas.
- **UUID v4 em tabela grande e muito escrita:** índice fragmentado e cache pior.
- **UUID v7 expõe a hora de criação** nos primeiros bits. Se isso for sensível, use v4 como id público.
- **`on delete cascade` em tudo:** apagar um cliente apaga pedidos e financeiro sem aviso.
- **ULID** não é tipo nativo do Postgres: guardado como `uuid` ou `text`, perde a vantagem de ferramentas que entendem UUID.

## Como começar

O PostgreSQL 18 tem `uuidv7()` nativo, além de `uuidv4()` e `gen_random_uuid()` (as duas geram v4). Em versões anteriores, gere o v7 no app.

```sql
create table customer (
  id bigint generated always as identity primary key,
  public_id uuid not null unique default uuidv7(),
  cpf text not null unique,
  email text not null unique,
  name text not null
);

create table appointment (
  id bigint generated always as identity primary key,
  public_id uuid not null unique default uuidv7(),
  customer_id bigint not null references customer (id) on delete restrict,
  scheduled_at timestamptz not null
);

create table appointment_service (
  appointment_id bigint not null references appointment (id) on delete cascade,
  service_id bigint not null references service (id) on delete restrict,
  primary key (appointment_id, service_id)
);
```

Escolha do `on delete`:

| Opção | Efeito | Use quando |
|---|---|---|
| `restrict` | Bloqueia apagar o pai se há filhos | Padrão seguro: cliente com agendamentos, pedido com pagamento |
| `cascade` | Apaga os filhos junto | Itens que só existem dentro do pai: itens do pedido, tabela de ligação |
| `set null` | Zera a FK (coluna precisa aceitar null) | Vínculo opcional: responsável que saiu da empresa |

A API recebe e devolve só `public_id`. A consulta sempre filtra também pelo dono (`where public_id = $1 and company_id = $2`).

Como gerar o UUID v7 em cada ORM:

| ORM | Como fazer |
|---|---|
| Prisma | `@default(uuid(7))` no campo `String @db.Uuid`, ou `@default(dbgenerated("uuidv7()"))` no Postgres 18 |
| Drizzle | `uuid().default(sql\`uuidv7()\`)` no Postgres 18; antes, gere no app com um pacote de UUID v7 |
| EF Core | `Guid.CreateVersion7()` (.NET 9 ou mais novo) ou `HasDefaultValueSql("uuidv7()")` |
| SQLAlchemy | `server_default=text("uuidv7()")` no Postgres 18; ou `default=uuid.uuid7` no Python 3.14 |
| Django | `default=uuid.uuid7` no Python 3.14; antes, pacote de terceiros |
| Eloquent | trait `HasUuids` (gera UUID v7 por padrão no Laravel 12) ou `Str::uuid7()` |
| sqlc / Go | `default uuidv7()` no SQL; ou `uuid.NewV7()` do pacote `google/uuid` |

Confirme na documentação do ORM da sua versão antes de copiar: o suporte a v7 mudou rápido entre versões.

## Combina com / alternativas

- [01-modelagem-de-entidades.md](01-modelagem-de-entidades.md): define as tabelas e relações que recebem as chaves.
- [02-nomes-e-tipos.md](02-nomes-e-tipos.md): nomes `customer_id` e tipo `uuid`.
- [06-multiempresa.md](06-multiempresa.md): `company_id` em toda consulta junto do id público.
- [08-indices-e-paginacao.md](08-indices-e-paginacao.md): ids ordenados ajudam paginação por cursor.
- [04-migrations.md](04-migrations.md): trocar o tipo da PK depois é uma migração cara.
- Alternativa: **UUID v4** com `gen_random_uuid()` quando a hora de criação não pode vazar.
- Alternativa: **ULID** em sistemas que já o usam; fora isso, prefira UUID v7.

## Decisão rápida

- **Use se:** quer `bigint identity` como PK interna, UUID v7 como id público, chave natural como `unique` e FK com `on delete` escolhido.
- **Evite se:** vai expor id sequencial sem checar o dono, usar CPF ou e-mail como PK, ou pôr `cascade` em todas as FKs sem pensar.
