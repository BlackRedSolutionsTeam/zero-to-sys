# Entrevista com o cliente

> Uma conversa curta e planejada, em linguagem do cliente, que descobre o que o sistema precisa fazer antes de qualquer decisão técnica.

| | |
|---|---|
| **Referência** | Jobs to be Done (Clayton Christensen; Bob Moesta, "Demand-Side Sales 101", 2020); Rob Fitzpatrick, "The Mom Test" (2013) |
| **Categoria** | Produto |
| **Tipo** | Prática de descoberta de requisitos |
| **Vale para** | Qualquer sistema novo ou funcionalidade grande, com cliente real ou interno |
| **Verificado em** | 2026-11-24 |

## O que é

É a conversa em que você descobre o que o cliente quer, antes de escolher stack, banco ou layout. O objetivo é sair com um resumo que o cliente aprova.

A base vem de duas ideias. A primeira é Jobs to be Done: ninguém "compra um sistema", a pessoa contrata uma solução para fazer um trabalho na vida dela. Pergunte qual é o trabalho. A segunda é o "The Mom Test": pergunte sobre a vida e o passado do cliente, não sobre a sua ideia. "Como você marca consultas hoje?" rende mais que "Você usaria um sistema de agenda?".

## Por que usar

- **Evita construir a coisa errada.** Refazer depois custa mais que perguntar agora.
- **Define o escopo.** Sem entrevista, o pedido cresce sem limite.
- **Respeita o tempo do cliente.** Poucas perguntas, bem escolhidas, em no máximo duas rodadas.
- **Gera um registro.** O resumo aprovado vira a base das próximas etapas.

## Quando usar

- No início de qualquer projeto, antes de escolher a stack.
- Quando o pedido chega vago: "quero um sistema para minha clínica".
- Quando uma funcionalidade grande aparece no meio do projeto.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site / landing | 🟡 Serve | Poucas perguntas: público, objetivo, visual e contato |
| MVP de SaaS | ✅ Ótimo | Define o problema e o que fica fora do MVP |
| SaaS em crescimento | ✅ Ótimo | Separa o pedido de um cliente da necessidade de todos |
| Sistema interno | ✅ Ótimo | Descobre como o trabalho é feito hoje e quem aprova o quê |
| API / integração | 🟡 Serve | Foque em quem consome, volume e o que acontece se falhar |
| App mobile | ✅ Ótimo | Confirma se o celular é mesmo necessário e se precisa de offline |
| Correção de bug pequena | ❌ Evite | Entrevista é exagero; basta ler o relato do erro |

## Quando é bom

- **O cliente fala do problema dele**, não de telas e tecnologias.
- **A pessoa certa responde.** Quem usa o sistema no dia a dia sabe mais que quem só paga.
- **O pedido já tem respostas.** Você pergunta só o que falta.
- **Você mostra o que assumiu.** O cliente corrige em vez de adivinhar.

## Quando é ruim

- **Perguntas técnicas:** "precisa de multi-tenancy?" não diz nada ao cliente.
- **Perguntas sobre a sua ideia:** "você gostaria disso?" leva a um "sim" educado e inútil.
- **Questionário gigante:** o cliente cansa e responde qualquer coisa.
- **Perguntar o que tem padrão sensato:** gasta a atenção dele à toa.
- **Aceitar resposta vaga:** "quero um app" pode ser só "uso no celular".

## Como começar

Regras da conversa:

1. Leia o pedido e a pasta do projeto antes. Não pergunte o que já está respondido.
2. Agrupe as perguntas por tema e envie tudo de uma vez.
3. Cada pergunta tem de 2 a 4 opções, com a recomendada primeiro.
4. Se existe padrão sensato, assuma e avise qual assumiu.
5. Se a resposta for vaga, pergunte o porquê. "Precisa de app" vira "Onde a pessoa vai usar?".
6. No máximo duas rodadas. A segunda só existe se a primeira abriu dúvida nova.
7. Feche com o resumo e peça o ok.

Roteiro pronto (exemplo: agendamento de clínica). Apague o que o pedido já respondeu:

