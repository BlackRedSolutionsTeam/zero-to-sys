# SLO, severidade e quem atende

> Combine, antes do primeiro problema, o quanto o sistema precisa funcionar, o que é grave e quem responde quando quebra.

| | |
|---|---|
| **Referência** | https://sre.google/sre-book/service-level-objectives/, https://www.pagerduty.com/pricing/incident-management/, https://betterstack.com/pricing |
| **Categoria** | Operação |
| **Tipo** | Prática de combinados do time, com ferramentas de plantão |
| **Vale para** | Qualquer sistema com usuário real, inclusive time de uma ou duas pessoas |
| **Verificado em** | 2026-11-25 |

## O que é

- **SLI** é o número que mede o serviço (por exemplo, a porcentagem de requisições que dão certo).
- **SLO** é a meta para esse número (por exemplo, 99,5% no mês).
- **SLA** é o contrato com o cliente, com consequência (desconto, multa) se a meta falhar. Sem consequência escrita, é só um SLO.
- **Orçamento de erro** é o quanto você pode errar sem estourar a meta. Se sobra, pode arriscar mais releases; se acabou, estabilize antes de lançar.
- **Severidade** é o nível de gravidade de um incidente, que define quem acorda e em quanto tempo.
- **Plantão** é quem está de olho e responde fora do horário.

A fonte oficial (livro de SRE do Google) recomenda partir do que o usuário percebe, ter poucos SLOs e começar com uma meta folgada para apertar depois, nunca o contrário.

## Por que usar

- Evita discutir às 3 da manhã se "isso é grave".
- Transforma "o sistema é estável" em número.
- Decide o que entra no [alerta que acorda](02-alertas-que-valem-acordar.md) e o que espera a manhã.
- Dá base honesta para o que prometer em contrato.

## Quando usar

- Antes do primeiro cliente pagante.
- Quando um cliente pedir disponibilidade em contrato.
- Quando o time passar a ter mais de uma pessoa que mexe em produção.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Uma meta de disponibilidade e um monitor bastam |
| MVP de SaaS | ✅ Ótimo | Duas metas simples evitam heróis e pânico |
| SaaS em crescimento | ✅ Ótimo | Orçamento de erro ajuda a decidir entre feature e estabilidade |
| Sistema interno | 🟡 Serve | Horário comercial costuma bastar; escreva isso |
| API de integração | ✅ Ótimo | O cliente depende da sua meta para a dele |
| Prometer 99,99% sem estrutura | ❌ Evite | Pede redundância que um servidor só não entrega |

## Quando é bom

- **Poucas metas:** disponibilidade e taxa de erro (ou latência) cobrem a maioria.
- **Meta em minutos de queda** é mais fácil de entender que porcentagem.
- **Plantão enxuto:** com 2 a 3 pessoas, revezamento semanal e só o crítico acorda.
- **Severidade escrita** reduz decisão no susto.

## Quando é ruim

- **Meta copiada de grande empresa:** 99,99% dá cerca de 4 minutos de queda por mês; uma VPS única não sustenta.
- **Plantão sem compensação** esgota o time; combine folga ou pagamento.
- **Muitas severidades:** quatro níveis bastam.
- **SLA sem SLO por baixo:** você promete o que não mede.

## Como começar

Quanto cada meta permite de queda por mês (30 dias):

| Meta | Queda permitida por mês |
|---|---|
| 99% | cerca de 7 h 12 min |
| 99,5% | cerca de 3 h 36 min |
| 99,9% | cerca de 43 min |
| 99,95% | cerca de 21 min |

Arquivo `docs/operacao.md` no repositório, com este conteúdo:

```markdown
# Operação de clinica-exemplo

## Metas (SLO)
- Disponibilidade do app e da API: 99,5% por mês, medida pelo monitor externo.
- Requisições da API com sucesso (sem 5xx): 99% por mês.
- Revisão das metas: a cada 3 meses.

## Severidade
| Nível | Quando | Resposta | Quem |
|---|---|---|---|
| SEV1 | Sistema fora para todos, perda de dado ou vazamento | Agora, a qualquer hora | Plantonista e responsável técnico |
| SEV2 | Função principal quebrada ou lenta para muitos | Até 30 min, horário estendido | Plantonista |
| SEV3 | Função secundária quebrada, existe contorno | Próximo dia útil | Quem estiver de suporte |
| SEV4 | Incômodo, sem impacto no uso | Backlog | Triagem semanal |

## Plantão
- Revezamento semanal, troca na segunda às 09:00.
- Titular: Ana. Reserva: Bruno. Se o titular não confirmar em 10 min, aciona o reserva.
- Fora do horário comercial só SEV1 acorda; SEV2 espera até as 07:30.
- Contatos e senhas de emergência: cofre do time (nunca neste arquivo).
```

Ferramentas para o chamado de plantão (preços conferidos em 2026-11-25 nas páginas oficiais):

| Ferramenta | Plano grátis | Pago |
|---|---|---|
| PagerDuty | Free: 5 usuários, 1 agenda de plantão, 1 política de escalonamento, SMS e ligação limitados a 100 por mês | Professional: US$ 21 por usuário/mês no anual, US$ 25 no mensal |
| Better Stack | 10 monitores e heartbeats, 1 página de status, alertas por Slack e e-mail | Licença de responsável (plantão): US$ 29 por mês no anual, US$ 34 no mensal |
| Grafana OnCall OSS | Arquivado em 2026-03-24 e somente leitura; o Cloud Connection (SMS, ligação, push) acabou na mesma data | Evite em projeto novo; o produto segue no Grafana Cloud IRM |
| Opsgenie | Fim de venda em 2025-06-04 | Fim de suporte em 2027-04-05; não adote |

Time de uma pessoa: o plano grátis do PagerDuty ou o Better Stack já ligam o celular com ligação; sem isso, alerta por e-mail às 3 da manhã não acorda ninguém.

## Combina com / alternativas

- [Alertas que valem acordar](02-alertas-que-valem-acordar.md) e [atender um incidente](04-atender-um-incidente.md).
- Monitoramento e limites técnicos: [monitoramento da VPS](../../vps/docs/06-monitoramento-e-alertas.md) e [observabilidade](../../infra/docs/10-observabilidade.md).
- Alternativa sem ferramenta: telefone do plantonista num grupo de mensagens, só para SEV1, enquanto o time é minúsculo.

## Decisão rápida

- **Use se:** há cliente real; escreva 2 metas, 4 severidades e um revezamento, e revise a cada trimestre.
- **Evite se:** a intenção é prometer 99,99% sem redundância; comece folgado e aperte com dados.
