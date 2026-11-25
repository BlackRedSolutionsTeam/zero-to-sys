# Nginx com Docker e deploy sem queda

> Rode o nginx em contêiner com a imagem oficial de tag fixa, config por volume, e troque a versão da aplicação com `nginx -t` seguido de `reload`, sem derrubar nenhuma conexão.

| | |
|---|---|
| **Referência** | nginx.org (Controlling nginx, ngx_http_upstream_module, ngx_http_proxy_module), imagem oficial `nginx` no Docker Hub e github.com/nginx/docker-nginx, documentação do Docker Compose e do Certbot |
| **Categoria** | Servidor |
| **Tipo** | Prática de empacotamento e de deploy |
| **Vale para** | VPS com Docker Compose sem Coolify/Dokploy; exemplos para a clínica de agendamento |
| **Verificado em** | 2026-11-25 |

## O que é

Em vez de instalar o nginx no servidor (host), você roda ele num contêiner (um processo isolado empacotado com suas dependências). A imagem oficial é a `nginx` do Docker Hub; a variante `alpine` é menor, baseada no Alpine Linux. Sua configuração fica em arquivos do servidor, montados no contêiner por volume (uma pasta do host visível dentro do contêiner).

Exemplo do doc: `clinica-exemplo.com.br`, com `app.` (front), `api.` (API) e `staging.`, todos atrás de um nginx.

## Por que usar

- **Versão reproduzível:** a tag da imagem diz qual nginx roda; voltar atrás é trocar a tag.
- **Um comando:** nginx, app e certbot sobem com `docker compose up -d`, e a app nem publica porta no host.

## Quando usar

- Quando a aplicação já roda em Docker Compose.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Hospedagem estática resolve com menos peças |
| MVP de SaaS | ✅ Ótimo | Um Compose com app, banco e nginx sobe em minutos |
| SaaS em crescimento | ✅ Ótimo | Blue/green e `max_fails` dão deploy sem queda em um servidor |
| Sistema interno/corporativo | ✅ Ótimo | Uma VPS, um Compose, atualização por troca de tag |
| API/integração | ✅ Ótimo | Proxy com limites e upstream saudável na frente da API |
| App mobile com backend | ✅ Ótimo | A API precisa de HTTPS estável e deploy sem erro para o app |
| Servidor já gerenciado por Coolify/Dokploy | ❌ Evite | A plataforma já tem proxy próprio; um nginx na frente briga pelas portas 80 e 443 |

## Quando é bom

- **Tag fixa:** `nginx:1.30.8-alpine` não muda sozinha; você decide quando atualizar.

## Quando é ruim

- **Tag `latest`:** a imagem muda sem aviso.
- **Tag fixa e esquecida:** a versão fica velha e acumula falhas conhecidas. Veja [o doc 11](11-correcoes-de-seguranca-e-atualizacao.md).
- **Certificados sem volume:** recriar o contêiner apaga os certificados.
- **`restart` no lugar de `reload`:** reiniciar derruba conexões.

## Como começar

### No contêiner ou no host

No contêiner, a versão é a da tag e atualizar é trocar a tag. No host, a versão vem do repositório e da distro (veja o doc 11 sobre backport). Prefira o host quando há vários sites sem Docker.

### Imagem e tag

Conferido em 2026-11-25 no Docker Hub: existem as tags `1.30.8-alpine` (linha stable) e `1.31.10-alpine` (linha mainline), além das variantes `-slim`, `-perl` e `-otel`. Use a linha stable com versão completa.

```bash
docker pull nginx:1.30.8-alpine
docker run --rm nginx:1.30.8-alpine nginx -V
```

A imagem lê `/etc/nginx/nginx.conf`, que inclui `/etc/nginx/conf.d/*.conf`.

### Compose com app e certbot

Pastas em `/srv/clinica/`: `compose.yaml`, `nginx/conf.d/`, `nginx/upstream/` e `certbot/{conf,www}/`.

`compose.yaml`:

