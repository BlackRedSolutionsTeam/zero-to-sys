# Revisão de código

> Revisar é uma conversa para melhorar o código e espalhar conhecimento, não um julgamento da pessoa.

| | |
|---|---|
| **Referência** | Google Engineering Practices, "The Standard of Code Review" e "How to do a code review" (google.github.io/eng-practices); Conventional Comments (conventionalcomments.org) |
| **Categoria** | Processo |
| **Tipo** | Prática de equipe |
| **Vale para** | Qualquer linguagem e qualquer host de Git; também vale para pareamento |
| **Verificado em** | 2026-11-24 |

## O que é

É outra pessoa ler a mudança antes de ela entrar no código principal. O padrão do Google resume: aprove quando a mudança melhora a saúde geral do código, mesmo que não seja perfeita ("The Standard of Code Review").

O Google ("What to look for in a code review") lista design, funcionalidade, complexidade, testes, nomes, comentários, estilo e documentação.

## Por que usar

- **Qualidade:** o Google usa a revisão para manter a qualidade do código e dos produtos (guia de revisão, introdução).
- **Mentoria:** o Google trata ensinar e compartilhar conhecimento como parte da saúde do código ("The Standard of Code Review").

## Quando usar

- Todo PR que vai para a branch principal.
- Mudanças em área crítica (pagamento, segurança), com revisor que conhece o assunto.
- Antes de uma refatoração grande, para alinhar a ideia.

## Para que tipo de código

| Tipo de código/projeto | Encaixe | Por quê |
|---|---|---|
| Time com mais de uma pessoa | ✅ Ótimo | Aprove quando a mudança melhora a saúde do código (Google, "The Standard of Code Review") |
| Time com júnior | ✅ Ótimo | Ensinar e compartilhar conhecimento faz parte da saúde do código (Google, "The Standard of Code Review") |

## Quando é bom

- **Rápido:** o Google fixa um dia útil como tempo máximo de resposta ("Speed of Code Reviews").
- **Comentário claro e gentil:** sobre o código, não sobre a pessoa; explique o motivo.
- **Marca o peso:** "Nit:" (prefixo usado pelo Google) para detalhe opcional, "bloqueante" para o que precisa mudar. A convenção Conventional Comments propõe rótulos como `suggestion`, `issue`, `nitpick` e `question`.
- **Checklist curto:** funciona? É legível? Tem teste? Cabe no padrão?
- **Autor ajuda:** descrição clara e PR pequeno.

## Quando é ruim

- **Revisão por estilo:** discutir espaço e aspas que o formatador resolve.
- **Perfeccionismo:** o padrão do Google manda aprovar se a mudança melhora a saúde do código, mesmo imperfeita.
- **Carimbo:** "LGTM" sem ler.
- **Tom duro:** o Google pede para ser gentil e comentar o código, nunca a pessoa ("How to write code review comments").
- **Divergência:** revisão obrigatória em todo PR contra revisão depois do merge (confiança alta, times pequenos). 

## Como começar

Comentário ruim:

```text
Isso está errado. Refaz.
```

Comentário bom (pergunta, motivo e sugestão):

```text
suggestion: `getData` não diz o que busca. Que tal `fetchOpenOrders`?
Assim quem lê a chamada entende sem abrir a função.
```

Checklist rápido do revisor:

1. Entendi a mudança só pela descrição e pelo código?
2. A lógica está correta e os casos de erro estão cobertos?
3. Há teste para o comportamento novo?
4. Algo ficou mais complicado do que precisava? ([Simplicidade](04-simplicidade.md))
5. Um júnior consegue ler isso?

Para o autor: reveja o próprio diff antes de abrir o PR e explique o contexto na descrição.

## Combina com / alternativas

Combina com:
- [Commits e PRs pequenos](11-commits-e-prs-pequenos.md): PR pequeno é revisado de verdade.
- [Formatação e lint automáticos](09-formatacao-e-lint-automaticos.md): tira o estilo da conversa.
- [Testes](08-testes.md): o Google pede ao revisor que confira se os testes estão corretos e úteis.

Alternativas e complementos: pareamento (pair programming), programação em grupo (mob), revisão assistida por IA como primeira passada (não substitui a humana; confira os achados).

## Decisão rápida

- **Use se:** o código entra num repositório compartilhado, ou toca em algo crítico.
- **Evite se:** a revisão vira disputa de gosto; nesse caso, automatize o estilo e foque em lógica e legibilidade.
