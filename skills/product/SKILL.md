---
name: product
description: Transforma o pedido do cliente em produto definido antes de escrever código — entrevista em linguagem do cliente, escopo do MVP (dentro, fora e depois), fluxo principal e jornadas, histórias de usuário com critérios de aceite em Dado/Quando/Então, regras de negócio e máquina de estados, e backlog em ordem de construção com fatias verticais. Use sempre que for começar um sistema ou uma funcionalidade nova e o "o que fazer" ainda não estiver claro, ou quando o usuário pedir "o que entra no MVP", "escreve as histórias", "critérios de aceite", "monta o backlog", "quais são as regras de negócio", "por onde começo a construir" ou "como saber quando está pronto". Não decide stack (skill stacks), modelo de dados (skill data), layout de tela (skill design-systems) nem como testar (skill coding).
---

# product

Guia para decidir **o que** construir antes de decidir **como**. A saída desta skill é o que todas as outras usam: o escopo diz o tamanho da stack e da infra, as regras de negócio viram o modelo de dados, o fluxo vira as telas e os critérios de aceite dizem ao agente quando um item terminou. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e modelos prontos para copiar.

## Como usar esta skill

1. **Leia o que já existe** antes de perguntar: o pedido, o `README`, issues, planilhas ou prints que o cliente mandou, e o código, se houver. Pergunte só o que continuar sendo dúvida.
2. **Entreviste em uma ou duas rodadas** seguindo o [doc 01](docs/01-entrevista-com-o-cliente.md). Feche com um resumo e espere o ok.
3. **Corte o escopo do MVP** com o quadro Dentro / Fora / Depois do [doc 02](docs/02-escopo-do-mvp.md).
4. **Escreva o fluxo principal** passo a passo, com os caminhos de erro ([doc 03](docs/03-fluxos-e-jornadas.md)).
5. **Escreva as regras de negócio** com id (RN-01) e a máquina de estados das entidades que mudam de situação ([doc 05](docs/05-regras-de-negocio.md)).
6. **Quebre em histórias com critérios de aceite** em Dado / Quando / Então ([doc 04](docs/04-historias-e-criterios-de-aceite.md)).
7. **Ordene o backlog** em fatias verticais, com o primeiro item andando de ponta a ponta ([doc 06](docs/06-backlog-e-ordem-de-construcao.md)).
8. **Registre no projeto** (`README`, `BACKLOG.md`, `docs/regras-de-negocio.md`) e aponte para eles no `CLAUDE.md` ([doc 07](docs/07-onde-registrar.md)).
9. **Mostre o resultado ao usuário** em poucas linhas: o que entra no MVP, quantos itens tem o backlog e qual é o primeiro.

## Quanto aprofundar

| Projeto | Entrevista | Escopo | Fluxos | Regras e estados | Histórias e critérios | Backlog |
|---|---|---|---|---|---|---|
| Site de conteúdo, landing | Curta: público, objetivo, seções | Lista de páginas | Só o caminho até a conversão | Raramente | Só para formulários e integrações | Lista de páginas em ordem |
| MVP de SaaS | Completa, uma rodada | Quadro Dentro / Fora / Depois | Fluxo principal e erros | Sim, das entidades centrais | Sim, em todo item | Sim, 8 a 20 itens |
| SaaS em crescimento | Por funcionalidade nova | Por entrega | Fluxo da funcionalidade | Sim, e revisar as antigas | Sim | Sim, contínuo |
| Sistema interno, corporativo | Completa, com quem usa no dia a dia | Quadro, alinhado com o gestor | Sim, com aprovações e papéis | Sim, é o centro do sistema | Sim | Sim |
| API, integração | Com quem vai consumir | Lista de operações | Sequência das chamadas | Sim, limites e validações | Sim, por operação | Sim |
| App mobile | Completa, com onde e como usa | Quadro | Sim, com offline e notificações | Sim | Sim | Sim |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Entrevista | [docs/01-entrevista-com-o-cliente.md](docs/01-entrevista-com-o-cliente.md) | Descobrir o problema, o público e as funcionalidades em linguagem do cliente |
| Escopo do MVP | [docs/02-escopo-do-mvp.md](docs/02-escopo-do-mvp.md) | O que fica dentro, fora e depois; como cortar |
| Fluxos e jornadas | [docs/03-fluxos-e-jornadas.md](docs/03-fluxos-e-jornadas.md) | Fluxo principal, erros, estados de tela, story mapping |
| Histórias e critérios de aceite | [docs/04-historias-e-criterios-de-aceite.md](docs/04-historias-e-criterios-de-aceite.md) | Como escrever cada item e como saber que terminou |
| Regras de negócio | [docs/05-regras-de-negocio.md](docs/05-regras-de-negocio.md) | O que pode e o que não pode; máquina de estados |
| Backlog | [docs/06-backlog-e-ordem-de-construcao.md](docs/06-backlog-e-ordem-de-construcao.md) | Fatias verticais e ordem de construção |
| Onde registrar | [docs/07-onde-registrar.md](docs/07-onde-registrar.md) | `README`, `BACKLOG.md`, issues e o que o agente lê |

