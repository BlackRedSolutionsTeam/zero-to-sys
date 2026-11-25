# Priorização e plano de correção

> Ordene os achados por risco e esforço (segurança e perda de dados primeiro), corrija em passos pequenos, um PR por achado, e reaudite depois.

| | |
|---|---|
| **Referência** | Google Engineering Practices, "Small CLs" (google.github.io/eng-practices/review/developer/small-cls.html); DORA, "Software delivery performance metrics" (dora.dev/guides/dora-metrics), que recomenda reduzir o tamanho das mudanças; OWASP ASVS 5.0.0 e OWASP Top 10 para ordenar riscos de segurança; "Refactoring Databases" (Ambler e Sadalage) para mudanças de banco em etapas |
| **Categoria** | Auditoria |
| **Tipo** | Prática de planejamento de correções |
| **Vale para** | Qualquer projeto com um relatório de auditoria pronto |
| **Verificado em** | 2026-11-24 |

## O que é

Depois do relatório ([doc 02](02-relatorio-e-status.md)), os achados precisam de ordem. A ordem vem de duas perguntas: quão grave é o que pode acontecer (risco) e quanto custa corrigir (esforço). Cada achado vira um passo pequeno, com um PR só, e a skill da área executa a correção.

## Por que usar

- **O mais perigoso sai primeiro,** mesmo que não seja o mais fácil.
- **PR pequeno é revisável e reversível.** O DORA aponta reduzir o tamanho da mudança como caminho para entregar mais rápido e com mais estabilidade.
- **Sem reforma geral.** O projeto continua entregando enquanto melhora.

## Quando usar

- Logo depois de entregar o relatório e ter o ok do usuário sobre o que corrigir.
- Em cada reauditoria, para renovar a fila.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucos achados; uma lista curta basta |
| MVP de SaaS | ✅ Ótimo | Pouco tempo e dinheiro: a matriz mostra o que dá para adiar |
| SaaS em crescimento | ✅ Ótimo | Muitos achados e várias pessoas; a fila evita brigas por prioridade |
| Sistema interno/corporativo | ✅ Ótimo | Sem dono claro de dívida; o plano dá ordem e responsável |
| API/integração | ✅ Ótimo | Mudança de contrato pede etapas e aviso a quem consome |
| App mobile com backend | ✅ Ótimo | Versão antiga do app limita o que pode mudar no backend |
| Projeto sem ninguém para revisar ou entregar os PRs | ❌ Evite | O plano não anda; resolva primeiro quem executa |

## Quando é bom

- **Risco antes de esforço.** Um achado de segurança grande vai antes de dez achados fáceis de estilo.
- **Ganho rápido junto:** o que é grave e barato (por exemplo, ligar o backup) entra logo.
- **Um achado, um PR,** com a evidência do relatório na descrição.
- **O usuário escolhe.** Você propõe a ordem; ele decide o que entra.

## Quando é ruim

- **Juntar tudo num PR de "melhorias".** Ninguém revisa direito e reverter fica impossível.
- **Corrigir pelo que é fácil,** deixando o grave para depois.
- **Trocar a stack por conta própria.** O relatório diz o que falta, não "reescreva em outra tecnologia". Veja a seção abaixo.
- **Plano sem reauditoria.** Sem rever, ninguém sabe se melhorou.

## Como começar

### Passo 1: classificar risco e esforço

Risco, da maior para a menor prioridade:

1. **Segurança e dados de outras pessoas:** vazamento entre clientes, senha ou chave exposta, permissão ausente.
2. **Perda de dados:** sem backup, migration sem rede de segurança, exclusão sem volta.
3. **Fora do ar:** sem monitoramento, deploy sem reversão, sem teste do fluxo principal.
4. **Manutenção:** código confuso, sem lint, estrutura difícil.
5. **Experiência:** tela ruim no celular, acessibilidade.

Esforço: **pequeno** (até um dia, um PR), **médio** (até uma semana, poucos PRs), **grande** (mais de uma semana ou muda o modelo).

### Passo 2: matriz

| | Esforço pequeno | Esforço médio | Esforço grande |
|---|---|---|---|
| **Risco alto** | Faça agora | Faça agora, em etapas | Quebre em PRs e comece já |
| **Risco médio** | Faça logo em seguida | Agende | Agende e reavalie |
| **Risco baixo** | Faça se sobrar tempo | Só se o time pedir | Não faça agora |

Dentro de uma mesma célula, segurança e perda de dados vêm antes.

### Passo 3: montar o plano em passos pequenos

Para o exemplo do [doc 02](02-relatorio-e-status.md):

| Ordem | Achado | Risco | Esforço | PR |
|---|---|---|---|---|
| 1 | A2: sem backup do Postgres | Alto | Pequeno | Rotina de backup e teste de restauração |
| 2 | A1: agenda sem filtro por clínica | Alto | Médio | PR 1: coluna `clinic_id` nula e backfill. PR 2: filtro nas rotas e `not null`. PR 3: teste |
| 3 | A3: sem e2e do agendamento | Médio | Médio | Teste do fluxo principal no CI |
| 4 | `lint` fora do CI | Baixo | Pequeno | Passo de lint no workflow |

