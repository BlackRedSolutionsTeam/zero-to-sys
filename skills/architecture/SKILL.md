---
name: architecture
description: Define a estrutura de pastas e arquivos de um projeto para que seja fácil achar um arquivo e dar manutenção, seguindo a documentação oficial, os templates e os apps de referência de cada stack (feature-first, colocation, vertical slice, camadas, monólito modular, monorepo, Next.js, React + Vite, Expo, NestJS, ASP.NET Core, FastAPI, Django, Laravel, Go). Use sempre que for criar um projeto do zero, reorganizar pastas, decidir "onde coloco este arquivo", "como organizo as pastas", "qual estrutura usar", "monorepo ou não", "separar em módulos" ou escrever o ARCHITECTURE.md do projeto.
---

# architecture

Guia de decisão para estruturar pastas e arquivos de um projeto. Cada padrão e cada stack tem um documento em `docs/` com quando usar, para que tipo de projeto, pontos fortes, limitações e a árvore de pastas completa, com a fonte oficial de cada item (documentação, template ou app de referência do framework).

## Como usar esta skill

1. **Descubra a stack, o tipo e o tamanho do projeto** antes de desenhar pastas: framework, se é front, back-end ou os dois, quantas pessoas, quantos assuntos de negócio. Olhe a estrutura que já existe. Em projeto existente, a estrutura atual e o AGENTS.md ou ARCHITECTURE.md têm prioridade sobre esta lista.
2. **Escolha a estrutura pela tabela abaixo.** Primeiro a convenção da stack (parte 2), depois o padrão de organização (parte 1) para o que o framework deixa livre.
3. **Leia o documento escolhido** em `docs/` antes de criar pastas. Veja "Quando é ruim" e "Como começar".
4. **Crie a árvore do documento** adaptando os nomes ao domínio do projeto. Comece pequeno: não crie pasta vazia "para o futuro".
5. **Aplique as regras de uso** abaixo.
6. **Registre a estrutura** em um ARCHITECTURE.md (ou AGENTS.md) na raiz, com a árvore e a regra de onde pôr cada coisa.
7. **Explique a escolha em uma ou duas frases.**

## Qual estrutura usar

| Stack ou tipo de projeto | Estrutura | Documento |
|---|---|---|
| Qualquer projeto com 3+ assuntos de negócio | Por feature + colocation | [01](docs/01-feature-first-colocation.md) |
| Next.js (App Router) | Convenção do App Router + `features/` | [06](docs/06-nextjs.md) |
| SPA React + Vite, ou ilhas React em Astro | `app/`, `common/`, `features/` | [07](docs/07-react-vite.md) |
| App mobile React Native + Expo | `src/app` só de rotas + `features/` | [08](docs/08-react-native-expo.md) |
| API em Node (NestJS, Hono, Fastify) | Módulos por assunto (Nest); rotas e plugins (Fastify) | [09](docs/09-nestjs-node.md) |
| API em C# / ASP.NET Core | Solução e projetos como no dotnet/eShop | [10](docs/10-aspnet-core.md) |
| Back-end Python (FastAPI, Django) | Template oficial do FastAPI / app por assunto | [11](docs/11-python-fastapi-django.md) |
| Laravel | Estrutura oficial (`laravel/laravel`) | [12](docs/12-laravel.md) |
| Back-end ou CLI em Go | Layout de módulos do go.dev | [13](docs/13-go.md) |
| API com muitos casos de uso independentes | Vertical slice | [02](docs/02-vertical-slice.md) |
| Domínio rico, sistema longo, time grande | Camadas dentro de cada módulo | [03](docs/03-camadas-clean-hexagonal.md) |
| Sistema médio ou grande, um deploy | Monólito modular | [04](docs/04-monolito-modular.md) |
| 2+ apps que compartilham código | Monorepo (pnpm + Turborepo) | [05](docs/05-monorepo.md) |
| Projeto pequeno, MVP, landing page | Convenção da stack, poucas pastas, sem padrão extra | o da stack |

