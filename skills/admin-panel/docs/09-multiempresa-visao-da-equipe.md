# Multiempresa: a visão da equipe sem quebrar o isolamento

> O painel enxerga todas as empresas por um caminho separado e explícito, sem enfraquecer a regra de isolamento que protege os clientes entre si no produto.

| | |
|---|---|
| **Referência** | PostgreSQL docs: Row Security Policies (postgresql.org/docs/current/ddl-rowsecurity.html); OWASP API Security Top 10 2023, API1 |
| **Categoria** | Dados e segurança |
| **Tipo** | Prática de acesso entre inquilinos |
| **Vale para** | SaaS multiempresa (modelo geral na skill `data`) |
| **Verificado em** | 2026-11-25 (documentação do PostgreSQL não reaberta nesta data) |

## O que é

No produto, cada consulta carrega o `tenant_id` da sessão ([data, doc 06](../../data/docs/06-multiempresa.md)). A equipe precisa do oposto: buscar em todas as empresas. O risco é resolver isso abrindo um buraco na regra do produto (por exemplo, "se for admin, ignora o filtro").

## Por que usar

- Um atalho no código do produto para a equipe vira vazamento entre clientes quando alguém o reaproveita.
- Mantém duas portas separadas: uma estreita e testada para o cliente, outra larga e auditada para a equipe.

## Quando usar

- Em todo SaaS multiempresa com painel interno.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Não é multiempresa |
| MVP de SaaS | ✅ Ótimo | Defina o caminho da equipe antes do primeiro cliente |
| SaaS em crescimento | ✅ Ótimo | Com RLS e usuário de banco separado |
| Sistema interno/corporativo | 🟡 Serve | Só se houver filiais isoladas |
| API/integração | 🟡 Serve | Chaves por empresa |
| App mobile com backend | ✅ Ótimo | Igual ao SaaS |
| Filtro do produto com exceção para admin | ❌ Evite | É o vazamento esperando acontecer |

## Padrões

| Padrão | Como funciona | Quando |
|---|---|---|
| Caminho separado | Rotas e serviços do painel próprios, com acesso a todas as empresas por consulta explícita | Padrão recomendado |
| Usuário de banco do painel | Papel de banco com políticas RLS que permitem todas as linhas, usado só pelo processo do painel | Quando o painel é outro processo ([doc 11](11-painel-separado-do-produto.md)) |
| Contexto de empresa selecionado | A equipe escolhe a empresa e o painel passa a filtrar por ela, com registro da escolha | Para telas de detalhe |
| Impersonação | Entrar na empresa como o cliente ([doc 05](05-impersonacao-entrar-como-cliente.md)) | Reproduzir problema |

## Quando é bom

- **Código do produto sem `if (staff)`.** A regra de isolamento não tem exceção.
- **Listas do painel** com coluna da empresa e filtro por ela.
- **Registrar a empresa consultada** em cada acesso da equipe ([doc 06](06-auditoria-do-que-a-equipe-faz.md)).
- **Teste:** cliente da empresa B nunca vê dado da A, mesmo com o painel ligado.

## Quando é ruim

- **Super admin do produto** que é só um usuário com papel e ignora `tenant_id`.
- **Mesmo processo, mesmo usuário de banco** para produto e painel: um bug no produto herda o poder do painel.
- **Cache compartilhado** sem `tenant_id` na chave.
- **Relatório cruzado** que traz dado de uma empresa para a tela de outra.

## Como começar

Papel de banco e política (SQL):

```sql
create role painel_equipe login;

alter table faturas enable row level security;

create policy isolamento_produto on faturas
  for all to app_user
  using (tenant_id = current_setting('app.tenant_id')::uuid);

create policy visao_equipe on faturas
  for select to painel_equipe
  using (true);
```

Teste que prova a barreira (TypeScript):

```ts
test("cliente da empresa B não vê fatura da empresa A", async () => {
  const res = await api.get(`/faturas/${faturaDaA.id}`).as(usuarioDaB);
  expect(res.status).toBe(404);
});

test("equipe vê fatura de qualquer empresa e deixa registro", async () => {
  const res = await painel.get(`/faturas/${faturaDaA.id}`).as(suporte);
  expect(res.status).toBe(200);
  expect(await ultimoRegistroDeAuditoria()).toMatchObject({ action: "fatura.ver", tenantId: faturaDaA.empresaId });
});
```

Mais testes de permissão: [quality, doc 04](../../quality/docs/04-testes-de-api-e-contrato.md).

## Combina com / alternativas

- [Data, doc 06](../../data/docs/06-multiempresa.md): isolamento no produto.
- [Security, doc 04](../../security/docs/04-papeis-e-permissoes.md): BOLA e papéis.

## Decisão rápida

- **Use** caminho e, se possível, usuário de banco separados para a equipe, com registro da empresa acessada.
- **Evite** exceção `if (admin)` no filtro do produto.
