# Tipos e validação na borda

> Dado que vem de fora não é confiável até ser validado; depois de validado, o resto do código usa tipos e confia neles.

| | |
|---|---|
| **Referência** | "Parse, don't validate" (Alexis King, 2019); TypeScript Handbook; Zod (zod.dev); Pydantic (docs.pydantic.dev); .NET nullable reference types (Microsoft Learn) |
| **Categoria** | Robustez |
| **Tipo** | Prática de escrita de código |
| **Vale para** | TypeScript (Zod, Valibot), Python (Pydantic, type hints + mypy ou pyright), C# (nullable, records) |
| **Verificado em** | 2026-11-24 |

## O que é

Borda é onde dado entra no sistema: requisição HTTP, formulário, arquivo, variável de ambiente, resposta de API externa. Ali você valida e converte o dado cru em um tipo confiável. Dentro do sistema, as funções recebem esse tipo e não revalidam.

Tipos estáticos (TypeScript, type hints do Python, C#) pegam erros de uso na compilação. Mas o tipo some em tempo de execução: um `as User` sobre JSON não valida nada. Por isso os dois andam juntos: validação na borda mais tipos por dentro.

## Por que usar

- **Erros na porta:** a entrada ruim falha com mensagem clara, não três funções depois.
- **Menos `if` espalhado:** o código interno assume dado válido.
- **Editor ajuda:** autocomplete e erro na hora de digitar.
- **Contrato explícito:** o esquema documenta o formato esperado.

## Quando usar

- Todo endpoint, formulário, leitura de arquivo e variável de ambiente.
- Resposta de API de terceiros em que você não controla o formato.
- Ao ver `any`, `as` ou `# type: ignore` para "fazer passar".
- Ao ver o mesmo `if (!x) ...` repetido em várias funções.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| API / backend | ✅ Ótimo | Dado de fora vira tipo confiável na borda ("Parse, don't validate", A. King, 2019) |
| Integração com terceiros | ✅ Ótimo | Resposta de fora é validada na borda ("Parse, don't validate", A. King, 2019) |

## Quando é bom

- **Esquema como fonte única:** com Zod, o tipo vem do esquema (`z.infer`), sem escrever duas vezes.
- **Parse em vez de checar:** a função devolve um tipo mais estreito que o recebido.
- **Tipos que impedem estado inválido:** união de estados em vez de vários booleanos.
- **Strict ligado:** `"strict": true` no `tsconfig`, nullable em C#, mypy ou pyright em Python.

## Quando é ruim

- **Validar em toda função:** a mesma checagem em cada camada polui e diverge. Valide uma vez.
- **`any` e `as` como atalho:** apaga a proteção do compilador exatamente onde havia risco.
- **Tipos elaborados demais:** tipos condicionais e genéricos aninhados que o júnior não lê. Prefira tipos simples e nomeados.
- **Esquema duplicado:** manter tipo à mão e validador separados; eles saem de sincronia.
- **Divergência:** há quem prefira só tipos estáticos e confiança no contrato interno; outros validam também entre serviços. Na borda externa, todos concordam: valide.

## Como começar

Antes:

```ts
app.post("/users", (req, res) => {
  const user = req.body as { email: string; age: number };
  save(user); // e se vier age: "abc"?
});
```

Depois (TypeScript com Zod 4, onde `z.email()` é a forma atual; confira a sintaxe em zod.dev):

```ts
import { z } from "zod";

const UserInput = z.object({ email: z.email(), age: z.number().int().min(0) });
type UserInput = z.infer<typeof UserInput>;

app.post("/users", (req, res) => {
  const parsed = UserInput.safeParse(req.body);
  if (!parsed.success) return res.status(400).json(parsed.error.flatten());
  save(parsed.data); // tipado e válido
});
```

Em Python, uma classe `BaseModel` do Pydantic faz o mesmo papel; em C#, `record` com validação no construtor ou FluentValidation (versão mais recente 12.2.0 em 2026-11-24, conferida no GitHub).

## Combina com / alternativas

Combina com:
- [Tratamento de erros](05-tratamento-de-erros.md): a validação falha com erro claro.
- [Modularização e limites](03-modularizacao-e-limites.md): a borda é o limite do módulo.
- [Testes](08-testes.md): teste os casos inválidos da borda.

Alternativas: Valibot, ArkType (TypeScript), JSON Schema; escolha de linguagem e biblioteca fica na skill **stacks**.

## Decisão rápida

- **Use se:** o dado vem de fora do seu código (HTTP, arquivo, env, terceiros).
- **Evite se:** o dado já foi validado e tipado pela sua própria borda; não revalide a cada camada.
