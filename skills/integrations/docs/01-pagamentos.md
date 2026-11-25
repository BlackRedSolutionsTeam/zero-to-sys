# Pagamentos

> Cobre pelo checkout do provedor, crie a cobrança no servidor e trate o webhook assinado como a única prova de que o pagamento aconteceu.

| | |
|---|---|
| **Referência** | Documentação oficial da Stripe (Checkout, Webhooks, Idempotent requests, Pix), do Asaas (Webhooks, API de cobranças), da AbacatePay (API v2, Webhooks) e do Mercado Pago (Checkout Pro, Webhooks); PCI Security Standards Council (escopo de conformidade de cartão) |
| **Categoria** | Integrações |
| **Tipo** | Prática de integração com serviço externo |
| **Vale para** | Node, Python, .NET, Java, Laravel, Go; Stripe, Mercado Pago, Asaas, AbacatePay |
| **Verificado em** | 2026-11-24 |

## O que é

Seu sistema não fala com o banco: pede ao provedor de pagamento para criar uma cobrança e espera ele avisar o resultado. Esse aviso chega por **webhook**: uma chamada HTTP que o provedor faz na sua API quando algo acontece (pagamento confirmado, falhou, estornado). Detalhes em [04-webhooks.md](04-webhooks.md).
**PCI** é o conjunto de regras de segurança para quem toca em número de cartão. Se ele passa pelo seu servidor, seu escopo de conformidade cresce muito; por isso o cartão só é digitado no campo do provedor.

## Por que usar

- **Menos risco e menos código:** o provedor guarda o cartão e já entrega boleto, Pix, parcelamento e histórico de cobranças.

## Quando usar
- Qualquer sistema que cobra dinheiro, ou ao trocar cobrança manual (planilha, Pix na mão) por algo rastreável.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Só se vender curso, doação ou assinatura; link de pagamento do provedor basta |
| MVP de SaaS | ✅ Ótimo | Checkout hospedado e webhook entregam a cobrança em poucos dias |
| SaaS em crescimento | ✅ Ótimo | Assinatura, split, conciliação e estorno viram requisito |
| Sistema interno/corporativo | 🟡 Serve | Quando há cobrança de clientes; boleto e Pix costumam bastar |
| API/integração | ✅ Ótimo | O webhook e a idempotência são o coração do trabalho |
| App mobile | 🟡 Serve | Compra de bens digitais dentro do app tem regras das lojas; consulte-as antes |
| Qualquer um, recebendo número de cartão no seu servidor | ❌ Evite | Escopo PCI inteiro nas suas costas |

## Quando é bom

- **Checkout hospedado ou elementos do provedor:** o cartão é digitado no domínio ou no iframe deles. **Cobrança criada no servidor:** o valor vem do banco.
- **Webhook como fonte da verdade, com assinatura verificada:** a volta ao site (`success_url`) só mostra uma tela; o cliente pode fechar a aba ou digitar a URL na mão.
- **Idempotência:** repetir a chamada não cobra duas vezes ([idempotência e retries](../../api/docs/06-idempotencia-e-retries.md)). **Sandbox:** troque a chave só no deploy.

## Quando é ruim

- **Liberar o serviço pela página de sucesso** ou **confiar no valor vindo do front:** ambos se burlam no navegador.
- **Ignorar duplicata e ordem:** a entrega é "pelo menos uma vez", e a Stripe avisa que não garante a ordem dos eventos.

## Como começar

### Qual provedor

Taxas mudam e dependem do seu volume e da forma de pagamento. Em todos os casos: consulte o preço atual na página oficial antes de decidir.

| Provedor | Quando escolher | O que a documentação oficial confirma |
|---|---|---|
| Stripe | Venda internacional, SaaS com assinatura, quer a melhor API | Checkout com mais de 125 formas de pagamento locais, Billing para assinaturas, Connect para marketplace; Pix aceito em conta Stripe do Brasil (e de outros países listados), exceto alguns ramos (a doc proíbe, por exemplo, serviços médicos, MCC 8099; confira o seu); Pix Automático para recorrência |
| Mercado Pago | Público brasileiro que já usa a carteira Mercado Pago | Checkout Pro com cartão, Pix, boleto e conta Mercado Pago; assinaturas com tópicos próprios de webhook |
| Asaas | Cobrança brasileira com boleto, Pix e cartão; clínica, escola, serviço recorrente | API com Pix, boleto, cartão de crédito e débito e TED; assinaturas; split (habilitado em Integrações > Segurança); sandbox próprio |
| AbacatePay | Pix simples, MVP, quer começar rápido | Pix, cartão e boleto no checkout; cobrança Pix transparente por API; assinaturas; split em até 10 partes; Modo Teste sem verificar a conta |

**Assinatura x avulsa.** Avulsa cobra uma vez (consulta paga ao agendar). Assinatura cobra todo ciclo (plano mensal da clínica) e exige tratar renovação, falha de cartão, cancelamento e troca de plano, tudo via webhook. Comece avulso se der.

### Estados do pagamento

Modele o pagamento como máquina de estados (veja [regras de negócio](../../product/docs/05-regras-de-negocio.md)). Só estas transições são válidas:

```
pendente -> pago | falhou | expirado
pago -> estornado
```

Na clínica, o agendamento só vira `confirmado` quando o pagamento vira `pago`. Se expirar, o horário volta a ficar livre.

### Exemplo: Stripe Checkout e webhook (Node, TypeScript)

Criar a cobrança no servidor. O valor vem do banco, a chave de idempotência é a do agendamento.

