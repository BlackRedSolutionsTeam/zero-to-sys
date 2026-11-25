# Skills

> Pasta com um `SKILL.md` que ensina ao agente um procedimento do seu time e só entra no contexto quando a tarefa pede.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/skills |
| **Categoria** | Procedimentos reutilizáveis |
| **Tipo** | Pasta com `SKILL.md` e arquivos de apoio |
| **Onde vale** | Claude Code. Codex e Cursor também usam pasta com `SKILL.md` (conferido em 2026-11-24) |
| **Equivalente em outras ferramentas** | Codex: skills em `.agents/skills`. Cursor: skills em `.agents/skills` ou `.cursor/skills`. GitHub Copilot: skills em `.github/skills`, `.claude/skills` ou `.agents/skills` (pessoais em `~/.copilot/skills`); a página não cita `SKILL.md` |
| **Verificado em** | 2026-11-24 |

## O que é

Uma skill é uma pasta com um `SKILL.md`: frontmatter em YAML e instruções em Markdown. Locais confirmados: `~/.claude/skills/<nome>/SKILL.md` (pessoal), `.claude/skills/<nome>/SKILL.md` (projeto, vai para o git), pasta de skills de um plugin e uma pasta gerenciada pela organização. Esta própria skill (`ia`) segue o formato.

O nome e a descrição de cada skill ficam sempre no contexto. O corpo só carrega quando o agente decide usar a skill ou quando você digita `/nome`. Depois de carregado, o corpo fica na conversa. Por isso a `description` é o campo mais importante: é ela que faz o agente acionar a skill. Campos úteis do frontmatter: `name`, `description`, `disable-model-invocation: true` (só você chama), `user-invocable: false` (só o agente chama), `allowed-tools`, `model`, `effort`, `context: fork` (roda em subagente) e `paths`.

## Por que usar

- **Procedimento do time fora do `CLAUDE.md`:** release, runbook, padrão de documentação ficam em skill e não pesam nas tarefas sem relação.
- **Reuso:** a mesma skill serve a todo o time pelo git.
- **Chamada manual:** `/release` roda só quando você manda, se usar `disable-model-invocation: true`.
- **Pode trazer scripts e referências:** arquivos ao lado do `SKILL.md` carregam só quando citados.

## Quando usar

- Fluxo com vários passos que você repete (release, migração, revisão, geração de relatório).
- Conhecimento que o modelo não tem: como o seu time faz algo.
- Guia de decisão como este, com documentos que o agente lê sob demanda.
- Ação com efeito colateral que só você deve disparar.

### Quando o agente deve propor

- **Sinais:** o usuário colou ou explicou o mesmo procedimento pela terceira vez (features-overview, "Build your setup over time"); o `CLAUDE.md` está crescendo com um passo a passo que só serve para um tipo de tarefa (a documentação manda mover procedimento de vários passos para skill).
- **O que fazer:** ao fim da tarefa, propor a skill com o nome, a `description` e os passos já escritos a partir do que funcionou. Com o ok, gravar em `.claude/skills/<nome>/SKILL.md` se é do projeto e do time, ou em `~/.claude/skills/<nome>/SKILL.md` se é um hábito da pessoa em qualquer projeto.
- **Não proponha se:** o procedimento só apareceu uma ou duas vezes, cabe em uma linha do `CLAUDE.md`, ou é uma regra sem exceção (isso é [hook](08-hooks.md)). Se a ação tem efeito colateral (publicar, enviar, apagar), crie com `disable-model-invocation: true`.

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Tarefa repetitiva | ✅ Ótimo | A documentação lista "repeatable tasks" e workflows como `/deploy` |
| Material de referência (guia de API, de estilo) | ✅ Ótimo | A tabela "CLAUDE.md vs Skill" indica skill para material de consulta |
| Ação com efeito colateral (deploy) | ✅ Ótimo | Com `disable-model-invocation: true` ela só roda quando você a chama |
| Regra sem exceção | ❌ Evite | Skill é texto lido pelo modelo; use hook |

## Quando é bom

- **Custo baixo de contexto:** só a descrição fica sempre carregada.
- **Versionável:** a skill de projeto fica em `.claude/skills/` e vai para o git.
- **Dá para travar a chamada:** `disable-model-invocation: true` impede que o agente dispare sozinho algo como deploy.
- **Recarrega ao editar:** mudanças nas pastas de skills valem na sessão; `/reload-skills` se a nova não aparecer.

## Quando é ruim

- **Descrição vaga:** o agente não aciona. Escreva os gatilhos ("use quando o usuário pedir X, Y, Z").
- **Descrições custam contexto:** o Claude vê nome e descrição das skills em toda requisição (features-overview). A listagem trunca `description` mais `when_to_use` em 1.536 caracteres por skill.
- **Corpo longo:** o oficial manda manter o `SKILL.md` abaixo de 500 linhas e mover o detalhe para arquivos de apoio.
- **Depois de compactar:** a skill é reinjetada, mas cortada em 5.000 tokens por skill e 25.000 no total; o corte mantém o início. Ponha o mais importante no topo.
- **Não é imposição:** o agente pode pular passos. O que precisa acontecer sempre vai em hook.
- **Skill do repositório pode liberar ferramentas:** o `allowed-tools` de uma skill de projeto vale até em `-p` numa pasta nunca confiada, e a documentação manda revisá-lo antes de rodar o Claude Code ali.

## Como começar

```bash
mkdir -p .claude/skills/release
```

```markdown
---
name: release
description: Faz o release: sobe a versão, escreve o changelog, cria a tag. Use quando o usuário pedir "fazer release" ou "publicar versão".
disable-model-invocation: true
---
1. Confirme que está na main e com a árvore limpa. Se não, pare e pergunte.
2. Rode `pnpm changeset version` e commite.
3. Resuma os PRs desde a última tag no CHANGELOG.md, uma linha cada.
4. Crie a tag `v<versão>` e envie. O CI publica; nunca publique da máquina.
```

Chamada: `/release`. Argumentos: `/fix-issue 123`, usando `$ARGUMENTS` no corpo.

## Combina com / alternativas

Combina com:
- [CLAUDE.md e AGENTS.md](01-claude-md-agents-md.md): o arquivo guarda o que vale sempre; a skill guarda o procedimento.
- [Subagentes](04-subagentes.md): `context: fork` roda a skill em subagente.
- [Hooks](08-hooks.md): hook garante o passo que a skill só pede.

Alternativas:
- Comando de barra antigo em `.claude/commands/`: a documentação de skills (code.claude.com/docs/en/skills, 2026-11-24) diz que os comandos personalizados foram unificados com as skills, que os arquivos em `.claude/commands/` continuam funcionando e que é o formato mais antigo ("Prefer a skill for new work"). Se skill e arquivo têm o mesmo nome, vale a skill.
- Plugin: empacota skills, subagentes e hooks para distribuir.

## Decisão rápida

- **Use se:** o procedimento é do seu time, se repete e é longo demais para o `CLAUDE.md`.
- **Evite se:** é uma tarefa única, uma regra sem exceção ou algo que o modelo já sabe fazer sem instrução.

Fontes das recomendações: code.claude.com/docs/en/skills e features-overview ("Match features to your goal", "CLAUDE.md vs Skill", "Skill vs Subagent", "Build your setup over time").
