# Deploy na VPS

> Escolha entre painel (Coolify ou Dokploy) e Docker Compose com GitHub Actions por SSH, e deixe o rollback a um comando.

| | |
|---|---|
| **Referência** | https://docs.docker.com/engine/containers/start-containers-automatically/, https://docs.docker.com/reference/cli/docker/compose/up/, https://docs.github.com/en/actions, https://coolify.io/docs |
| **Categoria** | Servidor |
| **Tipo** | Prática de deploy em servidor próprio |
| **Vale para** | VPS Ubuntu LTS com Docker, app em contêiner |
| **Verificado em** | 2026-11-25 |

## O que é

Deploy é colocar a nova versão no ar. Na VPS há dois caminhos:

- **Painel (Coolify ou Dokploy):** você conecta o repositório e o painel constrói, publica, cuida de HTTPS e faz rollback. Veja [VPS com Coolify ou Dokploy](../../infra/docs/02-vps-coolify-dokploy.md).
- **Docker Compose + GitHub Actions:** o GitHub constrói a imagem, envia para um registro (como o GHCR) e conecta por **SSH** no servidor para rodar `docker compose up`. Sem painel, menos peças, mais trabalho manual.

Duas bases valem nos dois caminhos: `restart: unless-stopped` (o contêiner volta após queda ou reinício do servidor, exceto se você o parou de propósito, conferido em 2026-11-25) e imagem com **tag fixa** (versão ou hash do commit) para poder voltar.

## Por que usar

- Deploy repetível, sem copiar arquivo à mão.
- Reinício automático quando o servidor reinicia.
- Rollback rápido, trocando só a tag.
- Chave SSH dedicada limita o estrago se o segredo vazar.

## Quando usar

- Toda VPS com app em produção.
- Painel: vários apps, quer previews e interface. Compose: um ou dois serviços e quer controle total.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Compose simples ou hospedagem estática, mais barata |
| MVP de SaaS | ✅ Ótimo | Painel acelera; Compose basta para um app |
| SaaS em crescimento | ✅ Ótimo | Compose com CI e tags, ou Dokploy com vários servidores |
| Sistema interno/corporativo | ✅ Ótimo | Pipeline com aprovação por ambiente |
| API/integração | ✅ Ótimo | Deploy sem queda e rollback por tag |
| App mobile com backend | ✅ Ótimo | A API deve ter rollback rápido; o app antigo segue usando |
| Deploy copiando arquivos por FTP ou na mão | ❌ Evite | Sem histórico, sem rollback e sujeito a erro |

## Quando é bom

- **Painel:** interface, variáveis, backup de banco e rollback prontos.
- **Compose + Actions:** poucas peças, tudo versionado no Git.
- **`--wait` do `docker compose up`:** espera os serviços ficarem saudáveis antes de encerrar (conferido em 2026-11-25).
- **`concurrency` no GitHub Actions:** garante um único deploy por vez no mesmo ambiente (conferido em 2026-11-25).

## Quando é ruim

- **Deploy sem queda real** exige mais de uma réplica ou balanceador; no Compose simples haverá poucos segundos de troca. Se isso for inaceitável, veja [nuvem grande](../../infra/docs/03-nuvem-grande.md).
- **Migração de banco incompatível** quebra o rollback: separe mudança de coluna em duas etapas.
- **Chave SSH com acesso total** vazada vira acesso root; use usuário sem privilégios e chave só para deploy.
- **Painel exposto** é alvo; restrinja o acesso.
- **Tag `latest`:** impede saber o que está rodando e voltar.

## Como começar

Chave dedicada ao deploy, gerada na sua máquina:

```bash
ssh-keygen -t ed25519 -f deploy_clinica -C "deploy-github" -N ""
```

Instale `deploy_clinica.pub` em `~/.ssh/authorized_keys` do usuário `deploy` no servidor (sem root, no grupo `docker`). A chave privada vai para o segredo `SSH_KEY` do ambiente `production` no GitHub, junto de `SSH_HOST` e `SSH_KNOWN_HOSTS` (saída de `ssh-keyscan` conferida por você).

`docker-compose.yml` no servidor:

```yaml
services:
  api:
    image: ghcr.io/clinica-exemplo/api:${TAG}
    restart: unless-stopped
    env_file: .env
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/saude"]
      interval: 10s
      retries: 5
    ports:
      - "127.0.0.1:3000:3000"
```

`.github/workflows/deploy.yml`:

```yaml
name: deploy
on:
  push:
    branches: [main]
concurrency:
  group: deploy-production
  cancel-in-progress: false
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - run: |
          docker build -t ghcr.io/clinica-exemplo/api:${{ github.sha }} .
          docker push ghcr.io/clinica-exemplo/api:${{ github.sha }}
      - run: |
          install -m 600 /dev/null key
          echo "${{ secrets.SSH_KEY }}" > key
          echo "${{ secrets.SSH_KNOWN_HOSTS }}" > known_hosts
          ssh -i key -o UserKnownHostsFile=known_hosts deploy@${{ secrets.SSH_HOST }} "cd /srv/clinica && TAG=${{ github.sha }} docker compose pull api && TAG=${{ github.sha }} docker compose up -d --wait --no-deps api && echo ${{ github.sha }} > .tag-atual"
```

Confira as versões das actions na página oficial antes de usar. O `--wait` falha se o healthcheck não passar, e o contêiner antigo só sai depois de o novo subir; ainda assim, há uma pequena troca.

**Rollback por tag:** guarde o SHA anterior (por exemplo em `.tag-anterior`) e rode:

```bash
cd /srv/clinica && TAG=$(cat .tag-anterior) docker compose up -d --wait --no-deps api
```

Mantenha as últimas 5 a 10 imagens no registro e limpe o resto.

## Combina com / alternativas

- [GitHub Actions](../../infra/docs/07-github-actions.md) e [feature flags e rollback](../../infra/docs/14-feature-flags-e-rollback.md).
- [Segredos e configuração](../../infra/docs/09-segredos-e-configuracao.md) para o `.env` e as chaves.
- [Monitoramento](06-monitoramento-e-alertas.md): alerte se o deploy deixar o healthcheck falhando.
- Alternativas: Watchtower e `docker rollout` (confira projeto e manutenção antes), ou PaaS.

## Decisão rápida

- **Use se:** quer deploy repetível em servidor próprio. Painel para vários apps; Compose com Actions para um app.
- **Evite se:** precisa de zero queda garantida com carga alta ou não tem quem cuide do servidor.
