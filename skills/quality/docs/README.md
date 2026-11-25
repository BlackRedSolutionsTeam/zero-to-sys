# Qualidade

Um documento por prática, explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com configuração pronta para copiar. O fio que liga todos: cada critério de aceite da skill `product` vira ao menos um teste, e um item só fecha com a definição de pronto. Comandos e versões foram conferidos em 2026-11-24.

## Estratégia

| Prática | O que entrega | Doc |
|---|---|---|
| Pirâmide de testes | Em que camada testar cada critério | [01-piramide-de-testes.md](01-piramide-de-testes.md) |

## Camadas

| Prática | O que entrega | Doc |
|---|---|---|
| Testes de unidade | Regras de negócio provadas sem banco nem rede | [02-testes-de-unidade.md](02-testes-de-unidade.md) |
| Integração com banco | Rotas e serviços testados com Postgres real | [03-testes-de-integracao-com-banco.md](03-testes-de-integracao-com-banco.md) |
| API e contrato | Status, erros, permissões e contrato com o front | [04-testes-de-api-e-contrato.md](04-testes-de-api-e-contrato.md) |
| Ponta a ponta | Fluxos principais no navegador, no CI e em staging | [05-ponta-a-ponta-com-playwright.md](05-ponta-a-ponta-com-playwright.md) |
| Acessibilidade e desempenho | Problemas de acessibilidade e lentidão pegos no PR | [06-acessibilidade-e-desempenho-automaticos.md](06-acessibilidade-e-desempenho-automaticos.md) |

## Fechar o item

| Prática | O que entrega | Doc |
|---|---|---|
| Quality gates no CI | PR que não passa se quebrar algo | [07-quality-gates-no-ci.md](07-quality-gates-no-ci.md) |
| Definição de pronto | Checklist único para todo item | [08-definition-of-done.md](08-definition-of-done.md) |
| Verificação pelo agente | Evidência do que foi feito, não só "funcionou" | [09-verificacao-pelo-agente.md](09-verificacao-pelo-agente.md) |

## Por onde começar

- **Projeto novo:** 01 → 07 (CI desde o primeiro PR) → 08; depois a camada de cada item.
- **Funcionalidade nova:** 01 para escolher as camadas, o doc de cada camada e 08 para fechar.
- **Projeto sem nenhum teste:** 03 primeiro (integração dá mais confiança por teste), depois 05 no fluxo principal e 07.
- **O CI está lento ou instável:** 07 e, se o problema for ponta a ponta, 05.
- **O agente diz que terminou mas quebrou algo:** 09 e 08.
