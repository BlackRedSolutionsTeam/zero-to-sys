# Elasticsearch e OpenSearch

> Motores de busca e análise para volumes grandes, agregações pesadas e logs; poderosos, mas caros de operar. Escolha só quando o banco, o Meilisearch e o Typesense não bastam.

| | |
|---|---|
| **Referência** | https://github.com/elastic/elasticsearch/releases, https://github.com/opensearch-project/OpenSearch/releases, https://www.elastic.co/pricing/faq/licensing e https://aws.amazon.com/opensearch-service/pricing/ |
| **Categoria** | Busca |
| **Tipo** | Serviço de busca e análise |
| **Vale para** | Qualquer stack, com clientes oficiais em Java, JavaScript, Python, .NET, Go, PHP e Ruby |
| **Verificado em** | 2026-11-25 |

## O que é

Dois motores baseados em Lucene que guardam documentos em índices divididos em **shards** (partes) e réplicas, com uma linguagem de consulta completa (query DSL) e agregações.

| | Elasticsearch | OpenSearch |
|---|---|---|
| Versão mais recente conferida | 9.5.7 (release de 23 de novembro) | 3.10.1 (release de 24 de novembro) |
| Origem | Elastic | Fork do Elasticsearch 7.10, hoje sob a Linux Foundation |
| Licença | O código pode ser usado sob SSPL 1.0, AGPLv3 ou Elastic License 2.0, à sua escolha; a distribuição padrão é ELv2 | Apache 2.0 (sem restrição para oferecer como serviço) |
| Nuvem gerenciada | Elastic Cloud (Hosted e Serverless) | Amazon OpenSearch Service e outros |
| Painéis | Kibana | OpenSearch Dashboards |

Conferido em 2026-11-25:

- **Licença do Elasticsearch:** pelo FAQ da Elastic, usar o Elasticsearch dentro de um SaaS seu e redistribuí-lo com a aplicação é permitido, desde que respeite as limitações da ELv2 (por exemplo, não oferecer o próprio Elasticsearch como serviço gerenciado a terceiros).
- **Preço do Elastic Cloud:** Hosted é cobrado por recursos e Serverless por uso; a página de preços não traz valores no texto e deve ser consultada no site.
- **Preço no Amazon OpenSearch Service:** domínios gerenciados cobram horas de instância, armazenamento e transferência, sem mínimo (exemplo oficial: `r6g.xlarge.search` a US$ 0,335 por hora); o modo Serverless cobra por OCU (cerca de 6 GB de RAM mais vCPU por unidade), com armazenamento à parte. A página tem exemplos de preço inconsistentes entre si; use a calculadora oficial da AWS antes de orçar.

## Por que usar

- **Escala horizontal madura:** índices em vários nós, réplicas e recuperação de falha.
- **Agregações poderosas:** estatísticas, histogramas e análises sobre milhões de documentos.
- **Logs e observabilidade:** o uso mais comum no mercado.
- **Controle fino da análise de texto:** analisadores, filtros e sinônimos personalizados por idioma.

## Quando usar

- Dezenas de milhões de documentos ou mais, ou necessidade de vários nós.
- Análise de logs, eventos ou métricas com agregações.
- A empresa já opera Elasticsearch ou OpenSearch e tem quem cuide.
- Requisitos que os motores simples não cobrem (consultas muito customizadas, busca em vários índices com regras complexas).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Excesso de complexidade para esse volume |
| MVP de SaaS | ❌ Evite | O banco ou o Meilisearch resolvem com uma fração do custo |
| SaaS em crescimento | 🟡 Serve | Só com volume alto ou análises que os outros não fazem |
| Sistema interno/corporativo | 🟡 Serve | Quando já existe a plataforma e o time |
| API/integração | 🟡 Serve | Busca em grande escala atrás da API |
| App mobile com backend | ❌ Evite | Complexidade sem ganho perto de Meilisearch ou Typesense |
| Plataforma de logs e eventos | ✅ Ótimo | É o caso de uso principal |

## Quando é bom

- Aguenta volume e concorrência que um nó único de motor simples não aguenta.
- Ferramentas de análise (Kibana, OpenSearch Dashboards) incluídas no ecossistema.
- OpenSearch com licença Apache 2.0 evita dúvida jurídica de licença (o `LICENSE.txt` do repositório `opensearch-project/OpenSearch` é a Apache License 2.0, conferido em 2026-11-25).

## Quando é ruim

