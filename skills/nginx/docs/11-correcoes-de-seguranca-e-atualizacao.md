# Correções de segurança e atualização do nginx

> Confira a versão do nginx contra a página oficial de avisos, atualize pelo canal oficial ou pelo pacote da distro com correção portada, e mantenha uma rotina para não ficar para trás.

| | |
|---|---|
| **Referência** | nginx.org/en/security_advisories.html, nginx.org/en/CHANGES, lista nginx-announce, NVD (nvd.nist.gov), Ubuntu Security Notices, Debian Security Tracker, documentação da imagem `nginx` no Docker Hub |
| **Categoria** | Servidor |
| **Tipo** | Prática de manutenção e segurança |
| **Vale para** | nginx no host (pacote oficial ou da distro) e em contêiner |
| **Verificado em** | 2026-11-25 |

## O que é

O projeto nginx publica cada falha de segurança numa página de avisos (security advisories) com a severidade, as versões afetadas e as corrigidas. Este doc mostra como ler essa página, a lista conferida em 2026-11-25, e como saber se o seu servidor está afetado e corrigir.

Versões em 2026-11-25 (nginx.org/en/download.html): stable 1.30.8 e mainline 1.31.10. O último aviso da página (CVE-2026-132779, TLS 1.3 com `ssl_early_data`) é corrigido em 1.31.10+ e 1.30.8+.

## Por que usar

- **A maioria das falhas é de módulo:** quem não usa o módulo costuma estar fora do alcance.

## Quando usar

- Quando sair um aviso (CVE) do nginx e uma vez por mês.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | nginx exposto à internet; atualização rápida |
| MVP de SaaS | ✅ Ótimo | Um aviso por semana não pode virar incidente |
| SaaS em crescimento | ✅ Ótimo | Imagem e pacote entram na rotina de CI |
| Sistema interno/corporativo | 🟡 Serve | Menos exposto, mas o nginx costuma ficar parado por anos |
| API/integração | ✅ Ótimo | HTTP/2 e TLS na borda são alvo comum |
| App mobile com backend | ✅ Ótimo | A API fica pública o tempo todo |
| Servidor atrás de Coolify/Dokploy/Cloudflare Tunnel | ❌ Evite | O proxy é da plataforma; acompanhe o aviso dela, não o pacote nginx |

## Quando é bom

- **Conferir pelo módulo:** o aviso só importa se o módulo estiver ligado.

## Quando é ruim

- **Comparar só o número da versão da distro:** pode estar corrigido por backport (a correção copiada para a versão antiga).
- **Imagem Docker parada:** sem rebuild, nginx e bibliotecas ficam velhos.

## Como começar

### Lista de avisos (nginx.org, 2026-11-25)

Copiada da página oficial, na ordem dela (do mais novo ao mais antigo). Severidade é a do nginx; a coluna NVD é a maior nota CVSS 3.1 da base NVD (nvd.nist.gov, conferida em 2026-11-25; "-" quando o NVD não tem nota 3.1). A página lista as versões afetadas e as corrigidas por linha; "Corrigido em" vale para a linha stable e a mainline que a página mostra. Os IDs de CVE estão como a página os publica; a coluna "Módulo" é uma classificação minha a partir do título.

