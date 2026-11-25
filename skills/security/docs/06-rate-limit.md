# Rate limit

> Limite quantas requisições cada IP, usuário e rota podem fazer por período, com limites mais apertados em login e recuperação de senha, e responda 429 com `Retry-After`.

| | |
|---|---|
| **Referência** | RFC 6585 (429 Too Many Requests); RFC 9110 (Retry-After); OWASP Cheat Sheet Series; documentação do ASP.NET Core (Rate limiting middleware), Django REST framework (Throttling), django-ratelimit, Laravel, Cloudflare Turnstile e das bibliotecas citadas |
| **Categoria** | Segurança |
| **Tipo** | Prática de proteção contra abuso |
| **Vale para** | Qualquer API ou site com login; exemplos em TypeScript (Hono) com tabela por stack |
| **Verificado em** | 2026-11-24 |

## O que é

Rate limit (limite de taxa) é uma regra do tipo "no máximo 5 tentativas de login por minuto por IP". Passou do limite, o servidor recusa com o status 429 até a janela de tempo acabar.

Exemplo do doc: sistema de agendamento de clínica, com login de profissionais, recuperação de senha e busca de pacientes.

## Por que usar

- **Força bruta:** sem limite, um robô testa milhares de senhas por minuto no login.
- **Scraping:** alguém copia a lista de pacientes ou horários chamando a busca sem parar.
- **Custo:** rotas que mandam e-mail ou SMS (recuperação, 2FA) custam dinheiro a cada chamada.
- **Estabilidade:** um cliente com bug em laço infinito não derruba os outros.

A documentação do ASP.NET Core lembra que limite por requisição não substitui proteção contra DDoS (ataque distribuído); para isso use CDN/WAF.

## Quando usar

- Em toda rota pública, com um limite geral generoso.
- Com limite apertado em login, recuperação de senha, 2FA, cadastro e envio de e-mail/SMS.
- Em API aberta a terceiros, por chave de API.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | A CDN já absorve; limite só em formulários |
| MVP de SaaS | ✅ Ótimo | Login e recuperação expostos desde o dia um |
| SaaS em crescimento | ✅ Ótimo | Limite por usuário e por empresa evita um cliente prejudicar os outros |
| Sistema interno/corporativo | 🟡 Serve | Menos exposição; mantenha no login |
| API/integração | ✅ Ótimo | Cota por chave é parte do contrato |
| App mobile | ✅ Ótimo | A API é pública; o app não limita ninguém |
| Sistema com várias instâncias e limite só em memória | ❌ Evite | Cada instância conta sozinha e o limite real vira N vezes maior |

## Quando é bom

- **Limites por camadas:** geral por IP, por usuário logado e por rota sensível.
- **Chave certa:** no login, limite por IP e também por conta (e-mail), para barrar ataque que muda de IP.
- **Resposta clara:** 429 com `Retry-After` deixa o cliente esperar em vez de insistir.

## Quando é ruim

- **Só por IP:** vários usuários atrás do mesmo IP (escritório, rede móvel) são bloqueados juntos, e o atacante troca de IP.
- **Confiar em `X-Forwarded-For` sem proxy confiável:** o cliente escreve o cabeçalho e foge do limite. Configure qual proxy é confiável.
- **Bloquear conta por tentativas erradas:** permite que um atacante tranque a conta da vítima de propósito. Prefira atrasar e pedir captcha.
- **Chave sem fim:** particionar por dado que o usuário inventa enche a memória (a documentação do ASP.NET Core alerta para isso).

## Como começar

**Valores iniciais (ajuste com medição):**

| Rota | Chave | Limite sugerido |
|---|---|---|
| Geral | IP | 100 por minuto |
| API logada | usuário | 300 por minuto |
| `POST /login` | IP e e-mail | 5 por minuto |
| `POST /recuperar-senha` | IP e e-mail | 3 por hora |
| Envio de SMS/2FA | usuário | 5 por hora |

**Algoritmos:**

| Algoritmo | Como funciona | Cuidado |
|---|---|---|
| Janela fixa | Conta por janela (ex.: minuto) e zera no fim | Permite rajada dupla na virada da janela |
| Janela deslizante (sliding window) | Considera os últimos N segundos de forma contínua | Guarda mais estado |
| Token bucket (balde de fichas) | Fichas voltam a um ritmo fixo; permite rajada até o tamanho do balde | Bom para APIs; dois parâmetros para ajustar |

