# OWASP no código

> Use o OWASP Top 10 como lista de ataques conhecidos e o ASVS nível 1 como checklist: cada ataque tem uma defesa simples que cabe em poucas linhas de código.

| | |
|---|---|
| **Referência** | OWASP Top 10:2025 (top10.owasp.org); OWASP ASVS 5.0.0 (asvs.owasp.org); OWASP Cheat Sheet Series; documentação do Helmet (helmetjs); MDN (CSP, CORS, cookies SameSite) |
| **Categoria** | Segurança |
| **Tipo** | Prática de código seguro |
| **Vale para** | Qualquer backend e frontend; exemplos em TypeScript (Node, Hono, Express) com tabela por stack |
| **Verificado em** | 2026-11-24 |

## O que é

O OWASP (projeto aberto de segurança de aplicações) publica o Top 10: as dez categorias de risco mais comuns. A edição atual conferida é a **2025**: A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions.

O ASVS (Application Security Verification Standard) é uma lista de requisitos verificáveis, em três níveis. A versão estável conferida é a 5.0.0. O nível 1 é o mínimo para qualquer sistema com login; use-o como checklist de revisão de PR.

Exemplo do doc: sistema de agendamento de clínica (pacientes, profissionais, agendamentos).

## Por que usar

- **Cobre o que mais derruba sistemas:** controle de acesso quebrado e injeção aparecem na lista há anos.
- **Defesa barata:** quase todas se resolvem com a biblioteca certa e uma regra de revisão.
- **Vocabulário comum:** "isso é um IDOR" encerra a discussão do PR.

## Quando usar

- Ao criar a primeira rota e ao revisar todo PR que lê entrada do usuário.
- Antes de ir para produção, como passada final.
- Ao integrar com serviço externo (URL, webhook, arquivo).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas entradas; headers e XSS já bastam |
| MVP de SaaS | ✅ Ótimo | Dados de clientes; IDOR e injeção são o risco real |
| SaaS em crescimento | ✅ Ótimo | Mais gente mexendo no código; o checklist vira regra de PR |
| Sistema interno/corporativo | ✅ Ótimo | "Interno" não impede ataque de dentro ou por link malicioso |
| API/integração | ✅ Ótimo | Sem tela, a validação e a autorização são toda a defesa |
| App mobile | ✅ Ótimo | A API é pública; o app não é barreira |
| Protótipo descartável com dados reais | ❌ Evite | Dado real pede o mínimo; use dado falso ou aplique o checklist |

## Quando é bom

- **Defesa na camada certa:** parametrizar a consulta evita injeção em todos os casos, em vez de "limpar" texto.
- **Padrão seguro por framework:** React, Django e Laravel escapam saída por padrão; o risco está em desligar isso.
- **Checklist curto e repetido** vence auditoria rara.

## Quando é ruim

- **Tratar OWASP como prova de segurança:** é piso, não teto.
- **"Limpar" entrada com regex** em vez de usar a defesa estrutural.
- **Copiar header de segurança sem entender:** um CSP errado quebra o site; teste antes de impor.
- **Fazer só no front:** validação e permissão no navegador não protegem nada.

## Como começar

Tabela de bolso: ataque, defesa e onde olhar.

| Ataque | Defesa | Onde olhar no código |
|---|---|---|
| Injeção (A05) | Consulta parametrizada; ORM sem SQL cru | Todo `query(`, `raw(`, `$queryRawUnsafe` |
| XSS | Escapar saída; nunca `innerHTML` com dado do usuário; CSP | `dangerouslySetInnerHTML`, `v-html`, `\|safe` |
| CSRF | Cookie `SameSite`; token anti-CSRF em formulário com cookie | Rotas POST/PUT/DELETE autenticadas por cookie |
| SSRF | Lista de hosts permitidos; bloquear IP interno | Todo `fetch(url)` onde `url` vem do usuário |
| IDOR (A01) | Checar dono e empresa em toda leitura por id | `findById(req.params.id)` sem filtro |
| Desserialização insegura (A08) | Só JSON validado com schema; nada de `pickle`/`unserialize` em dado externo | Parse de arquivo, fila, cookie assinado |
| Componentes vulneráveis (A03) | Auditar e atualizar dependências | `package.json`, lockfile, [dependências](08-dependencias-vulneraveis.md) |
| Erro que vaza detalhe (A02, A10) | Resposta genérica; detalhe só no log | `catch` que devolve `err.message` ou stack |
| Headers e CORS (A02) | Helmet; CORS com lista de origens | Middleware global |

**Injeção.** Ruim: o texto entra no SQL e vira comando. Bom: o valor viaja separado.

