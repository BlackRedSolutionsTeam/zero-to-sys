# Rotina trimestral de saúde do projeto

> A cada três meses, reserve meio dia para conferir versões, dependências, backup, dívida e código morto, registre o resultado e decida o que entra no próximo trimestre.

| | |
|---|---|
| **Referência** | DORA, "Software delivery performance metrics" (dora.dev/guides/dora-metrics); Google SRE Book, capítulo "Eliminating Toil"; fontes de cada item citadas nos docs 01 a 06 |
| **Categoria** | Manutenção |
| **Tipo** | Prática de processo recorrente |
| **Vale para** | Qualquer projeto em produção |
| **Verificado em** | 2026-11-25 |

## O que é

Uma reunião curta e um checklist que se repetem em datas fixas (1º de fevereiro, maio, agosto e novembro, por exemplo). O objetivo é achar cedo o que envelhece em silêncio: versão que vai vencer, backup que não restaura, alerta ignorado, pacote sem uso. O diagnóstico usa a skill `audit` (somente leitura); a correção segue os docs desta skill.

## Por que usar

- **O que não tem data não acontece.**
- **Mostra a tendência:** melhorou ou piorou desde o último trimestre.
- **Dá argumento ao negócio:** relatório curto com datas e riscos.

## Quando usar

- Em todo projeto em produção, a cada três meses.
- Também depois de um incidente grave ou de uma troca de equipe.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Uma versão enxuta, de 30 minutos |
| MVP de SaaS | ✅ Ótimo | Pega o que ficou para trás na correria |
| SaaS em crescimento | ✅ Ótimo | Vários donos; a rotina alinha o time |
| Sistema interno/corporativo | ✅ Ótimo | Evita o abandono silencioso |
| API/integração | ✅ Ótimo | Confere versão, contrato e consumidores |
| App mobile com backend | ✅ Ótimo | Confere também as versões de app em uso |
| Projeto desativado | ❌ Evite | Desligue-o em vez de manter |

## Quando é bom

- **Data marcada na agenda** de uma pessoa responsável, com substituto.
- **Mesmo checklist** todo trimestre, para comparar.
- **Resultado escrito** em um arquivo do repositório, com data.
- **Saída acionável:** no máximo 5 itens para o próximo trimestre, com dono.

## Quando é ruim

- **Virar reunião longa** sem decisão.
- **Fazer só quando dá tempo.**
- **Corrigir durante a revisão:** primeiro diagnostique, depois entre com PRs separados (como na skill `audit`).
- **Checklist enorme:** cansa e vira formalidade.

## Como começar

### Checklist (meio dia)

**1. Suporte e versões** ([doc 01](01-calendario-de-fim-de-suporte.md))
- [ ] Runtime, framework e banco: versão em uso e data de fim de suporte conferida hoje.
- [ ] Algo vence em menos de 6 meses? Vira item do trimestre.
- [ ] Imagem do Docker, sistema operacional da VPS e versão do Docker (skill `vps`, [doc 04](../../vps/docs/04-atualizacoes-docker-e-swap.md)).

**2. Dependências** ([doc 02](02-atualizacao-automatica-de-dependencias.md))
- [ ] PRs do robô abertos há mais de 30 dias: decidir.
- [ ] Auditoria no CI verde; alertas abertos com dono e prazo (skill `security`, doc 08).
- [ ] Algum pacote abandonado (sem lançamento há mais de um ano)?

**3. Segurança e acessos** (skill `security`)
- [ ] Contas de ex-membros removidas do repositório, do provedor e dos serviços.
- [ ] Chaves e segredos com mais de um ano trocados (skill `infra`, [doc 09](../../infra/docs/09-segredos-e-configuracao.md)).
- [ ] 2FA ativo nas contas críticas.

**4. Dados e continuidade** (skill `infra`, [doc 11](../../infra/docs/11-backup-e-recuperacao.md))
- [ ] Restauração do backup testada neste trimestre; data anotada.
- [ ] Disco, certificado e domínio com mais de 30 dias de folga.
- [ ] Alertas de monitoramento disparam de verdade (teste um).

**5. Saúde do código** ([doc 05](05-divida-tecnica.md) e [06](06-codigo-morto-e-dependencias-sem-uso.md))
- [ ] Dívida técnica: o que entrou, o que saiu, o que tem mais nota.
- [ ] Rodar a ferramenta de código morto e dependências sem uso.
- [ ] Tempo de build e de testes: piorou?
- [ ] Testes instáveis (flaky) listados.

**6. Entrega** (skill `quality`)
- [ ] Gates obrigatórios ainda ligados no CI ([doc 07](../../quality/docs/07-quality-gates-no-ci.md)).
- [ ] Tempo entre commit e produção e taxa de rollback (métricas DORA, se medidas).

### Usar a skill audit

Para o diagnóstico completo, siga a skill `audit`: [como auditar](../../audit/docs/01-como-auditar.md), [relatório e status](../../audit/docs/02-relatorio-e-status.md) e [priorização e plano](../../audit/docs/03-priorizacao-e-plano.md). A comparação com o trimestre anterior é o que a "reauditoria" faz.

### Comandos úteis

```bash
git log --since="3 months ago" --oneline | wc -l
git shortlog -sn --since="3 months ago"
gh pr list --state open --search "author:app/dependabot author:app/renovate"
npm outdated
dotnet list package --outdated
pip list --outdated
composer outdated --direct
```

### Registro

`docs/saude-do-projeto.md`:

```markdown
## 2026-11-25

| Área | Estado | Observação |
|---|---|---|
| Versões | Atenção | Postgres 14 sem suporte desde 2026-11-12 |
| Dependências | Ok | 0 alertas altos |
| Backup | Ok | Restauração testada em 2026-11-20 |
| Dívida | Atenção | 14 itens, 3 de nota alta |

## Para o próximo trimestre
1. Atualizar Postgres 14 para 18 (dono: Ana, até 2027-01-31)
2. Remover 6 pacotes sem uso (dono: Bruno)
```

Quem vai mexer em algo grande abre uma issue por item e usa o doc correspondente.

### Agendar

A rotina pode ser lembrada por uma issue recorrente criada por workflow agendado (skill `infra`, [GitHub Actions](../../infra/docs/07-github-actions.md)) ou por um evento de calendário. O agendador do GitHub Actions (`schedule`) usa horário UTC e pode atrasar em horários de pico.

## Combina com / alternativas

- Skill `audit`: diagnóstico e relatório.
- Skill `security`: [dependências vulneráveis](../../security/docs/08-dependencias-vulneraveis.md).
- Skill `quality`: [gates no CI](../../quality/docs/07-quality-gates-no-ci.md).
- Skill `infra`: backup, segredos e observabilidade.
- Alternativa: rotina mensal para sistemas críticos; semestral é o máximo aceitável para um sistema pequeno.

## Decisão rápida

- **Use se:** o sistema está em produção e alguém depende dele.
- **Evite se:** o sistema será desligado em menos de um trimestre.
