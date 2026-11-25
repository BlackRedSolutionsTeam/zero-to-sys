# ia

Skill para o Claude Code que orienta como trabalhar com agentes de IA de código da melhor forma: configurar o projeto, pedir, delegar, paralelizar, verificar e controlar custo e risco. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por recurso ([docs/](docs/)), explicando quando usar, como se encaixa em cada tarefa, quando é bom, quando é ruim e por quê.

## Recursos cobertos

Só entrou o que passa em três critérios: existe na documentação oficial, muda o resultado do trabalho e tem um limite que vale explicar.

| Recurso | Papel | Documento |
|---|---|---|
| CLAUDE.md e AGENTS.md | Instruções persistentes do projeto | [docs/01-claude-md-agents-md.md](docs/01-claude-md-agents-md.md) |
| Memória automática | Notas do agente entre sessões | [docs/02-memoria-automatica.md](docs/02-memoria-automatica.md) |
| Skills | Procedimentos reutilizáveis sob demanda | [docs/03-skills.md](docs/03-skills.md) |
| Subagentes | Delegação com contexto próprio | [docs/04-subagentes.md](docs/04-subagentes.md) |
| Fluxo planejar e implementar | Explorar, planejar, implementar, verificar | [docs/05-fluxo-planejar-e-implementar.md](docs/05-fluxo-planejar-e-implementar.md) |
| Gestão de contexto | Limpar, compactar e voltar atrás | [docs/06-gestao-de-contexto.md](docs/06-gestao-de-contexto.md) |
| MCP | Ligação com sistemas externos | [docs/07-mcp.md](docs/07-mcp.md) |
| Hooks | Regras e passos impostos | [docs/08-hooks.md](docs/08-hooks.md) |
| Permissões e segurança | Modos, regras, sandbox, injeção de prompt | [docs/09-permissoes-e-seguranca.md](docs/09-permissoes-e-seguranca.md) |
| Paralelismo e orquestração | Worktrees, `/batch`, agent teams | [docs/10-paralelismo-e-orquestracao.md](docs/10-paralelismo-e-orquestracao.md) |
| Prompt e verificação | Pedido específico, check e revisão | [docs/11-prompt-e-verificacao.md](docs/11-prompt-e-verificacao.md) |
| Modelo e esforço | Modelo e `/effort` por tarefa | [docs/12-modelo-e-esforco.md](docs/12-modelo-e-esforco.md) |

O [docs/README.md](docs/README.md) tem o índice, um guia "Qual escolher" e a lista do que foi avaliado e saiu, com o motivo. Indexação de código e economia de token ficam na skill `code-indexes`.

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/ia ~/.claude/skills/ia
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é configurar um projeto para trabalhar com IA, planejar uma tarefa grande com agente ou rodar agentes em paralelo ou sem supervisão. Também dá para chamar direto com `/ia`. Exemplos:

- "O que eu ponho no CLAUDE.md deste projeto?"
- "Skill ou subagente para revisar PRs?"
- "/ia vou deixar o Claude migrar 200 arquivos de madrugada, como faço com segurança?"

Com a skill carregada, o Claude:

1. identifica a situação (tamanho da tarefa, se há supervisão, o que o projeto já tem);
2. escolhe os recursos pela tabela do [SKILL.md](SKILL.md), começando pelo mais simples;
3. lê o documento de cada recurso escolhido antes de configurar;
4. aplica as regras de uso (um check para o agente conferir, `CLAUDE.md` curto, o que não admite exceção vira hook, menor privilégio);
5. ao fim da tarefa, propõe criar uma linha no `CLAUDE.md`, uma skill, um subagente, um hook ou um servidor MCP quando aparece um sinal da seção "Quando criar cada recurso" do [SKILL.md](SKILL.md);
6. explica a escolha em uma ou duas frases.

## Estrutura

```
ia/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md             índice, "Qual escolher" e o que saiu da lista
    ├── 01-claude-md-agents-md.md
    ├── 02-memoria-automatica.md
    ├── 03-skills.md
    ├── 04-subagentes.md
    ├── 05-fluxo-planejar-e-implementar.md
    ├── 06-gestao-de-contexto.md
    ├── 07-mcp.md
    ├── 08-hooks.md
    ├── 09-permissoes-e-seguranca.md
    ├── 10-paralelismo-e-orquestracao.md
    ├── 11-prompt-e-verificacao.md
    └── 12-modelo-e-esforco.md
```

## Como manter

- **Adicionar um recurso:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o recurso nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um recurso:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos, e registre o motivo em `docs/README.md`.
- **Revisar dados:** o Claude Code muda rápido (comandos, modelos, padrões de permissão). Os dados foram verificados em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
