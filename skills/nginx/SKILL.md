---
name: nginx
description: 'Configura o nginx como proxy reverso seguro e atualizado: quando usar nginx, Caddy ou Tunnel, HTTPS, IP real, limites, cabeçalhos, hardening, erros 502/504/413 e CVEs. Use quando pedirem "configurar o nginx", "proxy reverso", "HTTPS no servidor" ou "erro 502".'
---

# nginx

Guia para colocar o nginx na frente da aplicação sem copiar configuração de blog: HTTPS certo, IP real, limites, headers, logs úteis e versão sem falha de segurança conhecida. Em muitos projetos o proxy do Coolify ou do Dokploy (Traefik) ou o Caddy resolvem com menos trabalho; esta skill diz quando o nginx vale e como fazer quando vale. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e configurações prontas.

## Como usar esta skill

1. **Decida se é nginx** ([doc 01](docs/01-nginx-caddy-ou-traefik.md)): com Coolify ou Dokploy, use o proxy deles; servidor simples com um app, Caddy costuma bastar; vários sites ou controle fino, nginx.
2. **Instale pelo repositório oficial** (nginx.org) e organize um arquivo por site; rode `nginx -t` antes de todo `reload` ([doc 02](docs/02-instalacao-e-estrutura.md)).
3. **Configure o proxy** para a aplicação com os headers certos ([doc 03](docs/03-proxy-reverso-para-a-aplicacao.md)).
4. **Ligue o HTTPS** com Let's Encrypt e o perfil intermediate da Mozilla; teste a renovação ([doc 04](docs/04-https-com-letsencrypt.md)).
5. **Atrás da Cloudflare**, restaure o IP real e aceite só as faixas dela ([doc 05](docs/05-atras-da-cloudflare.md)).
6. **Ajuste estáticos, WebSocket, SSE e uploads** conforme o app ([doc 06](docs/06-estaticos-cache-e-compressao.md), [doc 07](docs/07-websocket-sse-e-uploads.md)).
7. **Aplique limites e hardening** ([doc 08](docs/08-limites-headers-e-hardening.md)) e configure logs ([doc 09](docs/09-logs-e-diagnostico.md)).
8. **Em contêiner ou com deploy sem queda**, siga o [doc 10](docs/10-nginx-com-docker-e-deploy-sem-queda.md).
9. **Compare a versão instalada com os avisos de segurança vigentes** e atualize ([doc 11](docs/11-correcoes-de-seguranca-e-atualizacao.md)).

## Configuração por caso

| Caso | Docs | Pontos principais |
|---|---|---|
| SPA estática (React, Vue) | 02, 04, 06 | `try_files` para o `index.html`, cache longo nos arquivos com hash |
| API (Node, .NET, Python) | 03, 04, 05, 08 | Headers `X-Forwarded-*`, timeouts, `limit_req` no login |
| Next.js e SSR | 03, 06 | Proxy para o servidor do Next, cache só de `/_next/static` |
| WebSocket ou SSE | 07 | `map` de `Upgrade`, `proxy_read_timeout`, `proxy_buffering off` |
| Upload grande | 07 | `client_max_body_size` por rota, `proxy_request_buffering` |
| Vários sites no mesmo servidor | 02, 04 | Um arquivo por site, um certificado por domínio |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| nginx, Caddy ou Traefik | [docs/01-nginx-caddy-ou-traefik.md](docs/01-nginx-caddy-ou-traefik.md) | Quando usar cada um |
| Instalação | [docs/02-instalacao-e-estrutura.md](docs/02-instalacao-e-estrutura.md) | Repositório oficial, mainline x stable, estrutura |
| Proxy reverso | [docs/03-proxy-reverso-para-a-aplicacao.md](docs/03-proxy-reverso-para-a-aplicacao.md) | Headers, timeouts, upstream |
| HTTPS | [docs/04-https-com-letsencrypt.md](docs/04-https-com-letsencrypt.md) | Certbot, TLS da Mozilla, HSTS, HTTP/2 e 3 |
| Atrás da Cloudflare | [docs/05-atras-da-cloudflare.md](docs/05-atras-da-cloudflare.md) | IP real, origem fechada |
| Estáticos e cache | [docs/06-estaticos-cache-e-compressao.md](docs/06-estaticos-cache-e-compressao.md) | SPA, gzip, brotli, Cache-Control |
| WebSocket, SSE e uploads | [docs/07-websocket-sse-e-uploads.md](docs/07-websocket-sse-e-uploads.md) | Conexões longas e arquivos grandes |
| Limites e hardening | [docs/08-limites-headers-e-hardening.md](docs/08-limites-headers-e-hardening.md) | limit_req, headers, arquivos ocultos |
| Logs e diagnóstico | [docs/09-logs-e-diagnostico.md](docs/09-logs-e-diagnostico.md) | log_format, logrotate, sintoma → causa |
| Docker e deploy sem queda | [docs/10-nginx-com-docker-e-deploy-sem-queda.md](docs/10-nginx-com-docker-e-deploy-sem-queda.md) | Contêiner, reload, blue/green |
| Correções de segurança | [docs/11-correcoes-de-seguranca-e-atualizacao.md](docs/11-correcoes-de-seguranca-e-atualizacao.md) | Avisos vigentes, CVEs, rotina de atualização |

