# Papéis e permissões

> Autenticação diz quem é a pessoa; autorização diz o que ela pode fazer. Cheque sempre no servidor, negue por padrão e confira o dono de cada recurso.

| | |
|---|---|
| **Referência** | OWASP API Security Top 10 2023 (API1 Broken Object Level Authorization, API5 Broken Function Level Authorization); OWASP Authorization Cheat Sheet; NIST SP 800-162 (ABAC); documentação oficial de ASP.NET Core (authorization policies), Laravel (Gates e Policies), Django (permissions), Spring Security (`@PreAuthorize`), CASL e Hono (middleware) |
| **Categoria** | Segurança |
| **Tipo** | Prática de autorização |
| **Vale para** | Qualquer sistema com mais de um tipo de usuário, em qualquer stack |
| **Verificado em** | 2026-11-24 |

## O que é

- **Autenticação:** provar quem você é (login). Falhou: 401.
- **Autorização:** decidir o que você pode fazer. Falhou: 403 (ou 404, veja abaixo).

Dois modelos, que se combinam:

- **RBAC** (controle por papéis): o usuário tem um papel (recepcionista, médico, admin) e o papel tem permissões.
- **Por recurso** (ownership, ou ABAC, controle por atributos): a regra olha o dado. "O médico só vê os agendamentos dele." "Só edita paciente da própria clínica."

Nome atual da falha mais comum, na lista OWASP API Security Top 10 de 2023: **API1, Broken Object Level Authorization (BOLA)**, também chamada de **IDOR**. É pedir `GET /pacientes/123` e receber o paciente de outra clínica porque o servidor só conferiu o login. A função (rota de admin sem checar papel) é a **API5, Broken Function Level Authorization**.

## Por que usar

- **BOLA é a falha número 1** de API segundo a OWASP.
- **Esconder botão não protege:** qualquer um chama a API direto.
- **Regra em um lugar só** evita esquecer a checagem numa rota nova.

## Quando usar

- Sempre que existir mais de um perfil ou mais de uma empresa.
- A cada rota nova: pergunte "quem pode, sobre qual registro?".

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Um papel de editor basta |
| MVP de SaaS | ✅ Ótimo | 2 ou 3 papéis fixos mais isolamento por empresa |
| SaaS em crescimento | ✅ Ótimo | Permissões por recurso e papéis por empresa |
| Sistema interno/corporativo | ✅ Ótimo | Muitos perfis; permissões em tabela |
| API/integração | ✅ Ótimo | Escopos por chave de API |
| App mobile | ✅ Ótimo | A checagem fica na API, nunca no app |
| Qualquer um, com checagem só no front | ❌ Evite | O front é do usuário; ele altera o que quiser |

## Quando é bom

- **Negar por padrão:** rota sem regra explícita responde 403. Esquecer é seguro.
- **Servidor decide:** o front só esconde para dar boa experiência.
- **Papel por empresa:** a mesma pessoa pode ser admin numa clínica e recepcionista em outra (tabela `memberships`).
- **Permissão como dado:** trocar o que um papel pode não exige deploy.
- **404 para recurso de outra empresa**, para não revelar que existe ([rotas e status](../../api/docs/02-rotas-verbos-e-status.md)).
- **Filtrar a consulta**, não só conferir depois: `where tenant_id = ?` ([multiempresa](../../data/docs/06-multiempresa.md)).

## Quando é ruim

- **Papel demais:** "médico-sênior-da-unidade-2" vira explosão de papéis. Passe a permissões.
- **Checar só papel** quando a regra depende do dono do registro.
- **Confiar em dado do cliente:** `empresaId` ou `papel` vindo do corpo ou do token sem conferir no banco.
- **Ids sequenciais** facilitam adivinhar; use UUID, mas isso não substitui a checagem.
- **Papel guardado no token** muda só quando o token renova ([sessão e tokens](./02-sessao-e-tokens.md)).

## Como começar

