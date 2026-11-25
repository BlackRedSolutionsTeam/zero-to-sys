# Alertas que valem acordar alguém

> Separe o que exige ação imediata do que só precisa ser visto de manhã, para que o alerta continue sendo levado a sério.

| | |
|---|---|
| **Referência** | https://sre.google/sre-book/monitoring-distributed-systems/, https://github.com/louislam/uptime-kuma, https://www.pagerduty.com/pricing/incident-management/ |
| **Categoria** | Operação |
| **Tipo** | Prática de desenho de alertas |
| **Vale para** | Qualquer sistema em produção; limites técnicos por servidor ficam na skill vps |
| **Verificado em** | 2026-11-25 |

## O que é

Alerta é uma mensagem automática de que algo passou do limite. Esta prática decide **qual alerta chama a pessoa** (página, ligação) e **qual só deixa um aviso** (ticket, e-mail). Como medir CPU, disco e uptime está em [monitoramento da VPS](../../vps/docs/06-monitoramento-e-alertas.md); aqui o foco é o que merece acordar.

## Por que usar

- Alerta demais vira ruído, e o importante passa.
- Quem acorda sem necessidade pede demissão do plantão.
- Cada alerta ligado a uma ação ([runbook](03-runbooks-modelo-e-primeiros.md)) encurta o incidente.

## Quando usar

- Ao ligar o primeiro monitor.
- Depois de cada incidente: o que avisou tarde ou avisou sem importar?
- Na [revisão mensal](08-revisao-operacional-mensal.md), contando quantos alertas viraram ação.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Só "site fora"; o resto é e-mail |
| MVP de SaaS | ✅ Ótimo | Três alertas bem escolhidos |
| SaaS em crescimento | ✅ Ótimo | Alerta por sintoma do usuário, não por máquina |
| Sistema interno | 🟡 Serve | Avise no horário comercial, sem plantão |
| API de integração | ✅ Ótimo | Erro 5xx e latência importam ao cliente |
| Alerta de CPU sem consequência | ❌ Evite | Gera barulho sem ação |

## Quando é bom

- **Alerta por sintoma** (o usuário não consegue entrar) em vez de causa (CPU alta).
- **Dois níveis:** página (acorda) e ticket (resolve de dia).
- **Cada alerta tem dono e runbook.**
- **Alerta de ausência:** o backup que não avisou que terminou.

## Quando é ruim

- **Alerta instantâneo** dispara com oscilação de rede; exija 2 falhas seguidas.
- **Limite chutado** sem olhar o histórico.
- **Mesmo canal para tudo:** o crítico se perde entre avisos.
- **Alerta que ninguém sabe resolver** não é alerta, é ansiedade.

## Como começar

Teste por alerta: "se disparar às 3 da manhã, existe algo que uma pessoa faz agora e que não pode esperar até as 8?". Se não, vira ticket.

| Alerta | Nível | Condição |
|---|---|---|
| Site ou API fora | Página | 2 falhas seguidas do monitor externo |
| Taxa de erro 5xx alta | Página | acima de 5% por 5 minutos |
| Backup sem aviso | Ticket de manhã | sem sinal em 26 horas |
| Disco quase cheio | Página se acima de 95%, ticket se acima de 80% | medido no servidor |
| Certificado perto do vencimento | Ticket | menos de 14 dias |
| Fila acumulando | Página se parada, ticket se lenta | itens sem consumo por 15 minutos |
| Erro novo no Sentry | Ticket | primeira ocorrência de um erro |
| CPU alta | Nenhum, só painel | só alerta se a latência subir junto |

Mensagem de alerta que ajuda quem acorda (modelo):

```text
[SEV2] API clinica-exemplo com 5xx acima de 5% há 5 min
Impacto: agendamento falha para parte dos clientes
Painel: https://grafana.clinica-exemplo.com.br/d/api
Runbook: docs/runbooks/api-com-erro.md
Última mudança: deploy v1.42 às 14:03
```

Monitor de heartbeat para tarefa agendada (padrão do Uptime Kuma, tipo Push): o script chama a URL ao final; sem chamada no prazo, vem o alerta.

```bash
pg_dump -Fc clinica | gzip > /backup/clinica.sql.gz && curl -fsS "https://status.clinica-exemplo.com.br/api/push/TOKEN?status=up"
```

## Combina com / alternativas

- [SLO, severidade e plantão](01-slo-severidade-e-plantao.md): a severidade define o canal.
- [Monitoramento da VPS](../../vps/docs/06-monitoramento-e-alertas.md) para limites de disco, RAM e CPU; [observabilidade](../../infra/docs/10-observabilidade.md) para erros e traços.
- Alternativa para poucos recursos: um único canal de mensagens com menção só para SEV1.

## Decisão rápida

- **Use se:** quer poucos alertas, cada um com ação e dono.
- **Evite se:** a ideia é alertar toda métrica "por segurança"; o ruído derruba a confiança.
