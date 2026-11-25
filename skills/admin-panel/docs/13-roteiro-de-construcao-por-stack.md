# Roteiro de construção do painel, por stack

> Nove passos, em ordem, do escopo do MVP até o deploy protegido, com exemplo de papéis, auditoria e permissão em Next.js, ASP.NET Core, Laravel e Django.

| | |
|---|---|
| **Referência** | Documentação oficial: Next.js (nextjs.org/docs), ASP.NET Core authorization (learn.microsoft.com/aspnet/core/security/authorization/), Laravel Gates e Policies (laravel.com/docs/authorization), Django permissions (docs.djangoproject.com/en/stable/topics/auth/default/) |
| **Categoria** | Roteiro |
| **Tipo** | Passo a passo |
| **Vale para** | Quem constrói um sistema do zero e vai incluir o painel no backlog |
| **Verificado em** | 2026-11-25 (os trechos de código seguem as APIs documentadas; não foram executados nesta data) |

## O que é

O caminho completo para criar o painel administrativo de um sistema novo. Cada passo aponta para o doc de detalhe e termina com uma checklist de pronto.

## Quando usar

- Ao montar o backlog de um sistema novo (junto com a skill `zero-to-sys`).
- Ao adicionar um painel a um sistema que hoje é operado por SQL manual.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Passos 1 a 3 e 9 bastam |
| MVP de SaaS | ✅ Ótimo | Passos 1 a 6 antes do primeiro cliente |
| SaaS em crescimento | ✅ Ótimo | Todos os passos |
| Sistema interno/corporativo | ✅ Ótimo | Passos 3, 6 e 8 em foco |
| API/integração | ✅ Ótimo | Painel de chaves e webhooks |
| App mobile com backend | ✅ Ótimo | Painel web da equipe |

## Passo 1: escopo do MVP do painel

Parta do produto: liste as 10 perguntas que o suporte vai fazer e as 5 ações que só um dev faria. Escolha da [tabela de fases](02-o-que-um-painel-precisa-ter.md).

- [ ] Lista de perguntas e ações escrita.
- [ ] Cada item vinculado a uma tela e a um papel.
- [ ] Itens do painel entraram no backlog do sistema com prioridade.

## Passo 2: construir, gerar ou comprar

Decisão em [doc 01](01-construir-comprar-ou-gerar.md). Regra: ação de dinheiro, acesso ou dado pessoal pede código seu.

- [ ] Opção escolhida e licença conferida na data.
- [ ] Custo por pessoa da equipe calculado.

## Passo 3: papéis internos e autenticação forte

Modelo de papéis (SQL), separado dos usuários dos clientes:

```sql
create table staff_users (
  id uuid primary key default gen_random_uuid(),
  email text not null unique,
  name text not null,
  active boolean not null default true,
  mfa_enrolled_at timestamptz,
  created_at timestamptz not null default now()
);

create table staff_roles (
  id uuid primary key default gen_random_uuid(),
  name text not null unique
);

create table staff_permissions (
  role_id uuid not null references staff_roles(id),
  code text not null,
  max_amount_cents bigint,
  primary key (role_id, code)
);

create table staff_user_roles (
  staff_id uuid not null references staff_users(id),
  role_id uuid not null references staff_roles(id),
  primary key (staff_id, role_id)
);
```

Detalhes: [doc 03](03-quem-acessa-papeis-e-menor-privilegio.md) e [doc 04](04-autenticacao-forte-do-painel.md).

- [ ] Tabela de equipe separada da de clientes.
- [ ] 2FA obrigatório e testado.
- [ ] Papel mínimo por pessoa; ninguém compartilha conta.

## Passo 4: estrutura de pastas e rotas, painel separado do produto

Decisão em [doc 11](11-painel-separado-do-produto.md); pastas pela skill `architecture`.

| Stack | Estrutura |
|---|---|
| Next.js | `app/(admin)/admin/` com `layout.tsx` que valida a sessão de equipe; `lib/admin/` com `permissoes.ts` e `auditoria.ts` |
| ASP.NET Core | Projeto `Admin` ou Area `Admin`; `Admin/Auditoria/`, `Admin/Permissoes/` |
| Laravel | `app/Filament/Resources/`, `app/Policies/`, `app/Models/StaffUser.php`, guard `staff` em `config/auth.php` |
| Django | `staff/` como app com `models.py`, `permissions.py`, `admin.py`; URLs sob `admin.` |

- [ ] Subdomínio e rota do painel definidos.
- [ ] Guard de equipe distinto do guard de clientes.

## Passo 5: telas mínimas primeiro

Busca global, ficha do cliente e as ações de suporte de menor risco ([doc 10](10-telas-operacionais.md)). Layout: [design-systems, doc 03](../../design-systems/docs/03-admin-crud.md).

- [ ] Busca acha por e-mail, CPF e id.
- [ ] Ficha com linha do tempo.
- [ ] Todas as telas leem por papel.

## Passo 6: auditoria desde a primeira ação

