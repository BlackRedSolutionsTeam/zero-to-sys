---
name: coding
description: 'Boas práticas para código simples e legível por qualquer senioridade: nomes, funções pequenas, módulos, erros, validação, sem comentários, testes, lint, refatoração, commits e revisão. Use ao escrever ou alterar código, revisar PR ou quando pedirem "refatorar" ou "deixar limpo".'
---

# coding

Guia de decisão para escrever código claro, simples e bem dividido. Cada prática tem um documento em `docs/` com quando usar, em que tipo de código encaixa, quando ajuda, quando atrapalha (o exagero), como começar com exemplos curtos e decisão rápida.

Fronteiras: estrutura de pastas e arquivos do projeto é da skill **architecture**; escolha de linguagem e framework é da skill **stacks**. Aqui o foco é o código dentro dos arquivos.

## Como usar esta skill

1. **Descubra o contexto** antes de aplicar qualquer coisa: linguagem, se o projeto é novo ou legado, se há testes, lint e formatador configurados e quais convenções o repositório já tem (`AGENTS.md`, `CONTRIBUTING.md`, `.editorconfig`). O que o projeto já define tem prioridade sobre esta lista.
2. **Escolha as práticas pela tabela de decisão abaixo.**
3. **Leia o documento de cada prática escolhida** antes de mexer no código, principalmente "Quando é ruim" (o exagero) e "Como começar".
4. **Aplique em passos pequenos**, sem reescrever o que não foi pedido. Ao mexer em legado, mude só o necessário e separe a refatoração da funcionalidade.
5. **Rode formatador, lint e testes** do projeto antes de dar a tarefa por pronta.
6. **Explique as escolhas ao usuário em uma ou duas frases.**

## Qual prática usar

| Situação | Leia |
|---|---|
| Estou escrevendo código novo | [01 Nomes claros](docs/01-nomes-claros.md), [04 Simplicidade](docs/04-simplicidade.md), [06 Tipos e validação na borda](docs/06-tipos-e-validacao-na-borda.md), [08 Testes](docs/08-testes.md) |
| Estou mexendo em código legado | [10 Refatoração segura](docs/10-refatoracao-segura.md), [08 Testes](docs/08-testes.md), [11 Commits e PRs pequenos](docs/11-commits-e-prs-pequenos.md) |
| A função ficou grande | [02 Funções pequenas](docs/02-funcoes-pequenas.md), [01 Nomes claros](docs/01-nomes-claros.md) |
| O arquivo ou módulo ficou grande, ou tudo importa tudo | [03 Modularização e limites](docs/03-modularizacao-e-limites.md) (pastas e estrutura: skill architecture) |
| Tenho código repetido | [04 Simplicidade](docs/04-simplicidade.md) (regra de três), depois [10 Refatoração segura](docs/10-refatoracao-segura.md) |
| Estou lidando com erro, entrada de usuário ou API externa | [05 Tratamento de erros](docs/05-tratamento-de-erros.md), [06 Tipos e validação na borda](docs/06-tipos-e-validacao-na-borda.md) |
| Tive vontade de escrever um comentário | [07 Sem comentários no código](docs/07-comentarios-e-documentacao.md) |
| Estou configurando um projeto novo | [09 Formatação e lint automáticos](docs/09-formatacao-e-lint-automaticos.md) |
| Vou commitar ou abrir PR | [11 Commits e PRs pequenos](docs/11-commits-e-prs-pequenos.md) |
| Estou revisando um PR | [12 Revisão de código](docs/12-revisao-de-codigo.md), [04 Simplicidade](docs/04-simplicidade.md) |

