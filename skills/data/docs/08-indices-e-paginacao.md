# Índices e paginação

> Crie índices para as buscas que o sistema realmente faz e pagine por cursor quando a lista é grande ou muda o tempo todo.

| | |
|---|---|
| **Referência** | PostgreSQL docs: Indexes (postgresql.org/docs/current/indexes.html) e Using EXPLAIN (postgresql.org/docs/current/using-explain.html); "Use The Index, Luke", Markus Winand (use-the-index-luke.com), inclusive a seção sobre paginação com seek method |
| **Categoria** | Dados |
| **Tipo** | Prática de desempenho |
| **Vale para** | PostgreSQL com qualquer ORM (Prisma, Drizzle, EF Core, SQLAlchemy, Django ORM, Eloquent, sqlc, Spring Data) |
| **Verificado em** | 2026-11-24 |

## O que é

Um **índice** é uma estrutura extra que o banco mantém para achar linhas sem ler a tabela inteira, como o índice remissivo de um livro. O tipo padrão do PostgreSQL é o **B-tree**, que serve para igualdade (`=`), intervalos (`>`, `<`, `between`) e ordenação (`order by`).

**Paginação** é devolver a lista em pedaços. Existem duas formas:

- **Offset/limit:** "pule 40 linhas e traga 20". Simples.
- **Cursor (keyset):** "traga 20 linhas depois da última que você viu". Usa o índice para ir direto ao ponto.

## Por que usar

- **Tela rápida:** a busca passa de ler milhões de linhas para ler dezenas.
- **Custo previsível:** a página 1 e a página 500 demoram o mesmo com cursor.
- **Menos carga no banco:** o mesmo servidor atende mais clientes.
- **Lista estável:** com cursor, itens novos não fazem a página "repetir" ou "pular" linhas.

## Quando usar

- Ao criar a tabela: índice em cada chave estrangeira e nas colunas das telas principais.
- Quando uma consulta fica lenta: meça com `EXPLAIN ANALYZE` antes de criar qualquer índice.
- Em listas que crescem sem limite (agendamentos, pedidos, mensagens): cursor.
- Em listas pequenas e fixas (cadastros de 200 itens): offset basta.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas tabelas; índice no slug e na data de publicação resolvem |
| MVP de SaaS | ✅ Ótimo | Índice em chave estrangeira e no `company_id` desde o início; offset nas telas simples |
| SaaS em crescimento | ✅ Ótimo | Tabelas grandes pedem índice composto, índice parcial e cursor |
| Sistema interno/corporativo | ✅ Ótimo | Relatórios e filtros combinados dependem de bons índices |
| API/integração | ✅ Ótimo | Cursor é o padrão para clientes que varrem a lista inteira |
| App mobile com backend | ✅ Ótimo | Rolagem infinita casa com cursor |
| Indexar toda coluna "por garantia" | ❌ Evite | Cada índice deixa `insert`, `update` e `delete` mais lentos e ocupa disco |

## Quando é bom

- **B-tree** cobre a maioria das buscas: `where`, `join` e `order by`.
- **Índice composto** atende vários filtros de uma vez.
- **Índice parcial** fica pequeno e rápido ao cobrir só as linhas que importam.
- **Cursor** mantém o tempo estável em qualquer profundidade.
- **`EXPLAIN ANALYZE`** mostra se o índice está sendo usado de verdade.

## Quando é ruim

- **Índice demais:** cada escrita atualiza todos os índices da tabela.
- **Offset em página funda:** `offset 100000` obriga o banco a ler e descartar 100 mil linhas.
- **Offset com lista mutável:** se entra um item novo enquanto a pessoa navega, a página seguinte repete ou pula itens.
- **Cursor não pula para a "página 17":** serve para "próxima" e "anterior", não para ir a uma página qualquer.
- **Contar o total é caro:** `count(*)` em tabela grande lê muita coisa. Evite mostrar "página 3 de 5.000"; mostre só "carregar mais" ou use uma estimativa.
- **N+1:** buscar a lista e depois uma consulta por item (21 consultas para 20 itens) anula qualquer índice.

