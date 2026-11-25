# Commits e PRs pequenos (Conventional Commits)

> Cada commit conta uma mudança só, com mensagem clara; cada PR cabe numa revisão de poucos minutos.

| | |
|---|---|
| **Referência** | Conventional Commits 1.0.0 (conventionalcommits.org); Google Engineering Practices, "Small CLs" (google.github.io/eng-practices); Pro Git (git-scm.com/book) |
| **Categoria** | Processo |
| **Tipo** | Prática de fluxo de trabalho |
| **Vale para** | Qualquer linguagem e qualquer host de Git (GitHub, GitLab, Azure DevOps) |
| **Verificado em** | 2026-11-24 |

## O que é

Duas práticas ligadas:

- **Commit atômico:** uma mudança lógica por commit, com mensagem que explica o quê e por quê (Pro Git, "Commit Guidelines": cada commit um conjunto de mudanças logicamente separado).
- **PR pequeno:** a soma dos commits é algo que alguém revisa de uma vez, sem se perder.

Conventional Commits 1.0.0 é uma convenção para a mensagem: `tipo(escopo opcional): descrição`. Os tipos do núcleo são `feat` (nova funcionalidade, vira MINOR no SemVer) e `fix` (correção, vira PATCH). A especificação permite outros tipos e cita que o `@commitlint/config-conventional` (convenção Angular) recomenda `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf` e `test`. Mudança que quebra compatibilidade usa `!` antes dos dois pontos (`feat!: ...`) ou o rodapé `BREAKING CHANGE:`.

## Por que usar

- **Revisão melhor:** o Google ("Small CLs") diz que mudanças pequenas são revisadas mais rápido e com mais cuidado.
- **Automação:** o Conventional Commits permite gerar CHANGELOG e determinar a versão a partir dos commits.

## Quando usar

- Em todo projeto com Git, e sempre que mais de uma pessoa revisa.
- Conventional Commits: quando o projeto gera changelog ou versão automática, ou o time quer um histórico padronizado.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Time com revisão de PR | ✅ Ótimo | Mudanças pequenas são revisadas mais rápido e com mais cuidado (Google, "Small CLs") |
| Biblioteca com versionamento | ✅ Ótimo | `feat` vira MINOR e `fix` vira PATCH no SemVer (Conventional Commits 1.0.0) |
| Monorepo | ✅ Ótimo | Escopo opcional no formato `tipo(escopo): descrição` (Conventional Commits 1.0.0) |

## Quando é bom

- **Uma ideia por commit:** corrigir bug e renomear arquivo são dois commits.
- **Mensagem no imperativo** (Pro Git) **e específica:** `fix: impede pedido sem itens`.
- **Corpo explica o porquê** quando não é óbvio.
- **PR com descrição:** o que muda, por que, como testar.
- **Refatoração separada:** commit ou PR só de refatoração, sem mudar comportamento.

## Quando é ruim

- **Fatiar demais:** 40 commits de "ajuste" num PR de 10 linhas; ou PRs que só fazem sentido juntos, entregues separados e quebrados.
- **Tipo errado:** `feat` correlaciona com MINOR e `fix` com PATCH no SemVer; tipo errado gera versão errada.
- **Divergência:** alguns times usam squash merge (um commit por PR, e a mensagem do PR é a que vale); outros preservam os commits. Defina uma regra e valide o título do PR.
- **Sem limite oficial de linhas por PR.** O guia de revisão do Google (eng-practices) diz que não há regra fixa: cerca de 100 linhas costuma ser um tamanho razoável e 1000 linhas costuma ser grande demais, e o número de arquivos também pesa. Referência conferida em 2026-11-24.

## Como começar

Antes:

```text
git commit -m "ajustes"
git commit -m "fix bug"
```

Depois:

```text
fix(orders): impede criar pedido sem itens

O endpoint aceitava lista vazia e gerava pedido com total zero.

feat(auth)!: troca o login por e-mail por login com CPF

BREAKING CHANGE: o campo `email` deixa de ser aceito em /login.
```

Fluxo: branch curta, commits pequenos, PR com descrição, merge rápido. Para validar a mensagem, existe o commitlint (commitlint.js.org); confira a configuração na documentação. Siga as regras do repositório se já houver.

## Combina com / alternativas

Combina com:
- [Revisão de código](12-revisao-de-codigo.md): PR pequeno é revisável.
- [Refatoração segura](10-refatoracao-segura.md): um passo, um commit.
- [Formatação e lint automáticos](09-formatacao-e-lint-automaticos.md): CI valida o PR.

Alternativas: mensagens livres com boas práticas (verbo no imperativo, resumo curto); gitmoji.

## Decisão rápida

- **Use se:** o código passa por revisão, ou o projeto tem versão e changelog.
- **Evite se:** a convenção seria só burocracia (projeto solo pequeno); mesmo assim, mantenha commits pequenos.
