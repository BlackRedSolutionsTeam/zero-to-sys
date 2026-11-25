# Estáticos, cache e compressão

> Sirva a SPA com `try_files`, comprima com gzip (e brotli se aceitar módulo de terceiros), cache longo só em arquivos com hash no nome e cache de proxy só do que é público.

| | |
|---|---|
| **Referência** | nginx.org/en/docs (ngx_http_core_module, ngx_http_gzip_module, ngx_http_gzip_static_module, ngx_http_headers_module, ngx_http_proxy_module); github.com/google/ngx_brotli; RFC 9111 (cache HTTP) |
| **Categoria** | Servidor |
| **Tipo** | Prática de entrega de arquivos |
| **Vale para** | SPA (React/Vite), site estático e cache de respostas públicas da API |
| **Verificado em** | 2026-11-25 |

## O que é

Os arquivos estáticos (HTML, JS, CSS, imagens) saem direto do disco pelo nginx, sem passar pela aplicação. Compressão deixa a resposta menor. Cache diz ao navegador (e ao proxy) por quanto tempo reaproveitar o arquivo.

Exemplo do doc: `app.clinica-exemplo.com.br`, uma SPA React gerada em `/var/www/clinica/dist`.

## Por que usar

- **Velocidade:** nginx entrega arquivo mais rápido que qualquer app server.
- **Menos banda:** texto comprimido costuma ficar bem menor.
- **Rotas da SPA:** `/agenda/42` não existe no disco; sem `try_files` o refresh dá 404.

## Quando usar

- Em todo front-end estático servido pelo nginx.
- Em respostas públicas e caras da API (lista de especialidades, por exemplo).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Quase tudo é estático e cacheável |
| MVP de SaaS | ✅ Ótimo | SPA no nginx, API em outro `location` |
| SaaS em crescimento | 🟡 Serve | CDN (Cloudflare) assume o cache; nginx cuida da origem |
| Sistema interno/corporativo | ✅ Ótimo | SPA simples sem CDN |
| API/integração | 🟡 Serve | Só gzip e cache de respostas públicas |
| App mobile com backend | 🟡 Serve | Só cache de respostas públicas |
| Resposta com dados do usuário ou de paciente | ❌ Evite | Cache de proxy pode entregar dado de uma pessoa a outra |

## Quando é bom

- **Hash no nome:** `app.3f9a1c.js` muda quando o conteúdo muda, então pode ficar um ano em cache.
- **`index.html` sem cache longo:** ele aponta para os arquivos novos a cada deploy.
- **`gzip_static`/`brotli_static`:** serve arquivo já comprimido no build, sem gastar CPU.

## Quando é ruim

- **Cache longo em arquivo sem hash** (`logo.png`): o usuário vê a versão velha por meses.
- **Cache de proxy em rota com cookie ou login:** vaza dado privado. Cache só de resposta pública.
- **Brotli no nginx oficial:** não vem no pacote. É módulo de terceiros (`ngx_brotli`, do Google), que você compila e carrega com `load_module`; a página do projeto diz que o módulo e a biblioteca estão em desenvolvimento ativo (conferido em 2026-11-25). Se não quer compilar, deixe a Cloudflare comprimir e use só gzip.

## Como começar

SPA com cache por tipo de arquivo:

```nginx
server {
    listen 443 ssl;
    http2 on;
    server_name app.clinica-exemplo.com.br;
    root /var/www/clinica/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache";
    }

    location /assets/ {
        try_files $uri =404;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location ~* \.(?:png|jpg|jpeg|webp|svg|ico|woff2)$ {
        expires 30d;
        add_header Cache-Control "public";
    }
}
```

O `try_files` testa o arquivo, depois a pasta, e por fim devolve `index.html`. `no-cache` não proíbe guardar: obriga o navegador a revalidar a cada uso. Um `add_header` dentro de `location` apaga os `add_header` do nível acima; repita HSTS e demais headers ali (veja `08-limites-headers-e-hardening.md`). `expires 1y` já cria `Cache-Control: max-age=31536000`; o `add_header` extra acrescenta `immutable`, que diz que o arquivo nunca muda. Vite coloca arquivos com hash em `/assets/`.

Gzip (nativo; `gzip_comp_level` padrão é 1, `gzip_min_length` e `gzip_types` você define):

```nginx
gzip on;
gzip_comp_level 5;
gzip_min_length 1024;
gzip_vary on;
gzip_proxied any;
gzip_types text/css application/javascript application/json image/svg+xml text/plain application/xml;
```

`text/html` sempre é comprimido. Não comprima imagem JPG, PNG, WebP nem vídeo: já são comprimidos. Se o build já gera arquivos `.gz`, ligue `gzip_static on;`. Esse módulo (`ngx_http_gzip_static_module`) só existe se o nginx foi compilado com `--with-http_gzip_static_module`; confira em `nginx -V`.

Brotli (opcional, módulo de terceiros): depois de compilar `ngx_brotli`, ponha no topo do `nginx.conf`:

```nginx
load_module modules/ngx_http_brotli_filter_module.so;
load_module modules/ngx_http_brotli_static_module.so;
```

E no `http`:

```nginx
brotli on;
brotli_static on;
brotli_comp_level 5;
brotli_types text/css application/javascript application/json image/svg+xml;
```

O módulo precisa ser compilado para a mesma versão do nginx; a cada atualização do nginx, recompile.

Cache de proxy, só de resposta pública da API:

```nginx
proxy_cache_path /var/cache/nginx/api levels=1:2 keys_zone=api_publica:10m max_size=200m inactive=10m;

server {
    location /api/especialidades {
        proxy_pass http://127.0.0.1:3000;
        proxy_cache api_publica;
        proxy_cache_valid 200 5m;
        proxy_cache_bypass $http_authorization $cookie_session;
        proxy_no_cache $http_authorization $cookie_session;
    }
}
```

`proxy_cache_bypass` ignora o cache e `proxy_no_cache` não grava nele quando há `Authorization` ou o cookie `session` (ajuste ao nome do seu cookie). Por padrão o nginx já não guarda resposta com `Set-Cookie`. Mesmo assim, deixe só rotas públicas dentro do `location`.

Teste:

```bash
curl -sI -H "Accept-Encoding: gzip" https://app.clinica-exemplo.com.br/assets/app.js
curl -sI https://app.clinica-exemplo.com.br/agenda/42
```

Procure `Content-Encoding: gzip`, `Cache-Control` e status 200 na rota da SPA.

## Combina com / alternativas

- `03-proxy-reverso-para-a-aplicacao.md` para o `location` da API.
- CDN da Cloudflare cacheia e comprime na borda (`../../infra/docs/08-cloudflare.md`).
- Para brotli sem compilar: Caddy (`encode zstd gzip`) ou compressão na Cloudflare.

## Decisão rápida

- **Use se:** o nginx entrega a SPA ou arquivos de upload e você controla o nome com hash.
- **Evite se:** a resposta depende do usuário (cache de proxy) ou você não quer manter módulo compilado (brotli).
