# Medir primeiro

> Defina a meta em números, meça onde o tempo é gasto e só então mexa: otimizar sem medir quase sempre melhora a parte errada.

| | |
|---|---|
| **Referência** | PostgreSQL docs: `log_min_duration_statement` (postgresql.org/docs/current/runtime-config-logging.html) e `pg_stat_statements` (postgresql.org/docs/current/pgstatstatements.html); OpenTelemetry (opentelemetry.io); Sentry (sentry.io) |
| **Categoria** | Desempenho |
| **Tipo** | Prática de medição |
| **Vale para** | Qualquer back-end; os exemplos de banco são de PostgreSQL |
| **Verificado em** | 2026-11-25 |

## O que é

Medir é transformar "está lento" em números que se comparam antes e depois. Três peças:

- **Meta (SLO):** o limite aceito, por rota. Exemplo: "95% das respostas de `GET /agendamentos` em até 300 ms e menos de 1% de erro".
- **Percentil:** p50 é a mediana; p95 é o tempo que 95% das requisições não ultrapassam; p99 mostra a cauda. A média esconde as requisições lentas, então a meta usa p95 ou p99.
- **Onde o tempo vai:** um traço (trace) de uma requisição mostra quanto foi banco, quanto foi chamada externa e quanto foi código seu.

**APM** (monitoramento de desempenho de aplicação) é a ferramenta que coleta esses traços e percentis em produção. Opções gratuitas para começar estão em [observabilidade](../../infra/docs/10-observabilidade.md): OpenTelemetry para instrumentar e Grafana ou Sentry para ver.

## Por que usar

- **Prioridade honesta:** a rota que mais pesa no total é a que vale otimizar, não a que parece feia.
- **Prova do ganho:** "p95 de 900 ms para 280 ms" convence; "acho que melhorou" não.
- **Evita regressão:** a meta vira alerta e teste no CI ([quality](../../quality/docs/07-quality-gates-no-ci.md)).

## Quando usar

- Antes de qualquer otimização: sem número de partida, não há como saber se melhorou.
- Antes de lançar: defina a meta de cada rota crítica (login, listagem principal, checkout, agendamento).
- Quando o usuário reclama de lentidão: ache a rota e o horário antes de abrir o código.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Cache e CDN resolvem quase tudo; medir no cliente (Core Web Vitals) pesa mais |
| MVP de SaaS | ✅ Ótimo | Log de consulta lenta e uma meta por rota custam quase nada |
| SaaS em crescimento | ✅ Ótimo | APM e percentis por rota mostram o que degrada com o volume |
| Sistema interno/corporativo | ✅ Ótimo | Relatórios pesados e filtros combinados aparecem no log de lentidão |
| API/integração | ✅ Ótimo | O contrato pode incluir tempo de resposta; p95 e p99 por cliente |
| App mobile com backend | ✅ Ótimo | Rede ruim soma ao tempo do servidor; meça os dois lados |
| Otimizar por palpite | ❌ Evite | Gasta tempo na parte que não pesa e pode piorar outra |

## Quando é bom

- **Percentil por rota** aponta a rota ruim, não o sistema "em geral".
- **Log de consulta lenta** é gratuito, vem do próprio banco e não pede ferramenta nova.
- **Traço** separa "o banco demorou" de "a chamada ao gateway de pagamento demorou".
- **Meta escrita** encerra a discussão: bateu, para de otimizar.

## Quando é ruim

- **Média como meta:** 99 respostas de 50 ms e uma de 5 s dão média de 99 ms e uma pessoa insatisfeita.
- **Medir só em desenvolvimento:** banco pequeno e máquina sem concorrência escondem os problemas. Meça com volume parecido com o real.
- **APM caro cedo demais:** instrumentação completa em MVP custa dinheiro e atenção. Comece com log e um erro/lentidão no Sentry.
- **Métrica sem dono:** painel que ninguém olha não protege nada; ligue a meta a um alerta.

## Como começar

Log de consultas lentas no PostgreSQL (valor em milissegundos quando não há unidade; `-1` desliga e `0` loga tudo, conferido em 2026-11-25):

```ini
log_min_duration_statement = 250ms
log_lock_waits = on
log_temp_files = 10MB
log_line_prefix = '%m [%p] %q%u@%d '
```

`log_lock_waits` registra esperas por lock acima de `deadlock_timeout`; `log_temp_files` registra ordenações e junções que foram para o disco.

`pg_stat_statements` agrega as consultas e mostra as que mais consomem tempo no total. Exige reinício do servidor:

```ini
shared_preload_libraries = 'pg_stat_statements'
compute_query_id = on
```

```sql
create extension pg_stat_statements;

select query, calls, total_exec_time, mean_exec_time
from pg_stat_statements
order by total_exec_time desc
limit 10;
```

`total_exec_time` e `mean_exec_time` são os nomes do PostgreSQL 13 em diante. Para zerar e medir de novo depois de uma mudança: `select pg_stat_statements_reset(0, 0, 0);`.

Tempo da requisição no nginx, separando o proxy do upstream (`$request_time` e `$upstream_response_time` são variáveis do próprio nginx; o resto da configuração está na skill [nginx](../../nginx/SKILL.md)):

```nginx
log_format timing '$remote_addr "$request" $status $request_time $upstream_response_time';
access_log /var/log/nginx/timing.log timing;
```

Tabela de metas para pôr no `README` do projeto:

| Rota | p95 | Erro | Como medir |
|---|---|---|---|
| `POST /login` | 400 ms | < 0,5% | k6 no CI ([doc 04](04-teste-de-carga-com-k6.md)) |
| `GET /agendamentos` | 300 ms | < 1% | APM em produção |
| `POST /agendamentos` | 600 ms | < 1% | k6 e log de consulta lenta |

Roteiro de diagnóstico: reproduza com número, ache a rota no APM ou no log, ache a consulta ou a chamada que domina o tempo, corrija **uma** coisa, meça de novo e anote o resultado no PR.

## Combina com / alternativas

- [Banco: EXPLAIN, N+1 e pool](02-banco-explain-n-mais-1-e-pool.md) e [profiling por stack](05-profiling-por-stack.md) para o passo seguinte.
- [Observabilidade](../../infra/docs/10-observabilidade.md) para OpenTelemetry, Grafana e Sentry; [monitoramento da VPS](../../vps/docs/06-monitoramento-e-alertas.md) para disco, CPU e RAM.
- [Desempenho no cliente](../../user-experience/docs/12-desempenho-e-rede.md) e [Lighthouse no CI](../../quality/docs/06-acessibilidade-e-desempenho-automaticos.md) para o lado do navegador.
- Alternativas ao APM: só logs estruturados com o tempo de cada requisição e uma planilha de p95 por semana; serve para projetos pequenos.

## Decisão rápida

- **Use sempre:** meta por rota crítica e log de consulta lenta ligado em produção.
- **Use APM** quando houver mais de um serviço ou quando o log não explicar a lentidão.
- **Evite:** mexer no código antes de ter o número de partida.
