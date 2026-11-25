# Tunnel e proteção da origem

> Esconda a origem: ou publique o serviço por um túnel que só faz conexões de saída, ou aceite conexões apenas dos IPs da Cloudflare.

| | |
|---|---|
| **Referência** | developers.cloudflare.com/cloudflare-one/connections/connect-networks (Cloudflare Tunnel), developers.cloudflare.com/fundamentals/concepts/cloudflare-ip-addresses, cloudflare.com/ips |
| **Categoria** | Borda |
| **Tipo** | Prática de proteção da origem |
| **Vale para** | Servidor (VPS) atrás da Cloudflare; exemplos com Ubuntu, `ufw` e nginx |
| **Verificado em** | 2026-11-25 |

## O que é

A **origem** é o seu servidor real. Se alguém descobre o IP dela, acessa direto e passa por cima do WAF e do rate limit.

Há dois jeitos de impedir:

- **Cloudflare Tunnel:** o programa `cloudflared`, no servidor, abre uma conexão de saída até a Cloudflare. O tráfego chega por ela. Nenhuma porta de entrada fica aberta.
- **Origem exposta com lista de IPs:** o nginx continua ouvindo nas portas 80 e 443, mas o firewall só aceita IPs da Cloudflare.

Exemplo do doc: VPS da `clinica-exemplo.com.br`, com a app em `app.`, a API em `api.` e o staging em `staging.`.

## Por que usar

- **Origem invisível:** com túnel, nem a porta 443 responde para a internet.
- **Sem atalho:** o atacante não contorna o WAF.
- **Sem certificado público na origem** no caso do túnel (a Cloudflare termina o TLS).
- **Funciona atrás de NAT** (rede de escritório, casa), sem IP fixo.

## Quando usar

- Qualquer origem com domínio na Cloudflare: escolha uma das duas opções, não deixe aberta.
- Túnel: serviço em máquina sem IP público, painel interno, staging.
- Lista de IPs: VPS pública com nginx que você já opera.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Origem aberta só para a Cloudflare já basta |
| MVP de SaaS | ✅ Ótimo | Túnel é rápido de montar e dispensa regra de firewall |
| SaaS em crescimento | ✅ Ótimo | Lista de IPs com nginx dá controle e várias instâncias |
| Sistema interno/corporativo | ✅ Ótimo | Túnel mais Access publica sem abrir porta |
| API/integração | 🟡 Serve | Cuidado com limites de upload e timeout da Cloudflare |
| App mobile com backend | 🟡 Serve | Funciona; a API continua passando pela borda |
| Origem sem proxy da Cloudflare (nuvem cinza) | ❌ Evite | Não há o que proteger com lista de IPs; todo mundo chega direto |

## Quando é bom

- **Túnel:** zero portas de entrada, nada a manter de lista de IPs, bom para staging.
- **Lista de IPs:** nginx normal, logs completos, desempenho sem salto extra.
- **Duas camadas juntas:** firewall por IP mais [Authenticated Origin Pulls](03-ssl-tls-e-hsts.md) (a origem confere o certificado da Cloudflare).

## Quando é ruim

- **Túnel é um ponto único:** se o `cloudflared` cair, o site cai. Rode como serviço e monitore.
- **Túnel não serve a tudo:** só tráfego pela Cloudflare; SSH, e-mail e outros protocolos precisam de outra solução.
- **Lista de IPs desatualizada** bloqueia visitantes. A Cloudflare diz que as faixas mudam pouco e que as novas entram na lista antes de entrar em produção; reconfira periodicamente.
- **Filtrar IP não prova identidade:** outra conta da Cloudflare também usa esses IPs. Use Authenticated Origin Pulls ou túnel para garantir que é a sua zona.

## Como começar

**Tunnel com arquivo de configuração** (conferido em 2026-11-25 na documentação oficial):

```sh
brew install cloudflared
cloudflared tunnel login
cloudflared tunnel create clinica-exemplo
```

Em Linux, instale pelo pacote da página de downloads da Cloudflare. O `create` devolve um UUID e grava o arquivo de credenciais. Crie o `config.yml` (por padrão em `$HOME/.cloudflared/`):

