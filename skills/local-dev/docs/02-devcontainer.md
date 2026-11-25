# Devcontainer e quando usar

> Coloque o editor dentro de um contêiner com o runtime, as ferramentas e as extensões certas, para que a máquina de cada pessoa deixe de importar.

| | |
|---|---|
| **Referência** | https://containers.dev/implementors/json_reference/ e https://containers.dev/implementors/features/ |
| **Categoria** | Ambiente de desenvolvimento |
| **Tipo** | Especificação aberta de ambiente em contêiner |
| **Vale para** | VS Code, GitHub Codespaces e outras ferramentas que suportam a especificação Dev Containers |
| **Verificado em** | 2026-11-25 |

## O que é

Um `devcontainer.json` descreve o contêiner em que você desenvolve: imagem, ferramentas (Features), portas e comandos de preparação. O editor abre o projeto dentro dele. Conferido na especificação em 2026-11-25:

- O arquivo fica em `.devcontainer/devcontainer.json`.
- Propriedades principais: `image` (ou `build`), `dockerComposeFile` e `service` (para usar Compose), `workspaceFolder`, `features`, `forwardPorts`, `postCreateCommand` e `remoteUser`.
- Features são pacotes instaláveis sobre qualquer imagem, referenciados como `ghcr.io/<namespace>/<feature>:<versão>`; sem versão, vale a `latest`. Fixe a versão.
- `customizations` guarda o que é de cada ferramenta (por exemplo, extensões do VS Code); a especificação só reserva o nome, e as chaves são definidas por cada ferramenta.

## Por que usar

- **Máquina nova em minutos:** abrir o projeto e esperar o contêiner montar.
- **Mesma versão de Node, Python ou .NET para todos.**
- **Isola o projeto:** nada de conflito entre versões globais.
- **Codespaces:** o mesmo arquivo serve para programar no navegador.
- **Agente de IA em ambiente descartável:** limite o estrago de comandos rodados sem supervisão (skill `ia`, doc 09).

## Quando usar

- Time com sistemas operacionais diferentes (macOS, Windows, Linux).
- Projeto com muitas ferramentas de sistema (compiladores, clientes de banco, `pg_dump`).
- Onboarding frequente, com estagiários ou terceiros.
- Quando se quer Codespaces.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ❌ Evite | `npm install` já resolve |
| MVP com uma pessoa | 🟡 Serve | Ganho pequeno; Compose para o banco costuma bastar |
| SaaS com time | ✅ Ótimo | Onboarding igual para todos |
| Sistema interno/corporativo | ✅ Ótimo | Máquinas restritas e ferramentas padronizadas |
| Projeto com muitas peças de sistema | ✅ Ótimo | O contêiner traz tudo instalado |
| App mobile (iOS) | ❌ Evite | Xcode não roda em contêiner Linux |
| Máquina com pouca RAM ou disco | ❌ Evite | O contêiner soma ao custo do Docker |

## Quando é bom

- **Configuração mínima:** imagem base, algumas Features e um `postCreateCommand`.
- **Reaproveita o Compose** do doc 01 para banco e cache.
- **Versionado no Git:** quem muda a ferramenta muda o arquivo.
- **Extensões e configurações do editor** acompanham o projeto.

## Quando é ruim

- **Lento em macOS e Windows** com arquivos montados da máquina; o I/O de disco do contêiner Docker Desktop é mais lento que o nativo.
- **Mais uma camada para depurar:** quando algo falha, é o projeto, o contêiner ou o Docker?
- **Obriga o time a usar editor compatível.**
- **Uso do Docker Desktop** tem licença própria para empresas grandes (skill `infra`, doc 04).
- **Imagem pesada** demora a baixar na primeira vez.

## Como começar

`.devcontainer/devcontainer.json` com imagem pronta, Features e um Compose já existente:

```json
{
  "name": "meu-app",
  "dockerComposeFile": ["../compose.yaml", "compose.dev.yaml"],
  "service": "workspace",
  "workspaceFolder": "/workspaces/meu-app",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "forwardPorts": [3000, 8025],
  "postCreateCommand": "npm ci",
  "remoteUser": "node"
}
```

`.devcontainer/compose.dev.yaml`:

```yaml
services:
  workspace:
    image: mcr.microsoft.com/devcontainers/javascript-node:24
    volumes:
      - ..:/workspaces/meu-app:cached
    command: sleep infinity
```

Para um projeto sem Compose, troque `dockerComposeFile` e `service` por `"image": "mcr.microsoft.com/devcontainers/javascript-node:24"`. A imagem `javascript-node` já traz o Node e o usuário `node` (com `sudo`), por isso o exemplo usa a Feature `github-cli`, que instala o `gh` por cima. A Feature `ghcr.io/devcontainers/features/node` serve para quem parte de uma imagem sem Node (use `:2`: a tag `:1` ficou na série 1.7 e a atual é a 2.1.2); a opção `version` dela aceita `lts`, `latest`, `none` ou um número como `"24"` (o padrão é `lts`).

Conferido em 2026-11-25 nas fontes oficiais, sem subir o contêiner (o daemon do Docker estava parado na máquina de teste): a tag `mcr.microsoft.com/devcontainers/javascript-node:24` existe no registro da MCR e a página da imagem lista as tags `24`, `24-trixie`, `24-bookworm`, `22` e `26`; a Feature `node` está na versão 2.1.2, com as tags de major `:1` e `:2` no registro `ghcr.io`, e a `github-cli` na 1.1.3, com `:1`. As tags mudam; confira o catálogo antes de usar.

Dentro do contêiner, o banco é acessado pelo nome do serviço (`db:5432`), não por `localhost`. Ajuste a `DATABASE_URL` do contêiner.

## Combina com / alternativas

- [01-docker-compose-banco-cache-fila-email.md](01-docker-compose-banco-cache-fila-email.md): dependências do contêiner.
- [07-readme-de-onboarding.md](07-readme-de-onboarding.md): documente as duas formas, com e sem devcontainer.
- Skill `ia`: rodar agentes sem supervisão em ambiente isolado.
- Alternativas: Compose só com as dependências e runtime na máquina (mais simples), `mise` ou `asdf` para fixar versões de runtime, Nix.

## Decisão rápida

- **Use se:** o time é misto, o setup passa de meia hora ou você quer Codespaces.
- **Evite se:** uma pessoa só, projeto simples ou máquinas fracas; use Compose e um gerenciador de versões.
