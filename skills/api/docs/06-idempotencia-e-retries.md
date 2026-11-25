# Idempotência e retries

> Se o cliente repetir a mesma requisição (clique duplo, rede ruim, retry), o efeito acontece uma vez só: use chave de idempotência no POST e retry com backoff e jitter.

| | |
|---|---|
| **Referência** | RFC 9110, seções de métodos idempotentes e Retry-After (rfc-editor.org/rfc/rfc9110); RFC 6585 (429 Too Many Requests); rascunho IETF "The Idempotency-Key HTTP Header Field" (datatracker.ietf.org, draft-ietf-httpapi-idempotency-key-header, ainda rascunho, não é RFC); documentação da Stripe sobre requisições idempotentes (docs.stripe.com/api/idempotent_requests) |
| **Categoria** | API |
| **Tipo** | Prática de robustez de API |
| **Vale para** | APIs HTTP/REST em qualquer linguagem; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

Uma operação é **idempotente** quando repeti-la tem o mesmo efeito que fazê-la uma vez. Pelo RFC 9110, `GET`, `HEAD`, `OPTIONS`, `TRACE`, `PUT` e `DELETE` são idempotentes. `POST` e `PATCH` não são por definição.

Problema típico: o paciente clica duas vezes em "Agendar", ou a rede cai depois de o servidor gravar e antes de a resposta chegar. O cliente repete o `POST /appointments` e a clínica fica com dois agendamentos (ou duas cobranças).

A solução é o cliente mandar uma **chave de idempotência** (um id único por tentativa de ação). O servidor guarda o resultado dessa chave e, se ela voltar, devolve o mesmo resultado sem repetir o efeito.

## Por que usar

- **Sem duplicidade:** clique duplo e retry não criam dois agendamentos nem duas cobranças.
- **Retry seguro:** o cliente pode repetir sem medo.

## Quando usar

- Todo `POST` que cria algo com efeito caro de repetir: pagamento, agendamento, envio de e-mail, pedido.
- Webhooks recebidos: o remetente reenvia o mesmo evento.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Quase sem escrita |
| MVP de SaaS | ✅ Ótimo | Cobrança e criação com clique duplo aparecem cedo |
| SaaS em crescimento | ✅ Ótimo | Filas, retries e webhooks aumentam as repetições |
| Sistema interno/corporativo | 🟡 Serve | Só nas operações caras de repetir |
| API pública/integração | ✅ Ótimo | Parceiros fazem retry; a chave é esperada |
| App mobile | ✅ Ótimo | Rede instável gera repetição o tempo todo |

## Quando é bom

- **Cliente simples:** gera a chave uma vez e repete à vontade.
- **Padrão conhecido:** a Stripe usa o cabeçalho `Idempotency-Key`, e o rascunho do IETF o descreve.

## Quando é ruim

- **Chave reaproveitada por engano:** usar a mesma chave em ações diferentes devolve a resposta errada. Gere uma chave nova por ação do usuário.
- **Tabela que cresce sem limite:** apague chaves vencidas.
- **Efeitos fora do banco:** se o handler envia e-mail antes de gravar a chave, a repetição envia de novo. Grave a chave na mesma transação.

## Como começar

**Cliente.** Gere um UUID quando o usuário abre o formulário (não a cada clique) e envie no cabeçalho:

```
POST /appointments
Idempotency-Key: 8e03978e-40d5-43e8-bc93-6894a57f9324
Content-Type: application/json

{ "patientId": "pat_1", "startsAt": "2026-12-01T14:00:00Z" }
```

**Tabela no banco**

| Coluna | Para que serve |
|---|---|
| `key` | A chave enviada (única por empresa/usuário) |
| `request_hash` | Hash do corpo, para detectar chave com corpo diferente |
| `status` | `processing` ou `done` |
| `response_status` e `response_body` | A resposta guardada |
| `expires_at` | Quando apagar (por exemplo, 24 horas) |

**Comportamento do servidor**

| Situação | Resposta |
|---|---|
| Chave nova | Executa, guarda a resposta, devolve |
| Mesma chave, mesmo corpo, já concluída | Devolve a resposta guardada, sem executar |
| Mesma chave, corpo diferente | 422 (é o que o rascunho recomenda) |
| Mesma chave ainda em processamento | 409 |
| Chave ausente em rota que exige | 400 |

