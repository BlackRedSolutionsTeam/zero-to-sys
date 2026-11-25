# Monitoramento e alertas da VPS

> Vigie disco, CPU e RAM por dentro e o site por fora, e mande o alerta para um lugar que você realmente olha.

| | |
|---|---|
| **Referência** | https://github.com/louislam/uptime-kuma, https://github.com/netdata/netdata, https://github.com/prometheus/node_exporter, https://grafana.com/pricing/ |
| **Categoria** | Servidor |
| **Tipo** | Prática de monitoramento e alerta |
| **Vale para** | VPS com Docker, com ou sem Coolify/Dokploy |
| **Verificado em** | 2026-11-25 |

## O que é

Dois tipos de vigilância que se completam:

- **Monitor interno:** mede o servidor por dentro (uso de disco, CPU, RAM, contêineres). Ferramentas: Netdata ou **node_exporter** com Prometheus e Grafana.
- **Monitor externo (uptime):** testa o site por fora, como o usuário. Se o servidor inteiro cair, o monitor interno cai junto e não avisa; só o externo avisa.

**Alerta** é a mensagem (Telegram, e-mail, Slack) enviada quando algo passa do limite. Mais observabilidade de aplicação (logs, erros) está em [observabilidade](../../infra/docs/10-observabilidade.md).

## Por que usar

- Disco cheio é a causa mais comum de VPS fora do ar, e é previsível.
- Você descobre a queda antes do cliente.
- Dados de CPU e RAM ajudam a decidir quando [dimensionar o servidor](02-dimensionar-o-servidor.md) de novo.

## Quando usar

- Desde o primeiro dia em produção, pelo menos o monitor externo.
- Quando houver mais de um serviço no mesmo servidor.
- Quando um cliente exigir disponibilidade medida.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Um monitor externo gratuito já basta |
| MVP de SaaS | ✅ Ótimo | Uptime Kuma mais alerta de disco, quase sem custo |
| SaaS em crescimento | ✅ Ótimo | Netdata ou Prometheus com Grafana e alertas por gravidade |
| Sistema interno/corporativo | ✅ Ótimo | Disponibilidade vira número para relatório |
| API/integração | ✅ Ótimo | Teste o endpoint de saúde e o tempo de resposta |
| App mobile com backend | ✅ Ótimo | O usuário não vê a causa, só o app quebrado |
| Monitor só dentro da mesma VPS | ❌ Evite | Se o servidor cair, ninguém é avisado |

## Quando é bom

- **Uptime Kuma:** licença MIT; testa HTTP, TCP, DNS, ping e Docker, e envia para mais de 90 serviços de notificação (conferido em 2026-11-25). Roda em um contêiner pequeno.
- **Netdata Agent:** licença GPL v3+; painel pronto com métricas e alertas. O Netdata Cloud tem plano Community gratuito para até 5 nós; o Business começa em US$ 7 por nó por mês no plano anual (conferido em 2026-11-25).
- **node_exporter:** licença Apache 2.0; escuta na porta 9100 e é o padrão do ecossistema Prometheus (conferido em 2026-11-25).
- **Grafana:** a edição de código aberto usa AGPLv3. O Grafana Cloud gratuito inclui 10 mil séries ativas de métricas, 14 dias de retenção e 3 usuários (conferido em 2026-11-25).
- **UptimeRobot:** plano gratuito com 50 monitores a cada 5 minutos (conferido em 2026-11-25); bom como segundo monitor externo.

## Quando é ruim

- **Uptime Kuma na mesma VPS que monitora** perde a utilidade na queda total. Rode em outro servidor, na máquina de casa ou use um serviço externo.
- **Prometheus com Grafana** dá trabalho: são quatro peças para manter e a retenção ocupa disco.
- **AGPLv3** exige atenção se você modificar o Grafana e oferecer como serviço; para uso interno costuma bastar.
- **Alerta demais:** se tudo apita, ninguém olha. Alerte só o que exige ação.
- **Netdata Cloud** é serviço fechado; o Agent funciona sozinho, mas confira os planos antes de ligar várias máquinas.

## Como começar

Uptime Kuma (no comando oficial usa `--restart=always`; aqui `unless-stopped`):

```bash
docker run -d --restart unless-stopped -p 127.0.0.1:3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:2
```

Publique a porta 3001 só atrás de proxy com HTTPS e login, nunca aberta ao mundo. Crie estes monitores:

- `https://app.clinica-exemplo.com.br` a cada 60 segundos;
- `https://api.clinica-exemplo.com.br/saude` com checagem de palavra-chave;
- vencimento do certificado TLS;
- um monitor do tipo Push para o backup noturno (o script chama a URL ao terminar; sem chamada, vem o alerta).

node_exporter em contêiner, como na documentação oficial:

```bash
docker run -d --restart unless-stopped --net=host --pid=host -v /:/host:ro,rslave quay.io/prometheus/node-exporter:latest --path.rootfs=/host
```

Alertas mínimos, em qualquer ferramenta:

| O que | Limite sugerido |
|---|---|
| Disco usado | acima de 80% |
| RAM livre | abaixo de 10% por 10 minutos |
| CPU | acima de 90% por 15 minutos |
| Site fora | 2 falhas seguidas |
| Certificado | vence em menos de 14 dias |
| Backup | sem aviso em 26 horas |

Limites são ponto de partida; ajuste ao seu uso. Rotina leve de disco, no `cron` semanal:

```bash
docker system df
df -h /
```

## Combina com / alternativas

- [Backup e restauração](05-backup-e-restauracao-na-vps.md) e [observabilidade](../../infra/docs/10-observabilidade.md).
- [Dimensionar o servidor](02-dimensionar-o-servidor.md) e [atualizações, Docker e swap](04-atualizacoes-docker-e-swap.md), para limpar logs e imagens.
- Alternativas: UptimeRobot ou Better Stack como monitor externo.

## Decisão rápida

- **Use se:** o servidor atende clientes e você quer saber da queda antes deles.
- **Evite se:** a ideia é montar Prometheus e Grafana completos para uma VPS pequena: comece com Uptime Kuma externo mais Netdata.
