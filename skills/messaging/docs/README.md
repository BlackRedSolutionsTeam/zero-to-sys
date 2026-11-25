# Mensageria pesada, vídeo e chamadas

Um documento por tópico, do broker ao vídeo. É para o que as [integrações](../../integrations/SKILL.md) deixam de fora. Preços e versões foram conferidos em 2026-11-25 nas páginas oficiais.

## Brokers e eventos

| Prática | O que entrega | Doc |
|---|---|---|
| Fila simples x broker | Quando sair do Postgres e do Redis | [01-fila-simples-x-broker.md](01-fila-simples-x-broker.md) |
| RabbitMQ | Filas, exchanges, retentativas | [02-rabbitmq.md](02-rabbitmq.md) |
| Kafka | Eventos, partições, quando é exagero | [03-kafka.md](03-kafka.md) |
| Outbox | Entrega confiável entre serviços | [04-outbox-e-entrega-confiavel.md](04-outbox-e-entrega-confiavel.md) |

## Vídeo

| Prática | O que entrega | Doc |
|---|---|---|
| Vídeo e chamadas | LiveKit, Daily, Twilio e custo por minuto | [05-video-e-chamadas.md](05-video-e-chamadas.md) |
| Transmissão e upload | Mux e Cloudflare Stream | [06-transmissao-e-upload-de-video.md](06-transmissao-e-upload-de-video.md) |

## Por onde começar

- **Fila lenta ou dúvida de broker:** 01.
- **Vários serviços com o mesmo evento:** 02, depois 04.
- **Volume alto e histórico de eventos:** 03, depois 04.
- **Chamada de vídeo no app:** 05.
- **Cursos, upload ou transmissão:** 06.