```ts
const ruim = await db.query(
  `select * from patient where name = '${req.query.name}'`
)

const bom = await db.query(
  'select * from patient where name = $1 and clinic_id = $2',
  [req.query.name, user.clinicId]
)
```

**IDOR** (acessar o registro de outro trocando o id na URL). Ruim: confia no id. Bom: o filtro de dono faz parte da consulta, e o não encontrado vira 404 (veja [papéis e permissões](04-papeis-e-permissoes.md) e [multiempresa](../../data/docs/06-multiempresa.md)).

```ts
const ruim = await db.appointment.findUnique({ where: { id } })

const bom = await db.appointment.findFirst({
  where: { id, clinicId: user.clinicId }
})
if (!bom) return c.json({ error: 'not_found' }, 404)
```

**XSS** (script injetado que roda no navegador de outra pessoa). O React escapa texto sozinho; o perigo é o HTML cru.

```tsx
const ruim = <div dangerouslySetInnerHTML={{ __html: patient.notes }} />

const bom = <div>{patient.notes}</div>
```

Se precisar de HTML do usuário (editor rico), passe por um sanitizador como DOMPurify antes. Cookie de sessão sempre `HttpOnly`, para o script não ler o cookie.

**SSRF** (o servidor busca uma URL escolhida pelo atacante e alcança a rede interna). Ruim: `fetch(req.body.url)`. Bom:

```ts
const allowed = new Set(['api.exemplo-laboratorio.com.br'])

function safeUrl(input: string): URL {
  const url = new URL(input)
  if (url.protocol !== 'https:' || !allowed.has(url.hostname)) {
    throw new Error('host_not_allowed')
  }
  return url
}
```

**Erros.** Ruim: `return c.json({ error: err.stack })`. Bom: registre o detalhe com um id e devolva só o id, no formato de [erro da API](../../api/docs/03-formato-de-erro.md).

```ts
app.onError((err, c) => {
  const id = crypto.randomUUID()
  logger.error({ id, err })
  return c.json({ error: 'internal_error', requestId: id }, 500)
})
```

**Headers (Helmet).** No Express, `app.use(helmet())` liga os padrões conferidos na documentação: Content-Security-Policy (`default-src 'self'` entre outras), Strict-Transport-Security (HSTS, força HTTPS), X-Content-Type-Options `nosniff`, Referrer-Policy e outros, e remove `X-Powered-By`. Ajuste o CSP ao seu front; se for API pura, o padrão serve.

**CORS** (quais sites podem chamar sua API pelo navegador). Ruim: `origin: '*'` com cookies. Bom:

```ts
import { cors } from 'hono/cors'

app.use('*', cors({
  origin: ['https://app.minhaclinica.com.br'],
  credentials: true
}))
```

**CSRF.** Com cookie de sessão, use `SameSite=Lax` (ou `Strict`) e, para ações sensíveis, token anti-CSRF; API com `Authorization: Bearer` não sofre CSRF.

Em cada stack:

| Stack | Injeção | Headers | CSRF |
|---|---|---|---|
| Node (Express/Fastify/Hono) | Driver com `$1`; Prisma/Drizzle | `helmet` / `@fastify/helmet` / `hono/secure-headers` | `SameSite` + token |
| ASP.NET Core | EF Core ou `SqlParameter` | Middleware próprio; HSTS com `UseHsts` | Antiforgery embutido |
| Django | ORM; `params` no `raw` | `SecurityMiddleware` | `CsrfViewMiddleware` ligado por padrão |
| Laravel | Eloquent/bindings `?` | Middleware próprio | `@csrf` ligado por padrão |

O `hono/secure-headers` é o middleware nativo do Hono, inspirado no Helmet; o `@fastify/helmet` é o plugin oficial do Fastify.

## Combina com / alternativas

- [Papéis e permissões](04-papeis-e-permissoes.md) (IDOR e A01) e [rate limit](06-rate-limit.md).
- [Upload de arquivos](07-upload-de-arquivos.md) e [dependências vulneráveis](08-dependencias-vulneraveis.md).
- [Segurança base da infra](../../infra/docs/12-seguranca-base.md) e [segredos](../../infra/docs/09-segredos-e-configuracao.md) para o que fica fora do código.
- [Formato de erro](../../api/docs/03-formato-de-erro.md) para o que devolver.
- Alternativa mais pesada: ASVS nível 2 e teste de invasão, para dados sensíveis em grande volume.

## Decisão rápida

- **Use se:** o sistema tem login, banco ou recebe qualquer entrada externa; ou seja, quase sempre.
- **Evite se:** a ideia é usar a lista como única garantia; combine com revisão, testes e [dependências em dia](08-dependencias-vulneraveis.md).
