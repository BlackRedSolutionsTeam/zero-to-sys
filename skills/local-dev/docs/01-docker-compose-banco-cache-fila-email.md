# Docker Compose para banco, cache, fila e e-mail local

> Suba Postgres, cache, fila e um servidor de e-mail falso com um comando, na mesma versão da produção, sem instalar nada na máquina de quem entra no time.

| | |
|---|---|
| **Referência** | https://docs.docker.com/compose/ , https://docs.docker.com/reference/compose-file/services/ , https://hub.docker.com/_/postgres , https://hub.docker.com/_/redis e https://hub.docker.com/r/axllent/mailpit |
| **Categoria** | Dependências locais |
| **Tipo** | Prática de ambiente local |
| **Vale para** | Qualquer stack que dependa de banco, cache, fila ou e-mail |
| **Verificado em** | 2026-11-25 |

## O que é

O Docker Compose descreve vários contêineres num arquivo e sobe todos com `docker compose up`. No ambiente local ele roda só as **dependências** (banco, cache, fila, e-mail); o app roda na máquina, com recarga rápida. Para empacotar o app em si, veja a skill `infra`, doc 04.

Conferido em 2026-11-25 na documentação oficial:

- O Compose atual é o v2 (e o v5, funcionalmente idêntico, que só acrescenta um SDK em Go). O v1 é legado.
- O campo `version:` no topo do arquivo é obsoleto e ignorado: não escreva.
- Os exemplos oficiais usam o nome `compose.yaml`.
- Imagem oficial do Postgres: linhas 19, 18, 17, 16 e 15 no Docker Hub (18.7 e 17.12 são os patches atuais). A partir do Postgres 18 o volume declarado é `/var/lib/postgresql`; nas versões 17 e anteriores é `/var/lib/postgresql/data`.
- Imagem oficial do Redis: 8.12 (`latest`), 7.4 e 6.2. O Redis 8 ou mais novo usa licença tripla (RSALv2, SSPLv1 ou AGPLv3); o 7.4 a 7.8 usa RSALv2 ou SSPLv1. Para uso local não muda nada, mas confira com o jurídico se for distribuir a imagem.
- Mailpit (`axllent/mailpit`): interface web na porta 8025 e SMTP na 1025; mantém as portas padrão do MailHog.

## Por que usar

- **Zero instalação:** não precisa de Postgres na máquina nem de versão conflitando entre projetos.
- **Reprodutível:** todo mundo roda a mesma versão, no mesmo arquivo versionado.
- **Descartável:** `docker compose down -v` apaga tudo e recomeça limpo.
- **E-mail sem risco:** o Mailpit captura tudo e nunca envia para cliente de verdade.

## Quando usar

- Em todo projeto com banco, desde o primeiro commit.
- Quando o sistema envia e-mail (cadastro, recuperação de senha) e você precisa ver a mensagem.
- Quando produção usa cache ou fila e o código local precisa da mesma peça.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ❌ Evite | Sem banco nem fila |
| MVP / protótipo | ✅ Ótimo | Postgres e Mailpit em 15 linhas |
| SaaS | ✅ Ótimo | Banco, cache, fila e e-mail iguais à produção |
| Sistema interno/corporativo | ✅ Ótimo | Sobe o banco do sistema sem pedir acesso a servidor |
| App mobile com backend | ✅ Ótimo | O backend local roda com as mesmas dependências |
| Projeto que usa só SQLite | 🟡 Serve | Só faz sentido se houver fila, cache ou e-mail |

## Quando é bom

- **Só as dependências no Compose:** o app roda fora, com debug e recarga normais.
- **Versão fixada** (`postgres:18`, nunca `latest`).
- **Healthcheck:** quem depende do banco espera ele estar pronto.
- **Portas presas em `127.0.0.1`:** o banco não fica exposto na rede do café.
- **Volume nomeado** para os dados sobreviverem a `docker compose down`.

## Quando é ruim

- **`latest` sem fixar:** um dia o banco muda de versão e quebra o ambiente de todos.
- **Senha de produção no arquivo:** use valores de desenvolvimento (doc 03).
- **Tudo no Compose, até o app:** perde recarga rápida e debug no editor.
- **Máquina com pouca RAM:** Docker Desktop e vários serviços pesam; suba só o que o projeto usa (use `profiles`).
- **Docker Desktop em empresa grande:** o uso gratuito tem limite de porte (veja a skill `infra`, doc 04); alternativas são Colima, Podman ou OrbStack, com o mesmo `compose.yaml`.

## Como começar

`compose.yaml` na raiz do projeto:

```yaml
services:
  db:
    image: postgres:18
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - db-data:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 5s
      timeout: 3s
      retries: 10

  cache:
    image: redis:8-alpine
    ports:
      - "127.0.0.1:6379:6379"
    profiles: ["cache"]

  mail:
    image: axllent/mailpit
    ports:
      - "127.0.0.1:1025:1025"
      - "127.0.0.1:8025:8025"

volumes:
  db-data:
```

```bash
docker compose up -d --wait
docker compose --profile cache up -d --wait
docker compose ps
docker compose logs -f db
docker compose down
docker compose down -v
```

- `--wait` espera os healthchecks ficarem saudáveis antes de devolver o terminal.
- Serviço com `profiles` só sobe quando o perfil é pedido; sem perfil, sobe sempre.
- Se o Postgres do projeto for 17 ou anterior, troque o volume para `/var/lib/postgresql/data`.
- Abra `http://localhost:8025` para ver os e-mails que o app mandou para `localhost:1025`.

Para o app esperar o banco dentro do próprio Compose:

```yaml
services:
  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
```

Fila: use a mesma peça da produção (RabbitMQ ou Redis, conforme o projeto) com imagem de versão fixa. Storage de arquivos compatível com S3 pode usar MinIO ou o emulador do provedor.

## Combina com / alternativas

- [02-devcontainer.md](02-devcontainer.md): o devcontainer pode usar este mesmo Compose.
- [03-env-example-e-segredos-de-desenvolvimento.md](03-env-example-e-segredos-de-desenvolvimento.md): a URL do banco vem do `.env`.
- [05-scripts-de-uma-linha.md](05-scripts-de-uma-linha.md): `make up` ou `just up` esconde os comandos.
- [08-paridade-com-producao.md](08-paridade-com-producao.md): mesma versão de banco da produção.
- Skill `infra`: Docker e Kubernetes (doc 04), Postgres gerenciado (doc 05).
- Alternativas: Postgres instalado no sistema (mais rápido, mas diverge entre máquinas), Testcontainers só para testes, Postgres embutido em memória (menos fiel).

## Decisão rápida

- **Use se:** o projeto tem banco, cache, fila ou envia e-mail.
- **Evite se:** o projeto é estático ou só usa SQLite sem outras dependências.
