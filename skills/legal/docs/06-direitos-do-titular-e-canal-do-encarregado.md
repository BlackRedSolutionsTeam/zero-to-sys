# Direitos do titular e canal do encarregado

> Tenha um canal público, uma fila de pedidos com prazo e o nome do encarregado (ou o canal que o substitui) visíveis no site.

| | |
|---|---|
| **Referência** | LGPD, arts. 18, 19 e 41 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); Resolução CD/ANPD nº 18/2024, regulamento do encarregado (publicada no DOU em 17/07/2024); Resolução CD/ANPD nº 2/2022, agentes de pequeno porte, art. 11; agenda regulatória da ANPD 2025-2026 (gov.br/anpd) |
| **Categoria** | Jurídico |
| **Tipo** | Prática de atendimento ao titular |
| **Vale para** | Qualquer sistema que trate dado de pessoa no Brasil |
| **Verificado em** | 2026-11-25 |

> Não substitui advogado. Quem deve indicar encarregado, e como responder cada pedido, é decisão jurídica.

## O que é

O **titular** é a pessoa a quem os dados se referem. O art. 18 lista o que ele pode pedir ao controlador: confirmação do tratamento, acesso, correção, anonimização, bloqueio ou eliminação de dado desnecessário ou excessivo, portabilidade, eliminação dos dados tratados com consentimento, informação sobre com quem os dados foram compartilhados, informação sobre as consequências de não consentir e revogação do consentimento. O **encarregado** (art. 41) é o canal entre controlador, titulares e ANPD; aceita reclamações, presta esclarecimentos e adota providências.

## Por que usar

- **Prazo legal:** a confirmação e o acesso saem de imediato, em formato simplificado, ou por declaração completa em até 15 dias (art. 19).
- **Reclamação ao ANPD:** quem não responde o titular acaba na autoridade.
- **Cliente B2B** pergunta quem é o encarregado e como pedidos são tratados.

## Quando usar

- Antes do lançamento: o canal precisa existir quando o primeiro usuário entra.
- Ao decidir se o produto indica encarregado ou usa o canal substituto.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS B2C | ✅ Ótimo | Muitos titulares, pedidos frequentes |
| SaaS B2B | ✅ Ótimo | Titulares são usuários do cliente; o pedido pode chegar a você e ao cliente (ver [07](07-contrato-de-operador-b2b-e-suboperadores.md)) |
| Loja online | ✅ Ótimo | Pedidos de exclusão e de nota |
| Site de conteúdo | 🟡 Serve | E-mail de contato e formulário |
| Startup e microempresa | 🟡 Serve | Pode estar dispensada de indicar encarregado, mas mantém canal (Resolução CD/ANPD nº 2/2022, art. 11), desde que não caia em exceção por alto risco |
| Sistema interno | 🟡 Serve | Titulares são funcionários; canal é o RH ou o encarregado |

## Quando é bom

- **Canal público** no rodapé, na política e na área da conta, com nome do encarregado e e-mail ou formulário.
- **Autoatendimento** para acesso, correção, exportação e exclusão (rotas da skill `security`).
- **Fila com prazo** e responsável.
- **Verificação de identidade** antes de entregar ou apagar dado.

## Quando é ruim

- **E-mail genérico sem dono**, que ninguém lê.
- **Exigir ligação ou carta** para exercer um direito.
- **Entregar dado sem verificar** quem pede: o pedido vira vazamento.
- **Apagar de tudo** o que a lei manda guardar, como nota fiscal (LGPD, art. 16, I).
- **Nome do encarregado só no contrato**, sem aparecer publicamente (art. 41, § 1).

## Como começar

**1. Decida o canal e o encarregado.** Se a empresa indicar encarregado, divulgue identidade e contato em destaque no site (art. 41, § 1; o regulamento de 2024, art. 8, trata da divulgação). Se estiver dispensada como agente de pequeno porte, mantenha o canal com o titular. Dispensa e exceções são análise do advogado.

**2. Crie o canal.** `privacidade@seudominio.com.br` e um formulário, com resposta automática confirmando o recebimento e o protocolo.

**3. Fila de pedidos.**

```sql
CREATE TYPE subject_request_kind AS ENUM ('confirmation', 'access', 'correction', 'anonymization', 'portability', 'deletion', 'sharing_info', 'consent_revocation', 'other');
CREATE TYPE subject_request_status AS ENUM ('received', 'identity_check', 'in_progress', 'answered', 'rejected');

CREATE TABLE subject_requests (
  id uuid PRIMARY KEY,
  subject_id uuid,
  email_hash text NOT NULL,
  kind subject_request_kind NOT NULL,
  status subject_request_status NOT NULL DEFAULT 'received',
  received_at timestamptz NOT NULL DEFAULT now(),
  due_at timestamptz NOT NULL,
  answered_at timestamptz,
  answer_note text
);
```

`due_at` nasce com `received_at` mais 15 dias para acesso e confirmação (art. 19, II). Para os demais direitos, a ANPD ainda prepara regulamento (a agenda 2025-2026 lista o projeto de direitos dos titulares em andamento, conferida em 2026-11-25); até lá, adote prazo interno igual e confirme com o advogado.

**4. Responder.** Exportação e exclusão automatizadas estão em [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md); apagar e anonimizar no banco, em [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md).

**5. Alerta de prazo.**

```sql
SELECT id, kind, due_at
FROM subject_requests
WHERE status NOT IN ('answered', 'rejected')
  AND due_at < now() + interval '3 days'
ORDER BY due_at;
```

**6. Modelo de bloco no rodapé e na política** (estrutura): "Encarregado: nome, e-mail, formulário. Para exercer seus direitos de acesso, correção, exclusão e demais previstos na LGPD, fale com o canal acima. Respondemos em até X dias." O texto e o prazo vêm do advogado.

**7. Registre o pedido e a resposta** sem copiar o dado exportado para a fila; guarde o tipo, as datas e quem respondeu.

## Combina com / alternativas

- Rotas, incidente e criança: [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md).
- Apagar, anonimizar e registrar acesso: [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md).
- E-mail de confirmação e de resposta: skill `integrations`.
- Tela de pedidos na conta: skill `design-systems`.
- Alternativa: encarregado terceirizado (serviço de DPO); a empresa continua responsável pela conformidade, não o encarregado.

## Decisão rápida

- **Use se:** o produto guarda dado de qualquer pessoa.
- **Evite se:** o plano é só ter um e-mail e nunca olhar; o prazo corre mesmo assim.
