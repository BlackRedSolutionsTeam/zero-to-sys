# Contrato de operador com clientes (B2B) e suboperadores

> Quando o seu SaaS guarda dado de pessoas em nome do cliente, você é operador: tenha um contrato de tratamento de dados e uma lista pública de suboperadores.

| | |
|---|---|
| **Referência** | LGPD, arts. 5 (controlador e operador), 33 (transferência internacional), 37, 39, 42 e 46 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); Resolução CD/ANPD nº 19/2024, transferência internacional e cláusulas-padrão contratuais (prazo de adequação encerrado em 23/08/2025); Guia de Agentes de Tratamento da ANPD (gov.br/anpd) |
| **Categoria** | Jurídico |
| **Tipo** | Prática de contrato de operador e lista de suboperadores |
| **Vale para** | SaaS B2B que trata dado de usuários, clientes ou pacientes do cliente |
| **Verificado em** | 2026-11-25 |

> Não substitui advogado. Classificar quem é controlador e quem é operador, e redigir o contrato, é trabalho jurídico. A transferência para fora do Brasil foi conferida em resumos de escritórios de advocacia; confirme no texto da resolução.

## O que é

- **Controlador:** quem decide como e para que o dado é tratado. Em um SaaS B2B, em geral o cliente.
- **Operador:** quem trata em nome do controlador e segundo as instruções dele (art. 39). Em geral o seu SaaS.
- **Suboperador:** o fornecedor que o operador contrata para tratar o dado do cliente (nuvem, e-mail, suporte, monitoramento).
- **Contrato de operador (DPA, acordo de tratamento de dados):** documento que fixa objeto, finalidade, instruções, segurança, suboperadores, devolução e apagamento, e incidente.

Um mesmo SaaS pode ser **operador** dos dados que os clientes põem nele e **controlador** dos dados dos próprios clientes (cobrança, login do administrador).

## Por que usar

- **Clareza de responsabilidade:** controlador e operador respondem por dano (art. 42); o contrato divide tarefas, a lei continua valendo.
- **Compra de empresa grande** depende dele.
- **Resposta ao titular e a incidente** ficam combinadas antes do problema.

## Quando usar

- Vende para empresa e armazena dado de pessoas ligadas a ela (pacientes, funcionários, clientes finais).
- Usa fornecedores que recebem esse dado.
- Os servidores ou fornecedores estão fora do Brasil.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS B2B multiempresa | ✅ Ótimo | Todo cliente é controlador do dado dele |
| API/plataforma usada por outras empresas | ✅ Ótimo | A API recebe dado de terceiros |
| SaaS para clínica ou saúde | ✅ Ótimo | Dado sensível, cliente exigente (ver [08](08-quando-procurar-advogado.md)) |
| SaaS B2C | 🟡 Serve | Você é o controlador; precisa de contratos só com fornecedores |
| Site institucional | ❌ Evite | Sem dado de terceiros em nome de cliente |

## Quando é bom

- **Contrato anexo aos termos**, aceito no cadastro da conta empresa (doc [05](05-aceite-versionado.md)).
- **Lista de suboperadores pública**, com aviso de mudança.
- **Cumprimento real:** o produto exporta, apaga e registra acesso como o contrato diz.

## Quando é ruim

- **Aceitar o contrato do cliente sem ler** e prometer o que o sistema não faz (prazo de resposta, região de dados, auditoria).
- **Lista de suboperadores desatualizada.**
- **Cláusulas copiadas de modelo estrangeiro** sem adaptar à LGPD.
- **Transferência para fora do Brasil sem mecanismo previsto no art. 33.**

## Como começar

**1. Lista de suboperadores** (arquivo no repositório e página pública).

| Fornecedor | O que recebe | Finalidade | País | Contrato |
|---|---|---|---|---|
| Provedor de nuvem | Todo o dado do cliente | Hospedagem | Brasil | Link |
| Provedor de e-mail | E-mail e nome do usuário final | Envio de notificações | País do provedor | Link |
| Ferramenta de erros | Dados técnicos, sem dado pessoal | Diagnóstico | País do provedor | Link |

**2. Modelo de estrutura do contrato de operador** (texto do advogado):

1. Partes e papéis: quem é controlador e quem é operador.
2. Objeto, duração, natureza, finalidade, tipos de dado e de titulares.
3. Instruções do controlador e limites de uso do dado (art. 39).
4. Confidencialidade da equipe.
5. Medidas de segurança (art. 46), em anexo técnico.
6. Suboperadores: lista, aviso de mudança, direito de objetar e mesmas obrigações repassadas.
7. Apoio ao controlador nos pedidos dos titulares (doc [06](06-direitos-do-titular-e-canal-do-encarregado.md)).
8. Incidente de segurança: prazo para avisar o controlador e conteúdo do aviso.
9. Transferência internacional, quando houver (art. 33; mecanismos e cláusulas-padrão da ANPD).
10. Devolução ou eliminação ao fim do contrato, com prazo.
11. Auditoria e evidências.
12. Responsabilidade e foro.

**3. Anexo técnico:** criptografia, backup, controle de acesso, registro, região dos dados. As respostas vêm do próprio sistema: [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md) e a skill `infra`.

**4. Transferência internacional.** O art. 33 só permite em hipóteses listadas, como país com grau de proteção adequado ou garantias como cláusulas contratuais. A Resolução CD/ANPD nº 19/2024 aprovou cláusulas-padrão contratuais, cujo texto deve ser incorporado ao contrato sem alterações; o prazo de 12 meses para adequação terminou em 23/08/2025 (conferido em resumos de escritórios em 2026-11-25). Se um suboperador está fora do Brasil, pergunte ao advogado qual mecanismo se aplica.

**5. Aviso de novo suboperador.**

```sql
CREATE TABLE subprocessors (
  id uuid PRIMARY KEY,
  name text NOT NULL,
  purpose text NOT NULL,
  data_categories text NOT NULL,
  country text NOT NULL,
  contract_url text,
  active_from date NOT NULL,
  active_until date
);

CREATE TABLE subprocessor_notices (
  id uuid PRIMARY KEY,
  subprocessor_id uuid NOT NULL REFERENCES subprocessors (id),
  announced_at timestamptz NOT NULL DEFAULT now(),
  effective_at timestamptz NOT NULL
);
```

Envie o aviso (skill `integrations`, e-mail) aos administradores das contas B2B com a antecedência do contrato.

**6. Pedido de titular que chega ao operador:** encaminhe ao controlador conforme o contrato, não responda por conta própria.

**7. Fim do contrato:** exporte, entregue, apague e emita comprovante, com prazo definido (backups expiram pela retenção).

## Combina com / alternativas

- Registro das operações e dado no banco: [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md).
- Segurança, incidente e lista de operadores: [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md).
- Multiempresa e isolamento: [../../data/docs/06-multiempresa.md](../../data/docs/06-multiempresa.md).
- Fornecedores de e-mail: skill `integrations`.
- Alternativa: anexar o contrato padrão do cliente grande, revisado pelo advogado antes de assinar.

## Decisão rápida

- **Use se:** o SaaS guarda dado de pessoas em nome de empresas clientes.
- **Evite se:** o produto só trata dado dos próprios usuários; aí o foco é política e termos.
