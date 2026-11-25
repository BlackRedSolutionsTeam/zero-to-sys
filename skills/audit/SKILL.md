---
name: audit
description: Audita um projeto existente e diz o que está bom e o que falta, área por área, com evidência — confronta o código com o checklist de cada skill do plugin (arquitetura, código, dados, API, testes, segurança, integrações, experiência do usuário, infra, configuração do agente e produto), classifica em ok, atenção, falta ou não verificado, e ordena o que corrigir por risco e esforço. Use sempre que o usuário pedir "audita o projeto", "o que falta nesse projeto", "diagnóstico", "está bem feito?", "saúde do código", "revisão geral", "por onde começo a melhorar" ou ao assumir um projeto desconhecido, antes de mudar qualquer coisa. Só diagnostica: não altera código; a correção passa pela skill da área.
---

# audit

Guia para avaliar um projeto existente com o mesmo critério do plugin, em vez de cada análise sair diferente. O resultado é um relatório com o status de cada área, a evidência de cada achado e uma ordem de correção. Esta skill não muda código nem escolhe a solução: aponta o problema e a skill que o resolve.

## Como usar esta skill

1. **Descubra o projeto sem perguntar:** leia manifestos (`package.json`, `*.csproj`, `pyproject.toml`, `go.mod`), `README`, `CLAUDE.md`, `ARCHITECTURE.md`, `BACKLOG.md`, `.github/workflows`, a árvore de pastas e o histórico recente do Git. Pergunte ao usuário só o que não der para descobrir.
2. **Escolha as áreas que se aplicam** ao tipo de projeto (por exemplo, projeto sem banco pula `data`; API pula `user-experience`).
3. **Rode o checklist de cada área.** Cada `SKILL.md` do plugin tem uma seção "Checklist" com itens verificáveis e o jeito de verificar. Use comandos só de leitura (`ls`, `grep`, `git log`, `pnpm lint`, `pnpm test`); nunca rode migration, deploy ou comando que altere dados.
4. **Registre a evidência de cada item:** arquivo e linha, ou a saída do comando. Item que não deu para verificar é "não verificado", nunca "ok" por suposição.
5. **Monte o relatório** no formato do [doc 02](docs/02-relatorio-e-status.md) e **ordene os achados** pelo [doc 03](docs/03-priorizacao-e-plano.md).
6. **Entregue e proponha o primeiro passo:** poucos itens, pequenos, cada um com a skill que resolve. Não corrija nada sem o usuário pedir.

Em base grande, use o índice de código da skill `code-indexes` e rode uma área por subagente, em paralelo.

## Áreas e onde está o checklist

| Área | Skill | Pergunta que responde |
|---|---|---|
| Produto | [product](../product/SKILL.md) | Existem escopo, regras e critérios de aceite escritos? |
| Stack | [stacks](../stacks/SKILL.md) | A stack está completa e coerente com o porte? |
| Arquitetura | [architecture](../architecture/SKILL.md) | As pastas seguem o padrão da stack e acham-se os arquivos? |
| Dados | [data](../data/SKILL.md) | O modelo, as migrations e o isolamento por empresa estão corretos? |
| API | [api](../api/SKILL.md) | Rotas, erros e listas seguem um padrão e há OpenAPI? |
| Código | [coding](../coding/SKILL.md) | Lint, formatação, erros e validação estão no lugar? |
| Qualidade | [quality](../quality/SKILL.md) | Há testes por camada, CI com gates e definição de pronto? |
| Segurança | [security](../security/SKILL.md) | Login, permissões, limites e dependências estão seguros? |
| Integrações | [integrations](../integrations/SKILL.md) | Pagamento, e-mail, filas e webhooks são robustos? |
| Experiência | [user-experience](../user-experience/SKILL.md), [design-systems](../design-systems/SKILL.md), [design](../design/SKILL.md) | A interface funciona em celular, tablet e desktop, com todos os estados? |
| Infra | [infra](../infra/SKILL.md) | Há CI/CD, staging, backup testado, segredos e monitoramento? |
| Agente | [ia](../ia/SKILL.md), [code-indexes](../code-indexes/SKILL.md) | O projeto está pronto para trabalhar com agente de IA? |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Como auditar | [docs/01-como-auditar.md](docs/01-como-auditar.md) | Procedimento, evidência, comandos seguros |
| Relatório e status | [docs/02-relatorio-e-status.md](docs/02-relatorio-e-status.md) | Formato do relatório e dos status |
| Priorização e plano | [docs/03-priorizacao-e-plano.md](docs/03-priorizacao-e-plano.md) | Ordem de correção e qual skill resolve |

## Regras de uso

- **Só leitura.** A auditoria não altera arquivo, banco nem ambiente. Se um comando puder mudar algo, não rode.
- **Evidência em todo achado.** Arquivo e linha ou saída de comando; sem evidência, é opinião.
- **Não verificado não é ok.** Se não deu para checar (sem acesso à produção, sem permissão), diga "não verificado" e o que faltou.
- **Segurança e perda de dados primeiro.** Segredo no repositório, backup nunca restaurado e permissão quebrada vêm antes de estilo.
- **Pouco e pequeno.** Entregue os 5 a 10 achados mais importantes, não uma lista de cem; o resto vai agrupado.
- **Respeite o que já existe.** Padrão do projeto que difere do plugin mas é coerente não é falha; diga e siga.
- **Não proponha trocar a stack.** Só se o usuário pedir.
- **Cada achado aponta uma skill e um documento** que resolve, para o próximo passo ser direto.

## Quando a lista não cobre

Auditoria de conformidade formal (ISO 27001, SOC 2, PCI), pentest, revisão de código linha a linha de um PR (use `/code-review`), análise de custo de nuvem e revisão jurídica ficam fora desta skill. Diga isso ao usuário.

## Validade dos dados

Esta skill não traz preços nem versões; os critérios vêm do checklist de cada skill, conferido em 2026-11-24. Se um checklist mudar, a auditoria muda junto.