| Aviso | CVE | Sev. | NVD | Afetadas | Corrigido em | Módulo |
|---|---|---|---|---|---|---|
| Excessive CPU usage in TLS 1.3 with ssl_early_data | CVE-2026-132779 | medium | 5.3 | 1.21.4-1.31.9 | 1.31.10+, 1.30.8+ | TLS 1.3 (early data) |
| Use-after-free during response processing in resolver | CVE-2026-123634 | medium | 8.1 | 0.6.18-1.31.8 | 1.31.9+, 1.30.7+ | resolver |
| Memory corruption in HTTP/2 flow control | CVE-2026-123007 | major | 8.1 | 1.9.5-1.31.8 | 1.31.9+, 1.30.7+ | HTTP/2 |
| Use-after-free in HTTP/3 | CVE-2026-121810 | medium | 8.1 | 1.25.0-1.31.8 | 1.31.9+, 1.30.7+ | HTTP/3 (QUIC) |
| Use-after-free in HTTP/2 | CVE-2026-123633 | medium | 8.1 | 1.19.7-1.31.8 | 1.31.9+, 1.30.7+ | HTTP/2 |
| Infinite loop while reading client request body over TLS 1.3 | CVE-2026-118899 | major | 7.5 | 1.13.0-1.31.8 | 1.31.9+, 1.30.7+ | TLS 1.3 |
| Use-after-free in mail proxy module | CVE-2026-113425 | major | 8.1 | 0.5.33-1.31.8 | 1.31.9+, 1.30.7+ | mail |
| NULL pointer dereference when using PROXY protocol version 2 | CVE-2026-120993 | minor | 5.3 | 1.31.4-1.31.8 | 1.31.9+ | PROXY protocol |
| Buffer overflow when using alias with try_files | CVE-2026-125283 | minor | 5.3 | 0.9.6-1.31.8 | 1.31.9+, 1.30.7+ | alias |
| SNI bypass when using client certificate validation in stream | CVE-2026-120967 | medium | 4.8 | 1.25.5-1.31.8 | 1.31.9+, 1.30.7+ | stream |
| Insufficient validation in stream ssl_preread module | CVE-2026-123640 | minor | 5.3 | 1.15.2-1.31.8 | 1.31.9+, 1.30.7+ | stream |
| Buffer overflow when using alias with rewrite | CVE-2026-15176 | medium | 8.1 | 0.1.29-1.31.6 | 1.31.7+, 1.30.6+ | rewrite |
| Buffer overflow in script evaluation | CVE-2026-93479 | medium | 8.1 | 1.31.2-1.31.6, 1.30.0-1.30.5 | 1.31.7+, 1.30.6+ | script/rewrite |
| Request body injection in HTTP/3 | CVE-2026-95101 | medium | 5.3 | 1.25.0-1.31.6 | 1.31.7+, 1.30.6+ | HTTP/3 (QUIC) |
| Session forgery when using TLS session tickets | CVE-2026-97629 | medium | 6.5 | 1.23.2-1.31.6 | 1.31.7+, 1.30.6+ | TLS (tickets) |
| Use-after-free when using asynchronous file I/O (AIO) | CVE-2026-97205 | medium | 9.8 | 0.8.11-1.31.6 | 1.31.7+, 1.30.6+ | AIO |
| Buffer overflow when using ngx_http_v3_module | CVE-2026-90439 | medium | 6.5 | 1.29.2-1.31.5 | 1.31.6+, 1.30.5+ | HTTP/3 (QUIC) |
| Buffer overflow when using map and regex | CVE-2026-42533 | major | 8.1 | 0.9.6-1.31.2 | 1.31.3+, 1.30.4+ | map/regex |
| Memory disclosure when using ngx_http_slice_module | CVE-2026-60005 | medium | 8.2 | 1.15.8-1.31.2 | 1.31.3+, 1.30.4+ | slice |
| Use-after-free when using ngx_http_ssi_module | CVE-2026-56434 | medium | 6.5 | 0.8.11-1.31.2 | 1.31.3+, 1.30.4+ | ssi |
| Use-after-free in HTTP/3 | CVE-2026-42530 | major | 8.1 | 1.31.0-1.31.1 | 1.31.2+ | HTTP/3 (QUIC) |
| Buffer overflow in the ngx_http_proxy_v2_module and ngx_http_grpc_module | CVE-2026-42055 | medium | 8.1 | 1.13.10-1.31.1 | 1.31.2+, 1.30.3+ | proxy_v2/grpc |
| Buffer overread in the ngx_http_charset_module | CVE-2026-48142 | low | 4.8 | 0.3.50-1.31.1 | 1.31.2+, 1.30.3+ | charset |
| Buffer overflow in the ngx_http_rewrite_module | CVE-2026-9256 | medium | 8.1 | 0.1.17-1.31.0 | 1.31.1+, 1.30.2+ | rewrite |
| HTTP/2 request injection in the ngx_http_proxy_module | CVE-2026-42926 | medium | 5.8 | 1.29.4-1.30.0 | 1.31.0+, 1.30.1+ | HTTP/2 |
| Buffer overflow in the ngx_http_rewrite_module | CVE-2026-42945 | medium | 8.1 | 0.6.27-1.30.0 | 1.31.0+, 1.30.1+ | rewrite |
| Buffer overread in the ngx_http_scgi_module and ngx_http_uwsgi_module | CVE-2026-42946 | medium | 7.4 | 0.8.42-1.30.0 | 1.31.0+, 1.30.1+ | scgi/uwsgi |
| Buffer overread in the ngx_http_charset_module | CVE-2026-42934 | low | 4.8 | 0.3.50-1.30.0 | 1.31.0+, 1.30.1+ | charset |
| HTTP/3 address spoofing | CVE-2026-40460 | medium | 6.5 | 1.25.0-1.30.0 | 1.31.0+, 1.30.1+ | HTTP/3 (QUIC) |
| resolver use-after-free in OCSP | CVE-2026-40701 | medium | 4.8 | 1.19.0-1.30.0 | 1.31.0+, 1.30.1+ | resolver |
| Buffer overflow in ngx_http_dav_module | CVE-2026-27654 | medium | 8.2 | 0.5.13-1.29.6 | 1.29.7+, 1.28.3+ | dav |
| Buffer overflow in the ngx_http_mp4_module | CVE-2026-27784 | medium | 7.8 | 1.1.19-1.29.6 | 1.29.7+, 1.28.3+ | mp4 |
| Buffer overflow in the ngx_http_mp4_module | CVE-2026-32647 | medium | 7.8 | 1.1.19-1.29.6 | 1.29.7+, 1.28.3+ | mp4 |
| NULL pointer dereference while using CRAM-MD5 or APOP | CVE-2026-27651 | low | 7.5 | 0.5.15-1.29.6 | 1.29.7+, 1.28.3+ | mail |
| Injection in auth_http and XCLIENT | CVE-2026-28753 | medium | 3.7 | 0.6.27-1.29.6 | 1.29.7+, 1.28.3+ | mail |
| OCSP result bypass in stream | CVE-2026-28755 | medium | 5.4 | 1.27.2-1.29.6 | 1.29.7+, 1.28.3+ | stream |
| SSL upstream injection | CVE-2026-1642 | medium | 5.9 | 1.3.0-1.29.4 | 1.29.5+, 1.28.2+ | proxy SSL (upstream) |
| Buffer overread in the ngx_mail_smtp_module | CVE-2025-53859 | low | 3.7 | 0.7.22-1.29.0 | 1.29.1+ | mail |
| SSL session reuse vulnerability | CVE-2025-23419 | medium | 4.3 | 1.11.4-1.27.3 | 1.27.4+, 1.26.3+ | TLS (sessão) |
| Buffer overread in the ngx_http_mp4_module | CVE-2024-7347 | low | 4.7 | 1.5.13-1.27.0 | 1.27.1+, 1.26.2+ | mp4 |
| Buffer overwrite in HTTP/3 | CVE-2024-32760 | medium | 6.5 | 1.25.0-1.25.5, 1.26.0 | 1.27.0+, 1.26.1+ | HTTP/3 (QUIC) |
| Stack overflow and use-after-free in HTTP/3 | CVE-2024-31079 | medium | 4.8 | 1.25.0-1.25.5, 1.26.0 | 1.27.0+, 1.26.1+ | HTTP/3 (QUIC) |
| NULL pointer dereference in HTTP/3 | CVE-2024-35200 | medium | 5.3 | 1.25.0-1.25.5, 1.26.0 | 1.27.0+, 1.26.1+ | HTTP/3 (QUIC) |
| Memory disclosure in HTTP/3 | CVE-2024-34161 | medium | 5.3 | 1.25.0-1.25.5, 1.26.0 | 1.27.0+, 1.26.1+ | HTTP/3 (QUIC) |
| NULL pointer dereference in HTTP/3 | CVE-2024-24989 | major | 7.5 | 1.25.3 | 1.25.4+ | HTTP/3 (QUIC) |
| Use-after-free in HTTP/3 | CVE-2024-24990 | major | 7.5 | 1.25.0-1.25.3 | 1.25.4+ | HTTP/3 (QUIC) |
| Memory corruption in the ngx_http_mp4_module | CVE-2022-41741 | medium | 7.8 | 1.1.3-1.23.1, 1.0.7-1.0.15 | 1.23.2+, 1.22.1+ | mp4 |
| Memory disclosure in the ngx_http_mp4_module | CVE-2022-41742 | medium | 7.1 | 1.1.3-1.23.1, 1.0.7-1.0.15 | 1.23.2+, 1.22.1+ | mp4 |
| 1-byte memory overwrite in resolver | CVE-2021-23017 | medium | 7.7 | 0.6.18-1.20.0 | 1.21.0+, 1.20.1+ | resolver |
| Excessive CPU usage in HTTP/2 with small window updates | CVE-2019-9511 | medium | 7.5 | 1.9.5-1.17.2 | 1.17.3+, 1.16.1+ | HTTP/2 |
| Excessive CPU usage in HTTP/2 with priority changes | CVE-2019-9513 | low | 7.5 | 1.9.5-1.17.2 | 1.17.3+, 1.16.1+ | HTTP/2 |
| Excessive memory usage in HTTP/2 with zero length headers | CVE-2019-9516 | low | 6.5 | 1.9.5-1.17.2 | 1.17.3+, 1.16.1+ | HTTP/2 |
| Excessive memory usage in HTTP/2 | CVE-2018-16843 | low | 7.5 | 1.9.5-1.15.5 | 1.15.6+, 1.14.1+ | HTTP/2 |
| Excessive CPU usage in HTTP/2 | CVE-2018-16844 | low | 7.5 | 1.9.5-1.15.5 | 1.15.6+, 1.14.1+ | HTTP/2 |
| Memory disclosure in the ngx_http_mp4_module | CVE-2018-16845 | medium | 6.1 | 1.1.3-1.15.5, 1.0.7-1.0.15 | 1.15.6+, 1.14.1+ | mp4 |
| Integer overflow in the range filter | CVE-2017-7529 | medium | - | 0.5.6-1.13.2 | 1.13.3+, 1.12.1+ | range filter |
| NULL pointer dereference while writing client request body | CVE-2016-4450 | medium | 7.5 | 1.3.9-1.11.0 | 1.11.1+, 1.10.1+ | núcleo (padrão) |
| Invalid pointer dereference in resolver | CVE-2016-0742 | medium | 7.5 | 0.6.18-1.9.9 | 1.9.10+, 1.8.1+ | resolver |
| Use-after-free during CNAME response processing in resolver | CVE-2016-0746 | medium | 9.8 | 0.6.18-1.9.9 | 1.9.10+, 1.8.1+ | resolver |
| Insufficient limits of CNAME resolution in resolver | CVE-2016-0747 | medium | 5.3 | 0.6.18-1.9.9 | 1.9.10+, 1.8.1+ | resolver |
| SSL session reuse vulnerability | CVE-2014-3616 | medium | - | 0.5.6-1.7.4 | 1.7.5+, 1.6.2+ | TLS (sessão) |
| STARTTLS command injection | CVE-2014-3556 | medium | - | 1.5.6-1.7.3 | 1.7.4+, 1.6.1+ | mail |
| SPDY heap buffer overflow | CVE-2014-0133 | major | - | 1.3.15-1.5.11 | 1.5.12+, 1.4.7+ | SPDY |
| SPDY memory corruption | CVE-2014-0088 | major | - | 1.5.10 | 1.5.11+ | SPDY |
| Request line parsing vulnerability | CVE-2013-4547 | medium | - | 0.8.41-1.5.6 | 1.5.7+, 1.4.4+ | núcleo (padrão) |
| Memory disclosure with specially crafted HTTP backend responses | CVE-2013-2070 | medium | - | 1.1.4-1.2.8, 1.3.9-1.4.0 | 1.5.0+, 1.4.1+, 1.2.9+ | núcleo (padrão) |
| Stack-based buffer overflow with specially crafted request | CVE-2013-2028 | major | - | 1.3.9-1.4.0 | 1.5.0+, 1.4.1+ | núcleo (padrão) |
| Vulnerabilities with Windows directory aliases | CVE-2011-4963 | medium | - | nginx/Windows 0.7.52-1.3.0 | 1.3.1+, 1.2.1+ | Windows |
| Buffer overflow in the ngx_http_mp4_module | CVE-2012-2089 | major | - | 1.1.3-1.1.18, 1.0.7-1.0.14 | 1.1.19+, 1.0.15+ | mp4 |
| Memory disclosure with specially crafted backend responses | CVE-2012-1180 | major | - | 0.1.0-1.1.16 | 1.1.17+, 1.0.14+ | núcleo (padrão) |
| Buffer overflow in resolver | CVE-2011-4315 | medium | - | 0.6.18-1.1.7 | 1.1.8+, 1.0.10+ | resolver |
| Vulnerabilities with invalid UTF-8 sequence on Windows | CVE-2010-2266 | major | - | nginx/Windows 0.7.52-0.8.40 | 0.8.41+, 0.7.67+ | Windows |
| Vulnerabilities with Windows file default stream | CVE-2010-2263 | major | - | nginx/Windows 0.7.52-0.8.39 | 0.8.40+, 0.7.66+ | Windows |
| Vulnerabilities with Windows 8.3 filename pseudonyms | CORE-2010-0121 | major | - | nginx/Windows 0.7.52-0.8.32 | 0.8.33+, 0.7.65+ | Windows |
| An error log data are not sanitized | CVE-2009-4487 | none | - | all | none | núcleo (padrão) |
| The renegotiation vulnerability in SSL protocol | CVE-2009-3555 | major | 9.8 | 0.1.0-0.8.22 | 0.8.23+, 0.7.64+ | TLS |
| Directory traversal vulnerability | CVE-2009-3898 | minor | - | 0.1.0-0.8.16 | 0.8.17+, 0.7.63+ | núcleo (padrão) |
| Buffer underflow vulnerability | CVE-2009-2629 | major | - | 0.1.0-0.8.14 | 0.8.15+, 0.7.62+, 0.6.39+, 0.5.38+ | núcleo (padrão) |
| Null pointer dereference vulnerability | CVE-2009-3896 | major | - | 0.1.0-0.8.13 | 0.8.14+, 0.7.62+, 0.6.39+, 0.5.38+ | núcleo (padrão) |
Com nginx 1.30.8 ou 1.31.10, nenhum aviso da lista fica aberto. Para versões abaixo, procure a sua nas colunas "Afetadas" e "Corrigido em".
### Como saber se está vulnerável