Note que a ordem 1 e 2 troca a mais fácil pela mais grave só quando as duas têm risco alto: o backup vem primeiro porque protege o trabalho da correção de dados.

Cada PR segue este roteiro:

1. Abra uma branch só para o achado.
2. Leia o doc da skill indicada na tabela abaixo.
3. Corrija só o que o achado descreve.
4. Rode testes e lint e anexe a saída (skill `quality`, [doc 08](../../quality/docs/08-definition-of-done.md)).
5. Na descrição do PR, cole a evidência do relatório e diga como conferir que sumiu.

### Passo 4: qual skill resolve cada achado

| Achado | Skill | Doc |
|---|---|---|
| Consulta sem filtro por cliente ou clínica | `data` | [06-multiempresa](../../data/docs/06-multiempresa.md) |
| Dado pessoal sem proteção | `data` | [10-dados-pessoais-e-lgpd](../../data/docs/10-dados-pessoais-e-lgpd.md) |
| Alteração de banco feita na mão | `data` | [04-migrations](../../data/docs/04-migrations.md) |
| Consulta lenta, falta índice | `data` | [08-indices-e-paginacao](../../data/docs/08-indices-e-paginacao.md) |
| Erro de API sem formato único | `api` | [03-formato-de-erro](../../api/docs/03-formato-de-erro.md) |
| Lista sem limite | `api` | [04-paginacao-e-filtros](../../api/docs/04-paginacao-e-filtros.md) |
| Sem OpenAPI | `api` | [07-openapi-e-documentacao](../../api/docs/07-openapi-e-documentacao.md) |
| Login ou sessão frágil | `security` | [02-sessao-e-tokens](../../security/docs/02-sessao-e-tokens.md) |
| Sem papéis e permissões | `security` | [04-papeis-e-permissoes](../../security/docs/04-papeis-e-permissoes.md) |
| Segredo no código | `infra` | [09-segredos-e-configuracao](../../infra/docs/09-segredos-e-configuracao.md) |
| Sem backup | `infra` | [11-backup-e-recuperacao](../../infra/docs/11-backup-e-recuperacao.md) |
| Sem monitoramento | `infra` | [10-observabilidade](../../infra/docs/10-observabilidade.md) |
| Sem CI | `infra` | [07-github-actions](../../infra/docs/07-github-actions.md) |
| Sem teste do fluxo principal | `quality` | [05-ponta-a-ponta-com-playwright](../../quality/docs/05-ponta-a-ponta-com-playwright.md) |
| Nada barra o PR | `quality` | [07-quality-gates-no-ci](../../quality/docs/07-quality-gates-no-ci.md) |
| Sem lint nem formatação | `coding` | [09-formatacao-e-lint-automaticos](../../coding/docs/09-formatacao-e-lint-automaticos.md) |
| Arquivo ou função gigante | `coding` | [02-funcoes-pequenas](../../coding/docs/02-funcoes-pequenas.md) |
| Pastas sem lógica | `architecture` | [01-feature-first-colocation](../../architecture/docs/01-feature-first-colocation.md) |
| Tela ruim no celular | `user-experience` | [02-mobile](../../user-experience/docs/02-mobile.md) |
| Sem acessibilidade | `user-experience` | [14-acessibilidade](../../user-experience/docs/14-acessibilidade.md) |
| Sem CLAUDE.md nem AGENTS.md | `ia` | [01-claude-md-agents-md](../../ia/docs/01-claude-md-agents-md.md) |
| Sem backlog nem regras escritas | `product` | [05-regras-de-negocio](../../product/docs/05-regras-de-negocio.md) |

### Passo 5: o que não corrigir de imediato

- **Não troque a stack.** Falta de teste não é motivo para sair do Next.js. Só a skill `stacks`, e só se o usuário pedir.
- **Não reorganize todas as pastas de uma vez.** Aplique a estrutura nova ao que for tocado.
- **Não renomeie colunas ou rotas em uso** sem as etapas dos docs de migrations e de versionamento.
- **Não corrija o que foi decisão consciente do usuário** (algo que ele fixou). Diga o risco em uma frase e siga.
- **Não conserte achado "não verificado"** como se fosse falta: primeiro consiga o acesso e verifique.

### Passo 6: reauditar

Reaudite depois de cada lote de PRs ou a cada trimestre. Use as mesmas áreas e a mesma ordem do relatório anterior, e compare: o que passou para ok, o que piorou, o que apareceu. O DORA sugere repetir o ciclo medir, melhorar e verificar, com o time, em vez de tratar a melhora como evento único.

## Combina com / alternativas

- [01-como-auditar.md](01-como-auditar.md) e [02-relatorio-e-status.md](02-relatorio-e-status.md): de onde vêm os achados.
- Skill `zero-to-sys`, seção "Projeto existente": a ordem geral das skills quando o projeto já tem código.
- Skill `coding`, [doc 11](../../coding/docs/11-commits-e-prs-pequenos.md): como manter cada PR pequeno.
- Alternativa: um backlog no `BACKLOG.md` (skill `product`) com os achados como histórias, quando o time já trabalha assim.

## Decisão rápida

- **Use se:** há achados de risco diferente e pouco tempo para corrigir tudo.
- **Evite se:** o relatório tem só um ou dois achados; corrija direto, sem matriz.
