# Modularização e limites entre módulos

> Agrupe o que muda junto, separe o que muda por motivos diferentes e deixe as dependências apontarem para um lado só.

| | |
|---|---|
| **Referência** | A Philosophy of Software Design (Ousterhout: módulos profundos); "The Clean Architecture" (R. Martin, blog.cleancoder.com, 2012: regra da dependência) |
| **Categoria** | Estrutura do código |
| **Tipo** | Princípio de design |
| **Vale para** | Qualquer linguagem; em TypeScript use `export` com intenção, em C# `internal`, em Python `_prefixo` e `__all__` |
| **Verificado em** | 2026-11-24 |

## O que é

Modularizar é dividir o sistema em partes (módulos) com responsabilidade clara, uma interface pequena e detalhes escondidos. Dois conceitos guiam:

- **Alta coesão:** o que está dentro do módulo pertence ao mesmo assunto.
- **Baixo acoplamento:** um módulo sabe pouco sobre os outros e só usa o que eles expõem de propósito.

A regra prática: dependências em uma direção só. Regra de negócio não importa tela nem banco; o contrário sim. Onde ficam as pastas e como nomear os módulos é assunto da skill **architecture**. Aqui o foco é o código: o que exportar, quem pode importar quem.

## Por que usar

- **Mudança local:** alterar um módulo não quebra dez outros.
- **Entendimento por partes:** o júnior lê um módulo sem carregar o sistema inteiro.
- **Testes isolados:** dá para trocar o banco por um falso (R. Martin, "The Clean Architecture", blog.cleancoder.com, 2012).

## Quando usar

- Um arquivo importa de tudo e tudo importa dele.
- Mudar uma regra exige editar vários arquivos em lugares distantes.
- Há importação circular (A importa B, B importa A).
- O arquivo passou de algumas centenas de linhas e mistura assuntos.
- Você quer testar uma regra sem subir banco ou rede.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Sistema com regra de negócio rica | ✅ Ótimo | Regra de negócio isolada do banco, que pode ser trocado por um falso (R. Martin, "The Clean Architecture", blog.cleancoder.com, 2012) |

## Quando é bom

- **Interface pequena:** o módulo expõe poucas funções e esconde o resto.
- **Dependência numa direção:** dá para desenhar o grafo sem setas voltando.
- **Nomes por assunto:** `billing`, `orders`, não `utils` e `helpers`.
- **Dependência injetada:** o módulo recebe o que precisa (banco, relógio, cliente HTTP) em vez de criar.
- **Regra checada por ferramenta:** lint de importação ou ferramentas como dependency-cruiser e madge em TypeScript acusam violações. Confira a configuração na documentação de cada uma.

## Quando é ruim

- **Camada por reflexo:** controller, service, repository, DTO e mapper para um CRUD de duas tabelas. Mais arquivos, mesma lógica.
- **Módulos rasos:** muita interface para pouco trabalho. Ousterhout os contrasta com módulos profundos.
- **Interface por tudo:** criar interface para classe que só tem uma implementação, "para o futuro".
- **Pasta `utils`:** vira depósito sem dono e acopla o sistema todo.
- **Divergência:** "The Clean Architecture" (R. Martin, 2012) organiza em camadas concêntricas; "vertical slices" organizam por funcionalidade. Escolha pelo tamanho do problema.

## Como começar

Antes (regra presa ao banco):

```ts
import { db } from "../infra/db";

export async function applyDiscount(orderId: string) {
  const order = await db.order.findUnique({ where: { id: orderId } });
  return order.total > 100 ? order.total * 0.9 : order.total;
}
```

Depois (regra pura, banco na borda):

```ts
// orders/discount.ts — sem import de infraestrutura
export function applyDiscount(total: number) {
  return total > 100 ? total * 0.9 : total;
}

// orders/service.ts — junta as partes
export async function priceOrder(orderId: string, repo: OrderRepo) {
  const order = await repo.find(orderId);
  return applyDiscount(order.total);
}
```

Regra para exportar: se ninguém fora do módulo precisa, não exporte.

## Combina com / alternativas

Combina com:
- [Funções pequenas](02-funcoes-pequenas.md): o módulo é feito delas.
- [Simplicidade](04-simplicidade.md): freia o excesso de camadas.
- [Tipos e validação na borda](06-tipos-e-validacao-na-borda.md): a borda é o limite do módulo.

Alternativas: arquitetura em camadas, hexagonal, vertical slices e monólito modular. A escolha e a estrutura de pastas ficam na skill **architecture**.

## Decisão rápida

- **Use se:** o sistema cresce, tem regra de negócio de verdade ou mais de uma pessoa mexe nele.
- **Evite se:** é um script, um protótipo ou um CRUD mínimo, onde a separação só adiciona arquivos.