```bash
nginx -v
nginx -V 2>&1 | tr ' ' '\n' | grep -E 'with-http_(v2|v3|mp4|slice|ssi|dav)|with-mail|with-stream'
nginx -T 2>/dev/null | grep -E 'listen .*(quic|http2)|http2 on|http3|mp4|resolver|ssl_early_data|alias|slice|ssi|auth_http|mail|stream'
```

`nginx -v` mostra a versão; `nginx -V` mostra os módulos compilados; `nginx -T` imprime a config inteira e mostra o que você usa de fato. Se o aviso é de um módulo que não está compilado nem usado, você não é afetado por ele. Se é do núcleo, compare a versão com "Afetadas".

Em contêiner, rode os mesmos comandos com `docker compose exec nginx` na frente.
### Como corrigir ou mitigar

- **Corrigir (preferido):** atualize para uma versão da coluna "Corrigido em". Pelo repositório oficial (nginx.org/en/linux_packages.html) ou pela distro.
- **Mitigar enquanto não atualiza:** desligue o recurso. Tire `quic` do `listen` e a diretiva `http3` (HTTP/3); remova o `location` com `mp4;`; tire `ssl_early_data on;`; remova os blocos `mail` e `stream` que não usa. Cada aviso tem um link com o texto da mitigação.

