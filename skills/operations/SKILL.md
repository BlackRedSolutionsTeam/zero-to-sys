---
name: operations
description: 'Organiza o que acontece depois do deploy: SLO e severidade, plantão para time pequeno, alertas, runbooks, incidentes e postmortem, página de status e suporte. Use quando o sistema entra no ar ou quando pedirem "plantão", "runbook", "incidente" ou "página de status".'
---

# operations

Guia para depois do deploy: acompanhar, responder a incidente, comunicar o cliente e aprender com cada queda. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim, modelos prontos e decisão rápida.

## Como usar esta skill

1. **Combine as metas e a severidade** antes do primeiro incidente ([doc 01](docs/01-slo-severidade-e-plantao.md)). Duas metas, quatro níveis, um revezamento.
2. **Crie poucos alertas**, cada um com ação ([doc 02](docs/02-alertas-que-valem-acordar.md)). Medir disco, CPU e uptime é da skill `vps` (doc 06) e da `infra` (doc 10).
3. **Escreva os runbooks** dos quatro problemas mais prováveis ([doc 03](docs/03-runbooks-modelo-e-primeiros.md)).
4. **No incidente**, siga o roteiro: confirmar, designar, conter, comunicar, resolver ([doc 04](docs/04-atender-um-incidente.md)). Contenha antes de investigar; volte a versão se houve deploy (skill `infra`, doc 14).
5. **Comunique** com a página de status e as mensagens prontas ([doc 05](docs/05-pagina-de-status-e-comunicacao.md)).
6. **Depois**, escreva o postmortem sem culpa ([doc 06](docs/06-postmortem-sem-culpa.md)) e leve as ações para o backlog (skill `product`).
7. **No dia a dia**, organize o suporte ([doc 07](docs/07-suporte-ao-cliente.md)) e faça a revisão mensal ([doc 08](docs/08-revisao-operacional-mensal.md)).

## O que fazer por situação

| Situação | Comece por |
|---|---|
| Primeiro cliente pagante chegando | Doc 01, 02 e 03 |
| O sistema está fora agora | Doc 04 e o runbook do doc 03 |
| Cliente pergunta "o que aconteceu" | Doc 05 e 06 |
| Cliente pede SLA em contrato | Doc 01 (meta honesta) e 08 |
| Muitos chamados repetidos | Doc 07 |
| Time cansado de ser acordado | Doc 02 e 01 (escala) |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| SLO, severidade e plantão | [docs/01-slo-severidade-e-plantao.md](docs/01-slo-severidade-e-plantao.md) | Metas, níveis, escala e ferramentas de plantão |
| Alertas | [docs/02-alertas-que-valem-acordar.md](docs/02-alertas-que-valem-acordar.md) | Página ou ticket, mensagem de alerta |
| Runbooks | [docs/03-runbooks-modelo-e-primeiros.md](docs/03-runbooks-modelo-e-primeiros.md) | Modelo e 4 primeiros |
| Atender um incidente | [docs/04-atender-um-incidente.md](docs/04-atender-um-incidente.md) | Roteiro e diagnóstico |
| Página de status | [docs/05-pagina-de-status-e-comunicacao.md](docs/05-pagina-de-status-e-comunicacao.md) | Ferramentas e mensagens de status |
| Postmortem | [docs/06-postmortem-sem-culpa.md](docs/06-postmortem-sem-culpa.md) | Modelo sem culpa |
| Suporte ao cliente | [docs/07-suporte-ao-cliente.md](docs/07-suporte-ao-cliente.md) | Triagem, SLA e backlog |
| Revisão mensal | [docs/08-revisao-operacional-mensal.md](docs/08-revisao-operacional-mensal.md) | Pauta e ata |

## Checklist

- [ ] Metas (SLO) e severidades escritas em `docs/operacao.md`.
- [ ] Escala de plantão com titular, reserva e canal que acorda (ligação, não só e-mail).
- [ ] Alertas de página só para o que exige ação imediata; o resto vira ticket.
- [ ] Runbooks dos 4 problemas principais no repositório, validados por quem não os escreveu.
- [ ] Monitor externo e página de status em outro servidor e outro domínio.
- [ ] Mensagens de status e e-mail ao cliente prontas.
- [ ] Modelo de postmortem no repositório e gatilhos definidos.
- [ ] Canal único de suporte com triagem por gravidade e prazos honestos.
- [ ] Revisão mensal agendada, com ata em `docs/operacao/`.
- [ ] Restauração de backup testada no último trimestre.

## Regras de uso

- **Conter antes de investigar.** Voltar a versão vale mais que descobrir a causa com o cliente parado.
- **Avisar cedo e de novo.** Primeira mensagem em 15 a 30 minutos; atualização no horário prometido.
- **Sem culpa.** O postmortem pergunta o que facilitou o erro, nunca quem errou.
- **Alerta sem ação não existe.** Cada alerta tem dono e runbook.
- **Meta honesta.** Não prometa o que uma infraestrutura de um servidor não entrega.
- **Preço só conferido.** Ferramentas de plantão e página de status mudam e acabam (o Grafana OnCall OSS foi arquivado e o Opsgenie encerra o suporte em 2027-04-05).
- **Fronteiras.** Medição técnica: skills `vps` e `infra`. Backup e rollback: `infra`. Proxy e diagnóstico de nginx: `nginx`. Borda, DNS e domínio: `cloudflare` e `domains`. Vazamento e invasão: `security`. Backlog e priorização: `product`.

## Quando a lista não cobre

Conformidade formal (ISO 27001, SOC 2), centro de operações 24 horas, SRE com orçamento de erro automatizado e resposta a incidente de segurança com prazo legal ficam fora desta skill. Diga isso e cubra com a documentação oficial e a skill `security`.

## Validade dos dados

Preços e limites de PagerDuty, Better Stack, Statuspage, Instatus, Chatwoot, HelpScout, Freshdesk e Crisp foram conferidos em 2026-11-25 nas páginas oficiais e mudam com frequência; cada documento tem a linha "Verificado em".