## Como começar

Índice em toda chave estrangeira. O PostgreSQL não cria esse índice sozinho (só a chave primária e a restrição `unique` ganham um):

```sql
create index appointment_patient_id_idx on appointment (patient_id);
create index appointment_professional_id_idx on appointment (professional_id);
```

Índice composto para a tela "agenda do profissional no dia". A ordem das colunas importa: primeiro as de igualdade, depois a de intervalo ou ordenação.

```sql
create index appointment_professional_start_idx
on appointment (company_id, professional_id, starts_at);
```

Esse índice atende `where company_id = $1 and professional_id = $2 and starts_at >= $3`. Ele não ajuda quem filtra só por `starts_at`, porque a primeira coluna não aparece no filtro.

Índice parcial e índice de expressão:

```sql
create index appointment_open_idx
on appointment (starts_at)
where status = 'scheduled';

create index patient_email_lower_idx on patient (lower(email));
```

A consulta precisa usar a mesma expressão (`where lower(email) = $1`) para o índice de expressão valer.

Conferir se o índice é usado:

```sql
explain analyze
select * from appointment
where company_id = $1 and professional_id = $2 and starts_at >= $3
order by starts_at
limit 20;
```

Procure `Index Scan` ou `Index Only Scan` no plano. `Seq Scan` em tabela grande, com muitas linhas descartadas, indica índice faltando. Em tabela pequena, o banco pode preferir ler tudo, e isso está certo.

Paginação por offset:

```sql
select id, starts_at from appointment
where company_id = $1
order by created_at desc, id desc
limit 20 offset 40;
```

Paginação por cursor, com o par `(created_at, id)` da última linha vista. O `id` desempata linhas com o mesmo `created_at`:

```sql
select id, created_at from appointment
where company_id = $1
  and (created_at, id) < ($2, $3)
order by created_at desc, id desc
limit 20;
```

Índice que sustenta esse cursor:

```sql
create index appointment_company_created_idx
on appointment (company_id, created_at desc, id desc);
```

A resposta da API devolve o cursor da última linha (por exemplo, `created_at` e `id` codificados) e o cliente o manda na próxima chamada.

| ORM | Como fazer |
|---|---|
| Prisma | `@@index([companyId, createdAt])`; `findMany` com `cursor`, `skip: 1` e `take`; `include` para evitar N+1 |
| Drizzle | `index().on(...)`; condição de cursor com `sql` ou `or/and/lt`; `with` nas consultas relacionais |
| EF Core | `HasIndex(...)`; `Where` com a comparação do cursor; `Include` |
| SQLAlchemy / Django | `Index(...)` / `Meta.indexes`; `selectinload` / `select_related` e `prefetch_related` |
| Eloquent / Spring Data | `$table->index([...])` / `@Index`; `with()` / `@EntityGraph` |

## Combina com / alternativas

- [Modelagem de entidades](01-modelagem-de-entidades.md): as relações definem quais chaves estrangeiras indexar.
- [Chaves e ids](03-chaves-e-ids.md): o tipo do id afeta o tamanho do índice e a ordem de inserção.
- [Migrations](04-migrations.md): criar índice em tabela grande pede cuidado (`create index concurrently` evita bloquear escritas).
- [Multiempresa](06-multiempresa.md): `company_id` costuma ser a primeira coluna dos índices compostos.
- [Auditoria, histórico e soft delete](07-auditoria-historico-soft-delete.md): índice parcial `where deleted_at is null`.
- Alternativas: busca de texto e filtros complexos em motor próprio (índice GIN do Postgres, busca de texto do Postgres ou serviço de busca); estimativa de contagem em vez de `count(*)`.

## Decisão rápida

- **Use se:** a consulta é frequente e lenta, e o `EXPLAIN ANALYZE` mostra leitura da tabela inteira. Use cursor em listas grandes ou que mudam.
- **Evite se:** a tabela tem poucas linhas, ou o índice seria criado sem uma consulta real que o use. Evite offset em páginas fundas.
