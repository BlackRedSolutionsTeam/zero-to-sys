# Node.js para API (Hono, Fastify ou NestJS)

> Backend em TypeScript no Node: Hono para APIs enxutas, Fastify para APIs de uso geral, NestJS para times grandes que querem estrutura imposta.

| | |
|---|---|
| **Site** | https://hono.dev, https://fastify.dev, https://nestjs.com |
| **Categoria** | Área 4 — Backend e API (Node/TypeScript) |
| **Tipo** | Stack de backend, com três escolhas de framework |
| **Stack/composição** | Framework: Hono, Fastify ou NestJS. Linguagem: TypeScript. Banco: PostgreSQL. ORM: Drizzle ou Prisma. Validação: Zod. Auth: Better Auth ou biblioteca do framework. Contrato: OpenAPI. Testes: Vitest e testes de integração com banco real |
| **Preço** | Grátis (open source) |
| **Licença** | Fastify: MIT; Hono: MIT (registro npm e repositórios, conferidos em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Três jeitos de montar uma API em Node. Hono se descreve como pequeno e simples, feito sobre padrões da web, e roda em Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Netlify, AWS Lambda e Node.js (fonte: hono.dev/docs). Fastify se descreve como framework de baixo overhead, com arquitetura de plugins (fonte: fastify.dev) e validação por JSON Schema (fastify.dev/docs/latest/Reference/Validation-and-Serialization). NestJS organiza o app em módulos e tem injeção de dependência nativa (fonte: nestjs.com); sua arquitetura é bastante inspirada no Angular (fonte: docs.nestjs.com).

Comandos oficiais: `npm create hono@latest my-app` e `npm i -g @nestjs/cli` seguido de `nest new project-name`. A documentação do NestJS pede Node 20.19 ou superior (ou 22.12+ na linha 22) para rodar, e Node 22.22.3+, 24.15+ ou 26+ para os geradores do CLI (`nest new`, `nest generate`) (fonte: docs.nestjs.com/first-steps). Versões no npm em 2026-11-24: `hono` 4.13.22, `fastify` 5.12.8, `@nestjs/core` 12.6.0 e `@nestjs/cli` 12.0.15.

## Por que usar

- **Mesma linguagem do front:** TypeScript nos dois lados; os frameworks têm suporte a TypeScript (fonte: hono.dev, fastify.dev/docs/latest/Reference/TypeScript, nestjs.com).
- **I/O assíncrono:** o Node.js é um runtime assíncrono orientado a eventos, projetado para aplicações de rede escaláveis, e trata muitas conexões ao mesmo tempo (fonte: nodejs.org/en/about).
- **Três níveis de estrutura:** Hono (enxuto), Fastify (plugins) e NestJS (módulos e injeção de dependência).

## Quando usar

- **Hono:** API pequena ou média, funções de borda, BFF (backend para o front).
- **Fastify:** API de uso geral, com plugins e validação por JSON Schema.
- **NestJS:** quando se quer estrutura em módulos e injeção de dependência, ou o time vem de Angular (arquitetura inspirada nele, docs.nestjs.com).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| API para SPA ou mobile | ✅ Ótimo | Caso central, ver [SPA + API](04-spa-vite-api.md) |
| BFF / integração entre serviços | ✅ Ótimo | Hono documenta runtimes de borda e Fastify/NestJS documentam plugins e módulos para integração |
| Tempo real (chat, notificações) | ✅ Ótimo | Hono tem helper de WebSocket (hono.dev/docs/helpers/websocket) e NestJS tem gateways (docs.nestjs.com/websockets/gateways) |
| SaaS / app web | 🟡 Serve | Melhor [Next.js](02-nextjs-saas.md) se a base for única |
| Sistema interno corporativo | 🟡 Serve | Depende da stack da empresa; em casa .NET ou Java veja [.NET](07-dotnet-aspnet-core.md) e [Java](08-java-spring-boot.md) |
| E-commerce | 🟡 Serve | Sem recurso oficial específico; avalie caso a caso |
| Dados/IA, cálculo pesado | ❌ Evite | O Node roda o JavaScript no event loop; tarefa pesada de CPU bloqueia (fonte: nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop); considere [Python](06-python-fastapi-django.md) ou [Go](10-go-api.md) |
| Site de conteúdo | ❌ Evite | Para conteúdo veja [Astro](01-astro-conteudo.md) |

## Quando é bom

- **Hono:** roda em vários runtimes com o mesmo código (lista em hono.dev/docs).
- **Fastify:** validação e serialização por schema já no núcleo (fastify.dev/docs/latest/Reference/Validation-and-Serialization).
- **NestJS:** módulos, injeção de dependência, OpenAPI e Passport documentados (docs.nestjs.com/openapi/introduction e docs.nestjs.com/recipes/passport).
- **Ecossistema npm:** pacotes instalados pelo npm.

## Quando é ruim

- **Três frameworks:** Hono e Fastify não impõem arquitetura; a estrutura de pastas e camadas fica por conta do time.
- **CPU pesada:** o event loop executa o JavaScript; tarefa longa bloqueia as demais, e o Node oferece worker pool para tarefas caras (fonte: nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop).
- **NestJS:** exige módulos, providers e decorators (docs.nestjs.com), mais conceitos que um app Hono de um arquivo (nestjs.com diz que se pode começar com um arquivo).
- **Hono:** auth vem como middleware embutido (Basic, Bearer, JWT; hono.dev/docs/middleware/builtin/jwt); filas não fazem parte do Hono, você integra a biblioteca.
- **Risco de cadeia de suprimentos** nos pacotes npm: fixe versões e audite dependências com `npm audit` (docs.npmjs.com/cli/commands/npm-audit).
- **Tipos somem na compilação:** as anotações do TypeScript são apagadas e não mudam o comportamento em execução (fonte: typescriptlang.org/docs/handbook/2/basic-types.html); valide a entrada em runtime (Zod, ou JSON Schema no Fastify).

## Como começar

```bash
npm create hono@latest my-app
npm i -g @nestjs/cli && nest new project-name
```

Fastify: a instalação é `npm install fastify` (fonte: fastify.dev; versão no npm: 5.12.8, conferida em 2026-11-24). ORM e auth: veja os comandos do [documento do Next.js](02-nextjs-saas.md).

## Combina com / alternativas

- Front: [SPA com Vite](04-spa-vite-api.md), [mobile](11-mobile.md).
- [Go](10-go-api.md): outra linguagem de backend, veja o documento.
- [Python](06-python-fastapi-django.md): quando há dados e IA no meio.
- Estrutura de pastas: skill architecture. Hospedagem: skill infra.

## Decisão rápida

- **Use se:** o time é de JavaScript/TypeScript e a API é de I/O assíncrono (CRUD, integrações, WebSocket).
- **Evite se:** o trabalho é de CPU pesada, ou a empresa já tem backend padronizado em .NET, Java ou Python.
