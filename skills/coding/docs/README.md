# Práticas de código

Um documento por prática, explicando quando usar, em que tipo de código encaixa, quando ajuda, quando atrapalha e por quê. A lista ficou só com o que passa em três critérios: referência reconhecida, benefício real no dia a dia e aplicação simples por um júnior. Ferramentas e convenções foram verificadas nas fontes oficiais em 2026-11-24.

## Escrever o código

| Prática | O que é | Doc |
|---|---|---|
| Nomes claros | Nomes que revelam a intenção | [01-nomes-claros.md](01-nomes-claros.md) |
| Funções pequenas | Uma responsabilidade por função | [02-funcoes-pequenas.md](02-funcoes-pequenas.md) |
| Modularização e limites | Coesão alta, acoplamento baixo, dependência numa direção | [03-modularizacao-e-limites.md](03-modularizacao-e-limites.md) |
| Simplicidade | KISS, YAGNI e regra de três | [04-simplicidade.md](04-simplicidade.md) |

## Proteger o código

| Prática | O que é | Doc |
|---|---|---|
| Tratamento de erros | Falhar cedo, com contexto, sem engolir | [05-tratamento-de-erros.md](05-tratamento-de-erros.md) |
| Tipos e validação na borda | Validar o que vem de fora, confiar nos tipos por dentro | [06-tipos-e-validacao-na-borda.md](06-tipos-e-validacao-na-borda.md) |
| Testes | Verificar o comportamento que importa | [08-testes.md](08-testes.md) |

## Explicar e manter o código

| Prática | O que é | Doc |
|---|---|---|
| Sem comentários no código | Nome, função, teste e commit no lugar do comentário | [07-comentarios-e-documentacao.md](07-comentarios-e-documentacao.md) |
| Formatação e lint automáticos | A máquina decide o estilo | [09-formatacao-e-lint-automaticos.md](09-formatacao-e-lint-automaticos.md) |
| Refatoração segura | Melhorar a estrutura em passos pequenos | [10-refatoracao-segura.md](10-refatoracao-segura.md) |

## Trabalhar em equipe

| Prática | O que é | Doc |
|---|---|---|
| Commits e PRs pequenos | Conventional Commits e PR revisável | [11-commits-e-prs-pequenos.md](11-commits-e-prs-pequenos.md) |
| Revisão de código | Conversa para melhorar o código | [12-revisao-de-codigo.md](12-revisao-de-codigo.md) |

## Qual escolher

- **Código novo:** [nomes](01-nomes-claros.md), [simplicidade](04-simplicidade.md), [validação na borda](06-tipos-e-validacao-na-borda.md) e [testes](08-testes.md).
- **Legado:** primeiro [testes](08-testes.md), depois [refatoração segura](10-refatoracao-segura.md) em [commits pequenos](11-commits-e-prs-pequenos.md).
- **Função grande:** [funções pequenas](02-funcoes-pequenas.md) e [nomes](01-nomes-claros.md).
- **Arquivo grande ou tudo acoplado:** [modularização](03-modularizacao-e-limites.md). Pastas e estrutura ficam na skill architecture.
- **Código repetido:** [regra de três](04-simplicidade.md) antes de abstrair.
- **Projeto novo:** configure [lint e formatação](09-formatacao-e-lint-automaticos.md) no primeiro dia.
- **Revisando PR:** [revisão de código](12-revisao-de-codigo.md), com a [simplicidade](04-simplicidade.md) como lente.

## O que saiu da lista e por quê

| Prática | Motivo |
|---|---|
| Regras de tamanho fixo (funções de até 5 linhas, arquivos de até 200) | Números arbitrários; o teste do nome e da responsabilidade funciona melhor. Cada doc cita o exagero |
| DRY como regra absoluta | Leva a abstração errada; ficou como regra de três em [04](04-simplicidade.md) |
| SOLID como lista de regras | Útil como vocabulário, mas os cinco princípios ficam abstratos para júnior e levam a interfaces demais; a essência cabe em [03](03-modularizacao-e-limites.md) |
| Padrões de projeto (GoF) | Úteis em caso certo, mas aplicados cedo viram sobre-engenharia; aprenda sob demanda |
| TDD estrito como regra | A comunidade diverge (DHH criticou em 2014); ficou como "teste o comportamento" em [08](08-testes.md) |
| Cobertura de testes como meta | Mede o que rodou, não o que foi verificado |
| Programação funcional pura como regra | Ótima em certos trechos, mas é escolha de estilo e de linguagem (skill stacks) |
| "Comente o porquê" | Visão de Ousterhout; preferimos levar o porquê para nome, teste e commit, ver [07](07-comentarios-e-documentacao.md) |
| Estrutura de pastas e arquitetura (camadas, hexagonal, DDD) | Assunto da skill architecture |
| Escolha de linguagem e framework | Assunto da skill stacks |
