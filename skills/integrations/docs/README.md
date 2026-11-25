# Integrações

Um documento por tema, explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com exemplos prontos. Preços e limites foram conferidos em 2026-11-24 quando citados; confira na página oficial antes de afirmar um valor.

## Falar com o mundo de fora

| Prática | O que entrega | Doc |
|---|---|---|
| Pagamentos | Stripe, Mercado Pago, Asaas, AbacatePay, Pix | [01-pagamentos.md](01-pagamentos.md) |
| E-mail transacional | Entrega, domínio, bounce | [02-email-transacional.md](02-email-transacional.md) |
| WhatsApp e SMS | Mensagens ativas, templates, consentimento | [03-whatsapp-e-sms.md](03-whatsapp-e-sms.md) |
| Webhooks | Assinatura, idempotência, reprocessamento | [04-webhooks.md](04-webhooks.md) |

## Trabalho em segundo plano

| Prática | O que entrega | Doc |
|---|---|---|
| Filas e jobs | Segundo plano com retry | [05-filas-e-jobs.md](05-filas-e-jobs.md) |
| Rotinas agendadas | Cron, fuso, não rodar duas vezes | [06-rotinas-agendadas.md](06-rotinas-agendadas.md) |

## Arquivos e dados

| Prática | O que entrega | Doc |
|---|---|---|
| Arquivos | Object storage e URL assinada | [07-armazenamento-de-arquivos.md](07-armazenamento-de-arquivos.md) |
| Planilhas | Importar e exportar sem travar | [09-importar-e-exportar-planilhas.md](09-importar-e-exportar-planilhas.md) |

## Experiência ao vivo

| Prática | O que entrega | Doc |
|---|---|---|
| Tempo real e notificações | SSE, WebSocket, push | [08-tempo-real-e-notificacoes.md](08-tempo-real-e-notificacoes.md) |

## Por onde começar

- **Vão cobrar:** 01, depois 04 (webhook) e 05 (fila).
- **Vão mandar aviso ao usuário:** 02, 03 e 08; consentimento no doc de LGPD da skill `security`.
- **Algo precisa rodar sozinho:** 06 e 05.
- **Vão guardar documentos e fotos:** 07 e o doc de upload da skill `security`.
- **O cliente tem planilhas:** 09.
