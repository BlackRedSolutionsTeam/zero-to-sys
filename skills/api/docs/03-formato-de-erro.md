# Formato de erro

> Toda falha da API sai no mesmo formato, o Problem Details (RFC 9457), com um `code` estável para o front e sem vazar nada interno.

| | |
|---|---|
| **Referência** | RFC 9457, "Problem Details for HTTP APIs" (rfc-editor.org/rfc/rfc9457), que torna obsoleta a RFC 7807; RFC 9110 (códigos de status); docs oficiais de ASP.NET Core, Spring, FastAPI, Hono, Fastify, Django REST framework e Laravel |
| **Categoria** | API |
| **Tipo** | Prática de contrato de erro |
| **Vale para** | APIs HTTP/JSON em qualquer stack; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

**Problem Details** é um formato padrão da IETF para dizer "deu errado" em JSON. A RFC 9457 substitui a RFC 7807 e mantém a ideia. O `Content-Type` é `application/problem+json`. Os campos padrão:

| Campo | Para que serve |
|---|---|
| `type` | URI que identifica o tipo do problema (pode ser só um identificador estável) |
| `title` | Resumo curto, igual para todo erro do mesmo tipo |
| `status` | O mesmo código HTTP da resposta |
| `detail` | Explicação deste caso, para quem lê |
| `instance` | Identifica esta ocorrência (a rota ou um id) |

Você pode somar **campos extras**. Neste doc usamos `code` (identificador estável para o front traduzir), `errors` (erros por campo) e `requestId`.

## Por que usar

- **Um só jeito de tratar erro no front:** um único interceptor serve a API inteira.
- **Padrão aberto:** bibliotecas e clientes já entendem.
- **Tradução e teste fácil:** o `code` não muda mesmo que o texto mude.
- **Suporte rápido:** o `requestId` leva direto ao log.
- **Segurança:** o formato fixo evita escapar stack trace e SQL.

## Quando usar

- Em toda API consumida por front, app ou outro sistema.
- Em qualquer status 4xx e 5xx, sem exceção, inclusive 401, 403, 404, 405 e 429.
- Nos erros gerados pelo framework (JSON inválido, rota inexistente), não só nos seus.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem API própria; basta a página de erro |
| MVP de SaaS | ✅ Ótimo | Custa um handler no começo e evita retrabalho no front |
| SaaS em crescimento | ✅ Ótimo | `code` estável sustenta tradução e métricas de erro |
| Sistema interno/corporativo | ✅ Ótimo | Vários times consomem a mesma API |
| API pública/integração | ✅ Ótimo | Padrão da IETF facilita a vida de quem integra |
| App mobile | ✅ Ótimo | Versões antigas do app dependem de `code` que não muda |

## Quando é bom

- **Previsível:** o front sempre sabe onde ler status, código e mensagem.
- **Erro de campo por campo:** a tela marca o campo certo.
- **Neutro de stack:** a maioria dos frameworks já tem suporte ou ponto de extensão.

## Quando é ruim

- **`detail` como contrato:** o texto muda; o front deve decidir por `code`, nunca por `detail`.
- **Vazar interno:** nunca ponha stack trace, SQL, nome de tabela ou caminho de arquivo no corpo. Registre no log e devolva só o `requestId`.
- **Status errado no corpo:** `status` precisa ser igual ao status HTTP.
- **Dois formatos na mesma API:** erros de framework fora do padrão quebram o interceptor.
- **Revelar demais:** "senha incorreta" e "e-mail não existe" separados ajudam atacante. Regras de login ficam na skill de segurança.

## Como começar

Regras:

1. Mesmo formato para 400, 401, 403, 404, 409, 422, 429 e 500.
2. `code` em `snake_case` ou `UPPER_SNAKE`, escolha um e mantenha. Aqui: `snake_case`.
3. Erro de validação (422) traz `errors`, uma lista com `field` e `message`, e um `code` por campo.
4. 500 devolve só mensagem genérica e `requestId`.
5. Validação da entrada: [tipos e validação na borda](../../coding/docs/06-tipos-e-validacao-na-borda.md). Tratamento interno: [tratamento de erros](../../coding/docs/05-tratamento-de-erros.md).

Resposta 422 ao agendar sem horário válido:

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://api.clinica.exemplo/problems/validation-error",
  "title": "Dados inválidos",
  "status": 422,
  "detail": "Corrija os campos indicados e tente de novo.",
  "instance": "/appointments",
  "code": "validation_error",
  "requestId": "req_8f3a2c",
  "errors": [
    { "field": "startsAt", "code": "date_in_past", "message": "O horário precisa ser futuro." },
    { "field": "patientId", "code": "required", "message": "Informe o paciente." }
  ]
}
```

Resposta 409 quando o horário já está ocupado:

```http
HTTP/1.1 409 Conflict
Content-Type: application/problem+json

{
  "type": "https://api.clinica.exemplo/problems/slot-taken",
  "title": "Horário indisponível",
  "status": 409,
  "detail": "O profissional já tem um agendamento nesse horário.",
  "instance": "/appointments",
  "code": "slot_taken",
  "requestId": "req_91be07"
}
```

Handler central em Hono (o mesmo desenho vale nas outras stacks):

```ts
class AppError extends Error {
  constructor(readonly status: number, readonly code: string, readonly title: string, readonly detail?: string) {
    super(title)
  }
}

app.onError((err, c) => {
  const requestId = c.get("requestId")
  if (err instanceof AppError) {
    return c.json({ type: `https://api.clinica.exemplo/problems/${err.code}`, title: err.title, status: err.status, detail: err.detail, instance: c.req.path, code: err.code, requestId }, err.status as 409, { "Content-Type": "application/problem+json" })
  }
  logger.error({ err, requestId })
  return c.json({ title: "Erro interno", status: 500, code: "internal_error", requestId }, 500, { "Content-Type": "application/problem+json" })
})
```

Em cada stack (confira o nome na versão que você usa):

| Stack | Onde gerar |
|---|---|
| ASP.NET Core | `AddProblemDetails()`, `IExceptionHandler` e `Results.Problem` / `Results.ValidationProblem` |
| Spring Boot | `ProblemDetail` e `@ExceptionHandler` / `ResponseEntityExceptionHandler` |
| FastAPI | `@app.exception_handler` e tratamento de `RequestValidationError` |
| Hono | `app.onError` |
| Fastify | `setErrorHandler` |
| Django REST framework | `EXCEPTION_HANDLER` em `REST_FRAMEWORK` |
| Laravel | `withExceptions` em `bootstrap/app.php` (render por tipo de exceção) |

Em todas, o `requestId` vem de um middleware que usa o header `X-Request-Id` recebido ou gera um novo, devolve no header da resposta e põe no log.

## Combina com / alternativas

- [Rotas, verbos e status](02-rotas-verbos-e-status.md): qual status usar em cada caso.
- [Idempotência e retries](06-idempotencia-e-retries.md): o cliente decide repetir pelo status e pelo `code`.
- [OpenAPI](07-openapi-e-documentacao.md): descreva o schema do erro uma vez e reuse em todas as rotas.
- [Testes de API](../../quality/docs/04-testes-de-api-e-contrato.md): um teste por status e formato.
- Alternativa: formato próprio `{ error: { code, message } }`. Funciona, mas perde o padrão e as ferramentas.

## Decisão rápida

- **Use se:** a API tem front, app ou integradores, e você quer um interceptor só e erros rastreáveis.
- **Evite se:** não há API HTTP, ou o protocolo já define o erro (GraphQL tem o seu `errors`).
