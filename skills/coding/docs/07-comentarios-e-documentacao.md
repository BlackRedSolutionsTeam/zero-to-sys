# Comentários e documentação

> Comente o porquê, não o quê: o código já diz o que faz; só você sabe por que fez assim.

| | |
|---|---|
| **Referência** | página do livro A Philosophy of Software Design (web.stanford.edu/~ouster/cgi-bin/book.php); TSDoc (tsdoc.org); PEP 257 (docstrings); documentação XML do C# (Microsoft Learn) |
| **Categoria** | Legibilidade |
| **Tipo** | Prática de escrita de código |
| **Vale para** | Qualquer linguagem; o formato do comentário de documentação muda (TSDoc, docstring, XML doc) |
| **Verificado em** | 2026-11-24 |

## O que é

Comentário é texto que o compilador ignora e que explica o que o código sozinho não mostra: a razão de uma decisão, uma restrição, uma armadilha. Documentação é o texto sobre o contrato público: o que a função recebe, devolve e quando falha.

Comentário que repete o código vira mentira quando o código muda. Comentário que explica o motivo continua válido.

## Por que usar

- **Guarda o contexto:** por que escolhemos isto, o que já foi tentado.
- **Evita "conserto" errado:** um aviso sobre um truque impede que alguém o desfaça.
- **API compreensível:** o editor mostra a documentação ao passar o mouse.
- **Onboarding:** README e documentação de decisão encurtam a entrada de gente nova.

## Quando usar

- Existe uma regra de negócio não óbvia ou uma exceção histórica.
- O código parece estranho de propósito (workaround de bug de terceiros, otimização).
- A função é pública e usada por outros módulos ou pessoas.
- Há uma decisão de arquitetura que vai ser questionada (registre em um documento de decisão).

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Biblioteca / API pública | ✅ Ótimo | Formatos TSDoc, PEP 257 e XML doc |
| Código interno simples | 🟡 Serve | Ousterhout e Martin divergem sobre o papel dos comentários (web.stanford.edu/~ouster/cgi-bin/book.php) |

## Quando é bom

- **Explica o porquê:** "Arredondamos para cima por exigência fiscal (NF-e)".
- **Aponta fonte:** link para issue, RFC ou página de documentação.
- **Marca pendência com dono:** `TODO(ticket-123): remover após migração`.
- **Documenta o contrato:** parâmetros, retorno, erros possíveis e exemplo, na função pública.
- **Fica perto do código:** comentário na linha que explica, não num arquivo distante.

## Quando é ruim

- **Comentário que repete:** `// busca o usuário` sobre `getUser()`.
- **Comentário que mente:** o código mudou e o texto ficou.
- **Código comentado:** o git guarda o histórico; apague.
- **Comentário para desculpar nome ruim:** renomeie em vez de comentar.
- **Documentação em excesso:** docblock em toda função privada gera ruído e desatualiza.
- **Divergência:** Ousterhout e Martin (Clean Code) têm diferenças significativas sobre o papel dos comentários (web.stanford.edu/~ouster/cgi-bin/book.php). O meio-termo: pouco comentário de implementação, bom comentário de contrato e de motivo.

## Como começar

Antes:

```ts
// incrementa o contador
count++;

// verifica se o usuário é maior de idade
if (u.a >= 18) { /* ... */ }
```

Depois:

```ts
count++;

const isAdult = user.age >= 18;
if (isAdult) { /* ... */ }

// A API de pagamentos devolve 202 mesmo quando a cobrança falha;
// o resultado real só chega pelo webhook. Ver ticket PAY-482.
if (res.status === 202) return { status: "pending" };
```

Documentação de função pública em TypeScript (TSDoc):

```ts
/** Calcula o frete. Lança `InvalidZipError` se o CEP não existir. */
export function calculateShipping(zip: string, weightKg: number): number { /* ... */ }
```

Em Python, use docstring (PEP 257); em C#, comentário XML `/// <summary>`. Se o time ou o repositório tiver regra própria (alguns só aceitam comentário em tipos e métodos públicos), a regra do time vale.

## Combina com / alternativas

Combina com:
- [Nomes claros](01-nomes-claros.md): nome bom reduz a necessidade de comentário.
- [Commits e PRs pequenos](11-commits-e-prs-pequenos.md): a mensagem do commit guarda o porquê da mudança.
- [Revisão de código](12-revisao-de-codigo.md): pergunta de revisor vira comentário ou nome melhor.

Alternativas: registro de decisões de arquitetura (ADR) para decisões grandes, README por módulo para visão geral.

## Decisão rápida

- **Use se:** o motivo não está claro no código, ou a função é pública e usada por terceiros.
- **Evite se:** o comentário só diz o que a linha já diz, ou se o nome melhor resolveria.
