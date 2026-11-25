# Pirâmide de testes

> Decida quantos testes de cada tipo escrever, e em que camada cada critério de aceite é provado, antes de escrever o primeiro teste.

| | |
|---|---|
| **Referência** | Mike Cohn, "Succeeding with Agile" (Addison-Wesley, 2009), origem da pirâmide; Martin Fowler, "TestPyramid" (martinfowler.com/bliki/TestPyramid.html); Kent C. Dodds, "The Testing Trophy and Testing Classifications" (kentcdodds.com); Vitest (vitest.dev), Playwright (playwright.dev), pytest (docs.pytest.org), xUnit (xunit.net) |
| **Categoria** | Qualidade |
| **Tipo** | Prática de estratégia de testes |
| **Vale para** | Qualquer linguagem e qualquer time, com ou sem agente de IA |
| **Verificado em** | 2026-11-24 |

## O que é

Testes automatizados se dividem por tamanho:

- **Unidade:** testa uma função ou classe isolada, sem banco e sem rede. Roda em milissegundos.
- **Integração:** testa várias peças juntas, como a rota da API com o banco real. Roda em segundos.
- **Ponta a ponta (e2e):** abre o sistema como o usuário, no navegador ou no app. Roda em dezenas de segundos.

A **pirâmide** (Cohn, 2009; Fowler) manda ter muitos testes de unidade na base, menos de integração no meio e poucos e2e no topo. Quanto mais alto, mais lento, mais caro e mais frágil.

O **troféu** (Dodds) muda a proporção: análise estática (tipos e lint) na base, poucos testes de unidade, **muitos de integração** e poucos e2e. A ideia é que o teste de integração dá mais confiança por real gasto.

Para a escrita do teste em si (nome, estrutura, o que evitar), veja [Testes](../../coding/docs/08-testes.md).

## Por que usar

- **Confiança sem lentidão:** a suíte roda inteira em minutos, e todo PR passa por ela.
- **Falha fácil de achar:** teste baixo aponta a linha; teste alto aponta só o fluxo.
- **Sem teste duplicado:** cada critério é provado na camada mais barata que o prova.

## Quando usar

- Ao começar o passo "Testes" de cada funcionalidade.
- Ao montar o projeto, para decidir ferramentas e pastas de teste.
- Quando a suíte está lenta ou instável: sinal de e2e demais.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Quase sem regra; basta build, links e um e2e do formulário de contato |
| MVP de SaaS | ✅ Ótimo | Regra de negócio testada em unidade, API com banco real e poucos e2e |
| SaaS em crescimento | ✅ Ótimo | Muitos papéis e regras; a divisão evita suíte lenta |
| Sistema interno/corporativo | ✅ Ótimo | Regra pesada e telas de CRUD; integração cobre quase tudo |
| API/integração | ✅ Ótimo | Sem tela: unidade, integração e contrato; e2e quase some |
| App mobile | 🟡 Serve | Teste de componente e poucos fluxos no aparelho; e2e mobile é caro |
| Protótipo descartável | ❌ Evite | Teste custa mais que jogar o protótipo fora |

## Quando é bom

- **Camada certa:** regra pura em unidade, rota com banco em integração, jornada em e2e.
- **Poucos e2e, bem escolhidos:** só os fluxos que dão dinheiro ou travam o uso.
- **Banco real nos testes de integração:** mock de banco esconde erro de SQL, constraint e migration.

## Quando é ruim

- **Pirâmide invertida:** muito e2e e pouca unidade. Suíte lenta e instável.
- **Unidade demais em código sem regra:** teste que só repete o código.
- **Dogma:** pirâmide e troféu são guias. O que decide é onde o erro mais provável mora.

## Como começar

### O que recomendar por tipo de projeto

