---
name: local-dev
description: 'Deixa o projeto no estado "clonou, rodou": Docker Compose, devcontainer, .env.example, seeds, scripts de uma linha, hooks de commit e onboarding. Use ao montar o repositório, quando alguém novo entra no time ou quando pedirem "ambiente local" ou "docker compose".'
---

# local-dev

Guia para deixar o projeto no estado clonou, rodou: quem entra no time sobe tudo em minutos, com as mesmas versões da produção e sem dado nem segredo real. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e exemplos prontos.

## Como usar esta skill

1. **Decida as versões** de banco e runtime pela produção ([doc 08](docs/08-paridade-com-producao.md)).
2. **Suba as dependências** com Compose ([doc 01](docs/01-docker-compose-banco-cache-fila-email.md)); só use devcontainer se o time justificar ([doc 02](docs/02-devcontainer.md)).
3. **Crie o `.env.example`** e ignore o `.env` ([doc 03](docs/03-env-example-e-segredos-de-desenvolvimento.md)).
4. **Ligue o seed** ao fluxo do dia 1 ([doc 04](docs/04-seeds-e-dados-de-teste-locais.md); receitas na skill `data`).
5. **Dê nomes curtos às tarefas** ([doc 05](docs/05-scripts-de-uma-linha.md)).
6. **Instale os hooks** depois de definir formatador e lint ([doc 06](docs/06-hooks-de-pre-commit-e-formatacao.md); ferramentas na skill `coding`).
7. **Escreva o README de onboarding** e teste com alguém de fora ([doc 07](docs/07-readme-de-onboarding.md)).
8. **Aponte o `CLAUDE.md`** para os atalhos do projeto (skill `ia`).

## Qual solução por situação

| Situação | Opção | Por quê |
|---|---|---|
| Projeto com banco | Compose só com as dependências | App roda fora, com debug e recarga rápidos |
| Time com macOS, Windows e Linux | Compose mais gerenciador de versões; devcontainer se o setup passar de meia hora | Menos camadas |
| Quer Codespaces | Devcontainer | Mesmo arquivo serve ao navegador |
| Projeto Node | npm scripts | Nada a instalar |
| Python, Go, .NET ou Laravel | `just` ou `make` | Atalhos independentes da linguagem |
| Time em Windows | npm scripts ou `just` | `make` pede instalação |
| Hook em projeto Node | Husky ou Lefthook | Husky sai do `package.json`; Lefthook não depende de Node |
| Hook em projeto Python | pre-commit | Padrão do ecossistema |
| Produção em versão antiga | Fixe a mesma maior localmente | Paridade vale mais que a versão nova |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Docker Compose | [docs/01-docker-compose-banco-cache-fila-email.md](docs/01-docker-compose-banco-cache-fila-email.md) | Postgres, cache, e-mail, healthcheck, perfis |
| Devcontainer | [docs/02-devcontainer.md](docs/02-devcontainer.md) | devcontainer.json, Features, Compose |
| .env e segredos | [docs/03-env-example-e-segredos-de-desenvolvimento.md](docs/03-env-example-e-segredos-de-desenvolvimento.md) | `.env.example`, `.gitignore`, o que nunca vai ao Git |
| Seeds | [docs/04-seeds-e-dados-de-teste-locais.md](docs/04-seeds-e-dados-de-teste-locais.md) | Fluxo do dia 1, usuários de teste |
| Scripts | [docs/05-scripts-de-uma-linha.md](docs/05-scripts-de-uma-linha.md) | npm scripts, just, make |
| Hooks | [docs/06-hooks-de-pre-commit-e-formatacao.md](docs/06-hooks-de-pre-commit-e-formatacao.md) | Husky, Lefthook, pre-commit |
| Onboarding | [docs/07-readme-de-onboarding.md](docs/07-readme-de-onboarding.md) | Pré-requisitos, passo a passo, problemas comuns |
| Paridade | [docs/08-paridade-com-producao.md](docs/08-paridade-com-producao.md) | Versões de banco e runtime iguais às da produção |

## Checklist

- [ ] `git clone`, `cp .env.example .env` e um comando sobem o sistema.
- [ ] `compose.yaml` com versões fixadas (nunca `latest`), healthcheck e portas em `127.0.0.1`.
- [ ] `.env` no `.gitignore` e `.env.example` completo, sem valor real.
- [ ] Nenhuma chave de produção na máquina de desenvolvimento.
- [ ] Seed de desenvolvimento idempotente, protegido contra produção, com usuários de teste listados.
- [ ] Atalhos `up`, `dev`, `test`, `lint`, `reset` e `clean` com o mesmo nome em todos os projetos.
- [ ] Hook de pré-commit rápido e o mesmo comando na CI.
- [ ] README com pré-requisitos versionados, passo a passo testado e problemas comuns.
- [ ] Versão maior do banco e runtime iguais às da produção.

## Regras de uso

- **Versão conferida.** Imagens, Compose e ferramentas mudam: confira na fonte oficial e cite a data.
- **Nunca `latest`.** Fixe a versão maior das imagens e dos runtimes.
- **Só valores de desenvolvimento.** Segredo de produção nunca vai ao `.env` local nem ao Git.
- **Dado real, nunca.** Seeds usam dados falsos; dump só anonimizado (skill `data`, doc 10).
- **Comece pelo mais simples.** Compose e um README bom resolvem a maioria; devcontainer só com motivo.
- **Teste o onboarding** com quem nunca rodou o projeto.
- **Sem comentários nos exemplos de código** (skill `coding`).
- **Fronteiras.** Docker, segredos e CI em produção são da `infra`; receitas de seed e LGPD, da `data`; lint e formatadores, da `coding`; `CLAUDE.md`, da `ia`; monorepo, da `architecture`.

## Quando a lista não cobre

Nix, Vagrant, Kubernetes local (kind, minikube), ambientes efêmeros por pull request e desenvolvimento mobile nativo (Xcode e Android Studio) ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial.

## Validade dos dados

Imagens do Docker Hub (Postgres, Redis, Mailpit), versões do Compose, do Node.js e das ferramentas de hook foram conferidas em 2026-11-25 nas páginas oficiais e mudam com frequência; cada documento tem a linha "Verificado em".
