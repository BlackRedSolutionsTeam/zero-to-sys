# infra

Skill para o Claude Code que escolhe e monta a infraestrutura de um projeto, do zero até produção, de forma escalável e segura. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por tópico ([docs/](docs/)), explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e por quê.

## Tópicos cobertos

Só entrou o que passa em três critérios: ser a escolha mais sólida da camada, ter versão grátis ou barata para começar e escalar sem trocar de base.

| Tópico | Papel | Documento |
|---|---|---|
| PaaS | Vercel, Railway, Render e Fly.io: subir sem administrar servidor | [docs/01-paas.md](docs/01-paas.md) |
| VPS com painel | Coolify e Dokploy em servidor próprio | [docs/02-vps-coolify-dokploy.md](docs/02-vps-coolify-dokploy.md) |
| Nuvem grande | AWS, GCP e Azure | [docs/03-nuvem-grande.md](docs/03-nuvem-grande.md) |
| Contêineres | Docker e quando Kubernetes vale | [docs/04-docker-kubernetes.md](docs/04-docker-kubernetes.md) |
| Postgres gerenciado | Neon, Supabase e RDS | [docs/05-postgres-gerenciado.md](docs/05-postgres-gerenciado.md) |
| IaC | OpenTofu, Terraform e Pulumi | [docs/06-iac-opentofu-pulumi.md](docs/06-iac-opentofu-pulumi.md) |
| CI/CD | GitHub Actions | [docs/07-github-actions.md](docs/07-github-actions.md) |
| Borda | Cloudflare: DNS, CDN, WAF | [docs/08-cloudflare.md](docs/08-cloudflare.md) |
| Segredos | Variáveis, chaves e senhas fora do código | [docs/09-segredos-e-configuracao.md](docs/09-segredos-e-configuracao.md) |
| Observabilidade | OpenTelemetry, Grafana e Sentry | [docs/10-observabilidade.md](docs/10-observabilidade.md) |
| Backup | Cópias, restauração testada, RPO e RTO | [docs/11-backup-e-recuperacao.md](docs/11-backup-e-recuperacao.md) |
| Segurança | Menor privilégio, rede, TLS e dependências | [docs/12-seguranca-base.md](docs/12-seguranca-base.md) |

O [docs/README.md](docs/README.md) tem o índice, um guia "Qual escolher" e a lista do que foi avaliado e saiu, com o motivo.

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/infra ~/.claude/skills/infra
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é hospedar, fazer deploy, montar pipeline, escolher banco gerenciado, configurar backup ou monitoramento. Também dá para chamar direto com `/infra`. Exemplos:

- "Onde hospedo esse SaaS que acabou de ter os primeiros clientes?"
- "Monta o deploy automático com GitHub Actions e um Postgres gerenciado."
- "/infra revisa a segurança básica da infra deste projeto."

Com a skill carregada, o Claude:

1. identifica o porte do projeto, quem opera a infra e o orçamento;
2. escolhe a combinação pela tabela do [SKILL.md](SKILL.md);
3. lê o documento de cada item escolhido antes de criar qualquer recurso;
4. monta a infra seguindo as regras de uso (começar simples, tudo em código, segredo fora do repositório, backup testado);
5. explica a escolha em uma ou duas frases, com o custo estimado.

## Estrutura

```
infra/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md                       índice, "Qual escolher" e o que saiu da lista
    ├── 01-paas.md
    ├── 02-vps-coolify-dokploy.md
    ├── 03-nuvem-grande.md
    ├── 04-docker-kubernetes.md
    ├── 05-postgres-gerenciado.md
    ├── 06-iac-opentofu-pulumi.md
    ├── 07-github-actions.md
    ├── 08-cloudflare.md
    ├── 09-segredos-e-configuracao.md
    ├── 10-observabilidade.md
    ├── 11-backup-e-recuperacao.md
    └── 12-seguranca-base.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos, e registre o motivo em `docs/README.md`.
- **Revisar dados:** preços, licenças e números foram verificados em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar. Preços de nuvem e de PaaS mudam com frequência.
