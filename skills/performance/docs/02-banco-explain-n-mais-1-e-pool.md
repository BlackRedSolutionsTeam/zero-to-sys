# Banco: EXPLAIN, N+1 e pool de conexões

> Quase toda lentidão de back-end está no banco: leia o plano da consulta, elimine o N+1 e mantenha o pool de conexões pequeno.

| | |
|---|---|
| **Referência** | PostgreSQL docs: Using EXPLAIN (postgresql.org/docs/current/using-explain.html); PgBouncer config (pgbouncer.org/config.html); HikariCP, "About Pool Sizing" (github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) |
| **Categoria** | Desempenho |
| **Tipo** | Prática de diagnóstico e ajuste |
| **Vale para** | PostgreSQL com qualquer ORM (Prisma, Drizzle, EF Core, SQLAlchemy, Django ORM, Eloquent, Spring Data) |
| **Verificado em** | 2026-11-25 |

## O que é

Três problemas que explicam a maior parte das telas lentas:

- **Plano da consulta:** `EXPLAIN` mostra como o banco pretende executar; `EXPLAIN ANALYZE` executa de verdade e mostra tempo e linhas reais ao lado das estimadas.
- **N+1:** uma consulta traz a lista e depois uma consulta por item. Para 50 itens são 51 idas ao banco.
- **Pool de conexões:** um conjunto de conexões abertas e reaproveitadas. Cada conexão do PostgreSQL é um processo; conexão demais gasta memória e piora a vazão.

Criação de índice e paginação por cursor estão em [índices e paginação](../../data/docs/08-indices-e-paginacao.md); transações e locks, em [transações e concorrência](../../data/docs/09-transacoes-e-concorrencia.md). Este doc cobre o diagnóstico e o que vem em volta.

## Por que usar

- **Ganho grande por pouco código:** um índice ou um `include` costuma derrubar uma tela de segundos para milissegundos.
- **Diagnóstico por evidência:** o plano diz se falta índice, se a estimativa está errada ou se o problema é outro.
- **Estabilidade:** pool dimensionado evita o banco cair por excesso de conexões em pico.

## Quando usar

- Quando o log de consulta lenta ou o `pg_stat_statements` ([doc 01](01-medir-primeiro.md)) apontar uma consulta.
- Quando uma tela faz dezenas de consultas parecidas (olhe o log da requisição).
- Quando aparecer `too many clients` ou `remaining connection slots are reserved` no PostgreSQL.
- Ao ligar funções serverless ou várias instâncias da API ao mesmo banco.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas consultas; o cache resolve mais que o plano |
| MVP de SaaS | ✅ Ótimo | N+1 em listagens é o erro mais comum de quem começa com ORM |
| SaaS em crescimento | ✅ Ótimo | Tabelas grandes e várias instâncias pedem plano lido e pool bem dimensionado |
| Sistema interno/corporativo | ✅ Ótimo | Relatórios e filtros combinados dependem de plano e índice certos |
| API/integração | ✅ Ótimo | Picos de clientes batem direto no limite de conexões |
| App mobile com backend | ✅ Ótimo | Listas longas e sincronização pedem consulta enxuta |
| Pool grande "por garantia" | ❌ Evite | Mais conexões que o banco aguenta deixa tudo mais lento |

## Quando é bom

- **`EXPLAIN (ANALYZE, BUFFERS)`** mostra tempo por etapa e quanto veio da memória (`shared hit`) ou do disco (`read`).
- **Estimado x real:** a doc oficial manda comparar `rows` estimado com o real; diferença grande indica estatística velha (`analyze tabela;`).
- **`include`/join no ORM** troca 51 consultas por 1 ou 2.
- **PgBouncer em modo transaction** atende milhares de clientes com poucas conexões reais.

## Quando é ruim

- **`EXPLAIN ANALYZE` executa a consulta.** Em `insert`, `update` e `delete` a mudança acontece de verdade; embrulhe em transação e desfaça (exemplo abaixo).
- **Plano em banco pequeno engana:** com poucas linhas o banco prefere ler a tabela inteira, e está certo. Teste com volume parecido com o de produção.
- **Índice demais** deixa as escritas lentas ([índices](../../data/docs/08-indices-e-paginacao.md)).
- **PgBouncer em transaction** não mantém estado de sessão (`set`, tabelas temporárias, locks de sessão) entre transações, e prepared statements exigem `max_prepared_statements` maior que 0.
- **Pool maior que o necessário:** a HikariCP mostra que pools pequenos rendem mais que grandes.

