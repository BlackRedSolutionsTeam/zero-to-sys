# Funções pequenas e com uma responsabilidade

> Cada função faz uma coisa, em um nível de detalhe, e cabe na tela sem rolar.

| | |
|---|---|
| **Referência** | catálogo de refatorações (refactoring.com/catalog, "Extract Function"); página do livro A Philosophy of Software Design (web.stanford.edu/~ouster/cgi-bin/book.php) |
| **Categoria** | Estrutura do código |
| **Tipo** | Prática de escrita de código |
| **Vale para** | Qualquer linguagem; em linguagens orientadas a objeto vale também para métodos |
| **Verificado em** | 2026-11-24 |

## O que é

É quebrar uma função grande em funções menores, cada uma com um propósito claro e um nome que o diz. A função de cima fica como um sumário: lê-se de cima para baixo e conta a história.

Não existe número mágico. O catálogo de refatorações (refactoring.com/catalog) traz Extract Function para isso. Aqui o critério é: se você precisa de um comentário para dizer o que um trecho faz, esse trecho é uma função.

## Por que usar

- **Lê-se rápido:** o nível alto mostra o fluxo; o detalhe fica um clique abaixo.
- **Testa-se fácil:** função pequena tem poucas entradas e uma saída.
- **Reuso natural:** pedaços com nome viram peças.
- **Revisão melhor:** o diff mostra a intenção da mudança.

## Quando usar

- Função passou de uma tela ou tem mais de um nível de indentação de `if`/`for`.
- Há blocos separados por comentário ("// valida", "// calcula", "// salva").
- A função mistura regra de negócio com acesso a banco, HTTP ou formatação.
- Você não consegue dar um nome simples à função sem usar "e".

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Regra de negócio | ✅ Ótimo | Extract Function (refactoring.com/catalog) |
| Handlers de API / controllers | ✅ Ótimo | Extract Function (refactoring.com/catalog) |
| Algoritmos densos | 🟡 Serve | Ousterhout e Martin divergem sobre o tamanho dos métodos (web.stanford.edu/~ouster/cgi-bin/book.php) |

## Quando é bom

- **Uma responsabilidade:** a função muda por um único motivo.
- **Um nível de abstração:** não mistura `total = a + b` com `db.query(...)`.
- **Poucos parâmetros:** muitos parâmetros sugerem agrupar em um objeto.
- **Sem efeito escondido:** se muda estado, o nome diz.
- **Retorno antecipado:** casos de erro saem cedo, e o caminho feliz fica sem aninhamento.

## Quando é ruim

- **Fragmentação excessiva:** dezenas de funções de 2 linhas obrigam a pular pelo arquivo para entender uma regra. Ousterhout (A Philosophy of Software Design) prefere módulos "profundos" (interface simples, trabalho relevante por dentro) a classes e funções rasas.
- **Nome que repete o corpo:** `addOne(x)` não ganha nada sobre `x + 1`.
- **Quebra sem coesão:** extrair trechos que só fazem sentido juntos.
- **Divergência:** Ousterhout e Robert Martin (Clean Code) têm diferenças significativas sobre o tamanho dos métodos (web.stanford.edu/~ouster/cgi-bin/book.php). Use o teste do nome, não a contagem de linhas.

## Como começar

Antes:

```ts
async function createOrder(input: OrderInput) {
  // valida
  if (!input.items.length) throw new Error("Pedido vazio");
  // calcula
  let total = 0;
  for (const i of input.items) total += i.price * i.qty;
  // salva
  const order = await db.order.create({ data: { ...input, total } });
  return order;
}
```

Depois:

```ts
async function createOrder(input: OrderInput) {
  assertHasItems(input.items);
  const total = calculateTotal(input.items);
  return db.order.create({ data: { ...input, total } });
}

function assertHasItems(items: OrderItem[]) {
  if (!items.length) throw new Error("Pedido vazio");
}

function calculateTotal(items: OrderItem[]) {
  return items.reduce((sum, i) => sum + i.price * i.qty, 0);
}
```

Em Python e C# o movimento é o mesmo: extraia, nomeie, rode os testes.

## Combina com / alternativas

Combina com:
- [Nomes claros](01-nomes-claros.md): a função extraída precisa de um bom nome.
- [Refatoração segura](10-refatoracao-segura.md): extrair função é o passo mais seguro.
- [Testes](08-testes.md): função pequena é fácil de testar.

Alternativa: um bloco longo e linear, quando ler de cima para baixo é mais claro que pular. Raro, mas existe.

## Decisão rápida

- **Use se:** a função tem comentários separando etapas, vários níveis de aninhamento ou o nome precisa de "e".
- **Evite se:** a quebra só cria funções de uma linha, ou espalha uma lógica que só faz sentido junta.
