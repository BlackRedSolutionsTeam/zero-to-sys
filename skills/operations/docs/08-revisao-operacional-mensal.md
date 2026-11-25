# Revisão operacional mensal

> Uma reunião curta por mês para olhar os números, os incidentes e o cansaço do plantão e decidir o que melhorar.

| | |
|---|---|
| **Referência** | https://sre.google/sre-book/service-level-objectives/, https://sre.google/sre-book/postmortem-culture/ |
| **Categoria** | Operação |
| **Tipo** | Prática de rotina |
| **Vale para** | Qualquer sistema em produção |
| **Verificado em** | 2026-11-25 |

## O que é

Encontro de 45 a 60 minutos, uma vez por mês, com pauta fixa: metas cumpridas, incidentes e ações, alertas, custo, backup e suporte. Termina com no máximo três decisões e um dono para cada.

## Por que usar

- Padrões aparecem só quando se olha o conjunto.
- Mantém as ações dos postmortems andando.
- Reajusta metas e alertas com dados.
- Evita surpresa na fatura e no vencimento de certificado, domínio e contrato.

## Quando usar

- Todo mês, em dia fixo, mesmo sem incidente.
- Mais curta (20 minutos) em time de uma pessoa, sozinho, com a lista.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | 15 minutos a cada trimestre |
| MVP de SaaS | ✅ Ótimo | Pega o que a correria esconde |
| SaaS em crescimento | ✅ Ótimo | Orçamento de erro guia a prioridade |
| Sistema interno | 🟡 Serve | Trimestral |
| Contrato com SLA | ✅ Ótimo | Relatório para o cliente sai daqui |
| Reunião sem números | ❌ Evite | Vira conversa de corredor |

## Quando é bom

- **Pauta fixa e números prontos** (30 minutos de preparo).
- **Poucas decisões**, com dono e data.
- **Registro** no repositório, em `docs/operacao/AAAA-MM.md`.

## Quando é ruim

- **Virar apresentação de slides.**
- **Mesma lista de problemas todo mês** sem ação.
- **Só técnica:** inclua suporte e custo.

## Como começar

Modelo de ata:

```markdown
# Revisão operacional AAAA-MM

Participantes:

## Números do mês
| Item | Meta | Resultado |
|---|---|---|
| Disponibilidade | 99,5% | |
| Requisições sem 5xx | 99% | |
| Minutos de queda | até 216 | |
| Incidentes SEV1 e SEV2 | | |
| Alertas que acordaram alguém | | |
| Desses, sem ação necessária | | |
| Chamados abertos / resolvidos | | |
| Tempo da primeira resposta (mediana) | | |

## Incidentes
- Resumo de cada um e link do postmortem.
- Ações do mês anterior: feitas / atrasadas.

## Alertas
- Silenciar, ajustar ou criar: lista com dono.

## Capacidade e custo
- Disco, RAM, banco: tendência e quando estoura.
- Custo do mês e variação.

## Backup e segurança
- Última restauração testada: data. Próxima: data.
- Certificados, domínios e contratos vencendo nos próximos 60 dias.
- Dependências com atualização de segurança pendente.

## Plantão
- Quantas vezes acordou alguém? Cansaço? Ajuste de escala.

## Suporte
- Cinco motivos mais comuns e itens enviados ao backlog.

## Decisões (máximo 3)
| Decisão | Dono | Prazo |
|---|---|---|
```

Conta do orçamento: com meta 99,5% em 30 dias, o orçamento é 216 minutos de queda (ver tabela do [doc 01](01-slo-severidade-e-plantao.md)). Se mais de 50% foi gasto em metade do mês, congele mudanças arriscadas.

Rotina de restauração (trimestral): restaure o último backup num banco de teste e meça o tempo; passo a passo em [backup e restauração](../../vps/docs/05-backup-e-restauracao-na-vps.md).

## Combina com / alternativas

- [SLO](01-slo-severidade-e-plantao.md), [alertas](02-alertas-que-valem-acordar.md), [postmortem](06-postmortem-sem-culpa.md) e [suporte](07-suporte-ao-cliente.md) alimentam a pauta.
- [Observabilidade](../../infra/docs/10-observabilidade.md) e [backup e recuperação](../../infra/docs/11-backup-e-recuperacao.md) fornecem os dados.
- Backlog: skill `product`.

## Decisão rápida

- **Use se:** há produção com cliente: um dia fixo por mês, a pauta acima, três decisões no máximo.
- **Evite se:** vai virar reunião sem números ou sem dono para as ações.
