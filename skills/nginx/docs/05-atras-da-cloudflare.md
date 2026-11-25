# nginx atrás da Cloudflare

> Restaure o IP real do visitante com `CF-Connecting-IP`, confie só nas faixas oficiais da Cloudflare e aceite conexões na origem apenas vindas dela.

| | |
|---|---|
| **Referência** | nginx.org/en/docs/http/ngx_http_realip_module.html; developers.cloudflare.com (IP ranges, Origin CA, Authenticated Origin Pulls); cloudflare.com/ips |
| **Categoria** | Servidor |
| **Tipo** | Prática de configuração de origem |
| **Vale para** | nginx na VPS com o domínio proxied (nuvem laranja) na Cloudflare |
| **Verificado em** | 2026-11-25 |

## O que é

Com a Cloudflare na frente, quem fala com o nginx é a Cloudflare, não o visitante. Sem ajuste, o log e o rate limit enxergam sempre o IP dela. O módulo `ngx_http_realip_module` troca o IP da conexão pelo valor de um cabeçalho, mas só quando a conexão vem de um endereço em que você confia.

Exemplo do doc: `api.clinica-exemplo.com.br` na Cloudflare, origem em uma VPS com nginx.

## Por que usar

- **IP certo nos logs** e no `limit_req` (veja `../../security/docs/06-rate-limit.md`): sem isso, todo mundo vira um IP só e o limite bloqueia todos de uma vez.
- **Origem protegida:** quem acha o IP da VPS não contorna a Cloudflare.
- **Sem spoofing:** só um proxy confiável pode dizer qual é o IP do cliente.

## Quando usar

- Sempre que o DNS do site está com proxy ligado na Cloudflare e o nginx recebe o tráfego.
- Não se aplica se usar Cloudflare Tunnel (veja `../../cloudflare/docs/06-tunnel-e-protecao-da-origem.md`); lá o IP vem do `cloudflared` local.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Log e estatística com IP correto |
| MVP de SaaS | ✅ Ótimo | Rate limit de login por IP real |
| SaaS em crescimento | ✅ Ótimo | Origem fechada reduz superfície de ataque |
| Sistema interno/corporativo | 🟡 Serve | Só se estiver exposto pela Cloudflare |
| API/integração | ✅ Ótimo | Rate limit por IP e auditoria |
| App mobile com backend | ✅ Ótimo | A API fica atrás da borda |
| Domínio sem proxy da Cloudflare (nuvem cinza) | ❌ Evite | Não há cabeçalho confiável; usar essa config permite forjar IP |

## Quando é bom

- **Lista oficial:** as faixas ficam em `https://www.cloudflare.com/ips-v4` e `https://www.cloudflare.com/ips-v6` (também na API `api.cloudflare.com/client/v4/ips`).
- **Atualização automática:** um script baixa a lista, gera o arquivo e recarrega o nginx.
- **Dupla trava:** `real_ip` mais firewall liberando só a Cloudflare nas portas 80 e 443.

## Quando é ruim

- **Faixa desatualizada:** a Cloudflare muda a lista de tempos em tempos; IP novo dela sem estar no arquivo vira IP "do cliente".
- **`set_real_ip_from 0.0.0.0/0`:** qualquer um forja `CF-Connecting-IP`. Nunca faça.
- **Confiar em `X-Forwarded-For` direto:** o cliente escreve esse cabeçalho.

## Como começar

Arquivo gerado, por exemplo `/etc/nginx/conf.d/cloudflare-realip.conf`. Faixas conferidas em 2026-11-25 (confira de novo antes de copiar):

