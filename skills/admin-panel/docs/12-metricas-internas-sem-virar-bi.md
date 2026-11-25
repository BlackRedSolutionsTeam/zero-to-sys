# Métricas internas sem virar BI

> Cinco números do negócio, calculados do próprio banco, numa tela só. Se a pergunta exige cruzar fontes, aí sim é caso de ferramenta de BI.

| | |
|---|---|
| **Referência** | Definições padrão de MRR, churn e ativação de SaaS (conceitos de mercado, sem fonte única; documente a fórmula que você adotar) |
| **Categoria** | Produto |
| **Tipo** | Prática de indicadores |
| **Vale para** | SaaS com assinatura |
| **Verificado em** | 2026-11-25 (as fórmulas abaixo são convenções; defina as suas por escrito) |

## O que é

Uma tela de resumo no painel com os números que o dono olha toda semana, calculados por consulta no banco ou numa tabela diária de totais.

## Por que usar

- O dono vê saúde do negócio sem pedir relatório.
- Mostra cedo problema de ativação ou aumento de cancelamento.

## Quando usar

- Quando houver cobrança recorrente. Antes disso, número de cadastros e ativação bastam.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Use a ferramenta de análise do site |
| MVP de SaaS | ✅ Ótimo | Três números bastam |
| SaaS em crescimento | ✅ Ótimo | Cinco números mais coorte simples |
| Sistema interno/corporativo | 🟡 Serve | Uso e volume |
| API/integração | ✅ Ótimo | Chamadas por cliente e por plano |
| App mobile com backend | 🟡 Serve | Ativação e retenção |

## Os cinco números

| Métrica | Fórmula sugerida |
|---|---|
| MRR | Soma da mensalidade normalizada das assinaturas ativas no fim do dia |
| Churn de clientes | Clientes que cancelaram no mês dividido pelos ativos no início do mês |
| Ativação | Contas novas que fizeram a ação-chave em N dias dividido pelas contas novas |
| Novos clientes pagantes | Primeira cobrança paga no período |
| Inadimplência | Faturas vencidas e não pagas dividido pelo total faturado |

## Quando é bom

- **Fórmula escrita** na própria tela ("o que é isso?").
- **Tabela diária de totais** (`metrics_daily`), preenchida por job, em vez de consulta pesada a cada abertura ([integrations, doc 06](../../integrations/docs/06-rotinas-agendadas.md)).
- **Mesma fonte do financeiro:** MRR confere com o provedor de pagamento.
- **Visão por empresa na ficha** (uso, plano, última atividade).

## Quando é ruim

- **Virar BI:** filtros infinitos, cruzamento de várias fontes, gráficos sob medida. Passe para uma ferramenta de BI e deixe o painel simples.
- **Consulta pesada no banco de produção** em horário de pico.
- **Métrica sem definição:** dois números diferentes para a mesma palavra.
- **Dado pessoal em agregado pequeno** que identifica pessoa.

## Como começar

Tabela e cálculo (SQL):

```sql
create table metrics_daily (
  day date primary key,
  mrr_cents bigint not null,
  active_customers int not null,
  new_paying int not null,
  churned int not null
);

insert into metrics_daily (day, mrr_cents, active_customers, new_paying, churned)
select current_date,
       coalesce(sum(case plan_interval when 'year' then price_cents / 12 else price_cents end), 0),
       count(*),
       count(*) filter (where first_paid_at::date = current_date),
       0
from subscriptions
where status = 'active'
on conflict (day) do update set
  mrr_cents = excluded.mrr_cents,
  active_customers = excluded.active_customers,
  new_paying = excluded.new_paying;
```

Gráficos: skill `dataviz` quando existir no ambiente; layout: [design-systems, doc 02](../../design-systems/docs/02-dashboard-analytics.md).

## Combina com / alternativas

- Alternativa: ferramenta de BI externa para análises cruzadas (fora desta skill).
- [O que um painel precisa ter](02-o-que-um-painel-precisa-ter.md): onde este módulo entra (prioridade 3).

## Decisão rápida

- **Use** cinco números com fórmula escrita e totais diários.
- **Evite** montar BI dentro do painel.
