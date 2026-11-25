# Monorepo (pnpm workspaces, Turborepo e Nx)

> Um repositório com vários apps e pacotes, onde o gerenciador de pacotes liga tudo e uma ferramenta de tarefas roda só o que mudou.

| | |
|---|---|
| **Referência oficial** | turborepo.dev/docs/crafting-your-repository/structuring-a-repository; pnpm: pnpm.io/workspaces; Nx: nx.dev (Nx conferido em 2026-11-24: cache, grafo de projetos e geradores) |
| **Categoria** | Parte 1 — Padrões que valem para qualquer stack |
| **Tipo** | Padrão de organização de repositório |
| **Vale para** | Principalmente JavaScript e TypeScript; .NET e Go têm solução e módulos próprios |
| **Verificado em** | 2026-11-24 |

## O que é

Monorepo é um repositório com mais de um projeto. Em JavaScript, os workspaces do gerenciador de pacotes (declarados em `pnpm-workspace.yaml` ou no campo `workspaces`) ligam os pacotes locais entre si. O Turborepo ou o Nx rodam build, teste e lint em ordem e com cache, só no que foi afetado.

A documentação do Turborepo recomenda: aplicações e serviços em `apps/`, o resto (bibliotecas e configurações) em `packages/`, globs de um nível só (`apps/*`, `packages/*`), `package.json` raiz privado, `turbo.json` na raiz e um lockfile commitado.

## Por que usar

- **Pacotes internos:** a UI, os tipos e a config viram pacotes do workspace (turborepo.dev/docs/crafting-your-repository/structuring-a-repository).
- **Cache e execução seletiva:** recurso do Turborepo e do Nx (turborepo.dev/docs; nx.dev).

## Quando usar

- Dois ou mais apps que compartilham código (site, painel, API, app mobile).
- Biblioteca de UI ou de tipos usada por mais de um app.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Vários apps com pacotes compartilhados (site, app, API, UI, tipos) | ✅ Ótimo | É o modelo `apps/` + `packages/` do Turborepo |
| App único | ❌ Evite | Workspaces e cache só pagam quando há mais de um pacote |

Outros tipos: a documentação oficial não trata esses casos.

## Quando é bom

- **Config compartilhada:** o Turborepo prevê pacotes de configuração (TypeScript, ESLint) reutilizados pelos demais.
- **Cache e filtro por pacote afetado** (Turborepo e Nx).

## Quando é ruim

- **Importar por `../`:** a documentação do Turborepo manda instalar a dependência e importar pelo nome do pacote, nunca atravessar a fronteira com caminho relativo.
- **Barrel file em pacote:** a documentação do Turborepo recomenda o campo `exports` do `package.json` para evitar arquivos barrel.

## Como começar

Estrutura confirmada na documentação do Turborepo; os nomes dentro de `packages/` são exemplo.

```
meu-repo/
├── apps/                          # o que roda ou é publicado
│   ├── web/                       # site (Next.js, por exemplo)
│   │   ├── package.json
│   │   └── src/
│   ├── api/                       # servidor
│   └── mobile/                    # app Expo
├── packages/                      # o que é compartilhado
│   ├── ui/                        # componentes (@acme/ui)
│   │   ├── package.json           # name, exports, scripts
│   │   └── src/
│   ├── types/                     # tipos e schemas (@acme/types)
│   ├── config-typescript/         # tsconfig base
│   └── config-eslint/             # regras de lint
├── package.json                   # privado; scripts que chamam "turbo run"
├── pnpm-workspace.yaml            # packages: ["apps/*", "packages/*"]
├── pnpm-lock.yaml                 # lockfile commitado
└── turbo.json                     # tarefas (build, test, lint) e dependências entre elas
```

Regras de nome e lugar:

- **Nome do pacote com prefixo** (`@acme/ui`), único no workspace.
- **Cada pacote tem seu `package.json`**, seu tsconfig e seu `src/`.
- **Scripts com o mesmo nome** em todos (`build`, `test`, `lint`), para o Turborepo rodar em lote.
- **Provavelmente sem `tsconfig.json` raiz:** a documentação do Turborepo diz que em TypeScript você provavelmente não precisa dele; cada pacote estende uma base de outro pacote.
- **Dentro de cada app e pacote**, siga a estrutura da stack (por exemplo [Next.js](06-nextjs.md)).
- **Agrupar pacotes:** globs `packages/*` e `packages/grupo/*`, sem `package.json` em `grupo/` (mesma página).

## Combina com / alternativas

- [Next.js](06-nextjs.md), [NestJS](09-nestjs-node.md), [Expo](08-react-native-expo.md) como apps.
- [Monólito modular](04-monolito-modular.md): módulos podem virar pacotes.
- Nx: alternativa ao Turborepo, com geradores e grafo de projetos. Confirmado em nx.dev: cache local, grafo de projetos e geradores (`nx g`). Estrutura (nx.dev/docs/kb/folder-structure): o Nx aceita qualquer pasta; o guia dá duas convenções, plana (`packages/`) e agrupada (`apps/` + `libs/`, com app fina e a maior parte do código em `libs/`, agrupada por domínio). `nx.json` configura o Nx (nx.dev/docs/reference/nx-json); o projeto pode ser definido por `package.json` ou `project.json` (nx.dev/docs/reference/project-configuration). Licença MIT (LICENSE do repositório nrwl/nx, conferido via GitHub em 2026-11-24).
- Alternativa: repositórios separados com o pacote compartilhado publicado em um registro (npm).

## Decisão rápida

- **Use se:** há 2+ apps que compartilham código e o time é um só.
- **Evite se:** é um app só, ou os projetos não compartilham nada.
