# Termos de uso e contrato de SaaS

> Escreva o contrato depois de decidir o que o sistema consegue cumprir: cancelamento, reembolso, SLA e limites precisam existir como funcionalidade, não só como cláusula.

| | |
|---|---|
| **Referência** | CDC, Lei 8.078/1990, arts. 6, 39, 46, 47, 49, 51 e 54 (planalto.gov.br/ccivil_03/leis/l8078compilado.htm); Decreto 7.962/2013, arts. 2, 4 e 5 (planalto.gov.br/ccivil_03/_ato2011-2014/2013/decreto/d7962.htm); Marco Civil, Lei 12.965/2014, art. 7, VI e XIII |
| **Categoria** | Jurídico |
| **Tipo** | Lista de cláusulas e do que o sistema precisa suportar |
| **Vale para** | SaaS B2C (consumidor) e B2B (empresa), vendido no Brasil |
| **Verificado em** | 2026-11-25 |

> Não substitui advogado. Cláusulas de responsabilidade, foro, propriedade intelectual e limitação de dano exigem revisão jurídica.

## O que é

- **Termos de uso:** regras de uso do produto, aceitas no cadastro (contrato de adesão: o usuário não negocia, CDC art. 54).
- **Contrato de SaaS:** acordo com o cliente que contrata a assinatura, geralmente empresa. Pode ser os mesmos termos aceitos online ou um contrato assinado, negociado.
- **Contrato de adesão ao consumidor:** o CDC interpreta as cláusulas de forma mais favorável ao consumidor (art. 47), anula as abusivas (art. 51) e não obriga quem não pôde conhecer o conteúdo (art. 46).

## Por que usar

- Define o que o cliente recebe, quanto paga e como sai.
- Reduz disputa: cancelamento, reembolso e suspensão por falta de pagamento ficam escritos.
- Cliente B2B pede o contrato antes de comprar.

## Quando usar

- Antes de cobrar o primeiro cliente.
- Ao lançar plano novo, mudar preço, limite ou política de cancelamento.
- Quando o cliente exige SLA ou cláusulas próprias.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS B2C | ✅ Ótimo | Contrato de adesão sob o CDC; cláusula abusiva é nula |
| SaaS B2B pequeno | ✅ Ótimo | Termos online aceitos no cadastro, com proposta comercial |
| SaaS B2B grande | 🟡 Serve | O cliente manda o próprio contrato; o sistema precisa suportar o que for assinado |
| Site de conteúdo | 🟡 Serve | Termos curtos de uso e propriedade intelectual |
| Marketplace | 🟡 Serve | Contrato de três partes, com advogado desde o início |
| Sistema interno | ❌ Evite | Política de uso interno, não contrato de SaaS |

## Quando é bom

- **Cada cláusula tem um recurso correspondente** no produto (botão de cancelar, fatura, exportação).
- **Aceite registrado por versão** (doc [05](05-aceite-versionado.md)).
- **Resumo claro das cláusulas que limitam direitos**, visível antes de contratar: o Decreto 7.962/2013 (art. 4) pede sumário do contrato e cláusulas destacadas.
- **Planos e limites no produto**, iguais ao que o contrato diz.

## Quando é ruim

- **Cláusula que o sistema não cumpre**, como "cancele quando quiser" sem botão para cancelar.
- **Cláusula que tira do consumidor o que a lei garante** (CDC, art. 51, I, IV e XV): é nula, e a empresa perde credibilidade.
- **Alterar termos por e-mail sem versão nem novo aceite** quando a mudança piora a posição do usuário.
- **Foro, limitação de responsabilidade e indenização copiados** de contrato de outro setor.

## Como começar

**1. Cláusulas e o que o sistema precisa ter.**

