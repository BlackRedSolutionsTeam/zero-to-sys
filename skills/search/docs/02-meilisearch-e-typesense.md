# Meilisearch e Typesense

> Motores de busca simples de operar, feitos para busca ao digitar, tolerância a erro de digitação, filtros e facetas, com pouca configuração.

| | |
|---|---|
| **Referência** | https://github.com/meilisearch/meilisearch e https://github.com/typesense/typesense (releases e README); https://typesense.org/docs/ |
| **Categoria** | Busca |
| **Tipo** | Serviço de busca |
| **Vale para** | Qualquer stack, com SDKs oficiais para JavaScript, Python, PHP, Ruby, Go, Java e .NET |
| **Verificado em** | 2026-11-25 |

## O que é

Dois motores open source que guardam uma cópia dos seus dados num índice próprio, pensado para respostas em milissegundos:

| | Meilisearch | Typesense |
|---|---|---|
| Versão mais recente conferida | v1.58.0 (release de 23 de novembro) | v30.2 (release de 19 de abril) |
| Licença | Edição Community sob MIT; recursos Enterprise sob licença comercial ou BUSL 1.1 | Servidor sob GPL-3.0; bibliotecas cliente sob Apache |
| Onde guarda o índice | Em disco, com cache em memória | Em memória (RAM), com cópia em disco |
| Esquema | Opcional; descobre os campos | Obrigatório: campos e tipos declarados |
| Isolamento por cliente | Tenant tokens (JWT com filtro embutido) | Chaves de busca com escopo (filtro embutido) |
| Nuvem gerenciada | Meilisearch Cloud | Typesense Cloud |
| Porta padrão | 7700 | 8108 |

Preço da nuvem, conferido em 2026-11-25:

- **Meilisearch Cloud:** os planos Build e Pro cobram uma mensalidade mais uso. Pela documentação oficial, o Build inclui 50 mil buscas por mês (depois, US$ 0,40 por mil) e 100 mil documentos (depois, US$ 0,30 por mil), em recursos compartilhados; o Pro inclui 250 mil buscas (depois, US$ 0,30 por mil) e 1 milhão de documentos (depois, US$ 0,20 por mil), em recursos dedicados. O valor da mensalidade não foi confirmado em página oficial (fontes de terceiros citam US$ 30 e US$ 300); veja no console antes de contar com ele.
- **Typesense Cloud:** cluster dedicado, sem limite de registros nem de operações, cobrado por memória (de 0,5 GB a 1024 GB), vCPUs, número de nós (de 3 a 7 para alta disponibilidade) e banda de saída. Não há preço fixo na página; use o assistente de configuração do site.

## Por que usar

- **Busca ao digitar** com resposta rápida e tolerância a erros, sem escrever SQL de relevância.
- **Facetas e filtros** prontos (contagem por categoria, faixa de preço).
- **Operação simples:** um binário ou uma imagem Docker.
- **Isolamento por cliente** com tokens que carregam o filtro (doc 07).

## Quando usar

- Autocomplete e busca instantânea em catálogo, base de conhecimento ou cadastro grande.
- A busca virou parte central do produto e o `ILIKE` não entrega a experiência.
- Quer relevância boa sem time dedicado a busca.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Vale para documentação com busca ao digitar; para blog pequeno, o banco basta |
| MVP de SaaS | 🟡 Serve | Só se a busca for o diferencial; senão, comece pelo banco |
| SaaS em crescimento | ✅ Ótimo | Facetas, filtros e multiempresa por token |
| Sistema interno/corporativo | 🟡 Serve | Útil em base grande de documentos ou produtos |
| API/integração | 🟡 Serve | Quando o cliente da API precisa de busca por texto |
| App mobile com backend | ✅ Ótimo | Resposta rápida e tolerante a erro no teclado do celular |
| Logs e métricas | ❌ Evite | Para isso, Elasticsearch ou OpenSearch (doc 03) |

## Quando é bom

- **Meilisearch** vem com regras de relevância prontas, sinônimos, filtros, facetas e ordenação, e não exige esquema.
- **Typesense** é rápido por manter o índice na RAM, tem esquema explícito e cluster com alta disponibilidade na nuvem.
- Ambos têm SDK de front-end para busca sem passar pelo seu backend, com chave restrita.

## Quando é ruim

