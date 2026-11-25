# Relevância, sinônimos, acentos e português

> Faça "acao" achar "ação", "carros" achar "carro" e "pc" achar "computador": ordem dos resultados, acentos, plural e sinônimos configurados no banco ou no motor.

| | |
|---|---|
| **Referência** | https://www.postgresql.org/docs/current/textsearch-controls.html, https://www.postgresql.org/docs/current/unaccent.html e https://www.elastic.co/docs/reference/text-analysis/analysis-lang-analyzer; documentação de relevância do Meilisearch e do Typesense |
| **Categoria** | Busca |
| **Tipo** | Prática de configuração |
| **Vale para** | PostgreSQL, Meilisearch, Typesense, Elasticsearch e OpenSearch |
| **Verificado em** | 2026-11-25 |

## O que é

**Relevância** é a ordem em que os resultados aparecem. Quatro peças a ajustar:

- **Pesos por campo:** achar no título vale mais que achar no corpo.
- **Acentos e maiúsculas:** "Ação", "acao" e "AÇÃO" devem dar o mesmo resultado.
- **Radical (stemming) e plural:** "advogados" encontra "advogado".
- **Sinônimos:** "celular" encontra "smartphone".

## Por que usar

- **Quem busca não sabe como o dado foi escrito:** teclado de celular sem acento é comum no Brasil.
- **Resultado certo no topo** evita a pessoa rolar a lista.
- **Menos chamados** do tipo "procurei e não achei, mas está cadastrado".

## Quando usar

- Antes de lançar a busca: monte uma lista de 20 a 30 consultas reais e o resultado esperado de cada.
- Depois de reclamação de "não acha": acrescente o caso à lista e ajuste.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Pesos título e corpo, português e destaque |
| MVP de SaaS | ✅ Ótimo | Acento e plural resolvem a maior parte |
| SaaS em crescimento | ✅ Ótimo | Sinônimos do domínio e lista de consultas de teste |
| Sistema interno/corporativo | ✅ Ótimo | Siglas e códigos da empresa viram sinônimos |
| API/integração | 🟡 Serve | Quem consome a API costuma buscar por código exato |
| App mobile com backend | ✅ Ótimo | Sem acento e com erro de digitação são a regra |
| Busca por código ou identificador exato | ❌ Evite | Stemming atrapalha; use igualdade ou prefixo |

## Quando é bom

- **PostgreSQL:** `unaccent`, configuração `portuguese`, `setweight` e `ts_rank_cd`.
- **Meilisearch e Typesense:** tolerância a erro e ranking por padrão; sinônimos por configuração.
- **Elasticsearch e OpenSearch:** analisador `portuguese` e `asciifolding` combináveis.

## Quando é ruim

- **Stemming agressivo junta palavras diferentes** ("copa" e "copo" em alguns stemmers); teste com o vocabulário do seu domínio.
- **Sinônimos demais** poluem resultados; comece com poucos e meça.
- **Mudar análise exige reindexar** (doc 04) em Elasticsearch e OpenSearch.
- **Nomes próprios e códigos** não devem passar por stemming nem sinônimo; use um campo separado sem análise.
- **A função `unaccent` não é imutável:** o PostgreSQL recusa-a em expressão de índice sem um invólucro (abaixo).

## Como começar

PostgreSQL, busca sem acento com índice. A função `unaccent` precisa de um invólucro `IMMUTABLE`; é uma afirmação sua, então se trocar o arquivo de regras, recrie o índice. Qualifique o esquema da função e do dicionário:

```sql
create extension if not exists unaccent;

create function f_unaccent(text) returns text
language sql immutable parallel safe strict
as $$ select public.unaccent('public.unaccent', $1) $$;

create index article_title_search_idx on article
using gin (to_tsvector('simple', f_unaccent(title)));

select id, title
from article
where to_tsvector('simple', f_unaccent(title)) @@ websearch_to_tsquery('simple', f_unaccent($1));
```

A consulta usa a mesma expressão do índice, senão o índice não é usado. A configuração `simple` não faz stemming; para acento e plural juntos, crie uma configuração própria baseada em `portuguese` com o dicionário `unaccent` antes do stemmer:

```sql
create text search configuration pt_unaccent (copy = portuguese);
alter text search configuration pt_unaccent
  alter mapping for hword, hword_part, word
  with unaccent, portuguese_stem;

select to_tsvector('pt_unaccent', 'Ação dos advogados') @@ websearch_to_tsquery('pt_unaccent', 'acao advogado');
```

Pesos por campo e ordenação com densidade de cobertura (pesos padrão `{D, C, B, A}` = `{0.1, 0.2, 0.4, 1.0}`):

```sql
select id, title,
  ts_rank_cd('{0.1, 0.2, 0.4, 1.0}', search, query, 32) as rank
from article, websearch_to_tsquery('pt_unaccent', $1) query
where search @@ query
order by rank desc
limit 20;
```

Meilisearch, sinônimos pela API de configurações (palavras trocadas nos dois sentidos quando listadas uma para a outra):

```bash
curl -X PUT "http://127.0.0.1:7700/indexes/products/settings/synonyms" \
  -H "Authorization: Bearer $MEILI_MASTER_KEY" \
  -H "Content-Type: application/json" \
  --data '{"celular":["smartphone","telefone"],"smartphone":["celular"],"telefone":["celular"]}'
```

Typesense: o servidor aceita regras de sinônimos por coleção e `typo_tolerance` por parâmetro de busca; confirme o formato na documentação da versão instalada, pois ele mudou entre versões maiores.

Elasticsearch e OpenSearch: use o analisador do [doc 03](03-elasticsearch-e-opensearch.md) (`asciifolding`, lista de palavras comuns e `light_portuguese`) e um filtro `synonym` com a lista no próprio índice.

Teste de regressão: guarde as consultas reais num arquivo e rode a cada mudança de configuração.

```ts
const cases = [
  { query: 'acao', expected: 'Ação civil' },
  { query: 'advogados', expected: 'Advogado trabalhista' },
]

for (const item of cases) {
  const result = await search(item.query)
  if (!result.some((r) => r.title === item.expected)) {
    throw new Error(`Sem resultado para ${item.query}`)
  }
}
```

## Combina com / alternativas

- [O banco basta](01-quando-o-banco-basta.md): extensões e pesos no PostgreSQL.
- [Meilisearch e Typesense](02-meilisearch-e-typesense.md): relevância pronta.
- [Elasticsearch e OpenSearch](03-elasticsearch-e-opensearch.md): analisador customizado.
- [Sincronizar índice e banco](04-sincronizar-indice-e-banco.md): reindexar depois de mudar a análise.

## Decisão rápida

- **Use se:** a busca será usada por gente que digita sem acento, no plural e com erro.
- **Evite se:** o campo é código ou identificador; busque por igualdade ou prefixo.
