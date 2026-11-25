# Tratamento de erros

> Falhe cedo, com mensagem útil, e trate o erro só onde dá para fazer algo a respeito.

| | |
|---|---|
| **Referência** | OWASP Cheat Sheet "Error Handling"; documentação de exceções do .NET (Microsoft Learn); PEP 20 e a seção de exceções do tutorial Python; MDN, `Error` e `cause` |
| **Categoria** | Robustez |
| **Tipo** | Prática de escrita de código |
| **Vale para** | Qualquer linguagem; exceções em TypeScript, Python e C#, valores de retorno em Go e Rust |
| **Verificado em** | 2026-11-24 |

## O que é

É decidir, para cada falha possível, quem descobre, quem trata e o que o usuário ou o log vê. Há dois tipos de erro: o esperado (senha errada, item fora de estoque) e o inesperado (bug, rede caiu).

Erro esperado vira resposta clara. Erro inesperado sobe até um ponto central, que registra e responde de forma segura. Um `catch` que engole o erro e segue esconde o bug.

## Por que usar

- **Bug aparece:** erro engolido vira dado errado vários passos depois.
- **Diagnóstico rápido:** mensagem com contexto poupa horas.
- **Experiência:** o usuário vê o que fazer, não um stack trace.
- **Segurança:** o OWASP Cheat Sheet "Error Handling" mostra que erro exibido ao usuário pode revelar a pilha tecnológica; devolva resposta genérica e registre o detalhe no servidor.

## Quando usar

- Toda chamada que pode falhar: rede, banco, arquivo, parsing.
- Ao escrever `catch`, `try/except` ou `try/catch`.
- Ao definir o que a API devolve em caso de erro.
- Ao revisar código com `catch {}` vazio.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| API / backend | ✅ Ótimo | Resposta genérica ao usuário e detalhe no log do servidor (OWASP, Cheat Sheet "Error Handling") |
| Código de alto desempenho | 🟡 Serve | Se o custo da exceção pesa, o .NET oferece formas sem exceção, como `TryParse` (Best practices for exceptions, Microsoft Learn) |

## Quando é bom

- **Falha cedo:** valide na entrada e lance o erro logo, não depois de três passos.
- **Mensagem com contexto:** "Pedido 123 não encontrado", não "erro".
- **Preserve a causa:** em JavaScript use `new Error("msg", { cause: err })`; em Python `raise X from err`; em C# passe a `innerException`.
- **Ponto central:** um tratador no topo (middleware, boundary) loga e responde.
- **Tipos de erro:** classes de erro de domínio deixam `catch` específico.

## Quando é ruim

- **Engolir erro:** `catch (e) {}` esconde bugs.
- **Captura ampla:** `except Exception` ou `catch (Exception)` onde só um erro era esperado.
- **Erro para controle de fluxo:** usar exceção para o que é caso normal.
- **Log e relança em toda camada:** o mesmo erro vira cinco linhas de log. Registre uma vez, no ponto central.
- **Exagero:** `try/catch` em volta de cada linha deixa o código ilegível. Trate onde há o que fazer.
- **Divergência:** exceções contra resultado (`Result`, retorno de erro) divide comunidades. Go e Rust usam valores (`error`, `Result`); TypeScript, Python e C# usam exceções. Siga a convenção da linguagem e do time.

## Como começar

Antes:

```ts
async function getUser(id: string) {
  try {
    const res = await fetch(`/api/users/${id}`);
    return await res.json();
  } catch (e) {
    console.log(e);
  }
}
```

Depois:

```ts
async function getUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) {
    throw new Error(`Falha ao buscar o usuário ${id} (HTTP ${res.status})`);
  }
  return res.json();
}
```

Quem chama decide o que fazer; um tratador central (middleware do framework) loga. Note que `fetch` não lança erro em respostas 4xx/5xx, por isso o `res.ok`.

## Combina com / alternativas

Combina com:
- [Tipos e validação na borda](06-tipos-e-validacao-na-borda.md): entrada inválida falha cedo.
- [Testes](08-testes.md): teste também o caminho de erro.
- [Nomes claros](01-nomes-claros.md): erros com nome de domínio.

Alternativas: padrão `Result`/`Either` (bibliotecas como neverthrow em TypeScript; última versão 8.2.0, de fev/2025, conferida no GitHub em 2026-11-24) quando o time prefere erro como valor.

## Decisão rápida

- **Use se:** o código fala com algo que pode falhar (quase sempre).
- **Evite se:** o `try/catch` só silencia, ou se repete em toda camada sem decidir nada.