- **Typesense na RAM:** o índice precisa caber na memória; a documentação cita cerca de 165 MB para 1 milhão de títulos e cerca de 14 GB para 28 milhões de livros. Dimensione a VPS por isso (skill `vps`, doc 02).
- **Licença GPL-3.0 do Typesense:** vale para o servidor; usar como serviço separado não obriga a abrir o seu código, mas se for modificar e distribuir o servidor, leia a licença.
- **Meilisearch Enterprise:** recursos Enterprise exigem acordo comercial em produção; a edição Community é MIT.
- **Mais um serviço para sincronizar** (doc 04) e para fazer backup (doc 08).
- **Consistência eventual:** um dado gravado no banco aparece na busca depois de alguns instantes.
- **Chave de administração no navegador** é vazamento total; no front-end use só chave de busca ou token com escopo.

## Como começar

Meilisearch com Docker (comando do README oficial; troque `latest` pela versão fixa e defina a chave mestra):

```bash
docker run -d --name meilisearch \
  -p 127.0.0.1:7700:7700 \
  -e MEILI_MASTER_KEY="$MEILI_MASTER_KEY" \
  -e MEILI_ENV=production \
  -v $(pwd)/meili_data:/meili_data \
  getmeili/meilisearch:v1.58.0
```

Indexar e buscar com a API (o endpoint cria o índice se não existir):

```bash
curl -X POST "http://127.0.0.1:7700/indexes/patients/documents?primaryKey=id" \
  -H "Authorization: Bearer $MEILI_MASTER_KEY" \
  -H "Content-Type: application/json" \
  --data '[{"id":1,"company_id":10,"name":"Maria Souza","city":"Recife"}]'

curl -X POST "http://127.0.0.1:7700/indexes/patients/search" \
  -H "Authorization: Bearer $MEILI_SEARCH_KEY" \
  -H "Content-Type: application/json" \
  --data '{"q":"sousa","filter":"company_id = 10","limit":20}'
```

Typesense com Docker (o README oficial mostra a 29.0; confirme no Docker Hub a etiqueta da versão que quer):

```bash
docker run -d --name typesense \
  -p 127.0.0.1:8108:8108 \
  -v $(pwd)/typesense_data:/data \
  typesense/typesense:30.2 \
  --data-dir /data --api-key="$TYPESENSE_API_KEY"
```

Criar a coleção, indexar e buscar:

```bash
curl -X POST "http://127.0.0.1:8108/collections" \
  -H "X-TYPESENSE-API-KEY: $TYPESENSE_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"name":"patients","fields":[{"name":"company_id","type":"int32","facet":true},{"name":"name","type":"string"},{"name":"city","type":"string","facet":true}]}'

curl -X POST "http://127.0.0.1:8108/collections/patients/documents" \
  -H "X-TYPESENSE-API-KEY: $TYPESENSE_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"id":"1","company_id":10,"name":"Maria Souza","city":"Recife"}'

curl -G "http://127.0.0.1:8108/collections/patients/documents/search" \
  -H "X-TYPESENSE-API-KEY: $TYPESENSE_SEARCH_KEY" \
  --data-urlencode "q=sousa" \
  --data-urlencode "query_by=name" \
  --data-urlencode "filter_by=company_id:=10"
```

Os campos e os nomes de parâmetros acima seguem a API de cada projeto; confirme na documentação da versão que for instalar. Portas presas em `127.0.0.1` e atrás de um proxy com HTTPS (skill `nginx`), porque o Docker ignora o `ufw` em portas publicadas (skill `vps`, doc 03).

## Combina com / alternativas

- [Sincronizar índice e banco](04-sincronizar-indice-e-banco.md): como manter a cópia atualizada.
- [Relevância e português](05-relevancia-sinonimos-acentos-e-portugues.md): sinônimos e acentos.
- [Multiempresa](07-multiempresa-isolar-resultados.md): tokens com filtro.
- [VPS com Coolify ou Dokploy](../../infra/docs/02-vps-coolify-dokploy.md): onde hospedar o contêiner.
- [Elasticsearch e OpenSearch](03-elasticsearch-e-opensearch.md): quando passar de escala.

## Decisão rápida

- **Use Meilisearch se:** quer o caminho mais curto para uma busca ao digitar boa, sem esquema fixo.
- **Use Typesense se:** o índice cabe na RAM, o esquema é bem definido e quer cluster de alta disponibilidade.
- **Evite os dois se:** a busca por `ILIKE` e trigram ainda atende, ou se o caso é análise de logs.
