# audit

Skill para o Claude Code que audita um projeto existente: confronta o código com o checklist de cada skill do plugin, classifica cada área em ok, atenção, falta ou não verificado, com evidência, e ordena o que corrigir. Só diagnostica; a correção passa pela skill da área. Ela reúne um guia ([SKILL.md](SKILL.md)) e três documentos ([docs/](docs/)).

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Como auditar | Procedimento, evidência, comandos seguros | [docs/01-como-auditar.md](docs/01-como-auditar.md) |
| Relatório e status | Formato do relatório e dos status | [docs/02-relatorio-e-status.md](docs/02-relatorio-e-status.md) |
| Priorização e plano | Ordem de correção e qual skill resolve | [docs/03-priorizacao-e-plano.md](docs/03-priorizacao-e-plano.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/audit ~/.claude/skills/audit
```

## Como usar

O Claude carrega a skill sozinho quando o pedido bate com o tema dela. Também dá para chamar direto com `/audit`. Exemplos:

- "Audita esse projeto e me diz o que falta."
- "/audit está bem feito? Por onde começo a melhorar?"
- "Acabei de assumir esse sistema, faz um diagnóstico."

Com a skill carregada, o Claude:

1. descobre stack, estado e estrutura sem perguntar;
2. roda o checklist de cada skill que se aplica, só com comandos de leitura;
3. registra a evidência de cada item (ou "não verificado");
4. monta o relatório e ordena por risco e esforço;
5. propõe o primeiro passo e a skill que o resolve, sem alterar nada.

## Estrutura

```
audit/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md     índice e "Por onde começar"
    ├── 01-como-auditar.md
    ├── 02-relatorio-e-status.md
    └── 03-priorizacao-e-plano.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** Esta skill não traz preços nem versões; os critérios vêm do checklist de cada skill. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
