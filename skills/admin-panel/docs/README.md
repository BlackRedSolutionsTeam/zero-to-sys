# Painel administrativo

Um documento por tópico, da decisão de construir até o deploy protegido. Preços, licenças e versões foram conferidos em 2026-11-25 nas fontes oficiais; o que não pôde ser conferido está marcado em cada doc.

## Decidir e planejar

| Prática | O que entrega | Doc |
|---|---|---|
| Construir, comprar ou gerar | Comparação com licença e preço | [01-construir-comprar-ou-gerar.md](01-construir-comprar-ou-gerar.md) |
| O que um painel precisa ter | Módulos e fases do MVP | [02-o-que-um-painel-precisa-ter.md](02-o-que-um-painel-precisa-ter.md) |
| Roteiro por stack | 9 passos, exemplos e checklist | [13-roteiro-de-construcao-por-stack.md](13-roteiro-de-construcao-por-stack.md) |

## Proteger o acesso

| Prática | O que entrega | Doc |
|---|---|---|
| Quem acessa | Papéis, menor privilégio, dupla aprovação | [03-quem-acessa-papeis-e-menor-privilegio.md](03-quem-acessa-papeis-e-menor-privilegio.md) |
| Autenticação forte | 2FA, SSO, Access, sessão curta | [04-autenticacao-forte-do-painel.md](04-autenticacao-forte-do-painel.md) |
| Painel separado | Subdomínio, deploy e borda | [11-painel-separado-do-produto.md](11-painel-separado-do-produto.md) |

## Agir com segurança

| Prática | O que entrega | Doc |
|---|---|---|
| Impersonação | Entrar como cliente com trava | [05-impersonacao-entrar-como-cliente.md](05-impersonacao-entrar-como-cliente.md) |
| Auditoria | Tabela imutável de ações | [06-auditoria-do-que-a-equipe-faz.md](06-auditoria-do-que-a-equipe-faz.md) |
| Ações perigosas | Confirmação, lote, reversão | [07-acoes-perigosas.md](07-acoes-perigosas.md) |
| Dados pessoais | Máscara e exportação | [08-dados-pessoais-no-painel.md](08-dados-pessoais-no-painel.md) |
| Multiempresa | Visão da equipe sem quebrar isolamento | [09-multiempresa-visao-da-equipe.md](09-multiempresa-visao-da-equipe.md) |

## Operar

| Prática | O que entrega | Doc |
|---|---|---|
| Telas operacionais | Busca, linha do tempo, filas, cobrança | [10-telas-operacionais.md](10-telas-operacionais.md) |
| Métricas internas | MRR, churn, ativação | [12-metricas-internas-sem-virar-bi.md](12-metricas-internas-sem-virar-bi.md) |

## Por onde começar

- **Sistema novo:** 02 → 13 (passos 1 a 6 no MVP).
- **Vai escolher ferramenta:** 01.
- **Painel já existe e precisa de segurança:** 03 → 04 → 06 → 05.
- **Vai mostrar dado de cliente:** 08 e 09.
