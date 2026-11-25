# .env.example, segredos de desenvolvimento e o que nunca vai no repositório

> O repositório mostra quais variáveis existem; os valores de verdade ficam fora do Git, e os do desenvolvimento nunca são os de produção.

| | |
|---|---|
| **Referência** | https://12factor.net/config e https://docs.docker.com/compose/how-tos/environment-variables/ |
| **Categoria** | Configuração |
| **Tipo** | Prática de configuração local |
| **Vale para** | Qualquer stack que leia variáveis de ambiente |
| **Verificado em** | 2026-11-25 |

## O que é

- **`.env`:** arquivo local com os valores reais da sua máquina. Fica no `.gitignore`.
- **`.env.example`:** modelo versionado, com todos os nomes de variáveis e valores seguros de desenvolvimento ou vazios. É a documentação de configuração do projeto.
- **Segredo de desenvolvimento:** senha ou chave que só vale no ambiente local (a senha `app` do banco do Compose, uma chave de API em modo de teste).

Para o conceito geral e os gerenciadores de segredos de produção, veja a skill `infra`, doc 09. Aqui é só o ambiente local.

## Por que usar

- **Clonou, copiou, rodou:** `cp .env.example .env` basta para começar.
- **Nenhuma variável escondida:** quem adiciona uma variável nova a coloca no exemplo.
- **Evita vazamento:** valor real nunca passa pelo Git.
- **Falha cedo:** o app valida as variáveis na partida e diz o que falta.

## Quando usar

- Em todo projeto, no primeiro commit.
- Sempre que o código ganhar uma variável nova.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | 🟡 Serve | Poucas variáveis |
| MVP / protótipo | ✅ Ótimo | Banco, e-mail e chaves de teste |
| SaaS | ✅ Ótimo | Muitas integrações, um modelo por ambiente |
| Sistema interno/corporativo | ✅ Ótimo | Pode usar um gerenciador de segredos além do `.env` |
| App mobile com backend | ✅ Ótimo | Backend e chaves de serviços de teste |
| Repositório público | ✅ Ótimo | Só o exemplo vai ao Git |

## Quando é bom

- **`.env.example` completo e comentado pelo nome:** o próprio nome da variável explica (`SMTP_HOST`, `STRIPE_SECRET_KEY`).
- **Valores de desenvolvimento já funcionais:** combinam com o Compose do doc 01.
- **Chaves de terceiros em modo sandbox**, nunca a de produção.
- **Validação na partida** com um esquema (zod, pydantic-settings, Options do .NET).
- **Varredura de segredos** antes do commit e no GitHub (skill `infra`, doc 09).

## Quando é ruim

- **`.env` commitado:** apagar depois não limpa o histórico; trate a chave como vazada e troque.
- **Chave de produção na máquina de desenvolvimento:** um notebook perdido vira incidente.
- **Dump de produção no `.env`** ou no banco local: veja a skill `data`, doc 10.
- **Segredo por chat ou e-mail:** use o gerenciador de senhas ou de segredos do time.
- **`.env.example` desatualizado:** quem clona perde horas descobrindo o que falta.
- **Valores reais no exemplo:** vira vazamento versionado.

## Como começar

`.env.example`:

```dotenv
DATABASE_URL=postgres://app:app@localhost:5432/app
REDIS_URL=redis://localhost:6379
SMTP_HOST=localhost
SMTP_PORT=1025
APP_URL=http://localhost:3000
SESSION_SECRET=troque-por-um-valor-aleatorio
STRIPE_SECRET_KEY=
```

`.gitignore`:

```gitignore
.env
.env.*
!.env.example
```

```bash
cp .env.example .env
openssl rand -hex 32
git check-ignore -v .env
git ls-files | grep -E '(^|/)\.env($|\.)'
```

- O `openssl rand -hex 32` gera um valor aleatório para `SESSION_SECRET`.
- O `git check-ignore` confirma que o `.env` está ignorado; o último comando lista arquivos `.env` já versionados por engano (só `.env.example` deve aparecer).
- O Compose lê `.env` na raiz para substituir `${VARIAVEL}` no `compose.yaml`; para passar as variáveis ao contêiner, use `env_file`.
- Para segredos de time sem gerenciador, use um cofre de senhas compartilhado; para equipes maiores, um gerenciador com acesso por papel (skill `infra`, doc 09).
- Se um `.env` real vazar para o Git: revogue a chave, gere outra e só depois limpe o histórico.

## Combina com / alternativas

- [01-docker-compose-banco-cache-fila-email.md](01-docker-compose-banco-cache-fila-email.md): os valores de desenvolvimento batem com o Compose.
- [06-hooks-de-pre-commit-e-formatacao.md](06-hooks-de-pre-commit-e-formatacao.md): hook que bloqueia segredo.
- Skill `infra`, doc 09: gerenciadores de segredos e rotação.
- Skill `data`, doc 10: dados pessoais e LGPD.
- Alternativas: `direnv`, `dotenvx` (arquivo criptografado versionado), Infisical (`infisical run`).

## Decisão rápida

- **Use se:** o projeto lê qualquer configuração por variável de ambiente.
- **Evite se:** não há o que evitar; a única variação é a ferramenta (`.env`, direnv ou gerenciador).
