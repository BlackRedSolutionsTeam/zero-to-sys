# Painel separado do produto

> Dê ao painel um subdomínio, uma rota e, se possível, um deploy próprios, e proteja a porta na borda antes de qualquer login.

| | |
|---|---|
| **Referência** | Cloudflare Access (developers.cloudflare.com/cloudflare-one/policies/access/) e Tunnel; skill `cloudflare`, docs 06 e 07; skill `domains`, doc 03 |
| **Categoria** | Arquitetura e infra |
| **Tipo** | Prática de isolamento |
| **Vale para** | Qualquer sistema com painel, em qualquer stack |
| **Verificado em** | 2026-11-25 (limite de 50 usuários no plano grátis do Access conferido na skill `cloudflare` na mesma data; o restante é prática de arquitetura) |

## O que é

Três níveis de separação, do mais simples ao mais forte:

1. **Mesmo app, rota própria:** `/admin` dentro do produto, com guarda de papel.
2. **Mesmo repositório, deploy próprio:** `admin.empresa.com.br` publicado como outro serviço.
3. **Repositório e banco de acesso próprios:** o painel fala com a API interna e usa um usuário de banco separado ([doc 09](09-multiempresa-visao-da-equipe.md)).

## Por que usar

- Falha ou ataque no produto público não derruba nem expõe o painel.
- A proteção na borda só cobre o painel, sem mexer no produto.
- O código do painel pode mudar sem republicar o produto, e o inverso.

## Quando usar

- Nível 1 no MVP; nível 2 quando houver dinheiro, dado sensível ou equipe de mais de 3 pessoas; nível 3 quando houver exigência de auditoria.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Admin do CMS em rota própria |
| MVP de SaaS | ✅ Ótimo | Nível 1 ou 2, com Access na frente |
| SaaS em crescimento | ✅ Ótimo | Nível 2 ou 3 |
| Sistema interno/corporativo | ✅ Ótimo | Atrás de VPN ou Access |
| API/integração | ✅ Ótimo | Painel de chaves em subdomínio próprio |
| App mobile com backend | ✅ Ótimo | Painel web independente do app |
| `/admin` na mesma origem, sem camada na borda, com dados de pagamento | ❌ Evite | Um XSS no produto alcança o painel |

## Quando é bom

- **Subdomínio próprio** (`admin.`): cookies e CSP separados; não compartilhe cookie de sessão com o domínio do produto ([security, doc 02](../../security/docs/02-sessao-e-tokens.md)).
- **Cloudflare Access ou Tunnel na frente** ([cloudflare, doc 06](../../cloudflare/docs/06-tunnel-e-protecao-da-origem.md) e [doc 07](../../cloudflare/docs/07-access-e-zero-trust.md)): quem não é da equipe não chega à tela de login.
- **Origem fechada** para tudo que não vem da Cloudflare ([nginx](../../nginx/SKILL.md)).
- **`noindex`** e `robots.txt` bloqueando o subdomínio.
- **Deploy e variáveis** próprios; segredos do painel não vão para o produto.
- **Ambiente de staging** do painel também atrás do Access ([domains, doc 03](../../domains/docs/03-subdominios-e-ambientes.md)).

## Quando é ruim

- **Divulgar a URL** em página pública.
- **Mesma sessão** do produto: login de cliente com sessão de equipe.
- **CORS aberto** entre produto e painel.
- **Painel acessível só por IP fixo**: quebra para quem trabalha remoto; prefira identidade.

## Como começar

Estrutura de pastas por stack (a skill `architecture` decide o resto):

| Stack | Onde o painel fica |
|---|---|
| Next.js | `app/(admin)/...` com layout e guarda próprios, ou app separado em monorepo (`apps/admin`) |
| ASP.NET Core | Projeto `Admin` na solução, ou Area `Admin` com `[Authorize(Policy = "Staff")]` |
| Laravel | Painel Filament em `app/Filament`, com `->domain('admin.exemplo.com.br')` no provider do painel |
| Django | `admin.py` em cada app, em `admin.exemplo.com.br` por roteamento de host, ou projeto de settings próprio |

Roteamento por host em Next.js (`middleware.ts`):

```ts
import { NextResponse, type NextRequest } from "next/server";

export function middleware(req: NextRequest) {
  const host = req.headers.get("host") ?? "";
  const url = req.nextUrl.clone();
  if (host.startsWith("admin.")) {
    url.pathname = `/admin${url.pathname}`;
    return NextResponse.rewrite(url);
  }
  if (url.pathname.startsWith("/admin")) return new NextResponse(null, { status: 404 });
  return NextResponse.next();
}
```

Cabeçalho para o subdomínio do painel (nginx):

```nginx
add_header X-Robots-Tag "noindex, nofollow" always;
add_header Cache-Control "no-store" always;
```

Valide também o cabeçalho `Cf-Access-Jwt-Assertion` na aplicação, para que a requisição só valha se tiver passado pelo Access.

## Combina com / alternativas

- [Autenticação forte](04-autenticacao-forte-do-painel.md), [infra](../../infra/SKILL.md) para o deploy e [vps](../../vps/SKILL.md).

## Decisão rápida

- **Use** subdomínio próprio, Access na frente e sessão separada.
- **Evite** `/admin` público sem camada na borda e cookie compartilhado com o produto.
