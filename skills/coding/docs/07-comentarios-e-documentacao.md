# Sem comentários no código

> O código não leva comentário. Se uma linha precisa de explicação, o nome está errado ou a função faz coisa demais: conserte o código. O porquê vai para o commit, o PR, o teste ou o documento de decisão.

| | |
|---|---|
| **Referência** | Clean Code, cap. 4 "Comments" (Robert C. Martin); A Philosophy of Software Design (web.stanford.edu/~ouster/cgi-bin/book.php), para a visão contrária; Conventional Commits (conventionalcommits.org) |
| **Categoria** | Legibilidade |
| **Tipo** | Prática de escrita de código |
| **Vale para** | Qualquer linguagem |
| **Verificado em** | 2026-11-24 |

## O que é

A regra é não escrever comentário em código de produção nem de teste: nem explicando a linha, nem descrevendo a função, nem código comentado. A intenção aparece no próprio código, por nome de variável, de função e de teste. O contexto que o código não consegue carregar (motivo histórico, ticket, decisão) fica fora do arquivo, onde não polui a leitura e não desatualiza escondido.

## Por que

- **Comentário desatualiza.** O código muda, o texto fica e passa a mentir. Ninguém testa comentário.
- **Comentário esconde nome ruim.** Quem comenta deixa de renomear.
- **Ruído visual.** O leitor lê duas vezes a mesma coisa, uma em português e outra em código.
- **O porquê tem lugar melhor.** O `git blame` leva ao commit e ao PR, que têm o contexto completo e a data.

## Onde fica cada coisa

| Você queria comentar… | Faça isto |
|---|---|
| O que a linha faz | Extraia uma variável ou função com nome que diga isso |
| O que a função faz | Renomeie a função; se não cabe num nome, ela faz coisa demais: divida |
| Por que foi feito assim (regra de negócio, exigência fiscal, limite de API) | Nome que carregue a regra (`roundUpForNfe`), teste com nome que conte o caso, e o motivo na mensagem do commit ou no PR |
| Armadilha que alguém pode "consertar" errado | Um teste que quebra se alguém desfizer, com nome explicando o motivo |
| Decisão de arquitetura | Documento de decisão (ADR) ou `ARCHITECTURE.md` |
| Pendência (`TODO`) | Issue no rastreador, não no código |
| Código antigo "por garantia" | Apague; o git guarda |
| Contrato de uma API pública | Tipos fortes, nomes de parâmetro claros e a documentação no README ou na página de referência da API |

## Exceções

Só o que uma ferramenta exige para funcionar, sempre na forma mais curta:

- diretivas de compilador, lint ou typecheck (`// @ts-expect-error`, `// biome-ignore lint/...: motivo`, `# type: ignore[...]`, `#pragma`), quando a ferramenta pede o motivo na própria diretiva;
- cabeçalho de licença quando a licença do projeto obriga;
- arquivos gerados por ferramenta (migrations, código gerado), que não se editam à mão.

Se o repositório já tem regra própria de comentários (por exemplo, documentação XML obrigatória em métodos públicos no C#), a regra do repositório vale.

## Como fazer

Antes:

```ts
const trimmedName = name.trim();
if (!trimmedName) return;
// Limpa o campo na hora para a pessoa já digitar o próximo item.
setName("");
void onAdd(trimmedName);
```

Depois:

```ts
const trimmedName = name.trim();
if (!trimmedName) return;
clearFieldForNextItem();
void onAdd(trimmedName);
```

Antes:

```ts
// A API de pagamentos devolve 202 mesmo quando a cobrança falha;
// o resultado real só chega pelo webhook. Ver ticket PAY-482.
if (res.status === 202) return { status: "pending" };
```

Depois:

```ts
const paymentAwaitsWebhook = res.status === 202;
if (paymentAwaitsWebhook) return { status: "pending" };
```

```ts
it("trata 202 como pendente porque a API só confirma a cobrança pelo webhook", () => { /* ... */ });
```

E o commit: `fix(pagamentos): tratar 202 como pendente até o webhook (PAY-482)`.

## Na revisão

Comentário em diff é apontamento de revisão: peça para trocar por nome, função ou teste, ou mover o motivo para o commit ou o PR. O agente de IA segue a mesma regra e não deixa comentário explicando o que acabou de escrever.

## Combina com

- [Nomes claros](01-nomes-claros.md): é o substituto direto do comentário.
- [Funções pequenas](02-funcoes-pequenas.md): função com um só propósito cabe num nome.
- [Testes](08-testes.md): o nome do teste documenta o comportamento e quebra quando ele muda.
- [Commits e PRs pequenos](11-commits-e-prs-pequenos.md): a mensagem guarda o porquê.
- [Revisão de código](12-revisao-de-codigo.md): comentário no diff é apontamento.

## Decisão rápida

- **Nunca:** comentário explicando linha, função, regra ou pendência; código comentado.
- **Só se a ferramenta exigir:** diretiva de lint, compilador ou typecheck, cabeçalho de licença.
