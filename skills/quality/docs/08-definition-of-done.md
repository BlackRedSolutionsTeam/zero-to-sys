# Definition of Done

> Uma lista única e curta que todo item precisa cumprir para ser considerado pronto, além dos critérios de aceite próprios dele.

| | |
|---|---|
| **Referência** | The Scrum Guide 2020 (scrumguides.org), seções Commitment: Definition of Done e Increment; "Specification by Example" (Gojko Adzic); GitHub Docs, pull request templates (docs.github.com) |
| **Categoria** | Qualidade |
| **Tipo** | Prática de acordo de equipe |
| **Vale para** | Qualquer stack e qualquer tamanho de equipe, inclusive uma pessoa com agente de IA |
| **Verificado em** | 2026-11-24 |

## O que é

Definition of Done (DoD, definição de pronto) é a lista de qualidade que todo item precisa cumprir. O Scrum Guide 2020 a descreve como "uma descrição formal do estado do Incremento quando ele atende às medidas de qualidade exigidas para o produto". Diz também que o trabalho não conta como parte do Incremento se não atender à DoD, e que um item que não a atende não pode ser entregue.

Não confunda com critério de aceite:

| | Definition of Done | Critério de aceite |
|---|---|---|
| Vale para | Todo item | Um item só |
| Responde | "O trabalho tem qualidade?" | "O item faz o que foi pedido?" |
| Exemplo | Testes, lint e build verdes | "Dado que o horário está ocupado, quando agendo, então vejo erro" |
| Quem define | O time | O produto (skill `product`) |

Um item está pronto quando cumpre os critérios de aceite dele e a DoD.

## Por que usar

- **Fim da discussão "está pronto?":** a lista responde.
- **Qualidade igual em todo item**, inclusive no que um agente de IA escreveu.
- **Trabalho escondido aparece:** migration, teste e documentação entram no item, não no "depois eu faço".

## Quando usar

- Em todo item do backlog, a cada ciclo da fase 9 da skill principal.
- Ao revisar PR: o revisor percorre a lista.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Versão curta: build, links, tela conferida |
| MVP de SaaS | ✅ Ótimo | Lista enxuta mantém velocidade sem acumular dívida |
| SaaS em crescimento | ✅ Ótimo | Clientes pagantes exigem teste, migration e staging |
| Sistema interno/corporativo | ✅ Ótimo | Auditoria e acessibilidade entram na lista |
| API/integração | ✅ Ótimo | Contrato e migration revisada são o centro |
| App mobile | ✅ Ótimo | Dois dispositivos e estados de rede entram na lista |
| Lista de 30 itens que ninguém cumpre | ❌ Evite | DoD ignorada é pior que nenhuma; corte até caber |

## Quando é bom

- **Verificável:** cada linha se responde com sim ou não, rodando algo.
- **Curta:** cabe numa tela; o que a máquina checa (teste, lint) o CI barra (veja `07-quality-gates-no-ci.md`).
- **Evolui:** quando um bug escapa, pergunte qual linha faltou na DoD e adicione.
- **Igual à do plugin:** a DoD abaixo é a da fase 9 da skill principal, em versão detalhada.

## Quando é ruim

- **Virar burocracia:** itens que ninguém confere.
- **Misturar com critério de aceite:** "o botão é azul" é critério do item, não da DoD.
- **Marcar sem rodar:** caixinha marcada sem verificar é mentira com checklist.

## Como começar

DoD do plugin (MVP e corporativo usam as mesmas linhas base; o porte muda o que se acrescenta):

- [ ] Critérios de aceite cumpridos e verificados rodando, não só lendo o código.
- [ ] Um teste automatizado por critério.
- [ ] Testes, lint, typecheck e build verdes.
- [ ] Migration revisada e banco recriado do zero sem erro, se o item mexe no banco.
- [ ] Tela conferida no dispositivo principal e no secundário, com estados vazio, carregando e erro.
- [ ] Acessibilidade básica: foco visível, navegação por teclado, rótulo nos campos, contraste.
- [ ] Nenhum segredo no código ou no histórico do Git.
- [ ] `BACKLOG.md` atualizado no mesmo PR.
- [ ] Regra nova registrada em `docs/regras-de-negocio.md`.
- [ ] Deploy em staging verificado, quando já houver staging.

Por porte:

| Porte | O que a DoD inclui |
|---|---|
| MVP | As linhas acima; staging só quando existir; acessibilidade básica e um dispositivo secundário conferido por olho |
| Corporativo | Tudo do MVP, mais: revisão de outra pessoa, teste de permissão por papel, auditoria de dependências limpa, e2e do fluxo, plano de reversão, documentação de uso atualizada |

Exemplo (agendamento de clínica). Critério do item: "Dado que o horário já está ocupado, quando o paciente tenta agendar, então vê o aviso e nada é gravado". A DoD exige um teste que cubra essa frase, a tela do aviso nos estados de erro e carregando, e o `BACKLOG.md` com o item marcado.

Colar no `CLAUDE.md` (o agente passa a seguir sozinho):

```md
## Definição de pronto

Antes de dizer que um item está pronto, rode e confirme:

- Cada critério de aceite tem um teste e passa.
- `npm test`, `npm run lint`, `npx tsc --noEmit` e `npm run build` estão verdes.
- Se mexeu no banco: migration revisada e banco recriado do zero.
- Se tem tela: dispositivo principal e secundário, estados vazio, carregando e erro.
- Sem segredo no código.
- `BACKLOG.md` atualizado no mesmo PR; regra nova em `docs/regras-de-negocio.md`.
- Relate o que foi verificado e como; não diga "pronto" sem ter rodado.
```

Colar em `.github/pull_request_template.md`:

```md
## O que muda

Item do backlog: #

## Definição de pronto

- [ ] Critérios de aceite cumpridos e verificados rodando
- [ ] Um teste por critério
- [ ] Testes, lint, typecheck e build verdes
- [ ] Migration revisada e banco recriado do zero (se mexe no banco)
- [ ] Tela conferida no dispositivo principal e no secundário, com estados vazio, carregando e erro
- [ ] Acessibilidade básica conferida
- [ ] Sem segredo no código
- [ ] `BACKLOG.md` atualizado neste PR
- [ ] Regra nova registrada em `docs/regras-de-negocio.md`
- [ ] Deploy em staging verificado

## Como verifiquei

Passos e resultado:
```

## Combina com / alternativas

- `07-quality-gates-no-ci.md`: automatiza as linhas que uma máquina consegue checar.
- `09-verificacao-pelo-agente.md`: como o agente prova cada linha.
- `../../product/docs/04-historias-e-criterios-de-aceite.md`: origem dos critérios de aceite.
- `../../coding/docs/08-testes.md`: como escrever o teste legível.
- Alternativa: checklist informal no PR, sem versão fixa; funciona só em equipe de uma pessoa.

## Decisão rápida

- **Use se:** mais de um item por semana vai para produção ou um agente escreve parte do código.
- **Evite se:** a lista tem itens que ninguém verifica; reduza antes de adotar.
