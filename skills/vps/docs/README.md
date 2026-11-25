# VPS

Um documento por tópico, da escolha do fornecedor até a migração. Preços e datacenters foram conferidos em 2026-11-25 nas páginas oficiais.

## Escolher

| Prática | O que entrega | Doc |
|---|---|---|
| As 5 VPS do Brasil | Hostinger, HostGator, Locaweb, KingHost, HostDime | [01-as-5-melhores-vps-do-brasil.md](01-as-5-melhores-vps-do-brasil.md) |
| Dimensionar | CPU, RAM, disco, swap | [02-dimensionar-o-servidor.md](02-dimensionar-o-servidor.md) |

## Preparar

| Prática | O que entrega | Doc |
|---|---|---|
| Primeiro acesso seguro | SSH, firewall, fail2ban | [03-primeiro-acesso-seguro-ssh-e-firewall.md](03-primeiro-acesso-seguro-ssh-e-firewall.md) |
| Atualizações e Docker | unattended-upgrades, Docker, swap | [04-atualizacoes-docker-e-swap.md](04-atualizacoes-docker-e-swap.md) |

## Operar

| Prática | O que entrega | Doc |
|---|---|---|
| Backup | Snapshot, pg_dump, cópia externa, restauração | [05-backup-e-restauracao-na-vps.md](05-backup-e-restauracao-na-vps.md) |
| Monitoramento | Uptime, disco, alertas | [06-monitoramento-e-alertas.md](06-monitoramento-e-alertas.md) |
| Deploy | Coolify/Dokploy ou Compose + Actions | [07-deploy-na-vps.md](07-deploy-na-vps.md) |

## Mudar

| Prática | O que entrega | Doc |
|---|---|---|
| Migrar ou sair | Trocar de VPS ou ir para a nuvem | [08-migrar-ou-sair-da-vps.md](08-migrar-ou-sair-da-vps.md) |

## Por onde começar

- **Vai contratar:** 01 e 02.
- **Servidor novo:** 03 → 04 → 05 → 06 → 07.
- **O servidor caiu ou encheu o disco:** 06.
- **Vai trocar de VPS ou ir para a nuvem:** 08.
