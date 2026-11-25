# Testes de unidade para regra de negócio

> Teste a regra pura, sem banco e sem rede, com data injetada e uma tabela de casos.

| | |
|---|---|
| **Referência** | Vitest (vitest.dev/api/vi, vi.useFakeTimers e vi.setSystemTime); pytest (docs.pytest.org, parametrize); xUnit (xunit.net, Theory e InlineData); Martin Fowler, "TestCoverage" (2012) e "UnitTest" (2014); Bill Wake, padrão Arrange-Act-Assert (2001) |
| **Categoria** | Qualidade |
| **Tipo** | Prática de teste automatizado |
| **Vale para** | Qualquer linguagem; exemplos em TypeScript com Vitest |
| **Verificado em** | 2026-11-24 |

## O que é

Teste de unidade verifica uma regra de negócio em isolamento: uma função que recebe dados e devolve um resultado. Sem banco, sem rede, sem arquivo.

Regra pura é a que depende só do que entra: cálculo de preço, política de cancelamento, transição de estado de um agendamento (agendado, confirmado, cancelado).

Estrutura **Arrange-Act-Assert** (arrumar, agir, verificar): prepare os dados, chame a regra, compare o resultado. Como escrever o teste legível está em [Testes](../../coding/docs/08-testes.md). Onde ele entra na estratégia: [Pirâmide de testes](01-piramide-de-testes.md).

## Por que usar

- **Rápido:** milhares de casos em poucos segundos.
- **Falha aponta a causa:** o erro está na regra, não no banco nem na rede.
- **Cobre os cantos:** exatamente 24 h, 23 h 59 min, consulta no passado.

## Quando usar

- Cálculo (preço, taxa, desconto, imposto).
- Regra com condição e data (cancelamento, vencimento, prazo).
- Máquina de estados (quais transições são permitidas).
- Validação com regra própria.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas regras; teste só o que calcula algo |
| MVP de SaaS | ✅ Ótimo | Preço, plano e cancelamento são regras que não podem errar |
| SaaS em crescimento | ✅ Ótimo | A tabela de casos protege regras que crescem |
| Sistema interno/corporativo | ✅ Ótimo | Regras de negócio densas, a parte que mais muda |
| API/integração | ✅ Ótimo | Regras de mapeamento e validação isoladas da rota |
| App mobile | ✅ Ótimo | Lógica fora da tela roda sem aparelho |
| CRUD sem regra | ❌ Evite | O teste só repetiria o código; use integração |

## Quando é bom

- **Regra separada da infraestrutura:** a função recebe a data e o valor, não busca no banco.
- **Um caso por linha:** a tabela mostra a regra inteira de relance.
- **Sem sleep e sem relógio real:** o teste dá o mesmo resultado em qualquer dia.

## Quando é ruim

- **Mock do que você controla:** mockar sua própria classe de regra faz o teste provar o mock.
- **Cobertura como meta:** para Fowler, cobertura serve para achar código sem teste, não para dizer que os testes são bons. Use como sinal.
- **Teste que espelha o código:** repete a fórmula da implementação e nunca falha.
- **Regra misturada com banco:** se a função precisa de banco para rodar, extraia a regra.

## Como começar

Critério de aceite da funcionalidade "Cancelar agendamento":

- Dado um agendamento em 30 h, quando o paciente cancela, então não há taxa.
- Dado um agendamento em 2 h, quando o paciente cancela, então a taxa é 50% do valor.
- Dado um agendamento em exatamente 24 h, quando cancela, então não há taxa.

A regra recebe o relógio por parâmetro, em vez de chamar `Date.now()` dentro dela:

```ts
export function taxaDeCancelamento(
  consultaEm: Date,
  agora: Date,
  valor: number,
): number {
  const horasAntes = (consultaEm.getTime() - agora.getTime()) / 3_600_000;
  return horasAntes >= 24 ? 0 : valor * 0.5;
}
```

Teste com tabela de casos (`it.each` no Vitest):

```ts
import { describe, expect, it } from "vitest";
import { taxaDeCancelamento } from "./taxa-de-cancelamento";

const consulta = new Date("2026-12-10T15:00:00Z");

describe("taxaDeCancelamento", () => {
  it.each([
    { horasAntes: 30, taxa: 0 },
    { horasAntes: 24, taxa: 0 },
    { horasAntes: 23.9, taxa: 50 },
    { horasAntes: 2, taxa: 50 },
  ])("com $horasAntes h de antecedência cobra $taxa", ({ horasAntes, taxa }) => {
    const agora = new Date(consulta.getTime() - horasAntes * 3_600_000);

    expect(taxaDeCancelamento(consulta, agora, 100)).toBe(taxa);
  });
});
```

Quando o relógio é lido dentro do código que você não quer mudar, congele a hora. No Vitest, `vi.useFakeTimers()` já troca o `Date` (junto com `setTimeout` e `setInterval`), e `vi.setSystemTime()` define a hora; `vi.useRealTimers()` desfaz:

```ts
import { afterEach, beforeEach, expect, it, vi } from "vitest";

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date("2026-12-09T09:00:00Z"));
});

afterEach(() => {
  vi.useRealTimers();
});

it("lê a hora congelada", () => {
  expect(new Date().toISOString()).toBe("2026-12-09T09:00:00.000Z");
});
```

Prefira passar a data por parâmetro; use o relógio falso só quando não der. Chame `vi.useRealTimers()` no `afterEach` para não vazar a hora para outros testes.

Máquina de estados: uma tabela de transições permitidas e proibidas, cada linha um teste.

### Em cada stack

| Stack | Tabela de casos | Comando para rodar |
|---|---|---|
| TypeScript (Vitest) | `it.each` / `test.each` | `npx vitest run` |
| TypeScript (Jest) | `it.each` / `test.each` | `npx jest` |
| .NET (xUnit) | `[Theory]` + `[InlineData]` | `dotnet test` |
| Python (pytest) | `@pytest.mark.parametrize` | `pytest` |
| PHP (Pest) | `->with([...])` (dataset) | `./vendor/bin/pest` |
| PHP (PHPUnit) | `#[DataProvider]` | `./vendor/bin/phpunit` |
| Go | tabela de structs + `t.Run` | `go test ./...` |
| Java (JUnit 5) | `@ParameterizedTest` | `mvn test` ou `./gradlew test` |
| Flutter | `for` sobre lista de casos | `flutter test` |

Mocks só na **fronteira**: serviço de e-mail, gateway de pagamento, API de terceiros. Regra, entidade e função sua rodam de verdade.

## Combina com / alternativas

Combina com:
- [Pirâmide de testes](01-piramide-de-testes.md): a base da estratégia.
- [Testes de integração com banco](03-testes-de-integracao-com-banco.md): prova a rota que chama a regra.
- [Testes](../../coding/docs/08-testes.md): como escrever o teste legível.
- [Funções pequenas](../../coding/docs/02-funcoes-pequenas.md): regra pequena é fácil de testar.

Alternativas: property-based testing (gera casos aleatórios), testes de mutação para medir a força dos testes.

## Decisão rápida

- **Use se:** a regra decide algo (valor, prazo, estado) e pode ser chamada sem banco.
- **Evite se:** o código só repassa dados ao banco; use teste de integração.
