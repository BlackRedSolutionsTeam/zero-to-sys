# Webhooks

> Receba webhooks verificando a assinatura sobre o corpo bruto, responda 2xx rápido, grave o evento e processe em fila com idempotência pelo id; ao enviar, assine, tente de novo com backoff e desative endpoint que só falha.

| | |
|---|---|
| **Referência** | Documentação de webhooks da Stripe (docs.stripe.com/webhooks), incluindo assinatura, tolerância de timestamp, eventos duplicados e fora de ordem; Stripe CLI (`stripe listen`); documentação do ngrok e do Cloudflare Quick Tunnels; RFC 2104 (HMAC) |
| **Categoria** | Integrações |
| **Tipo** | Prática de integração por eventos |
| **Vale para** | Node, Python, .NET, Java, Laravel e Go; exemplos em TypeScript e C# |
| **Verificado em** | 2026-11-24 |

## O que é

**Webhook** é uma chamada HTTP que um sistema faz no seu quando algo acontece lá (pagamento aprovado, mensagem entregue). Em vez de você perguntar toda hora, ele avisa.

Duas pontas:

- **Receber:** seu endpoint público recebe eventos de Stripe, Meta, Asaas etc.
- **Enviar:** seu sistema avisa os clientes (por exemplo, "agendamento criado" para o sistema do convênio da clínica).

## Por que usar

- **Tempo real sem polling:** o aviso chega quando o fato ocorre.
- **Menos chamadas:** você não consulta a API do provedor a cada minuto.
- **Padrão do mercado:** pagamentos e mensagens dependem dele.

## Quando usar

- Confirmação de pagamento ([01](01-pagamentos.md)) e status de mensagem ([03](03-whatsapp-e-sms.md)).
- Avisar sistemas de terceiros sobre mudanças no seu domínio.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Normalmente não há evento externo a tratar |
| MVP de SaaS | ✅ Ótimo | Pagamento e e-mail dependem de webhook |
| SaaS em crescimento | ✅ Ótimo | Precisa de fila, reprocesso e painel de entregas |
| Sistema interno/corporativo | 🟡 Serve | Útil na integração com outros sistemas |
| API/integração | ✅ Ótimo | Oferecer webhooks é parte do produto |
| App mobile | 🟡 Serve | O webhook chega no backend, não no app |
| Endpoint sem verificação de assinatura | ❌ Evite | Qualquer um forja um "pagamento aprovado" |

## Quando é bom

- **Verificar a assinatura sempre:** sem isso, qualquer pessoa chama seu endpoint.
- **Responder 2xx logo:** a Stripe pede retornar sucesso antes de lógica que cause timeout.
- **Registrar antes de processar:** o evento fica salvo e pode ser reprocessado.
- **Idempotência:** o provedor pode mandar o mesmo evento mais de uma vez; guarde os ids já processados (ver [idempotência](../../api/docs/06-idempotencia-e-retries.md)).
- **Não depender da ordem:** a Stripe avisa que eventos podem chegar fora de ordem e que `created` não serve para ordenar.

## Quando é ruim

- **Processar dentro da requisição:** lento, estoura timeout, o provedor reenvia.
- **Reformatar o corpo antes de verificar:** a Stripe exige o corpo bruto; qualquer alteração quebra a assinatura.
- **Confiar no payload sem consultar:** para decisões críticas, busque o objeto na API do provedor se o evento chegou fora de ordem.
- **Endpoint sem proteção de CSRF isenta:** frameworks como Rails e Django bloqueiam o POST; isente só essa rota.
- **Segredo no código:** fica no ambiente, e a Stripe recomenda trocá-lo periodicamente.

## Como começar

### Receber

1. Endpoint público HTTPS, ex.: `POST /webhooks/stripe`.
2. Ler o **corpo bruto** (bytes) antes de qualquer parser JSON.
3. Verificar a assinatura.
4. Gravar em `webhook_events` e responder `200`.
5. Um job na fila ([05](05-filas-e-jobs.md)) processa e muda o status.

Assinatura (formato da Stripe): o cabeçalho `Stripe-Signature` traz `t=<timestamp>` e uma ou mais `v1=<assinatura>`. A mensagem assinada é `timestamp + "." + corpo`; a assinatura é HMAC-SHA256 com o segredo do endpoint. Compare em tempo constante e rejeite timestamp fora da tolerância (as bibliotecas da Stripe usam cinco minutos; nunca use 0). Prefira a biblioteca oficial; o código abaixo é a versão manual, serve para qualquer provedor com esquema parecido.

