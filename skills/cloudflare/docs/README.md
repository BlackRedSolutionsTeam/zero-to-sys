# Cloudflare

Um documento por tópico, na ordem em que a configuração costuma ser feita. Limites e planos foram conferidos em 2026-11-25.

## Entrar

| Prática | O que entrega | Doc |
|---|---|---|
| Colocar o domínio | Conta, nameservers, plano Free | [01-colocar-o-dominio-na-cloudflare.md](01-colocar-o-dominio-na-cloudflare.md) |
| DNS e proxy | Laranja x cinza, IP real | [02-dns-e-proxy.md](02-dns-e-proxy.md) |
| SSL/TLS e HSTS | Full (strict), certificado de origem | [03-ssl-tls-e-hsts.md](03-ssl-tls-e-hsts.md) |

## Proteger e acelerar

| Prática | O que entrega | Doc |
|---|---|---|
| Cache | Regras seguras, purge, nunca página logada | [04-cache-e-performance.md](04-cache-e-performance.md) |
| WAF, rate limit e bots | Regras, limites, Turnstile | [05-waf-rate-limit-e-bots.md](05-waf-rate-limit-e-bots.md) |
| Tunnel e origem | Publicar sem abrir porta, origem fechada | [06-tunnel-e-protecao-da-origem.md](06-tunnel-e-protecao-da-origem.md) |
| Access | Proteger painéis internos | [07-access-e-zero-trust.md](07-access-e-zero-trust.md) |

## Serviços

| Prática | O que entrega | Doc |
|---|---|---|
| Pages e Workers | Site estático e funções na borda | [08-pages-e-workers.md](08-pages-e-workers.md) |
| R2 e extras | R2, Email Routing, redirects | [09-r2-email-routing-e-extras.md](09-r2-email-routing-e-extras.md) |

## Em código

| Prática | O que entrega | Doc |
|---|---|---|
| Cloudflare com IaC | DNS e regras em código | [10-cloudflare-com-iac.md](10-cloudflare-com-iac.md) |

## Por onde começar

- **Domínio novo na Cloudflare:** 01 → 02 → 03 → 04 → 05.
- **Servidor exposto na internet:** 06.
- **Painel interno (Coolify, Grafana, staging) aberto:** 07.
- **Site estático ou função simples:** 08.
- **Arquivos e e-mail do domínio:** 09.
- **Mais de um ambiente ou time:** 10.