| Projeto | Distribuição sugerida |
|---|---|
| SaaS web (API + banco) | Unidade nas regras de negócio puras; **muitos de integração na API com banco real**; poucos e2e só nos fluxos principais |
| Sistema interno de CRUD | Quase tudo em integração; unidade só onde há cálculo ou regra; 1 e2e por fluxo crítico |
| API pública | Unidade nas regras, integração em cada rota, contrato para quem consome |
| App mobile | Unidade na lógica, teste de componente nas telas, e2e só do login e do fluxo principal |

### O que testar em cada camada

| O que você quer provar | Camada | Exemplo na clínica |
|---|---|---|
| Regra de negócio | Unidade | Cancelamento grátis até 24 h antes da consulta |
| Rota ou ação com banco | Integração | `POST /agendamentos` grava e devolve 201; horário ocupado devolve 409 |
| Contrato da API | Contrato | A resposta de `GET /pacientes` tem os campos que o app espera |
| Fluxo principal | e2e | Paciente agenda uma consulta pelo navegador |
| Acessibilidade e desempenho | Automático | Tela de agenda sem violação de contraste; lista abre em menos de 2 s |

### Do critério de aceite ao teste

Regra: cada **Dado / Quando / Então** vira **ao menos um teste**, na **camada mais barata que prova o critério**. Origem dos critérios: [Histórias e critérios de aceite](../../product/docs/04-historias-e-criterios-de-aceite.md).

| Critério (Dado / Quando / Então) | Camada | Teste |
|---|---|---|
| Dado consulta em 30 h, quando cancelo, então sem taxa | Unidade | `cobra 0 de taxa com 30 h de antecedência` |
| Dado consulta em 2 h, quando cancelo, então taxa de 50% | Unidade | `cobra 50% de taxa com 2 h de antecedência` |
| Dado horário ocupado, quando agendo, então erro 409 | Integração | `POST /agendamentos` em horário ocupado |
| Dado paciente sem permissão, quando abre a agenda, então 403 | Integração | rota com usuário sem papel |
| Dado paciente logado, quando agenda e confirma, então vê na lista | e2e | jornada completa, uma vez |

Comece pelo critério: se uma regra pode ser provada em unidade, não suba para integração.

### O que não testar

- **Getter e setter simples** e código sem decisão.
- **O framework:** que o Express roteia, que o ORM grava. Já é testado por quem o fez.
- **A biblioteca:** não teste se o `zod` valida e-mail. Teste a sua regra que usa o `zod`.
- **Detalhe de implementação:** nome de função interna, ordem de chamadas.

### Ferramentas por stack

| Stack | Unidade | Integração | e2e |
|---|---|---|---|
| TypeScript | Vitest ou Jest | Vitest + banco real (Testcontainers) | Playwright |
| .NET | xUnit ou NUnit | WebApplicationFactory | Playwright |
| Python | pytest | pytest, pytest-django | Playwright |
| PHP | PHPUnit ou Pest | PHPUnit ou Pest com banco de teste | Playwright |
| Go | go test | go test com banco de teste | Playwright |
| Java | JUnit 5 | Spring Boot Test | Playwright |
| Mobile | Jest + React Native Testing Library, flutter test | Testing Library | Maestro, Detox |

## Combina com / alternativas

Combina com:
- [Testes de unidade](02-testes-de-unidade.md): a base da pirâmide.
- [Testes de integração com banco](03-testes-de-integracao-com-banco.md): o meio, ou o centro do troféu.
- [Testes de API e contrato](04-testes-de-api-e-contrato.md).
- [Ponta a ponta com Playwright](05-ponta-a-ponta-com-playwright.md): o topo.
- [Acessibilidade e desempenho automáticos](06-acessibilidade-e-desempenho-automaticos.md).
- [Quality gates no CI](07-quality-gates-no-ci.md): o que barra o PR.

Alternativas: troféu de Dodds (mais integração), testes manuais exploratórios para o que não vale automatizar.

## Decisão rápida

- **Use se:** o projeto tem regra de negócio ou vai durar mais que algumas semanas.
- **Evite se:** o código é descartável; ou se for usar a pirâmide como cota a cumprir em vez de guia.