```yaml
services:
  api:
    image: registry.exemplo.com/clinica-api:2026.11.25
    restart: unless-stopped

  nginx:
    image: nginx:1.30.8-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/upstream:/etc/nginx/upstream:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro

  certbot:
    image: certbot/certbot:latest
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: /bin/sh -c "trap exit TERM; while :; do certbot renew --webroot -w /var/www/certbot; sleep 12h & wait $${!}; done"
```

Troque `latest` do certbot por uma versão fixa. O desafio HTTP-01 usa o bloco da porta 80 abaixo, e o nginx precisa de `reload` após cada renovação.

`nginx/conf.d/app.conf`:

```nginx
server {
    listen 80;
    server_name api.clinica-exemplo.com.br;
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 301 https://$host$request_uri; }
}

server {
    listen 443 ssl;
    http2 on;
    server_name api.clinica-exemplo.com.br;
    ssl_certificate     /etc/letsencrypt/live/api.clinica-exemplo.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.clinica-exemplo.com.br/privkey.pem;
    client_max_body_size 10m;

    location / {
        include /etc/nginx/upstream/api.conf;
        proxy_pass http://api_pool;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

O primeiro certificado precisa existir antes do bloco 443 subir (veja o doc 04). O `http2 on;` exige nginx 1.25.1 ou mais novo (veja o doc 11).

### Alternativa com Caddy

Sem querer cuidar de certificado, troque nginx e certbot pela imagem `caddy:2-alpine` com um `Caddyfile` de duas linhas (`api.clinica-exemplo.com.br { reverse_proxy api:3000 }`). Confira a sintaxe na documentação do Caddy.

### Reload sem queda

O sinal `HUP` (o `reload`) faz o processo mestre validar a config nova, abrir workers novos e pedir aos antigos que terminem as conexões em andamento e saiam. Se a config for inválida, o nginx continua com a antiga. Fonte: nginx.org/en/docs/control.html.

```bash
docker compose exec nginx sh -c "nginx -t && nginx -s reload"
```

Depois de cada renovação do certificado, rode o `reload` (por exemplo, num cron do servidor).

### Blue/green com upstream

A app roda em dois serviços, `api_blue` e `api_green`. O nginx aponta para um arquivo que diz qual está ativo.

`nginx/upstream/api.conf`:

```nginx
upstream api_pool {
    server api_blue:3000 max_fails=3 fail_timeout=10s;
    server api_green:3000 backup;
    keepalive 16;
}
```

O parâmetro `backup` só recebe tráfego quando o outro falha. `max_fails=3` com `fail_timeout=10s` marca o servidor como indisponível por 10 segundos depois de 3 falhas dentro dessa janela (health check passivo: o nginx só descobre o problema quando um pedido real falha). Conferido em nginx.org/en/docs/http/ngx_http_upstream_module.html.

Rotina de deploy: suba a versão nova no serviço parado (`api_green`) e espere o healthcheck do Compose; troque no arquivo qual é principal e qual é `backup`; rode `nginx -t` e `nginx -s reload`; observe o `error.log` por alguns minutos (se falhar, desfaça o arquivo e recarregue); só então pare o `api_blue`.

As duas versões convivem por um tempo, então as migrações do banco precisam ser compatíveis com a versão anterior.

## Combina com / alternativas

- **Combina com:** [doc 04, HTTPS com Let's Encrypt](04-https-com-letsencrypt.md), [doc 11, atualização e correções](11-correcoes-de-seguranca-e-atualizacao.md), [infra, VPS com Coolify/Dokploy](../../infra/docs/02-vps-coolify-dokploy.md).
- **Alternativas:** Caddy, Traefik, Coolify/Dokploy. Comparação no doc 01.

## Decisão rápida

- **Use se:** a app roda em Compose e você quer versão reproduzível e deploy sem queda em um servidor.
- **Evite se:** a VPS é gerenciada por Coolify/Dokploy, ou você não vai manter a tag atualizada (prefira o pacote da distro com atualização automática).
