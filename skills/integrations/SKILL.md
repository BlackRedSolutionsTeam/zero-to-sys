---
name: integrations
description: Integra o sistema com serviços externos e trabalho em segundo plano sem quebrar em produção — pagamentos (Stripe, Mercado Pago, Asaas, AbacatePay, Pix), e-mail transacional, WhatsApp e SMS, webhooks recebidos e enviados, filas e jobs, rotinas agendadas, armazenamento de arquivos, tempo real e notificações, importar e exportar planilhas. Use sempre que o sistema precisar cobrar, mandar e-mail ou mensagem, receber webhook, rodar algo em segundo plano ou todo dia, guardar arquivos, notificar o usuário ou importar planilha, ou quando o usuário pedir "integrar pagamento", "mandar e-mail", "WhatsApp", "webhook", "fila", "job", "rodar todo dia", "upload para S3", "notificação" ou "importar CSV". Não decide hospedagem do worker e segredos do ambiente (skill infra), formato das rotas (skill api) nem segurança de upload (skill security).
---

# integrations

Guia para ligar o sistema ao mundo de fora sem perder cobrança, e-mail ou evento. Integração é onde mais se quebra em produção: webhook perdido, e-mail que cai no spam, job que roda duas vezes, importação que trava o servidor. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e exemplos prontos.

## Como usar esta skill

1. **Levante as integrações** que a skill `product` registrou na entrevista (pagamento, e-mail, WhatsApp, planilha, rotina diária). Cada uma vira um item do backlog.
2. **Escolha o serviço** pela tabela abaixo e pelo documento do tema; confira preço e plano grátis na página oficial antes de afirmar ao usuário.
3. **Isole a integração num módulo** (um cliente por serviço): segredo no ambiente, timeout, retry com backoff, log da chamada e erro tratado.
4. **Todo evento de fora vira fila.** Responda rápido ao webhook e processe depois ([doc 04](docs/04-webhooks.md) e [doc 05](docs/05-filas-e-jobs.md)).
5. **Torne tudo idempotente:** a mesma mensagem duas vezes não pode cobrar duas vezes (skill `api`, doc 06).
6. **Teste com sandbox e mock** do provedor; o fluxo real roda só em staging ([skill `quality`](../quality/SKILL.md)).
7. **Deixe observável:** log, alerta de falha e painel de entregas e jobs.

## Qual serviço usar

| Necessidade | Opções | Documento |
|---|---|---|
| Cobrar no Brasil (Pix, boleto, cartão) | Asaas, Mercado Pago, AbacatePay; Stripe se houver cartão internacional ou assinatura complexa | [01](docs/01-pagamentos.md) |
| E-mail de sistema (verificação, recibo, lembrete) | Resend, Postmark, Amazon SES | [02](docs/02-email-transacional.md) |
| Aviso por WhatsApp ou SMS | API oficial do WhatsApp (Meta) por provedor, SMS por provedor | [03](docs/03-whatsapp-e-sms.md) |
| Receber ou enviar eventos | Webhooks assinados + fila | [04](docs/04-webhooks.md) |
| Tarefa demorada ou que precisa de retry | Fila no banco (pg-boss) ou Redis (BullMQ) ou a da stack | [05](docs/05-filas-e-jobs.md) |
| Rodar todo dia ou toda hora | Cron do provedor ou job agendado na fila | [06](docs/06-rotinas-agendadas.md) |
| Guardar arquivos | Object storage (S3, R2, Supabase Storage) | [07](docs/07-armazenamento-de-arquivos.md) |
| Atualizar a tela ao vivo, avisar o usuário | SSE, WebSocket, serviço pronto; push | [08](docs/08-tempo-real-e-notificacoes.md) |
| Importar ou exportar planilha | Upload → job → relatório de erros | [09](docs/09-importar-e-exportar-planilhas.md) |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Pagamentos | [docs/01-pagamentos.md](docs/01-pagamentos.md) | Stripe, Mercado Pago, Asaas, AbacatePay, Pix |
| E-mail transacional | [docs/02-email-transacional.md](docs/02-email-transacional.md) | Entrega, domínio, bounce |
| WhatsApp e SMS | [docs/03-whatsapp-e-sms.md](docs/03-whatsapp-e-sms.md) | Mensagens ativas, templates, consentimento |
| Webhooks | [docs/04-webhooks.md](docs/04-webhooks.md) | Assinatura, idempotência, reprocessamento |
| Filas e jobs | [docs/05-filas-e-jobs.md](docs/05-filas-e-jobs.md) | Segundo plano com retry |
| Rotinas agendadas | [docs/06-rotinas-agendadas.md](docs/06-rotinas-agendadas.md) | Cron, fuso, não rodar duas vezes |
| Arquivos | [docs/07-armazenamento-de-arquivos.md](docs/07-armazenamento-de-arquivos.md) | Object storage e URL assinada |
| Tempo real e notificações | [docs/08-tempo-real-e-notificacoes.md](docs/08-tempo-real-e-notificacoes.md) | SSE, WebSocket, push |
| Planilhas | [docs/09-importar-e-exportar-planilhas.md](docs/09-importar-e-exportar-planilhas.md) | Importar e exportar sem travar |

