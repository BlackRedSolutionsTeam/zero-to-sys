# Prompt e verificação

> Pedir com contexto e dar ao agente algo que ele rode e responda passou ou falhou, para ele conferir o próprio trabalho e para você revisar com evidência.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/best-practices |
| **Categoria** | Método de trabalho |
| **Tipo** | Prática, com apoio de `/goal`, hook `Stop`, `/code-review` e `/verify` |
| **Onde vale** | Qualquer agente de código. Os comandos citados são do Claude Code |
| **Equivalente em outras ferramentas** | A prática vale em todas; comandos equivalentes não foram verificados |
| **Verificado em** | 2026-11-24 |

## O que é

Duas ideias da documentação de boas práticas. Primeiro, o agente já lê o código; o que ele não vê é decisão de reunião, preferência entre duas abordagens e o que significa "pronto". Isso vai no pedido: arquivo, sintoma e resultado esperado. Segundo, sem um check que dê passou ou falhou, "parece pronto" é tudo o que o agente tem, e você vira o teste.

O check pode ser um arquivo de teste, o código de saída do build, um linter, um script que compara saída com um arquivo esperado ou uma captura de tela do navegador ao lado do mockup. Graus de rigor, do mais solto ao mais firme: pedir no prompt ("rode os testes de auth e continue até passar"); `/goal condição`, em que outro modelo confere a condição a cada turno; um hook `Stop` que bloqueia o fim enquanto o script falha; e revisão por quem não escreveu o código (`/code-review` roda a revisão do diff em um subagente que não viu a conversa, e pode comentar no PR com `--comment`).

## Por que usar

- **O que o agente não vê:** decisão de reunião, preferência entre abordagens e o que é "pronto" só chegam se estiverem no pedido (best-practices, "Tell Claude what it can't see").
- **Você deixa de ser o teste:** o agente repete até passar.
- **Evidência:** o comando e a saída valem mais que "tudo passa".
- **Revisão sem viés:** o revisor não é influenciado pelo raciocínio que gerou o código.

## Quando usar

- Em trabalho longo ou sem supervisão: as cinco perguntas incluem "Can it check its own work?" (best-practices, "Let Claude run without you").
- Em interface: captura de tela comparada ao desenho.

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Bug difícil | ✅ Ótimo | Teste que reproduz a falha primeiro, depois a correção |
| Feature grande | ✅ Ótimo | A especificação vira a régua; revisão contra o `SPEC.md` |
| Trabalho sem supervisão | ✅ Ótimo | `/goal`, hook `Stop` e `--max-turns` dão fim e limite |
| Interface | ✅ Ótimo | A documentação lista "a browser screenshot next to the mockup" como check (best-practices; extensão do Chrome em code.claude.com/docs/en/chrome) |
| Exploração ("o que você melhoraria?") | 🟡 Serve | A documentação diz que pedido vago é aceitável quando se explora; você corrige mais |
| Código sem nenhum teste | ❌ Evite confiar | Sem check, escreva o teste antes ou valide à mão |

## Quando é bom

- **Pedido específico:** "usuários falham no login depois do timeout; veja o refresh de token em `src/auth/`, escreva um teste que falhe e corrija" supera "arrume o login".
- **Entregar o material:** `@arquivo` inclui o conteúdo; cole imagens; `cat erro.log | claude -p "o que houve"` leva saída de comando.
- **Entrevista antes de construir:** para o que ainda está vago (ver [05](05-fluxo-planejar-e-implementar.md)).
- **`/verify`:** é uma skill embutida que confirma uma mudança construindo e rodando o app do projeto e observando o resultado, em vez de confiar só em testes e typecheck (conferido em 2026-11-24). `/run-skill-generator` ensina o `/run` e o `/verify` a subir o seu app.

## Quando é ruim

- **"Todos os testes passam" sem a saída:** peça o comando e o resultado.
- **Revisor que "sempre acha algo":** se você corrige tudo, ganha camadas e testes para casos impossíveis. Peça só lacunas de correção e "ignore estilo".
- **`/goal` e hooks de modelo não são firmes:** quem confere é outro modelo. Só `command`, `http` e `mcp_tool` são determinísticos.
- **Frases mágicas:** "pense bem" e "seja minucioso" são texto comum. O controle é o nível de esforço (ver [12](12-modelo-e-esforco.md)). Já `seja ambicioso` ajuda, porque informa escopo, que só você sabe.
- **Loop longo:** tarefas agendadas e `/goal` podem enviar o contexto inteiro mesmo com a sessão parada (costs); a documentação manda limitar turnos ou gasto (`--max-turns`, `--max-budget-usd`).
- **O que a IA gerou ainda é seu:** a documentação de segurança diz que você é responsável por revisar o que o agente propõe antes de aprovar (security, "User responsibility").

## Como começar

```text
usuários relatam que o login falha depois do timeout da sessão. Veja o refresh
de token em src/auth/, escreva um teste que reproduza, corrija e rode
pnpm vitest run src/auth até passar. Mostre o comando e a saída.
```

```text
/goal todos os testes em tests/auth passam e o lint está limpo
```

```text
construa a tela de configurações a partir do mockup. Seja ambicioso: estados
vazio e de erro, fluxo de salvar, navegação por teclado. Confira com uma
captura de tela e compare com o mockup.
```

Em script (um arquivo por vez, com limites):

```bash
claude --bare -p "Migre $arquivo para a nova API de log e commite. Responda OK ou FALHA." \
  --allowedTools "Read,Edit,Bash(git add *),Bash(git commit *)" \
  --permission-mode dontAsk --max-turns 20
```

Teste em três arquivos antes de rodar o resto.

## Combina com / alternativas

Combina com:
- [Hooks](08-hooks.md): `Stop` torna o check obrigatório.
- [Subagentes](04-subagentes.md): revisor com ferramentas só de leitura.
- [Fluxo planejar e implementar](05-fluxo-planejar-e-implementar.md): `SPEC.md` como critério de pronto.

Alternativas:
- CI e proteção de branch: a barreira final, fora da sessão.
- Segunda sessão de revisão, com você levando as mensagens.
- Revisão humana: a documentação de segurança diz que revisar o que o agente propõe é responsabilidade sua.

## Decisão rápida

- **Use se:** a mudança altera comportamento e existe (ou dá para criar) um comando que prove que funciona.
- **Evite se:** você ia aceitar "pronto" sem ver evidência; nesse caso, defina o check antes de pedir.

Fontes das recomendações: code.claude.com/docs/en/best-practices ("Tell Claude what it can't see", "Give Claude a check to run", "Let Claude run without you") e goal.