Tabela e função em [doc 06](06-auditoria-do-que-a-equipe-faz.md). Regra: nenhuma rota de escrita sem passar por ela.

- [ ] `staff_audit_log` só com insert e select.
- [ ] Teste falha se uma ação de escrita não gravar registro.

## Passo 7: ações perigosas, impersonação e dados pessoais

[Doc 07](07-acoes-perigosas.md), [doc 05](05-impersonacao-entrar-como-cliente.md) e [doc 08](08-dados-pessoais-no-painel.md).

- [ ] Confirmação específica, soft delete e limite de lote.
- [ ] Impersonação com motivo, 15 minutos, banner e leitura por padrão.
- [ ] CPF e e-mail mascarados no servidor.

## Passo 8: testes de permissão

Para cada papel e cada ação sensível, um teste de negação e um de permissão ([quality, doc 04](../../quality/docs/04-testes-de-api-e-contrato.md)).

- [ ] Suporte não reembolsa; financeiro não impersonar.
- [ ] Cliente de outra empresa recebe 404.
- [ ] Sem 2FA, 403.

## Passo 9: deploy isolado e proteção na borda

[Doc 11](11-painel-separado-do-produto.md), [cloudflare, doc 07](../../cloudflare/docs/07-access-e-zero-trust.md) e [infra](../../infra/SKILL.md).

- [ ] Deploy do painel independente.
- [ ] Access ou Tunnel na frente, `noindex`, sem cookie compartilhado.

## Exemplos de permissão por stack

Next.js (TypeScript), guarda no servidor em cada ação:

```ts
import { redirect } from "next/navigation";

export async function exigirPermissao(codigo: string) {
  const staff = await sessaoDaEquipe();
  if (!staff || !staff.mfa) redirect("/admin/entrar");
  if (!staff.permissoes.includes(codigo)) throw new Error("Sem permissão.");
  return staff;
}

export async function reembolsar(faturaId: string, motivo: string) {
  "use server";
  const staff = await exigirPermissao("refund.create");
  return agir({ staffId: staff.id, motivo }, "refund.create", { tipo: "fatura", id: faturaId }, () => estornar(faturaId));
}
```

ASP.NET Core (C#), política por permissão:

```csharp
builder.Services.AddAuthorization(o =>
{
    o.AddPolicy("RefundCreate", p => p.RequireClaim("permission", "refund.create").RequireClaim("mfa", "true"));
});

app.MapPost("/admin/faturas/{id:guid}/reembolsar",
    async (Guid id, RefundRequest req, RefundService svc, ClaimsPrincipal user) =>
        Results.Ok(await svc.RefundAsync(id, req.Reason, user.GetStaffId())))
   .RequireAuthorization("RefundCreate");
```

Laravel (PHP), policy e resource do Filament:

```php
Gate::define('refund.create', fn (StaffUser $s) => $s->hasPermission('refund.create') && $s->mfa_verified);

Tables\Actions\Action::make('reembolsar')
    ->authorize(fn () => Gate::allows('refund.create'))
    ->requiresConfirmation()
    ->form([Forms\Components\Textarea::make('motivo')->required()])
    ->action(fn (Fatura $fatura, array $data) => app(Estorno::class)->executar($fatura, $data['motivo']));
```

Django (Python), permissão de modelo e auditoria:

```python
from django.contrib.admin import ModelAdmin, action
from django.db import transaction

class FaturaAdmin(ModelAdmin):
    actions = ["reembolsar"]

    @action(description="Reembolsar", permissions=["refund"])
    def reembolsar(self, request, queryset):
        with transaction.atomic():
            for fatura in queryset[:100]:
                estornar(fatura)
                StaffAuditLog.objects.create(staff=request.user, action="refund.create", target_id=str(fatura.pk))

    def has_refund_permission(self, request):
        return request.user.has_perm("faturas.refund")
```

Tabela de auditoria: [doc 06](06-auditoria-do-que-a-equipe-faz.md).

## Checklist de pronto do painel

- [ ] Painel no backlog do sistema, com MVP e fases.
- [ ] Equipe em tabela própria, com papéis mínimos e 2FA obrigatório.
- [ ] Painel em subdomínio próprio, atrás de Access ou Tunnel.
- [ ] Toda escrita grava auditoria imutável com motivo e ator real.
- [ ] Ações perigosas com confirmação, limite e modo somente leitura.
- [ ] Impersonação com banner, limite de tempo e aviso.
- [ ] Dados pessoais mascarados no servidor; exportação controlada.
- [ ] Testes de permissão por papel e por empresa passando no CI.
- [ ] Runbook de "perdi o 2FA" e "saiu alguém da equipe" escrito.

## Combina com / alternativas

- Skills `security`, `data`, `legal`, `design-systems`, `operations`, `integrations`, `cloudflare`, `quality`.

## Decisão rápida

- **Use** o roteiro como épico do backlog: passos 1 a 6 antes do primeiro cliente, 7 a 9 antes da primeira cobrança.
- **Evite** deixar o painel "para depois" sem prever o acesso por SQL manual.