### Mainline e stable

- **Mainline (1.31.x):** recursos novos e correções primeiro.
- **Stable (1.30.x):** só correções importantes; é o padrão para produção. Vá de mainline se precisar de um recurso novo.
- Alguns avisos só afetam a mainline (CVE-2026-120993, PROXY protocol v2, 1.31.4 a 1.31.8).

### Backport nas distros

Ubuntu e Debian costumam manter a versão antiga do nginx e portar só o patch. O número não prova nada. Confira:
```bash
apt changelog nginx | grep -i CVE
dpkg -l nginx
rpm -q --changelog nginx | grep -i CVE
```

Cruze com o Ubuntu Security Notices (ubuntu.com/security/notices) e o Debian Security Tracker (security-tracker.debian.org, pesquisa por `nginx`). Se o CVE aparece como corrigido na versão do seu pacote, está corrigido.

### Imagem Docker desatualizada

Uma tag fixa não recebe correção. Para atualizar:

```bash
docker pull nginx:1.30.8-alpine
docker build --pull --no-cache -t clinica-nginx .
```

Troque a tag quando um aviso exigir, e rode `nginx -t` e `reload`. Imagem própria baseada em `nginx` precisa de rebuild, porque o pacote do sistema (OpenSSL, zlib) também envelhece.