| Cláusula | O que o sistema precisa suportar |
|---|---|
| Objeto e plano contratado | Plano e limites visíveis na conta e iguais ao contrato |
| Preço, reajuste e meios de pagamento | Preço total, com despesas extras, antes de pagar; aviso prévio de reajuste |
| Cancelamento | Cancelar pelo mesmo canal da contratação, sem ligar para ninguém; confirmação imediata |
| Arrependimento (consumidor, contratação fora do estabelecimento) | 7 dias a contar da contratação, devolução dos valores (CDC, art. 49); meio claro e eficaz, ferramenta da contratação, confirmação imediata e aviso à operadora do cartão (Decreto 7.962/2013, art. 5) |
| Reembolso | Estorno parcial ou total conforme a política; registro do motivo e da data |
| Suspensão por falta de pagamento | Estado "suspenso" com leitura liberada, prazo de carência e aviso por e-mail antes |
| SLA (disponibilidade e suporte) | Página de status e medição real do uptime; canal e prazo de suporte medidos |
| Dados do cliente ao fim do contrato | Exportação e prazo de guarda antes da exclusão |
| Limites de uso razoável | Limites no código e mensagem clara ao atingir |
| Uso proibido | Moderação, suspensão e registro do motivo |
| Alteração dos termos | Versão nova, aviso e novo aceite (doc [05](05-aceite-versionado.md)) |
| Propriedade intelectual e dados do cliente | Dados do cliente continuam dele; licença de uso do produto |
| Privacidade e operador | Remete à política e ao contrato de operador (docs [02](02-politica-de-privacidade-e-o-mapa-de-dados.md) e [07](07-contrato-de-operador-b2b-e-suboperadores.md)) |
| Lei aplicável e foro | Decisão do advogado; o consumidor tem regras próprias |

**2. Modelo de estrutura dos termos** (o texto vem do advogado):

1. Quem somos e quem pode usar.
2. O serviço e o plano.
3. Conta, senha e responsabilidade de acesso.
4. Preço, cobrança, reajuste, inadimplência.
5. Cancelamento, arrependimento e reembolso.
6. Uso aceitável e proibições.
7. Disponibilidade e suporte (SLA, quando houver).
8. Seus dados e nossa privacidade.
9. Propriedade intelectual.
10. Responsabilidade e limites.
11. Mudanças nos termos.
12. Contato, lei e foro.
13. Versão e data de vigência.

**3. Estado de assinatura no banco**, para o contrato ter correspondência no código.

```sql
CREATE TYPE subscription_status AS ENUM ('trialing', 'active', 'past_due', 'suspended', 'cancel_scheduled', 'canceled');

CREATE TABLE subscriptions (
  id uuid PRIMARY KEY,
  account_id uuid NOT NULL,
  plan_code text NOT NULL,
  status subscription_status NOT NULL,
  started_at timestamptz NOT NULL,
  cancel_requested_at timestamptz,
  canceled_at timestamptz,
  refund_reason text,
  terms_version text NOT NULL
);
```

**4. Cancelamento pelo mesmo canal.**

```ts
app.post("/billing/cancel", requireAuth, async (c) => {
  const accountId = c.get("accountId");
  await db.exec(
    "UPDATE subscriptions SET status = 'cancel_scheduled', cancel_requested_at = now() WHERE account_id = $1 AND status = 'active'",
    [accountId],
  );
  await mailer.send(accountId, "cancel-confirmation");
  return c.body(null, 202);
});
```

## Combina com / alternativas

- Regras de plano, cobrança e cancelamento do produto: skill `product`.
- Telas de aceite e checkout: skill `design-systems`.
- E-mails de confirmação: skill `integrations`.
- Contrato de operador: [07](07-contrato-de-operador-b2b-e-suboperadores.md).
- Alternativa: contrato negociado por advogado para clientes grandes; os termos online ficam para o autoatendimento.

## Decisão rápida

- **Use se:** o produto cobra ou aceita cadastro com regras de uso.
- **Evite se:** a cláusula promete algo que o sistema não faz; implemente primeiro, escreva depois.
