# Operar: custo, backup e atualização

> Saiba quanta memória o índice pede, como recuperá-lo se o servidor morrer e como atualizar o motor sem perder a busca.

| | |
|---|---|
| **Referência** | https://github.com/meilisearch/meilisearch/releases, https://github.com/typesense/typesense/releases, https://www.elastic.co/pricing/faq/licensing e https://aws.amazon.com/opensearch-service/pricing/; documentação de snapshots e atualização de cada motor |
| **Categoria** | Busca |
| **Tipo** | Prática de operação |
| **Vale para** | Meilisearch, Typesense, Elasticsearch e OpenSearch, em VPS, contêiner ou nuvem gerenciada |
| **Verificado em** | 2026-11-25 |

## O que é

Operar a busca é cuidar de quatro coisas depois que ela está no ar:

- **Custo:** memória, disco e, na nuvem, mensalidade e uso.
- **Backup e recuperação:** como voltar se o servidor ou o índice se perderem.
- **Atualização:** trocar a versão do motor sem derrubar a busca.
- **Monitoramento:** espaço, memória, latência e atraso do índice em relação ao banco.

Como o índice é cópia do banco (doc 04), o backup principal é o próprio banco; o do índice existe para não esperar horas de reindexação.

## Por que usar

- **Reindexar um volume grande leva tempo:** medir isso decide se o snapshot vale.
- **Typesense mantém o índice na RAM:** falta de memória derruba o serviço.
- **Atualizações de versão maior** podem mudar o formato do dado em disco.

## Quando usar

- Antes de lançar a busca em produção.
- A cada atualização do motor e a cada mudança grande de volume.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Reindexar tudo é rápido e basta como recuperação |
| MVP de SaaS | ✅ Ótimo | Mesmo servidor, `--restart unless-stopped` e reindexação |
| SaaS em crescimento | ✅ Ótimo | Snapshot agendado e alerta de memória |
| Sistema interno/corporativo | ✅ Ótimo | Janela de atualização combinada |
| API/integração | 🟡 Serve | Combine o que fazer quando a busca ficar fora do ar |
| App mobile com backend | 🟡 Serve | Trate falha da busca na tela sem travar o app |
| Busca crítica sem nenhum plano de falha | ❌ Evite | Um nó único é ponto único de falha |

## Quando é bom

- **Nuvem gerenciada** cuida de backup, atualização e alta disponibilidade (Meilisearch Cloud, Typesense Cloud, Elastic Cloud, Amazon OpenSearch Service).
- **Snapshots do motor** (Meilisearch tem snapshots e dumps; Typesense tem a API de snapshot; Elasticsearch e OpenSearch têm repositórios de snapshot) encurtam a recuperação.
- **Atualizar numa cópia primeiro** mostra problemas antes da produção.

## Quando é ruim

- **Backup do volume com o serviço em escrita** pode dar um arquivo inconsistente; use o recurso de snapshot do motor ou pare o serviço.
- **Dump e snapshot não são intercambiáveis entre versões:** o formato muda; leia as notas da versão.
- **Subestimar memória:** Typesense na RAM e a JVM do Elasticsearch e do OpenSearch pedem folga; o sistema mata o processo sem aviso quando acaba.
- **Mensalidade e uso na nuvem** crescem com buscas e documentos (Meilisearch Cloud cobra excedente de buscas e de documentos; Amazon OpenSearch cobra horas de instância).
- **Esquecer a atualização de segurança** do motor ou do contêiner.

## Como começar

Custo e dimensionamento, conferidos em 2026-11-25:

| Motor | O que pesa | Referência de partida |
|---|---|---|
| PostgreSQL (doc 01) | Disco e CPU do banco já pago | Sem custo extra |
| Meilisearch | Disco e memória do índice; na nuvem, buscas e documentos | Build: 50 mil buscas e 100 mil documentos incluídos; Pro: 250 mil buscas e 1 milhão de documentos (mensalidade: confira no console) |
| Typesense | RAM proporcional aos dados | Cerca de 30 MB do servidor vazio; cerca de 165 MB para 1 milhão de títulos (README oficial) |
| Elasticsearch e OpenSearch | RAM da JVM, disco, vários nós | Exemplo oficial da AWS: `r6g.xlarge.search` a US$ 0,335 por hora |

Para uma VPS, some a RAM do motor ao que já roda lá (skill `vps`, doc 02), e prefira separar quando a busca passar de metade da memória.

Reinício automático e dados em volume, com versão fixa (nunca `latest` em produção):

```yaml
services:
  meilisearch:
    image: getmeili/meilisearch:v1.58.0
    restart: unless-stopped
    environment:
      MEILI_ENV: production
      MEILI_MASTER_KEY: ${MEILI_MASTER_KEY}
    ports:
      - "127.0.0.1:7700:7700"
    volumes:
      - meili_data:/meili_data

volumes:
  meili_data:
```

Backup, Meilisearch (a API de dumps gera um arquivo importável; confira o fluxo na documentação da versão):

```bash
curl -X POST "http://127.0.0.1:7700/dumps" -H "Authorization: Bearer $MEILI_MASTER_KEY"
```

Backup, Typesense (a API de snapshot grava uma cópia consistente do diretório de dados):

```bash
curl -X POST "http://127.0.0.1:8108/operations/snapshot?snapshot_path=/data/snapshots/$(date +%F)" \
  -H "X-TYPESENSE-API-KEY: $TYPESENSE_API_KEY"
```

Copie o resultado para fora do servidor (skill `vps`, doc 05) e teste a restauração em outra máquina, anotando a data no `README`.

Atualização, em ordem:

1. Leia as notas da versão (Meilisearch v1.58.0 e Typesense v30.2 eram as mais recentes em 2026-11-25).
2. Tire um snapshot ou dump e confirme que ele restaura.
3. Suba a nova versão numa cópia, restaure o dump e rode as consultas de teste do [doc 05](05-relevancia-sinonimos-acentos-e-portugues.md).
4. Troque em produção fora do horário de pico, com a reindexação completa pronta como plano B.

Monitoramento mínimo (skill `infra`, doc 10): uso de memória e disco com alerta acima de 80%, latência de busca, contagem de documentos do índice contra a do banco e falhas do worker de indexação.

## Combina com / alternativas

- [Sincronizar índice e banco](04-sincronizar-indice-e-banco.md): reindexação como plano B.
- [Dimensionar o servidor](../../vps/docs/02-dimensionar-o-servidor.md): RAM e disco.
- [Backup e restauração na VPS](../../vps/docs/05-backup-e-restauracao-na-vps.md): cópia externa e teste.
- [Observabilidade](../../infra/docs/10-observabilidade.md): alertas e métricas.
- [Backup e recuperação](../../infra/docs/11-backup-e-recuperacao.md): estratégia geral.
- [VPS com Coolify ou Dokploy](../../infra/docs/02-vps-coolify-dokploy.md): hospedar o contêiner.

## Decisão rápida

- **Use se:** a busca roda em servidor próprio; fixe a versão, agende snapshot, teste a restauração e monitore memória.
- **Evite se:** ninguém vai cuidar disso; contrate a versão gerenciada ou fique no PostgreSQL.
