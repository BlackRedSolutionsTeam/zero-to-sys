# Suporte ao cliente: triagem, SLA e ligação com o backlog

> Receba os pedidos num só lugar, classifique rápido, responda no prazo e devolva ao produto o que se repete.

| | |
|---|---|
| **Referência** | https://www.chatwoot.com/pricing, https://github.com/chatwoot/chatwoot, https://www.atlassian.com/software/statuspage/pricing |
| **Categoria** | Operação |
| **Tipo** | Prática de atendimento, com ferramentas de caixa de entrada |
| **Vale para** | Qualquer sistema com usuário externo |
| **Verificado em** | 2026-11-25 |

## O que é

Suporte é o fluxo que leva um pedido do cliente (dúvida, erro, sugestão) até a resposta e, quando for o caso, até o backlog. **Triagem** é classificar na entrada: tipo, gravidade e dono. **SLA de atendimento** é o prazo prometido de primeira resposta e de resolução. Não confunda com o SLA de disponibilidade (ver [SLO](01-slo-severidade-e-plantao.md)).

## Por que usar

- Nenhum pedido se perde em conversas soltas.
- O cliente sabe o que esperar.
- Erros repetidos viram melhoria no produto em vez de apagar incêndio.

## Quando usar

- Quando houver o primeiro cliente fora do time.
- Quando o suporte começar a competir com o desenvolvimento.
- Quando o contrato citar prazo de resposta.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Um e-mail de contato basta |
| MVP de SaaS | ✅ Ótimo | Caixa compartilhada e etiquetas |
| SaaS em crescimento | ✅ Ótimo | Ferramenta de atendimento e SLA por plano |
| Sistema interno | 🟡 Serve | Canal da empresa com formulário |
| App mobile | ✅ Ótimo | Chat dentro do app e captura de versão e aparelho |
| Pedidos pelo WhatsApp pessoal de um dev | ❌ Evite | Sem histórico, sem prazo, sem substituto |

## Quando é bom

- **Um canal de entrada** principal (e-mail ou chat), com os outros redirecionados.
- **Triagem por gravidade** que conversa com as severidades.
- **Respostas prontas** para as 10 perguntas mais comuns.
- **Etiqueta de causa:** bug, dúvida, pedido, cobrança.

## Quando é ruim

- **Prazo sem capacidade:** prometer 1 hora com uma pessoa em tempo parcial.
- **Reportar bug sem reprodução**: peça passos, versão e captura de tela.
- **Backlog virando lixeira** de tudo que o cliente falou.
- **Ferramenta cara demais** para o volume.

## Como começar

Ferramentas (conferidas em 2026-11-25 na página oficial do Chatwoot; outras: confira antes de assinar):

| Ferramenta | Grátis | Pago |
|---|---|---|
| Chatwoot Cloud | Hacker: até 2 agentes, 500 conversas por mês, só chat ao vivo, retenção de 30 dias | Startups US$ 19, Business US$ 39 e Enterprise US$ 99 por agente/mês |
| Chatwoot autohospedado | Existe versão aberta; a página não informou preço nem licença | Veja a licença no repositório antes de adotar |
| E-mail compartilhado | Caixa `suporte@` com etiquetas | Sem custo adicional |

Triagem na entrada:

| Gravidade | Exemplo | Primeira resposta | Ação |
|---|---|---|---|
| Crítica | Cliente não consegue usar o sistema | 1 hora útil | Vira SEV1/SEV2 ([incidente](04-atender-um-incidente.md)) |
| Alta | Função principal com erro e há contorno | 4 horas úteis | Ticket com prioridade no sprint |
| Normal | Dúvida de uso, erro menor | 1 dia útil | Responde e etiqueta |
| Baixa | Sugestão | 3 dias úteis | Registra e agradece |

Prazos são exemplos; defina conforme sua capacidade e o plano do cliente.

Modelo de pedido que a pessoa de suporte preenche ao abrir um bug:

```text
Título: Confirmação de agendamento volta erro 500 ao escolher horário após 18:00
Cliente: Clínica Aurora (plano Pro)
Gravidade: Alta
Passos: 1) Entrar 2) Agenda 3) Escolher dia 26/11 às 18:30 4) Confirmar
Esperado: consulta confirmada
Ocorreu: mensagem "Algo deu errado"
Versão/aparelho: web, Chrome 130, Windows 11
Captura/log: link
Quantos clientes afetados: 3 relatos hoje
```

Ligação com o backlog:

- Todo bug confirmado vira item no backlog com link para as conversas.
- Pedido repetido (3 ou mais clientes) sobe de prioridade e vai para a priorização da skill `product`.
- Resposta de encerramento avisa o cliente quando a correção sai (changelog).
- Revisão semanal de 15 minutos: abertos, mais antigos, repetidos.

## Combina com / alternativas

- [Página de status](05-pagina-de-status-e-comunicacao.md): aponte o cliente para ela durante incidentes.
- [Revisão operacional mensal](08-revisao-operacional-mensal.md): tempo de resposta e motivos mais comuns.
- Backlog e priorização: skill `product`.
- Alternativas: HelpScout, Freshdesk, Crisp (preços não conferidos aqui) ou issues no GitHub para produto aberto.

## Decisão rápida

- **Use se:** tem cliente pagante: um canal, quatro gravidades, prazos honestos e ligação com o backlog.
- **Evite se:** pretende prometer atendimento 24 horas sem plantão.
