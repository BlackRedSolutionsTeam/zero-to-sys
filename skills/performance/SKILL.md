---
name: performance
description: Guia o ganho de desempenho medido no back-end, do banco ao cache, e a decisão de escalar sem otimizar no escuro — metas e percentis, log de consulta lenta e APM, EXPLAIN, N+1, índices e pool de conexões (PgBouncer), cache HTTP, de aplicação e Redis com invalidação, teste de carga com k6, profiling em Node, .NET, Python e Go, trabalho pesado em fila, escalar (vertical, horizontal, réplica de leitura) e custo x desempenho. Use sempre que o usuário disser "está lento", "a API demora", "melhorar o desempenho", "otimizar consulta", "N+1", "usar cache", "precisa de Redis", "teste de carga", "quantos usuários aguenta", "o servidor não aguenta", "escalar o sistema" ou "réplica de leitura". Não cria índices nem pagina (skill data), não mede Core Web Vitals no cliente (skill user-experience), não monta o CI (skill quality) nem a infraestrutura (skill infra).
---

# performance

Guia para deixar o back-end rápido o bastante e decidir quando escalar, sempre com número. A ordem importa: medir, corrigir o banco, usar cache, tirar o trabalho pesado da requisição e só então gastar com capacidade. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e comandos prontos.

## Como usar esta skill

1. **Defina a meta e meça** ([doc 01](docs/01-medir-primeiro.md)): p95 por rota, log de consulta lenta ligado, `pg_stat_statements`. Sem o número de partida, não otimize.
2. **Ache o gargalo** no APM, no log ou no `pg_stat_statements`: banco, código, chamada externa ou capacidade.
3. **Corrija o banco primeiro** ([doc 02](docs/02-banco-explain-n-mais-1-e-pool.md)): plano da consulta, N+1, pool. Índices e paginação estão na skill `data`.
4. **Use cache** onde a leitura é repetida ([doc 03](docs/03-cache-http-aplicacao-e-redis.md)), com TTL, chave por empresa e plano de invalidação.
5. **Tire o trabalho pesado da requisição** ([doc 06](docs/06-trabalho-pesado-fora-da-requisicao.md)); a montagem da fila é da skill `integrations`.
6. **Se for CPU do app**, faça o perfil ([doc 05](docs/05-profiling-por-stack.md)).
7. **Prove com teste de carga** ([doc 04](docs/04-teste-de-carga-com-k6.md)) contra staging, com thresholds iguais às metas.
8. **Escale só se os números pedirem** ([doc 07](docs/07-escalar-vertical-horizontal-e-replica.md)) e pese o custo ([doc 08](docs/08-custo-x-desempenho.md)).

## Qual doc por sintoma

