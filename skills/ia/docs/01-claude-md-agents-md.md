# CLAUDE.md e AGENTS.md

> Arquivo de texto na raiz do projeto que o agente lê no início de toda sessão: é onde ficam os comandos e as regras que ele não descobre sozinho lendo o código.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/memory e https://agents.md |
| **Categoria** | Instruções persistentes |
| **Tipo** | Arquivo Markdown versionado no repositório |
| **Onde vale** | Claude Code (`CLAUDE.md`); `AGENTS.md` é lido por Claude Code e por Codex, Cursor, Copilot, Gemini CLI, Zed, Windsurf e outros |
| **Equivalente em outras ferramentas** | `AGENTS.md` (padrão aberto, sem formato obrigatório). Regras próprias de cada ferramenta (ex.: pasta de regras do Cursor) não foram verificadas |
| **Verificado em** | 2026-11-24 |

## O que é

`CLAUDE.md` é um arquivo Markdown com instruções que o Claude Code carrega em toda sessão. Os locais confirmados na documentação: `./CLAUDE.md` ou `./.claude/CLAUDE.md` (projeto, vai para o git), `~/.claude/CLAUDE.md` (pessoal, todos os projetos), `./CLAUDE.local.md` (pessoal do projeto, entra no `.gitignore`) e um arquivo gerenciado pela organização.

O Claude Code sobe a árvore de diretórios e junta os arquivos que encontra. Arquivos em subpastas carregam só quando o agente lê algum arquivo ali. Um arquivo pode importar outro com `@caminho/do/arquivo`. Para regras que valem só para parte do código, use `.claude/rules/*.md` com o campo `paths:` no frontmatter.

`AGENTS.md` é o padrão aberto para a mesma função, mantido pela Agentic AI Foundation (Linux Foundation). O Claude Code lê `AGENTS.md` quando não existe nenhum `CLAUDE.md` acima do diretório de trabalho. Se existir os dois, só o `CLAUDE.md` vale, a menos que o `CLAUDE.md` importe o `AGENTS.md` (`@AGENTS.md`) ou você mude a opção "Project instructions" em `/config`. Ler `AGENTS.md` direto exige versão recente do Claude Code (a documentação cita v2.1.277); confira com `claude --version`.

## Por que usar

- **Conhecimento que não está no código:** comando de teste, decisão de reunião, variável de ambiente, armadilha conhecida.
- **Menos correção repetida:** o que você corrigiu duas vezes vira uma linha.
- **Vale para o time:** vai no git, então todo mundo (e todo agente) parte do mesmo ponto.
- **Portátil:** com `AGENTS.md`, o mesmo arquivo serve a várias ferramentas.

## Quando usar

- Quando o agente erra uma convenção ou comando duas vezes (gatilho da tabela "Build your setup over time", code.claude.com/docs/en/features-overview).
- Para o comando de build, teste e lint e como rodar um arquivo de teste (code.claude.com/docs/en/best-practices).
- Quando há um padrão antigo que o código novo não deve copiar (best-practices).
- Quando o time usa mais de uma ferramenta de IA (use `AGENTS.md` e importe no `CLAUDE.md`).

### Quando o agente deve propor

- **Sinais** (o primeiro vem do gatilho "wrong twice" da tabela "Build your setup over time", features-overview): o usuário corrigiu a mesma coisa pela segunda vez; o agente errou um comando de build, teste ou lint e descobriu o certo; apareceu uma armadilha que não dá para ver lendo o código (variável de ambiente, pasta legada, ordem de passos).
- **O que fazer:** propor a linha exata e, com o ok, gravar no `CLAUDE.md` da raiz (ou no `AGENTS.md`, se o time usa mais de uma ferramenta). Uma linha por aprendizado, na seção que já existe.
- **Não proponha se:** a informação está no código ou no `README`, vale só para a tarefa atual, ou é preferência de uma pessoa só (isso vai para a [memória automática](02-memoria-automatica.md) ou para `~/.claude/CLAUDE.md`). Se a mesma regra já está no arquivo e foi ignorada, o caminho é um [hook](08-hooks.md), não mais uma linha.

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Base desconhecida | ✅ Ótimo | `/init` gera um ponto de partida a partir do código |
| Tarefa repetitiva | ✅ Ótimo | A documentação indica o `CLAUDE.md` para convenções e regras "sempre faça X" |
| Feature grande | ✅ Ótimo | A documentação manda pôr aí o comando de verificação e as decisões que não estão no repositório |
| Trabalho em paralelo | ✅ Ótimo | Worktree é checkout novo; a documentação sugere deixar o comando de instalação no `CLAUDE.md` |
| Regra que não admite exceção | ❌ Evite | É texto que o modelo lê; ele pode decidir não seguir. Use hook ou regra `deny` (ver [08](08-hooks.md) e [09](09-permissoes-e-seguranca.md)) |