**Middleware (Hono, com Postgres via `pg`)**

```ts
import { createHash } from "node:crypto";
import type { MiddlewareHandler } from "hono";
import { pool } from "./db";

export const idempotency: MiddlewareHandler = async (c, next) => {
  const key = c.req.header("Idempotency-Key");
  if (!key) return c.json({ title: "Idempotency-Key obrigatório", status: 400 }, 400);

  const body = await c.req.text();
  const hash = createHash("sha256").update(body).digest("hex");
  const scope = c.get("companyId") as string;

  const inserted = await pool.query(
    `insert into idempotency_keys (company_id, key, request_hash, status, expires_at)
     values ($1, $2, $3, 'processing', now() + interval '24 hours')
     on conflict (company_id, key) do nothing returning key`,
    [scope, key, hash],
  );

  if (inserted.rowCount === 0) {
    const { rows } = await pool.query(
      `select request_hash, status, response_status, response_body
       from idempotency_keys where company_id = $1 and key = $2`,
      [scope, key],
    );
    const saved = rows[0];
    if (saved.request_hash !== hash)
      return c.json({ title: "Chave usada com outro corpo", status: 422 }, 422);
    if (saved.status === "processing")
      return c.json({ title: "Requisição em andamento", status: 409 }, 409);
    return c.json(saved.response_body, saved.response_status);
  }

  await next();

  const responseBody = await c.res.clone().json();
  await pool.query(
    `update idempotency_keys
     set status = 'done', response_status = $3, response_body = $4
     where company_id = $1 and key = $2`,
    [scope, key, c.res.status, responseBody],
  );
};
```

O `insert ... on conflict do nothing` é atômico: dois cliques ao mesmo tempo, só um passa. Se o handler falhar com erro de servidor, apague a chave para o cliente poder tentar de novo. Um job apaga as linhas com `expires_at` vencido.

**Retry no cliente**

Repita só quando é seguro: erro de rede, timeout, `429`, `502`, `503`, `504`. Nunca repita `400`, `401`, `403`, `404`, `409` ou `422`: o resultado seria o mesmo. Use espera exponencial com **jitter** (sorteio na espera, para mil clientes não voltarem no mesmo segundo) e respeite o `Retry-After` (RFC 9110) quando vier.

```ts
const retryable = new Set([429, 502, 503, 504]);

export async function fetchWithRetry(url: string, init: RequestInit, max = 4) {
  for (let attempt = 0; ; attempt++) {
    try {
      const res = await fetch(url, { ...init, signal: AbortSignal.timeout(10_000) });
      if (!retryable.has(res.status) || attempt === max) return res;
      const retryAfter = Number(res.headers.get("Retry-After"));
      await sleep(retryAfter ? retryAfter * 1000 : backoff(attempt));
    } catch (error) {
      if (attempt === max) throw error;
      await sleep(backoff(attempt));
    }
  }
}

const backoff = (attempt: number) => Math.random() * Math.min(10_000, 500 * 2 ** attempt);
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
```

Retry em `POST` só com `Idempotency-Key`. Sempre ponha **timeout** no cliente (10 s acima) e no servidor, para nada ficar pendurado.

**Limite de taxa.** `429 Too Many Requests` (RFC 6585) diz "devagar"; mande `Retry-After`. Como proteger contra abuso fica na skill `security`.

**Webhooks recebidos.** O remetente reenvia eventos. Guarde o `id` do evento numa tabela com chave única e ignore repetidos: `insert ... on conflict do nothing` e só processe se inseriu. Responda `200` logo, para ele parar de reenviar.

## Combina com / alternativas

- [02-rotas-verbos-e-status.md](02-rotas-verbos-e-status.md): `PUT` e `DELETE` já nascem idempotentes.
- Transações e concorrência: [../../data/docs/09-transacoes-e-concorrencia.md](../../data/docs/09-transacoes-e-concorrencia.md).
- Alternativa: restrição única de negócio (por exemplo, um agendamento por paciente e horário). Cobre a duplicidade, mas não devolve a resposta original.

## Decisão rápida

- **Use se:** o `POST` cria algo caro de repetir (pagamento, agendamento) ou o cliente faz retry.
- **Evite se:** a rota só lê ou já é idempotente por natureza; não crie tabela de chaves à toa.
