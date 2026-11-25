# nginx

Skill para o Claude Code que configura o nginx como proxy reverso e servidor web: instalação, proxy para a aplicação, HTTPS com Let's Encrypt, IP real atrás da Cloudflare, estáticos e cache, WebSocket e uploads, limites e hardening, logs e diagnóstico, Docker e as correções de segurança vigentes. Ela reúne um guia ([SKILL.md](SKILL.md)) e um documento por tópico ([docs/](docs/)).

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| nginx, Caddy ou Traefik | Quando usar cada um | [docs/01-nginx-caddy-ou-traefik.md](docs/01-nginx-caddy-ou-traefik.md) |
| Instalação | Repositório oficial, estrutura, nginx -t | [docs/02-instalacao-e-estrutura.md](docs/02-instalacao-e-estrutura.md) |
| Proxy reverso | Repassar para a aplicação | [docs/03-proxy-reverso-para-a-aplicacao.md](docs/03-proxy-reverso-para-a-aplicacao.md) |
| HTTPS | Let's Encrypt, TLS, HSTS, HTTP/2 e 3 | [docs/04-https-com-letsencrypt.md](docs/04-https-com-letsencrypt.md) |
| Atrás da Cloudflare | IP real, origem fechada | [docs/05-atras-da-cloudflare.md](docs/05-atras-da-cloudflare.md) |
| Estáticos e cache | SPA, compressão, Cache-Control | [docs/06-estaticos-cache-e-compressao.md](docs/06-estaticos-cache-e-compressao.md) |
| WebSocket, SSE e uploads | Conexões longas e arquivos grandes | [docs/07-websocket-sse-e-uploads.md](docs/07-websocket-sse-e-uploads.md) |
| Limites e hardening | limit_req, headers, arquivos ocultos | [docs/08-limites-headers-e-hardening.md](docs/08-limites-headers-e-hardening.md) |
| Logs e diagnóstico | 502, 504, 413 e outros | [docs/09-logs-e-diagnostico.md](docs/09-logs-e-diagnostico.md) |
| Docker e deploy sem queda | Contêiner, reload, blue/green | [docs/10-nginx-com-docker-e-deploy-sem-queda.md](docs/10-nginx-com-docker-e-deploy-sem-queda.md) |
| Correções de segurança | Avisos vigentes, CVEs e rotina de atualização | [docs/11-correcoes-de-seguranca-e-atualizacao.md](docs/11-correcoes-de-seguranca-e-atualizacao.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/nginx ~/.claude/skills/nginx
```

## Como usar

O Claude carrega a skill sozinho quando o pedido bate com o tema dela. Também dá para chamar direto com `/nginx`. Exemplos:

- "Configura o nginx na frente da API com HTTPS."
- "Está dando 502 Bad Gateway."
- "/nginx o meu nginx está vulnerável?"

Com a skill carregada, o Claude:

1. decide se nginx é a escolha certa (ou Caddy, Traefik, Tunnel);
2. instala pelo repositório oficial e organiza um arquivo por site;
3. configura proxy, HTTPS, IP real, limites e headers;
4. testa com `nginx -t` e confere o diagnóstico;
5. compara a versão com os avisos de segurança vigentes e confere o checklist.

## Estrutura

```
nginx/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md     índice e "Por onde começar"
    ├── 01-nginx-caddy-ou-traefik.md
    ├── 02-instalacao-e-estrutura.md
    ├── 03-proxy-reverso-para-a-aplicacao.md
    ├── 04-https-com-letsencrypt.md
    ├── 05-atras-da-cloudflare.md
    ├── 06-estaticos-cache-e-compressao.md
    ├── 07-websocket-sse-e-uploads.md
    ├── 08-limites-headers-e-hardening.md
    ├── 09-logs-e-diagnostico.md
    ├── 10-nginx-com-docker-e-deploy-sem-queda.md
    └── 11-correcoes-de-seguranca-e-atualizacao.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** Diretivas e avisos de segurança foram conferidos em 2026-11-25 em nginx.org. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