### Mudanças de config ligadas à segurança

- **`http2 on;`:** a diretiva `http2` por servidor chegou no nginx 1.25.1 (13 jun 2023, nginx.org/en/CHANGES) e o parâmetro `http2` do `listen` ficou obsoleto. Use `listen 443 ssl;` com `http2 on;`. 
- **HTTP/3:** o módulo `ngx_http_v3_module` entra com `listen 443 quic reuseport;` (nginx 1.25.0 em diante, segundo a coluna "Afetadas" da página). Como o módulo concentra avisos, ligue só se precisar.

### Rotina de atualização

1. **Assine o nginx-announce** (mailman.nginx.org): cada versão e cada aviso chega por e-mail.
2. **Pacote:** `unattended-upgrades` (Ubuntu e Debian) ou `dnf-automatic` (RHEL e derivados) aplica as correções da distro; ative só o canal de segurança.
3. **Contêiner:** revise a tag todo mês (ou use Renovate/Dependabot para abrir o PR) e refaça `pull` e `up -d`.
4. **Checagem mensal:** compare `nginx -v` com a página de avisos e anote a data.

## Combina com / alternativas

- **Combina com:** [doc 10, Docker e deploy sem queda](10-nginx-com-docker-e-deploy-sem-queda.md), [doc 08, hardening](08-limites-headers-e-hardening.md).
- **Alternativas:** Caddy ou Traefik (também precisam de atualização); proxy da plataforma.

## Decisão rápida

- **Use se:** o nginx está exposto à internet e você quer saber se uma versão tem aviso aberto.
- **Evite se:** o proxy é de uma plataforma gerenciada; acompanhe o aviso do provedor.
