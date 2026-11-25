# Quem acessa: papéis internos e menor privilégio

> Cada pessoa da equipe recebe só o que precisa para o trabalho dela, e a ação que pode custar caro exige uma segunda pessoa para aprovar.

| | |
|---|---|
| **Referência** | OWASP Authorization Cheat Sheet (cheatsheetseries.owasp.org); OWASP API Security Top 10 2023, API5 (Broken Function Level Authorization); princípio do menor privilégio (NIST SP 800-53, controle AC-6, citado de memória e não reconferido nesta data) |
| **Categoria** | Segurança |
| **Tipo** | Prática de autorização interna |
| **Vale para** | Qualquer painel com mais de uma pessoa na equipe |
| **Verificado em** | 2026-11-25 (OWASP API5 conferido pelo doc de papéis da skill `security`; NIST AC-6 não reconferido) |

## O que é

O modelo de papéis e permissões é o da skill `security` ([doc 04](../../security/docs/04-papeis-e-permissoes.md)). Aqui entra o que é específico de quem trabalha **dentro** da empresa: os papéis da equipe, que ficam numa tabela separada dos usuários dos clientes.

## Papéis sugeridos

| Papel | Pode | Não pode |
|---|---|---|
| Suporte | Ver clientes, linha do tempo, reenviar e-mail, impersonar com limite | Mexer em cobrança, apagar, exportar em massa |
| Financeiro | Ver faturas, reembolsar até um limite, ajustar cobrança | Impersonar, mudar permissões |
| Operação | Jobs, filas, flags, reprocessar webhook | Ver dado financeiro completo |
| Super admin | Gerir equipe e papéis, ações críticas com aprovação | Nada sem registro de auditoria |
| Somente leitura | Ver telas liberadas | Qualquer ação |

## Por que usar

- Credencial vazia ou erro humano de quem só lê não causa dano.
- Ex-funcionário: remover um papel é mais simples que revisar tudo.
- Auditoria e LGPD pedem acesso "por necessidade" ([doc 08](08-dados-pessoais-no-painel.md)).

## Quando usar

- Assim que houver a segunda pessoa na equipe. Com uma pessoa, o papel ainda ajuda: separa a conta do dia a dia da conta de super admin.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Editor e admin bastam |
| MVP de SaaS | ✅ Ótimo | Três papéis: suporte, financeiro e super admin |
| SaaS em crescimento | ✅ Ótimo | Permissões por ação e aprovação em duas pessoas |
| Sistema interno/corporativo | ✅ Ótimo | Papéis por área |
| API/integração | 🟡 Serve | Papel para quem gere chaves |
| App mobile com backend | ✅ Ótimo | Igual ao SaaS |
| Todo mundo como super admin | ❌ Evite | Um clique errado vira incidente |

## Quando é bom

- **Permissões por ação** (`refund.create`, `refund.limit.500`), não só por tela.
- **Tabela separada** para a equipe (`staff_users`): não mistura com `users` dos clientes.
- **Revisão trimestral** de quem tem o quê.
- **Aprovação em duas pessoas** para ação crítica: quem pede não aprova.

## Quando é ruim

- **Papel único "admin"** com tudo.
- **Esconder o botão** sem checar no servidor.
- **Aprovação por chat** sem registro no sistema.
- **Contas compartilhadas**: auditoria perde o "quem".

## Como começar

Fluxo de aprovação em duas pessoas, modelo (SQL):

```sql
create table approval_requests (
  id uuid primary key default gen_random_uuid(),
  action text not null,
  payload jsonb not null,
  requested_by uuid not null references staff_users(id),
  approved_by uuid references staff_users(id),
  status text not null default 'pending',
  created_at timestamptz not null default now(),
  decided_at timestamptz,
  check (approved_by is null or approved_by <> requested_by)
);
```

Execução (TypeScript):

```ts
async function aprovar(id: string, aprovadorId: string) {
  const pedido = await db.approvalRequest.findUniqueOrThrow({ where: { id } });
  if (pedido.requestedBy === aprovadorId) throw new Erro("Quem pede não aprova.");
  await db.approvalRequest.update({
    where: { id },
    data: { approvedBy: aprovadorId, status: "approved", decidedAt: new Date() },
  });
  await executar(pedido.action, pedido.payload);
  await auditar({ ator: aprovadorId, acao: `approve:${pedido.action}`, alvo: id });
}
```

Teste de negação por papel: [quality, doc 04](../../quality/docs/04-testes-de-api-e-contrato.md).

## Combina com / alternativas

- [Autenticação forte](04-autenticacao-forte-do-painel.md) e [ações perigosas](07-acoes-perigosas.md).
- [Auditoria](06-auditoria-do-que-a-equipe-faz.md): toda decisão fica registrada.

## Decisão rápida

- **Use** papéis por área, permissões por ação e dupla aprovação para dinheiro e exclusão.
- **Evite** super admin para todos e botões escondidos sem checagem no servidor.