## Quando é bom

- **Curto e verificável:** a documentação contrapõe "Run `npm test` before committing" a "Test your changes" e "API handlers live in `src/api/handlers/`" a "Keep files organized" (memory, "Write effective instructions").
- **Só o que o agente não acha sozinho:** a documentação oficial manda deixar de fora o que ele descobre lendo o repositório.
- **Escopo por pasta:** `.claude/rules/` com `paths:` carrega a regra só quando o agente mexe naquele código.
- **Fácil de auditar:** `/context` mostra se o arquivo carregou; `/doctor` sugere cortes.

## Quando é ruim

- **Arquivo grande:** a recomendação oficial é menos de 200 linhas por arquivo. Mais que isso gasta contexto e o agente passa a ignorar linhas. Importar com `@` organiza, mas não reduz o custo, porque o arquivo importado carrega junto.
- **Descrever a arquitetura e a árvore de pastas:** o agente lê o repositório. É o primeiro corte que o `/doctor` sugere.
- **Regras que se contradizem:** o agente escolhe uma sem avisar. Revise o arquivo e as regras de subpastas de tempos em tempos.
- **ÊNFASE em maiúsculas:** a documentação diz que modelos atuais seguem uma linha escrita normal e que gritar tende a fazer o agente exagerar a regra.
- **Instrução de outra época:** linhas escritas para modelos antigos viram ruído. `/doctor prompt-audit` aponta essas linhas.
- **`CLAUDE.local.md` com `AGENTS.md`:** ter um `CLAUDE.local.md` conta como "tem CLAUDE.md" e faz o Claude parar de ler o `AGENTS.md` (comportamento descrito na documentação).

## Como começar

```bash
# Gera um CLAUDE.md inicial a partir do código (dentro de uma sessão do claude)
/init

# Confere o que carregou
/context all
```

Exemplo enxuto, no formato que a documentação oficial recomenda:

```markdown
# Comandos
- Instalar: pnpm install
- Um arquivo de teste: pnpm vitest run caminho/do/arquivo.test.ts
- Typecheck: pnpm tsc --noEmit

# Convenções
- Erros: use os helpers de src/lib/errors.ts, nunca lance string
- src/legacy/ está em uso, mas não copie o padrão dele

# Armadilhas
- Teste de integração precisa de DATABASE_URL (veja .env.example)
```

Para usar um `AGENTS.md` existente junto com o Claude:

```markdown
# CLAUDE.md
@AGENTS.md

## Só para o Claude Code
- Use o modo de planejamento antes de mexer em src/billing/
```

## Combina com / alternativas

Combina com:
- [Skills](03-skills.md): procedimento longo vai para skill, não para o `CLAUDE.md`.
- [Hooks](08-hooks.md): o que não admite exceção sai do arquivo e vira hook.
- [Memória automática](02-memoria-automatica.md): complementa, com o que o agente anota sozinho.

Alternativas:
- Regras de outras ferramentas (Cursor, Copilot etc.): têm formato próprio descrito na documentação de cada ferramenta; este guia não os detalha, então prefira `AGENTS.md`.

## Decisão rápida

- **Use se:** você usa agente no projeto mais de uma vez e quer parar de repetir comando, convenção e armadilha.
- **Evite se:** a regra não pode ter exceção (use hook ou `deny`) ou é um procedimento longo de uma tarefa específica (use skill).

Fontes das recomendações: code.claude.com/docs/en/memory (tamanho, especificidade, `AGENTS.md`), best-practices (o que entra no `CLAUDE.md`, hook para regra sem exceção) e features-overview ("CLAUDE.md vs Skill", "Build your setup over time").
