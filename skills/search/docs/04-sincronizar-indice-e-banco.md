# Sincronizar índice e banco

> O banco é a fonte da verdade e o índice é uma cópia: atualize por eventos, tenha uma reindexação completa à mão e aceite que a busca pode atrasar alguns segundos.

| | |
|---|---|
| **Referência** | https://www.postgresql.org/docs/current/sql-notify.html, https://www.postgresql.org/docs/current/logicaldecoding.html; documentação de indexação em lote do Meilisearch, do Typesense e do OpenSearch |
| **Categoria** | Busca |
| **Tipo** | Prática de integração |
| **Vale para** | Qualquer sistema com banco relacional e um motor de busca separado |
| **Verificado em** | 2026-11-25 |

## O que é

Com um motor de busca separado, o mesmo dado vive em dois lugares. Sincronizar é garantir que o que mudou no banco chegue ao índice, inclusive remoções, e que dê para reconstruir tudo se algo falhar.

Quatro formas, da mais simples à mais robusta:

| Forma | Como funciona | Quando serve |
|---|---|---|
| Indexar na hora | O código grava no banco e chama o motor na mesma requisição | Protótipo; falha do motor quebra a gravação |
| Job após gravar | A gravação enfileira um job que indexa (skill `integrations`, doc 05) | Padrão para a maioria |
| Outbox | Evento gravado na mesma transação do dado; um processo lê e indexa | Quando não pode perder atualização |
| Captura de mudanças (CDC) | Lê o log do banco (decodificação lógica do PostgreSQL) e envia ao índice | Muitos sistemas escrevendo na mesma tabela |

## Por que usar

- **O índice nunca vira fonte da verdade:** se estragar, reconstrói.
- **Falha do motor não derruba o sistema:** a gravação no banco continua.
- **Remoções e atualizações chegam ao índice:** sem resultado fantasma.

## Quando usar

- Em todo sistema que usa Meilisearch, Typesense, Elasticsearch ou OpenSearch.
- Antes de ligar a busca em produção, e de novo a cada mudança no formato do documento indexado.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Reindexar tudo ao publicar basta |
| MVP de SaaS | ✅ Ótimo | Job após gravar mais reindexação completa |
| SaaS em crescimento | ✅ Ótimo | Outbox garante que nada se perde |
| Sistema interno/corporativo | ✅ Ótimo | Reindexação noturna cobre o resto |
| API/integração | 🟡 Serve | Depende de quantos sistemas escrevem no dado |
| App mobile com backend | ✅ Ótimo | A pessoa espera ver o que acabou de criar; trate o atraso |
| Busca só em banco (PostgreSQL) | ❌ Evite | Não há o que sincronizar; veja o [doc 01](01-quando-o-banco-basta.md) |

## Quando é bom

- **Job idempotente:** indexar o mesmo documento duas vezes dá o mesmo resultado (use o `id` do banco como `id` do documento).
- **Reindexação completa** serve de backup, de correção de bug e de migração de esquema.
- **Lotes** (centenas ou milhares de documentos por chamada) são muito mais rápidos que um por vez.

## Quando é ruim

- **Indexar na hora:** se o motor cai, a gravação falha ou o índice fica atrás sem aviso.
- **Esquecer a remoção:** `delete` e `soft delete` (skill `data`, doc 07) precisam retirar do índice.
- **Atraso invisível:** a pessoa cria um registro e não o acha na busca. Mostre o item recém-criado na tela, ou espere o job terminar quando o fluxo exigir.
- **Ordem de eventos:** duas atualizações do mesmo registro processadas fora de ordem deixam o índice errado. Indexe lendo o estado atual do banco no momento do job, não o payload do evento.
- **Reindexar sem janela:** apagar o índice e recriar deixa a busca vazia; use o padrão de troca de índice (abaixo).

## Como começar

Fluxo recomendado: gravar no banco, enfileirar o job com o id e indexar lendo o estado atual.

```ts
export async function savePatient(input: PatientInput) {
  const patient = await db.transaction(async (tx) => {
    const saved = await tx.patient.upsert(input)
    await tx.searchOutbox.insert({ entity: 'patient', entityId: saved.id })
    return saved
  })
  return patient
}

export async function indexPatient(id: string) {
  const patient = await db.patient.findById(id)
  if (!patient || patient.deletedAt) {
    await searchClient.index('patients').deleteDocument(id)
    return
  }
  await searchClient.index('patients').addDocuments([toSearchDocument(patient)])
}
```

Um processo lê a tabela `search_outbox`, chama `indexPatient` e marca como processado. Com fila (skill `integrations`, doc 05), o processo é um worker com repetição e fila de falhas.

Reindexação completa em lotes, com paginação por cursor (skill `data`, doc 08):

```ts
export async function reindexPatients() {
  let lastId = ''
  for (;;) {
    const batch = await db.patient.listAfter(lastId, 1000)
    if (batch.length === 0) break
    await searchClient.index('patients_new').addDocuments(batch.map(toSearchDocument))
    lastId = batch[batch.length - 1].id
  }
}
```

Troca sem janela de busca vazia: indexe num índice novo (`patients_new`), confira a contagem e troque o alias ou o nome que a aplicação usa. No Elasticsearch e no OpenSearch isso é um **alias**; no Meilisearch há o recurso de trocar índices (`swap-indexes`) e no Typesense há alias de coleção. Confirme o nome exato na documentação da versão que usa.

Conferir se o índice bate com o banco:

```sql
select count(*) from patient where deleted_at is null;
```

Compare com a contagem de documentos do índice; diferença é sinal de job perdido. Agende essa conferência (skill `integrations`, doc 06) e alerte quando passar de um limite.

## Combina com / alternativas

- [Filas e jobs](../../integrations/docs/05-filas-e-jobs.md): repetição, fila de falhas, idempotência.
- [Rotinas agendadas](../../integrations/docs/06-rotinas-agendadas.md): reindexação e conferência noturnas.
- [Auditoria, histórico e soft delete](../../data/docs/07-auditoria-historico-soft-delete.md): como a remoção chega ao índice.
- [Operar](08-operar-custo-backup-e-atualizacao.md): tempo de reindexação como parte do plano de recuperação.

## Decisão rápida

- **Use se:** tem um motor de busca separado: job após gravar ou outbox, mais reindexação completa agendada.
- **Evite se:** a busca está no PostgreSQL; a coluna `tsvector` gerada (doc 01) se atualiza sozinha.
