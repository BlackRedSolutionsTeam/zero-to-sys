---
name: cloudflare
description: 'Configura a Cloudflare na frente do sistema: domínio e DNS, proxy e IP real, SSL Full (strict), cache seguro, WAF e rate limit, Tunnel, Access, Pages, Workers e R2. Use quando pedirem "pôr a Cloudflare", "proteger o site", "cache da Cloudflare" ou "Tunnel".'
---

# cloudflare

Guia para usar a Cloudflare como a camada que fica entre a internet e o servidor: DNS, HTTPS, cache, proteção e, quando fizer sentido, a própria hospedagem. O plano grátis cobre a maioria dos projetos do plugin; o erro comum não é o plano, é a configuração (SSL Flexible, cache de página logada, origem aberta para qualquer IP). Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e configurações prontas.

## Como usar esta skill

1. **Tenha o domínio registrado** e em nome do cliente (skill `domains`).
2. **Coloque o domínio na Cloudflare** e confira os registros importados ([doc 01](docs/01-colocar-o-dominio-na-cloudflare.md)).
3. **Defina o proxy por registro:** laranja para o que é web, cinza para MX, SSH e o que não for HTTP ([doc 02](docs/02-dns-e-proxy.md)).
4. **Ligue SSL Full (strict)** com certificado na origem, Always Use HTTPS e, depois de testado, HSTS ([doc 03](docs/03-ssl-tls-e-hsts.md)).
5. **Configure o cache** só para o que é público e estático ([doc 04](docs/04-cache-e-performance.md)).
6. **Proteja:** WAF, regra para `/admin` e `/login`, rate limit e Turnstile nos formulários ([doc 05](docs/05-waf-rate-limit-e-bots.md)).
7. **Feche a origem:** Tunnel ou firewall aceitando só IPs da Cloudflare ([doc 06](docs/06-tunnel-e-protecao-da-origem.md)); painéis internos atrás do Access ([doc 07](docs/07-access-e-zero-trust.md)).
8. **Use os serviços que fizerem sentido:** Pages e Workers ([doc 08](docs/08-pages-e-workers.md)), R2, Email Routing e redirecionamentos ([doc 09](docs/09-r2-email-routing-e-extras.md)).
9. **Leve para código** a partir do segundo ambiente ([doc 10](docs/10-cloudflare-com-iac.md)).

## Configuração por tipo de projeto

| Projeto | Proxy e SSL | Cache | Proteção | Hospedagem na Cloudflare |
|---|---|---|---|---|
| Site de conteúdo, landing | Laranja, Full (strict) | Estáticos e, se o site for estático, o HTML | WAF grátis | Pages |
| MVP ou SaaS | Laranja, Full (strict) | Só estáticos com hash; nada do app logado | WAF, rate limit no login, Turnstile no cadastro | Origem em VPS ou PaaS; Tunnel se for VPS |
| API | Laranja, Full (strict) | Nenhum (ou só GET público) | Rate limit por rota | Origem própria |
| Sistema interno | Laranja | Nenhum | Access na frente de tudo | Tunnel |
| Painéis (Coolify, Grafana, staging) | Laranja | Nenhum | Access | Tunnel |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Colocar o domínio | [docs/01-colocar-o-dominio-na-cloudflare.md](docs/01-colocar-o-dominio-na-cloudflare.md) | Conta, nameservers, importar registros, plano Free |
| DNS e proxy | [docs/02-dns-e-proxy.md](docs/02-dns-e-proxy.md) | Laranja x cinza, portas, IP real, WebSocket |
| SSL/TLS e HSTS | [docs/03-ssl-tls-e-hsts.md](docs/03-ssl-tls-e-hsts.md) | Full (strict), certificado de origem, HSTS |
| Cache | [docs/04-cache-e-performance.md](docs/04-cache-e-performance.md) | Cache Rules seguras, purge, compressão |
| WAF, rate limit e bots | [docs/05-waf-rate-limit-e-bots.md](docs/05-waf-rate-limit-e-bots.md) | Regras, limites do Free, Turnstile |
| Tunnel e origem | [docs/06-tunnel-e-protecao-da-origem.md](docs/06-tunnel-e-protecao-da-origem.md) | Publicar sem abrir porta, IPs da Cloudflare |
| Access | [docs/07-access-e-zero-trust.md](docs/07-access-e-zero-trust.md) | Login na frente de painéis internos |
| Pages e Workers | [docs/08-pages-e-workers.md](docs/08-pages-e-workers.md) | Site estático e funções na borda |
| R2 e extras | [docs/09-r2-email-routing-e-extras.md](docs/09-r2-email-routing-e-extras.md) | Armazenamento, Email Routing, redirects, limites do proxy |
| IaC | [docs/10-cloudflare-com-iac.md](docs/10-cloudflare-com-iac.md) | Provider do OpenTofu, token de escopo mínimo |

## Checklist

- [ ] SSL/TLS em Full (strict), com certificado válido na origem (painel SSL/TLS; `curl -vI https://dominio`).
- [ ] Always Use HTTPS ligado; HSTS ligado só depois de todos os subdomínios terem HTTPS.
- [ ] MX, SSH e registros não HTTP em modo só DNS (cinza).
- [ ] Nenhuma página autenticada ou resposta com `Set-Cookie` em cache (testar o cabeçalho `cf-cache-status` logado).
- [ ] WAF ligado e regra protegendo `/admin` ou o painel.
- [ ] Rate limit na rota de login e Turnstile nos formulários públicos.
- [ ] Origem fechada: Tunnel ou firewall aceitando só as faixas de IP da Cloudflare (testar acesso direto ao IP).
- [ ] Painéis internos (Coolify, Grafana, staging) atrás do Access.
- [ ] Aplicação e nginx leem o IP real (`CF-Connecting-IP`), não o IP da Cloudflare.
- [ ] Token de API com escopo mínimo, guardado como segredo; DNS e regras em IaC a partir do segundo ambiente.

## Regras de uso

- **Nunca SSL Flexible.** Ele deixa o trecho Cloudflare → servidor sem criptografia e causa redirecionamento infinito. Use Full (strict).
- **Cache só do que é público.** Página logada em cache mostra os dados de um usuário para outro.
- **Feche a origem.** Cloudflare na frente não protege se o IP do servidor continua aberto para todos.
- **HSTS por último.** Ligado antes da hora, trava o acesso a subdomínios ainda sem HTTPS por meses.
- **Confira os limites do plano** (upload, timeout, número de regras) antes de prometer algo ao usuário; eles estão no doc 09 e na página oficial.
- **Uma pessoa não é o único admin.** A conta tem 2FA e pelo menos dois administradores; o cliente tem acesso.
- **Fronteiras.** Registro do domínio é da `domains`; servidor da `vps` e da `nginx`; regras de permissão e rate limit dentro da aplicação são da `security`; IaC geral é da `infra`.

## Quando a lista não cobre

Load Balancing pago, Argo, Spectrum, Magic Transit, Zero Trust corporativo avançado (Gateway, WARP para a empresa toda), Workers com Durable Objects e D1 em produção e contratos Enterprise ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial.

## Validade dos dados

Limites, planos e versões (provider do OpenTofu, cotas do Free) foram conferidos em 2026-11-25 em developers.cloudflare.com. Cada documento tem a linha "Verificado em"; a Cloudflare muda o painel e os limites com frequência, confira antes de afirmar.
