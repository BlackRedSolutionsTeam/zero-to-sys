# Histórias e critérios de aceite

> Cada pedaço do produto vira uma história curta com critérios que dizem, sem dúvida, quando ela está pronta.

| | |
|---|---|
| **Referência** | Mike Cohn, "User Stories Applied" (Addison-Wesley, 2004); Bill Wake, "INVEST in Good Stories, and SMART Tasks" (2003); Ron Jeffries, os 3 Cs (Card, Conversation, Confirmation); Dan North, "Introducing BDD" (2006); Gherkin (cucumber.io/docs/gherkin) |
| **Categoria** | Produto |
| **Tipo** | Prática de especificação de requisitos |
| **Vale para** | Qualquer linguagem e qualquer time, com ou sem agente de IA |
| **Verificado em** | 2026-11-24 |

## O que é

História de usuário é uma descrição curta de algo que uma pessoa quer fazer no sistema. O formato clássico, popularizado por Mike Cohn, é:

**Como** `<papel>`, **quero** `<ação>`, **para** `<benefício>`.

Critério de aceite é a lista de condições que precisam ser verdadeiras para a história valer como terminada. Um formato comum, vindo do Behaviour-Driven Development (Dan North) e da linguagem Gherkin, é **Dado / Quando / Então**:

- **Dado** o ponto de partida (o estado do sistema).
- **Quando** a pessoa faz algo.
- **Então** o resultado esperado.

Ron Jeffries descreve a história em 3 Cs:

- **Card (cartão):** o texto curto que lembra do assunto.
- **Conversation (conversa):** o que cliente e time combinam falando.
- **Confirmation (confirmação):** os critérios que provam que ficou certo.

Bill Wake propôs o **INVEST** para checar se a história é boa: Independent (independente), Negotiable (negociável), Valuable (com valor), Estimable (estimável), Small (pequena) e Testable (testável).

## Por que usar

- **Agente de IA sabe quando parar:** o critério de aceite é o que ele usa para saber que o item terminou.
- **Vira teste automatizado:** cada critério pode virar um teste (veja [Testes](../../coding/docs/08-testes.md) e a skill `quality`).
- **Cliente e time falam a mesma língua:** o texto é simples, sem jargão técnico.

## Quando usar

- Depois de definir o escopo do MVP e os fluxos.
- Antes de pedir uma funcionalidade ao agente de IA.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site/landing | 🟡 Serve | Poucas ações; basta uma história por formulário ou fluxo de contato |
| MVP de SaaS | ✅ Ótimo | Cada funcionalidade do MVP vira história com critérios testáveis |
| SaaS em crescimento | ✅ Ótimo | Papéis, permissões e erros se multiplicam; o texto evita regressões |
| Sistema interno | ✅ Ótimo | Muitos papéis e regras; o critério deixa o combinado registrado |
| API/integração | ✅ Ótimo | O "usuário" é outro sistema; critérios descrevem pedido e resposta |
| App mobile | ✅ Ótimo | Inclui casos de rede ruim, permissão do aparelho e erro |
| Protótipo descartável | ❌ Evite | Escrever critério completo custa mais que jogar o protótipo fora |
| Tarefa técnica sem usuário (trocar versão de biblioteca) | ❌ Evite | Não há papel nem benefício de negócio; use uma tarefa técnica simples |

## Quando é bom

- **Critérios verificáveis:** qualquer pessoa consegue dizer "passou" ou "não passou".
- **Caminho feliz, erro e permissão cobertos** em cada história.

## Quando é ruim

- **Critério vago:** "rápido", "fácil", "bonito" não se testam.
- **História gigante:** "Como usuário, quero gerenciar pedidos" é um épico. Quebre em partes.
- **Detalhe técnico no texto:** "usar Redis" é decisão de stack, não história.
- **Documento que ninguém atualiza:** vira mentira. Revise quando o combinado mudar.

Critério vago x verificável, lado a lado:

| Ruim | Bom |
|---|---|
| A lista é rápida | A lista carrega em menos de 2 s com 1.000 itens |
| O erro é claro | Se o e-mail já existe, mostra "E-mail já cadastrado" e mantém os outros campos preenchidos |
| Só quem pode vê | Usuário sem a permissão "financeiro" recebe erro 403 e não vê o menu Relatórios |

## Como começar

Modelo para copiar:

```markdown
## História: <nome curto>

Como <papel>,
quero <ação>,
para <benefício>.

### Critérios de aceite

Caminho feliz
- Dado <estado inicial>
  Quando <ação>
  Então <resultado observável>
Erro
- Dado <estado inicial>
  Quando <ação inválida>
  Então <mensagem ou comportamento exato>
Permissão
- Dado <usuário sem acesso>
  Quando <tenta a ação>
  Então <bloqueio e o que ele vê>
```

Exemplo 1, agendar consulta:

```markdown
## História: Agendar consulta

Como paciente,
quero escolher um horário livre com um médico,
para ser atendido sem precisar ligar.

### Critérios de aceite

Caminho feliz
- Dado que estou logado e o Dr. Silva tem o horário das 10h livre amanhã
  Quando escolho esse horário e confirmo
  Então a consulta aparece em "Minhas consultas" e recebo um e-mail de confirmação
Erro
- Dado que outra pessoa agendou o horário das 10h um segundo antes
  Quando confirmo o mesmo horário
  Então vejo "Horário indisponível" e a lista de horários livres é atualizada
Permissão
- Dado que não estou logado
  Quando abro a tela de agendamento
  Então sou levado ao login e volto para a tela depois de entrar
```

Exemplo 2, cancelar pedido:

```markdown
## História: Cancelar pedido

Como cliente,
quero cancelar um pedido que ainda não foi enviado,
para não pagar por algo que não quero mais.

### Critérios de aceite

Caminho feliz
- Dado um pedido meu com status "Pago"
  Quando clico em "Cancelar pedido" e confirmo
  Então o status muda para "Cancelado" e o reembolso é solicitado
Erro
- Dado um pedido com status "Enviado"
  Quando abro o pedido
  Então o botão "Cancelar" não aparece e vejo "Pedido já enviado"
- Dado que a falha ocorre ao solicitar o reembolso
  Quando confirmo o cancelamento
  Então o pedido continua "Pago" e vejo "Não foi possível cancelar, tente de novo"
Permissão
- Dado um pedido de outro cliente
  Quando tento cancelá-lo pela URL ou pela API
  Então recebo erro 403 e nada muda
```

## Combina com / alternativas

- [Entrevista com o cliente](01-entrevista-com-o-cliente.md): de onde saem os papéis e as ações.
- [Escopo do MVP](02-escopo-do-mvp.md): define quais histórias entram.
- [Fluxos e jornadas](03-fluxos-e-jornadas.md): cada passo do fluxo vira uma ou mais histórias.
- [Regras de negócio](05-regras-de-negocio.md): regras como "só cancela antes do envio" alimentam os critérios.
- [Backlog e ordem de construção](06-backlog-e-ordem-de-construcao.md): as histórias entram na fila.
- [Testes](../../coding/docs/08-testes.md): critério vira teste.
- Alternativas: casos de uso formais (mais detalhe, mais peso); lista simples de tarefas (para time de uma pessoa só); Job Stories ("Quando..., quero..., para...") quando o papel importa menos que a situação.

## Decisão rápida

- **Use se:** o sistema terá regras, papéis ou erros, ou um agente de IA vai construir o item.
- **Evite se:** é um protótipo para jogar fora ou uma tarefa técnica sem pessoa usuária.
