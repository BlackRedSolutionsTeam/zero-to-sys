# Gestão de contexto

> Saber o que ocupa a janela do agente e usar `/clear`, `/compact` e `/rewind` para manter a sessão focada e barata.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/context-window e https://code.claude.com/docs/en/best-practices |
| **Categoria** | Operação da sessão |
| **Tipo** | Comandos e hábitos |
| **Onde vale** | Claude Code. Todo agente tem uma janela finita; os comandos variam por ferramenta |
| **Equivalente em outras ferramentas** | Codex CLI: `/compact` (resume o chat) e `/new` (novo chat na mesma sessão), em developers.openai.com/codex/cli/slash-commands. Copilot CLI: `/compact [foco]`, `/context` e `/clear` (também `/new`). Cursor: `/summarize` resume o contexto sob demanda (cursor.com/changelog/1-6); o resumo automático das partes antigas está em cursor.com/docs/agent/prompting. Conferido em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

A janela de contexto guarda tudo que o agente sabe na sessão: instruções, arquivos lidos, saídas de comandos e as próprias respostas. Antes de você digitar já entram o prompt de sistema, o `CLAUDE.md`, a memória automática, os nomes das ferramentas de MCP e as descrições das skills.

Comandos confirmados na documentação:
- `/context` mostra o uso do contexto (e `/context all` lista os arquivos de memória carregados).
- `/clear` começa do zero; `/clear nome` guarda a sessão atual com esse nome para voltar depois.
- `/compact instruções` resume a conversa mantendo o que você pedir (ex.: `/compact manter as mudanças de API e os comandos de teste`).
- `/rewind` (ou `Esc` duas vezes) volta código, conversa ou os dois; também resume um trecho antigo.
- `/btw` responde uma pergunta rápida sem entrar no histórico.
- `/usage` mostra para onde foi o consumo.

O Claude Code compacta sozinho perto do limite. Na documentação atual, a maioria dos modelos recentes tem janela de 1 milhão de tokens.

## Por que usar

- **Respostas melhores e custo menor:** a documentação diz que um contexto focado dá respostas melhores e custa menos.
- **Histórico se paga a cada turno:** cada requisição envia a conversa inteira (best-practices, "Keep cost and context down").
- **Recomeço limpo:** depois de duas correções falhas, uma sessão nova com um pedido melhor funciona mais que uma terceira correção.

## Quando usar

- Ao trocar de assunto: `/clear`.
- Em pausas naturais entre tarefas: `/compact` com foco (prompt-caching: "save `/compact` for natural breaks between tasks").
- Quando o agente insiste no erro: `Esc`, `/rewind` ou `/clear`.
- Quando a sessão ficou cara: `/usage` e `/context`.

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Tarefas diferentes na mesma sessão | ✅ Ótimo | `/clear` entre elas evita pagar o histórico anterior |
| Feature grande | ✅ Ótimo | `/clear` entre plano e implementação; `/compact` com foco no meio |
| Bug difícil | ✅ Ótimo | `/rewind` descarta beco sem saída sem perder o código bom |
| Base desconhecida | 🟡 Serve | Leitura ampla pede subagente `Explore` para não encher a janela |
| Sessão retomada depois de pausa longa | ❌ Cuidado | A primeira mensagem depois do tempo de vida do cache reprocessa o contexto inteiro (costs; prompt-caching) |

## Quando é bom

- **Gratuito:** `/clear` não custa nada.
- **Compactação dirigida:** você escolhe o que o resumo preserva, em vez de deixar o agente adivinhar.
- **Parte importante sobrevive:** a documentação lista o que volta do disco depois de compactar: `CLAUDE.md` da raiz, regras sem `paths`, memória automática, descrições de skills, o plano do modo de planejamento e até cinco arquivos lidos recentemente.

## Quando é ruim

- **Compactar perde detalhe:** é um resumo. Instrução dada só na conversa pode sumir; o que importa vai no `CLAUDE.md`.
- **Compactar também custa:** em sessão longa, o `/compact` lê a conversa toda para resumir, e custa mais com o cache expirado.
- **O que carrega sob demanda não sobrevive:** regras com `paths:` e `CLAUDE.md` de subpastas entram na conversa quando o agente lê o arquivo gatilho e são resumidos junto. Regra que precisa persistir fica sem `paths` ou no `CLAUDE.md` da raiz.
- **Corpo de skill truncado:** limite de 5.000 tokens por skill e 25.000 no total depois da compactação.
- **`/rewind` não cobre tudo:** não restaura arquivos alterados só por comando de shell. Ele complementa o git, não o substitui.
- **Janela grande não é desculpa:** com 1 milhão de tokens raramente falta espaço, mas contexto sujo ainda piora a resposta e custa mais.

## Como começar

```text
/context                       ver o que está ocupando
/clear                         trocar de assunto
/clear migracao-oauth          trocar e guardar esta sessão com nome
/compact manter as mudanças de API e os comandos de teste
/rewind                        voltar a um ponto anterior (ou Esc Esc)
/usage                         ver o consumo por skill, subagente e MCP
```

Retomar depois, no terminal:

```bash
claude --resume migracao-oauth
claude --continue          # a sessão mais recente
```

Para trabalho de vários dias, `/rename nome` dentro da sessão.

## Combina com / alternativas

Combina com:
- [Subagentes](04-subagentes.md): leituras grandes ficam no contexto deles.
- [MCP](07-mcp.md): servidores conectados somam ao contexto fixo.
- [CLAUDE.md](01-claude-md-agents-md.md): arquivo curto gasta menos em toda sessão.

Alternativas:
- Ferramentas de indexação de código para ler menos arquivos inteiros: pertencem à skill `code-indexes`, não são tratadas aqui.
- Reduzir o custo fixo (cortar MCP, enxugar `CLAUDE.md`) em vez de limpar a conversa.

## Decisão rápida

- **Use se:** a sessão mistura assuntos, ficou lenta ou cara, ou o agente repete o mesmo erro.
- **Evite se:** a conversa tem instrução que você deu só nela e não anotou: a documentação diz que isso pode se perder na compactação (memory, solução de problemas). Escreva no `CLAUDE.md` primeiro.

Fontes das recomendações: code.claude.com/docs/en/best-practices ("Keep cost and context down"), context-window, prompt-caching, costs e checkpointing.