| Padrão ou stack | Documento | Papel |
|---|---|---|
| Feature-first e colocation | [docs/01-feature-first-colocation.md](docs/01-feature-first-colocation.md) | Pasta por assunto, teste e estilo ao lado |
| Vertical slice | [docs/02-vertical-slice.md](docs/02-vertical-slice.md) | Uma pasta por caso de uso |
| Camadas, Clean, hexagonal | [docs/03-camadas-clean-hexagonal.md](docs/03-camadas-clean-hexagonal.md) | Domínio isolado, quando vale o custo |
| Monólito modular | [docs/04-monolito-modular.md](docs/04-monolito-modular.md) | Módulos com fronteira, um deploy |
| Monorepo | [docs/05-monorepo.md](docs/05-monorepo.md) | Vários apps e pacotes, pnpm e Turborepo |
| Next.js | [docs/06-nextjs.md](docs/06-nextjs.md) | Convenções do App Router |
| React + Vite | [docs/07-react-vite.md](docs/07-react-vite.md) | SPA por features (e nota de Astro) |
| React Native + Expo | [docs/08-react-native-expo.md](docs/08-react-native-expo.md) | Expo Router |
| Node (NestJS, Hono, Fastify) | [docs/09-nestjs-node.md](docs/09-nestjs-node.md) | Módulos por assunto (Nest); rotas e plugins (Fastify) |
| ASP.NET Core | [docs/10-aspnet-core.md](docs/10-aspnet-core.md) | Solução e projetos (eShop) |
| Python (FastAPI, Django) | [docs/11-python-fastapi-django.md](docs/11-python-fastapi-django.md) | Template FastAPI e apps Django |
| Laravel | [docs/12-laravel.md](docs/12-laravel.md) | Estrutura oficial |
| Go | [docs/13-go.md](docs/13-go.md) | Layout oficial do go.dev |

## Regras de uso

- **A convenção do framework ganha da preferência pessoal.** Onde o framework define pasta ou arquivo (`app/` do Next.js, `routes/` do Laravel, `internal/` do Go), siga-o. Escolha o padrão só para o que ele deixa livre.
- **O nome da pasta diz o domínio, não o tipo.** `orders/`, `billing/`, não `services/` e `helpers/` com tudo dentro.
- **Por feature primeiro, por tipo dentro dela.** `orders/components`, `orders/api.ts`, não `components/orders`.
- **Colocation:** teste, estilo e tipo ficam ao lado do código que servem.
- **`shared/` (ou `common/`, o nome do Redux Style Guide) só para o que mais de uma feature usa.** Nasce dentro da feature e só sobe quando a segunda precisar. Nada de `utils/` genérico.
- **Arquivo `index` ou barrel com cuidado.** Use `index.ts` como porta pública de uma feature, não em todas as pastas. O Next.js documenta que pacotes que exportam centenas de módulos (como bibliotecas de ícones) causam problemas de desempenho e oferece `optimizePackageImports` (nextjs.org/docs/app/guides/package-bundling). Em pacotes de monorepo, prefira o campo `exports` do `package.json`, recomendado pelo Node.js (nodejs.org/api/packages.html).
- **Uma coisa por arquivo.** Um componente, uma classe, um caso de uso. O nome do arquivo diz o que ele é.
- **Nomes de arquivo consistentes.** Um padrão de caixa por projeto (`kebab-case`, `PascalCase` ou `snake_case`, conforme a stack) e um sufixo para o papel (`.service`, `.test`, `Endpoint`).
- **Feature não importa de feature por caminho interno.** Só pela porta pública. Reforce com lint ou projeto separado.
- **Comece pequeno e divida quando doer.** Pasta nova só quando há arquivos que a justifiquem.
- **Padrão pesado só com motivo.** Camadas, microserviços e monorepo têm custo. Registre por que o projeto precisa deles.
- **Documente a estrutura.** ARCHITECTURE.md ou AGENTS.md na raiz com a árvore, o critério de onde pôr cada coisa e as regras de importação.
- **Fronteiras com outras skills.** Qual stack escolher é da skill stacks. Estilo dentro do arquivo (nome de função, tamanho, erros) é da coding. Hospedagem e deploy são da infra.

## Quando a lista não cobre

Se a stack não está aqui (Rails, Spring, Flutter, Rust, Elixir, Svelte Kit, Nuxt), diga isso ao usuário. Procure a página de estrutura de pastas da documentação oficial, aplique as regras de uso acima e marque no ARCHITECTURE.md o que é convenção do framework e o que é escolha do time. O `docs/README.md` registra o que foi avaliado e saiu da lista.

## Validade dos dados

As convenções foram verificadas na documentação oficial em 2026-11-24 (Next.js, Expo, NestJS, FastAPI, Django, Laravel 12.x e 13.x, go.dev e Turborepo). Itens que não puderam ser confirmados estão marcados nos documentos. Frameworks mudam nomes de arquivo (por exemplo `middleware.ts` virou `proxy.ts` no Next.js); confira a versão do projeto antes de criar arquivos especiais.
