# architecture

Skill para o Claude Code que define a estrutura de pastas e arquivos de um projeto, para que seja fácil achar um arquivo e dar manutenção, seguindo a documentação oficial, os templates e os apps de referência de cada stack. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por padrão ou stack ([docs/](docs/)), com a árvore de pastas completa, quando usar, para que tipo de projeto, quando é bom, quando é ruim e por quê.

## O que é coberto

Só entrou o que passa em três critérios: convenção oficial ou prática amplamente aceita, utilidade real para achar e manter arquivos e custo razoável.

| Item | Papel | Documento |
|---|---|---|
| Feature-first e colocation | Pasta por assunto, teste e estilo ao lado | [docs/01-feature-first-colocation.md](docs/01-feature-first-colocation.md) |
| Vertical slice | Uma pasta por caso de uso | [docs/02-vertical-slice.md](docs/02-vertical-slice.md) |
| Camadas, Clean, hexagonal | Domínio isolado, quando vale o custo | [docs/03-camadas-clean-hexagonal.md](docs/03-camadas-clean-hexagonal.md) |
| Monólito modular | Módulos com fronteira, um deploy | [docs/04-monolito-modular.md](docs/04-monolito-modular.md) |
| Monorepo | pnpm workspaces, Turborepo e Nx | [docs/05-monorepo.md](docs/05-monorepo.md) |
| Next.js | App Router: arquivos, grupos, pastas privadas | [docs/06-nextjs.md](docs/06-nextjs.md) |
| React + Vite | SPA por features | [docs/07-react-vite.md](docs/07-react-vite.md) |
| React Native + Expo | Expo Router | [docs/08-react-native-expo.md](docs/08-react-native-expo.md) |
| NestJS, Hono, Fastify | Back-end Node por módulos | [docs/09-nestjs-node.md](docs/09-nestjs-node.md) |
| ASP.NET Core | Solução, projetos e slices | [docs/10-aspnet-core.md](docs/10-aspnet-core.md) |
| FastAPI e Django | Python por domínio | [docs/11-python-fastapi-django.md](docs/11-python-fastapi-django.md) |
| Laravel | Estrutura oficial + domínio | [docs/12-laravel.md](docs/12-laravel.md) |
| Go | Layout oficial de módulos | [docs/13-go.md](docs/13-go.md) |

O [docs/README.md](docs/README.md) tem o índice, um guia "Qual escolher" e a lista do que foi avaliado e saiu, com o motivo.

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/architecture ~/.claude/skills/architecture
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é criar um projeto, organizar pastas ou decidir onde pôr um arquivo. Também dá para chamar direto com `/architecture`. Exemplos:

- "Cria a estrutura de pastas de uma API em NestJS."
- "Onde eu coloco o teste e o estilo deste componente?"
- "/architecture reorganiza este projeto Next.js por funcionalidade."

Com a skill carregada, o Claude:

1. identifica a stack, o tipo e o tamanho do projeto;
2. escolhe a estrutura pela tabela do [SKILL.md](SKILL.md);
3. lê o documento escolhido antes de criar pastas;
4. monta a árvore seguindo as regras de uso (nome de pasta pelo domínio, colocation, `shared` só para o que é de várias features, convenção do framework primeiro);
5. registra a estrutura em um ARCHITECTURE.md ou AGENTS.md;
6. explica a escolha em uma ou duas frases.

## Estrutura

```
architecture/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md                      índice, "Qual escolher" e o que saiu da lista
    ├── 01-feature-first-colocation.md
    ├── 02-vertical-slice.md
    ├── 03-camadas-clean-hexagonal.md
    ├── 04-monolito-modular.md
    ├── 05-monorepo.md
    ├── 06-nextjs.md
    ├── 07-react-vite.md
    ├── 08-react-native-expo.md
    ├── 09-nestjs-node.md
    ├── 10-aspnet-core.md
    ├── 11-python-fastapi-django.md
    ├── 12-laravel.md
    └── 13-go.md
```

## Como manter

- **Adicionar um padrão ou stack:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua-o nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um documento:** apague o arquivo, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos, e registre o motivo em `docs/README.md`.
- **Revisar dados:** convenções de pasta e nomes de arquivo foram verificados em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar, principalmente quando o framework lançar versão maior.
