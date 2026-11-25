# Proxy reverso para a aplicação

> O nginx recebe a requisição, repassa para a aplicação com os headers certos e usa conexões reaproveitadas (keepalive) para não perder tempo.

| | |
|---|---|
| **Referência** | nginx.org/en/docs/http/ngx_http_proxy_module.html, nginx.org/en/docs/http/ngx_http_upstream_module.html |
| **Categoria** | Servidor |
| **Tipo** | Prática de configuração de proxy reverso |
| **Vale para** | API Node, .NET e Python; Next.js; qualquer app HTTP atrás do nginx |
| **Verificado em** | 2026-11-25 |

## O que é

`proxy_pass` manda a requisição para outro endereço (a aplicação). Como a aplicação só enxerga o nginx, ela perde o domínio, o IP e o protocolo originais. Por isso o nginx repassa essas informações em headers:

- **Host:** o domínio pedido pelo cliente.
- **X-Real-IP:** o IP do cliente.
- **X-Forwarded-For:** a lista de IPs por onde o pedido passou. `$proxy_add_x_forwarded_for` é o header do cliente com o `$remote_addr` anexado.
- **X-Forwarded-Proto:** `http` ou `https`, para a aplicação gerar links e cookies corretos.

`upstream` é um grupo de servidores com nome. Com `keepalive`, o nginx guarda conexões abertas com a aplicação e as reutiliza.

## Por que usar

- **IP e protocolo corretos** nos logs e nos redirecionamentos da aplicação.
- **Menos conexões novas** com a aplicação.
- **Vários processos** da mesma aplicação atrás de um nome só.
- **Falha isolada:** o nginx tenta o próximo servidor se um cair.

## Quando usar

- Toda aplicação web em servidor próprio.
- Ao rodar mais de um processo da API.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Se for estático, sirva direto; proxy só para a parte dinâmica |
| MVP de SaaS | ✅ Ótimo | Um `location /` com os quatro headers resolve |
| SaaS em crescimento | ✅ Ótimo | `upstream` com vários processos e keepalive |
| Sistema interno/corporativo | ✅ Ótimo | Esconde a porta da aplicação e centraliza o log |
| API/integração | ✅ Ótimo | Timeouts e limite de upload sob controle |
| App mobile com backend | ✅ Ótimo | A API fica em `api.clinica-exemplo.com.br` |
| App que escuta em `0.0.0.0` aberta ao mundo | ❌ Evite | O proxy não protege se a porta da aplicação está exposta |

## Quando é bom

- **Os quatro headers** deixam a aplicação saber quem chamou.
- **Padrões atuais:** `proxy_http_version` é `1.1` por padrão desde o nginx 1.29.7 (mainline), conferido em nginx.org em 2026-11-25. Antes disso, o padrão era `1.0` e você precisava declarar.
- **Timeouts de 60s** (padrão de conexão, envio e leitura) cobrem a maioria das APIs.

## Quando é ruim

- **Esquecer o `Host`:** o padrão é `$proxy_host` (o endereço do `proxy_pass`), então a aplicação vê `127.0.0.1:3000` em vez do domínio.
- **`proxy_set_header` herdado só se o nível atual não definir nenhum.** Definir um header no `location` apaga os do `server`. Repita todos juntos, ou use um arquivo de snippet.
- **Timeout curto** em rota demorada vira 504; timeout longo demais segura conexões.
- **Retry de POST:** o nginx não repete requisições não idempotentes por padrão; não ligue `non_idempotent` sem pensar em duplicidade.
- **Keepalive grande demais** pode esgotar as conexões da aplicação: use número pequeno.

## Como começar

Snippet reutilizável, em `/etc/nginx/snippets/proxy-app.conf` (crie a pasta `snippets` se não existir):

```nginx
proxy_http_version 1.1;
proxy_set_header Connection "";
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_connect_timeout 5s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

`proxy_http_version 1.1` e `Connection ""` são obrigatórios para keepalive antes do nginx 1.29.7 e inofensivos depois. O `proxy_connect_timeout` de 5s é escolha nossa (o padrão é 60s): se a aplicação não aceita conexão em 5s, falhe rápido.

API Node, .NET ou Python (Gunicorn, Uvicorn, Kestrel), em `api.clinica-exemplo.com.br`:

```nginx
upstream api_clinica {
    server 127.0.0.1:3000 max_fails=3 fail_timeout=10s;
    keepalive 16;
}

server {
    listen 80;
    server_name api.clinica-exemplo.com.br;

    location / {
        include snippets/proxy-app.conf;
        proxy_pass http://api_clinica;
    }
}
```

Troque a porta: Node 3000, Kestrel (.NET) 5000 e Gunicorn/Uvicorn 8000 são convenções, defina a sua. Para mais processos, acrescente linhas `server 127.0.0.1:3001;` ao `upstream`; o balanceamento padrão é round-robin (um de cada vez). `max_fails` e `fail_timeout` valem só com mais de um servidor no grupo (ignorados com um só, segundo a documentação).

Na aplicação, diga que há proxy na frente, senão ela não confia nos headers: Express `app.set('trust proxy', 1)`, ASP.NET Core `UseForwardedHeaders` com `X-Forwarded-For` e `X-Forwarded-Proto`, Uvicorn `--proxy-headers` (e `--forwarded-allow-ips` com o IP do proxy). Consulte a página de cada framework.

Next.js (`next start` na 3000), em `app.clinica-exemplo.com.br`:

```nginx
upstream app_clinica {
    server 127.0.0.1:3000;
    keepalive 16;
}

server {
    listen 80;
    server_name app.clinica-exemplo.com.br;

    location / {
        include snippets/proxy-app.conf;
        proxy_pass http://app_clinica;
    }
}
```

Teste e aplique:

```bash
sudo nginx -t && sudo nginx -s reload
curl -I -H "Host: api.clinica-exemplo.com.br" http://127.0.0.1/
```

O HTTPS entra no [doc 04](04-https-com-letsencrypt.md); WebSocket e SSE (que exigem `Upgrade` e `proxy_buffering off`) no doc 07.

## Combina com / alternativas

- [Instalação e estrutura](02-instalacao-e-estrutura.md) para onde salvar cada arquivo.
- [Rate limit](../../security/docs/06-rate-limit.md) para limitar por IP já no proxy.
- Caddy resolve o mesmo com `reverse_proxy` e headers padrão ([doc 01](01-nginx-caddy-ou-traefik.md)).

## Decisão rápida

- **Use `upstream` com keepalive se:** a aplicação recebe tráfego contínuo ou tem mais de um processo.
- **Evite `proxy_pass` direto sem headers se:** a aplicação depende do domínio, do IP ou do protocolo original (login, cookies seguros, logs).