```yml
tunnel: <UUID-DO-TUNEL>
credentials-file: /home/deploy/.cloudflared/<UUID-DO-TUNEL>.json

ingress:
  - hostname: app.clinica-exemplo.com.br
    service: http://localhost:3000
  - hostname: api.clinica-exemplo.com.br
    service: http://localhost:8080
  - service: http_status:404
```

A última regra, sem `hostname`, é obrigatória. Valide, crie os registros DNS e rode:

```sh
cloudflared tunnel ingress validate
cloudflared tunnel route dns clinica-exemplo app.clinica-exemplo.com.br
cloudflared tunnel route dns clinica-exemplo api.clinica-exemplo.com.br
cloudflared tunnel run clinica-exemplo
```

O `route dns` cria um CNAME para `<UUID>.cfargotunnel.com`. Para rodar sempre, instale como serviço:

```sh
sudo cloudflared --config /home/deploy/.cloudflared/config.yml service install
sudo systemctl start cloudflared
```

Após mudar a configuração: `systemctl restart cloudflared`.

**Pelo painel (túnel gerenciado remotamente):** Networking > Tunnels > Create a tunnel, escolha Linux, copie o comando de instalação, rode no servidor e adicione uma rota em Published application com hostname e URL do serviço (ex.: `http://localhost:3000`). O servidor precisa alcançar a Cloudflare na porta de saída 7844.

**Origem exposta: listas oficiais.** Fonte: `https://www.cloudflare.com/ips-v4`, `https://www.cloudflare.com/ips-v6` e a API `https://api.cloudflare.com/client/v4/ips`. Faixas IPv4 em 2026-11-25:

```
173.245.48.0/20 103.21.244.0/22 103.22.200.0/22 103.31.4.0/22
141.101.64.0/18 108.162.192.0/18 190.93.240.0/20 188.114.96.0/20
197.234.240.0/22 198.41.128.0/17 162.158.0.0/15 104.16.0.0/13
104.24.0.0/14 172.64.0.0/13 131.0.72.0/22
```

Não copie a lista à mão: baixe e aplique com script. Exemplo com `ufw`:

```sh
sudo ufw default deny incoming
sudo ufw allow from <SEU-IP> to any port 22 proto tcp
for ip in $(curl -s https://www.cloudflare.com/ips-v4) $(curl -s https://www.cloudflare.com/ips-v6); do
  sudo ufw allow from "$ip" to any port 443 proto tcp
done
sudo ufw enable
```

Rode o script por agendamento (cron) para manter a lista em dia. Libere a porta 80 do mesmo modo só se precisar dela. No nginx, para registrar o IP real do visitante, veja `../../nginx/docs/` (cabeçalho `CF-Connecting-IP` e `set_real_ip_from`).

**Tunnel ou nginx exposto?**

| Situação | Escolha |
|---|---|
| Sem IP público, atrás de NAT | Tunnel |
| Staging, painel interno, serviço de teste | Tunnel |
| Quer zero porta de entrada | Tunnel |
| VPS pública, nginx já em uso, vários sites | nginx com lista de IPs |
| Precisa de upload grande ou WebSocket pesado | Confira os limites da Cloudflare nos dois casos |

## Combina com / alternativas

- [WAF, rate limit e bots](05-waf-rate-limit-e-bots.md): só valem se a origem não tiver porta aberta ao mundo.
- [Access e Zero Trust](07-access-e-zero-trust.md): põe login na frente do que o túnel publica.
- [SSL/TLS e HSTS](03-ssl-tls-e-hsts.md): modo Full (strict) e Authenticated Origin Pulls.
- [VPS com Coolify ou Dokploy](../../infra/docs/02-vps-coolify-dokploy.md): onde a origem costuma rodar.
- Alternativas: VPN (Tailscale, WireGuard) para acesso de equipe.

## Decisão rápida

- **Use se:** a origem tem domínio na Cloudflare e você não quer que o IP dela receba tráfego de ninguém mais.
- **Evite se:** precisa de protocolo que o túnel não cobre (use firewall e VPN), ou não tem como monitorar o `cloudflared`.
