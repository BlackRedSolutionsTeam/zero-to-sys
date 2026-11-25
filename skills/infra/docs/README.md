# Infraestrutura

Um documento por tópico, explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e por quê. A lista ficou só com o que passa em três critérios: ser a escolha mais sólida da camada, ter versão grátis ou barata para começar e escalar sem trocar de base. Preços, licenças e números foram verificados nos sites oficiais em 2026-11-24; o que não tem fonte oficial está dito no texto.

## Onde rodar

| Tópico | O que é | Custo para começar | Doc |
|---|---|---|---|
| PaaS | Vercel, Railway, Render e Fly.io: você envia o código, a plataforma roda | Grátis ou de US$ 5 a US$ 20 por mês, conforme a plataforma | [01-paas.md](01-paas.md) |
| VPS com painel | Coolify e Dokploy: deploy estilo PaaS no seu servidor | Software grátis (open source), mais o servidor (Hetzner a partir de € 5,49) | [02-vps-coolify-dokploy.md](02-vps-coolify-dokploy.md) |
| Nuvem grande | AWS, GCP e Azure | Créditos para conta nova; depois, pago por uso | [03-nuvem-grande.md](03-nuvem-grande.md) |
| Contêineres | Docker como padrão; Kubernetes só quando vale | Docker grátis; Kubernetes gerenciado tem custo fixo | [04-docker-kubernetes.md](04-docker-kubernetes.md) |

## Dados, código da infra e entrega

| Tópico | O que é | Custo para começar | Doc |
|---|---|---|---|
| Postgres gerenciado | Neon, Supabase e RDS | Neon e Supabase têm plano grátis; Supabase Pro a partir de US$ 25 | [05-postgres-gerenciado.md](05-postgres-gerenciado.md) |
| IaC | OpenTofu, Terraform e Pulumi | OpenTofu grátis; Pulumi individual grátis | [06-iac-opentofu-pulumi.md](06-iac-opentofu-pulumi.md) |
| CI/CD | GitHub Actions | Grátis em repositório público; minutos incluídos em privado | [07-github-actions.md](07-github-actions.md) |

## Proteção e operação

| Tópico | O que é | Custo para começar | Doc |
|---|---|---|---|
| Cloudflare | DNS, CDN, WAF e DDoS na frente do sistema | WAF e DDoS incluídos no plano grátis | [08-cloudflare.md](08-cloudflare.md) |
| Segredos | Onde guardar chaves e senhas | Do grátis do provedor a ferramentas dedicadas | [09-segredos-e-configuracao.md](09-segredos-e-configuracao.md) |
| Observabilidade | OpenTelemetry, Grafana e Sentry | Planos grátis nos dois serviços | [10-observabilidade.md](10-observabilidade.md) |
| Backup | Cópias, restauração testada, RPO e RTO | Incluído em parte dos bancos gerenciados | [11-backup-e-recuperacao.md](11-backup-e-recuperacao.md) |
| Segurança | Base mínima de segurança | Prática, sem licença | [12-seguranca-base.md](12-seguranca-base.md) |
| Analytics | Medir o uso do produto (eventos, funil) | Plano grátis ou self-host, conforme a ferramenta | [13-analytics-de-produto.md](13-analytics-de-produto.md) |
| Feature flags | Liberar aos poucos e voltar atrás | Prática; serviços com plano grátis | [14-feature-flags-e-rollback.md](14-feature-flags-e-rollback.md) |

## Qual escolher

- **Site estático ou blog:** [Cloudflare](08-cloudflare.md) ou [Vercel](01-paas.md), sem banco e sem servidor.
- **MVP:** um [PaaS](01-paas.md) com [Postgres gerenciado](05-postgres-gerenciado.md) e [Sentry](10-observabilidade.md).
- **SaaS pequeno:** PaaS pago, ou VPS com [Coolify ou Dokploy](02-vps-coolify-dokploy.md) se já houver quem opere servidor; [GitHub Actions](07-github-actions.md); backup restaurado em teste.
- **SaaS em crescimento:** [nuvem grande](03-nuvem-grande.md) com contêineres gerenciados, [OpenTofu ou Pulumi](06-iac-opentofu-pulumi.md), [observabilidade](10-observabilidade.md) completa.
- **Sistema corporativo:** a nuvem que a empresa já contrata, com [segurança](12-seguranca-base.md) e [backup](11-backup-e-recuperacao.md) formalizados.
- **Quase todo projeto:** [Docker](04-docker-kubernetes.md), [GitHub Actions](07-github-actions.md), [segredos](09-segredos-e-configuracao.md) fora do código e [segurança base](12-seguranca-base.md).

## O que saiu da lista e por quê

| Tópico ou ferramenta | Motivo |
|---|---|
| Kubernetes como tópico próprio | Entrou dentro do doc 04 com a regra de quando vale; como ponto de partida é complexidade demais para a maioria |
| Heroku | Planos pagos a partir de US$ 5/mês (Eco, dorme após 30 min parado), Basic US$ 7 e Standard-1X US$ 25; sem plano grátis; Postgres Essential-0 a US$ 5/mês (heroku.com/pricing, conferido em 2026-11-24). Render e Railway cobrem o mesmo uso |
| Netlify | Cobre o mesmo caso de Vercel e Cloudflare Pages; plano Free sem prazo, limitado a 300 créditos; Personal US$ 9/mês e Pro US$ 20/mês (netlify.com/pricing, conferido em 2026-11-24) |
| DigitalOcean, Linode e Vultr | Bons VPS, mas o ponto do doc 02 é o painel (Coolify, Dokploy), que roda em qualquer um deles; menor servidor: DigitalOcean US$ 4/mês (512 MiB, 1 vCPU), Linode Nanode 1 GB US$ 5/mês, Vultr a partir de US$ 2,50/mês (0,5 GB), US$ 5 com 1 GB (páginas oficiais, conferido em 2026-11-24) |
| CapRover | Painel de deploy parecido com Coolify e Dokploy; menos recursos de equipe e previews; ainda mantido: último release v1.16.1 em 2026-11-18 (GitHub, conferido em 2026-11-24) |
| Terraform (HashiCorp) como padrão | Licença BSL 1.1 (LICENSE no GitHub, conferido em 2026-11-24) e OpenTofu faz o mesmo sob governança aberta; fica citado no doc 06 |
| Ansible | Útil para configurar servidores, mas contêineres e IaC cobrem a maioria dos casos novos; licença GPL-3.0 (GitHub, conferido em 2026-11-24) |
| GitLab CI, CircleCI, Jenkins | GitHub Actions é o padrão de fato para projetos no GitHub; os outros só valem se o código já estiver neles |
| Datadog, New Relic | Completos, mas caros e com cobrança por volume; Grafana e Sentry cobrem o começo; Datadog tem grátis até 5 hosts e Pro a partir de US$ 15 por host/mês; New Relic dá 100 GB/mês grátis e cobra US$ 0,40 por GB depois (conferido em 2026-11-24) |
| HashiCorp Vault | Poderoso, mas pesado de operar; ferramentas gerenciadas resolvem melhor para times pequenos |
| Redis, filas e busca gerenciados | Dependem do produto, não são camada base; entram quando o projeto exigir |
| Serverless puro (Lambda, Cloud Functions) | Bom para cargas de pico; como base de produto aumenta acoplamento e dificulta teste local; citado no doc 03 |