```markdown
## 1. Problema e público
1. Qual é o maior problema hoje?
   a) Perder consultas por falta de aviso (recomendada)
   b) Agenda em papel ou WhatsApp bagunçado
   c) Dificuldade de ver o faturamento
2. Quem vai usar no dia a dia?
   a) Recepção e profissionais (recomendada)
   b) Também os pacientes, para marcar sozinhos

## 2. Usuários e acessos
3. Cada pessoa vê tudo ou só o que é dela?
   a) Cada profissional vê só a própria agenda; a recepção vê todas (recomendada)
   b) Todos veem tudo
4. A clínica é uma só ou o sistema atende várias clínicas separadas?

## 3. Dia a dia
5. Quais são as 3 a 5 coisas mais feitas? (ex.: marcar, remarcar, cancelar, confirmar, ver o dia)

## 4. Dados
6. Que informações do paciente precisam ficar guardadas? Tem prontuário ou dado de saúde?

## 5. Integrações
7. Quer aviso por WhatsApp ou e-mail?
   a) WhatsApp (recomendada)  b) E-mail  c) Os dois  d) Nenhum
8. Hoje existe planilha ou outro sistema para trazer os dados?

## 6. Onde usa
9. Onde as pessoas vão usar?
   a) Computador da recepção + celular só para consulta (recomendada)
   b) Só computador  c) Só celular

## 7. Visual
10. Tem logo, cores ou algum site que você gosta?

## 8. Escala e orçamento
11. Quantos atendimentos por dia hoje? E em um ano?
12. Se o sistema ficar fora do ar por uma hora, o que acontece?
13. Quanto pode gastar por mês e quem cuida depois?
```

Quando a resposta vier vaga, use o porquê:

```markdown
Cliente: "Preciso de um app."
Você: "Quem vai usar e onde? Na recepção, no computador, ou o paciente no celular?"
Cliente: "O paciente, no celular."
Registro: usa no celular. Um site que se adapta ao celular resolve; app instalado só se precisar de notificação ou offline.
```

Modelo do resumo final, para o cliente dar o ok:

```markdown
## O que entendi
- **Problema:** clínica perde consultas por falta de confirmação.
- **Quem usa:** recepção e profissionais (paciente só recebe aviso).
- **MVP:** marcar, remarcar, cancelar, ver agenda do dia, aviso por WhatsApp.
- **Fica para depois:** pagamento online, prontuário.
- **Dados:** nome, telefone, histórico de consultas (dado pessoal: LGPD).
- **Onde usa:** computador na recepção; celular só para consulta.
- **Escala:** cerca de 60 atendimentos por dia, uma clínica.
- **Orçamento:** até R$ X por mês; quem mantém: a equipe de TI.

## O que assumi (corrija se estiver errado)
- Login por e-mail e senha.
- Horário comercial de segunda a sexta.
- Fora do ar por poucas horas não é crítico.

Posso seguir com esse escopo? Responda "ok" ou diga o que mudar.
```

## Combina com / alternativas

- [Escopo do MVP](02-escopo-do-mvp.md): o resumo aprovado decide o que entra e o que fica de fora.
- [Fluxos e jornadas](03-fluxos-e-jornadas.md): as "3 a 5 coisas do dia a dia" viram fluxos.
- [Histórias e critérios de aceite](04-historias-e-criterios-de-aceite.md): cada funcionalidade vira história.
- [Regras de negócio](05-regras-de-negocio.md): as exceções ditas na conversa viram regras.
- [Backlog e ordem de construção](06-backlog-e-ordem-de-construcao.md): as prioridades do cliente definem a fila.
- [Onde registrar](07-onde-registrar.md): onde guardar o resumo aprovado.
- Alternativas: observar o trabalho do cliente por um dia; oficina rápida com a equipe; protótipo de tela para o cliente reagir.

## Decisão rápida

- **Use se:** o pedido é vago, o projeto é novo ou a funcionalidade é grande.
- **Evite se:** é um ajuste pequeno e bem descrito, ou o cliente já entregou um escopo claro e aprovado.
