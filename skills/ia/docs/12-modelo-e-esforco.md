# Modelo e nível de esforço

> Escolher qual modelo e quanto raciocínio usar por tarefa: o padrão serve na maioria, e subir ou descer o esforço é a alavanca principal.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/model-config e https://code.claude.com/docs/en/costs |
| **Categoria** | Custo e qualidade |
| **Tipo** | Comandos `/model` e `/effort`, flags e variáveis de ambiente |
| **Onde vale** | Claude Code. Outras ferramentas oferecem seletor de modelo com opções próprias |
| **Equivalente em outras ferramentas** | Codex CLI: `/model` e `/reasoning` (esforço do chat), flag `--model`. Copilot CLI: `/model` (ou Auto); a referência (docs.github.com/copilot, 2026-11-24) diz que `/model` muda modelo, esforço de raciocínio ou janela de contexto na sessão, e que agentes aceitam `reasoningEffort` (`low`, `medium`, `high`). Cursor: seletor de modelo; no plano Plus o esforço é fixo em médio, e nos planos Premium ou acima dá para escolher. Conferido em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

O modelo define a capacidade e o custo por requisição. O esforço define quanto o modelo raciocina antes de responder. Aliases confirmados: `opus`, `sonnet`, `haiku`, `fable`, `best` (igual a `opus`) e `opusplan` (Opus no modo de planejamento, Sonnet na execução). Na API da Anthropic, `opus`, `sonnet` e `haiku` resolvem hoje para Opus 5.5, Sonnet 5.5 e Haiku 5.5; os aliases acompanham a versão recomendada, então fixe o nome completo se precisar de versão estável.

Como trocar: `/model nome` na sessão, `claude --model nome` ao abrir, a variável `ANTHROPIC_MODEL` ou o campo `model` das configurações. Esforço: `/effort low|medium|high|xhigh|max`, `/effort auto` para limpar e `/effort status`. Para os modelos atuais citados, o padrão é `medium`. A palavra `ultrathink` num pedido pede raciocínio mais profundo só naquele turno. Subagentes aceitam `model` e `effort` no frontmatter.

## Por que usar

- **Qualidade onde importa:** esforço alto em bug sutil, baixo em renomear.
- **Custo sob controle:** modelo menor em tarefa rotineira e em subagente simples.
- **Menos espera:** esforço baixo quando você revisa cada passo mesmo.
- **Previsível:** fixar a versão evita mudança silenciosa de comportamento.

## Quando usar

- Antes de uma tarefa difícil ou de uma rotineira em volume.
- Quando uma tarefa custou mais do que devia (`/usage` mostra onde).
- Ao definir subagentes.

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Bug em código que você não escreveu | ✅ Ótimo | A documentação sugere `high` ou `xhigh` quando o caso é fácil de deixar passar |
| Tarefa de rotina | ✅ Ótimo | A documentação diz que o Sonnet custa menos em trabalho de rotina e que o Haiku serve a subagentes de tarefa simples (best-practices) |
| Brainstorm, esboço, renomear | ✅ Ótimo | `/effort low` acelera quando você revisa cada passo |
| Feature com escopo claro | 🟡 Serve | `medium` (padrão) "fits day-to-day engineering work with a clear scope, such as implementing a new feature" (model-config) |
| Caça a vulnerabilidade sem você por perto | 🟡 Serve | `max` só aqui; em tarefa comum tende a pensar demais |
| Tarefa comum | 🟡 Serve | A documentação diz que o padrão atende a maioria das tarefas |
| `max` como padrão | ❌ Evite | A documentação diz que `max` "is prone to overthinking" e pode render retornos decrescentes |

## Quando é bom

- **Padrão sensato:** a documentação diz que o padrão atual já serve à maioria das tarefas.
- **Troca no meio da sessão:** `/model` e `/effort` valem na hora; `ultrathink` vale um turno.
- **Hierarquia clara:** a documentação lista a ordem de precedência (variável `CLAUDE_CODE_EFFORT_LEVEL`, depois a escolha na sessão, a flag `--effort`, as configurações e o padrão do modelo).
- **Janela de 1 milhão de tokens** nos modelos atuais citados, sem sufixo; versões antigas usam `[1m]`.

## Quando é ruim

- **Nome de modelo muda:** alias aponta para a versão recomendada de agora. O que está nesta página sobre versões pode envelhecer rápido; confira em `/model`.
- **Disponibilidade varia por plano e provedor:** nem todo modelo ou nível existe em todo lugar (o modo `auto`, por exemplo, depende de modelo e provedor).
- **`max` vale só para a sessão** (a menos que defina por variável de ambiente) e pode piorar o custo sem melhorar a resposta.
- **Esforço baixo testa menos:** a documentação diz que em nível mais alto o Claude testou mais casos de borda e verificou mais do próprio trabalho (model-config, "Choose an effort level").
- **Subagente não dá resposta melhor:** a documentação diz que entregar a mesma tarefa a um subagente não melhora a resposta (best-practices).
- **Trocar de modelo perde o cache:** o histórico é reenviado no preço cheio na primeira requisição. A documentação de prompt caching confirma: cada modelo tem o próprio cache, e trocar com `/model` faz a próxima requisição reler todo o histórico sem cache (conferido em 2026-11-24). O Claude Code pede confirmação se o cache ainda está quente. Mudar o esforço também invalida o cache na maioria dos modelos. Veja `/usage`.
- **Texto de prompt não substitui o controle:** "pense mais" não eleva o esforço; só `ultrathink` ou `/effort`.

## Como começar

```text
/model sonnet                 trocar na sessão
/model opusplan               Opus para planejar, Sonnet para executar
/effort high                  subir o esforço
/effort auto                  voltar ao padrão do modelo
ultrathink: por que esse teste falha só no CI?
```

```bash
claude --model opus --effort high
```

Subagente barato:

```markdown
---
name: coletor
description: Lista os arquivos que importam um módulo
tools: Read, Grep, Glob
model: haiku
---
Liste os arquivos que importam o módulo pedido. Responda só com a lista.
```

Para ver para onde foi o gasto: `/usage`.

## Combina com / alternativas

Combina com:
- [Subagentes](04-subagentes.md): `model` e `effort` por definição.
- [Fluxo planejar e implementar](05-fluxo-planejar-e-implementar.md): `opusplan`.
- [Gestão de contexto](06-gestao-de-contexto.md): contexto enxuto também reduz custo.

Alternativas:
- Economia de token por indexação de código: outra skill (`code-indexes`), não tratada aqui.
- Deixar o padrão: a escolha certa até uma tarefa custar mais do que devia.

## Decisão rápida

- **Use se:** a tarefa é claramente mais difícil ou mais simples que o normal, ou roda em volume.
- **Evite se:** você está mexendo em configuração por hábito; só ajuste depois de ver custo ou qualidade ruins.

Fontes das recomendações: code.claude.com/docs/en/model-config ("Choose an effort level"), best-practices ("Change the model and effort", "Know what subagents cost") e prompt-caching.
