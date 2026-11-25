# Verificação pelo agente

> O agente de IA só diz "pronto" depois de rodar os comandos do projeto, abrir o app de verdade e mostrar a evidência, com um revisor que não viu o raciocínio dele.

| | |
|---|---|
| **Referência** | code.claude.com/docs/en/best-practices ("Give Claude a check to run"), code.claude.com/docs/en/hooks (evento `Stop`), github.com/microsoft/playwright-mcp, playwright.dev |
| **Categoria** | Qualidade |
| **Tipo** | Prática de verificação por agente, com apoio de hook e subagente |
| **Vale para** | Qualquer agente de código; os comandos e o formato de hook citados são do Claude Code |
| **Verificado em** | 2026-11-24 |

## O que é

Verificar é o agente provar, com saída de comando ou imagem, que a funcionalidade cumpre o critério de aceite. Não é o agente dizer "funcionou". Quatro passos, nesta ordem:

1. **Rodar os comandos do projeto** (teste, lint, typecheck, build) e ler a saída inteira, não só o código de saída.
2. **Abrir o app** e conferir o critério como usuário: navegar, clicar, tirar screenshot, olhar o console do navegador e as chamadas de rede.
3. **Conferir em celular e em desktop.**
4. **Mostrar a evidência** e, em mudança grande, pedir a um revisor independente.

O que torna isso obrigatório, e não um favor que o modelo faz quando lembra, é o hook `Stop`. Como pedir o check no prompt, `/goal` e `/verify` já estão em [Prompt e verificação](../../ia/docs/11-prompt-e-verificacao.md); como funciona o hook, em [Hooks](../../ia/docs/08-hooks.md). Este doc cobre o que verificar e as armadilhas.

## Por que usar

- **O agente erra com confiança:** o texto "tudo certo" sai igual quando funciona e quando não funciona.
- **Teste verde não prova a tela:** um botão pode passar no teste de unidade e estar escondido no celular.
- **Você deixa de ser o teste:** o agente acha a falha antes de você abrir o app.
- **Revisão com evidência:** você olha uma saída e uma imagem, não uma promessa.

## Quando usar

- Ao fim de toda funcionalidade, no passo "Pronto" do ciclo (ver [Definition of Done](08-definition-of-done.md)).
- Em trabalho longo ou sem supervisão, junto com o hook `Stop`.
- Em mudança de interface, onde teste automático sozinho não vê layout quebrado.
- Depois de o agente mexer em teste: aí a verificação é redobrada.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Build e screenshot bastam; pouca lógica para testar |
| MVP de SaaS | ✅ Ótimo | Pouco tempo de revisão humana; o agente precisa provar o fluxo |
| SaaS em crescimento | ✅ Ótimo | Muita regressão possível; typecheck e testes no `Stop` seguram |
| Sistema interno/corporativo | ✅ Ótimo | Fluxos longos de formulário e tabela, difíceis de revisar à mão |
| API/integração | ✅ Ótimo | Sem tela: a evidência é a saída do teste de API e a resposta real |
| App mobile | 🟡 Serve | Exige emulador ou Maestro; o navegador não cobre |
| Protótipo descartável | ❌ Evite | Hook e revisor custam mais que o código que vai ser jogado fora |

## Quando é bom

- **Critério de aceite como régua:** "Dado um horário já ocupado, quando a recepcionista tenta agendar, então vê o aviso de conflito". O agente roda o teste desse critério e também faz o fluxo no navegador.
- **Evidência pedida no prompt:** "mostre o comando e a saída; anexe o screenshot da tela de agendamento".
- **Hook `Stop`:** o agente não encerra com o typecheck ou os testes quebrados.
- **Navegador de verdade:** o Playwright MCP expõe ferramentas como `browser_take_screenshot`, `browser_console_messages`, `browser_network_requests` e `browser_resize`. O Claude in Chrome serve quando a tela precisa de login que já está na sua sessão.
- **Dois tamanhos:** 375 px de largura (celular) e 1280 px (desktop), com screenshot de cada. Ver [Ponta a ponta com Playwright](05-ponta-a-ponta-com-playwright.md).
- **Revisor independente:** um subagente que lê o diff e o critério sem ver a conversa não herda o viés de quem escreveu. Ver [Subagentes](../../ia/docs/04-subagentes.md).

## Quando é ruim

