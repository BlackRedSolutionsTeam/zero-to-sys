# Scripts de uma linha: make, just ou npm scripts

> Um nome curto para cada tarefa (`up`, `test`, `reset`, `clean`) esconde os comandos longos e serve de documentação executável.

| | |
|---|---|
| **Referência** | https://just.systems/man/en/ , https://www.gnu.org/software/make/manual/ e https://docs.npmjs.com/cli/using-npm/scripts |
| **Categoria** | Automação local |
| **Tipo** | Atalhos de tarefas do projeto |
| **Vale para** | Qualquer projeto; escolha a ferramenta pela stack |
| **Verificado em** | 2026-11-25 |
| **Testado com** | `just` 1.59.0 (macOS arm64, binário oficial do GitHub), em pasta temporária: receita padrão, `set dotenv-load`, dependência entre receitas, `just up` dentro de receita, `[private]` e `set default-list` |

## O que é

Um arquivo na raiz que mapeia nomes curtos a comandos:

- **npm scripts** (`package.json`): já vêm com o Node, nada a instalar.
- **`just`:** executor de comandos com sintaxe inspirada no `make`, mas pensado para tarefas, não para compilar (manual em just.systems). Lê o `.env` para preencher variáveis, aceita parâmetros e lista as tarefas.
- **`make`:** presente em Linux e macOS; no Windows exige instalação à parte. Foi feito para compilar arquivos, então tarefas "falsas" precisam de `.PHONY`.

## Por que usar

- **Um vocabulário só:** `up`, `test`, `reset`, `clean` em todo projeto da empresa.
- **Documentação que executa:** o README aponta para o arquivo em vez de copiar comandos.
- **CI e local iguais:** a pipeline chama o mesmo `test` que você roda.
- **Menos erro:** não se esquece uma flag.

## Quando usar

- Quando o passo a passo de subir o projeto passa de dois comandos.
- Quando há comandos longos de Docker, migration ou lint que o time repete.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | 🟡 Serve | `npm run dev` e `build` bastam |
| Projeto Node/TypeScript | ✅ Ótimo | npm scripts, sem ferramenta extra |
| Projeto Python, Go, .NET ou Laravel | ✅ Ótimo | `just` ou `make` como atalho independente da linguagem |
| Monorepo | ✅ Ótimo | Um `justfile` na raiz orquestra os pacotes (skill `architecture`, doc 05) |
| Time em Windows | 🟡 Serve | Prefira npm scripts ou `just`; `make` pede instalação |

## Quando é bom

- **Nomes padronizados:** `up`, `down`, `dev`, `test`, `lint`, `reset`, `clean`.
- **Uma linha por tarefa**, chamando comandos já documentados.
- **Lista autoexplicativa:** `just --list` ou `make help` mostra o que existe.
- **Sem lógica dentro:** se virou programa, vire um script de verdade (`scripts/`).

## Quando é ruim

- **Scripts que escondem demais:** ninguém mais sabe o que roda por baixo.
- **Dois sistemas ao mesmo tempo** (Makefile e npm scripts repetindo): escolha um.
- **Comandos destrutivos sem aviso:** `clean` e `reset` apagam dados; o nome deve deixar isso claro.
- **`make` em time com Windows** sem WSL.
- **Depender de uma ferramenta que ninguém instalou:** documente a instalação no onboarding (doc 07).

## Como começar

npm scripts:

```json
{
  "scripts": {
    "up": "docker compose up -d --wait",
    "down": "docker compose down",
    "dev": "npm run up && next dev",
    "test": "vitest run",
    "lint": "biome check",
    "reset": "docker compose down -v && npm run up && prisma migrate reset --force && prisma db seed",
    "clean": "docker compose down -v --remove-orphans"
  }
}
```

`justfile`:

```just
set dotenv-load

[private]
default:
    @just --list

up:
    docker compose up -d --wait

down:
    docker compose down

dev: up
    npm run dev

test:
    npm test

reset:
    docker compose down -v
    just up
    npm run db:reset

clean:
    docker compose down -v --remove-orphans
```

`Makefile`:

```make
.PHONY: up down test reset clean

up:
	docker compose up -d --wait

down:
	docker compose down

test:
	npm test

reset:
	docker compose down -v
	$(MAKE) up
	npm run db:reset

clean:
	docker compose down -v --remove-orphans
```

No Makefile, a indentação precisa ser com tabulação. O `justfile` roda a primeira receita quando se digita só `just`; por isso `default` vem primeiro, e `[private]` a esconde da própria lista. Com `set dotenv-load`, o `just` lê o `.env` da pasta e deixa as variáveis disponíveis nas receitas (`$DB_URL`); o padrão é `false`. Uma alternativa é `set default-list`, que lista as receitas sem precisar de uma receita `default`.

Instale o `just` pelo gerenciador de pacotes da página de pacotes do manual (just.systems/man/en/packages.html): `brew install just` no macOS, `winget install --id Casey.Just --exact` no Windows, `apt install just` no Debian 13 e Ubuntu 24.04, `dnf install just` no Fedora, `cargo install just` onde há Rust. O `down -v` apaga os volumes, ou seja, o banco local inteiro; o `reset` serve para recomeçar do zero.

## Combina com / alternativas

- [01-docker-compose-banco-cache-fila-email.md](01-docker-compose-banco-cache-fila-email.md): comandos de `up` e `down`.
- [04-seeds-e-dados-de-teste-locais.md](04-seeds-e-dados-de-teste-locais.md): o atalho `reset`.
- [07-readme-de-onboarding.md](07-readme-de-onboarding.md): o README cita só os atalhos.
- Skill `ia`: o `CLAUDE.md` lista os atalhos (`just test`, `just lint`) para o agente rodar e verificar.
- Skill `architecture`, doc 05: tarefas em monorepo.
- Alternativas: Taskfile (`task`), `mise tasks`, scripts em `scripts/*.sh`.

## Decisão rápida

- **Use se:** o time repete os mesmos comandos longos.
- **Evite se:** o projeto tem dois comandos e o `package.json` já resolve.
