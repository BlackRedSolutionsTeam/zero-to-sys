# Manutenção contínua

Um documento por tópico, do calendário de suporte à rotina trimestral. Datas e opções de ferramentas foram conferidas em 2026-11-25 nas fontes oficiais.

## Saber o que vence

| Prática | O que entrega | Doc |
|---|---|---|
| Calendário de fim de suporte | Node, .NET, Python, Postgres e frameworks com data | [01-calendario-de-fim-de-suporte.md](01-calendario-de-fim-de-suporte.md) |

## Automatizar

| Prática | O que entrega | Doc |
|---|---|---|
| Atualização automática | Renovate, Dependabot e regras de merge | [02-atualizacao-automatica-de-dependencias.md](02-atualizacao-automatica-de-dependencias.md) |

## Atualizar com segurança

| Prática | O que entrega | Doc |
|---|---|---|
| Versão maior de framework | Passo a passo e testes de proteção | [03-atualizar-versao-maior-do-framework.md](03-atualizar-versao-maior-do-framework.md) |
| Postgres sem queda | pg_upgrade, replicação lógica, volta | [04-atualizar-o-postgres-sem-queda.md](04-atualizar-o-postgres-sem-queda.md) |

## Reduzir o peso

| Prática | O que entrega | Doc |
|---|---|---|
| Dívida técnica | Registro, prioridade e fatias | [05-divida-tecnica.md](05-divida-tecnica.md) |
| Código morto | Achar e remover código e pacotes | [06-codigo-morto-e-dependencias-sem-uso.md](06-codigo-morto-e-dependencias-sem-uso.md) |

## Manter o hábito

| Prática | O que entrega | Doc |
|---|---|---|
| Rotina trimestral | Checklist de saúde do projeto | [07-rotina-trimestral-de-saude.md](07-rotina-trimestral-de-saude.md) |

## Por onde começar

- **Projeto recém-assumido:** 01, depois 02.
- **Alguma versão saiu de suporte:** 01 e depois 03 (framework, runtime) ou 04 (Postgres).
- **Chegam muitos PRs de atualização:** 02.
- **Projeto lento para mexer:** 05 e 06.
- **Quer um hábito:** 07.
