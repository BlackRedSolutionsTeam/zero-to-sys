# Nuvem grande (AWS, GCP e Azure)

> Os três grandes provedores de nuvem: catálogo enorme, rede privada, conformidade e escala, ao custo de mais complexidade e conta variável.

| | |
|---|---|
| **Site** | https://aws.amazon.com, https://cloud.google.com, https://azure.microsoft.com |
| **Categoria** | Hospedagem |
| **Tipo** | Nuvem pública (IaaS e serviços gerenciados) |
| **Stack** | Qualquer; contêineres gerenciados, máquinas virtuais, funções e bancos gerenciados |
| **Preço** | Pago por uso. AWS: conta nova ganha até US$ 200 em créditos (US$ 100 ao abrir e até US$ 100 ao explorar serviços); o plano grátis encerra em 6 meses ou ao acabar o crédito. Cloud Run (us-central1, cobrança por requisição): US$ 0,000024 por vCPU-segundo, US$ 0,0000025 por GiB-segundo e US$ 0,40 por milhão de requisições, com 2 milhões de requisições, 180.000 vCPU-s e 360.000 GiB-s grátis por mês. Azure Container Apps (plano de consumo, East US): US$ 0,000024 por vCPU-segundo ativo, US$ 0,000003 por GiB-segundo ativo e US$ 0,40 por milhão de requisições, com os mesmos valores grátis por mês (páginas de preços e API de preços do Azure, conferido em 2026-11-24) |
| **Licença** | Serviços proprietários |
| **Verificado em** | 2026-11-24 |

## O que é

São plataformas com centenas de serviços: máquinas, contêineres, bancos, filas, armazenamento, rede privada, identidade e auditoria. A AWS é a maior. GCP e Azure competem, e o Azure costuma pesar mais em empresas que já usam produtos Microsoft.

Para um projeto novo, o caminho mais enxuto é usar poucos serviços: contêineres gerenciados (ECS Fargate, Cloud Run ou Azure Container Apps), um banco gerenciado, armazenamento de objetos e um balanceador. Cloud Run e Azure Container Apps constam nas páginas de preços oficiais (conferido em 2026-11-24); o ECS Fargate custa, em us-east-1, US$ 0,04048 por vCPU-hora e US$ 0,004445 por GB-hora no Linux/x86 (tabela pública de preços da AWS, conferido em 2026-11-24).

## Por que usar

- **Escala e alcance:** muitas regiões e capacidade para crescer sem trocar de base.
- **Rede privada e identidade:** controle fino de quem acessa o quê.
- **Conformidade e auditoria:** certificações e registros que clientes corporativos pedem.
- **Serviços gerenciados:** banco, filas e cache sem operar servidor.
- **Contratos e suporte** pagos quando o negócio exige.

## Quando usar

- SaaS em crescimento que passou dos limites de PaaS ou VPS.
- Sistema corporativo, ou cliente que exige a nuvem dele.
- Exigência de região específica, rede privada ou auditoria.
- Time com pelo menos uma pessoa que domine a nuvem escolhida.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ❌ Evite | Cloudflare ou Vercel são mais simples e baratos |
| MVP / protótipo | ❌ Evite | Complexidade e risco de conta surpresa sem ganho |
| SaaS pequeno | 🟡 Serve | Só se já houver conhecimento; PaaS ou VPS rendem mais |
| SaaS em crescimento | ✅ Ótimo | Contêineres gerenciados, banco, rede e métricas no mesmo lugar |
| Sistema corporativo | ✅ Ótimo | Rede privada, identidade, auditoria e contrato |
| Carga com picos | ✅ Ótimo | Escala automática e funções para trabalhos pontuais |
| Time sem experiência em nuvem | ❌ Evite | Erro de configuração vira falha de segurança ou custo alto |
| Projeto com orçamento fixo e rígido | 🟡 Serve | Exige alertas de orçamento; a cobrança é por uso |

## Quando é bom

- **Catálogo completo:** quase tudo que o sistema precisar existe pronto.
- **Controle de acesso detalhado:** papéis e políticas por recurso.
- **Evolui com o projeto:** a mesma conta serve do pequeno ao grande.
- **Muita documentação e profissionais no mercado.**

## Quando é ruim

- **Complexidade:** o catálogo grande leva a escolhas demais e erros de configuração.
- **Custo imprevisível:** tráfego de saída, NAT e logs geram cobranças que surpreendem. Ative orçamento e alerta no primeiro dia.
- **Créditos acabam:** na AWS, o plano grátis fecha em 6 meses ou ao esgotar o crédito.
- **Lock-in:** serviços proprietários dificultam sair. Mitigação: contêineres e Postgres padrão.
- **Serverless puro como base:** acopla o código à plataforma e dificulta teste local; use para tarefas pontuais, não como arquitetura de tudo.
- **Segurança é responsabilidade compartilhada:** bucket aberto ou chave exposta é erro seu.

## Como começar

Antes de criar qualquer recurso:

1. Crie a conta com MFA no usuário raiz e guarde o raiz fora do uso diário.
2. Crie usuários ou papéis com o mínimo de permissão (veja [segurança base](12-seguranca-base.md)).
3. Configure orçamento mensal com alerta por e-mail.
4. Descreva a infra em código com [OpenTofu ou Pulumi](06-iac-opentofu-pulumi.md), não no clique.

Exemplo com a AWS CLI (comando da CLI oficial; confira a versão instalada):

```bash
aws sts get-caller-identity
```

## Combina com / alternativas

- [Docker e Kubernetes](04-docker-kubernetes.md): contêineres como unidade de deploy.
- [Postgres gerenciado](05-postgres-gerenciado.md): RDS ou equivalente.
- [Cloudflare](08-cloudflare.md): CDN e WAF na frente.
- Alternativas: [PaaS](01-paas.md) e [VPS](02-vps-coolify-dokploy.md) para projetos menores.

## Decisão rápida

- **Use se:** o projeto já é grande, há exigência de rede privada, auditoria ou nuvem específica, e existe quem a opere.
- **Evite se:** é MVP ou projeto pequeno, ninguém no time conhece a nuvem escolhida, ou não há como acompanhar o custo.
