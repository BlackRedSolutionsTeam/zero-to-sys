# Dados pessoais e LGPD

> Guarde o mínimo de dado pessoal, proteja o sensível, não deixe vazar em log, apague no prazo e saiba exportar e apagar os dados de uma pessoa.

| | |
|---|---|
| **Referência** | Lei 13.709/2018, LGPD (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); guias da ANPD (gov.br/anpd); documentação do pgcrypto (postgresql.org/docs/current/pgcrypto.html) |
| **Categoria** | Dados |
| **Tipo** | Prática de proteção de dados no banco e na aplicação |
| **Vale para** | PostgreSQL com qualquer ORM; qualquer sistema que guarde dado de pessoa no Brasil |
| **Verificado em** | 2026-11-24 |

## O que é

Esta prática mostra como o banco e o código tratam dado pessoal. O lado jurídico não é decidido aqui: base legal, encarregado (DPO), termos de uso, política de privacidade e contratos precisam de advogado e do responsável da empresa.

Pela LGPD (art. 5º), **dado pessoal** é informação relacionada a pessoa natural identificada ou identificável: nome, CPF, e-mail, telefone, endereço, IP. **Dado pessoal sensível** é o que trata de origem racial ou étnica, convicção religiosa, opinião política, filiação sindical, saúde, vida sexual, dado genético ou biométrico. Prontuário e queixa de consulta são sensíveis. CPF é pessoal, mas não está nessa lista; mesmo assim merece cuidado extra.

## Por que usar

- **Menos dano num vazamento:** quem não tem o dado não vaza o dado.
- **Obrigação legal:** a lei pede segurança (art. 46) e registro das operações (art. 37).
- **Confiança do cliente:** clínicas e empresas pedem isso em contrato.
- **Direitos do titular** (art. 18) ficam fáceis de atender se o dado estiver organizado.

## Quando usar

- Qualquer tabela com nome, CPF, e-mail, telefone ou endereço.
- Todo dado de saúde, biometria ou outro sensível.
- Antes de ligar log, analytics ou ferramenta de erro, que também recebem dado.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Costuma ter só formulário de contato e newsletter |
| MVP de SaaS | ✅ Ótimo | Mais barato começar certo do que corrigir com clientes |
| SaaS em crescimento | ✅ Ótimo | Clientes grandes pedem evidência de proteção |
| Sistema interno/corporativo | ✅ Ótimo | Dados de funcionários e clientes, com acesso por papel |
| API/integração | ✅ Ótimo | Dado trafega e vai para log de terceiros |
| App mobile com backend | ✅ Ótimo | Cadastro de pessoas e dados do aparelho |
| Pedir CPF, data de nascimento e endereço "por garantia" | ❌ Evite | Sem finalidade, é risco sem benefício (art. 6º, III: mínimo necessário) |

## Quando é bom

- **Minimização:** só coletar o que a funcionalidade usa.
- **Separação:** dado sensível em tabela própria, com acesso restrito.
- **Prazo definido:** o dado nasce com data para sair.
- **Rastro de acesso:** dá para responder "quem viu o prontuário?".

## Quando é ruim

- **Log com dado pessoal:** CPF em log de erro vai para ferramentas de terceiros e fica anos.
- **Criptografia só no provedor:** protege o disco roubado, não o acesso com credencial válida.
- **Chave junto do dado:** criptografar e deixar a chave na mesma tabela ou repositório não protege.
- **Cópia de produção em desenvolvimento:** use dados falsos (ver seeds).
- **Esquecer os backups:** eles também contêm dado pessoal.

## Como começar

**1. Minimize.** Para cada campo, escreva a finalidade. Sem finalidade, não crie a coluna.

**2. Separe o sensível.**

```sql
CREATE TABLE patients (
  id uuid PRIMARY KEY,
  company_id uuid NOT NULL,
  full_name text NOT NULL,
  cpf_encrypted bytea NOT NULL,
  cpf_hash text NOT NULL,
  anonymized_at timestamptz
);

CREATE TABLE patient_health_records (
  id uuid PRIMARY KEY,
  patient_id uuid NOT NULL REFERENCES patients (id),
  notes_encrypted bytea NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
```

`cpf_hash` (hash com segredo, como HMAC) permite buscar por CPF sem descriptografar.

**3. Criptografia.** A do provedor (disco e backup criptografados em repouso) é o mínimo e já vem em banco gerenciado. A de coluna protege campos específicos. Duas formas:

- **Na aplicação (preferida):** a chave fica no gerenciador de segredos, fora do banco; o banco só vê bytes.
- **pgcrypto:** `pgp_sym_encrypt` e `pgp_sym_decrypt`. A própria documentação avisa que a chave e o texto passam pelo servidor e podem aparecer em log de consultas, então não é protegida contra quem administra o banco.

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
INSERT INTO patients (id, company_id, full_name, cpf_encrypted, cpf_hash)
VALUES ($1, $2, $3, pgp_sym_encrypt($4, $5), $6);
```

Coluna criptografada não permite busca nem ordenação: use o hash ou outro campo.

**4. Não logue dado pessoal.** Registre ids, nunca CPF, e-mail ou corpo da requisição. Configure o logger e a ferramenta de erros para ocultar campos como `cpf`, `email`, `password`.

**5. Retenção e exclusão.** Defina o prazo por tipo de dado (com o jurídico, pois pode haver obrigação legal de guardar; art. 16, I). Crie rotina agendada que apaga ou anonimiza.

```sql
UPDATE patients
SET full_name = 'Anonimizado', cpf_encrypted = '\x', cpf_hash = id::text, anonymized_at = now()
WHERE id = $1;
```

**6. Atender o titular (art. 18).** A pessoa pode pedir confirmação do tratamento, acesso, correção, anonimização, bloqueio ou eliminação, portabilidade, entre outros. Tenha duas funções prontas: exportar tudo de uma pessoa (JSON ou CSV) e apagar ou anonimizar tudo dela, passando por todas as tabelas. Registre o pedido e a data.

**7. Registro de acesso.**

```sql
CREATE TABLE sensitive_access_log (
  id uuid PRIMARY KEY,
  user_id uuid NOT NULL,
  patient_id uuid NOT NULL,
  action text NOT NULL,
  accessed_at timestamptz NOT NULL DEFAULT now()
);
```

Grave sem o conteúdo do dado. Ver também [07-auditoria-historico-soft-delete.md](07-auditoria-historico-soft-delete.md).

**8. Backups.** Defina quanto tempo ficam guardados, criptografe e lembre que apagar do banco não apaga das cópias antigas; elas expiram pela retenção.

## Combina com / alternativas

- [01-modelagem-de-entidades.md](01-modelagem-de-entidades.md) e [02-nomes-e-tipos.md](02-nomes-e-tipos.md): decida o que existe antes de coletar.
- [05-seeds-e-dados-de-teste.md](05-seeds-e-dados-de-teste.md): dados falsos fora de produção.
- [06-multiempresa.md](06-multiempresa.md): um cliente nunca vê dado de outro.
- Backup: `skills/infra/docs/11-backup-e-recuperacao.md`. Login e permissões: skill `security`.
- Alternativa a guardar o dado: não guardar, ou delegar a um provedor especializado (pagamento, prontuário).

## Decisão rápida

- **Use se:** o sistema guarda dado de pessoa, principalmente CPF ou saúde.
- **Evite se:** a ideia é usar este doc no lugar de orientação jurídica; base legal, DPO e termos cabem ao jurídico da empresa.
