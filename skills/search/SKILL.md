---
name: search
description: 'Escolhe e monta a busca textual, do Postgres (ILIKE, trigram, full-text) ao Meilisearch, Typesense e OpenSearch, com sincronização, relevância em português e isolamento por empresa. Use quando o produto precisa de busca com filtros ou quando pedirem "busca" ou "Meilisearch".'
---

# search

Guia para colocar uma busca no sistema sem comprar complexidade antes da hora. A maioria dos produtos começa bem com o próprio PostgreSQL; um motor de busca separado entra quando a busca vira parte central da experiência (digitou, apareceu, tolerou erro, filtrou) ou quando o volume pede. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e comandos prontos.

## Como usar esta skill

1. **Comece pelo banco.** Se o sistema já tem PostgreSQL e a busca é "achar um cliente pelo nome", `ILIKE` com trigram resolve ([doc 01](docs/01-quando-o-banco-basta.md)).
2. **Suba para Meilisearch ou Typesense** quando precisar de busca ao digitar, tolerância a erros, facetas e relevância boa sem ajuste manual ([doc 02](docs/02-meilisearch-e-typesense.md)).
3. **Só use Elasticsearch ou OpenSearch** com muito volume, análise de logs, agregações pesadas ou time que já os opera ([doc 03](docs/03-elasticsearch-e-opensearch.md)).
4. **Se escolheu um motor separado, planeje a sincronização** antes da primeira linha de código ([doc 04](docs/04-sincronizar-indice-e-banco.md)): o banco é a fonte da verdade, o índice é uma cópia.
5. **Ajuste a relevância e o português** ([doc 05](docs/05-relevancia-sinonimos-acentos-e-portugues.md)) e **desenhe filtros, facetas e paginação** ([doc 06](docs/06-filtros-facetas-e-paginacao.md)).
6. **Em sistema multiempresa, isole os resultados** ([doc 07](docs/07-multiempresa-isolar-resultados.md)) antes de ir para produção.
7. **Defina como operar** ([doc 08](docs/08-operar-custo-backup-e-atualizacao.md)): custo, backup, atualização.

## Qual opção por perfil

| Perfil | Opção | Por quê |
|---|---|---|
| Cadastro com poucos milhares de linhas, busca por nome | `ILIKE` + `pg_trgm` no PostgreSQL | Zero serviço novo, índice no próprio banco |
| Texto longo (artigos, documentos) com português | Full-text do PostgreSQL (`tsvector`) | Stemming, ranking e destaque sem outro serviço |
| Busca ao digitar com tolerância a erro e facetas | Meilisearch | Configuração simples, bom padrão de relevância |
| Busca com muitos filtros, alto volume e cluster | Typesense | Tudo em memória, rápido, chaves com escopo |
| Logs, métricas ou bilhões de documentos | Elasticsearch ou OpenSearch | Agregações e escala horizontal maduras |
| Time pequeno que não quer operar servidor | Serviço gerenciado (Meilisearch Cloud, Typesense Cloud, Elastic Cloud) | Paga mais, opera menos |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| O banco basta | [docs/01-quando-o-banco-basta.md](docs/01-quando-o-banco-basta.md) | ILIKE, pg_trgm, tsvector, quando migrar |
| Meilisearch e Typesense | [docs/02-meilisearch-e-typesense.md](docs/02-meilisearch-e-typesense.md) | Quando entram, comparação, subir e indexar |
| Elasticsearch e OpenSearch | [docs/03-elasticsearch-e-opensearch.md](docs/03-elasticsearch-e-opensearch.md) | Quando vale a complexidade e licenças |
| Sincronizar | [docs/04-sincronizar-indice-e-banco.md](docs/04-sincronizar-indice-e-banco.md) | Eventos, reindexação, consistência |
| Relevância e português | [docs/05-relevancia-sinonimos-acentos-e-portugues.md](docs/05-relevancia-sinonimos-acentos-e-portugues.md) | Pesos, sinônimos, acentos, plural |
| Filtros e paginação | [docs/06-filtros-facetas-e-paginacao.md](docs/06-filtros-facetas-e-paginacao.md) | Facetas, filtros e paginação sem surpresa |
| Multiempresa | [docs/07-multiempresa-isolar-resultados.md](docs/07-multiempresa-isolar-resultados.md) | Filtro obrigatório, tokens com escopo, índice por cliente |
| Operar | [docs/08-operar-custo-backup-e-atualizacao.md](docs/08-operar-custo-backup-e-atualizacao.md) | Memória, custo, backup, atualização |

## Checklist

- [ ] A escolha do motor está justificada por uma necessidade que o PostgreSQL não atende.
- [ ] O banco é a fonte da verdade e o índice pode ser reconstruído do zero com um comando.
- [ ] Toda escrita que importa para a busca gera um evento ou job de indexação (skill `integrations`, doc 05).
- [ ] Remoções no banco removem do índice.
- [ ] Busca sem acento, com plural e com erro de digitação testada com exemplos reais em português.
- [ ] Filtro por empresa aplicado no servidor ou em token com escopo; chave de administração nunca no navegador.
- [ ] Paginação com limite máximo e sem mostrar contagem exata onde o motor só estima.
- [ ] Índice com backup ou procedimento de reindexação testado e com tempo medido.
- [ ] Memória e disco do serviço monitorados (skill `infra`, doc 10).
- [ ] Versão do motor anotada e atualização planejada.

## Regras de uso

- **Banco primeiro.** Motor separado é mais um serviço para sincronizar, proteger, monitorar e pagar.
- **O índice é cópia, não fonte.** Nunca grave nele um dado que não exista no banco.
- **Medir antes de trocar.** Rode `EXPLAIN ANALYZE` (skill `data`, doc 08) antes de concluir que o banco não aguenta.
- **Isolamento no servidor.** Nenhum resultado de outra empresa pode depender de o front-end lembrar de filtrar.
- **Preço e versão só conferidos.** Cite a data da conferência; planos e limites mudam.
- **Fronteiras.** Índices comuns e multiempresa no banco são da `data`; filas e jobs da `integrations`; hospedagem da `infra`; autorização e vazamento entre empresas da `security`.

## Quando a lista não cobre

Busca semântica e por vetores (embeddings, RAG), busca geográfica avançada, busca em imagens e relevância aprendida (learning to rank) ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial do motor escolhido.

## Validade dos dados

Versões, licenças e preços foram conferidos em 2026-11-25 nas páginas oficiais e nos repositórios. Cada documento tem a linha "Verificado em" e diz o que não foi possível conferir.
