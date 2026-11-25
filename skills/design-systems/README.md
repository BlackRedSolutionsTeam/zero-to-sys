# design-systems

Skill para o Claude Code com um catálogo de layouts por tipo de sistema. Cada tipo tem um documento ([docs/](docs/)) com a anatomia do layout, medidas, tokens, padrões essenciais e erros comuns, e um exemplo pronto ([examples/](examples/)): um HTML autocontido, com tema claro e escuro, para abrir no navegador e usar como referência. O guia de decisão está no [SKILL.md](SKILL.md).

Ela decide a estrutura e o visual da tela. Os componentes e ícones para montá-la vêm da skill [design](../design/).

## Layouts cobertos

| Layout | Para quê | Documento | Exemplo |
|---|---|---|---|
| Fundamentos | Regras de espaçamento, tipografia, cor e estados que valem para todos | [docs/01-fundamentos.md](docs/01-fundamentos.md) | — |
| Dashboard de análise | Indicadores, gráficos e itens recentes | [docs/02-dashboard-analytics.md](docs/02-dashboard-analytics.md) | [examples/02-dashboard-analytics.html](examples/02-dashboard-analytics.html) |
| Painel admin / CRUD | Tabela, filtros e formulário de cadastro | [docs/03-admin-crud.md](docs/03-admin-crud.md) | [examples/03-admin-crud.html](examples/03-admin-crud.html) |
| Login, onboarding e configurações | Telas de entrada e de conta | [docs/04-auth-onboarding-configuracoes.md](docs/04-auth-onboarding-configuracoes.md) | [examples/04-auth-onboarding-configuracoes.html](examples/04-auth-onboarding-configuracoes.html) |
| Landing page de SaaS | Página de venda de produto digital | [docs/05-landing-saas.md](docs/05-landing-saas.md) | [examples/05-landing-saas.html](examples/05-landing-saas.html) |
| E-commerce | Vitrine, produto e carrinho | [docs/06-ecommerce.md](docs/06-ecommerce.md) | [examples/06-ecommerce.html](examples/06-ecommerce.html) |
| CRM / kanban | Quadro de etapas com cartões | [docs/07-crm-kanban.md](docs/07-crm-kanban.md) | [examples/07-crm-kanban.html](examples/07-crm-kanban.html) |
| Caixa de entrada / chat | Atendimento em três colunas | [docs/08-inbox-chat.md](docs/08-inbox-chat.md) | [examples/08-inbox-chat.html](examples/08-inbox-chat.html) |
| Financeiro | Saldo, fluxo de caixa e transações | [docs/09-financeiro.md](docs/09-financeiro.md) | [examples/09-financeiro.html](examples/09-financeiro.html) |
| Agendamento | Agenda semanal e marcação de horário | [docs/10-agendamento.md](docs/10-agendamento.md) | [examples/10-agendamento.html](examples/10-agendamento.html) |
| Documentação | Navegação em árvore e coluna de leitura | [docs/11-documentacao.md](docs/11-documentacao.md) | [examples/11-documentacao.html](examples/11-documentacao.html) |
| App mobile | Abas inferiores, listas e folha inferior | [docs/12-app-mobile.md](docs/12-app-mobile.md) | [examples/12-app-mobile.html](examples/12-app-mobile.html) |
| Estados de tela | Vazio, carregando, erro, sem permissão, offline | [docs/13-estados-de-tela.md](docs/13-estados-de-tela.md) | no próprio doc |
| SEO | Metadados, sitemap, dados estruturados, renderização | [docs/14-seo.md](docs/14-seo.md) | no próprio doc |

O [docs/README.md](docs/README.md) tem o índice, um guia "Qual escolher" e a lista do que ficou fora, com o motivo.

## Ver os exemplos

Cada exemplo é um arquivo só, sem build e sem dependência de script. Abra direto no navegador:

```bash
open examples/02-dashboard-analytics.html
```

O botão de tema na tela alterna entre claro e escuro. As marcas e os dados são fictícios.

## Instalação

A skill é a pasta inteira (`SKILL.md`, `docs/` e `examples/`). Coloque-a em um destes lugares:

```bash
# Para todos os projetos
ln -s ~/zero-to-sys/skills/design-systems ~/.claude/skills/design-systems

# Só para um projeto
ln -s ~/zero-to-sys/skills/design-systems .claude/skills/design-systems
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é desenhar ou montar uma tela. Também dá para chamar direto com `/design-systems`. Exemplos:

- "Monta o dashboard inicial do sistema."
- "Qual o melhor layout para a tela de atendimento?"
- "/design-systems me mostra um exemplo de tela de agendamento."

Com a skill carregada, o Claude:

1. identifica o tipo de tela e o que o projeto já tem de marca e de UI kit;
2. escolhe o layout pela tabela do [SKILL.md](SKILL.md);
3. lê o documento e abre o exemplo do tipo, mais os fundamentos;
4. monta a tela na stack do projeto com os componentes da skill `design`, trocando os tokens pela marca;
5. confere o resultado renderizado, em tela grande e celular, claro e escuro;
6. explica a escolha em uma ou duas frases.

## Estrutura

```
design-systems/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
├── docs/
│   ├── README.md             índice, "Qual escolher" e o que ficou fora
│   ├── 01-fundamentos.md     regras comuns a todos os layouts
│   └── NN-nome.md            um documento por tipo de sistema
└── examples/
    └── NN-nome.html          um exemplo por tipo, com o mesmo número do documento
```

## Como manter

- **Adicionar um layout:** crie `docs/NN-nome.md` com as mesmas seções dos outros e `examples/NN-nome.html` no mesmo formato (um arquivo, tokens em variáveis CSS, claro e escuro, responsivo, dados fictícios em português). Inclua-o nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Mudar um exemplo:** atualize a tabela "Tokens do exemplo" e a "Anatomia do layout" do documento junto, para os dois não divergirem.
- **Revisar referências:** os produtos reais citados foram conferidos em 2026-11-24. Cada documento tem a data em "Verificado em"; atualize-a ao revisar.
