# Multiempresa: isolar resultados por cliente

> Uma empresa nunca pode ver o documento de outra na busca: filtro por empresa aplicado no servidor ou embutido em token assinado, nunca confiado ao navegador.

| | |
|---|---|
| **Referência** | https://typesense.org/docs/latest/api/api-keys.html (chaves com escopo); documentação de tenant tokens do Meilisearch (meilisearch.com/docs/learn/security/tenant_tokens); documentação de índices e alias do Elasticsearch e do OpenSearch |
| **Categoria** | Busca |
| **Tipo** | Prática de segurança |
| **Vale para** | Sistemas multiempresa com PostgreSQL, Meilisearch, Typesense, Elasticsearch ou OpenSearch |
| **Verificado em** | 2026-11-25 |

## O que é

No sistema multiempresa (skill `data`, doc 06), cada empresa vê só os seus dados. O banco pode impor isso com Row Level Security; um motor de busca separado não herda essa regra, então ela precisa ser refeita no índice. Três jeitos:

| Jeito | Como funciona | Vantagem | Custo |
|---|---|---|---|
| Campo `company_id` e filtro no servidor | Seu backend sempre acrescenta o filtro | Simples, um índice só | Um esquecimento vaza dados |
| Token com filtro embutido | O backend gera um token com `company_id` dentro; o navegador busca direto no motor | Busca sem passar pelo seu servidor, sem poder trocar o filtro | Gerar e renovar tokens |
| Índice por empresa | Cada cliente tem o seu índice | Isolamento forte, apagar um cliente é apagar um índice | Muitos índices consomem memória e gestão |

Nos motores:

- **Meilisearch:** os tenant tokens são JWTs gerados pela sua aplicação a partir de uma chave de busca; a regra (`searchRules`) guarda um `filter`, aplicado a toda busca feita com o token, e vale só para os índices listados. Hoje o filtro é o único parâmetro de busca que o token suporta, e a documentação recomenda definir validade.
- **Typesense:** chaves de busca com escopo são geradas fora do servidor a partir de uma chave-mãe com permissão só de `documents:search`; os parâmetros embutidos (como `filter_by`) são aplicados automaticamente e o usuário não os sobrescreve. Se revogar a chave-mãe, todas as derivadas deixam de valer.
- **Elasticsearch e OpenSearch:** filtro `term` no `company_id` em toda consulta, filtro por alias (um alias por cliente apontando para um índice compartilhado, com filtro) ou índice por cliente. Controle de acesso por documento depende do recurso de segurança do plano ou do plugin de segurança do OpenSearch; confirme o que a sua licença inclui.

## Por que usar

- **Vazamento entre clientes é o pior bug de um SaaS:** na busca ele é mais fácil de causar que no banco.
- **Token com escopo** permite busca direta do navegador sem expor dados de outros clientes.
- **Isolamento comprovável** facilita auditoria e resposta a clientes grandes.

## Quando usar

- Todo sistema em que mais de uma empresa compartilha o mesmo motor de busca.
- Antes de ligar a busca em produção, junto com os testes de isolamento da skill `security`.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Normalmente não há dados por cliente |
| MVP de SaaS | ✅ Ótimo | Campo `company_id` e filtro no servidor desde o início |
| SaaS em crescimento | ✅ Ótimo | Tokens com escopo para busca direta do front-end |
| Sistema interno/corporativo | 🟡 Serve | Vale se há filiais ou áreas com dados separados |
| API/integração | ✅ Ótimo | Cada chave de integração presa à empresa |
| App mobile com backend | ✅ Ótimo | Token de curta duração por sessão |
| Poucos clientes grandes com exigência contratual | ✅ Ótimo | Índice por cliente com chaves próprias |

## Quando é bom

- **Filtro no servidor** cobre a maioria dos casos com uma função única de busca.
- **Token com filtro** impede que quem inspeciona a rede troque a empresa.
- **Índice por cliente** apaga todos os dados de um cliente de uma vez (útil para LGPD, skill `security`, doc 09).

