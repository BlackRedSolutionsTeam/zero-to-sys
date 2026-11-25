# coding

Skill para o Claude Code que guia como escrever código bem organizado, simples e fácil de ler por qualquer senioridade, principalmente júnior. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por prática ([docs/](docs/)), explicando quando usar, em que tipo de código encaixa, quando ajuda, quando atrapalha e como começar.

## Práticas cobertas

Só entrou o que passa em três critérios: referência reconhecida, benefício real no dia a dia e exemplo que um júnior aplica sem treino.

| Prática | Papel | Documento |
|---|---|---|
| Nomes claros | O nome diz o que a coisa é ou faz | [docs/01-nomes-claros.md](docs/01-nomes-claros.md) |
| Funções pequenas | Uma responsabilidade por função | [docs/02-funcoes-pequenas.md](docs/02-funcoes-pequenas.md) |
| Modularização e limites | Coesão alta, acoplamento baixo | [docs/03-modularizacao-e-limites.md](docs/03-modularizacao-e-limites.md) |
| Simplicidade | KISS, YAGNI e regra de três | [docs/04-simplicidade.md](docs/04-simplicidade.md) |
| Tratamento de erros | Falhar cedo, com contexto | [docs/05-tratamento-de-erros.md](docs/05-tratamento-de-erros.md) |
| Tipos e validação na borda | Validar o que vem de fora | [docs/06-tipos-e-validacao-na-borda.md](docs/06-tipos-e-validacao-na-borda.md) |
| Sem comentários no código | Nome, função e teste no lugar do comentário | [docs/07-comentarios-e-documentacao.md](docs/07-comentarios-e-documentacao.md) |
| Testes | Comportamento, pirâmide ou troféu | [docs/08-testes.md](docs/08-testes.md) |
| Formatação e lint automáticos | Biome, ESLint + Prettier, Ruff, dotnet format | [docs/09-formatacao-e-lint-automaticos.md](docs/09-formatacao-e-lint-automaticos.md) |
| Refatoração segura | Passos pequenos com testes | [docs/10-refatoracao-segura.md](docs/10-refatoracao-segura.md) |
| Commits e PRs pequenos | Conventional Commits | [docs/11-commits-e-prs-pequenos.md](docs/11-commits-e-prs-pequenos.md) |
| Revisão de código | Revisar lógica e legibilidade | [docs/12-revisao-de-codigo.md](docs/12-revisao-de-codigo.md) |

O [docs/README.md](docs/README.md) tem o índice, um guia "Qual escolher" e a lista do que foi avaliado e saiu, com o motivo. Estrutura de pastas é da skill architecture; escolha de linguagem e framework é da stacks.

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/coding ~/.claude/skills/coding
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é escrever, simplificar, refatorar ou revisar código. Também dá para chamar direto com `/coding`. Exemplos:

- "Escreve o serviço de pedidos, com código limpo."
- "Essa função ficou enorme, como eu divido?"
- "/coding revisa este PR pensando em quem é júnior."

Com a skill carregada, o Claude:

1. descobre linguagem, convenções do repositório e se há testes, lint e formatador;
2. escolhe as práticas pela tabela de decisão do [SKILL.md](SKILL.md);
3. lê o documento de cada prática escolhida;
4. aplica em passos pequenos, seguindo as regras de uso (sem comentários no código, simples primeiro, validar na borda, refatoração separada);
5. roda formatador, lint e testes;
6. explica a escolha em uma ou duas frases.

## Estrutura

```
coding/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md             índice, "Qual escolher" e o que saiu da lista
    ├── 01-nomes-claros.md
    ├── 02-funcoes-pequenas.md
    ├── 03-modularizacao-e-limites.md
    ├── 04-simplicidade.md
    ├── 05-tratamento-de-erros.md
    ├── 06-tipos-e-validacao-na-borda.md
    ├── 07-comentarios-e-documentacao.md
    ├── 08-testes.md
    ├── 09-formatacao-e-lint-automaticos.md
    ├── 10-refatoracao-segura.md
    ├── 11-commits-e-prs-pequenos.md
    └── 12-revisao-de-codigo.md
```

## Como manter

- **Adicionar uma prática:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua a prática nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover uma prática:** apague o documento, tire-a das três tabelas e dos links em "Combina com / alternativas" dos outros documentos, e registre o motivo em `docs/README.md`.
- **Revisar dados:** nomes de ferramentas, comandos e convenções foram verificados em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
