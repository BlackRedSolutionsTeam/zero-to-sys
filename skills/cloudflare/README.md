# cloudflare

Skill para o Claude Code que configura a Cloudflare na frente do sistema: DNS e proxy, SSL Full (strict), cache seguro, WAF e rate limit, Tunnel, Access para painéis internos, Pages, Workers, R2 e tudo em IaC. Ela reúne um guia ([SKILL.md](SKILL.md)) e um documento por tópico ([docs/](docs/)).

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Colocar o domínio | Conta, nameservers, plano Free | [docs/01-colocar-o-dominio-na-cloudflare.md](docs/01-colocar-o-dominio-na-cloudflare.md) |
| DNS e proxy | Laranja x cinza, IP real | [docs/02-dns-e-proxy.md](docs/02-dns-e-proxy.md) |
| SSL/TLS e HSTS | Full (strict), certificado de origem | [docs/03-ssl-tls-e-hsts.md](docs/03-ssl-tls-e-hsts.md) |
| Cache | Regras seguras, purge, nunca página logada | [docs/04-cache-e-performance.md](docs/04-cache-e-performance.md) |
| WAF, rate limit e bots | Regras, limites, Turnstile | [docs/05-waf-rate-limit-e-bots.md](docs/05-waf-rate-limit-e-bots.md) |
| Tunnel e origem | Publicar sem abrir porta, origem fechada | [docs/06-tunnel-e-protecao-da-origem.md](docs/06-tunnel-e-protecao-da-origem.md) |
| Access | Proteger painéis internos | [docs/07-access-e-zero-trust.md](docs/07-access-e-zero-trust.md) |
| Pages e Workers | Site estático e funções na borda | [docs/08-pages-e-workers.md](docs/08-pages-e-workers.md) |
| R2 e extras | R2, Email Routing, redirects | [docs/09-r2-email-routing-e-extras.md](docs/09-r2-email-routing-e-extras.md) |
| Cloudflare com IaC | DNS e regras em código | [docs/10-cloudflare-com-iac.md](docs/10-cloudflare-com-iac.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/cloudflare ~/.claude/skills/cloudflare
```

## Como usar

O Claude carrega a skill sozinho quando o pedido bate com o tema dela. Também dá para chamar direto com `/cloudflare`. Exemplos:

- "Coloca o domínio da clínica na Cloudflare com SSL e WAF."
- "Protege o painel do Coolify com login."
- "/cloudflare quero publicar o app sem abrir porta no servidor."

Com a skill carregada, o Claude:

1. coloca o domínio na Cloudflare e revisa os registros;
2. liga SSL Full (strict), HSTS e redirecionamento para HTTPS;
3. define cache seguro e regras de WAF e rate limit;
4. fecha a origem (Tunnel ou só IPs da Cloudflare) e protege painéis com Access;
5. leva DNS e regras para IaC e confere o checklist.

## Estrutura

```
cloudflare/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md     índice e "Por onde começar"
    ├── 01-colocar-o-dominio-na-cloudflare.md
    ├── 02-dns-e-proxy.md
    ├── 03-ssl-tls-e-hsts.md
    ├── 04-cache-e-performance.md
    ├── 05-waf-rate-limit-e-bots.md
    ├── 06-tunnel-e-protecao-da-origem.md
    ├── 07-access-e-zero-trust.md
    ├── 08-pages-e-workers.md
    ├── 09-r2-email-routing-e-extras.md
    └── 10-cloudflare-com-iac.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** Limites e planos foram conferidos em 2026-11-25 em developers.cloudflare.com. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
