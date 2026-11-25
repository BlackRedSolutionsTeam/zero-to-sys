# Formatação e lint automáticos

> Deixe a máquina decidir aspas, espaços e estilo; o time discute só o que importa.

| | |
|---|---|
| **Referência** | Biome (biomejs.dev); ESLint (eslint.org); Prettier (prettier.io); Ruff (docs.astral.sh/ruff); `dotnet format` (Microsoft Learn); EditorConfig (editorconfig.org) |
| **Categoria** | Ferramentas |
| **Tipo** | Automação de qualidade |
| **Vale para** | TypeScript e JavaScript (Biome ou ESLint + Prettier), Python (Ruff), C# (`dotnet format` e analisadores .NET) |
| **Verificado em** | 2026-11-24 |

## O que é

Formatador reescreve o código num estilo único (indentação, aspas, quebra de linha). Linter aponta problemas de qualidade (variável sem uso, `==` em vez de `===`).

Na prática:

- **TypeScript:** Biome faz as duas coisas numa ferramenta só (`biome check`). A alternativa clássica é ESLint (lint) mais Prettier (formato).
- **Python:** Ruff faz lint (`ruff check`) e formatação (`ruff format`).
- **C#:** `dotnet format` aplica o estilo do `.editorconfig`; analisadores do compilador cuidam do lint.

## Por que usar

- **Fim da discussão de estilo:** o Prettier cita como principal motivo de adoção parar os debates contínuos de estilo (prettier.io, "Why Prettier?").
- **Diff limpo:** ninguém reformata o arquivo inteiro sem querer.
- **Pega bug:** o ESLint identifica e reporta padrões problemáticos no código (eslint.org).

## Quando usar

- Em todo projeto novo, no primeiro dia.
- Em projeto antigo: adote em um PR dedicado de formatação, sem mudar lógica.
- Na integração contínua, para barrar PR fora do padrão.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Projeto em equipe | ✅ Ótimo | Parar os debates contínuos de estilo (prettier.io, "Why Prettier?") |
| Código TypeScript/JavaScript | ✅ Ótimo | O ESLint identifica e reporta padrões problemáticos no código (eslint.org) |

## Quando é bom

- **Formata ao salvar:** o editor roda a ferramenta; ninguém lembra de nada.
- **Hook de commit e CI:** o formato e o lint rodam antes do merge.
- **Configuração mínima:** padrões da ferramenta, poucas regras ajustadas.
- **Uma ferramenta por trabalho:** não deixe ESLint e Prettier brigarem; use o pacote de integração oficial ou escolha Biome.

## Quando é ruim

- **Configuração demais:** comece pelas regras recomendadas de cada ferramenta (ex.: a configuração `recommended` do `@eslint/js`; o Ruff já traz um conjunto padrão de regras).
- **Regras de gosto no lint:** o que é estilo pessoal fica com o formatador, sem opção.
- **Plugins:** o ESLint aceita plugins de terceiros; se você depende de um, confira na documentação do Biome se há regra equivalente.
- **Dois formatadores:** ESLint com regras de formato junto com Prettier gera conflito; o Prettier documenta isso em "Integrating with Linters".
- **Divergência:** Biome (formatador e linter numa ferramenta) contra ESLint + Prettier (duas ferramentas). Escolha uma e padronize.

## Como começar

TypeScript com Biome (comandos da documentação oficial):

```bash
npm i -D -E @biomejs/biome
npx biome init
npx biome check --write   # formata, aplica correções seguras e lint
```

Python com Ruff (comandos da CLI; confira a instalação na documentação):

```bash
pip install ruff
ruff check --fix
ruff format
```

C#:

```bash
dotnet format
```

Para ESLint e Prettier, siga a documentação de cada um (ESLint usa configuração "flat" em `eslint.config.js` nas versões atuais; a versão mais recente do ESLint em 2026-11-24 é a 10.15.0, segundo o npm). Adicione o comando na CI e um `.editorconfig` na raiz.

## Combina com / alternativas

Combina com:
- [Revisão de código](12-revisao-de-codigo.md): sobra tempo para lógica.
- [Commits e PRs pequenos](11-commits-e-prs-pequenos.md): CI barra o que fugir do padrão.
- [Nomes claros](01-nomes-claros.md): o lint verifica a convenção de caixa.

Alternativas: ESLint + Prettier, Standard, dprint (TypeScript); Black + Flake8 ou Pylint (Python).

## Decisão rápida

- **Use se:** o projeto tem mais de uma pessoa, ou vai durar mais que um fim de semana.
- **Evite se:** o script é descartável e o editor já formata.