- **Armadilha 1, apagar ou afrouxar teste:** o agente remove a asserção, troca `toBe(3)` por `toBeDefined()`, adiciona `skip` ou aumenta o timeout até passar.
- **Armadilha 2, mockar o que devia testar:** o teste de agendamento mocka o repositório e o banco, e passa sem exercitar a regra de conflito. Ver [Testes de integração com banco](03-testes-de-integracao-com-banco.md).
- **Armadilha 3, "pronto" sem rodar:** a frase aparece sem nenhum comando no histórico. Cobre-se com o hook e pedindo a saída.
- **Armadilha 4, verificar só o caminho feliz:** o app abre, mas o estado vazio, o erro e o celular nunca foram vistos.
- **Armadilha 5, ler só o final da saída:** "1 failed" no meio de mil linhas passa despercebido.
- **Hook lento:** um `Stop` que roda a suíte de uma hora trava a sessão. Rode o rápido (typecheck, unidade) no hook e deixe o ponta a ponta para o CI. Ver [Quality gates no CI](07-quality-gates-no-ci.md).
- **Limite do hook:** o Claude Code encerra mesmo assim se o `Stop` bloquear muitas vezes seguidas (detalhe em [Hooks](../../ia/docs/08-hooks.md)). O hook não substitui o CI.

**Regra:** teste nunca é alterado para passar sem dizer por quê. Se o agente mudou um teste, a resposta dele precisa trazer o motivo (o requisito mudou, o teste estava errado) e o diff do teste. Sem isso, a mudança é rejeitada.

## Como começar

Trecho para o `CLAUDE.md` do projeto:

```markdown
## Verificação antes de dizer "pronto"

- Rode `pnpm typecheck`, `pnpm lint`, `pnpm test` e `pnpm build`. Mostre o comando e o resultado de cada um.
- Em mudança de tela, abra o app, siga o critério de aceite, tire screenshot em 375 px e em 1280 px e olhe o console e a rede.
- Nunca apague, ignore (`skip`) ou afrouxe um teste para ele passar. Se o teste precisa mudar, explique o motivo e mostre o diff do teste antes.
- Não mocke o banco nem a regra que o teste existe para provar.
- Se não conseguiu rodar algo, diga qual e por quê. Não escreva "pronto" nesse caso.
```

Hook `Stop` em `.claude/settings.json`, que bloqueia o fim enquanto typecheck ou testes falham (código de saída 2 devolve o stderr ao agente):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "(pnpm typecheck && pnpm test --run) 1>&2 || exit 2"
          }
        ]
      }
    ]
  }
}
```

Playwright MCP no projeto:

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

Pedido ao agente, com evidência e conferência de tamanhos:

```text
implemente o aviso de conflito de horário no agendamento. Rode os testes do
critério e mostre a saída. Abra o app, tente agendar um horário ocupado e
tire screenshot em 375 px e 1280 px. Leia o console e a rede. Se mudar algum
teste, diga por quê.
```

Revisor independente (subagente em `.claude/agents/revisor.md`):

```markdown
---
name: revisor
description: Revisa o diff contra o critério de aceite, sem ver a conversa. Use depois de implementar.
tools: Read, Grep, Glob, Bash
---

Leia o diff e o critério de aceite. Aponte só lacunas de correção: critério sem teste,
teste afrouxado ou removido, mock no lugar da regra real. Ignore estilo.
```

Em cada stack, só trocam os comandos do hook e do `CLAUDE.md`:

| Stack | Typecheck/compilação | Testes |
|---|---|---|
| TypeScript | `pnpm tsc --noEmit` | `pnpm vitest run` |
| .NET | `dotnet build` | `dotnet test` |
| Python | `mypy .` | `pytest` |
| PHP | `phpstan analyse` | `vendor/bin/pest` |
| Go | `go vet ./...` | `go test ./...` |
| Java | `./mvnw compile` | `./mvnw test` |

## Combina com / alternativas

Combina com:
- [Prompt e verificação](../../ia/docs/11-prompt-e-verificacao.md): como pedir o check e `/goal`.
- [Hooks](../../ia/docs/08-hooks.md): o `Stop` torna a verificação obrigatória.
- [Subagentes](../../ia/docs/04-subagentes.md): o revisor sem contexto.
- [Definition of Done](08-definition-of-done.md): a lista que a verificação confirma.
- [Quality gates no CI](07-quality-gates-no-ci.md): a barreira final, fora da sessão.

Alternativas:
- Revisão humana do diff e do screenshot, sempre que o risco for alto.
- Segunda sessão de revisão, com você levando as mensagens.

## Decisão rápida

- **Use se:** o agente escreve código que você não vai ler linha a linha, ou o trabalho roda sem supervisão.
- **Evite se:** a mudança é descartável, ou você aceitaria "pronto" sem ver evidência; nesse caso, defina o check antes de pedir.
