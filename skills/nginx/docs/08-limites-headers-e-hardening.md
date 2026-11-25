# Limites, headers de segurança e hardening no nginx

> Limite requisições e conexões por IP, envie os headers de segurança certos (sem perdê-los na herança), esconda a versão e bloqueie `.git`, `.env` e arquivos ocultos.

| | |
|---|---|
| **Referência** | nginx.org/en/docs: ngx_http_limit_req_module, ngx_http_limit_conn_module, ngx_http_headers_module, ngx_http_core_module, ngx_core_module; RFC 6797 (HSTS); OWASP Secure Headers Project |
| **Categoria** | Servidor |
| **Tipo** | Prática de endurecimento (hardening) do servidor |
| **Vale para** | nginx 1.31.10 (versão atual da página CHANGES em 2026-11-25); qualquer site ou API atrás do nginx |
| **Verificado em** | 2026-11-25 |

## O que é

Hardening é reduzir o que o servidor expõe e limitar o estrago de abuso. No nginx são quatro frentes:

- **Limites:** `limit_req` (requisições por tempo) e `limit_conn` (conexões simultâneas) por IP.
- **Headers de segurança:** instruções que o navegador segue (só HTTPS, não adivinhar tipo de arquivo, restringir origem de scripts).
- **Esconder informação:** versão do nginx, listagem de pastas, arquivos de configuração.
- **Menos privilégio:** processos de trabalho com usuário comum.

Exemplo do doc: sistema de agendamento de clínica em `app.clinica-exemplo.com.br`, com login em `/login` e API em `api.clinica-exemplo.com.br`.

## Por que usar

- **Força bruta no login:** sem limite, um robô tenta milhares de senhas.
- **Vazamento por descuido:** um `.git` ou `.env` na pasta publicada entrega o código e as senhas.
- **Defesa em camadas:** a aplicação valida, o nginx barra o excesso antes de chegar nela.

## Quando usar

- Em todo servidor público, desde o primeiro deploy.
- Depois de qualquer mudança de `location`: reconfira a herança dos headers.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Headers e bloqueio de ocultos custam pouco |
| MVP de SaaS | ✅ Ótimo | Login exposto desde o dia um |
| SaaS em crescimento | ✅ Ótimo | Limites por rota e por IP protegem a API |
| Sistema interno/corporativo | 🟡 Serve | Menos exposição, mas bloqueio de ocultos continua valendo |
| API/integração | ✅ Ótimo | `limit_req` por rota; CSP importa pouco |
| App mobile com backend | 🟡 Serve | Limite de API sim; headers de navegador pouco |
| Limite só por IP atrás de CDN sem restaurar IP real | ❌ Evite | Todos chegam com o IP da CDN e um limite bloqueia todo mundo ([doc 05](05-atras-da-cloudflare.md)) |

## Quando é bom

- **Zona de limite pequena e nomeada:** `10m` guarda dezenas de milhares de IPs.
- **429 no lugar de 503:** deixa claro para o cliente que foi limite.
- **Headers num arquivo só:** um `include` repetido em cada `location` que declara `add_header`.

## Quando é ruim

- **Limite por IP sem IP real:** atrás de Cloudflare ou outro proxy, `$binary_remote_addr` é o do proxy.
- **Burst alto demais:** o `burst` deixa passar rajadas; no login mantenha baixo.
- **CSP copiada de blog:** uma política rígida quebra scripts e estilos; comece em modo `Report-Only`.
- **HSTS sem certeza do HTTPS:** com `max-age` longo, o navegador recusa HTTP por muito tempo, inclusive subdomínios se usar `includeSubDomains`.

## Como começar

**1. Limite no login e geral.** As zonas ficam em `http {}`:

```nginx
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=geral:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=conexoes:10m;
limit_req_status 429;
limit_conn_status 429;
```

