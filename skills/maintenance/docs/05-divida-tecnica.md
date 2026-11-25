# Dívida técnica: registrar, priorizar, pagar em fatias

> Anote cada dívida em uma lista única com custo e risco, ordene pelo que mais atrapalha e pague uma fatia pequena por ciclo, sem parar o projeto.

| | |
|---|---|
| **Referência** | Ward Cunningham, "The WyCash Portfolio Management System" (1992), origem da metáfora; Martin Fowler, "TechnicalDebtQuadrant" (martinfowler.com/bliki); Refactoring, 2ª ed. (M. Fowler, 2018); Google Engineering Practices, "Small CLs"; DORA (dora.dev/guides/dora-metrics) |
| **Categoria** | Manutenção |
| **Tipo** | Prática de gestão |
| **Vale para** | Qualquer projeto com código em evolução, em qualquer stack |
| **Verificado em** | 2026-11-25 |

## O que é

Dívida técnica é o custo futuro de uma escolha de hoje que facilitou entregar rápido e dificulta mudar depois. Fowler a divide em dois eixos: deliberada ou acidental, prudente ou imprudente. Dívida deliberada e prudente ("lançamos sem cache e vamos tratar depois da primeira venda") é uma decisão de negócio. A acidental ou imprudente é só bagunça.

Como o juro é cobrado: cada mudança leva mais tempo, cada bug é mais difícil de achar, o time evita mexer em certas partes.

## Por que usar

- **O que é visível se paga:** dívida invisível só aparece quando quebra.
- **Decisão com dados:** o registro mostra custo e risco, e vira argumento para o negócio.
- **Sem refatoração gigante:** fatias pequenas cabem no ciclo normal.

## Quando usar

- Ao assumir ou auditar um projeto (a skill `audit` gera os achados, [doc 03](../../audit/docs/03-priorizacao-e-plano.md)).
- Quando alguém diz "tenho medo de mexer nisso".
- Ao decidir entre uma funcionalidade nova e limpar a casa.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Uma lista curta basta |
| MVP de SaaS | ✅ Ótimo | Dívida deliberada é normal; registre para pagar depois |
| SaaS em crescimento | ✅ Ótimo | O juro cresce com o time; priorização evita brigas |
| Sistema interno/corporativo | ✅ Ótimo | Dono trocado e pouca documentação |
| API/integração | ✅ Ótimo | Dívida de contrato afeta quem consome |
| App mobile com backend | ✅ Ótimo | Dívida de versão de API trava a atualização do app |
| Projeto a ser desligado em semanas | ❌ Evite | O custo de pagar supera o do juro |

## Quando é bom

- **Lista única** (issues com um rótulo `divida-tecnica`), não uma planilha por pessoa.
- **Cada item com:** o que é, onde está, o que custa hoje, o risco e o tamanho da correção.
- **Orçamento fixo por ciclo:** por exemplo 15 a 20% da capacidade, ou uma tarefa de dívida por sprint.
- **Fatias de até um dia ou dois,** cada uma com valor próprio e PR pequeno (skill `coding`, [doc 11](../../coding/docs/11-commits-e-prs-pequenos.md)).
- **Pagar onde se mexe:** quem vai alterar um módulo já limpa o que está no caminho (regra do escoteiro).

## Quando é ruim

- **Sprint de limpeza gigante,** que para as entregas e nunca termina.
- **Tudo é dívida:** gosto pessoal de estilo não entra; lint e formatação resolvem (skill `coding`, doc 09).
- **Registrar e nunca olhar:** lista sem dono vira cemitério.
- **Reescrita do zero** para "pagar tudo": Spolsky a chamou de pior erro estratégico possível; prefira estrangular aos poucos.
- **Esconder a dívida** do negócio: o time paga com horas extras.

## Como começar

### Modelo de registro

Uma issue por dívida, com este corpo:

```markdown
## O que é
Cobrança de imposto calculada em três lugares diferentes.

## Onde
src/orders/tax.ts, src/invoices/calc.ts, src/reports/summary.ts

## Custo hoje
Cada mudança de alíquota exige 3 edições; já gerou 2 bugs no trimestre.

## Risco
Alto: afeta valor cobrado.

## Tamanho da correção
M (2 a 3 dias, em 3 fatias)

## Fatias
1. Extrair função única com testes
2. Trocar o uso em orders
3. Trocar invoices e reports
```

### Priorizar

Dê nota de 1 a 3 para três perguntas e some:

| Pergunta | 1 | 3 |
|---|---|---|
| Quanto atrapalha hoje? | Raramente | Toda semana |
| Qual o risco se der errado? | Baixo | Dinheiro, dados ou segurança |
| Quão barato é pagar? | Semanas | Horas |

Soma alta primeiro. Em empate, vence o que toca o código que será alterado a seguir. Itens de segurança e perda de dados passam à frente (skill `audit`, doc 03).

### Tipos comuns e a próxima ação

| Tipo | Exemplo | Ação | Onde |
|---|---|---|---|
| Versão vencida | Node sem suporte | Atualizar | [Doc 01](01-calendario-de-fim-de-suporte.md) e [03](03-atualizar-versao-maior-do-framework.md) |
| Dependência vulnerável | Pacote com CVE alto | Atualizar ou trocar | Skill `security`, doc 08 |
| Código duplicado ou confuso | Função de 300 linhas | Refatorar em passos | Skill `coding`, doc 10 |
| Sem testes | Fluxo de pagamento sem teste | Testes de caracterização | Skill `quality` |
| Pastas bagunçadas | Arquivo sem lugar | Reorganizar | Skill `architecture` |
| Sem uso | Módulo que ninguém chama | Remover | [Doc 06](06-codigo-morto-e-dependencias-sem-uso.md) |
| Manual | Deploy à mão | Automatizar | Skill `infra` |

### Pagar em fatias

1. Escolha o item de maior nota.
2. Corte em fatias que deixam o sistema funcionando a cada merge.
3. Escreva ou confirme o teste que cobre o trecho.
4. Um PR por fatia; commit de refatoração separado do de comportamento.
5. Feche a issue só quando a última fatia entra; a dívida some do código, não só da lista.

### Rever

A cada trimestre ([doc 07](07-rotina-trimestral-de-saude.md)): a lista cresceu ou encolheu? O que foi pago? Itens que ninguém tocou em dois trimestres e não causam dano são fechados com a justificativa "aceita".

## Combina com / alternativas

- Skill `audit`: [priorização e plano](../../audit/docs/03-priorizacao-e-plano.md).
- Skill `coding`: [refatoração segura](../../coding/docs/10-refatoracao-segura.md) e [commits pequenos](../../coding/docs/11-commits-e-prs-pequenos.md).
- Alternativa: ferramentas de análise estática com métricas de dívida (SonarQube e similares); confira o plano gratuito antes. Servem de apoio, não substituem o julgamento sobre o que atrapalha.

## Decisão rápida

- **Use se:** o projeto vai viver mais de seis meses.
- **Evite se:** a lista for virar fim em si; limite a 20 itens ativos.
