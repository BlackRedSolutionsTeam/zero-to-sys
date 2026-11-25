# Back-end Node (NestJS, Hono e Fastify)

> NestJS organiza por módulos de funcionalidade, com `x.module.ts`, `x.controller.ts` e `x.service.ts` lado a lado; Hono e Fastify não impõem nada e seguem a estrutura dos seus guias oficiais.

| | |
|---|---|
| **Referência oficial** | docs.nestjs.com/modules (NestJS). Hono: guia "Best Practices" (hono.dev/docs/guides/best-practices), que recomenda handlers direto na rota em vez de controllers, mas não prescreve pastas. Fastify: template oficial do `fastify generate` (github.com/fastify/fastify-cli, `templates/app`), com `app.js`, `plugins/`, `routes/` e `test/` |
| **Categoria** | Parte 2 — Estrutura recomendada por stack |
| **Tipo** | Convenção de framework (NestJS), template oficial do fastify-cli e guia "Best Practices" do Hono |
| **Vale para** | APIs em Node com TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

No NestJS, um módulo agrupa o código de um domínio. A documentação mostra `CatsModule` com `CatsController` e `CatsService`, criados com `nest g module cats`. O arquivo se chama `<feature>.module.ts`, ao lado de `<feature>.controller.ts` e `<feature>.service.ts`. Um módulo compartilha provedores pelo `exports`. O `@Global()` existe, mas a documentação avisa: "tornar tudo global não é uma prática de design recomendada" (docs.nestjs.com/modules).

Hono e Fastify são mínimos. O Fastify tem o template do `fastify generate`: `plugins/` e `routes/` carregados pelo `app`. O Hono não traz pastas; o guia só manda montar um arquivo por assunto com `app.route` e escrever os handlers na rota.

## Por que usar

- **Módulos nativos no Nest:** `imports` e `exports` tornam explícito o que cada módulo expõe (docs.nestjs.com/modules).
- **Convenção de nome** `<feature>.module.ts`, `.controller.ts`, `.service.ts` na documentação e no `nest g resource`.
- **Hono e Fastify:** sem pastas impostas; seguem o guia Best Practices e o template do fastify-cli.

## Quando usar

- NestJS: API organizada em módulos por domínio.
- Hono ou Fastify: API pequena, com estrutura própria (guia do Hono; template do fastify-cli).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| API / back-end de negócio | ✅ Ótimo | Módulos por domínio, `nest g resource` gera o CRUD (docs.nestjs.com/recipes/crud-generator) |
| SaaS / app web | ✅ Ótimo | Um módulo por assunto, com `exports` explícitos (docs.nestjs.com/modules) |
| Sistema interno corporativo | ✅ Ótimo | Mesma convenção de módulo/controller/service da documentação |
| MVP / protótipo | 🟡 Serve | Hono e Fastify não exigem módulos nem controllers |
| Função serverless ou serviço fino | 🟡 Serve | Hono e Fastify não impõem camadas; avalie conforme o caso |
| Landing page / site estático | ❌ Evite | Não precisa de back-end |
| App sem back-end próprio | ❌ Evite | Use um BaaS |

## Quando é bom

- **Padrão oficial** de módulo no Nest (docs.nestjs.com/modules).
- **Dependências explícitas** nos módulos, via `imports` e `exports`.
- **Encaixa** em [monólito modular](04-monolito-modular.md), por módulos.

## Quando é ruim

- **Mais arquivos no Nest:** módulo, controller e service por assunto, contra o guia do Hono, que manda handlers direto na rota.
- **Módulo global em excesso:** esconde dependências, contra o conselho oficial.
- **Pastas `controllers/` e `services/` globais:** viram por tipo e perdem a vantagem dos módulos.
- **Dependência circular entre módulos:** a documentação trata em docs.nestjs.com/fundamentals/circular-dependency (`forwardRef`); evitar o ciclo é melhor.
- **Hono e Fastify não prescrevem pastas** (guia Best Practices; template fastify-cli): a convenção é do time.

## Como começar

NestJS. A árvore da documentação mostra `cats/` com `dto/`, `interfaces/` e os três arquivos, mais `app.module.ts` e `main.ts`. `entities/` é gerada por `nest g resource` (docs.nestjs.com/recipes/crud-generator). `common/` (decorators, filters, guards, interceptors, middleware, pipes) vem do app de referência nestjs/nest `sample/01-cats-app`. `config/configuration.ts` vem de docs.nestjs.com/techniques/configuration e de `sample/39-file-storage`. Conferido em 2026-11-24.

```
src/
├── main.ts                          # OFICIAL: inicia o app
├── app.module.ts                    # OFICIAL: módulo raiz, importa os demais
├── orders/                          # OFICIAL (padrão): um módulo por assunto
│   ├── dto/                         # OFICIAL: formato de entrada e saída
│   │   └── create-order.dto.ts
│   ├── entities/                    # OFICIAL (nest g resource): modelo do banco
│   │   └── order.entity.ts
│   ├── orders.controller.ts         # OFICIAL: rotas HTTP
│   ├── orders.controller.spec.ts    # teste ao lado (padrão do Nest)
│   ├── orders.service.ts            # OFICIAL: regra do assunto
│   ├── orders.service.spec.ts
│   └── orders.module.ts             # OFICIAL: registro e exports
├── users/                           # mesma forma
├── common/                          # OFICIAL (sample 01-cats-app): filtros, guards, pipes usados por todos
└── config/                          # OFICIAL (docs de configuração): leitura de variáveis
test/                                # testes de ponta a ponta
```

Fastify: árvore do template oficial do fastify-cli (`templates/app-ts-esm` em github.com/fastify/fastify-cli, conferido em 2026-11-24):

```
src/
├── app.ts                           # monta o app e carrega plugins e rotas
├── plugins/                         # plugins (sensible.ts, support.ts)
└── routes/                          # uma pasta por grupo de rotas
    ├── root.ts
    └── orders/
        └── index.ts                 # rotas de /orders
test/
├── helper.ts
├── plugins/
└── routes/
```

Hono: o guia "Best Practices" (hono.dev/docs/guides/best-practices, conferido em 2026-11-24) não prescreve pastas. Mostra um arquivo por assunto, ao lado do `index.ts`, cada um com `new Hono()` exportado e montado com `app.route()`, e manda escrever os handlers direto na rota, sem controllers:

```
index.ts                             # app principal, monta com app.route('/orders', orders)
orders.ts                            # sub-app de pedidos
users.ts
```

Regras de nome e lugar:

- **Nest:** `nome.tipo.ts` em `kebab-case` (`orders.service.ts`); classe em `PascalCase`.
- **Um módulo por assunto**, no plural; `exports` só do que outro módulo precisa.
- **Criação:** `nest g resource orders` gera a pasta completa.
- **`common/` e `shared/`** só com o que mais de um módulo usa.

## Combina com / alternativas

- [Monólito modular](04-monolito-modular.md) e [vertical slice](02-vertical-slice.md).
- [Monorepo](05-monorepo.md): `apps/api` com pacotes de tipos compartilhados.
- Alternativas: Express, ou outra stack ([Python](11-python-fastapi-django.md)).

## Decisão rápida

- **Use se:** a API se organiza em vários módulos de domínio (Nest); ou prefere estrutura própria (Hono, Fastify).
- **Evite se:** é só um site, ou a API é mínima e não precisa de módulos.
