# Paridade com produção: mesma versão de banco e runtime

> Rode localmente o mesmo banco, o mesmo runtime e os mesmos serviços da produção, nas mesmas versões, para o bug não nascer só no deploy.

| | |
|---|---|
| **Referência** | https://12factor.net/dev-prod-parity , https://www.postgresql.org/support/versioning/ , https://nodejs.org/en/about/previous-releases e https://hub.docker.com/_/postgres |
| **Categoria** | Consistência de ambientes |
| **Tipo** | Prática de ambiente local |
| **Vale para** | Qualquer projeto que vai para produção |
| **Verificado em** | 2026-11-25 |

## O que é

O método 12-factor pede manter desenvolvimento e produção o mais parecidos possível. Na prática: mesma **versão maior** do banco, mesmo **runtime** (Node, Python, .NET), mesmo tipo de cache e fila, mesma imagem base quando há contêiner.

Versões conferidas em 2026-11-25:

- **PostgreSQL:** o projeto publica atualizações menores pelo menos a cada três meses e recomenda rodar sempre a menor mais recente da sua versão maior. Na imagem oficial do Docker Hub existiam as linhas 19, 18 (18.7), 17 (17.12), 16 (16.16) e 15 (15.20). O PostgreSQL 14 parou de receber correções em 12/11/2026. Fixe a versão **maior** que a produção usa (`postgres:18`) e deixe a menor flutuar.
- **Node.js:** a página de releases mostrava as linhas 26, 24 e 22 como LTS; escolha a mesma LTS da produção e declare em `.nvmrc`, `.node-version` ou `engines`.
- **Redis:** imagens 8.12, 7.4 e 6.2; fixe a linha que a produção roda.

## Por que usar

- **Bug pego na máquina,** não no deploy: tipos, funções SQL e comportamento de índice mudam entre versões.
- **Migration confiável:** a que passou local passa em produção.
- **Menos "só dá erro lá".**

## Quando usar

- Em todo projeto, ao escolher o banco e o runtime.
- Ao atualizar versão de produção: atualize o local antes e na mesma PR.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | 🟡 Serve | Só o runtime do build |
| MVP / protótipo | ✅ Ótimo | Custa só fixar duas versões |
| SaaS | ✅ Ótimo | Banco gerenciado de versão conhecida |
| Sistema interno/corporativo | ✅ Ótimo | Produção costuma ter versão mais antiga e rígida |
| App mobile com backend | ✅ Ótimo | O backend precisa casar com o de produção |

## Quando é bom

- **Versão maior fixada** no `compose.yaml` (doc 01), no `.nvmrc` e na imagem do `Dockerfile`.
- **Uma fonte de verdade:** CI, Dockerfile e local leem a mesma versão (`.node-version`, `global.json`, `.python-version`).
- **Mesmos serviços:** se produção usa Redis, o local usa Redis, não um substituto em memória.
- **Banco gerenciado com a mesma maior** (skill `infra`, doc 05).

## Quando é ruim

- **`latest` no local:** o banco do notebook salta de versão sem aviso.
- **SQLite local e Postgres em produção:** SQL e tipos diferentes escondem erros.
- **Atualizar produção sem atualizar o local** (ou o contrário).
- **Versão em fim de vida:** o PostgreSQL 14 já saiu de suporte; o Node 22 entra no fim em 2027 (confira o calendário oficial).
- **Paridade total é impossível:** escala, latência e dados reais nunca serão iguais; aceite isso e use homologação para o resto.

## Como começar

```bash
psql --version
docker compose exec db postgres --version
node --version
cat .node-version
```

Fixe as versões:

```yaml
services:
  db:
    image: postgres:18
```

```text
24
```

Esse segundo bloco é o conteúdo do `.node-version`, na raiz. No `Dockerfile` use a mesma linha (`FROM node:24-slim`; veja a skill `infra`, doc 04).

Checklist de paridade: banco (versão maior e extensões), cache e fila (tipo e versão), runtime (LTS), fuso e locale do banco, variáveis de ambiente (nomes iguais, doc 03) e serviços externos (sandbox do mesmo provedor).

Para atualizar: suba a versão no Compose e no código na mesma PR, rode os testes, e só então atualize o banco de produção (backup antes: skill `infra`, doc 11).

## Combina com / alternativas

- [01-docker-compose-banco-cache-fila-email.md](01-docker-compose-banco-cache-fila-email.md): onde a versão do banco é fixada.
- [03-env-example-e-segredos-de-desenvolvimento.md](03-env-example-e-segredos-de-desenvolvimento.md): mesmos nomes de variável.
- Skill `infra`: Docker (doc 04), Postgres gerenciado (doc 05), backup (doc 11).
- Skill `data`: migrations (doc 04).
- Alternativas: homologação (staging) para o que o local não reproduz; Testcontainers com a mesma tag nos testes.

## Decisão rápida

- **Use se:** o sistema vai a produção com banco e runtime definidos.
- **Evite se:** o projeto é descartável e não tem produção.
