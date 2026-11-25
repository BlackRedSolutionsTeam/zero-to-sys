# HTTPS com Let's Encrypt

> Emita o certificado com Certbot (ou acme.sh), deixe a renovação automática, teste com `certbot renew --dry-run` e use o perfil intermediate da Mozilla no nginx.

| | |
|---|---|
| **Referência** | nginx.org/en/docs (ngx_http_ssl_module, ngx_http_v2_module, quic); ssl-config.mozilla.org; documentação do Certbot (eff-certbot.readthedocs.io); letsencrypt.org |
| **Categoria** | Servidor |
| **Tipo** | Prática de HTTPS no servidor |
| **Vale para** | nginx instalado direto na VPS, sem Coolify/Dokploy |
| **Verificado em** | 2026-11-25 |

## O que é

HTTPS é o HTTP dentro de uma conexão criptografada (TLS). O servidor prova quem é com um certificado. A Let's Encrypt emite certificados grátis, com validade curta, então a renovação precisa ser automática.

Exemplo do doc: sistema de agendamento de clínica, com `app.clinica-exemplo.com.br`, `api.clinica-exemplo.com.br` e `staging.clinica-exemplo.com.br`.

## Por que usar

- **Obrigatório na prática:** navegador marca site sem HTTPS como inseguro e recursos novos exigem HTTPS.
- **Dados de pacientes:** login e agenda não podem trafegar em texto puro.
- **Grátis e automático:** sem compra nem renovação manual.

## Quando usar

- Em todo domínio público servido pelo nginx.
- Atrás da Cloudflare, na origem, junto com o modo Full (strict) (veja `05-atras-da-cloudflare.md`).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Certificado grátis e renovação sozinha |
| MVP de SaaS | ✅ Ótimo | Um comando por domínio |
| SaaS em crescimento | ✅ Ótimo | Vários domínios, ou wildcard com DNS-01 |
| Sistema interno/corporativo | 🟡 Serve | Sem acesso público, use DNS-01 ou CA interna |
| API/integração | ✅ Ótimo | Clientes exigem TLS válido |
| App mobile com backend | ✅ Ótimo | iOS e Android exigem HTTPS |
| Servidor com Coolify/Dokploy ou Caddy | ❌ Evite | O proxy deles já emite o certificado; Certbot disputa a porta 80 |

## Quando é bom

- **Plugin nginx do Certbot:** valida pela porta 80, edita a config e recarrega o nginx.
- **Renovação:** o pacote do Certbot instala um timer (systemd) ou cron que roda a renovação; confira com `systemctl list-timers`.
- **Perfil intermediate da Mozilla:** compatível com navegadores atuais (TLS 1.2 e 1.3, só cifras com sigilo futuro).

## Quando é ruim

- **Validação HTTP-01 com a porta 80 fechada** (firewall ou bloco que redireciona errado): a emissão falha. Para wildcard (`*.clinica-exemplo.com.br`) use DNS-01.
- **Cloudflare com "Always Use HTTPS" mais regra de redirect na origem:** pode gerar laço de redirecionamento.
- **Testar com `certbot` sem `--dry-run`:** estoura o limite de emissões da Let's Encrypt.

## Como começar

Instale e emita (Ubuntu/Debian, pacotes da distro; confira o método recomendado na página do Certbot):

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d app.clinica-exemplo.com.br -d api.clinica-exemplo.com.br
sudo systemctl list-timers | grep certbot
sudo certbot renew --dry-run
```

`--dry-run` usa o ambiente de teste da Let's Encrypt e prova que a renovação vai funcionar. Para recarregar o nginx depois de renovar, use `certbot renew --deploy-hook "systemctl reload nginx"` (o `--nginx` já faz isso no fluxo normal).

Alternativa `acme.sh` (script único, bom para DNS-01 e wildcard):

```bash
acme.sh --issue -d api.clinica-exemplo.com.br -w /var/www/acme
acme.sh --install-cert -d api.clinica-exemplo.com.br \
  --key-file /etc/nginx/tls/api.key \
  --fullchain-file /etc/nginx/tls/api.crt \
  --reloadcmd "systemctl reload nginx"
```

Config do site (perfil intermediate da Mozilla, gerador em ssl-config.mozilla.org, guideline 6.0, conferido em 2026-11-25):

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name api.clinica-exemplo.com.br;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name api.clinica-exemplo.com.br;

    ssl_certificate     /etc/letsencrypt/live/api.clinica-exemplo.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.clinica-exemplo.com.br/privkey.pem;

    ssl_session_timeout 1d;
    ssl_session_cache shared:MozSSL:10m;
    ssl_session_tickets off;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;

    add_header Strict-Transport-Security "max-age=63072000" always;

    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}
```

Pontos conferidos:

- **TLS 1.3 não usa `ssl_ciphers`:** a lista vale só para o 1.2. O gerador da Mozilla pede `ssl_prefer_server_ciphers off`.
- **HSTS:** `max-age=63072000` (2 anos) é o valor do perfil. HSTS faz o navegador recusar HTTP no domínio; teste com `max-age` curto antes. Só use `includeSubDomains` se todos os subdomínios têm HTTPS.
- **`http2 on;`:** a diretiva `http2` existe desde o nginx 1.25.1 (CHANGES de 13/06/2023) e o parâmetro `http2` do `listen` ficou obsoleto. Em versão mais antiga, use `listen 443 ssl http2;`.
- **OCSP stapling:** a Let's Encrypt desligou o OCSP (URLs removidas dos certificados em 07/05/2025, responders desligados em 06/08/2025, segundo o aviso oficial). `ssl_stapling on;` não serve mais para esses certificados; não ative, e não peça "Must Staple". O perfil da Mozilla ainda o lista para CAs que mantêm OCSP.
- **HTTP/3 (QUIC):** exige nginx compilado com `--with-http_v3_module` (confira com `nginx -V`; pacotes oficiais costumam incluir). Abra a porta UDP 443 no firewall.

```nginx
server {
    listen 443 ssl;
    listen 443 quic reuseport;
    listen [::]:443 ssl;
    listen [::]:443 quic reuseport;
    http2 on;
    http3 on;
    add_header Alt-Svc 'h3=":443"; ma=86400' always;
}
```

`reuseport` aparece em um `listen quic` por par endereço:porta. A página nginx.org/en/docs/quic.html descreve `quic` e `reuseport`; confirme `http3 on;` em ngx_http_v3_module na versão instalada.

## Combina com / alternativas

- `05-atras-da-cloudflare.md` para modo Full (strict) e certificado de origem.
- `08-limites-headers-e-hardening.md` para os demais headers de segurança.
- Caddy emite e renova sozinho; Cloudflare Tunnel dispensa certificado na origem.

## Decisão rápida

- **Use se:** o nginx é quem recebe o tráfego público na porta 443.
- **Evite se:** outro proxy (Coolify, Dokploy, Traefik, Caddy) já cuida do certificado.
