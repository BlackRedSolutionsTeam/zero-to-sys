---
name: admin-panel
description: 'Guia o painel administrativo do sistema (backoffice da equipe): usuários, empresas, assinaturas, papéis internos, impersonação, auditoria, feature flags e telas de suporte. Use quando pedirem "painel admin", "backoffice", "entrar como cliente" ou gerir o sistema sem mexer no banco.'
---

# admin-panel

Guia para incluir no sistema que você está criando o **painel administrativo**: a área interna em que a equipe gerencia usuários, empresas, assinaturas, configurações, filas, logs e suporte sem abrir o banco. Vale para qualquer stack. O painel entra no **backlog do sistema** desde o início: sem ele, a equipe passa a usar SQL manual, sem papel nem auditoria. Distinta do layout de CRUD (`design-systems`, doc 03) e do modelo geral de papéis (`security`) e de auditoria (`data`): esta skill diz o que o painel precisa fazer, quem acessa, com que limites e como as ações ficam registradas.

## Quando o painel entra no backlog

| Fase | O que entra | Gatilho |
|---|---|---|
| MVP do sistema | Busca de usuário e empresa, ficha, bloquear, papéis (suporte e super admin), 2FA, auditoria | Antes do primeiro cliente pagante |
| Primeiros clientes | Assinaturas e cobranças, reprocessar jobs e webhooks, somente leitura, dupla aprovação | Primeira cobrança em produção |
| Crescimento | Feature flags, configurações, logs e saúde, métricas, exportação controlada | Equipe com mais de 3 pessoas ou mais de 50 clientes |

## Roteiro de construção

Passo a passo completo, com exemplos em Next.js, ASP.NET Core, Laravel e Django, modelo de tabelas de papéis e de auditoria e checklist: [doc 13](docs/13-roteiro-de-construcao-por-stack.md).

1. **Escopo do MVP do painel** a partir do produto ([doc 02](docs/02-o-que-um-painel-precisa-ter.md)). Pronto quando: lista de perguntas do suporte e ações só de dev está no backlog.
2. **Construir, gerar ou comprar** ([doc 01](docs/01-construir-comprar-ou-gerar.md)). Pronto quando: opção escolhida e custo por pessoa calculado.
3. **Papéis internos e autenticação forte** ([doc 03](docs/03-quem-acessa-papeis-e-menor-privilegio.md), [doc 04](docs/04-autenticacao-forte-do-painel.md)). Pronto quando: equipe em tabela própria e 2FA obrigatório.
4. **Estrutura de pastas e rotas, painel separado do produto** ([doc 11](docs/11-painel-separado-do-produto.md), skill `architecture`). Pronto quando: subdomínio e guard de equipe definidos.
5. **Telas mínimas primeiro** ([doc 10](docs/10-telas-operacionais.md)): busca global, ficha do cliente, ações de suporte. Pronto quando: o suporte resolve os 10 casos mais comuns sem o dev.
6. **Auditoria desde a primeira ação** ([doc 06](docs/06-auditoria-do-que-a-equipe-faz.md)). Pronto quando: tabela só de inserção e teste que falha se faltar registro.
7. **Ações perigosas, impersonação e dados pessoais** ([doc 07](docs/07-acoes-perigosas.md), [doc 05](docs/05-impersonacao-entrar-como-cliente.md), [doc 08](docs/08-dados-pessoais-no-painel.md)). Pronto quando: confirmação, limite de lote, banner e máscara no servidor.
8. **Testes de permissão** (skill `quality`). Pronto quando: negação por papel e por empresa passa no CI.
9. **Deploy isolado e proteção na borda** (skills `cloudflare` e `infra`). Pronto quando: Access na frente, `noindex`, cookie separado.

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Construir, comprar ou gerar | [docs/01-construir-comprar-ou-gerar.md](docs/01-construir-comprar-ou-gerar.md) | Comparação com licença e preço |
| O que um painel precisa ter | [docs/02-o-que-um-painel-precisa-ter.md](docs/02-o-que-um-painel-precisa-ter.md) | Módulos e fases |
| Quem acessa | [docs/03-quem-acessa-papeis-e-menor-privilegio.md](docs/03-quem-acessa-papeis-e-menor-privilegio.md) | Papéis e dupla aprovação |
| Autenticação forte | [docs/04-autenticacao-forte-do-painel.md](docs/04-autenticacao-forte-do-painel.md) | 2FA, SSO, Access, sessão |
| Impersonação | [docs/05-impersonacao-entrar-como-cliente.md](docs/05-impersonacao-entrar-como-cliente.md) | Entrar como cliente com trava |
| Auditoria | [docs/06-auditoria-do-que-a-equipe-faz.md](docs/06-auditoria-do-que-a-equipe-faz.md) | Tabela imutável |
| Ações perigosas | [docs/07-acoes-perigosas.md](docs/07-acoes-perigosas.md) | Confirmação, lote, reversão |
| Dados pessoais | [docs/08-dados-pessoais-no-painel.md](docs/08-dados-pessoais-no-painel.md) | Máscara e exportação |
| Multiempresa | [docs/09-multiempresa-visao-da-equipe.md](docs/09-multiempresa-visao-da-equipe.md) | Visão da equipe |
| Telas operacionais | [docs/10-telas-operacionais.md](docs/10-telas-operacionais.md) | Busca, fila, cobrança |
| Painel separado | [docs/11-painel-separado-do-produto.md](docs/11-painel-separado-do-produto.md) | Subdomínio e borda |
| Métricas internas | [docs/12-metricas-internas-sem-virar-bi.md](docs/12-metricas-internas-sem-virar-bi.md) | MRR, churn, ativação |
| Roteiro por stack | [docs/13-roteiro-de-construcao-por-stack.md](docs/13-roteiro-de-construcao-por-stack.md) | 9 passos com exemplos |

## Checklist

- [ ] Painel no backlog do sistema, com MVP e fases.
- [ ] Equipe em tabela própria, papéis mínimos, 2FA obrigatório.
- [ ] Painel em subdomínio próprio atrás de Access ou Tunnel.
- [ ] Toda escrita grava auditoria imutável com motivo e ator real.
- [ ] Ações perigosas com confirmação, limite de lote e modo somente leitura.
- [ ] Impersonação com banner, tempo limitado e aviso ao cliente.
- [ ] Dados pessoais mascarados no servidor; exportação com limite e registro.
- [ ] Testes de permissão por papel e por empresa no CI.

## Regras de uso

- **Painel é backlog, não luxo.** Planeje junto com o produto.
- **Ação com nome, não edição de tabela.** "Reembolsar", "reprocessar".
- **Servidor decide.** Esconder botão não protege.
- **Preço e licença só conferidos**, com a data; no que não deu para conferir, diga ao usuário.
- **Fronteiras.** Papéis gerais e 2FA são da `security`; auditoria, soft delete, multiempresa e LGPD da `data`; base legal da `legal`; layout da `design-systems`; suporte e incidentes da `operations`; webhooks e filas da `integrations`; Access da `cloudflare`; testes da `quality`.

## Quando a lista não cobre

BI completo, painel de cliente final, portal de parceiros e CMS editorial ficam fora. Diga isso ao usuário.

## Validade dos dados

Preços, licenças e versões foram conferidos em 2026-11-25 nas páginas oficiais; cada doc tem a linha "Verificado em" e marca o que não foi conferido (licença do Appsmith, versões do AdminJS e Rails Admin, regra de receita do Directus).