```ts
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function criarCheckout(agendamento: { id: string; valorEmCentavos: number; descricao: string }) {
  const sessao = await stripe.checkout.sessions.create(
    {
      mode: "payment",
      line_items: [{
        quantity: 1,
        price_data: { currency: "brl", unit_amount: agendamento.valorEmCentavos, product_data: { name: agendamento.descricao } },
      }],
      client_reference_id: agendamento.id,
      success_url: `${process.env.APP_URL}/agendamentos/${agendamento.id}`,
      cancel_url: `${process.env.APP_URL}/agendamentos/${agendamento.id}`,
    },
    { idempotencyKey: `checkout-${agendamento.id}` },
  );
  return sessao.url;
}
```

Webhook: ler o corpo cru (a assinatura vale para os bytes exatos), verificar `Stripe-Signature` e responder 2xx rápido.

```ts
import express from "express";

const app = express();

app.post("/webhooks/stripe", express.raw({ type: "application/json" }), async (req, res) => {
  let evento: Stripe.Event;
  try {
    evento = stripe.webhooks.constructEvent(req.body, req.headers["stripe-signature"] as string, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return res.sendStatus(400);
  }

  const jaProcessado = await db.eventoPagamento.registrarSeNovo(evento.id);
  if (!jaProcessado) return res.sendStatus(200);

  const sessao = evento.data.object as Stripe.Checkout.Session;
  const pago = ["checkout.session.completed", "checkout.session.async_payment_succeeded"].includes(evento.type);
  const falhou = ["checkout.session.async_payment_failed", "checkout.session.expired"].includes(evento.type);

  if (pago && sessao.payment_status === "paid") {
    await filaDePagamentos.enfileirar({ agendamentoId: sessao.client_reference_id!, estado: "pago" });
  } else if (falhou) {
    await filaDePagamentos.enfileirar({ agendamentoId: sessao.client_reference_id!, estado: "falhou" });
  }

  res.sendStatus(200);
});
```

`registrarSeNovo` grava o `evento.id` numa tabela com chave única e devolve `false` se já existir. O trabalho pesado (marcar `pago`, confirmar o agendamento, mandar e-mail) vai para a fila ([05-filas-e-jobs.md](05-filas-e-jobs.md)), na mesma transação do registro quando possível ([transações e outbox](../../data/docs/09-transacoes-e-concorrencia.md)). Teste local: `stripe listen --forward-to localhost:3000/webhooks/stripe`.

### Equivalente com Pix: Asaas

Cobrança: `POST /v3/payments`, header `access_token`, sandbox `https://api-sandbox.asaas.com`. Obrigatórios: `customer` (id já criado no Asaas), `billingType` (`PIX`), `value` e `dueDate` (`AAAA-MM-DD`). Webhook: o Asaas envia o token que você cadastrou no header `asaas-access-token`; compare antes de processar. A entrega é "pelo menos uma vez": grave o `id` do evento e ignore repetidos. Após 15 falhas seguidas a fila pausa (eventos ficam 14 dias). Confira os eventos (como `PAYMENT_RECEIVED`) em "Eventos de Webhooks".

### Equivalente com Pix: AbacatePay

Cobrança: `POST https://api.abacatepay.com/v2/transparents/create` com `Authorization: Bearer <chave>`. Corpo: `method: "PIX"` e `data` com `amount` em centavos (mínimo 100) e `expiresIn` em segundos (mínimo 300); `externalId` guarda o id do seu agendamento. A resposta traz `brCode` (copia e cola) e `brCodeBase64` (QR Code). Modo teste ou produção depende da chave, não da URL. Webhook: evento `transparent.completed` para pagamento confirmado; use o `id` do evento para descartar duplicatas (ele se repete nas retentativas, mas muda no reenvio manual do painel). Para `X-Webhook-Signature`, a doc de segurança deles descreve HMAC-SHA256 sobre o corpo cru, em base64, com uma chave pública fixa da AbacatePay (a mesma para todas as contas); confira o valor da chave e o exemplo em "Segurança dos webhooks". Ela não substitui o `webhookSecret` que você cadastra na URL do webhook: verifique os dois.

### Conciliação e estorno

- **Conciliação:** rotina diária que lista os pagamentos do provedor e compara com a sua tabela; divergência vira alerta e cobre webhook perdido.
- **Estorno:** peça pela API; o estado muda para `estornado` só quando o webhook confirmar. Na Stripe, o Pix aceita estorno total ou parcial em até 90 dias.

### Em cada stack

| Stack | Cliente | Corpo cru do webhook |
|---|---|---|
| Node | SDK `stripe` | `express.raw` ou equivalente do framework |
| Python | SDK `stripe` | `request.body` (bytes), antes de parsear |
| .NET | SDK `Stripe.net` | ler o corpo como string antes do binding |
| Java | SDK `stripe-java` | `@RequestBody String` |
| Laravel | SDK `stripe-php` | `$request->getContent()` |
| Go | SDK `stripe-go` | `io.ReadAll(r.Body)` |

Teste com sandbox, mock do cliente e payloads reais de webhook como fixture ([testes de API](../../quality/docs/04-testes-de-api-e-contrato.md)).

## Combina com / alternativas

- [04-webhooks.md](04-webhooks.md), [05-filas-e-jobs.md](05-filas-e-jobs.md), [06-rotinas-agendadas.md](06-rotinas-agendadas.md) e [02-email-transacional.md](02-email-transacional.md) (recibo): receber, processar, conciliar e avisar.
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md) e [regras de negócio](../../product/docs/05-regras-de-negocio.md).

## Decisão rápida

- **Use se:** o sistema cobra dinheiro; escolha Stripe para internacional ou assinatura sofisticada, Asaas ou AbacatePay para Pix e boleto no Brasil, Mercado Pago se o público já usa a carteira.
- **Evite se:** a ideia é receber número de cartão no seu servidor, ou liberar o serviço pela página de sucesso em vez do webhook.