Modelo em SQL (a modelagem fina é da skill de dados):

```sql
create table roles (
  id   uuid primary key default gen_random_uuid(),
  name text not null unique
);

create table permissions (
  id   uuid primary key default gen_random_uuid(),
  code text not null unique
);

create table role_permissions (
  role_id       uuid not null references roles(id),
  permission_id uuid not null references permissions(id),
  primary key (role_id, permission_id)
);

create table memberships (
  user_id   uuid not null references users(id),
  tenant_id uuid not null references tenants(id),
  role_id   uuid not null references roles(id),
  primary key (user_id, tenant_id)
);
```

Exemplos de `code`: `agendamento.ler`, `agendamento.cancelar`, `paciente.exportar`.

Middleware e checagem de dono (TypeScript, Hono):

```ts
const exige = (permissao: string) => async (c, next) => {
  const { permissoes } = c.get("contexto");
  if (!permissoes.includes(permissao)) return c.json({ erro: "Sem permissão." }, 403);
  await next();
};

app.get("/agendamentos/:id", exige("agendamento.ler"), async (c) => {
  const { empresaId, usuarioId, papel } = c.get("contexto");
  const ag = await db.agendamento.findFirst({
    where: { id: c.req.param("id"), empresaId },
  });
  if (!ag) return c.json({ erro: "Não encontrado." }, 404);
  if (papel === "medico" && ag.profissionalId !== usuarioId) {
    return c.json({ erro: "Sem permissão." }, 403);
  }
  return c.json(ag);
});
```

O `empresaId` vem da sessão, nunca da URL. Outra empresa dá 404; mesma empresa sem permissão dá 403.

Em cada stack:

| Stack | Onde fica a regra |
|---|---|
| ASP.NET Core | Policies (`AddAuthorization`, `[Authorize(Policy = "...")]`) e handlers por recurso |
| Laravel | Gates e Policies (`$this->authorize('cancel', $agendamento)`) |
| Django | `has_perm` e permissões de modelo; para dono, filtre o queryset |
| Spring | `@PreAuthorize("hasAuthority('agendamento.cancelar')")` e checagem de dono no serviço |
| Node (Hono, Express, Fastify) | Middleware como acima; CASL para regras por atributo |
| Next.js | Cheque na rota, na Server Action e no acesso a dados; não só no middleware |

Teste que prova a barreira (veja [testes de API](../../quality/docs/04-testes-de-api-e-contrato.md)):

```ts
test("recepcionista não cancela agendamento", async () => {
  const res = await api.delete(`/agendamentos/${ag.id}`).as(recepcionista);
  expect(res.status).toBe(403);
});

test("clínica B não vê paciente da clínica A", async () => {
  const res = await api.get(`/pacientes/${pacienteDaA.id}`).as(medicoDaB);
  expect(res.status).toBe(404);
});
```

Um teste de negação por papel e por rota sensível; use o token do papel, não um mock da checagem.

## Combina com / alternativas

- [Escolha do login](./01-escolha-do-login.md): a biblioteca de auth traz a identidade; os papéis são seus.
- [Sessão e tokens](./02-sessao-e-tokens.md): onde mora o contexto do usuário.
- [OWASP no código](./05-owasp-no-codigo.md): as outras falhas da lista.
- [Multiempresa](../../data/docs/06-multiempresa.md): isolamento por `tenant_id` e RLS.
- [Rotas, verbos e status](../../api/docs/02-rotas-verbos-e-status.md) e [formato de erro](../../api/docs/03-formato-de-erro.md): 401, 403 e 404.
- [Testes de API](../../quality/docs/04-testes-de-api-e-contrato.md): testes de papel.

## Decisão rápida

- **Use se:** há mais de um perfil ou empresa; papéis para "o que", checagem de dono para "qual registro", tudo no servidor com negação por padrão.
- **Evite se:** a única barreira é esconder botão ou confiar em `empresaId` enviado pelo cliente.