## Checklist de toda integração

- [ ] Cliente isolado num módulo próprio, sem chamada ao provedor espalhada pelo código (`grep -rn "api.stripe.com\|fetch(" src`).
- [ ] Segredo e chaves em variáveis de ambiente, nunca no repositório; chave de teste e de produção separadas.
- [ ] Timeout configurado e retry com backoff apenas em erro seguro.
- [ ] Operação que cobra, envia ou cria é idempotente (chave de idempotência ou id do evento).
- [ ] Webhook verifica a assinatura, responde 2xx rápido e processa em fila.
- [ ] Falha vira log com contexto e alerta, não erro silencioso.
- [ ] Nada de chamada externa dentro de transação de banco (outbox na skill `data`).
- [ ] Teste com sandbox ou mock do provedor, e um teste do caminho de falha.
- [ ] Rotina agendada não roda em duas instâncias ao mesmo tempo e avisa se não rodou.
- [ ] Mensagem ativa (e-mail, WhatsApp, SMS) respeita o consentimento e tem descadastro quando aplicável.

## Regras de uso

- **O provedor é a fonte da verdade.** Pagamento confirmado é o webhook dele, não a volta do usuário ao site.
- **Nunca toque em dado de cartão.** Use checkout hospedado ou os elementos do provedor.
- **Responda rápido, processe depois.** Webhook e requisição externa só enfileiram.
- **Mesma mensagem duas vezes não pode ter efeito duas vezes.** Provedores repetem eventos; o seu código precisa aguentar.
- **Falha é esperada.** Todo job tem retry, limite de tentativas e destino para o que não deu certo.
- **Um serviço por necessidade.** Não adicione fila, Redis ou provedor novo antes de a necessidade existir.
- **Conta e custo são do usuário.** Peça confirmação antes de criar conta paga ou conectar um serviço que gera cobrança.
- **Fronteiras.** Hospedagem do worker e segredos do ambiente são da `infra`; formato das rotas e idempotência da API são da `api`; segurança do arquivo enviado é da `security`; tabelas de eventos e outbox são da `data`.

## Quando a lista não cobre

ERP e emissão de nota fiscal, OCR, mensageria pesada (Kafka, RabbitMQ), busca (Elasticsearch, Meilisearch), vídeo e chamadas (WebRTC), IA e LLMs e integrações específicas de um setor ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial do serviço.

## Validade dos dados

Preços, planos e limites mudam com frequência: foram conferidos em 2026-11-24 quando citados, e cada documento tem a linha "Verificado em". Confira na página oficial antes de afirmar um valor ao usuário.
