# Custo x desempenho

> Desempenho tem preço: pague só até a meta e compare sempre o custo da solução com o custo do problema.

| | |
|---|---|
| **Referência** | Skill `vps`, doc 01 (preços de VPS conferidos em 2026-11-25) e doc 02; skill `infra`, docs 01, 03 e 05 (preços de PaaS, nuvem e Postgres gerenciado); Grafana Cloud pricing (grafana.com/pricing) |
| **Categoria** | Desempenho |
| **Tipo** | Guia de decisão |
| **Vale para** | Qualquer projeto que paga por servidor, banco ou serviço gerenciado |
| **Verificado em** | 2026-11-25 |

## O que é

Cada ganho de desempenho custa dinheiro, tempo de quem desenvolve ou complexidade para operar. O objetivo não é o sistema mais rápido possível, e sim o sistema **dentro da meta** ([doc 01](01-medir-primeiro.md)) ao menor custo total, contando horas de pessoa.

Este doc não repete preços: eles mudam com frequência e já estão conferidos nas skills de origem. Consulte [vps, doc 01](../../vps/docs/01-as-5-melhores-vps-do-brasil.md) para as VPS do Brasil, [infra, doc 01](../../infra/docs/01-paas.md) para PaaS, [infra, doc 03](../../infra/docs/03-nuvem-grande.md) para nuvem e [infra, doc 05](../../infra/docs/05-postgres-gerenciado.md) para Postgres gerenciado, sempre com a data da conferência.

## Por que usar

- **Evita gastar à toa:** servidor maior para um problema que um índice resolvia.
- **Evita economizar errado:** perder cliente por lentidão custa mais que a diferença de plano.
- **Decisão defensável:** com custo e ganho em números, a escolha se explica para quem paga.

## Quando usar

- Antes de subir de plano ou contratar um serviço gerenciado.
- Quando a fatura cresce mais rápido que o uso.
- Ao escolher entre otimizar (tempo de pessoa) e escalar (dinheiro de infraestrutura).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | CDN e cache entregam muito desempenho por pouco |
| MVP de SaaS | ✅ Ótimo | Orçamento curto: a melhor troca é índice e cache, não servidor |
| SaaS em crescimento | ✅ Ótimo | Receita por cliente permite pagar por capacidade, mas só com meta clara |
| Sistema interno/corporativo | ✅ Ótimo | Poucos usuários: máquina modesta e consulta bem feita |
| API/integração | ✅ Ótimo | Custo por requisição é uma métrica útil |
| App mobile com backend | ✅ Ótimo | Pico por notificação: capacidade que sobe e desce paga menos |
| Otimizar além da meta | ❌ Evite | Cada hora a mais tem retorno cada vez menor |

## Quando é bom

- **Otimização no código e no banco** é o ganho com melhor custo-benefício: grátis em infraestrutura e vale para sempre.
- **Cache e CDN** tiram carga da origem por pouco dinheiro.
- **Vertical** tem custo previsível e nenhum trabalho de código.
- **Capacidade sob demanda** (instâncias que sobem e descem) cobra só o pico.

## Quando é ruim

- **Fatura de nuvem sem teto:** pague por uso sem alerta de orçamento e um laço infinito vira uma conta alta. Configure alerta de custo.
- **Infraestrutura "por garantia":** duas réplicas e um cluster para 20 usuários.
- **Barato que sai caro:** servidor mínimo que cai no pico e custa uma venda.
- **Complexidade escondida:** cada peça extra (Redis, fila, réplica, PgBouncer) tem custo de operação e de ser entendida por outra pessoa.
- **Economizar tirando observabilidade:** sem medir, o gasto cresce sem que se saiba por quê.

## Como começar

### Ordem de custo-benefício

| Ação | Custo típico | Retorno |
|---|---|---|
| Índice e correção de N+1 | Horas de pessoa | Muito alto, vale para sempre |
| Cache HTTP e CDN nos estáticos | Configuração | Alto, quase de graça |
| Cache de aplicação (Redis) | Uma peça nova a operar | Alto para leitura repetida |
| Tarefa pesada em fila | Worker e fila | Alto para latência e estabilidade |
| Subir o plano (vertical) | Mensalidade maior | Imediato, tem teto |
| Mais instâncias e réplica | Mensalidade, operação e conexões | Alto, mas só depois de tudo acima |

### Conta de decisão

Escreva em uma linha por opção, com número, no PR ou no `README`:

| Opção | Custo mensal | Ganho medido | Custo de operar |
|---|---|---|---|
| Índice composto em `appointment` | R$ 0 | p95 de 900 ms para 120 ms | Nenhum |
| Subir de 4 para 8 GB de RAM | Diferença do plano (consulte o provedor na data) | p95 de 900 ms para 700 ms | Nenhum |
| Redis para a listagem | Memória extra mais o tempo de operar | p95 de 120 ms para 40 ms | Monitorar e invalidar |

Os valores acima são exemplos de formato, não preços. O custo do plano você lê na página do provedor no dia.

### Controle de custo

- **Alerta de orçamento** no provedor de nuvem e no PaaS; muitos têm o recurso nativo.
- **Custo por unidade:** divida a fatura mensal por usuário ativo ou por mil requisições e acompanhe a tendência.
- **Revisão trimestral:** o que foi dimensionado para o pico de lançamento pode ser reduzido.
- **Desligar o que não usa:** ambientes de teste fora do horário, snapshots antigos, volumes soltos.
- **Observabilidade com teto:** os planos gratuitos têm limite (por exemplo, Grafana Cloud gratuito com 10 mil séries e 14 dias de retenção, conferido em 2026-11-25 em [infra, doc 10](../../infra/docs/10-observabilidade.md)); acompanhe o volume antes de pagar.

### Quando pagar por um serviço gerenciado

Pague quando o custo da sua hora de operação (backup, atualização, alta disponibilidade) for maior que a diferença de preço para o serviço gerenciado. Para banco em produção com cliente pagante, costuma ser. Veja [Postgres gerenciado](../../infra/docs/05-postgres-gerenciado.md) e [VPS ou saída para a nuvem](../../vps/docs/08-migrar-ou-sair-da-vps.md).

## Combina com / alternativas

- [Escalar](07-escalar-vertical-horizontal-e-replica.md) para o que cada passo exige.
- [Teste de carga](04-teste-de-carga-com-k6.md) para provar que o plano menor ainda atende.
- [Dimensionar a VPS](../../vps/docs/02-dimensionar-o-servidor.md) e [infra](../../infra/SKILL.md) para preço e plano.
- Alternativa: contrato anual de VPS ou instância reservada na nuvem reduz o preço por mês, em troca de prazo e de menos flexibilidade.

## Decisão rápida

- **Primeiro** o que não custa mensalidade: índice, N+1, cache HTTP.
- **Depois** o que custa pouco: cache de aplicação, fila, vertical.
- **Por último** o que custa e complica: horizontal, réplica, serviços gerenciados extras.
- **Pare** quando bater a meta; revise o gasto a cada trimestre.
