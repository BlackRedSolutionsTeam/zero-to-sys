# vps

Skill para o Claude Code que ajuda a escolher uma VPS no Brasil e a deixar o servidor pronto e seguro: as 5 opções brasileiras comparadas (Hostinger, HostGator, Locaweb, KingHost e HostDime), dimensionamento, SSH e firewall, atualizações, Docker, backup, monitoramento, deploy e migração. Ela reúne um guia ([SKILL.md](SKILL.md)) e um documento por tópico ([docs/](docs/)).

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| As 5 VPS do Brasil | Hostinger, HostGator, Locaweb, KingHost, HostDime | [docs/01-as-5-melhores-vps-do-brasil.md](docs/01-as-5-melhores-vps-do-brasil.md) |
| Dimensionar | CPU, RAM, disco, swap | [docs/02-dimensionar-o-servidor.md](docs/02-dimensionar-o-servidor.md) |
| Primeiro acesso seguro | SSH, firewall, fail2ban | [docs/03-primeiro-acesso-seguro-ssh-e-firewall.md](docs/03-primeiro-acesso-seguro-ssh-e-firewall.md) |
| Atualizações e Docker | unattended-upgrades, Docker, swap | [docs/04-atualizacoes-docker-e-swap.md](docs/04-atualizacoes-docker-e-swap.md) |
| Backup | Snapshot, pg_dump, cópia externa, restauração | [docs/05-backup-e-restauracao-na-vps.md](docs/05-backup-e-restauracao-na-vps.md) |
| Monitoramento | Uptime, disco, alertas | [docs/06-monitoramento-e-alertas.md](docs/06-monitoramento-e-alertas.md) |
| Deploy | Coolify/Dokploy ou Compose + Actions | [docs/07-deploy-na-vps.md](docs/07-deploy-na-vps.md) |
| Migrar ou sair | Trocar de VPS ou ir para a nuvem | [docs/08-migrar-ou-sair-da-vps.md](docs/08-migrar-ou-sair-da-vps.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/vps ~/.claude/skills/vps
```

## Como usar

O Claude carrega a skill sozinho quando o pedido bate com o tema dela. Também dá para chamar direto com `/vps`. Exemplos:

- "Qual VPS eu contrato no Brasil para esse SaaS?"
- "Prepara esse Ubuntu novo: SSH, firewall e Docker."
- "/vps o servidor caiu, como eu monitoro isso?"

Com a skill carregada, o Claude:

1. escolhe a VPS pelo perfil do projeto, com preço conferido;
2. dimensiona o servidor;
3. faz o primeiro acesso seguro e liga o firewall;
4. instala Docker, atualizações automáticas, backup e monitoramento;
5. monta o deploy e confere o checklist.

## Estrutura

```
vps/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md     índice e "Por onde começar"
    ├── 01-as-5-melhores-vps-do-brasil.md
    ├── 02-dimensionar-o-servidor.md
    ├── 03-primeiro-acesso-seguro-ssh-e-firewall.md
    ├── 04-atualizacoes-docker-e-swap.md
    ├── 05-backup-e-restauracao-na-vps.md
    ├── 06-monitoramento-e-alertas.md
    ├── 07-deploy-na-vps.md
    └── 08-migrar-ou-sair-da-vps.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** Preços, planos e datacenters das VPS foram conferidos em 2026-11-25 nas páginas oficiais; mudam com frequência. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