```typescript
import { createHmac, timingSafeEqual } from "node:crypto";

export function verifySignature(rawBody: string, header: string, secret: string, toleranceSeconds = 300) {
  const parts = header.split(",").map((item) => item.split("="));
  const timestamp = parts.find(([key]) => key === "t")?.[1];
  const signatures = parts.filter(([key]) => key === "v1").map(([, value]) => value);
  if (!timestamp || signatures.length === 0) return false;

  const age = Math.abs(Date.now() / 1000 - Number(timestamp));
  if (age > toleranceSeconds) return false;

  const expected = createHmac("sha256", secret).update(`${timestamp}.${rawBody}`).digest();
  return signatures.some((signature) => {
    const received = Buffer.from(signature, "hex");
    return received.length === expected.length && timingSafeEqual(received, expected);
  });
}
```

```csharp
using System.Security.Cryptography;
using System.Text;

public static bool VerifySignature(string rawBody, string header, string secret, int toleranceSeconds = 300)
{
    var parts = header.Split(',').Select(item => item.Split('=', 2)).ToList();
    var timestamp = parts.FirstOrDefault(p => p[0] == "t")?[1];
    var signatures = parts.Where(p => p[0] == "v1").Select(p => p[1]).ToList();
    if (timestamp is null || signatures.Count == 0) return false;

    var age = Math.Abs(DateTimeOffset.UtcNow.ToUnixTimeSeconds() - long.Parse(timestamp));
    if (age > toleranceSeconds) return false;

    var key = Encoding.UTF8.GetBytes(secret);
    var message = Encoding.UTF8.GetBytes($"{timestamp}.{rawBody}");
    var expected = HMACSHA256.HashData(key, message);

    return signatures.Any(signature =>
        CryptographicOperations.FixedTimeEquals(Convert.FromHexString(signature), expected));
}
```

Tabela de eventos recebidos:

```sql
create table webhook_events (
  id uuid primary key default gen_random_uuid(),
  provider text not null,
  event_id text not null,
  payload jsonb not null,
  status text not null default 'received',
  attempts int not null default 0,
  last_error text,
  received_at timestamptz not null default now(),
  processed_at timestamptz,
  unique (provider, event_id)
);
```

O `unique (provider, event_id)` faz a idempotência: `insert ... on conflict do nothing`; se não inseriu, é duplicado, responda `200` e pare. Status: `received`, `processed`, `failed`. Para **reprocessar**, o painel interno volta `failed` para `received` e reenfileira. O job lê o objeto atual na API do provedor quando a ordem importa.

Convenção prática: não valide `Date.now()` do próprio servidor sem NTP; relógio errado rejeita eventos válidos (a Stripe recomenda NTP).

### Enviar

- **Assine** cada entrega com HMAC e um segredo por cliente; envie `timestamp` e id do evento.
- **Retry com backoff:** tente de novo em intervalos crescentes. Referência: a Stripe tenta por até três dias com atraso exponencial em produção.
- **Painel de entregas:** liste cada tentativa com status HTTP e horário, e um botão de reenviar (a Stripe tem uma aba de entregas assim).
- **Desativar endpoint que falha sempre:** depois de N dias de falha, pause, avise o dono da conta e permita reativar.
- **Timeout curto** e corpo pequeno; o cliente deve consultar a API para detalhes.

### Testar localmente

| Ferramenta | Comando |
|---|---|
| Stripe CLI | `stripe listen --forward-to localhost:4242/webhook` (imprime o segredo de assinatura local) |
| ngrok | `ngrok http 4242` (precisa instalar e configurar o authtoken) |
| Cloudflare | `cloudflared tunnel --url http://localhost:4242` (Quick Tunnel só para teste; a URL muda a cada execução e fica aberta a quem tiver o link) |

## Combina com / alternativas

- [Pagamentos](01-pagamentos.md) e [WhatsApp e SMS](03-whatsapp-e-sms.md): principais fontes de eventos.
- [Filas e jobs](05-filas-e-jobs.md): processamento depois do 2xx.
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md): mesmo evento, um efeito.
- [Transações e concorrência](../../data/docs/09-transacoes-e-concorrencia.md): outbox para enviar webhooks sem perder evento.
- Alternativa: polling na API do provedor, quando ele não oferece webhook; mais lento e mais caro.

## Decisão rápida

- **Use se:** o provedor avisa por evento: verifique a assinatura, grave, responda 2xx e processe na fila.
- **Evite se:** o endpoint não consegue validar a origem; use polling ou outro canal autenticado.
