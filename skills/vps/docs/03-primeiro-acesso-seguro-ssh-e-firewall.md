# Primeiro acesso seguro: SSH e firewall

> Antes de instalar qualquer coisa, crie um usuário sem root, entre só com chave SSH, desligue senha e login root e deixe só 22, 80 e 443 abertas.

| | |
|---|---|
| **Referência** | https://ubuntu.com/server/docs/how-to/security/openssh-server/ e https://docs.docker.com/engine/network/packet-filtering-firewalls/ |
| **Categoria** | Servidor |
| **Tipo** | Prática de segurança do servidor |
| **Vale para** | Ubuntu LTS e Debian em VPS, com ou sem Coolify e Dokploy |
| **Verificado em** | 2026-11-25 |

## O que é

Um servidor novo chega com acesso por **root** (usuário com poder total) e, em muitos provedores, com senha. Robôs na internet tentam entrar em servidores novos em minutos. Este doc fecha essa porta.

Termos usados:

- **SSH:** protocolo para controlar o servidor pelo terminal.
- **Chave Ed25519:** par de arquivos (privado no seu computador, público no servidor) que prova quem você é, no lugar da senha.
- **fail2ban:** programa que bloqueia por um tempo os IPs que erram o login várias vezes.
- **ufw:** firewall simples do Ubuntu, que decide quais portas ficam abertas.
- **cloud-init:** script que o provedor roda na primeira inicialização.

## Por que usar

- **Senha SSH é o alvo número um** de ataque automático; chave elimina esse risco.
- **Sem root direto**, um erro de comando não apaga o sistema inteiro e o log mostra quem fez o quê.
- **Firewall** reduz o que o mundo enxerga.
- **Fica pronto antes** de qualquer app ou banco entrar no servidor.

## Quando usar

- No primeiro acesso a qualquer VPS, antes de instalar o Docker.
- Ao herdar um servidor que ainda entra por senha.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Servidor exposto na internet precisa do básico |
| MVP de SaaS | ✅ Ótimo | Leva 10 minutos e evita o pior |
| SaaS em crescimento | ✅ Ótimo | Some rede privada e firewall do provedor |
| Sistema interno/corporativo | ✅ Ótimo | Pode limitar o SSH por VPN ou por IP fixo |
| API/integração | ✅ Ótimo | Credenciais e dados passam por ali |
| App mobile com backend | ✅ Ótimo | Dados de usuário no servidor |
| Servidor com senha de root na internet | ❌ Evite | Questão de tempo até ser invadido |

## Quando é bom

- **Chave Ed25519** é curta, rápida e segura para uso comum.
- **Arquivo em `sshd_config.d`:** na documentação da Ubuntu, o `sshd_config` padrão inclui `/etc/ssh/sshd_config.d/*.conf`, e o OpenSSH usa o primeiro valor que lê, então o seu arquivo prevalece sem mexer no original (conferido em 2026-11-25). Dê a ele um nome que venha antes dos outros, como `00-endurecer.conf`.
- **Validar antes de aplicar:** `sudo sshd -t` acusa erro antes de você se trancar para fora.

## Quando é ruim

- **Fechar a senha antes de testar a chave** tranca você para fora. Abra uma segunda sessão e só então desligue.
- **Docker ignora o ufw:** portas publicadas por contêineres passam por fora das regras do ufw (conferido na documentação do Docker em 2026-11-25). Publique só o que precisa, com `-p 127.0.0.1:porta:porta` para o que deve ficar local, e deixe o proxy (Traefik do painel) receber 80 e 443.
- **Painel na porta aberta:** o Dokploy usa a 3000 até você ligar domínio e HTTPS; restrinja-a ao seu IP ou feche depois.
- **Mudar a porta SSH não substitui chave:** pode tirar ruído de log, mas não é defesa.

## Como começar

Na sua máquina, gere a chave e envie a pública:

```bash
ssh-keygen -t ed25519 -C "vagner@clinica-exemplo"
ssh-copy-id root@IP_DO_SERVIDOR
```

No servidor, crie o usuário e dê acesso a administrar com `sudo`:

```bash
adduser deploy
usermod -aG sudo deploy
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

Em outro terminal, teste `ssh deploy@IP_DO_SERVIDOR` e `sudo whoami`. Só então crie o arquivo de endurecimento:

```bash
sudo tee /etc/ssh/sshd_config.d/00-endurecer.conf <<'EOF'
PasswordAuthentication no
PermitRootLogin no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
EOF
sudo sshd -t
sudo systemctl restart ssh
```

O serviço se chama `ssh` no Ubuntu (conferido na documentação). Confira o valor efetivo:

```bash
sudo sshd -T | grep -E 'passwordauthentication|permitrootlogin'
```

Firewall e fail2ban:

```bash
sudo apt update && sudo apt install -y ufw fail2ban
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
```

Script **cloud-init** pronto para colar no campo "user data" do provedor (troque a chave pela sua pública). Ele cria o usuário `deploy`, endurece o SSH e liga o firewall:

```yaml
#cloud-config
package_update: true
package_upgrade: true
packages:
  - ufw
  - fail2ban
  - unattended-upgrades
users:
  - name: deploy
    groups: sudo
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: true
    ssh_authorized_keys:
      - ssh-ed25519 AAAA...SUA_CHAVE_PUBLICA vagner@clinica-exemplo
write_files:
  - path: /etc/ssh/sshd_config.d/00-endurecer.conf
    content: |
      PasswordAuthentication no
      PermitRootLogin no
      KbdInteractiveAuthentication no
      PubkeyAuthentication yes
runcmd:
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow 22/tcp
  - ufw allow 80/tcp
  - ufw allow 443/tcp
  - ufw --force enable
  - systemctl enable --now fail2ban
  - systemctl restart ssh
```

Observações: o `NOPASSWD` evita pedir senha a um usuário sem senha; troque se preferir definir uma senha para o `sudo`. Cloud-init não foi executado em servidor real nesta escrita: teste em um servidor descartável. Habilite também **2FA na conta do provedor**, porque quem entra no painel dele pode reiniciar ou apagar o servidor, e use o firewall de nuvem do provedor (quando existir) como segunda camada.

## Combina com / alternativas

- [Dimensionar o servidor](02-dimensionar-o-servidor.md): passo anterior.
- [Atualizações, Docker e swap](04-atualizacoes-docker-e-swap.md): passo seguinte.
- [Segurança base](../../infra/docs/12-seguranca-base.md) e [VPS com Coolify ou Dokploy](../../infra/docs/02-vps-coolify-dokploy.md).
- [Cloudflare](../../infra/docs/08-cloudflare.md): esconde o IP de origem e filtra tráfego.
- Alternativas: `sshguard` no lugar do fail2ban; Tailscale ou VPN para fechar a 22 ao mundo.

## Decisão rápida

- **Use se:** o servidor é novo ou ainda entra por senha ou como root.
- **Evite se:** você ainda não testou a chave em uma segunda sessão; teste antes de desligar a senha.
