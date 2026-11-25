# Simplicidade: KISS, YAGNI e regra de três

> Escreva o código mais simples que resolve o problema de hoje e só abstraia quando a repetição provar que vale.

| | |
|---|---|
| **Referência** | Fowler, "Yagni" (martinfowler.com/bliki/Yagni.html); Sandi Metz, "The Wrong Abstraction" (sandimetz.com, 2016) |
| **Categoria** | Princípio de design |
| **Tipo** | Princípio de decisão |
| **Vale para** | Qualquer linguagem e tamanho de projeto |
| **Verificado em** | 2026-11-24 |

## O que é

Três ideias que andam juntas:

- **KISS:** prefira a solução mais simples que funciona.
- **YAGNI** ("você não vai precisar disso"): não construa o que ninguém pediu ainda.
- **Regra de três:** copie na primeira e na segunda vez; na terceira, extraia a abstração.

Isso corrige um uso cego do DRY. Duas funções iguais por acaso, que mudam por motivos diferentes, não são duplicação de verdade.

## Por que usar

- **Mudança barata:** é mais fácil juntar código duplicado do que desfazer uma abstração errada (Sandi Metz, "The Wrong Abstraction", 2016: "duplication is far cheaper than the wrong abstraction").

## Quando usar

- Você pensa "e se um dia precisarmos de...".
- Vai criar parâmetro, flag ou interface para um único uso.
- Dois trechos parecem iguais, mas pertencem a assuntos diferentes.
- Revisando um PR com configuração, plugin ou camada que ninguém pediu.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Produto em evolução | ✅ Ótimo | Duplicação é bem mais barata que a abstração errada (Metz, "The Wrong Abstraction", 2016) |

## Quando é bom

- **Código óbvio:** um `if` claro vence uma estratégia com fábrica.
- **Duplicação tolerada:** duas cópias pequenas e isoladas custam menos que um helper com cinco flags.
- **Extração com evidência:** três usos reais mostram o formato certo.
- **Remoção:** código morto sai, o histórico do git guarda.

## Quando é ruim

- **Simplicidade como desculpa:** copiar 200 linhas dez vezes não é KISS. A regra de três manda extrair na terceira.
- **YAGNI cego:** ignorar o que é caro de mudar depois (modelo de dados, contrato de API, segurança).
- **Abstração errada:** helper com `if (modo === "a")` e `if (modo === "b")` espalhados, cada chamada com sua flag. Metz recomenda reinlinar o código e recomeçar.
- **Complexidade escondida:** "simples" para quem escreveu, truque para quem lê. Simples é o que o júnior entende.
- **Divergência:** Sandi Metz ("The Wrong Abstraction", sandimetz.com, 2016) defende tolerar a duplicação até a abstração certa aparecer: "duplication is far cheaper than the wrong abstraction".

## Como começar

Antes (generalidade que ninguém pediu):

```ts
function formatValue(v: unknown, opts: { type?: "money" | "date"; locale?: string; fallback?: string } = {}) {
  /* 40 linhas para três tipos que o sistema nunca usa */
}
```

Depois (o que existe hoje):

```ts
const formatMoney = (cents: number) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(cents / 100);
```

Pergunta antes de abstrair: "tenho três usos reais, que mudam pelo mesmo motivo?". Se não, deixe duplicado. Em C#, resista a criar `IFooService` com uma implementação só; em Python, a uma classe quando uma função resolve.

## Combina com / alternativas

Combina com:
- [Modularização e limites](03-modularizacao-e-limites.md): evita camadas sem uso.
- [Refatoração segura](10-refatoracao-segura.md): extrai a abstração quando ela se prova.
- [Revisão de código](12-revisao-de-codigo.md): é onde o excesso é pego.

Alternativa: DRY estrito, aceitável em código que sempre muda junto (por exemplo, constantes e regras fiscais compartilhadas).

## Decisão rápida

- **Use se:** o requisito ainda muda, o time é pequeno ou o júnior precisa ler o código.
- **Evite se:** o ponto é caro de mudar (contrato público, esquema de banco, segurança) ou a repetição já passou de três e muda junto.
