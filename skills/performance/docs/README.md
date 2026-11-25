# Desempenho e escala

Um documento por tópico, de medir até decidir quanto gastar. Versões, flags e comandos foram conferidos em 2026-11-25 nas fontes oficiais (k6 v2.4.0, PostgreSQL documentação atual, Redis 8.12.0, PgBouncer 1.26.1).

## Medir

| Prática | O que entrega | Doc |
|---|---|---|
| Medir primeiro | Metas por rota, percentis, APM, log de consulta lenta | [01-medir-primeiro.md](01-medir-primeiro.md) |
| Teste de carga com k6 | Cenário, thresholds e leitura do resultado | [04-teste-de-carga-com-k6.md](04-teste-de-carga-com-k6.md) |
| Profiling por stack | Node, .NET, Python e Go | [05-profiling-por-stack.md](05-profiling-por-stack.md) |

## Otimizar

| Prática | O que entrega | Doc |
|---|---|---|
| Banco | EXPLAIN, N+1, pool, PgBouncer | [02-banco-explain-n-mais-1-e-pool.md](02-banco-explain-n-mais-1-e-pool.md) |
| Cache | HTTP, aplicação, Redis, invalidação | [03-cache-http-aplicacao-e-redis.md](03-cache-http-aplicacao-e-redis.md) |
| Trabalho pesado fora da requisição | Quando mover para fila e worker | [06-trabalho-pesado-fora-da-requisicao.md](06-trabalho-pesado-fora-da-requisicao.md) |

## Escalar e decidir

| Prática | O que entrega | Doc |
|---|---|---|
| Escalar | Vertical, horizontal, réplica de leitura | [07-escalar-vertical-horizontal-e-replica.md](07-escalar-vertical-horizontal-e-replica.md) |
| Custo x desempenho | Ordem de custo-benefício e conta de decisão | [08-custo-x-desempenho.md](08-custo-x-desempenho.md) |

## Por onde começar

- **Está lento e não sabe onde:** 01 → 02.
- **Vai lançar ou tem pico chegando:** 01 → 04 → 07.
- **CPU do app alta, banco tranquilo:** 05.
- **Mesma leitura repetida demais:** 03.
- **Tarefa que demora trava a tela:** 06.
- **Vai subir o plano ou contratar serviço:** 07 → 08.
