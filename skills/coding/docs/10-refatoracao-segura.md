# Refatoração segura em passos pequenos

> Melhore a estrutura sem mudar o comportamento, um passo pequeno por vez, com testes rodando a cada passo.

| | |
|---|---|
| **Referência** | Refactoring, 2ª ed. (M. Fowler, 2018); Working Effectively with Legacy Code (M. Feathers, 2004); refactoring.com (catálogo) |
| **Categoria** | Manutenção |
| **Tipo** | Prática de processo |
| **Vale para** | Qualquer linguagem; editores e IDEs oferecem refatorações automáticas (renomear, extrair função) |
| **Verificado em** | 2026-11-24 |

## O que é

Refatorar é mudar o jeito como o código está escrito sem mudar o que ele faz. Fowler define como uma sequência de passos pequenos, cada um preservando o comportamento. O catálogo de passos tem nomes: Extract Function, Rename Variable, Inline Function, Move Function.

Segurança vem de duas coisas: testes que provam que o comportamento não mudou, e passos tão pequenos que, se algo quebra, você sabe qual foi.

## Por que usar

- **Código continua mudável:** refatorar torna o código mais fácil de entender e de modificar.
- **Risco baixo:** passos pequenos e verificados por testes.

## Quando usar

- Antes de adicionar uma funcionalidade difícil de encaixar.
- Ao ver função grande, nome ruim ou duplicação de verdade.
- Ao corrigir um bug em código confuso.
- Em legado, depois de colocar uma rede mínima de testes.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Código com testes | ✅ Ótimo | Catálogo de passos nomeados (refactoring.com/catalog) |
| Legado sem testes | 🟡 Serve | Primeiro escreva testes de caracterização (Feathers, Working Effectively with Legacy Code, 2004), depois refatore |

## Quando é bom

- **Um passo, um teste:** renomear, rodar testes, commitar.
- **Separado de funcionalidade:** commit de refatoração e commit de comportamento nunca se misturam.
- **Ferramenta faz o trabalho:** renomear e extrair pelo editor é mais seguro que à mão.
- **Regra do escoteiro** deixe o código um pouco melhor do que encontrou, no que você já está tocando.

## Quando é ruim

- **Refatoração gigante:** perde a vantagem dos passos pequenos e verificáveis. Prefira passos incrementais.
- **Refatorar sem teste:** você acha que não mudou nada, e mudou.
- **Misturar com funcionalidade:** o PR fica impossível de revisar.
- **Reescrever do zero:** Joel Spolsky ("Things You Should Never Do, Part I", 2000) chamou de "the single worst strategic mistake that any software company can make". Prefira estrangular aos poucos.
- **Divergência:** alguns times só aceitam refatoração junto de tarefa de negócio; outros reservam tempo próprio. Ambos funcionam, desde que o tempo exista.

## Como começar

Antes:

```ts
function price(o: Order) {
  let t = 0;
  for (const i of o.items) t += i.p * i.q;
  if (o.vip) t = t * 0.9;
  return t;
}
```

Passo 1, renomear (testes rodam). Passo 2, extrair a função (testes rodam). Depois:

```ts
function price(order: Order) {
  const subtotal = sumItems(order.items);
  return order.isVip ? applyVipDiscount(subtotal) : subtotal;
}
```

Receita:

1. Garanta testes que cobrem o comportamento (ou escreva-os primeiro).
2. Faça uma mudança mínima.
3. Rode os testes.
4. Commit. Repita.

Se os testes falham, desfaça o passo; não conserte em cima.

## Combina com / alternativas

Combina com:
- [Testes](08-testes.md): a rede de segurança.
- [Funções pequenas](02-funcoes-pequenas.md) e [Nomes claros](01-nomes-claros.md): os primeiros passos.
- [Commits e PRs pequenos](11-commits-e-prs-pequenos.md): um passo, um commit.

Alternativas: reescrita (arriscada), padrão "strangler" (estrangular o sistema antigo aos poucos; Fowler, "StranglerFigApplication", bliki).

## Decisão rápida

- **Use se:** vai mexer em código bagunçado e há (ou pode haver) testes.
- **Evite se:** o código é estável e ninguém o toca, ou a entrega é amanhã e não há rede de testes.