- **Operação pesada:** cluster, shards, memória da JVM, atualização de versão e reindexação de mapeamento são trabalho de gente especializada.
- **Custo:** mínimo de recursos bem acima de um Meilisearch (um nó de produção costuma pedir vários GB de RAM; confirme na documentação da versão).
- **Mapeamento difícil de mudar:** trocar o tipo de um campo exige criar outro índice e reindexar (doc 04).
- **Relevância e tolerância a erro exigem configuração** que Meilisearch e Typesense trazem prontas.
- **Dois produtos parecidos e divergentes:** Elasticsearch e OpenSearch seguem caminhos diferentes desde o fork; um cliente de uma versão pode não falar com o outro.

## Como começar

OpenSearch de um nó para desenvolvimento, com Docker. Comando executado em 2026-11-25 com `opensearchproject/opensearch:3` (OpenSearch 3.10.1, Docker Desktop no macOS): subiu e respondeu em `https://localhost:9200`. A variável `OPENSEARCH_INITIAL_ADMIN_PASSWORD` é obrigatória desde a 2.12 e exige senha forte (a documentação cita tamanho mínimo, várias classes de caracteres e verificação de entropia; sem ela, ou com ela fraca, o contêiner encerra). Em Linux, o `vm.max_map_count` precisa ser pelo menos 262144 (`sudo sysctl -w vm.max_map_count=262144`, e a linha `vm.max_map_count=262144` em `/etc/sysctl.conf` para persistir; confira com `cat /proc/sys/vm/max_map_count`). No Docker Desktop o valor já era 262144 e não foi preciso mudar; o ajuste num servidor Linux real não foi testado aqui. Use o `-k` do `curl` com o certificado de teste autoassinado:

```bash
docker run -d --name opensearch \
  -p 127.0.0.1:9200:9200 \
  -e discovery.type=single-node \
  -e OPENSEARCH_INITIAL_ADMIN_PASSWORD="$OPENSEARCH_PASSWORD" \
  opensearchproject/opensearch:3
```

Índice com analisador de português que também ignora acentos. O analisador `portuguese` embutido usa o tokenizador padrão, minúsculas, lista de palavras comuns e o stemmer `light_portuguese`; para ignorar acentos, recrie-o como analisador customizado e acrescente o filtro `asciifolding` (na documentação da Elastic o `asciifolding` não aparece no exemplo do português; esta adição é uma extensão padrão do filtro; testado no OpenSearch 3.10.1: a busca `acao advogado` achou "Ação civil dos advogados"):

```bash
curl -k -X PUT "https://localhost:9200/patients" -u "admin:$OPENSEARCH_PASSWORD" \
  -H "Content-Type: application/json" \
  --data '{
    "settings": {
      "analysis": {
        "filter": {
          "pt_stop": { "type": "stop", "stopwords": "_portuguese_" },
          "pt_stemmer": { "type": "stemmer", "language": "light_portuguese" }
        },
        "analyzer": {
          "pt_sem_acento": {
            "tokenizer": "standard",
            "filter": ["lowercase", "asciifolding", "pt_stop", "pt_stemmer"]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "company_id": { "type": "keyword" },
        "name": { "type": "text", "analyzer": "pt_sem_acento" }
      }
    }
  }'
```

Busca com filtro obrigatório por empresa (o filtro vai em `filter`, que não afeta a pontuação):

```bash
curl -X POST "https://localhost:9200/patients/_search" -u "admin:$OPENSEARCH_PASSWORD" \
  -H "Content-Type: application/json" \
  --data '{
    "query": {
      "bool": {
        "must": { "match": { "name": { "query": "acao", "fuzziness": "AUTO" } } },
        "filter": { "term": { "company_id": "10" } }
      }
    },
    "size": 20
  }'
```

Certificados e senha de teste não servem em produção; ver [segurança base](../../infra/docs/12-seguranca-base.md).

## Combina com / alternativas

- [Meilisearch e Typesense](02-meilisearch-e-typesense.md): a alternativa mais simples.
- [Operar](08-operar-custo-backup-e-atualizacao.md): snapshots e atualização.
- [Nuvem grande](../../infra/docs/03-nuvem-grande.md): OpenSearch Service na AWS.
- [Observabilidade](../../infra/docs/10-observabilidade.md): logs e métricas do sistema.

## Decisão rápida

- **Use se:** o volume ou a análise passam do que o banco e os motores simples fazem, e há quem opere o cluster ou verba para o serviço gerenciado.
- **Evite se:** é um MVP, um cadastro ou um catálogo de tamanho médio; comece pelo banco ou pelo Meilisearch.
