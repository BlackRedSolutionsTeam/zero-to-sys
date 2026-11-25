# Busca

Um documento por tópico, da decisão entre banco e motor de busca até a operação. Versões, licenças e preços foram conferidos em 2026-11-25 nas páginas oficiais.

## Escolher

| Prática | O que entrega | Doc |
|---|---|---|
| O banco basta | ILIKE, pg_trgm, tsvector | [01-quando-o-banco-basta.md](01-quando-o-banco-basta.md) |
| Meilisearch e Typesense | Busca ao digitar, facetas, tolerância a erro | [02-meilisearch-e-typesense.md](02-meilisearch-e-typesense.md) |
| Elasticsearch e OpenSearch | Escala, agregações, logs | [03-elasticsearch-e-opensearch.md](03-elasticsearch-e-opensearch.md) |

## Montar

| Prática | O que entrega | Doc |
|---|---|---|
| Sincronizar índice e banco | Eventos, reindexação, consistência | [04-sincronizar-indice-e-banco.md](04-sincronizar-indice-e-banco.md) |
| Relevância e português | Pesos, sinônimos, acentos, plural | [05-relevancia-sinonimos-acentos-e-portugues.md](05-relevancia-sinonimos-acentos-e-portugues.md) |
| Filtros, facetas e paginação | Consultas combinadas e listas grandes | [06-filtros-facetas-e-paginacao.md](06-filtros-facetas-e-paginacao.md) |

## Proteger e operar

| Prática | O que entrega | Doc |
|---|---|---|
| Multiempresa | Resultados isolados por cliente | [07-multiempresa-isolar-resultados.md](07-multiempresa-isolar-resultados.md) |
| Operar | Custo, backup, atualização | [08-operar-custo-backup-e-atualizacao.md](08-operar-custo-backup-e-atualizacao.md) |

## Por onde começar

- **Primeira busca do sistema:** 01.
- **O banco ficou lento ou a busca precisa ser ao digitar:** 02 → 04.
- **Volume enorme ou logs:** 03.
- **Resultados ruins em português:** 05.
- **Sistema com várias empresas:** 07 antes de ir para produção.
- **Índice diferente do banco:** 04.
