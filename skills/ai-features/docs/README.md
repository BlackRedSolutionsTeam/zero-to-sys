# IA no produto

Um documento por tópico, da decisão de usar IA até a interface. Preços, limites e versões foram conferidos em 2026-11-25 nas páginas oficiais.

## Decidir

| Prática | O que entrega | Doc |
|---|---|---|
| Quando IA vale a pena | LLM ou regra comum | [01-quando-ia-vale-a-pena.md](01-quando-ia-vale-a-pena.md) |
| Provedor e modelo | Modelos Claude, preço, limites, privacidade | [02-provedor-e-modelo.md](02-provedor-e-modelo.md) |

## Construir

| Prática | O que entrega | Doc |
|---|---|---|
| Prompts e saída estruturada | JSON Schema, Zod, validação | [03-prompts-saida-estruturada-e-validacao.md](03-prompts-saida-estruturada-e-validacao.md) |
| RAG | Chunking, embeddings, pgvector | [04-rag-chunking-embeddings-pgvector.md](04-rag-chunking-embeddings-pgvector.md) |
| Ferramentas e agentes | Tool use, laço, confirmação humana | [05-ferramentas-e-agentes-no-produto.md](05-ferramentas-e-agentes-no-produto.md) |

## Garantir

| Prática | O que entrega | Doc |
|---|---|---|
| Avaliação | Conjunto de testes e regressão de prompt | [06-avaliacao-e-regressao-de-prompt.md](06-avaliacao-e-regressao-de-prompt.md) |
| Guardrails e LGPD | Injeção de prompt, dados pessoais | [07-guardrails-injecao-e-lgpd.md](07-guardrails-injecao-e-lgpd.md) |

## Operar

| Prática | O que entrega | Doc |
|---|---|---|
| Custo e fallback | Cache, lote, orçamento, erros | [08-custo-cache-limites-e-fallback.md](08-custo-cache-limites-e-fallback.md) |
| Streaming e filas | SSE, tarefas longas, timeouts | [09-streaming-filas-e-timeouts.md](09-streaming-filas-e-timeouts.md) |

## Por onde começar

- **Vai pôr IA pela primeira vez:** 01 → 02 → 03 → 06 → 07 → 08.
- **Responder sobre documentos:** 04, depois 06.
- **Assistente que age no sistema:** 05 e 07.
- **Chat na tela:** 09.
- **A conta de IA subiu:** 08.
