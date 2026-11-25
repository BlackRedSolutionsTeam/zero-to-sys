# Next.js (SaaS full-stack em TypeScript)

> Stack para SaaS e apps web com uma base de código só: Next.js no front e no servidor, Postgres com Drizzle, autenticação com Better Auth.

| | |
|---|---|
| **Site** | https://nextjs.org |
| **Categoria** | Área 2 — SaaS e app web full-stack em TypeScript |
| **Tipo** | Stack completa opinativa |
| **Stack/composição** | Frontend: Next.js (App Router), React, Tailwind, shadcn/ui. Backend: Server Actions e Route Handlers do próprio Next. Banco: PostgreSQL. ORM: Drizzle (alternativa: Prisma). Auth: Better Auth. Testes: Vitest (unidade), Playwright (ponta a ponta) |
| **Preço** | Grátis (open source). Hospedagem à parte, veja a skill infra |
| **Licença** | Next.js: MIT; Better Auth: MIT; Drizzle ORM: Apache-2.0 (LICENSE nos repositórios, conferidos em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Next.js é um framework React com roteamento por pastas e arquivos, componentes de servidor e de cliente, Server Actions para alterar dados e Route Handlers para endpoints HTTP (fontes: nextjs.org/docs/app/getting-started/layouts-and-pages, /server-and-client-components, /mutating-data e /route-handlers). Tela e backend ficam no mesmo repositório, em TypeScript.

A versão atual no npm é a 16.4.6 (conferido em 2026-11-24). A documentação de instalação lista Turbopack como bundler padrão, "Cache Components" no setup recomendado e Node.js 20.9 como versão mínima (fonte: nextjs.org/docs/app/getting-started/installation).

Drizzle é um ORM com schema em TypeScript e migrações geradas pelo drizzle-kit (fonte: orm.drizzle.team/docs/get-started/postgresql-new). Nessa página, os pacotes aparecem com a tag `@rc`; no npm, a tag `latest` do drizzle-orm é a 0.45.4 e a `rc` é a 1.0.0-rc.6 (conferido em 2026-11-24). Confira antes de fixar a versão. Better Auth é um framework de autenticação para TypeScript com plugins; a documentação cobre e-mail e senha e login social (fontes: better-auth.com/docs/authentication/email-password e /authentication/github).

Para autenticação, a documentação do Next.js descreve autenticação, gerenciamento de sessão e autorização e os recursos do React e do Next.js para cada uma (fonte: nextjs.org/docs/app/guides/authentication). O Better Auth tem guia de integração com o Next.js (fonte: better-auth.com/docs/integrations/next).

## Por que usar

- **Um idioma só:** tela, Server Actions e Route Handlers são TypeScript no mesmo projeto (fontes: nextjs.org/docs/app/getting-started/mutating-data e /route-handlers).
- **Auth documentada:** guia oficial de autenticação, sessão e autorização (nextjs.org/docs/app/guides/authentication).
- **Testes documentados:** guias oficiais para Vitest e Playwright (nextjs.org/docs/app/guides/testing).
- **Pronto para agentes de código:** o `create-next-app` pode incluir um `AGENTS.md` (nextjs.org/docs/app/getting-started/installation).

## Quando usar

- SaaS, painel, área logada, app B2B.
- MVP que pode virar produto.
- Site com partes públicas (SEO) e partes logadas no mesmo projeto.
- Time que já sabe React e TypeScript.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS / app web | ✅ Ótimo | Server Actions, Route Handlers e guia oficial de autenticação (nextjs.org/docs/app/guides/authentication) |
| Dashboard / painel admin | ✅ Ótimo | Área logada com layouts aninhados e formulários com Server Actions (nextjs.org/docs/app/guides/forms) |
| MVP / protótipo | 🟡 Serve | Um projeto cobre tela, servidor e auth; a escolha pesa mais pelo que o time já sabe (SKILL.md) |
| E-commerce | 🟡 Serve | Páginas estáticas e dinâmicas no mesmo projeto (nextjs.org/docs/app/guides/rendering-philosophy); pagamento via serviço externo |
| Site institucional / blog | 🟡 Serve | Funciona, mas o [Astro](01-astro-conteudo.md) foi desenhado para sites de conteúdo (docs.astro.build/en/concepts/why-astro) |
| Sistema interno corporativo | 🟡 Serve | Serve se o time é de JavaScript; em empresa .NET ou Java, siga a stack da casa |
| API pura para vários clientes | 🟡 Serve | Dá para expor endpoints com Route Handlers (nextjs.org/docs/app/getting-started/route-handlers); para API como produto veja [Hono/Fastify/NestJS](05-node-api.md) |
| Tempo real | ❌ Evite | A documentação trata de streaming de resposta e avisa que nem toda plataforma serverless o suporta (nextjs.org/docs/app/guides/streaming); sem recurso oficial de WebSocket lido; use [Go ou Node](05-node-api.md) |
| Dados/IA pesada | ❌ Evite | Sem recurso oficial de dados e IA no Next.js lido; veja [Python](06-python-fastapi-django.md) |
| App mobile | ❌ Evite | O Next.js é framework web; para app de celular veja [Expo ou Flutter](11-mobile.md) |

## Quando é bom

- **Tudo no mesmo repositório:** uma mudança de dados e tela vai no mesmo PR.
- **Renderização flexível:** o Next.js trata conteúdo estático e dinâmico como um espectro, por componente (nextjs.org/docs/app/guides/rendering-philosophy).
- **Popularidade:** cerca de 143,7 mil estrelas no GitHub (vercel/next.js, conferido em 2026-11-24).
- **Auth e banco no seu repositório:** Better Auth (MIT) e Drizzle (Apache-2.0) são bibliotecas, sem serviço hospedado obrigatório (LICENSE nos repositórios).
- **Hospedagem:** só exige um servidor Node.js; `next start` atende todos os recursos (nextjs.org/docs/app/guides/deploying-to-platforms).

## Quando é ruim

- **Mudanças de cache entre versões:** no Next.js 15, `fetch` deixou de ser cacheado por padrão (nextjs.org/docs/app/guides/upgrading/version-15); o 16 traz Cache Components e Turbopack como padrão (nextjs.org/docs/app/guides/upgrading/version-16). Atualizar exige ler os guias de upgrade.
- **Fronteira servidor/cliente:** é preciso decidir o que roda em cada lado (nextjs.org/docs/app/getting-started/server-and-client-components).
- **Acoplamento:** quem usa Server Actions para a regra de negócio tem de expor outro endpoint para um segundo cliente, como um app mobile; Route Handlers cumprem esse papel (nextjs.org/docs/app/getting-started/route-handlers).
- **Hospedagem:** em ambiente serverless, o cache em disco é de curta duração e por instância, e nem toda plataforma suporta streaming (nextjs.org/docs/app/guides/self-hosting e /guides/streaming).
- **Drizzle em transição:** a documentação de início usa pacotes com a tag `@rc` (veja "Como começar").

## Como começar

Comando da documentação oficial (nextjs.org/docs/app/getting-started/installation):

```bash
pnpm create next-app@latest my-app --yes
```

O `--yes` usa os padrões salvos ou os padrões da ferramenta: TypeScript, Tailwind CSS, ESLint, App Router e Turbopack, alias `@/*`, e inclui `AGENTS.md`. Depois, dados e auth (comandos de orm.drizzle.team/docs/get-started/postgresql-new e better-auth.com/docs/concepts/cli; pacotes do Drizzle com a tag `@rc`):

```bash
npm i drizzle-orm@rc pg dotenv
npm i -D drizzle-kit@rc tsx @types/pg
npm install better-auth
npx auth@latest generate
```

Migrações: `npx drizzle-kit generate` e `npx drizzle-kit migrate` (mesma página do Drizzle; ela também mostra `npx drizzle-kit push` para testes locais). O `npx auth@latest generate` cria o schema do Better Auth para o seu ORM. Componentes e ícones: skill design (shadcn/ui, Lucide). Testes: Vitest e Playwright, com guias em nextjs.org/docs/app/guides/testing.

## Combina com / alternativas

- [React Router/TanStack Start](03-react-router-tanstack-start.md): alternativa full-stack em React.
- [SPA + API](04-spa-vite-api.md): quando o backend precisa servir mais de um cliente.
- [Laravel/Rails](09-laravel-rails.md): frameworks completos para quem não precisa de TypeScript.
- Alternativa de ORM: Prisma (licença Apache-2.0, conferida no registro npm e no GitHub em 2026-11-24).

## Decisão rápida

- **Use se:** o time sabe React/TypeScript e o produto é um SaaS ou app web com parte pública e parte logada.
- **Evite se:** o backend vai servir vários clientes, precisa de conexão longa ou processamento pesado, ou a empresa já padronizou outra linguagem.