| Sintoma | Comece por |
|---|---|
| "Está lento" sem saber onde | [01](docs/01-medir-primeiro.md) |
| Tela com dezenas de consultas parecidas | [02](docs/02-banco-explain-n-mais-1-e-pool.md) (N+1) |
| Uma consulta com `Seq Scan` e muitas linhas descartadas | [02](docs/02-banco-explain-n-mais-1-e-pool.md) e skill `data` (índices) |
| `too many clients` no PostgreSQL | [02](docs/02-banco-explain-n-mais-1-e-pool.md) (pool e PgBouncer) |
| Mesma leitura pesada repetida | [03](docs/03-cache-http-aplicacao-e-redis.md) |
| Quanto o sistema aguenta antes de um pico | [04](docs/04-teste-de-carga-com-k6.md) |
| CPU do processo alta e banco tranquilo | [05](docs/05-profiling-por-stack.md) |
| Relatório, PDF ou e-mail trava a tela | [06](docs/06-trabalho-pesado-fora-da-requisicao.md) |
| "Preciso de servidor maior ou de mais instâncias?" | [07](docs/07-escalar-vertical-horizontal-e-replica.md) |
| Fatura crescendo mais que o uso | [08](docs/08-custo-x-desempenho.md) |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Medir primeiro | [docs/01-medir-primeiro.md](docs/01-medir-primeiro.md) | Metas, percentis, APM, log de consulta lenta |
| Banco | [docs/02-banco-explain-n-mais-1-e-pool.md](docs/02-banco-explain-n-mais-1-e-pool.md) | EXPLAIN, N+1, pool de conexões, PgBouncer |
| Cache | [docs/03-cache-http-aplicacao-e-redis.md](docs/03-cache-http-aplicacao-e-redis.md) | Cache-Control, cache-aside, Redis, invalidação |
| Teste de carga | [docs/04-teste-de-carga-com-k6.md](docs/04-teste-de-carga-com-k6.md) | Cenário, thresholds e leitura do resultado |
| Profiling | [docs/05-profiling-por-stack.md](docs/05-profiling-por-stack.md) | Node, .NET, Python e Go |
| Fora da requisição | [docs/06-trabalho-pesado-fora-da-requisicao.md](docs/06-trabalho-pesado-fora-da-requisicao.md) | Quando mover para fila e worker |
| Escalar | [docs/07-escalar-vertical-horizontal-e-replica.md](docs/07-escalar-vertical-horizontal-e-replica.md) | Vertical, horizontal, réplica de leitura |
| Custo x desempenho | [docs/08-custo-x-desempenho.md](docs/08-custo-x-desempenho.md) | Ordem de custo-benefício e conta de decisão |

## Checklist

- [ ] Meta de p95 e de erro por rota crítica escrita no `README`.
- [ ] `log_min_duration_statement` ligado em produção e `pg_stat_statements` ativo.
- [ ] Nenhuma listagem com N+1 (conferido com o log de consultas numa tela real).
- [ ] Plano (`EXPLAIN (ANALYZE, BUFFERS)`) lido nas 5 consultas que mais consomem tempo.
- [ ] Soma dos pools de todas as instâncias abaixo de `max_connections`.
- [ ] `Cache-Control` correto: estáticos com hash por um ano, dado de usuário com `private` ou `no-store`.
- [ ] Todo cache com TTL, chave com a empresa e forma de invalidar; app funciona sem o Redis.
- [ ] Tarefa que passa de 1 a 2 segundos ou depende de terceiro roda em worker.
- [ ] Teste de carga com k6 contra staging, com thresholds iguais às metas.
- [ ] Porta de depuração (`--inspect`, `pprof`) só em `127.0.0.1`.
- [ ] Alerta de custo e revisão trimestral do dimensionamento.

## Regras de uso

- **Meça antes e depois.** Toda mudança de desempenho entra com o número antes e o número depois no PR.
- **Percentil, não média.** A meta usa p95 ou p99.
- **O banco primeiro.** Na maioria dos sistemas, a lentidão está em consulta mal feita, não em falta de servidor.
- **Cache não conserta consulta ruim.** Ajuste o banco e só então cacheie.
- **Dado de uma pessoa nunca no cache público.** `private` ou `no-store`, e chave com escopo de empresa.
- **Escalar é o último passo.** Vertical antes de horizontal; réplica só para leitura que tolera atraso.
- **Teste de carga em staging, nunca em produção nem contra terceiros.**
- **Fronteiras.** Índices, paginação e transações são da `data`; Core Web Vitals e peso de página, da `user-experience`; gates no CI, da `quality`; filas, da `integrations`; servidor, proxy e provedor, da `vps`, `nginx` e `infra`.

## Quando a lista não cobre

Particionamento e sharding de banco, bancos não relacionais, profiling de Java e PHP, otimização de GPU e de processamento em lote massivo (Spark) ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial.

## Validade dos dados

Versões e comandos foram conferidos em 2026-11-25 nas fontes oficiais: k6 v2.4.0, documentação atual do PostgreSQL, Redis 8.12.0, PgBouncer 1.26.1 e dotnet-trace. Ferramentas mudam rápido; cada documento tem a linha "Verificado em".
