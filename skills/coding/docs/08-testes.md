# Testes

> Teste o comportamento que importa, perto de como o código é usado, sem amarrar o teste à implementação.

| | |
|---|---|
| **Referência** | Test Pyramid (M. Fowler, "TestPyramid", 2012); Testing Trophy (Kent C. Dodds, "Static vs Unit vs Integration vs E2E Testing"); Testing Library, princípios; Vitest (vitest.dev), pytest (docs.pytest.org), xUnit (xunit.net) |
| **Categoria** | Qualidade |
| **Tipo** | Prática de verificação |
| **Vale para** | Qualquer linguagem; ferramentas comuns: Vitest ou Jest (TypeScript), pytest (Python), xUnit (C#) |
| **Verificado em** | 2026-11-24 |

## O que é

Teste automatizado é código que verifica se outro código se comporta como esperado. Dá segurança para mudar sem medo.

Dois modelos populares de distribuição:

- **Pirâmide** (Fowler): muitos testes unitários, alguns de integração, poucos de ponta a ponta.
- **Troféu** (Dodds): poucos unitários, ênfase em integração, base de análise estática (tipos e lint).

Os dois modelos divergem na proporção. O Testing Library (guiding principles) diz que quanto mais os testes se parecem com o uso do software, mais confiança dão.

## Por que usar

- **Refatorar sem medo:** o teste avisa se algo quebrou.
- **Bug não volta:** todo bug corrigido ganha um teste.

## Quando usar

- Regra de negócio, cálculo, validação.
- Antes de refatorar código legado sem testes.
- Todo bug corrigido (escreva o teste que falha, depois conserte).
- Fluxos críticos: login, pagamento, cadastro.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Regra de negócio / funções puras | ✅ Ótimo | Base da pirâmide: muitos testes unitários (Fowler, "TestPyramid", 2012) |
| API / backend | ✅ Ótimo | O troféu dá ênfase à integração (Dodds, "Static vs Unit vs Integration vs E2E Testing") |
| UI | 🟡 Serve | Quanto mais o teste se parece com o uso, mais confiança dá (Testing Library, guiding principles) |

## Quando é bom

- **Nome descreve comportamento:** `rejeita pedido sem itens`.
- **Estrutura arrumar, agir, verificar:** três blocos claros em cada teste.
- **Independente e rápido:** um teste não depende de outro; teste lento é rodado menos.
- **Roda na integração contínua:** o PR só passa se os testes passarem.

## Quando é ruim

- **Meta de cobertura como fim:** 100% de linhas com testes que não verificam nada. Para Fowler ("TestCoverage", 2012), cobertura serve para achar código não testado, e é pouco útil como número que diz se os testes são bons.
- **Testar a implementação:** o teste quebra a cada refatoração, mesmo com o comportamento igual.
- **Mock em excesso:** o teste só confirma o que os mocks foram programados para fazer.
- **Teste instável:** depende de horário, ordem ou rede; ninguém mais confia no resultado.
- **Ponta a ponta demais:** lento, frágil e difícil de depurar. Deixe para os fluxos críticos.
- **Divergência:** pirâmide contra troféu, e TDD estrito contra teste depois.

## Como começar

Antes (só uma chamada, sem verificar nada útil):

```ts
test("calculateTotal", () => {
  expect(calculateTotal([])).toBeDefined();
});
```

Depois (Vitest ou Jest, mesma sintaxe):

```ts
describe("calculateTotal", () => {
  it("soma preço vezes quantidade dos itens", () => {
    const items = [{ price: 10, qty: 2 }, { price: 5, qty: 1 }];
    expect(calculateTotal(items)).toBe(25);
  });

  it("devolve zero para lista vazia", () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

Em Python com pytest: `def test_soma_itens(): assert calculate_total(...) == 25`. Em C# com xUnit: método com `[Fact]` e `Assert.Equal(25, ...)`. Comece pelo teste de um bug real.

## Combina com / alternativas

Combina com:
- [Funções pequenas](02-funcoes-pequenas.md): fácil de testar.
- [Refatoração segura](10-refatoracao-segura.md): o teste é a rede de segurança.
- [Formatação e lint automáticos](09-formatacao-e-lint-automaticos.md): a base da pirâmide ou do troféu.

Alternativas e complementos: testes de contrato, property-based testing, testes de snapshot (a documentação do Jest manda tratar snapshots como código e revisá-los).

## Decisão rápida

- **Use se:** o código tem regra, será alterado ou é crítico.
- **Evite se:** o código é descartável ou trivial, ou se o teste só espelha a implementação.