```nginx
server {
    limit_req zone=geral burst=20 nodelay;
    limit_conn conexoes 20;

    location = /login {
        limit_req zone=login burst=5 nodelay;
        limit_req zone=geral burst=20 nodelay;
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Pontos conferidos na documentação:

- `rate=5r/m` é 5 requisições por minuto por IP; `burst` é a fila de excesso; `nodelay` atende o excesso na hora em vez de atrasar.
- O padrão de `limit_req_status` e `limit_conn_status` é `503`; o exemplo troca por `429`.
- As diretivas só herdam do nível anterior se não houver nenhuma `limit_req` no nível atual. Por isso o `/login` repete `zone=geral`.
- Em HTTP/2 e HTTP/3 cada requisição simultânea conta como uma conexão no `limit_conn`.
- `limit_req_dry_run on;` conta sem bloquear: use para medir antes de valer.

Limite por IP não vê a conta atacada. A regra por e-mail e o `Retry-After` ficam na aplicação: [rate limit](../../security/docs/06-rate-limit.md).

**2. Headers de segurança.** Arquivo `/etc/nginx/snippets/seguranca.conf`:

```nginx
add_header Strict-Transport-Security "max-age=31536000" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; frame-ancestors 'self'" always;
```

- **HSTS** (RFC 6797) manda o navegador usar só HTTPS. Comece com `max-age=300`, confirme que tudo funciona e só então suba. Não use `includeSubDomains` ou `preload` sem decidir por todos os subdomínios.
- **`X-Content-Type-Options: nosniff`** impede o navegador de "adivinhar" o tipo do arquivo.
- **`Referrer-Policy`** controla quanto da URL anterior vai para outros sites.
- **CSP** (Content-Security-Policy) limita de onde vêm scripts, estilos e imagens. A linha acima é só ponto de partida: teste com `Content-Security-Policy-Report-Only` e ajuste por aplicação (Next.js e bibliotecas de terceiros costumam exigir mais fontes).
- **`always`:** sem ele o header só sai em respostas 200, 201, 204, 206, 301, 302, 303, 304, 307 e 308; erros 404 e 500 ficam sem proteção.

**3. Herança de `add_header`.** Os `add_header` só passam do nível anterior se o nível atual não tiver nenhum. Um `add_header Cache-Control ...` dentro de um `location` apaga os de segurança do `server`. Solução simples: repetir o `include` onde houver `add_header`:

```nginx
location /assets/ {
    include snippets/seguranca.conf;
    add_header Cache-Control "public, max-age=31536000, immutable";
}
```

A diretiva `add_header_inherit merge;` (desde a 1.29.3) junta os valores dos níveis; confira a versão instalada com `nginx -v`.

**4. Esconder e bloquear.** Em `http {}` e no `server`:

```nginx
server_tokens off;
autoindex off;

location ~ /\.(?!well-known) {
    deny all;
    return 404;
}

location ~* \.(env|bak|sql|log|ini)$ {
    deny all;
    return 404;
}
```

- `server_tokens off` tira a versão da resposta e da página de erro (o padrão é `on`).
- `autoindex` já vem `off`; deixe explícito e nunca ligue em pasta pública.
- A regra dos ocultos barra `.git`, `.env`, `.htaccess`, mas libera `.well-known` (necessário para o certificado, veja [HTTPS](04-https-com-letsencrypt.md)).
- O melhor bloqueio é não publicar o arquivo: o `root` deve apontar para a pasta de build, não para a raiz do repositório.

**5. Usuário sem privilégio.** Em `nginx.conf`, no topo:

```nginx
user nginx;
```

Os processos de trabalho usam esse usuário (o padrão da documentação é `nobody`; o pacote oficial já define `nginx`, o da distro costuma usar `www-data`). O processo mestre roda como root só para abrir as portas 80 e 443. O usuário não deve ter shell nem ser dono do código.

## Combina com / alternativas

- [Segurança no código (OWASP)](../../security/docs/05-owasp-no-codigo.md): o nginx complementa, não substitui validação na aplicação.
- [Rate limit](../../security/docs/06-rate-limit.md): limite por conta e resposta `Retry-After`.
- [Atrás da Cloudflare](05-atras-da-cloudflare.md): restaurar o IP real antes de limitar por IP.
- [Logs e diagnóstico](09-logs-e-diagnostico.md): ver os 429 no log.
- Alternativa: WAF e rate limit da Cloudflare, na borda, antes de chegar ao servidor.

## Decisão rápida

- **Use se:** o servidor é público; aplique os cinco passos e teste com `curl -I` e `nginx -t`.
- **Evite se:** a ideia é copiar uma CSP ou um HSTS `preload` sem teste, ou limitar por IP sem restaurar o IP real.