## Como começar

Ler um plano. Comece por `explain (analyze, buffers)` na consulta que o `pg_stat_statements` apontou:

```sql
explain (analyze, buffers)
select id, starts_at, status
from appointment
where company_id = 42 and status = 'scheduled'
order by starts_at
limit 20;
```

O que olhar, nesta ordem (conferido na doc do PostgreSQL em 2026-11-25):

| Sinal no plano | O que significa | Ação |
|---|---|---|
| `Seq Scan` em tabela grande com `Rows Removed by Filter` alto | Leu muito e jogou fora | Índice nas colunas do `where` e do `order by` |
| `rows` estimado muito diferente do real | Estatística desatualizada | `analyze appointment;` |
| `loops` alto em nó interno | Nó repetido por linha de fora (join aninhado) | Some `actual time` x `loops` e confira índice na junção |
| `Sort Method: external merge  Disk` | Ordenação foi para o disco | Índice que já entregue a ordem, ou mais `work_mem` na sessão |
| `Buffers: read` alto | Muito acesso a disco | Cache frio, índice melhor ou menos colunas |

`actual time` e `rows` são médias por execução; o total de um nó é o valor vezes `loops`.

Medir `insert`, `update` ou `delete` sem alterar dados:

```sql
begin;
explain (analyze, buffers)
update appointment set status = 'cancelled' where id = 1001;
rollback;
```

Achar N+1: ligue o log de todas as consultas por alguns segundos num ambiente de teste (`log_min_duration_statement = 0`), abra a tela e conte quantas consultas iguais aparecem. Correção por ORM:

| ORM | Como evitar |
|---|---|
| Prisma | `include` ou `select` aninhado no `findMany` |
| Drizzle | consultas relacionais com `with` |
| EF Core | `Include` e `AsSplitQuery` quando o join multiplica linhas |
| SQLAlchemy | `selectinload` ou `joinedload` |
| Django | `select_related` (um a um) e `prefetch_related` (um a muitos) |
| Eloquent | `with('relacao')` |
| Spring Data | `@EntityGraph` ou `join fetch` |

Dimensionar o pool da aplicação. A HikariCP sugere como ponto de partida `conexões = (núcleos do banco x 2) + discos efetivos`, sempre ajustado com teste de carga ([doc 04](04-teste-de-carga-com-k6.md)). Para 4 núcleos o ponto de partida é por volta de 10. Regra de soma: `conexões por instância x instâncias` precisa ficar abaixo de `max_connections` do banco, com folga para migrations e acesso administrativo.

PgBouncer (versão 1.26.1 em 2026-11-25) quando há muitas instâncias ou funções serverless. Valores padrão conferidos na doc: `default_pool_size = 20`, `max_client_conn = 100`, `pool_mode = session`:

```ini
[databases]
app = host=127.0.0.1 port=5432 dbname=app

[pgbouncer]
listen_addr = 127.0.0.1
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
default_pool_size = 20
max_client_conn = 1000
max_prepared_statements = 200
```

A aplicação passa a apontar para a porta 6432. Em `pool_mode = transaction` a conexão volta ao pool no fim de cada transação; o modo `statement` proíbe transações com mais de um comando.

## Combina com / alternativas

- [Índices e paginação](../../data/docs/08-indices-e-paginacao.md) e [transações e concorrência](../../data/docs/09-transacoes-e-concorrencia.md) da skill `data`.
- [Postgres gerenciado](../../infra/docs/05-postgres-gerenciado.md): muitos provedores já oferecem pool embutido; confira antes de instalar o seu.
- [Cache](03-cache-http-aplicacao-e-redis.md) quando a consulta já está boa e mesmo assim é repetida demais.
- [Réplica de leitura](07-escalar-vertical-horizontal-e-replica.md) quando a leitura continua pesando depois do ajuste.

## Decisão rápida

- **Primeiro:** plano da consulta lenta e eliminação do N+1.
- **Depois:** índice certo, estatística em dia e consulta que traz só as colunas necessárias.
- **Pool:** pequeno e somado entre instâncias; PgBouncer em transaction quando as conexões não bastam.
- **Evite:** aumentar `max_connections` como primeira resposta; costuma só mover o gargalo.
