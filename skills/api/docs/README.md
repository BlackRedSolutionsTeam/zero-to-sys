# API

Um documento por prática, explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com exemplos prontos do agendamento de uma clínica. O fio que liga todos: um contrato único e previsível, gerado do código e consumido por cliente tipado. RFCs e bibliotecas foram conferidos em 2026-11-24.

## Desenhar o contrato

| Prática | O que entrega | Doc |
|---|---|---|
| Estilo | REST, RPC tipado ou GraphQL, conforme quem consome | [01-rest-rpc-ou-graphql.md](01-rest-rpc-ou-graphql.md) |
| Rotas, verbos e status | Nomes e códigos HTTP consistentes | [02-rotas-verbos-e-status.md](02-rotas-verbos-e-status.md) |
| Formato de erro | Um erro único, com campo e código estável | [03-formato-de-erro.md](03-formato-de-erro.md) |
| Paginação e filtros | Listas com limite, cursor, filtro e ordem | [04-paginacao-e-filtros.md](04-paginacao-e-filtros.md) |

## Evoluir sem quebrar

| Prática | O que entrega | Doc |
|---|---|---|
| Versionamento | Regra de quando versionar e como deprecar | [05-versionamento.md](05-versionamento.md) |
| Idempotência e retries | Operação segura contra repetição | [06-idempotencia-e-retries.md](06-idempotencia-e-retries.md) |

## Documentar e consumir

| Prática | O que entrega | Doc |
|---|---|---|
| OpenAPI e documentação | Spec gerada do código e página navegável | [07-openapi-e-documentacao.md](07-openapi-e-documentacao.md) |
| Cliente gerado no front | Tipos e chamadas geradas, erro de tipo se o contrato quebrar | [08-cliente-gerado-no-front.md](08-cliente-gerado-no-front.md) |

## Por onde começar

- **API nova:** 01 → 02 → 03 → 04 antes da primeira rota; depois 07 e 08.
- **Rota nova numa API que já existe:** 02, o checklist do [SKILL.md](../SKILL.md) e o 08.
- **O front quebra quando o back muda:** 08 e 05, e os testes de contrato da skill `quality`.
- **Cliente clicou duas vezes e duplicou o agendamento:** 06.
- **Erros chegam em formatos diferentes:** 03.
- **A lista está lenta ou trava:** 04 e o doc de índices da skill `data`.
