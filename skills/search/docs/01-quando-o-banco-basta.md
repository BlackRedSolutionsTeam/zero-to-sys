# Quando o banco basta

> Antes de subir um motor de busca, use o que o PostgreSQL já tem: `ILIKE` com índice trigram para achar por pedaço do nome e full-text (`tsvector`) para texto longo em português.

| | |
|---|---|
| **Referência** | https://www.postgresql.org/docs/current/pgtrgm.html, https://www.postgresql.org/docs/current/textsearch.html e https://www.postgresql.org/docs/current/unaccent.html |
| **Categoria** | Busca |
| **Tipo** | Prática de consulta |
| **Vale para** | PostgreSQL com qualquer ORM (consulta em SQL cru ou view) |
| **Verificado em** | 2026-11-25 |

## O que é

Três níveis, do mais simples ao mais completo:

- **`ILIKE '%texto%'`:** acha o pedaço em qualquer posição, sem diferenciar maiúsculas. Sem índice especial, lê a tabela inteira.
- **`pg_trgm` (trigram):** quebra o texto em trios de letras e deixa o `ILIKE` e a busca por semelhança usarem índice. Tolera erro de digitação leve.
- **Full-text (`tsvector` e `tsquery`):** entende palavras, remove palavras comuns, reduz ao radical (stemming) e ordena por relevância. Serve para texto longo.

## Por que usar

- **Nenhum serviço novo:** sem sincronizar, hospedar ou pagar outro sistema.
- **Consistência total:** a busca vê o dado na mesma transação em que ele foi gravado.
- **Mesmas permissões e multiempresa** do restante do banco (skill `data`, doc 06).

## Quando usar

- Cadastros (clientes, produtos, pacientes) com busca por nome, e-mail ou código.
- Até algumas centenas de milhares de linhas por tabela, confirmado com `EXPLAIN ANALYZE`.
- Busca por texto longo simples (artigos, descrições) sem exigir autocomplete instantâneo.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Full-text em português cobre blog e documentação |
| MVP de SaaS | ✅ Ótimo | Trigram resolve a busca de cadastros sem outro serviço |
| SaaS em crescimento | 🟡 Serve | Funciona até a busca virar o centro da experiência |
| Sistema interno/corporativo | ✅ Ótimo | Poucos usuários, dados já no banco |
| API/integração | ✅ Ótimo | Filtro e ordenação normais, sem serviço extra |
| App mobile com backend | 🟡 Serve | Autocomplete a cada tecla pede um motor próprio |
| Catálogo grande com facetas e correção de erro | ❌ Evite | Facetas e relevância ajustada dão mais trabalho no SQL que num motor |

## Quando é bom

- **Trigram** acelera `LIKE '%foo%'` e `ILIKE`, que um B-tree comum não acelera.
- **`websearch_to_tsquery`** aceita o que a pessoa digita (aspas, `or`, `-`) sem erro de sintaxe, então pode receber texto cru do usuário.
- **`setweight`** dá peso maior ao título que ao corpo.
- **`ts_headline`** devolve o trecho com o termo destacado.

## Quando é ruim

- **`ILIKE '%x%'` sem índice trigram** faz leitura da tabela inteira e fica lento com o crescimento.
- **Trigram não entende palavra:** "carro" não acha "carros" por radical; acha por semelhança de letras, com resultados menos previsíveis.
- **Full-text não tolera erro de digitação:** "advogdo" não acha "advogado".
- **Acentos:** o full-text com configuração `portuguese` reduz ao radical, mas não remove acento; "ação" e "acao" são tratados como diferentes sem a extensão `unaccent` (doc 05).
- **`ts_headline` e `ts_rank` leem o texto de cada resultado** e ficam lentos em listas grandes; aplique só nas linhas já filtradas e paginadas.
- **`ts_headline` não é seguro para HTML:** sanitize antes de exibir.

## Como começar

Extensões (ambas "trusted" na documentação: quem tem `CREATE` no banco instala):

```sql
create extension if not exists pg_trgm;
create extension if not exists unaccent;
```

Busca por pedaço do nome, com índice GIN trigram:

```sql
create index patient_name_trgm_idx on patient using gin (name gin_trgm_ops);

select id, name
from patient
where company_id = $1 and name ilike '%' || $2 || '%'
order by name
limit 20;
```

Busca por semelhança (tolera erro de digitação leve). O operador `%` usa o limite `pg_trgm.similarity_threshold`, padrão 0.3:

```sql
select id, name, similarity(name, $2) as score
from patient
where company_id = $1 and name % $2
order by score desc
limit 20;
```

Full-text em português com coluna gerada e índice GIN, pesos A para o título e B para o corpo:

```sql
alter table article add column search tsvector generated always as (
  setweight(to_tsvector('portuguese', coalesce(title, '')), 'A') ||
  setweight(to_tsvector('portuguese', coalesce(body, '')), 'B')
) stored;

create index article_search_idx on article using gin (search);

select id, title, ts_rank_cd(search, query) as rank
from article, websearch_to_tsquery('portuguese', $1) query
where search @@ query
order by rank desc
limit 20;
```

Trecho com destaque, só para as linhas já escolhidas:

```sql
select ts_headline('portuguese', body, websearch_to_tsquery('portuguese', $1),
  'MaxWords=30, MinWords=15, StartSel=<mark>, StopSel=</mark>')
from article
where id = any($2);
```

Para busca sem acento com índice, use a função `IMMUTABLE` do doc 05.

Quando migrar: se `EXPLAIN ANALYZE` mostra a busca acima de algumas centenas de milissegundos com índice usado, se a equipe pede autocomplete, facetas ou tolerância a erro, passe ao [doc 02](02-meilisearch-e-typesense.md).

## Combina com / alternativas

- [Índices e paginação](../../data/docs/08-indices-e-paginacao.md): `EXPLAIN ANALYZE`, B-tree e cursor.
- [Multiempresa](../../data/docs/06-multiempresa.md): `company_id` em toda consulta.
- [Relevância e português](05-relevancia-sinonimos-acentos-e-portugues.md): acentos e sinônimos no próprio banco.
- [Meilisearch e Typesense](02-meilisearch-e-typesense.md): quando o banco não basta.

## Decisão rápida

- **Use se:** os dados já estão no PostgreSQL e a busca é por nome, código ou texto simples.
- **Evite se:** o produto exige busca a cada tecla com correção de erro e facetas; vá para o doc 02.
