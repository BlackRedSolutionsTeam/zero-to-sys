# Cache e performance na Cloudflare

> Deixe a Cloudflare cachear só o que é igual para todo mundo (arquivos estáticos), nunca página logada nem resposta com `Set-Cookie`, e mande o `Cache-Control` certo pela origem.

| | |
|---|---|
| **Referência** | developers.cloudflare.com/cache (comportamento padrão, Cache Rules, purge, Tiered Cache) e /speed (Brotli, HTTP/3) |
| **Categoria** | Borda |
| **Tipo** | Prática de cache e desempenho |
| **Vale para** | Domínios com proxy ligado (nuvem laranja) |
| **Verificado em** | 2026-11-25 |

## O que é

Cache é uma cópia guardada perto do visitante. Se a Cloudflare tem a cópia, responde sem chamar seu servidor. Isso deixa o site mais rápido e a origem mais leve.

O risco é servir a cópia errada: a página de um paciente aparecer para outro. Por isso a regra central deste doc é o que **não** cachear.

Exemplo: `clinica-exemplo.com.br` com site público, `app.` (SPA logada) e `api.`.

## Por que usar

- **Velocidade:** imagens, CSS e JS saem da borda.
- **Menos carga** na VPS, que pode ser pequena.
- **Menos banda** da origem em picos.

## Quando usar

- Em qualquer site com arquivos estáticos.
- Em API só quando a resposta é pública e igual para todos (lista de especialidades, por exemplo).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Dá para cachear até o HTML com regra e purge |
| MVP de SaaS | 🟡 Serve | Só estáticos (`/assets`); HTML da app fica sem cache |
| SaaS em crescimento | ✅ Ótimo | Estáticos com hash e TTL longo; áreas logadas em bypass |
| Sistema interno/corporativo | 🟡 Serve | Pouco público; cache só de estáticos |
| API/integração | 🟡 Serve | Padrão é não cachear JSON; cache só de rotas públicas |
| App mobile com backend | 🟡 Serve | API autenticada em bypass; imagens e mídia podem cachear |
| Qualquer página com dados por usuário ou com `Set-Cookie` | ❌ Evite | Risco de vazar dados de um usuário para outro |

## Quando é bom

- **Nomes com hash** (`app.3f9a1c.js`): cacheie por um ano sem medo.
- **Origem manda `Cache-Control` correto:** a Cloudflare obedece e você quase não precisa de regra.
- **Imagens e vídeos** pesados saem da VPS.

## Quando é ruim

- **Cache de HTML dinâmico** sem critério: serve dado velho ou de outro usuário.
- **Arquivo sem hash com TTL longo:** o usuário continua com o JS antigo após o deploy; só o purge resolve.
- **Cache Rule ampla demais** (`/*` elegível): cacheia o que não devia, inclusive rotas de API.
- **Purge de tudo a cada deploy:** a origem leva um pico de requisições (e o purge em massa tem limite no plano grátis).

## Como começar

### O que é cacheado por padrão (conferido em 2026-11-25)

- A Cloudflare decide pela **extensão** do arquivo, não pelo tipo MIME. A lista inclui imagens (jpg, png, svg, webp, avif...), CSS, JS, fontes (woff, woff2, ttf, otf), PDF, zip e vídeos como mp4.
- **HTML e JSON não são cacheados por padrão.**
- Não cacheia se `Cache-Control` é `private`, `no-store`, `no-cache` ou `max-age=0`.
- Não cacheia se a resposta tem `Set-Cookie`.
- Só cacheia requisições GET.
- Cacheia se `Cache-Control` é `public` com `max-age` maior que zero ou `Expires` no futuro. Se houver os dois, vale o `max-age`.
- Sem cabeçalhos: 200, 206 e 301 ficam 120 minutos; 302 e 303, 20 minutos; 404 e 410, 3 minutos.
- Tamanho máximo de arquivo cacheável: 512 MB nos planos Free, Pro e Business. Upload de 100 MB no Free e no Pro.