**Onde aplicar:**

| Camada | Serve para | Limite |
|---|---|---|
| CDN/WAF (veja [Cloudflare](../../infra/docs/08-cloudflare.md)) | Barrar volume e bots antes de chegar no servidor | Pouco contexto: não conhece o usuário logado |
| Aplicação | Regras por usuário, empresa e rota | Gasta recurso do servidor para recusar |
| Gateway | Um ponto só para várias instâncias e serviços | Mais uma peça para operar |

Use as duas primeiras juntas: borda para volume, aplicação para login e regras de negócio.

**Armazenamento:** Redis (ou Upstash, Redis gerenciado) é o padrão para várias instâncias. Memória só serve com instância única, e zera a cada deploy. Postgres funciona com baixo volume, mas cada requisição vira escrita no banco.

**Exemplo em Hono** (pacote `hono-rate-limiter`):

```ts
import { rateLimiter } from 'hono-rate-limiter'

const loginLimiter = rateLimiter({
  windowMs: 60_000,
  limit: 5,
  keyGenerator: (c) => c.req.header('cf-connecting-ip') ?? 'unknown'
})

app.post('/login', loginLimiter, loginHandler)
```

Em produção, passe também um `store` com Redis, senão a contagem fica em memória. Confira as opções na documentação do pacote.

**Resposta 429** (RFC 6585, com `Retry-After` em segundos, definido na RFC 9110), no formato de [erro da API](../../api/docs/03-formato-de-erro.md):

```ts
return c.json({ error: 'rate_limited' }, 429, { 'Retry-After': '60' })
```

O cliente deve esperar esse tempo antes de tentar de novo; veja [idempotência e retries](../../api/docs/06-idempotencia-e-retries.md).

**Bloqueio progressivo e captcha:** a cada falha, aumente a espera (1 s, 2 s, 4 s...). Depois de algumas falhas, exija um captcha. O Cloudflare Turnstile tem plano gratuito (conferido: até 20 widgets e 10 hostnames por widget, desafios ilimitados). O front envia o token, e o servidor valida:

```ts
const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ secret: env.TURNSTILE_SECRET, response: token })
})
const { success } = await res.json()
```

**Em cada stack:**

| Stack | Biblioteca |
|---|---|
| Hono | `hono-rate-limiter` |
| Fastify | `@fastify/rate-limit` |
| Express | `express-rate-limit` |
| ASP.NET Core | `AddRateLimiter` nativo (janela fixa, deslizante, token bucket e concorrência); `OnRejected` para o `Retry-After` |
| Django | `django-ratelimit` (`@ratelimit(key='ip', rate='5/m', block=True)`) ou throttling do DRF (`AnonRateThrottle`, `UserRateThrottle`, `ScopedRateThrottle`) |
| Laravel | `RateLimiter` com `throttle` nas rotas |
| FastAPI | `slowapi` (`@limiter.limit("5/minute")`, com `request: Request` no endpoint) |

No ASP.NET Core, os contadores ficam na memória de cada instância; com várias instâncias, use gateway ou um limitador próprio com repositório compartilhado. No DRF, as contagens ficam no cache do Django.

## Combina com / alternativas

- [Escolha do login](01-escolha-do-login.md), [recuperação e 2FA](03-recuperacao-e-2fa.md) (rotas que mais precisam de limite).
- [OWASP no código](05-owasp-no-codigo.md) e [upload de arquivos](07-upload-de-arquivos.md).
- [Cloudflare](../../infra/docs/08-cloudflare.md) para limite na borda e [idempotência e retries](../../api/docs/06-idempotencia-e-retries.md) para o lado do cliente.
- Alternativa: cota por plano comercial (contagem mensal no banco), que é regra de negócio, não proteção.

## Decisão rápida

- **Use se:** existe login, recuperação de senha, envio de e-mail/SMS ou API pública.
- **Evite se:** o limite fica só em memória com várias instâncias, ou se a única chave é o IP atrás de proxy não configurado.
