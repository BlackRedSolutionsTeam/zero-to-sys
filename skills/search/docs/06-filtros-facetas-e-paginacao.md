# Filtros, facetas e paginação

> Filtre pelo que o usuário já escolheu, mostre contagens por categoria (facetas) e pagine sem prometer um total exato que o motor não sabe.

| | |
|---|---|
| **Referência** | https://www.postgresql.org/docs/current/queries-limit.html; documentação de filtros e facetas do Meilisearch e do Typesense; documentação de paginação (`search_after`) do Elasticsearch e do OpenSearch |
| **Categoria** | Busca |
| **Tipo** | Prática de consulta |
| **Vale para** | PostgreSQL, Meilisearch, Typesense, Elasticsearch e OpenSearch |
| **Verificado em** | 2026-11-25 |

## O que é

- **Filtro:** restringe o conjunto (categoria = "Roupas", preço entre 50 e 100).
- **Faceta:** mostra, ao lado da busca, quantos resultados existem em cada valor ("Roupas (120)", "Calçados (45)"), já respeitando a busca atual.
- **Paginação:** devolver o resultado em pedaços. Em motor de busca, o total costuma ser uma **estimativa**.

## Por que usar

- **Quem busca refina:** busca de "camisa" e depois filtra por tamanho e preço.
- **Listas curtas e rápidas:** pedaços pequenos mantêm a resposta rápida.
- **Contagem de facetas** mostra quais filtros ainda têm resultado, evitando o clique que dá "nada encontrado".

## Quando usar

- Catálogos, listas de cadastros com várias colunas filtráveis, bases de documentos com tipo, ano e autor.
- Qualquer busca que devolva mais de uma tela de resultados.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Filtrar por categoria, tag e ano |
| MVP de SaaS | ✅ Ótimo | Filtro por status e responsável, paginação simples |
| SaaS em crescimento | ✅ Ótimo | Facetas e rolagem infinita |
| Sistema interno/corporativo | ✅ Ótimo | Tabelas com muitos filtros |
| API/integração | ✅ Ótimo | Paginação por cursor para quem varre tudo |
| App mobile com backend | ✅ Ótimo | Rolagem infinita e filtros em folha deslizante |
| Total exato em lista gigante | ❌ Evite | Contagem exata é cara; mostre "mais de 1.000" |

## Quando é bom

- **Facetas calculadas pelo motor** respeitam a busca e os filtros atuais sem consulta extra.
- **Filtro antes da busca** reduz o conjunto e acelera a ordenação.
- **Cursor** (PostgreSQL, `search_after` no Elasticsearch e OpenSearch) mantém o custo estável em páginas profundas.

## Quando é ruim

- **Campos precisam ser declarados como filtráveis:** no Meilisearch, em `filterableAttributes`; no Typesense, `facet: true` no esquema; trocar isso depois reindexa.
- **Limite de páginas profundas:** no Meilisearch o padrão alcança até 1.000 resultados (`maxTotalHits`, confirmado na v1.58.0); no OpenSearch 3.10.1 `from + size` é limitado a 10.000 por padrão (`index.max_result_window`, confirmado: `from=9990&size=20` devolveu "Result window is too large"); o Elasticsearch tem o mesmo padrão segundo sua documentação, que não foi executada aqui. Para varrer tudo, use cursor ou exportação.
- **Facetas demais** deixam a consulta lenta e a tela confusa; limite a quatro ou cinco.
- **Total exato e contagem de página** ("página 3 de 80") pedem cálculo caro ou inexistente; prefira "carregar mais".
- **Filtro montado concatenando texto** com entrada do usuário é injeção; escape e valide os valores.

## Como começar

PostgreSQL, filtro com cursor (skill `data`, doc 08, para a explicação):

```sql
select id, name, created_at
from product
where company_id = $1
  and category = $2
  and (created_at, id) < ($3, $4)
order by created_at desc, id desc
limit 20;
```

Meilisearch, declarar atributos filtráveis e ordenáveis, e depois buscar com filtro e facetas:

```bash
curl -X PATCH "http://127.0.0.1:7700/indexes/products/settings" \
  -H "Authorization: Bearer $MEILI_MASTER_KEY" \
  -H "Content-Type: application/json" \
  --data '{"filterableAttributes":["company_id","category","price"],"sortableAttributes":["price"]}'

curl -X POST "http://127.0.0.1:7700/indexes/products/search" \
  -H "Authorization: Bearer $MEILI_SEARCH_KEY" \
  -H "Content-Type: application/json" \
  --data '{"q":"camisa","filter":"company_id = 10 AND price 50 TO 100","facets":["category"],"page":1,"hitsPerPage":20}'
```

Testado no Meilisearch v1.58.0 em 2026-11-25, com 1.500 documentos: com `page` e `hitsPerPage` a resposta traz `totalHits` e `totalPages`; com `offset` e `limit` traz `estimatedTotalHits`. O `maxTotalHits` (padrão 1000) limita quantos resultados dá para alcançar, não o número informado: o total veio como 1500, mas `page=51` com `hitsPerPage=20` e `offset=1100` vieram vazios, e `limit=5000` devolveu só 1000 itens. Para alcançar mais, suba o `maxTotalHits` em `PATCH /indexes/<índice>/settings/pagination` (com 5000, `limit=5000` devolveu os 1500). Por isso a tela não deve oferecer páginas além do que o servidor entrega.

Typesense, facetas, filtro e paginação (testado na 30.2 em 2026-11-25; `per_page` tem máximo de 250, e `per_page=251` devolve o erro "Only upto 250 hits can be fetched per page", como diz a documentação; com `group_by` o limite vale para grupos):

```bash
curl -G "http://127.0.0.1:8108/collections/products/documents/search" \
  -H "X-TYPESENSE-API-KEY: $TYPESENSE_SEARCH_KEY" \
  --data-urlencode "q=camisa" \
  --data-urlencode "query_by=name" \
  --data-urlencode "filter_by=company_id:=10 && price:[50..100]" \
  --data-urlencode "facet_by=category" \
  --data-urlencode "page=1" \
  --data-urlencode "per_page=20"
```

Elasticsearch e OpenSearch, cursor com `search_after` (ordene por um campo e um desempate único):

```bash
curl -X POST "https://localhost:9200/products/_search" -u "admin:$OPENSEARCH_PASSWORD" \
  -H "Content-Type: application/json" \
  --data '{
    "size": 20,
    "query": { "bool": { "filter": [{ "term": { "company_id": "10" } }] } },
    "sort": [{ "created_at": "desc" }, { "id": "desc" }],
    "search_after": ["2026-11-20T10:00:00Z", "abc123"],
    "aggs": { "categorias": { "terms": { "field": "category" } } }
  }'
```

Regras para a tela: limite máximo de itens por página no servidor (por exemplo 50), ignore `page` ou `limit` negativos, e mostre "carregar mais" quando o total é estimativa.

## Combina com / alternativas

- [Índices e paginação](../../data/docs/08-indices-e-paginacao.md): cursor no banco.
- [Relevância e português](05-relevancia-sinonimos-acentos-e-portugues.md): ordenação por relevância.
- [Multiempresa](07-multiempresa-isolar-resultados.md): o filtro por empresa é obrigatório.
- [Rate limit](../../security/docs/06-rate-limit.md): limitar buscas por usuário.

## Decisão rápida

- **Use se:** a busca devolve mais de uma tela ou o usuário refina por categoria, preço ou status.
- **Evite se:** a lista é curta e fixa; um filtro simples no banco basta.