## Quando é ruim

- **Filtro opcional:** qualquer rota de busca que esqueça o `company_id` vaza dados. Centralize numa única função.
- **Chave de administração ou chave mestra no front-end** dá acesso a tudo; ela só existe no servidor.
- **Token sem validade** vale para sempre se vazar; use tempo curto e renove.
- **Empresa mudou de plano ou foi bloqueada:** o token já emitido continua válido até expirar.
- **Índice por cliente com milhares de clientes** sobrecarrega o motor (memória, arquivos, gestão); prefira o campo `company_id` com filtro.
- **Campo `company_id` não declarado como filtrável** faz o filtro falhar ou não funcionar (doc 06).

## Como começar

Função única de busca no servidor, que sempre aplica a empresa da sessão:

```ts
export async function searchPatients(session: Session, query: string, page: number) {
  const companyId = session.companyId
  return searchClient.index('patients').search(query, {
    filter: `company_id = ${Number(companyId)}`,
    limit: 20,
    offset: (page - 1) * 20,
  })
}
```

O valor do filtro vem da sessão, nunca do corpo da requisição, e é convertido para número para impedir injeção.

Meilisearch, token com escopo gerado no servidor (SDK JavaScript oficial; confirme a assinatura na versão do SDK que instalar):

```ts
import { Meilisearch } from 'meilisearch'

const client = new Meilisearch({ host: process.env.MEILI_HOST!, apiKey: process.env.MEILI_ADMIN_KEY! })

export async function tokenForCompany(companyId: number) {
  const searchRules = { patients: { filter: `company_id = ${companyId}` } }
  return client.generateTenantToken(process.env.MEILI_SEARCH_KEY_UID!, searchRules, {
    apiKey: process.env.MEILI_SEARCH_KEY!,
    expiresAt: new Date(Date.now() + 60 * 60 * 1000),
  })
}
```

Typesense, chave com escopo (a chave-mãe só pode ter permissão `documents:search`; o exemplo oficial usa `filter_by` e `expires_at`):

```ts
import Typesense from 'typesense'

const client = new Typesense.Client({
  nodes: [{ host: process.env.TS_HOST!, port: 443, protocol: 'https' }],
  apiKey: process.env.TS_ADMIN_KEY!,
})

export function keyForCompany(companyId: number) {
  return client.keys().generateScopedSearchKey(process.env.TS_SEARCH_PARENT_KEY!, {
    filter_by: `company_id:=${companyId}`,
    expires_at: Math.floor(Date.now() / 1000) + 3600,
  })
}
```

Teste de isolamento, obrigatório antes de ir para produção: crie dois clientes com o mesmo termo e confirme que cada um só vê os seus.

```ts
test('empresa A não vê dados da empresa B', async () => {
  await indexPatient({ id: 'a1', companyId: 1, name: 'Maria Souza' })
  await indexPatient({ id: 'b1', companyId: 2, name: 'Maria Souza' })
  const result = await searchPatients({ companyId: 1 }, 'Maria', 1)
  expect(result.hits.map((hit) => hit.id)).toEqual(['a1'])
})
```

## Combina com / alternativas

- [Multiempresa](../../data/docs/06-multiempresa.md): Row Level Security e `company_id` no banco.
- [Papéis e permissões](../../security/docs/04-papeis-e-permissoes.md): quem pode ver o quê dentro da empresa.
- [OWASP no código](../../security/docs/05-owasp-no-codigo.md): injeção em filtros e controle de acesso.
- [Segredos e configuração](../../infra/docs/09-segredos-e-configuracao.md): onde guardar a chave mestra.
- [Filtros, facetas e paginação](06-filtros-facetas-e-paginacao.md): declarar `company_id` como filtrável.

## Decisão rápida

- **Use se:** mais de uma empresa compartilha o motor; filtro no servidor, e token com escopo para busca direta do navegador.
- **Evite se:** pensa em confiar o `company_id` ao front-end ou deixar a chave de administração fora do servidor.
