# Produto

Um documento por prática, explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com modelos prontos para copiar. As práticas seguem a ordem em que são usadas: entender, cortar, desenhar o fluxo, escrever as regras, quebrar em histórias, ordenar e registrar. As referências foram conferidas em 2026-11-24.

## Entender e cortar

| Prática | O que entrega | Doc |
|---|---|---|
| Entrevista com o cliente | Problema, público, funcionalidades e restrições, fechados num resumo aprovado | [01-entrevista-com-o-cliente.md](01-entrevista-com-o-cliente.md) |
| Escopo do MVP | Quadro Dentro / Fora / Depois | [02-escopo-do-mvp.md](02-escopo-do-mvp.md) |

## Descrever o sistema

| Prática | O que entrega | Doc |
|---|---|---|
| Fluxos e jornadas | Fluxo principal passo a passo, caminhos de erro, diagrama em Mermaid | [03-fluxos-e-jornadas.md](03-fluxos-e-jornadas.md) |
| Regras de negócio | Tabela de regras com id e máquina de estados | [05-regras-de-negocio.md](05-regras-de-negocio.md) |

## Planejar a construção

| Prática | O que entrega | Doc |
|---|---|---|
| Histórias e critérios de aceite | Itens com Dado / Quando / Então verificáveis | [04-historias-e-criterios-de-aceite.md](04-historias-e-criterios-de-aceite.md) |
| Backlog e ordem de construção | `BACKLOG.md` em fatias verticais, com dependências | [06-backlog-e-ordem-de-construcao.md](06-backlog-e-ordem-de-construcao.md) |
| Onde registrar | O que vai no `README`, no `BACKLOG.md`, nas issues e no `CLAUDE.md` | [07-onde-registrar.md](07-onde-registrar.md) |

## Por onde começar

- **Sistema novo:** 01 → 02 → 03 → 05 → 04 → 06 → 07, nessa ordem.
- **Funcionalidade nova num sistema que já existe:** 03 → 05 → 04, e acrescente o item no backlog (06).
- **O cliente mandou uma lista enorme de desejos:** 02 primeiro, para cortar; depois o resto.
- **O agente não sabe quando um item terminou:** 04, e reescreva os critérios de aceite.
- **Ninguém sabe o que já foi decidido:** 07, e junte tudo no repositório.
