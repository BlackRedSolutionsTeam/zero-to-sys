# O que um painel precisa ter

> Comece pelo que a equipe faz todo dia (achar o cliente, ver o que aconteceu, corrigir) e deixe o resto para quando houver dor.

| | |
|---|---|
| **Referência** | Prática de operação de SaaS; OWASP ASVS (v5) para requisitos de controle de acesso e registro; documentação das ferramentas do [doc 01](01-construir-comprar-ou-gerar.md) |
| **Categoria** | Escopo |
| **Tipo** | Checklist de funcionalidades |
| **Vale para** | SaaS, sistemas internos e e-commerce com equipe de suporte, financeiro ou operação |
| **Verificado em** | 2026-11-25 (ASVS: nome da referência, versão e capítulos não reconferidos nesta data) |

## O que é

A lista de módulos de um painel administrativo, em ordem de prioridade, com o que cada um precisa mostrar e permitir.

## Por que usar

- Evita o painel de "uma tabela por tabela do banco", que ninguém consegue usar.
- Mostra o que dá para adiar sem prejudicar o suporte.
- Cada módulo já aponta quem deve ter acesso e o que precisa ser auditado.

## Quando usar

- Ao planejar o painel antes de escolher a ferramenta.
- Ao receber o pedido "preciso mexer no cliente sem ligar pro dev".

## Módulos, por prioridade

| Prioridade | Módulo | O que tem | Ação de risco |
|---|---|---|---|
| 1 | Usuários e empresas | Busca, perfil, status, papéis, último acesso, convites | Bloquear, trocar e-mail, excluir |
| 1 | Assinaturas e cobranças | Plano, status, faturas, tentativas de pagamento | Reembolsar, trocar plano, dar crédito |
| 1 | Suporte | Linha do tempo do cliente, notas internas, atalho para impersonar | Impersonar |
| 2 | Configurações | Limites por plano, textos, parâmetros do sistema | Mudar limite global |
| 2 | Feature flags | Liga e desliga recurso por empresa ou percentual | Ligar para todos |
| 2 | Jobs e filas | Pendentes, falhos, reprocessar | Reprocessar em lote |
| 3 | Logs e saúde | Erros recentes, status de integrações, versão publicada | Nenhuma (somente leitura) |
| 3 | Métricas internas | MRR, churn, ativação ([doc 12](12-metricas-internas-sem-virar-bi.md)) | Nenhuma |

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Usuários e configurações bastam |
| MVP de SaaS | ✅ Ótimo | Módulos de prioridade 1 e um job de reprocessar |
| SaaS em crescimento | ✅ Ótimo | Todos, mais feature flags e saúde |
| Sistema interno/corporativo | 🟡 Serve | O próprio sistema já é interno; foque em configurações e logs |
| API/integração | ✅ Ótimo | Chaves, uso, webhooks com falha |
| App mobile com backend | ✅ Ótimo | Usuários, versões e flags |
| Projeto sem ninguém na equipe de suporte | ❌ Evite | Construa depois, quando houver demanda |

## O que entra no MVP e o que fica para depois

O painel é parte do backlog do sistema, não um extra. Planeje-o junto com o produto.

| Fase | Entra | Gatilho |
|---|---|---|
| MVP do sistema | Busca de usuário e empresa, ficha, bloquear e desbloquear, papéis (suporte e super admin), 2FA, tabela de auditoria, banner de impersonação se houver suporte | Antes do primeiro cliente pagante |
| Primeiros clientes | Assinaturas e cobranças, reprocessar job e webhook, modo somente leitura, aprovação em duas pessoas | Primeira cobrança em produção |
| Crescimento | Feature flags, configurações por plano, logs e saúde, métricas, exportação controlada, papel de financeiro e operação | Equipe com mais de 3 pessoas ou mais de 50 clientes |

Sem painel no MVP, a equipe acaba usando o banco direto, sem papel nem auditoria. Roteiro completo em [13-roteiro-de-construcao-por-stack.md](13-roteiro-de-construcao-por-stack.md).

## Quando é bom

- **Um módulo por pergunta frequente do suporte:** "por que cobrou?", "por que não recebeu e-mail?".
- **Somente leitura primeiro:** entregar consulta sem ação reduz o risco do primeiro mês.
- **Feature flag com histórico** de quem ligou e quando.

## Quando é ruim

- **Editar qualquer campo de qualquer tabela:** o suporte quebra invariantes (plano ativo sem assinatura).
- **Duplicar regra do produto no painel:** a regra muda num lado só.
- **Painel que lê tabelas de outras empresas sem filtro** ([doc 09](09-multiempresa-visao-da-equipe.md)).

## Como começar

Modelo mínimo de flag por empresa (SQL):

```sql
create table feature_flags (
  key text primary key,
  description text not null,
  enabled_default boolean not null default false
);

create table feature_flag_overrides (
  flag_key text not null references feature_flags(key),
  tenant_id uuid not null references tenants(id),
  enabled boolean not null,
  changed_by uuid not null references staff_users(id),
  changed_at timestamptz not null default now(),
  primary key (flag_key, tenant_id)
);
```

Jobs e webhooks: veja [integrations, doc 04](../../integrations/docs/04-webhooks.md) e [doc 05](../../integrations/docs/05-filas-e-jobs.md). Telas: [doc 10](10-telas-operacionais.md).

## Combina com / alternativas

- [Quem acessa](03-quem-acessa-papeis-e-menor-privilegio.md): cada módulo vira permissões.
- [Operations, doc 07](../../operations/docs/07-suporte-ao-cliente.md): o fluxo de suporte que o painel atende.

## Decisão rápida

- **Use** a tabela de prioridades: entregue o 1, depois o 2.
- **Evite** telas genéricas de edição de tabela; crie ações com nome ("reembolsar", "reprocessar").