### Cache-Control da origem

A origem é a fonte da verdade. Valores sugeridos:

```
Cache-Control: public, max-age=31536000, immutable
Cache-Control: no-store
Cache-Control: public, max-age=300
```

- A primeira vai em arquivos com hash no nome.
- `no-store` vai em páginas e respostas de usuário logado.
- A terceira serve para HTML público que pode ficar 5 minutos velho (página de especialidades).

### Cache Rules

No painel: Caching, Cache Rules, Create rule. Passos: nome, expressão de filtro, Cache eligibility (Bypass cache ou Eligible for cache), posição, Deploy. O DNS precisa estar com proxy. O plano grátis permite 10 regras (conferido). As opções de TTL de borda e de navegador ficam na página de configurações da regra; confira lá antes de usar.

Use o Rules simulator (na própria página) para testar se uma URL casa com a regra.

### Regras seguras por tipo de projeto

Site de conteúdo:

1. Estáticos (`/assets/*`, imagens, fontes): elegível, respeitando o cache da origem.
2. HTML público: elegível só com TTL curto e purge no deploy.
3. `/admin`, `/wp-login`, `/preview`: bypass.

SaaS (`app.clinica-exemplo.com.br`):

1. `/assets/*` com hash: elegível, TTL longo.
2. Todo o resto do host, incluindo HTML da app: bypass.
3. Qualquer requisição com cookie de sessão ou cabeçalho `Authorization`: bypass.

API (`api.clinica-exemplo.com.br`):

1. Host inteiro em bypass.
2. Exceção explícita só para rotas públicas e idênticas para todos, com TTL curto.

Em todas, a primeira regra a escrever é a de bypass das áreas logadas.

### Nunca cachear

- Página ou API de usuário autenticado.
- Qualquer resposta com `Set-Cookie`.
- Respostas com dados pessoais (LGPD), como prontuário, agenda e exames.

Confirme no navegador (aba Rede): o cabeçalho `cf-cache-status` indica se veio da borda. Em páginas logadas ele nunca deve dizer HIT.

### Purge

- **Por URL** (recomendado): rápido e barato.
- Por hostname, prefixo, tag (cache-tag) ou tudo.
- Limites no Free (conferido): 5 requisições por minuto para hostname, tag, prefixo e tudo; 800 URLs por segundo para purge por URL, até 100 por requisição.
- Se usar chave de cache personalizada com cabeçalhos ou cookies, o purge por URL do painel pode não funcionar; use a API.

### Tiered Cache, Brotli e HTTP/3

- **Tiered Cache:** a borda consulta outra camada da Cloudflare antes da origem. Smart Topology está em todos os planos, inclusive Free. Em Caching, Tiered Cache, ligue e escolha Smart. Via API: PATCH em `/zones/$ZONE_ID/argo/tiered_caching`. A função agora também aparece no produto Smart Shield; consulte os termos atuais.
- **Compressão:** Free usa Zstandard por padrão, Pro e Business usam Brotli, Enterprise usa Gzip. Só comprime se o navegador aceitar. Ajuste com Compression Rules.
- **HTTP/3:** em Speed, Settings, Protocol Optimization, ligue HTTP/3. Todos os planos. Vale só entre visitante e Cloudflare, não até a origem.

## Combina com / alternativas

- [DNS e proxy](02-dns-e-proxy.md): cache só funciona com a nuvem laranja.
- [WAF e rate limit](05-waf-rate-limit-e-bots.md): proteção que roda antes do cache.
- [Pages e Workers](08-pages-e-workers.md): site estático já nasce na borda.
- [Cloudflare na infra](../../infra/docs/08-cloudflare.md).
- Alternativa: cache na própria origem (nginx), sem CDN.

## Decisão rápida

- **Use se:** o projeto tem arquivos estáticos, imagens ou HTML público que muda pouco.
- **Evite se:** a resposta depende de quem está logado, tem `Set-Cookie` ou carrega dado pessoal.
