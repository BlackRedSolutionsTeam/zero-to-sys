# Nomes claros

> O nome certo dispensa comentário: quem lê entende o que a coisa é ou faz sem abrir o corpo da função.

| | |
|---|---|
| **Referência** | guias oficiais de estilo de cada linguagem; diretrizes de nomes do .NET (Microsoft Learn) |
| **Categoria** | Legibilidade |
| **Tipo** | Prática de escrita de código |
| **Vale para** | Qualquer linguagem; convenção de caixa muda (camelCase em TypeScript, snake_case em Python, PascalCase em C#) |
| **Verificado em** | 2026-11-24 |

## O que é

É escolher nomes de variáveis, funções, classes, arquivos e parâmetros que revelam a intenção. O nome responde "o que é isso?" ou "o que isso faz?" sem exigir contexto.

A convenção de caixa vem do guia da linguagem: PEP 8 em Python, as convenções da Microsoft em C#, e o que o time adotar em TypeScript (o lint força). O que esta prática cobre é o sentido do nome, não a caixa.

## Por que usar

- **Leitura rápida:** o código vira quase uma frase em português ou inglês.
- **Menos comentário:** o que o nome já diz não precisa ser repetido.
- **Onboarding:** o júnior entende o fluxo sem perguntar.
- **Busca:** nome específico se acha com Ctrl+F; `item` não.

## Quando usar

- Sempre, em todo código novo.
- Ao tocar em código antigo com nome ruim (renomear é a refatoração mais barata).
- Em revisão de PR, quando você precisa de um comentário para entender uma variável.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| API pública / biblioteca | ✅ Ótimo | As diretrizes de nomes do .NET (Microsoft Learn) fixam o nome até no `I` da interface em C# |

## Quando é bom

- **Nome revela intenção:** `remainingAttempts` em vez de `n`.
- **Mesmo conceito, mesmo nome:** não alternar `user`, `customer` e `client` para a mesma coisa.
- **Booleano como pergunta:** `isActive`, `hasPermission`, `canEdit`.
- **Função com verbo, tipo com substantivo:** `calculateTotal()`, `Invoice`.
- **Vocabulário do domínio:** o time de negócio reconhece os termos.

## Quando é ruim

- **Nome comprido demais:** `getUserListFilteredByActiveStatusAndRole` indica função que faz coisa demais. O nome longo é sintoma.
- **Prefixos de tipo:** `strName`, `UserClass` (notação húngara). O compilador e o editor já mostram o tipo. A exceção é o `I` de interface, que as diretrizes de nomes do .NET (Microsoft Learn) pedem em C#.
- **Abreviação própria:** `usrMgr`, `cfgSvc`. Quem chegou agora não decifra.
- **Exagero:** renomear tudo a cada PR gera ruído no diff e conflito de merge. Renomeie o que atrapalha, em PR separado.
- **Divergência:** nome longo e descritivo contra nome curto. O que pesa é o nome não ser vago; use o teste de leitura em voz alta, abaixo.

## Como começar

Antes:

```ts
function calc(d: number[], f: boolean) {
  let t = 0;
  for (const x of d) t += f ? x * 0.9 : x;
  return t;
}
```

Depois:

```ts
function calculateOrderTotal(itemPrices: number[], hasDiscount: boolean) {
  const DISCOUNT_FACTOR = 0.9;
  let total = 0;
  for (const price of itemPrices) {
    total += hasDiscount ? price * DISCOUNT_FACTOR : price;
  }
  return total;
}
```

Teste prático: leia o código em voz alta para alguém que não o conhece. Onde você precisar explicar, falta um nome. Em Python use `snake_case` (`calculate_order_total`); em C#, `PascalCase` para métodos (`CalculateOrderTotal`).

## Combina com / alternativas

Combina com:
- [Funções pequenas](02-funcoes-pequenas.md): função curta é fácil de nomear.
- [Sem comentários no código](07-comentarios-e-documentacao.md): o nome substitui o comentário.
- [Formatação e lint automáticos](09-formatacao-e-lint-automaticos.md): o lint força a convenção de caixa.

Alternativas: não há. Nomes ruins com comentário em cima é pior que nome bom sem comentário.

## Decisão rápida

- **Use se:** o código será lido por outra pessoa, ou por você daqui a seis meses (sempre).
- **Evite se:** nunca evite. Só relaxe em notação matemática consagrada e laços minúsculos.
