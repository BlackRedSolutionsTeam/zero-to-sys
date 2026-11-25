# nginx

Um documento por tópico, da instalação às correções de segurança. Diretivas e avisos foram conferidos em 2026-11-25 em nginx.org.

## Decidir e instalar

| Prática | O que entrega | Doc |
|---|---|---|
| nginx, Caddy ou Traefik | Quando usar cada um | [01-nginx-caddy-ou-traefik.md](01-nginx-caddy-ou-traefik.md) |
| Instalação | Repositório oficial, estrutura, nginx -t | [02-instalacao-e-estrutura.md](02-instalacao-e-estrutura.md) |

## Configurar

| Prática | O que entrega | Doc |
|---|---|---|
| Proxy reverso | Repassar para a aplicação | [03-proxy-reverso-para-a-aplicacao.md](03-proxy-reverso-para-a-aplicacao.md) |
| HTTPS | Let's Encrypt, TLS, HSTS, HTTP/2 e 3 | [04-https-com-letsencrypt.md](04-https-com-letsencrypt.md) |
| Atrás da Cloudflare | IP real, origem fechada | [05-atras-da-cloudflare.md](05-atras-da-cloudflare.md) |
| Estáticos e cache | SPA, compressão, Cache-Control | [06-estaticos-cache-e-compressao.md](06-estaticos-cache-e-compressao.md) |
| WebSocket, SSE e uploads | Conexões longas e arquivos grandes | [07-websocket-sse-e-uploads.md](07-websocket-sse-e-uploads.md) |

## Proteger e operar

| Prática | O que entrega | Doc |
|---|---|---|
| Limites e hardening | limit_req, headers, arquivos ocultos | [08-limites-headers-e-hardening.md](08-limites-headers-e-hardening.md) |
| Logs e diagnóstico | 502, 504, 413 e outros | [09-logs-e-diagnostico.md](09-logs-e-diagnostico.md) |
| Docker e deploy sem queda | Contêiner, reload, blue/green | [10-nginx-com-docker-e-deploy-sem-queda.md](10-nginx-com-docker-e-deploy-sem-queda.md) |
| Correções de segurança | Avisos vigentes, CVEs e rotina de atualização | [11-correcoes-de-seguranca-e-atualizacao.md](11-correcoes-de-seguranca-e-atualizacao.md) |

## Por onde começar

- **Servidor novo:** 01 → 02 → 03 → 04, e o 05 se houver Cloudflare.
- **Erro 502, 504 ou 413:** 09 e 07.
- **O nginx está vulnerável?** 11.
- **Deploy sem derrubar o site:** 10.
