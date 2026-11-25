---
name: messaging
description: 'Decide e monta mensageria pesada, vídeo e chamadas quando a fila do Postgres ou do Redis não basta: RabbitMQ, Kafka, NATS, outbox, idempotência e WebRTC. Use quando pedirem "RabbitMQ", "Kafka", "eventos entre serviços" ou "videochamada no sistema".'
---

# messaging

Guia de nicho para quando a fila simples não basta: brokers, eventos entre serviços, vídeo e chamadas. Para a maioria dos projetos a resposta é "não precisa": a fila do Postgres ou do Redis e o SSE resolvem. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e exemplos prontos.

## Como usar esta skill

1. **Comece negando.** Pergunte o volume, quantos serviços consomem o evento e se há necessidade de reler eventos antigos. Sem isso, fique em [filas e jobs](../integrations/docs/05-filas-e-jobs.md) ([doc 01](docs/01-fila-simples-x-broker.md)).
2. **Escolha o broker pelo problema:** roteamento e tarefas, RabbitMQ ([doc 02](docs/02-rabbitmq.md)); histórico e volume alto, Kafka ([doc 03](docs/03-kafka.md)).
3. **Garanta a entrega** com outbox no produtor e inbox no consumidor ([doc 04](docs/04-outbox-e-entrega-confiavel.md)).
4. **Chamada de vídeo no app:** [doc 05](docs/05-video-e-chamadas.md); calcule o custo por minuto de participante antes.
5. **Vídeo para assistir (curso, upload, ao vivo):** [doc 06](docs/06-transmissao-e-upload-de-video.md).
6. **Opere o broker** pela skill `infra` e, em VPS, pela skill `vps`.

## Qual opção por situação

| Situação | Opção | Por quê |
|---|---|---|
| Tarefas em segundo plano num monólito | Fila no Postgres (pg-boss, River) ou BullMQ | Sem serviço novo |
| Vários serviços, roteamento, prioridades | RabbitMQ | Exchanges, filas, DLX |
| Alto volume e releitura de histórico | Kafka | Log por partição |
| Mensagens leves e rápidas entre serviços | NATS | Binário único; JetStream para persistência |
| Banco e broker sem perder evento | Outbox | Mesma transação |
| Teleconsulta, aula ao vivo | LiveKit, Daily ou Twilio | WebRTC pronto |
| Curso gravado, upload de vídeo | Mux ou Cloudflare Stream | Transcodificação e CDN |
| Chamada rara | Link do Google Meet ou Zoom | Custo zero |

Preços e versões de cada ferramenta estão nos docs, conferidos em 2026-11-25.

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Fila simples x broker | [docs/01-fila-simples-x-broker.md](docs/01-fila-simples-x-broker.md) | Quando sair do Postgres e do Redis |
| RabbitMQ | [docs/02-rabbitmq.md](docs/02-rabbitmq.md) | Filas, exchanges, retentativas |
| Kafka | [docs/03-kafka.md](docs/03-kafka.md) | Eventos, partições, quando é exagero |
| Outbox | [docs/04-outbox-e-entrega-confiavel.md](docs/04-outbox-e-entrega-confiavel.md) | Entrega confiável entre serviços |
| Vídeo e chamadas | [docs/05-video-e-chamadas.md](docs/05-video-e-chamadas.md) | LiveKit, Daily, Twilio e custo por minuto |
| Transmissão e upload | [docs/06-transmissao-e-upload-de-video.md](docs/06-transmissao-e-upload-de-video.md) | Mux e Cloudflare Stream |

## Checklist

- [ ] Medida a fila atual (tamanho e idade do job mais antigo) antes de propor um broker.
- [ ] Alguém definido para operar o broker, ou serviço gerenciado escolhido.
- [ ] Consumidores idempotentes (entrega pelo menos uma vez).
- [ ] Fila de mortos e limite de tentativas configurados.
- [ ] Evento publicado por outbox quando o dado e o evento precisam andar juntos.
- [ ] Alerta de tamanho da fila, lag e idade da mensagem mais antiga.
- [ ] Custo por minuto de chamada ou de vídeo calculado e alerta de gasto ligado.
- [ ] Token de sala gerado no backend; chave secreta fora do navegador.
- [ ] Vídeo pago com URL assinada e limite de tamanho e duração no upload.
- [ ] Consentimento avisado quando a chamada é gravada.

## Regras de uso

- **Preço e versão só conferidos.** Confirme na página oficial e diga a data.
- **Broker é último recurso.** Sem medição, fique na fila do banco.
- **Kafka não é fila de tarefas.** Diga isso quando o pedido for só enviar e-mails.
- **Entrega é pelo menos uma vez.** Peça idempotência no consumidor.
- **Chamada e vídeo cobram por minuto.** Mostre a conta antes de escolher.
- **Fronteiras.** Fila simples, jobs, SSE, WebSocket e push são da `integrations`; monólito x serviços da `architecture`; operar servidor, backup e monitoramento da `infra` e da `vps`.

## Quando a lista não cobre

ActiveMQ, Pulsar, Redpanda, SQS e SNS, Google Pub/Sub, Azure Service Bus, MQTT para IoT, event sourcing completo, CQRS, malha de serviços, SIP e telefonia, e servidor de mídia próprio com FFmpeg ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial.

## Validade dos dados

Preços, planos e versões (RabbitMQ 4.4.1, Kafka 4.4.0, NATS 2.15.3, Debezium 3.7.1.Final, LiveKit, Daily, Twilio, Mux e Cloudflare Stream) foram conferidos em 2026-11-25 nas fontes oficiais e mudam com frequência; cada documento tem a linha "Verificado em".
