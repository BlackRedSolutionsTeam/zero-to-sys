# Atualizações, Docker e swap

> Deixe o servidor se atualizar sozinho, instale o Docker pelo repositório oficial, limite o tamanho dos logs e tenha swap como rede de segurança.

| | |
|---|---|
| **Referência** | https://docs.docker.com/engine/install/ubuntu/ e https://ubuntu.com/server/docs/how-to/software/automatic-updates/ |
| **Categoria** | Servidor |
| **Tipo** | Prática de manutenção do servidor |
| **Vale para** | Ubuntu LTS e Debian em VPS com Docker, Compose, Coolify ou Dokploy |
| **Verificado em** | 2026-11-25 |

## O que é

Três tarefas que mantêm o servidor saudável sem trabalho diário:

- **Atualizações automáticas de segurança** (`unattended-upgrades`).
- **Docker instalado pelo repositório apt oficial**, com o plugin Compose, para receber atualizações pelo `apt`.
- **Swap**, um arquivo em disco que o Linux usa quando a RAM acaba. É lento: serve para evitar que o sistema mate processos num pico, não para rodar o dia a dia.

Versões conferidas em 2026-11-25:

| Sistema | Versão | Observação |
|---|---|---|
| Ubuntu LTS mais nova | 26.04 "Resolute Raccoon" (26.04.1 em 27/08/2026) | Suporte padrão até maio de 2031 |
| Ubuntu LTS anterior | 24.04 "Noble Numbat" | Suporte padrão até junho de 2029 |
| Ubuntu LTS antiga | 22.04 "Jammy Jellyfish" | Suporte padrão até junho de 2027 |
| Debian estável | 13 "trixie" | O 12 "bookworm" é a oldstable |

O Docker lista suporte a Ubuntu 26.04, 24.04 e 22.04, e a Debian 13 e 12. Versões não LTS (como o Ubuntu 26.10) duram pouco: evite em produção.

## Por que usar

- **Correções de segurança chegam sem você lembrar.**
- **Docker pelo apt** atualiza junto com o sistema e evita scripts de origem desconhecida.
- **Logs com rotação** impedem que um contêiner encha o disco. Sem `max-size`, o Docker não limita o log (conferido na documentação).
- **Swap** dá fôlego em picos de memória.

## Quando usar

- Logo depois do [primeiro acesso seguro](03-primeiro-acesso-seguro-ssh-e-firewall.md).
- Antes de instalar o Coolify ou o Dokploy, se quiser controlar a versão do Docker.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Menos manutenção manual |
| MVP de SaaS | ✅ Ótimo | Ninguém tem tempo de atualizar servidor |
| SaaS em crescimento | ✅ Ótimo | Combine com janela de reinício combinada |
| Sistema interno/corporativo | ✅ Ótimo | Defina horário de reinício fora do expediente |
| API/integração | 🟡 Serve | Reinício automático pode cortar chamadas; escolha a hora |
| App mobile com backend | 🟡 Serve | Mesmo cuidado com o horário de reinício |
| Servidor que nunca pode reiniciar | ❌ Evite | Kernel novo exige reinício; sem alta disponibilidade, isso é queda |

## Quando é bom

- **Só segurança por padrão:** o `unattended-upgrades` já vem instalado no Ubuntu e atualiza pacotes de segurança.
- **Reinício na hora que você escolher**, com `Automatic-Reboot-Time`.

## Quando é ruim

- **Reinício automático sem aviso** derruba o app por alguns segundos; use `restart: unless-stopped` nos serviços para voltarem sozinhos.
- **Atualizar o Docker pode reiniciar contêineres** em alguns casos; faça fora do horário de pico.
- **Config de log vale só para contêineres novos**; recrie os existentes.
- **`docker system prune -a` apaga imagens sem uso** e pode apagar a que você quer reverter; use com cuidado.

## Como começar

Atualizações automáticas, com reinício às 04:00:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

Ajuste o reinício em `/etc/apt/apt.conf.d/50unattended-upgrades`:

```text
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:00";
```

Os dois arquivos que mandam são `50unattended-upgrades` (comportamento) e `20auto-upgrades` (frequência). Teste sem aplicar:

```bash
sudo unattended-upgrade -v --dry-run
```

Docker no Ubuntu, pelo repositório apt (comandos da documentação oficial; no Debian troque `ubuntu` por `debian` na URL e a documentação usa o mesmo formato):

```bash
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
```

Se for usar o `deploy`, dê acesso ao Docker e saiba que isso equivale a poder de root:

```bash
sudo usermod -aG docker deploy
```

Rotação de logs em `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Cada contêiner guarda até 3 arquivos de 10 MB. Aplique e recrie os contêineres:

```bash
sudo systemctl restart docker
docker compose up -d --force-recreate
```

Limpeza de imagens e cache que não são usados:

```bash
docker image prune -f
docker builder prune -f
```

Criar uma swap de 2 GB (ajuste o tamanho; não é necessária se o provedor já fornece):

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swap.conf
sudo sysctl --system
free -h
```

Os comandos de swap são os padrões do Linux e não foram conferidos em página oficial nesta escrita; confirme em `man swapon` e `man mkswap`.

## Combina com / alternativas

- [Dimensionar o servidor](02-dimensionar-o-servidor.md): decide se swap resolve ou se falta RAM.
- [Primeiro acesso seguro](03-primeiro-acesso-seguro-ssh-e-firewall.md): o passo anterior.
- [VPS com Coolify ou Dokploy](../../infra/docs/02-vps-coolify-dokploy.md): ambos instalam Docker sozinhos; instalar antes dá controle da versão.
- [Backup e recuperação](../../infra/docs/11-backup-e-recuperacao.md): tire um snapshot antes de atualizar o sistema ou o Docker.

## Decisão rápida

- **Use se:** o servidor é seu e ninguém lembra de atualizar; escolha o horário do reinício.
- **Evite se:** o app não suporta reinício e não há outro servidor para assumir; planeje antes uma janela de manutenção.
