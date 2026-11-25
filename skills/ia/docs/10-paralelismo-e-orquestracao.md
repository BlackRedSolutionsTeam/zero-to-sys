# Paralelismo e orquestração

> Rodar várias sessões ou agentes ao mesmo tempo, cada um com seu próprio checkout, sem que as edições colidam.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/worktrees, /agent-teams e /best-practices |
| **Categoria** | Execução em paralelo |
| **Tipo** | `claude --worktree`, `/batch`, agent teams (experimental), sessões na nuvem |
| **Onde vale** | Claude Code. `git worktree` serve a qualquer ferramenta |
| **Equivalente em outras ferramentas** | `git worktree` manual funciona com qualquer agente; recursos próprios de outras ferramentas não foram verificados |
| **Verificado em** | 2026-11-24 |

## O que é

Há quatro níveis, do mais simples ao mais pesado:

1. **Subagentes** dentro de uma sessão (ver [04](04-subagentes.md)).
2. **Sessões em worktrees:** `claude --worktree nome` (ou `-w`) cria um worktree em `.claude/worktrees/<nome>/`, num branch `worktree-<nome>`, e abre a sessão nele. Em outro terminal, outro nome, outra sessão isolada. O arquivo `.worktreeinclude` (sintaxe de `.gitignore`) lista arquivos ignorados, como `.env`, para copiar a cada worktree novo. Subagentes podem usar `isolation: worktree`.
3. **`/batch`:** divide uma mudança mecânica grande em 5 a 30 unidades, mostra o plano e, aprovado, cada unidade roda em seu worktree e abre um PR ou relata o resultado.
4. **Agent teams:** vários agentes com lista de tarefas compartilhada e troca de mensagens. É experimental e vem desligado; liga-se com `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

Também existem sessões na nuvem e, na linha de comando, `claude agents` (prévia de pesquisa) para ver o que roda em segundo plano.

## Por que usar

- **Sem colisão:** a documentação diz que cada sessão em seu worktree edita o próprio checkout, na própria branch.
- **Segunda sessão como revisora:** a documentação chama de "easiest independent reviewer" uma sessão que revisa sem ter visto o código ser escrito (best-practices).
- **Mudança mecânica em massa:** `/batch` reparte o trabalho e entrega vários PRs.

## Quando usar

- Duas ou mais tarefas que não dependem uma da outra.
- Migração repetitiva em muitos arquivos.
- Revisão independente de um PR.
- Investigação de bug com hipóteses concorrentes (em agent teams).

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Trabalho em paralelo (tarefas independentes) | ✅ Ótimo | Um worktree por tarefa, sem colisão |
| Migração mecânica em muitos arquivos | ✅ Ótimo | `/batch` reparte e abre os PRs |
| Revisão e pesquisa | ✅ Ótimo | A documentação sugere começar por aí em agent teams: fronteiras claras, sem editar |
| Feature grande com camadas separadas | 🟡 Serve | Funciona se cada agente tem arquivos próprios; coordenação custa |
| Bug difícil | 🟡 Serve | Hipóteses em paralelo ajudam; um só agente tende a ancorar na primeira |
| Tarefas sequenciais ou no mesmo arquivo | ❌ Evite | A documentação diz que agent teams rendem pouco nesses casos; dois agentes no mesmo arquivo se sobrescrevem |

## Quando é bom

- **Isolamento de arquivos:** cada worktree tem os próprios arquivos e branch (worktrees).
- **Limpeza ao sair:** numa sessão sem nome, o worktree limpo é removido com o branch; sessão nomeada ou com mudanças pergunta antes (worktrees, "Clean up worktrees").
- **Começar por 3 a 5 agentes:** recomendação da documentação de agent teams.

## Quando é ruim

- **Custa muito token:** cada agente tem a própria janela. A documentação diz que agent teams usam "significativamente mais" tokens que uma sessão.
- **Worktree é checkout novo:** não tem `.env` nem dependências instaladas. Use `.worktreeinclude` e deixe o comando de instalação no `CLAUDE.md`.
- **`node_modules` no `.worktreeinclude` copia, não faz link:** uma cópia por worktree. Para pastas grandes há a opção `worktree.symlinkDirectories`.
- **Compartilha parte do estado:** o worktree usa o mesmo diretório `.git`, os plugins de projeto e as aprovações "don't ask again" do checkout principal (worktrees, "What worktrees share with the main checkout").
- **Agent teams são experimentais:** limitações citadas na documentação: não retomam teammates com `/resume`, status de tarefa pode atrasar, um time por sessão, sem times aninhados.
- **Líder pode agir sozinho:** às vezes o líder começa a implementar em vez de esperar. É preciso mandá-lo aguardar.
- **Conflito entra no merge:** mudanças que tocam as mesmas áreas voltam como conflito. Divida por arquivos e módulos.
- **Limpeza manual com `-p`:** execuções `claude -p --worktree` não são limpas sozinhas (`git worktree remove`, e `git worktree unlock` se estiver travado).

## Como começar

```bash
# duas sessões isoladas, em dois terminais
claude --worktree feature-auth
claude --worktree fix-relatorio

# a partir de um PR
claude --worktree "#1234"

# worktree manual, a partir de um branch existente
git worktree add ../projeto-fix fix-issue-456
```

`.worktreeinclude` na raiz:

```text
.env
.env.local
```

Boa prática: adicione `.claude/worktrees/` ao `.gitignore`. Para mudança em massa, dentro da sessão: `/batch migrar todos os handlers para o helper de resposta v2`.

## Combina com / alternativas

Combina com:
- [Subagentes](04-subagentes.md): `isolation: worktree` e definições reaproveitadas como teammates.
- [CLAUDE.md](01-claude-md-agents-md.md): comando de instalação e testes valem em todo worktree.
- [Permissões e segurança](09-permissoes-e-seguranca.md): teammates começam no modo de permissão do líder.

Alternativas:
- Uma sessão só, com `/clear` entre tarefas: mais barata quando não há pressa.
- Subagentes sem worktree: para pesquisa e revisão, que não editam.
- Orquestração por script (`claude -p` em laço): ver [11](11-prompt-e-verificacao.md).

## Decisão rápida

- **Use se:** as tarefas são independentes, mexem em arquivos diferentes e o tempo vale mais que o token.
- **Evite se:** o trabalho é sequencial, concentrado nos mesmos arquivos ou pequeno.

Fontes das recomendações: code.claude.com/docs/en/worktrees, agent-teams ("Start with research and review", "Limitations") e best-practices ("Run sessions in parallel").