```nginx
set_real_ip_from 173.245.48.0/20;
set_real_ip_from 103.21.244.0/22;
set_real_ip_from 103.22.200.0/22;
set_real_ip_from 103.31.4.0/22;
set_real_ip_from 141.101.64.0/18;
set_real_ip_from 108.162.192.0/18;
set_real_ip_from 190.93.240.0/20;
set_real_ip_from 188.114.96.0/20;
set_real_ip_from 197.234.240.0/22;
set_real_ip_from 198.41.128.0/17;
set_real_ip_from 162.158.0.0/15;
set_real_ip_from 104.16.0.0/13;
set_real_ip_from 104.24.0.0/14;
set_real_ip_from 172.64.0.0/13;
set_real_ip_from 131.0.72.0/22;
set_real_ip_from 2400:cb00::/32;
set_real_ip_from 2606:4700::/32;
set_real_ip_from 2803:f800::/32;
set_real_ip_from 2405:b500::/32;
set_real_ip_from 2405:8100::/32;
set_real_ip_from 2a06:98c0::/29;
set_real_ip_from 2c0f:f248::/32;
real_ip_header CF-Connecting-IP;
```

Ponto fora do bloco: `real_ip_header` e `set_real_ip_from` valem em `http`, `server` e `location`. Se usar `X-Forwarded-For` no lugar, adicione `real_ip_recursive on;`.

Script de atualização (rode por cron semanal, e `nginx -t` antes do reload):

```bash
#!/usr/bin/env bash
set -euo pipefail
out=/etc/nginx/conf.d/cloudflare-realip.conf
tmp=$(mktemp)
{
  for f in ips-v4 ips-v6; do
    curl -fsS "https://www.cloudflare.com/$f" | sed 's/^/set_real_ip_from /; s/$/;/'
    echo
  done
  echo "real_ip_header CF-Connecting-IP;"
} | grep -v '^$' > "$tmp"
install -m 644 "$tmp" "$out"
nginx -t && systemctl reload nginx
```

Aceitar só IPs da Cloudflare. Use o firewall (a regra vale para qualquer serviço) e, opcionalmente, o nginx:

```nginx
geo $realip_remote_addr $from_cloudflare {
    default 0;
    include /etc/nginx/conf.d/cloudflare-geo.conf;
}

server {
    if ($from_cloudflare = 0) { return 444; }
}
```

O `geo` olha `$realip_remote_addr`, o endereço original da conexão (o `$remote_addr` já foi trocado pelo IP do visitante). Gere `cloudflare-geo.conf` com linhas `173.245.48.0/20 1;` pelo mesmo script. Teste antes de fechar o firewall.

Certificado de origem (Cloudflare Origin CA): a Cloudflare emite um certificado grátis que só ela confia, com validade escolhida na criação (veja a página Origin CA). Instale no nginx e mude o SSL/TLS da zona para Full (strict):

```nginx
ssl_certificate     /etc/nginx/tls/origin.pem;
ssl_certificate_key /etc/nginx/tls/origin.key;
```

Navegador direto na origem vai reclamar do certificado, o que é esperado. Para provar que a requisição veio da Cloudflare, ative Authenticated Origin Pulls (mTLS): baixe o CA indicado na documentação da Cloudflare e use `ssl_client_certificate` e `ssl_verify_client on;`. Siga o passo a passo da página oficial, pois o CA muda por modo (global, por zona, por hostname).

Teste:

```bash
curl -I https://api.clinica-exemplo.com.br
curl -Ik --resolve api.clinica-exemplo.com.br:443:IP_DA_VPS https://api.clinica-exemplo.com.br
```

O segundo, direto na origem, deve falhar quando a origem está fechada. Confira nos logs se aparece o IP do visitante e não o da Cloudflare.

## Combina com / alternativas

- `../../cloudflare/docs/06-tunnel-e-protecao-da-origem.md`: Tunnel elimina porta aberta e dispensa esta lista.
- `04-https-com-letsencrypt.md`: Let's Encrypt também funciona em Full (strict), mas o HTTP-01 precisa chegar na origem.
- `../../infra/docs/08-cloudflare.md`.

## Decisão rápida

- **Use se:** o domínio está proxied na Cloudflare e o nginx recebe o tráfego direto.
- **Evite se:** o acesso é só por Tunnel, ou o DNS está sem proxy.
