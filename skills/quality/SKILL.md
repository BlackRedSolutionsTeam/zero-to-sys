---
name: quality
description: Define como provar que o sistema funciona — estratégia de testes por camada (pirâmide ou troféu), testes de unidade das regras de negócio, testes de integração com banco real (Testcontainers), testes de API e de contrato, ponta a ponta com Playwright nos fluxos principais, acessibilidade e desempenho automáticos (axe, Lighthouse CI), o que barra o PR no CI, a definição de pronto de cada funcionalidade e como o agente de IA verifica o próprio trabalho. Use sempre que for planejar ou escrever testes de uma funcionalidade, configurar o CI de qualidade, ou quando o usuário perguntar "como testar isso", "escreve os testes", "teste e2e", "Playwright", "o que barra o PR", "está pronto?", "definição de pronto" ou "como sei que o agente não quebrou nada". Não decide como escrever um teste legível nem lint e format (skill coding), nem o pipeline de deploy e os ambientes (skill infra).
---

# quality

Guia para provar, com teste e com o sistema rodando, que cada funcionalidade faz o que o critério de aceite diz. Sem isso, "pronto" é opinião. Cada critério de aceite da skill `product` vira pelo menos um teste, na camada mais barata que consegue prová-lo. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e configuração pronta para copiar.

## Como usar esta skill

1. **Leia os critérios de aceite** do item no `BACKLOG.md` (skill `product`). Eles são a lista do que precisa ser provado.
2. **Escolha a camada de cada critério** pela tabela abaixo e pelo [doc 01](docs/01-piramide-de-testes.md): regra pura na unidade, rota e banco na integração, fluxo principal no ponta a ponta.
3. **Escreva os testes** seguindo o doc da camada. Para o estilo do teste (nome, arrange-act-assert, o que não mockar), siga a skill `coding`, doc 08.
4. **Rode tudo localmente** e leia a saída. Teste que nunca falhou não prova nada: confira que ele falha sem o código.
5. **Confira os quality gates do CI** ([doc 07](docs/07-quality-gates-no-ci.md)); se o projeto ainda não tem, crie.
6. **Feche com a definição de pronto** ([doc 08](docs/08-definition-of-done.md)) e mostre a evidência: comandos rodados, resultado, e screenshot quando há tela ([doc 09](docs/09-verificacao-pelo-agente.md)).

## Onde testar cada coisa

| O que provar | Camada | Documento |
|---|---|---|
| Cálculo, regra de negócio, transição de estado | Unidade | [02](docs/02-testes-de-unidade.md) |
| Rota ou ação com banco, constraint, isolamento entre empresas | Integração com banco real | [03](docs/03-testes-de-integracao-com-banco.md) |
| Status, formato de erro, permissão, contrato com o front | API e contrato | [04](docs/04-testes-de-api-e-contrato.md) |
| Fluxo principal do usuário, de ponta a ponta | Ponta a ponta (Playwright) | [05](docs/05-ponta-a-ponta-com-playwright.md) |
| Contraste, rótulos, teclado; velocidade da página | Automático (axe, Lighthouse CI) | [06](docs/06-acessibilidade-e-desempenho-automaticos.md) |

## Quanto testar por projeto

| Projeto | Unidade | Integração | API e contrato | Ponta a ponta | Acessibilidade e desempenho |
|---|---|---|---|---|---|
| Site de conteúdo, landing | Pouco | Formulários e integrações | Raro | Páginas principais | Sim: é o que mais pesa |
| MVP de SaaS | Regras de negócio | A maior parte dos testes | Status e permissão | 1 a 3 fluxos principais | axe nas telas principais |
| SaaS em crescimento | Sim | Sim | + contrato com o front | Todos os fluxos críticos | axe e Lighthouse CI no PR |
| Sistema interno, corporativo | Sim | Sim | Sim | Fluxos com aprovação e papéis | axe; desempenho nas telas pesadas |
| API, integração | Regras | Sim | O centro dos testes | Não se aplica | Não se aplica |
| App mobile | Regras | API do backend | Sim | Maestro ou Detox nos fluxos principais | Acessibilidade da plataforma |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Pirâmide de testes | [docs/01-piramide-de-testes.md](docs/01-piramide-de-testes.md) | Estratégia: o que testar em cada camada |
| Testes de unidade | [docs/02-testes-de-unidade.md](docs/02-testes-de-unidade.md) | Regras de negócio puras, sem banco nem rede |
| Integração com banco | [docs/03-testes-de-integracao-com-banco.md](docs/03-testes-de-integracao-com-banco.md) | Banco real, migrations reais, isolamento |
| API e contrato | [docs/04-testes-de-api-e-contrato.md](docs/04-testes-de-api-e-contrato.md) | Testar como o cliente usa; não quebrar o front |
| Ponta a ponta | [docs/05-ponta-a-ponta-com-playwright.md](docs/05-ponta-a-ponta-com-playwright.md) | Fluxos principais no navegador |
| Acessibilidade e desempenho | [docs/06-acessibilidade-e-desempenho-automaticos.md](docs/06-acessibilidade-e-desempenho-automaticos.md) | axe e Lighthouse CI |
| Quality gates no CI | [docs/07-quality-gates-no-ci.md](docs/07-quality-gates-no-ci.md) | O que barra o PR |
| Definição de pronto | [docs/08-definition-of-done.md](docs/08-definition-of-done.md) | Quando um item está pronto de verdade |
| Verificação pelo agente | [docs/09-verificacao-pelo-agente.md](docs/09-verificacao-pelo-agente.md) | Como o agente prova o que fez |

## Regras de uso

- **Um teste por critério de aceite, no mínimo.** Critério sem teste não está provado; teste sem critério pode estar testando a coisa errada.
- **A camada mais barata que prova o critério.** Ponta a ponta é caro e lento; use só para o fluxo, não para cada regra.
- **Banco real nos testes de integração.** Mock do ORM esconde erro de SQL, de constraint e de migration.
- **Teste falha antes de passar.** Confira que o teste quebra sem o código ou com o bug; senão ele não protege nada.
- **Nunca afrouxe um teste para ele passar.** Se o teste está errado, diga por quê e corrija; se o código está errado, corrija o código.
- **Teste instável é bug.** Conserte ou remova com issue aberta; não deixe "às vezes falha" no CI.
- **Cobertura é sinal, não meta.** Use para achar o que ficou sem teste, não como número a bater.
- **Pronto com evidência.** Mostre a saída dos comandos e, se houver tela, o screenshot. "Funcionou" sem prova não fecha o item.
- **Fronteiras.** O estilo do teste, lint e format são da `coding`; o pipeline de deploy e os ambientes são da `infra`; os critérios vêm da `product`. Esta skill decide o que testar, onde, e quando está pronto.

## Quando a lista não cobre

Teste de carga e estresse (k6, Gatling), testes de segurança dinâmicos (OWASP ZAP), teste de mutação, testes visuais por screenshot e testes em dispositivos reais em nuvem ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial da ferramenta.

## Validade dos dados

Comandos, opções e versões das ferramentas foram conferidos em 2026-11-24. Cada documento tem a linha "Verificado em"; confira a versão instalada no projeto antes de copiar uma configuração.
