---
name: infra
description: Escolhe e monta a infraestrutura de um projeto, do zero até produção, de forma escalável e segura (hospedagem PaaS, VPS com Coolify/Dokploy, nuvem grande, Docker e Kubernetes, Postgres gerenciado, OpenTofu/Pulumi, GitHub Actions, Cloudflare, segredos, observabilidade, backup e segurança básica). Use sempre que o usuário pedir para "colocar no ar", "fazer deploy", "onde hospedar", "montar a infra", "configurar CI/CD", "subir em produção", "escolher banco gerenciado", "configurar backup", "monitorar" ou "deixar seguro". Não decide linguagem ou framework (skill stacks), pastas (architecture) nem estilo de código (coding).
---

# infra

Guia de decisão para montar a infraestrutura de um projeto, do zero até produção, sem pagar por complexidade que ainda não é necessária. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, pontos fortes, limitações, comandos e decisão rápida.

## Como usar esta skill

1. **Descubra o porte e as restrições** antes de escolher qualquer coisa: fase do projeto (MVP, SaaS pequeno, em crescimento, corporativo, site estático), quem opera a infra (um dev ou um time), orçamento mensal, dados sensíveis ou exigências legais (LGPD, contrato com cliente) e o que já está rodando. O que já existe no projeto tem prioridade sobre esta lista.
2. **Escolha pela tabela abaixo.** Comece pela combinação mais simples do porte; só suba de nível quando houver um motivo concreto (carga, equipe, exigência de cliente).
3. **Leia o documento de cada item escolhido** em `docs/` antes de criar conta, escrever pipeline ou rodar comando. Confira principalmente "Para que tipo de projeto", "Quando é ruim" e "Como começar".
4. **Siga os comandos de "Como começar".** Confira a versão e o preço na fonte oficial antes de rodar.
5. **Aplique as regras de uso** desta skill.
6. **Explique a escolha ao usuário em uma ou duas frases**, com o custo mensal estimado e o que muda quando o projeto crescer.

## Qual combinação usar

| Projeto | Hospedagem | Dados | Entrega e código da infra | Operação |
|---|---|---|---|---|
| Site estático ou blog | Cloudflare (Pages) ou Vercel | Sem banco | GitHub Actions ou deploy direto do Git | Cloudflare na frente; uptime simples |
| MVP ou protótipo | PaaS (Vercel, Railway, Render ou Fly.io) | Postgres gerenciado no plano grátis ou de entrada (Neon ou Supabase) | Deploy pelo Git; GitHub Actions só com testes | Sentry grátis; backup do provedor |
| SaaS pequeno (primeiros clientes pagantes) | PaaS pago, ou um VPS com Coolify ou Dokploy se o dev já opera servidor | Postgres gerenciado pago, com backup diário e restauração testada | GitHub Actions; Docker; segredos no provedor | Sentry; OpenTelemetry quando houver mais de um serviço; Cloudflare na frente |
| SaaS em crescimento | PaaS maior ou nuvem grande (AWS, GCP, Azure) com contêineres gerenciados | RDS ou equivalente, com réplica e recuperação por ponto no tempo | OpenTofu ou Pulumi no Git; GitHub Actions com ambientes | OpenTelemetry com Grafana; gerenciador de segredos; Cloudflare WAF |
| Sistema corporativo | Nuvem grande, na nuvem que a empresa já contrata | Banco gerenciado da nuvem, com rede privada e criptografia | OpenTofu ou Pulumi; pipeline com aprovação; Kubernetes só se houver time para operar | Observabilidade completa, auditoria, backup em outra região |

| Tópico | Documento | Papel |
|---|---|---|
| PaaS | [docs/01-paas.md](docs/01-paas.md) | Vercel, Railway, Render e Fly.io: subir sem administrar servidor |
| VPS com painel | [docs/02-vps-coolify-dokploy.md](docs/02-vps-coolify-dokploy.md) | Servidor próprio com deploy estilo PaaS |
| Nuvem grande | [docs/03-nuvem-grande.md](docs/03-nuvem-grande.md) | AWS, GCP e Azure: quando compensam |
| Contêineres | [docs/04-docker-kubernetes.md](docs/04-docker-kubernetes.md) | Docker como padrão; Kubernetes só quando vale |
| Postgres gerenciado | [docs/05-postgres-gerenciado.md](docs/05-postgres-gerenciado.md) | Neon, Supabase e RDS |
| IaC | [docs/06-iac-opentofu-pulumi.md](docs/06-iac-opentofu-pulumi.md) | Infra descrita em código |
| CI/CD | [docs/07-github-actions.md](docs/07-github-actions.md) | Testes e deploy automáticos |
| Borda | [docs/08-cloudflare.md](docs/08-cloudflare.md) | DNS, CDN, WAF e proteção contra DDoS |
| Segredos | [docs/09-segredos-e-configuracao.md](docs/09-segredos-e-configuracao.md) | Variáveis, chaves e senhas fora do código |
| Observabilidade | [docs/10-observabilidade.md](docs/10-observabilidade.md) | OpenTelemetry, Grafana e Sentry |
| Backup | [docs/11-backup-e-recuperacao.md](docs/11-backup-e-recuperacao.md) | Cópias, restauração testada e metas de recuperação |
| Segurança | [docs/12-seguranca-base.md](docs/12-seguranca-base.md) | Menor privilégio, rede, TLS e dependências |

## Regras de uso

- **Comece pelo mais simples que aguenta o porte.** Kubernetes, multi-região e microsserviços não são ponto de partida. Cada camada a mais precisa de alguém para operá-la.
- **Tudo reproduzível.** Infra criada só no painel não se recupera nem se revisa. Do SaaS pequeno em diante, descreva em código (OpenTofu ou Pulumi) ou ao menos em Dockerfile e pipeline versionados.
- **Segredo nunca no repositório.** Nem em `.env` commitado, nem em imagem Docker, nem em log. Veja o doc 09.
- **Backup só vale se a restauração foi testada.** Teste restaurar em ambiente separado antes do primeiro cliente pagante.
- **Plano grátis é para validar, não para operar.** Vários grátis dormem, expiram ou não têm backup (Render, Supabase). Migre para plano pago antes de ter usuário real.
- **Menor privilégio e HTTPS em tudo.** Chaves com o mínimo de permissão, banco sem IP público aberto, TLS em toda borda.
- **Um ambiente de homologação** a partir do SaaS pequeno. Nunca teste migração de banco direto em produção.
- **Defina alerta antes de precisar.** Erro, indisponibilidade e custo mensal fora do normal geram aviso, não descoberta tardia.
- **Cuidado com custo variável.** Plataformas cobradas por uso (Vercel, Railway, Fly.io, Neon) pedem limite de gasto e alerta de orçamento.
- **Fronteiras.** Escolha de linguagem e framework é da skill stacks, organização de pastas da architecture e estilo de código da coding. Esta skill cuida de onde e como o sistema roda.

## Quando a lista não cobre

Se o projeto pede algo fora destes doze tópicos (mensageria, filas, busca, data warehouse, edge computing avançado, requisitos regulatórios como PCI ou HIPAA, multi-região ativa), diga isso ao usuário em vez de forçar um deles. O `docs/README.md` registra o que foi avaliado e saiu da lista, com o motivo.

## Validade dos dados

Preços, planos, licenças e versões dos documentos foram verificados em 2026-11-24. Preço de nuvem muda com frequência: antes de afirmar um valor ao usuário, confira no site oficial se a informação for decisiva.