| Prática | Documento | Papel |
|---|---|---|
| Nomes claros | [docs/01-nomes-claros.md](docs/01-nomes-claros.md) | O nome diz o que a coisa é ou faz |
| Funções pequenas | [docs/02-funcoes-pequenas.md](docs/02-funcoes-pequenas.md) | Uma responsabilidade por função |
| Modularização e limites | [docs/03-modularizacao-e-limites.md](docs/03-modularizacao-e-limites.md) | Alta coesão, baixo acoplamento, dependência numa direção |
| Simplicidade | [docs/04-simplicidade.md](docs/04-simplicidade.md) | KISS, YAGNI e regra de três |
| Tratamento de erros | [docs/05-tratamento-de-erros.md](docs/05-tratamento-de-erros.md) | Falhar cedo, com contexto, sem engolir |
| Tipos e validação na borda | [docs/06-tipos-e-validacao-na-borda.md](docs/06-tipos-e-validacao-na-borda.md) | Validar o que vem de fora e confiar nos tipos por dentro |
| Sem comentários no código | [docs/07-comentarios-e-documentacao.md](docs/07-comentarios-e-documentacao.md) | Nada de comentário: nome, função, teste e commit explicam |
| Testes | [docs/08-testes.md](docs/08-testes.md) | Testar comportamento, pirâmide ou troféu |
| Formatação e lint automáticos | [docs/09-formatacao-e-lint-automaticos.md](docs/09-formatacao-e-lint-automaticos.md) | Biome, ESLint + Prettier, Ruff, dotnet format |
| Refatoração segura | [docs/10-refatoracao-segura.md](docs/10-refatoracao-segura.md) | Passos pequenos com testes rodando |
| Commits e PRs pequenos | [docs/11-commits-e-prs-pequenos.md](docs/11-commits-e-prs-pequenos.md) | Conventional Commits e PR revisável |
| Revisão de código | [docs/12-revisao-de-codigo.md](docs/12-revisao-de-codigo.md) | Revisar a lógica e a legibilidade, não o estilo |

## Checklist de todo código novo ou alterado

- [ ] Formatador e lint passam sem erro (`pnpm lint`, ou o comando equivalente do projeto).
- [ ] Typecheck ou build passa (`pnpm typecheck`, `pnpm build`, ou o equivalente da stack).
- [ ] Os testes passam e o comportamento novo tem teste (`pnpm test`).
- [ ] Não há comentário no código, só diretivas exigidas por ferramenta (`git diff | grep -nE '^\+\s*(//|#|/\*)'`).
- [ ] Não há `console.log`, `print` ou código morto esquecido (`grep -rn 'console.log' src`).
- [ ] Não há `any`, `as` nem `catch` vazio para fazer passar (`grep -rnE ': any|as any|catch *\(.*\) *\{ *\}' src`).
- [ ] Dado de fora (formulário, API, arquivo) é validado uma vez na borda (abrir o ponto de entrada e achar o schema ou validador).
- [ ] Nenhuma função faz mais de uma coisa: o nome não pede "e" (ler o `git diff`).
- [ ] Refatoração e funcionalidade estão em commits separados, com mensagem no padrão do projeto (`git log --oneline -5`).

## Regras de uso

- **Escreva para o júnior.** Se uma pessoa em início de carreira não entende o código lendo uma vez, simplifique.
- **Sem comentários no código.** Se algo precisa de explicação, renomeie, extraia uma função ou escreva um teste; o porquê vai no commit ou no PR. Só diretivas exigidas por ferramenta (lint, typecheck, licença) são aceitas.
- **Uma responsabilidade por função e por módulo.** Se o nome pede "e", divida.
- **Simples primeiro.** Sem abstração, flag ou camada que ninguém pediu. Extraia na terceira repetição real, não na segunda.
- **Valide na borda, confie por dentro.** Dado de fora é validado uma vez; o resto usa tipos. Nada de `any` ou `as` para fazer passar.
- **Nunca engula erro.** `catch` vazio é proibido; trate onde há o que fazer ou deixe subir.
- **Dependência numa direção só.** Regra de negócio não importa banco, tela ou framework.
- **Siga o projeto.** Convenção, formatador e lint do repositório vencem esta lista. A máquina decide o estilo, não a revisão.
- **Refatoração separada de funcionalidade.** Commits e PRs diferentes, sempre com testes rodando.
- **Não reescreva o que não foi pedido.** Mude o mínimo que resolve e deixe o código um pouco melhor do que estava, só na área tocada.
- **Exagero também é defeito.** Funções de duas linhas, camadas para um CRUD e regras de lint demais pioram a leitura. Cada documento diz onde está o limite.

## Quando a lista não cobre

Se o pedido está fora destas doze práticas (arquitetura e pastas, escolha de stack, segurança, desempenho, acessibilidade, DDD), diga isso ao usuário em vez de forçar uma delas. Estrutura do projeto é da skill **architecture** e linguagem e framework são da **stacks**. O `docs/README.md` registra o que foi avaliado e saiu, com o motivo.

## Validade dos dados

Nomes de ferramentas, comandos e convenções foram verificados em 2026-11-24. Antes de afirmar versão ou comando decisivo ao usuário, confira na documentação oficial da ferramenta.
