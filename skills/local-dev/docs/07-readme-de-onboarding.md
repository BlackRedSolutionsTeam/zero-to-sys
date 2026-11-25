# README de onboarding

> Um README que leva alguém do `git clone` ao sistema rodando em minutos: pré-requisitos, passo a passo e os problemas que sempre aparecem.

| | |
|---|---|
| **Referência** | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes e https://www.makeareadme.com |
| **Categoria** | Documentação |
| **Tipo** | Prática de onboarding |
| **Vale para** | Qualquer repositório com mais de uma pessoa |
| **Verificado em** | 2026-11-25 |

## O que é

A seção "Como rodar" do `README.md` (ou um `docs/onboarding.md`) escrita para quem nunca viu o projeto. O teste é simples: alguém de fora do projeto segue o texto, sem ajuda, e chega ao login funcionando. Quando algo travar, o erro vai para o README, não para o chat.

## Por que usar

- **Onboarding sem interrupção:** o time não vira suporte do novato.
- **Setup testado a cada mudança:** o README quebra quando o projeto muda.
- **Agente de IA também lê:** o `CLAUDE.md` pode apontar para ele (skill `ia`, doc 01).

## Quando usar

- Antes de chamar a segunda pessoa para o projeto.
- Sempre que o passo a passo mudar.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | 🟡 Serve | Três comandos |
| MVP / protótipo | ✅ Ótimo | Prepara a entrada do primeiro sócio ou freelancer |
| SaaS | ✅ Ótimo | Muitas dependências e variáveis |
| Sistema interno/corporativo | ✅ Ótimo | Alta rotatividade de equipe |
| Monorepo | ✅ Ótimo | Um README raiz e um por pacote |
| Repositório público | ✅ Ótimo | Contribuidores externos dependem dele |

## Quando é bom

- **Pré-requisitos com versão:** Docker, Node 24, `just`.
- **Comandos copiáveis**, em ordem, sem "então configure o banco".
- **Resultado esperado em cada passo:** "abra `http://localhost:3000`, você vê o login".
- **Usuários de teste** listados (doc 04).
- **Seção de problemas comuns** alimentada pelo time.
- **Atalhos em vez de comandos longos** (doc 05).

## Quando é ruim

- **README com passos que só quem fez o projeto entende.**
- **Versões desatualizadas** de Node, Postgres e portas.
- **Copiar o que já está no `compose.yaml`:** aponte para o arquivo.
- **Segredos reais no README:** só valores de desenvolvimento.
- **Textão:** comece pelo caminho feliz; detalhes vão para `docs/`.

## Como começar

Modelo de seção:

````markdown
## Como rodar

### Pré-requisitos

- Docker (Compose v2 ou mais novo)
- Node 24 (LTS) e npm
- just (opcional; sem ele, use os comandos do `package.json`)

### Passo a passo

```bash
git clone <url-do-repositorio>
cd meu-app
cp .env.example .env
npm ci
just up
just reset
just dev
```

Abra http://localhost:3000. Entre com `admin@exemplo.com` e `senha-local`.
E-mails enviados aparecem em http://localhost:8025.

### Comandos do dia a dia

| Comando | O que faz |
|---|---|
| `just dev` | Sobe as dependências e o app |
| `just test` | Roda os testes |
| `just reset` | Recria o banco e popula |
| `just clean` | Apaga contêineres e volumes |

### Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `port is already allocated` | Outro Postgres usa a 5432 | Pare o outro ou mude a porta no `compose.yaml` |
| `connection refused` ao conectar no banco | Contêiner ainda subindo | `docker compose ps` e espere ficar `healthy` |
| Banco com dados antigos ou erro de versão | Volume de outra versão | `just clean` e `just up` |
| `command not found: just` | Ferramenta não instalada | Instale conforme just.systems ou use `npm run` |
````

Teste o README: peça a alguém que nunca rodou o projeto (ou rode num contêiner limpo) e anote onde travou.

## Combina com / alternativas

- [05-scripts-de-uma-linha.md](05-scripts-de-uma-linha.md): os atalhos citados.
- [02-devcontainer.md](02-devcontainer.md): descreva o caminho com devcontainer, se existir.
- Skill `ia`, doc 01: o `CLAUDE.md` aponta para este README em vez de copiá-lo.
- Skill `architecture`: documentação de arquitetura é outro arquivo (`ARCHITECTURE.md`).
- Alternativas: script `./setup.sh` que faz tudo (útil, mas o README ainda precisa existir).

## Decisão rápida

- **Use se:** mais de uma pessoa vai rodar o projeto.
- **Evite se:** não evite; só mantenha curto e testado.