## Checklist de todo escopo antes de construir

- [ ] O problema a resolver e o público estão escritos em uma ou duas frases (`head README.md`).
- [ ] O escopo tem as listas dentro, fora e depois (`grep -niE 'dentro|fora|depois' README.md BACKLOG.md`).
- [ ] Todo item do backlog tem critério de aceite verificável, sem "rápido" nem "fácil" (`grep -c 'Critério' BACKLOG.md`).
- [ ] O fluxo principal e os fluxos de erro estão descritos, com estados de tela vazio, carregando e erro (`ls docs`).
- [ ] As regras de negócio estão em `docs/regras-de-negocio.md`, com a máquina de estados das entidades que mudam de status (`ls docs/regras-de-negocio.md`).
- [ ] Os nomes do sistema usam as palavras do cliente, iguais no documento e no código (`grep -rn` pelos termos principais).
- [ ] O primeiro item do backlog atravessa dados, API e tela e prova o deploy (`head -30 BACKLOG.md`).
- [ ] Cada item é uma fatia vertical, não uma camada como "fazer todo o banco" (`grep -niE 'todo o banco|toda a api' BACKLOG.md`).
- [ ] O que foi decidido está no repositório (README, BACKLOG, docs), e não só na conversa (`git status docs README.md BACKLOG.md`).

## Regras de uso

- **Problema antes de solução.** Entenda o que o usuário precisa resolver antes de aceitar "precisa de um app" ou "precisa de um dashboard". O pedido do cliente é uma pista, não a especificação.
- **Linguagem do cliente.** Pergunte e escreva com as palavras de quem usa o sistema ("agendamento", "paciente", "remarcar"). Os mesmos nomes vão para o código.
- **Assuma o padrão sensato e diga qual assumiu.** Pergunte só o que não tem resposta óbvia para o tipo de projeto.
- **Todo item tem critério de aceite verificável.** "Rápido" e "fácil de usar" não são critérios. Sem critério, o item não entra no backlog.
- **Corte funcionalidade, não qualidade.** Um MVP pequeno ainda tem login seguro, backup e tratamento de erro. O que sai é a funcionalidade inteira, não o cuidado.
- **Fatia vertical, não camada.** Cada item do backlog atravessa dados, API e tela e entrega algo usável. Não planeje "fazer todo o banco primeiro".
- **O primeiro item anda de ponta a ponta.** Ele prova a stack, o deploy e o fluxo principal antes de o resto ser construído.
- **Registre no repositório, não na conversa.** O que foi decidido vai para `README`, `BACKLOG.md` e `docs/regras-de-negocio.md`. Não crie documento de planejamento solto.
- **Atualize junto com o código.** O status do item muda no mesmo PR que o entrega; regra nova entra no doc antes ou junto com o código que a implementa.
- **Fronteiras.** Esta skill não escolhe stack (`stacks`), tabelas (`data`), layout (`design-systems`) nem ferramenta de teste (`coding`). Ela entrega o que essas skills precisam para decidir.

## Quando a lista não cobre

Pesquisa de mercado, precificação, discovery com muitos usuários, testes A/B e métricas de produto ficam fora desta skill. Diga isso ao usuário e cubra com a referência do tema; para métricas de uso, veja a observabilidade na skill `infra`.

## Validade dos dados

Esta skill traz práticas, não preços nem versões. As referências (livros, autores e sites) foram conferidas em 2026-11-24; cada documento tem a linha "Verificado em".
