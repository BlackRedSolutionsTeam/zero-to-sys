# stacks

Skill para o Claude Code que escolhe a stack completa de um sistema novo, com ferramentas gratuitas, de acordo com o tipo de projeto. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por stack ([docs/](docs/)), explicando a composição inteira, quando usar, para que tipo de projeto, quando é bom, quando é ruim e por quê.

## Stacks cobertas

Só entrou o que passa em três critérios: maturidade real, manutenção ativa e documentação oficial completa.

| Stack | Papel | Documento |
|---|---|---|
| Astro | Sites de conteúdo, institucionais e blogs | [docs/01-astro-conteudo.md](docs/01-astro-conteudo.md) |
| Next.js + Postgres + Drizzle + Better Auth | SaaS e app web full-stack em TypeScript | [docs/02-nextjs-saas.md](docs/02-nextjs-saas.md) |
| React Router / TanStack Start | Full-stack React sobre Vite | [docs/03-react-router-tanstack-start.md](docs/03-react-router-tanstack-start.md) |
| React + Vite + API separada | SPA com backend independente | [docs/04-spa-vite-api.md](docs/04-spa-vite-api.md) |
| Node (Hono, Fastify, NestJS) | APIs e tempo real em TypeScript | [docs/05-node-api.md](docs/05-node-api.md) |
| Python (FastAPI, Django) | Dados, IA e sistemas com admin | [docs/06-python-fastapi-django.md](docs/06-python-fastapi-django.md) |
| .NET (ASP.NET Core) | Sistema corporativo e interno | [docs/07-dotnet-aspnet-core.md](docs/07-dotnet-aspnet-core.md) |
| Java (Spring Boot) | Sistema corporativo e regulado | [docs/08-java-spring-boot.md](docs/08-java-spring-boot.md) |
| Laravel e Rails | Framework web completo (monólito) | [docs/09-laravel-rails.md](docs/09-laravel-rails.md) |
| Go | APIs, serviços de rede e CLI | [docs/10-go-api.md](docs/10-go-api.md) |
| Mobile (Expo, Flutter, nativo) | Apps de celular | [docs/11-mobile.md](docs/11-mobile.md) |
| Desktop (Tauri, Electron) | Apps de computador | [docs/12-desktop.md](docs/12-desktop.md) |

O [docs/README.md](docs/README.md) tem o índice, um guia "Qual escolher" e a lista do que foi avaliado e saiu, com o motivo.

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/stacks ~/.claude/skills/stacks
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é começar um sistema ou decidir tecnologia. Também dá para chamar direto com `/stacks`. Exemplos:

- "Qual stack eu uso para um SaaS de agendamento?"
- "Preciso de uma API para um app mobile; Node, .NET ou Go?"
- "/stacks monta o projeto base de um sistema interno de cadastros."

Com a skill carregada, o Claude:

1. verifica o que o projeto já tem e o que o time sabe;
2. identifica o tipo de projeto;
3. escolhe a stack pela tabela do [SKILL.md](SKILL.md);
4. lê o documento da stack antes de criar o projeto;
5. cria o projeto com os comandos oficiais e respeita as regras de uso (o que o time já sabe pesa mais que a moda, monólito primeiro, só grátis);
6. explica a escolha e o principal ponto fraco em poucas frases.

## Estrutura

```
stacks/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md                         índice, "Qual escolher" e o que saiu da lista
    ├── 01-astro-conteudo.md
    ├── 02-nextjs-saas.md
    ├── 03-react-router-tanstack-start.md
    ├── 04-spa-vite-api.md
    ├── 05-node-api.md
    ├── 06-python-fastapi-django.md
    ├── 07-dotnet-aspnet-core.md
    ├── 08-java-spring-boot.md
    ├── 09-laravel-rails.md
    ├── 10-go-api.md
    ├── 11-mobile.md
    └── 12-desktop.md
```

## Como manter

- **Adicionar uma stack:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua a stack nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover uma stack:** apague o documento, tire-a das três tabelas e dos links em "Combina com / alternativas" dos outros documentos, e registre o motivo em `docs/README.md`.
- **Revisar dados:** versões, comandos e licenças foram verificados em 2026-11-24. Cada documento tem a data na linha "Verificado em" e cita a fonte de cada dado; atualize-os ao revisar.
