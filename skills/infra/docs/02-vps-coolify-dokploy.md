# VPS com Coolify ou Dokploy

> Painéis open source que dão ao seu servidor o jeito de um PaaS: deploy pelo Git, HTTPS automático, banco e backups, com custo fixo baixo.

| | |
|---|---|
| **Site** | https://coolify.io e https://dokploy.com |
| **Categoria** | Hospedagem |
| **Tipo** | Painel de deploy autohospedado (self-hosted PaaS) |
| **Stack** | Docker, qualquer linguagem em contêiner, Docker Compose; Dokploy também usa Docker Swarm para vários servidores |
| **Preço** | Software gratuito para instalar; você paga o servidor (Hetzner cloud a partir de € 5,49/mês sem IVA). Dokploy oferece versão em nuvem com teste de 7 dias; o plano Hobby custa US$ 4,50/mês por servidor e o Startup a partir de US$ 15/mês (página de preços do Dokploy, conferido em 2026-11-24) |
| **Licença** | Coolify: Apache 2.0. Dokploy: Apache 2.0, exceto o conteúdo de uma pasta `/proprietary`, que tem licença própria (arquivos LICENSE no GitHub, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Você contrata um servidor (VPS), roda um script de instalação e ganha um painel para publicar aplicações, bancos e serviços. O painel cuida de Docker, proxy reverso, certificados e variáveis de ambiente.

**Coolify** exige no mínimo 2 núcleos, 2 GB de RAM e 10 GB de disco, em amd64 ou arm64. **Dokploy** lista deploy por Nixpacks, Railpack, buildpacks, Dockerfile e Compose, previews de pull request, rollback, backups agendados para armazenamento compatível com S3, métricas, variáveis criptografadas e integração com Vault e Infisical.

## Por que usar

- **Custo fixo e baixo:** um servidor pequeno roda vários apps sem cobrança por requisição.
- **Experiência de PaaS:** deploy pelo Git, previews e rollback.
- **Dados e servidor sob seu controle**, útil quando há exigência de onde os dados ficam.
- **Sem lock-in:** tudo é Docker, e dá para migrar para outro servidor.
- **Templates prontos** de serviços comuns (bancos, ferramentas internas).

## Quando usar

- SaaS pequeno com orçamento apertado e alguém que sabe administrar Linux.
- Vários projetos pequenos ou ferramentas internas no mesmo servidor.
- Time que quer sair de um PaaS por causa do custo, mas ainda não precisa de nuvem grande.
- Ambiente de homologação barato.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | 🟡 Serve | Funciona, mas Cloudflare Pages ou Vercel dão de graça e sem servidor |
| MVP / protótipo | 🟡 Serve | Barato, mas exige configurar o servidor; PaaS é mais rápido para começar |
| SaaS pequeno | ✅ Ótimo | Melhor custo-benefício se o dev opera servidor |
| SaaS em crescimento | 🟡 Serve | Dokploy com vários servidores ajuda; o banco deve sair para serviço gerenciado |
| Sistema corporativo | 🟡 Serve | Bom para ferramentas internas; produção crítica pede SLA e suporte |
| Ferramentas internas | ✅ Ótimo | Muitos serviços pequenos, custo fixo |
| Sem ninguém que opere Linux | ❌ Evite | Atualização, firewall e backup passam a ser sua responsabilidade |
| Produção que não pode cair | ❌ Evite | Servidor único é ponto único de falha |

## Quando é bom

- **Previsibilidade de custo:** a conta é o preço do servidor.
- **Controle total:** você escolhe região, tamanho e rede.
- **Comunidade grande** (coollabsio/coolify com cerca de 66,4 mil estrelas e Dokploy/dokploy com 38,7 mil no GitHub, 2026-11-24) e documentação própria para cada painel.
- **Backups para S3** (Dokploy) com agendamento pelo painel.

## Quando é ruim

- **A operação é sua:** atualizar o sistema, o painel e o Docker, e vigiar disco e memória.
- **Ponto único de falha:** um servidor só cai por inteiro; sem alta disponibilidade, prepare restauração rápida.
- **Banco no mesmo servidor é risco:** disputa recursos e depende do seu backup. Prefira [Postgres gerenciado](05-postgres-gerenciado.md).
- **Segurança é sua:** o painel exposto vira alvo. Restrinja acesso, ative 2FA e firewall (veja [segurança base](12-seguranca-base.md)).
- **Licença própria em parte do Dokploy:** o restante é Apache 2.0, mas leia o repositório antes de usar em produto comercial.
- **Sem SLA:** suporte é comunidade (no Dokploy Cloud, o Hobby tem suporte da comunidade no Discord; e-mail e chat só a partir do Startup).

## Como começar

Coolify, em servidor Linux limpo (comando da documentação oficial):

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

Dokploy (comando da página oficial):

```bash
curl -sSL https://dokploy.com/install.sh | sh
```

Depois: crie o usuário admin, aponte o domínio para o IP, ative o firewall liberando só 22, 80 e 443 (e a porta do painel só para seu IP), conecte o repositório e configure backup do banco.

## Combina com / alternativas

- [Cloudflare](08-cloudflare.md): esconde o IP do servidor e filtra tráfego.
- [Postgres gerenciado](05-postgres-gerenciado.md): tira o dado do servidor único.
- [Backup e recuperação](11-backup-e-recuperacao.md): obrigatório aqui.
- Alternativas: [PaaS](01-paas.md) se ninguém quer operar servidor; [nuvem grande](03-nuvem-grande.md) se há exigência de alta disponibilidade.

## Decisão rápida

- **Use se:** há alguém que opera Linux, o orçamento é curto e o projeto aceita um servidor como base.
- **Evite se:** ninguém sabe administrar servidor, a produção não pode ter ponto único de falha, ou a licença do painel não foi lida e aprovada.
