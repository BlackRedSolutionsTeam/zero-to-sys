# Auditoria de tudo o que a equipe faz

> Registre quem fez, o quê, quando, em qual registro, o valor antes e depois e de onde, numa tabela que ninguém altera nem apaga.

| | |
|---|---|
| **Referência** | OWASP Logging Cheat Sheet (cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html); PostgreSQL docs: privilégios (postgresql.org/docs/current/ddl-priv.html) e triggers |
| **Categoria** | Segurança e dados |
| **Tipo** | Prática de rastreabilidade |
| **Vale para** | Todo painel; modelagem geral de auditoria na skill `data` |
| **Verificado em** | 2026-11-25 (links de referência não reabertos nesta data) |

## O que é

Um log de auditoria de **ações da equipe**, separado do histórico de dados do produto. O modelo geral (triggers, histórico, soft delete) está em [data, doc 07](../../data/docs/07-auditoria-historico-soft-delete.md); aqui está o que o painel acrescenta.

## Por que usar

- Responder "quem mudou o plano desse cliente?" em segundos.
- Provar que a equipe só acessou dado com motivo.
- Dissuadir abuso e achar erro humano.

## Quando usar

- Desde o primeiro dia do painel, antes da primeira ação de escrita.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Histórico de publicação basta |
| MVP de SaaS | ✅ Ótimo | Uma tabela e uma função |
| SaaS em crescimento | ✅ Ótimo | Com retenção e exportação |
| Sistema interno/corporativo | ✅ Ótimo | Exigência comum de auditoria |
| API/integração | ✅ Ótimo | Quem criou e revogou chave |
| App mobile com backend | ✅ Ótimo | Igual ao SaaS |
| Painel sem registro de ação | ❌ Evite | Sem "quem", não há investigação |

## O que gravar

| Campo | Exemplo |
|---|---|
| Ator real | `staff_id`, e-mail, papel |
| Ator exibido | cliente impersonado, se houver |
| Ação | `refund.create`, `user.block`, `impersonate.start` |
| Alvo | tipo e id do registro e da empresa |
| Antes e depois | só os campos que mudaram |
| Motivo e ticket | texto livre e número |
| Origem | IP, agente de navegador, id da requisição |
| Quando | `timestamptz` do servidor |
| Resultado | sucesso, negado, erro |

Leituras de dado pessoal sensível também entram (quem abriu a ficha, quem exportou), mas em tabela própria para não afogar o resto.

## Quando é bom

- **Imutável:** o usuário de aplicação tem só `insert` e `select`, sem `update` nem `delete`.
- **Gravar na mesma transação** da ação: se a ação falha, não há registro falso; se grava, o registro existe.
- **Sem segredo no registro:** senha, token, número de cartão e CPF completo ficam fora ou mascarados.
- **Cópia externa** (armazenamento só de anexação) para o caso de invasão do banco principal.
- **Tela de consulta** no painel, só para super admin e auditor, com filtro por ator, alvo e período.

## Quando é ruim

- **Log em arquivo de texto** que o app reescreve.
- **Guardar o objeto inteiro** a cada mudança: pesado e cheio de dado pessoal.
- **Auditar só escrita pelo painel** e esquecer o script de produção ou o acesso direto ao banco.

## Como começar

Tabela (SQL):

```sql
create table staff_audit_log (
  id bigint generated always as identity primary key,
  occurred_at timestamptz not null default now(),
  staff_id uuid not null,
  impersonated_user_id uuid,
  action text not null,
  target_type text not null,
  target_id text not null,
  tenant_id uuid,
  before jsonb,
  after jsonb,
  reason text,
  ticket text,
  ip inet,
  request_id text,
  result text not null default 'ok'
);

revoke update, delete, truncate on staff_audit_log from app_user;
grant insert, select on staff_audit_log to app_user;
```

Função de gravação na transação (TypeScript):

```ts
export async function agir<T>(ctx: Ctx, acao: string, alvo: Alvo, mudar: (tx: Tx) => Promise<{ antes: unknown; depois: unknown; valor: T }>) {
  return db.$transaction(async (tx) => {
    const r = await mudar(tx);
    await tx.staffAuditLog.create({
      data: {
        staffId: ctx.staffId,
        impersonatedUserId: ctx.impersonandoId,
        action: acao,
        targetType: alvo.tipo,
        targetId: alvo.id,
        tenantId: alvo.empresaId,
        before: r.antes,
        after: r.depois,
        reason: ctx.motivo,
        ticket: ctx.ticket,
        ip: ctx.ip,
        requestId: ctx.requestId,
      },
    });
    return r.valor;
  });
}
```

Toda ação do painel passa por `agir`; não existe rota que altere dado sem ela. Retenção do log: veja [data, doc 10](../../data/docs/10-dados-pessoais-e-lgpd.md).

## Combina com / alternativas

- [Ações perigosas](07-acoes-perigosas.md), [impersonação](05-impersonacao-entrar-como-cliente.md) e [dados pessoais](08-dados-pessoais-no-painel.md).
- Alternativa em Postgres: triggers gerais ([data, doc 07](../../data/docs/07-auditoria-historico-soft-delete.md)), que pegam também o acesso fora do painel, mas sem motivo e ator humano.

## Decisão rápida

- **Use** uma tabela só de inserção, gravada na mesma transação, com antes, depois, motivo e ator real.
- **Evite** log em arquivo, objeto inteiro e dado sensível sem máscara.
