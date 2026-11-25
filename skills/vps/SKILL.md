---
name: vps
description: Ajuda a escolher uma VPS no Brasil e a deixar o servidor pronto, seguro e operável — as 5 opções brasileiras comparadas com preço conferido (Hostinger, HostGator, Locaweb, KingHost e HostDime, esta para servidores grandes e dedicados), dimensionamento, primeiro acesso seguro (SSH com chave, sem root, firewall, fail2ban), atualizações automáticas, Docker e swap, backup com restauração testada, monitoramento e alertas, deploy (Coolify, Dokploy ou Compose com GitHub Actions) e migração para outra VPS ou para a nuvem. Use sempre que o usuário perguntar "qual VPS contratar", "VPS no Brasil", "servidor barato", "preparar o servidor", "proteger o SSH", "Ubuntu server", "instalar Docker no servidor", "backup do servidor", "o servidor caiu" ou "migrar de servidor". Não configura o nginx (skill nginx), a Cloudflare (skill cloudflare), o domínio (skill domains) nem o Coolify e o Dokploy em si (skill infra, doc 02).
---

# vps

Guia para quem vai rodar o sistema num servidor próprio no Brasil: qual contratar e como deixá-lo pronto sem virar alvo. VPS é mais barata e dá mais controle que um PaaS, mas tudo o que o PaaS fazia (atualizar, proteger, fazer backup, monitorar) passa a ser seu. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e comandos prontos.

## Como usar esta skill

1. **Confirme que VPS é a escolha certa.** Se ninguém no time vai operar servidor, um PaaS (skill `infra`, doc 01) costuma sair mais barato no fim.
2. **Escolha o fornecedor** pelo perfil do projeto ([doc 01](docs/01-as-5-melhores-vps-do-brasil.md)). Confira o preço na página oficial antes de afirmar: as ofertas mudam e quase sempre exigem contrato longo.
3. **Dimensione** pelo que vai rodar ([doc 02](docs/02-dimensionar-o-servidor.md)): Coolify e Dokploy pedem pelo menos 2 GB de RAM.
4. **Faça o primeiro acesso seguro** antes de instalar qualquer coisa ([doc 03](docs/03-primeiro-acesso-seguro-ssh-e-firewall.md)).
5. **Instale atualizações automáticas, Docker e swap** ([doc 04](docs/04-atualizacoes-docker-e-swap.md)).
6. **Ponha o proxy e o HTTPS:** proxy do Coolify ou Dokploy, ou nginx (skill `nginx`); na frente, a Cloudflare (skill `cloudflare`).
7. **Configure backup e teste a restauração** ([doc 05](docs/05-backup-e-restauracao-na-vps.md)) e o **monitoramento** ([doc 06](docs/06-monitoramento-e-alertas.md)).
8. **Monte o deploy** ([doc 07](docs/07-deploy-na-vps.md)) e documente no `README` como acessar e como restaurar.
9. **Quando o projeto crescer**, use o [doc 08](docs/08-migrar-ou-sair-da-vps.md) para trocar de VPS ou ir para a nuvem.

## Qual VPS por perfil

| Perfil | Opção | Por quê |
|---|---|---|
| MVP com o menor custo mensal | Hostinger ou HostGator | Planos de entrada mais baratos, com contrato longo |
| SaaS pequeno com Coolify ou Dokploy | Hostinger (plano com 4 GB ou mais) ou KingHost | RAM suficiente para painel, app e banco |
| Agência com vários sites de clientes | KingHost ou Locaweb | Provedores nacionais com suporte em português |
| Cliente que exige nota fiscal e suporte nacional | Locaweb ou KingHost | Confirme a emissão de nota com o comercial: as páginas não informam |
| Servidor grande ou dedicado | HostDime | Datacenter próprio no Brasil e linha de dedicados |
| Já usa AWS ou precisa de serviços gerenciados | Nuvem grande em São Paulo (skill `infra`, doc 03) | Sai das brasileiras quando o serviço gerenciado vale mais que o preço |