## Checklist

- [ ] Versão do nginx sem aviso de segurança aberto para os módulos em uso (`nginx -V` comparado ao doc 11 e a nginx.org/en/security_advisories.html).
- [ ] `nginx -t` roda antes de todo reload, inclusive no deploy.
- [ ] HTTPS válido, com renovação testada (`certbot renew --dry-run`) e HTTP redirecionando para HTTPS.
- [ ] TLS 1.2 e 1.3 com o perfil intermediate da Mozilla; `ssl_stapling` desligado com Let's Encrypt (o OCSP deles foi desligado).
- [ ] `server_tokens off` e listagem de diretório desligada.
- [ ] `.git`, `.env` e arquivos ocultos bloqueados, mantendo `/.well-known` (`curl -I https://dominio/.env` responde 404 ou 403).
- [ ] `client_max_body_size` definido conforme o maior upload do app.
- [ ] IP real restaurado quando atrás da Cloudflare (o log mostra o IP do visitante, não o da Cloudflare).
- [ ] `limit_req` na rota de login.
- [ ] Logs com `$request_id` e rotação configurada (`/etc/logrotate.d/nginx`).

## Regras de uso

- **Versão sem CVE aberto.** Confira a página de avisos do nginx ao instalar e a cada atualização; na distro, a correção pode vir por backport sem mudar o número da versão.
- **`nginx -t` sempre.** Reload com config quebrada derruba todos os sites do servidor.
- **Um arquivo por site.** Config gigante única é onde nascem os erros de `server_name`.
- **Copie das fontes oficiais**, não de blog: diretivas mudam (por exemplo, `http2 on;` no lugar do parâmetro no `listen`).
- **`add_header` não herda** quando o bloco filho define outro `add_header`; repita os headers de segurança ou use o mecanismo da versão atual (doc 08).
- **Proxy do painel primeiro.** Com Coolify ou Dokploy, não coloque um nginx na frente do Traefik sem motivo.
- **Fronteiras.** VPS e sistema operacional são da `vps`; borda, DNS e WAF da `cloudflare`; regras de permissão e rate limit dentro da aplicação da `security`.

## Quando a lista não cobre

nginx Plus, módulos compilados à mão além do brotli, balanceamento entre vários servidores com health check ativo, servidor de streaming (RTMP), mail proxy e configuração de PHP-FPM detalhada ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial.

## Validade dos dados

Versões (mainline e stable), diretivas e avisos de segurança foram conferidos em 2026-11-25 em nginx.org. Cada documento tem a linha "Verificado em"; a lista de avisos do doc 11 envelhece rápido, confira a página oficial antes de afirmar que uma versão está segura.
