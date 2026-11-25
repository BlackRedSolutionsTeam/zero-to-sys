# Instalação e estrutura do nginx

> Instale do repositório oficial para ter versão atual, separe um arquivo por site e rode `nginx -t` antes de todo `reload`.

| | |
|---|---|
| **Referência** | nginx.org/en/linux_packages.html, nginx.org/en/download.html, nginx.org/en/docs/beginners_guide.html |
| **Categoria** | Servidor |
| **Tipo** | Prática de instalação e organização |
| **Vale para** | VPS Debian ou Ubuntu; a lógica vale para outras distros |
| **Verificado em** | 2026-11-25 |

## O que é

O nginx lê um arquivo principal, o `nginx.conf` (por padrão em `/etc/nginx`, segundo o guia oficial), que inclui os arquivos de cada site. Há duas fontes de pacote: o **repositório do nginx.org** (versões novas, canais stable e mainline) e o **repositório da distro** (versão mais antiga, mantida pela distro).

Conferido em 2026-11-25 (nginx.org/en/download.html):

| Canal | Versão |
|---|---|
| Mainline | 1.31.10 |
| Stable | 1.30.8 |
| Legacy mais novo | 1.28.3 |

**Mainline** recebe os recursos novos primeiro. **Stable** é a linha que só recebe correções. A página oficial de instalação indica o stable como padrão.

## Por que usar

- **Versão atual** e correções de segurança sem esperar a distro.
- **Pacote assinado:** o apt confere a chave do nginx.org.
- **Estrutura previsível:** um arquivo por site facilita revisar e desfazer.

## Quando usar

- Servidor novo, sem painel.
- Quando precisa de um recurso de versão recente.
- Quando a versão da distro está velha demais.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Stable do nginx.org mantém o servidor leve e atual |
| MVP de SaaS | ✅ Ótimo | Instalação em minutos, um arquivo por domínio |
| SaaS em crescimento | ✅ Ótimo | Versão controlada e atualização pelo apt |
| Sistema interno/corporativo | 🟡 Serve | A política interna pode exigir o pacote da distro |
| API/integração | ✅ Ótimo | Um arquivo para `api.clinica-exemplo.com.br` |
| App mobile com backend | ✅ Ótimo | Mesmo caso da API |
| Servidor com Coolify ou Dokploy | ❌ Evite | O painel já ocupa as portas 80 e 443 |

## Quando é bom

- **nginx.org:** versão nova e canal à sua escolha.
- **Distro:** vem com o sistema; a distro aplica as correções de segurança na versão antiga (confira o changelog do pacote, não só o número).
- **Um arquivo por site:** `nginx -t` aponta o erro e o rollback é apagar um link.

## Quando é ruim

- **Pacote da distro:** versão atrasada e sem recursos recentes.
- **Misturar as duas fontes** sem o pinning: o apt pode trocar de origem sem aviso.
- **Editar o `nginx.conf` para tudo:** vira um arquivo enorme e frágil.

## Como começar

Pré-requisitos e chave de assinatura (Ubuntu; no Debian troque `ubuntu-keyring` por `debian-archive-keyring`):

```bash
sudo apt install curl gnupg2 ca-certificates lsb-release ubuntu-keyring
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg
```

A saída deve mostrar a fingerprint `573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62`. Se for diferente, pare.

Repositório stable, pinning e instalação:

```bash
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] https://nginx.org/packages/ubuntu $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" | sudo tee /etc/apt/preferences.d/99nginx
sudo apt update
sudo apt install nginx
nginx -v
```

Para o mainline, use `https://nginx.org/packages/mainline/ubuntu` na linha do repositório. No Debian, troque `ubuntu` por `debian`. O pinning de prioridade 900 faz o apt preferir o nginx.org à distro (que usa 500).

Organização por site. Nos pacotes do nginx.org, o `nginx.conf` inclui os arquivos de `conf.d/*.conf`. Nos pacotes de Debian e Ubuntu da distro, a convenção é `sites-available` e `sites-enabled`. Abra o seu `nginx.conf` e veja qual `include` existe antes de decidir.

```bash
sudo nano /etc/nginx/conf.d/api.clinica-exemplo.com.br.conf
sudo nginx -t
sudo nginx -s reload
```

Com `sites-available`, o arquivo fica em `sites-available` e você ativa com um link em `sites-enabled`:

```bash
sudo ln -s /etc/nginx/sites-available/api.clinica-exemplo.com.br /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Sobre o reload (guia oficial, conferido em 2026-11-25): o processo master verifica a sintaxe; se for válida, inicia workers novos e manda os antigos terminarem as requisições em andamento; se houver erro, volta à configuração anterior. O reload não derruba conexões ativas, mas rode `nginx -t` antes para ver o erro com a linha. Para ver a configuração completa já mesclada, use `nginx -T`.

Em deploy, use sempre `nginx -t && nginx -s reload`: o `&&` só recarrega se o teste passar.

## Combina com / alternativas

- [Proxy reverso](03-proxy-reverso-para-a-aplicacao.md) logo a seguir.
- [Comparação com Caddy e Traefik](01-nginx-caddy-ou-traefik.md) se ainda não decidiu.
- [Segurança base da infra](../../infra/docs/12-seguranca-base.md) para firewall e usuário sem privilégio.

## Decisão rápida

- **Use o repositório do nginx.org se:** quer versão atual e controle do canal (stable para produção).
- **Evite se:** a política exige pacote da distro; nesse caso, acompanhe o changelog do pacote para as correções de segurança.