Preços, recursos e datacenters de cada uma estão no [doc 01](docs/01-as-5-melhores-vps-do-brasil.md), conferidos em 2026-11-25.

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| As 5 VPS do Brasil | [docs/01-as-5-melhores-vps-do-brasil.md](docs/01-as-5-melhores-vps-do-brasil.md) | Comparação com preço conferido e recomendação por perfil |
| Dimensionar | [docs/02-dimensionar-o-servidor.md](docs/02-dimensionar-o-servidor.md) | CPU, RAM, disco e quando separar o banco |
| Primeiro acesso seguro | [docs/03-primeiro-acesso-seguro-ssh-e-firewall.md](docs/03-primeiro-acesso-seguro-ssh-e-firewall.md) | SSH com chave, sem root, ufw, fail2ban, cloud-init |
| Atualizações e Docker | [docs/04-atualizacoes-docker-e-swap.md](docs/04-atualizacoes-docker-e-swap.md) | unattended-upgrades, Docker oficial, logs, swap |
| Backup | [docs/05-backup-e-restauracao-na-vps.md](docs/05-backup-e-restauracao-na-vps.md) | Snapshot, pg_dump, cópia externa, restauração |
| Monitoramento | [docs/06-monitoramento-e-alertas.md](docs/06-monitoramento-e-alertas.md) | Uptime externo, disco, CPU, alertas |
| Deploy | [docs/07-deploy-na-vps.md](docs/07-deploy-na-vps.md) | Coolify, Dokploy ou Compose com GitHub Actions |
| Migrar ou sair | [docs/08-migrar-ou-sair-da-vps.md](docs/08-migrar-ou-sair-da-vps.md) | Trocar de VPS sem queda ou ir para a nuvem |

## Checklist

- [ ] Login como root desligado e só chave SSH aceita (`sshd -T | grep -E "permitrootlogin|passwordauthentication"`).
- [ ] Firewall ativo liberando só 22, 80 e 443 (`ufw status`); painel do Coolify ou Dokploy fora da internet aberta (Access ou Tunnel).
- [ ] Portas de contêiner que não são públicas presas em `127.0.0.1` (Docker ignora o ufw nas portas publicadas).
- [ ] Atualizações de segurança automáticas ligadas (`systemctl status unattended-upgrades`).
- [ ] 2FA na conta do provedor.
- [ ] Rotação de logs do Docker configurada (`/etc/docker/daemon.json`).
- [ ] Backup diário do banco com cópia fora do servidor e uma restauração testada (data anotada no `README`).
- [ ] Monitor externo de disponibilidade e alerta de disco acima de 80%.
- [ ] Deploy reproduzível (painel ou Compose no Git), sem passo manual no servidor.
- [ ] Acesso, backup e restauração documentados para outra pessoa conseguir operar.

## Regras de uso

- **Preço só conferido.** As páginas das hospedagens mostram preço promocional de contrato longo; diga o prazo e o valor de renovação ao usuário.
- **Segurança antes de tudo.** Nada é instalado antes de SSH com chave, sem root e com firewall.
- **Backup que nunca foi restaurado não existe.** Teste a restauração antes do primeiro cliente.
- **Um servidor é um ponto único de falha.** Diga isso ao usuário; para disponibilidade alta, a resposta é outra arquitetura, não uma VPS maior.
- **Nada manual no servidor.** Toda mudança vai por painel, Compose ou script versionado; o que só existe no servidor se perde.
- **Separe o banco quando ele crescer** ou quando o app precisar de mais de uma instância.
- **Fronteiras.** Proxy e HTTPS no servidor são da `nginx`; borda e DNS da `cloudflare` e da `domains`; Coolify, Dokploy, IaC e observabilidade geral da `infra`.

## Quando a lista não cobre

Servidor dedicado físico, colocation, Kubernetes em VPS, alta disponibilidade com vários servidores, VPS Windows e licenças (cPanel, Plesk) ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial.

## Validade dos dados

Preços, planos e datacenters das 5 VPS foram conferidos em 2026-11-25 nas páginas oficiais e mudam com frequência, principalmente as promoções. Versões de Ubuntu, Debian e Docker também foram conferidas na data; cada documento tem a linha "Verificado em".
