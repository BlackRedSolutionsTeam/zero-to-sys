# Onde registrar o que foi decidido

> Cada decisão de produto vai para um arquivo do repositório, com um lugar só para cada coisa, para que pessoas e agentes de IA leiam a mesma fonte.

| | |
|---|---|
| **Referência** | docs.github.com (GitHub Issues e Projects); agents.md e code.claude.com/docs/en/memory (arquivos de instruções); linear.app e atlassian.com/software/jira (ferramentas externas) |
| **Categoria** | Produto |
| **Tipo** | Prática de documentação |
| **Vale para** | Qualquer projeto com repositório Git, com ou sem agente de IA |
| **Verificado em** | 2026-11-24 |

## O que é

É decidir, antes de escrever, onde cada tipo de informação mora. O `README` diz o que o sistema faz e para quem. O `BACKLOG.md` guarda itens, histórias, critérios de aceite e status. O `docs/regras-de-negocio.md` guarda regras e máquinas de estado (os estados de algo e as passagens permitidas, como pedido: novo, pago, enviado). O `CLAUDE.md` ou `AGENTS.md` só aponta para esses arquivos.

Tudo fica versionado no Git. Quem abre o repositório, humano ou agente, acha a mesma coisa no mesmo lugar.

## Por que usar

- **O agente lê o repositório, não a sua cabeça:** o que não está escrito ele inventa.
- **Uma fonte por assunto:** sem cópias que divergem.
- **Histórico de graça:** o Git mostra quando e por que uma regra mudou.
- **Entrada rápida:** pessoa nova entende o sistema em minutos.

## Quando usar

- Ao fechar o escopo do MVP, antes de começar a construir.
- Quando o cliente decide algo na conversa: grave no mesmo dia.
- Quando um agente de IA vai trabalhar no projeto.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site/landing | 🟡 Serve | Basta o `README` e uma lista curta de páginas |
| MVP de SaaS | ✅ Ótimo | `BACKLOG.md` e regras no repositório bastam no começo |
| SaaS em crescimento | ✅ Ótimo | Regras no repositório; itens migram para issues ou ferramenta externa |
| Sistema interno | ✅ Ótimo | Regras do negócio costumam ser a parte mais valiosa |
| API/integração | ✅ Ótimo | Regras e estados evitam divergência entre quem consome e quem fornece |
| App mobile | 🟡 Serve | Registre também o que muda entre versões publicadas |
| Time grande com vários squads | ❌ Evite só `BACKLOG.md` | Use issues ou ferramenta externa para itens; regras ficam no repositório |

## Quando é bom

- **Regras no repositório:** mudam no mesmo PR do código.
- **`BACKLOG.md` em projeto pequeno:** o agente lê e edita sem integração.
- **Issues do GitHub:** gratuitas, ligadas a PRs, com quadro no GitHub Projects.
- **Ferramenta externa (Linear, Jira):** boa quando há várias pessoas, filtros, relatórios e clientes acompanhando.

## Quando é ruim

- **Documento de planejamento solto** (Notion, Google Docs, planilha) que ninguém relê: fica velho em uma semana.
- **Mesma informação em três lugares:** quando muda, só um é atualizado.
- **`CLAUDE.md` copiando o conteúdo:** engorda o arquivo e diverge do original.
- **Status que não muda:** item entregue ainda aparece como "a fazer".
- **Backlog gigante em um arquivo só:** passa de umas poucas dezenas de itens, migre para issues.

## Como começar

O que vai onde:

| O que | Onde | Quem lê |
|---|---|---|
| O que o sistema faz e para quem (poucas linhas) | `README.md` | Todos |
| Itens, histórias, critérios de aceite, status | `BACKLOG.md` ou issues | Time e agente |
| Regras de negócio e máquinas de estado | `docs/regras-de-negocio.md` | Time e agente |
| Stack, pastas, hospedagem | `ARCHITECTURE.md` | Time e agente |
| Comandos, armadilhas e ponteiros | `CLAUDE.md` / `AGENTS.md` | Agente |

Qual lugar para os itens:

| Situação | Use |
|---|---|
| Uma pessoa ou dupla, MVP pequeno | `BACKLOG.md` |
| Time pequeno que já usa GitHub | GitHub Issues e Projects |
| Vários times, relatórios, cliente acompanhando | Linear ou Jira (confira planos e preços nos sites) |

Árvore sugerida:

```text
.
├── README.md
├── BACKLOG.md
├── ARCHITECTURE.md
├── CLAUDE.md
└── docs/
    └── regras-de-negocio.md
```

Modelo de item no `BACKLOG.md`:

```markdown
## B-003 Cliente cancela agendamento
- Status: a fazer | em andamento | feito
- História: Como cliente, quero cancelar um agendamento, para liberar o horário.
- Critérios de aceite:
  - Dado um agendamento futuro, quando o cliente cancela, então o horário fica livre.
  - Dado um agendamento a menos de 2h, quando o cliente cancela, então o sistema recusa.
- Regras: ver "Cancelamento" em docs/regras-de-negocio.md
```

Trecho do `CLAUDE.md` (só ponteiros):

```markdown
## Produto
- O que o sistema faz: README.md
- O que construir e em que ordem: BACKLOG.md (atualize o status no mesmo PR que entrega o item)
- Regras de negócio e estados: docs/regras-de-negocio.md (leia antes de mexer em cadastro, cobrança ou cancelamento)
- Não crie documento de planejamento novo; registre nesses arquivos.
```

Rotina: o PR que entrega o item muda o status dele. Se a regra mudou, o mesmo PR muda `docs/regras-de-negocio.md`.

## Combina com / alternativas

- [Histórias e critérios de aceite](04-historias-e-criterios-de-aceite.md): o formato de cada item.
- [Regras de negócio](05-regras-de-negocio.md): o conteúdo de `docs/regras-de-negocio.md`.
- [Backlog e ordem de construção](06-backlog-e-ordem-de-construcao.md): como ordenar os itens.
- [Escopo do MVP](02-escopo-do-mvp.md): o que entra no `README` e no backlog.
- Para o `CLAUDE.md`/`AGENTS.md`, veja a skill `ia`: [CLAUDE.md e AGENTS.md](../../ia/docs/01-claude-md-agents-md.md).
- Alternativas: GitHub Issues e Projects, Linear, Jira, Notion (só se o time realmente relê e mantém).

## Decisão rápida

- **Use se:** o projeto terá mais de uma sessão de trabalho, mais de uma pessoa ou um agente de IA.
- **Evite se:** é um experimento descartável de uma tarde, em que um `README` curto basta.
