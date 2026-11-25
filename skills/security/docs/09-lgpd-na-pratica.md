# LGPD na prática

> Transforme o que a lei pede em telas, rotas, tabelas e rotinas do sistema: consentimento registrado, exportar e apagar dados, cookies, registro de acesso e plano para incidente.

| | |
|---|---|
| **Referência** | Lei 13.709/2018, LGPD, arts. 8, 11, 14, 16, 18, 19, 37, 39, 41, 46 e 48 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm; texto conferido na versão compilada da Câmara dos Deputados, pois o Planalto não respondeu); Resolução CD/ANPD nº 15/2024, comunicação de incidente de segurança; guias da ANPD (gov.br/anpd), entre eles o guia orientativo sobre cookies |
| **Categoria** | Segurança |
| **Tipo** | Prática de adequação do sistema à LGPD |
| **Vale para** | Qualquer sistema que trate dado de pessoa no Brasil; exemplos em TypeScript (Hono) e SQL (PostgreSQL) |
| **Verificado em** | 2026-11-24 |

## O que é

A LGPD define o que se pode fazer com dado pessoal e o que a pessoa (o **titular**) pode exigir. Este doc cobre só o lado do **sistema**: o que construir para que a empresa consiga cumprir a lei.

O lado do banco (minimizar, criptografar, anonimizar, retenção por tabela) está em [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md). Não é repetido aqui.

Este doc **não é orientação jurídica**. Exigem advogado: a **base legal** de cada tratamento (art. 7 e 11), o texto da política de privacidade e dos termos, o **encarregado** (DPO, art. 41) e os contratos com fornecedores. O código só registra e executa o que o jurídico decidiu.

Termos: **controlador** decide o tratamento (a clínica); **operador** trata em nome dele (o provedor de e-mail, a nuvem); **dado sensível** inclui saúde (art. 11).

## Por que usar

- **Prova:** pelo art. 8, § 2, cabe ao controlador provar o consentimento. Sem registro, não há prova.
- **Atender o titular sem improviso:** pedido de acesso tem prazo (art. 19); sem rota pronta, vira trabalho manual em cima da hora.
- **Incidente:** com registro de acesso e lista de fornecedores, a resposta é rápida e o dano, menor.

## Quando usar

- Antes do primeiro usuário real: consentimento, política e rotas do titular.
- Ao adicionar analytics, pixel, chat ou fornecedor novo, ou ao tratar dado de criança ou de saúde.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Basta política, banner de cookies e formulário de contato |
| MVP de SaaS | ✅ Ótimo | Consentimento, exportar e apagar são baratos no início e caros depois |
| SaaS em crescimento | ✅ Ótimo | Clientes grandes pedem lista de subprocessadores e registro de acesso |
| Sistema interno/corporativo | ✅ Ótimo | Dado de funcionário e cliente também é pessoal |
| API/integração | 🟡 Serve | O controlador é quem consome; a API precisa permitir exportar e apagar |
| App mobile | ✅ Ótimo | SDKs de terceiros coletam dado; a loja exige declarar |
| Sistema que não trata dado de pessoa natural | ❌ Evite | A LGPD não se aplica a dado anonimizado nem de empresa; não crie burocracia à toa |

## Quando é bom

- **Uma finalidade por consentimento:** o art. 8, § 4, diz que autorização genérica é nula.
- **Revogar com facilidade:** o art. 8, § 5, exige procedimento gratuito e facilitado.
- **Exportar e apagar como funções testadas:** uma por tabela com dado de pessoa, e um teste que falha se criarem tabela nova sem elas.

## Quando é ruim

- **Caixa de aceite marcada de fábrica ou "ao continuar você aceita":** não demonstra manifestação de vontade (art. 8).
- **Consentimento para tudo:** contrato e obrigação legal são outras bases; o jurídico decide.
- **Apagar de verdade o que a lei manda guardar:** o art. 16, I, permite conservar por obrigação legal (prontuário, nota fiscal). Anonimize o resto.

## Como começar

**1. Consentimento registrado.** Cada aceite é uma linha que nunca é editada; revogar é uma nova linha.

```sql
CREATE TABLE consents (
  id uuid PRIMARY KEY,
  subject_id uuid NOT NULL REFERENCES patients (id),
  purpose text NOT NULL,
  text_version text NOT NULL,
  granted boolean NOT NULL,
  channel text NOT NULL,
  ip_hash text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX consents_subject_purpose_idx ON consents (subject_id, purpose, created_at DESC);
```

`purpose` é a finalidade (`lembrete_whatsapp`, `marketing_email`). `text_version` aponta para a versão exata do texto mostrado (guarde cada versão em arquivo ou tabela). O consentimento vigente é a linha mais recente de cada finalidade.

```ts
export async function currentConsent(subjectId: string, purpose: string) {
  const row = await db.queryOne(
    "SELECT granted FROM consents WHERE subject_id = $1 AND purpose = $2 ORDER BY created_at DESC LIMIT 1",
    [subjectId, purpose],
  );
  return row?.granted === true;
}
```

Antes de enviar lembrete por WhatsApp, chame `currentConsent`. Sem linha, a resposta é "não".

**2. Política de privacidade e termos.** Publique em URL fixa, com data e versão, linkada no rodapé e no cadastro. O texto vem do jurídico; o sistema só o exibe e registra qual versão a pessoa viu.

**3. Direitos do titular (art. 18) viram rotas.** Acesso, correção, eliminação e portabilidade têm tela na área da conta (botões "Baixar meus dados", "Corrigir" e "Excluir minha conta").

```ts
app.get("/me/export", requireAuth, async (c) => {
  const userId = c.get("userId");
  const data = await exportSubjectData(userId);
  await db.exec("INSERT INTO subject_requests (id, subject_id, kind) VALUES ($1, $2, 'export')", [newId(), userId]);
  c.header("Content-Disposition", 'attachment; filename="meus-dados.json"');
  return c.json(data);
});

app.post("/me/deletion", requireAuth, requireRecentLogin, async (c) => {
  const userId = c.get("userId");
  await db.exec("INSERT INTO subject_requests (id, subject_id, kind) VALUES ($1, $2, 'deletion')", [newId(), userId]);
  await queue.enqueue("erase-subject", { subjectId: userId });
  return c.body(null, 202);
});
```

`exportSubjectData` percorre todas as tabelas do titular e devolve JSON em formato aberto (portabilidade, art. 18, V). `erase-subject` apaga ou anonimiza, mantém o que a lei manda guardar (art. 16, I) e avisa os operadores (art. 18, § 6). Peça login recente para excluir e registre cada pedido em `subject_requests`.

Prazos: o art. 19 fixa resposta imediata em formato simplificado ou declaração completa em até 15 dias para confirmação e acesso. Para os demais direitos, o prazo vem de regulamento da ANPD; confirme com o jurídico.

**4. Cookies e analytics.** Cookie estritamente necessário (sessão, CSRF) dispensa banner de aceite. Os demais (analytics, anúncios, pixels) só carregam depois do aceite, e o banner tem "Recusar" tão visível quanto "Aceitar". O guia orientativo da ANPD sobre cookies detalha categorias e boas práticas.

```ts
export function loadAnalytics(consent: { analytics: boolean }) {
  if (!consent.analytics) return;
  const s = document.createElement("script");
  s.src = "https://analytics.example.com/script.js";
  s.defer = true;
  document.head.appendChild(s);
}
```

Prefira analytics sem cookie e sem identificar a pessoa (métricas agregadas, auto-hospedado). Menos coleta, menos banner e menos risco.

**5. Registro de acesso a dado sensível.** Toda leitura de prontuário grava quem, quando e qual paciente, sem o conteúdo. A tabela `sensitive_access_log` está em [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md). Aqui, a regra é ligar na rota:

```ts
app.get("/patients/:id/records", requireAuth, requirePermission("record:read"), async (c) => {
  await logSensitiveAccess(c.get("userId"), c.req.param("id"), "read_records");
  return c.json(await loadRecords(c.req.param("id")));
});
```

Isso sustenta o dever de segurança (art. 46) e o registro das operações (art. 37).

**6. Incidente de segurança (art. 48).** O controlador comunica a ANPD e o titular quando o incidente puder causar risco ou dano relevante. O § 1 lista o conteúdo mínimo: natureza dos dados, titulares envolvidos, medidas de segurança usadas, riscos, motivos de demora e medidas de mitigação. O art. 48 fala em "prazo razoável"; a Resolução CD/ANPD nº 15/2024 fixou **3 dias úteis** (informações podem ser complementadas em até 20 dias úteis, segundo a página da ANPD sobre o tema).

Prepare antes: roteiro de uma página (quem decide, quem fala com a ANPD, modelo de comunicado), logs retidos e a lista do passo 8. Medida técnica que torna o dado ininteligível (criptografia) pesa na avaliação de gravidade (art. 48, § 3).

**7. Retenção.** Tabela de prazo por tipo de dado, definida com o jurídico (art. 16), e job agendado que apaga ou anonimiza. Detalhe SQL em [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md).

**8. Operadores e subprocessadores.** Mantenha `docs/subprocessadores.md` no repositório: nome, o que recebe, finalidade, país e link do contrato. Atualize no mesmo PR que adiciona a integração. O operador trata conforme instruções do controlador (art. 39). Contrato e transferência para fora do Brasil (art. 33) são com advogado.

**9. Criança e adolescente (art. 14).** Tratar dado de criança exige consentimento específico e em destaque de um dos pais ou do responsável (§ 1), com esforços razoáveis para verificar quem consentiu (§ 5). Se o sistema pode ter menores (paciente pediátrico), o cadastro é feito pelo responsável, e o campo "responsável legal" é obrigatório quando a data de nascimento indica criança (a definição de criança e adolescente vem do ECA; confirme com o jurídico). Para adolescente, o jurídico define a base legal. Mantenha pública a informação sobre dados coletados e como exercer os direitos (§ 2).
**Em cada stack.** A lógica é a mesma; muda onde plugar.

| Stack | Onde ligar |
|---|---|
| Node / Next.js | Route Handlers ou Hono; fila para apagar |
| ASP.NET Core | Minimal API com `[Authorize]`; `IHostedService` ou Hangfire para o job |
| Django | View com `login_required`; Celery ou comando agendado |
| Laravel / Spring Boot | Controller com auth; `Queue` e `Schedule` / `@Scheduled` |

## Combina com / alternativas

- [01-escolha-do-login.md](01-escolha-do-login.md) e [03-recuperacao-e-2fa.md](03-recuperacao-e-2fa.md): confirmar identidade antes de exportar ou apagar.
- [04-papeis-e-permissoes.md](04-papeis-e-permissoes.md) e [05-owasp-no-codigo.md](05-owasp-no-codigo.md): quem lê dado sensível e como evitar vazamento.
- [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md) e [../../data/docs/07-auditoria-historico-soft-delete.md](../../data/docs/07-auditoria-historico-soft-delete.md): lado do banco.
- [../../infra/docs/12-seguranca-base.md](../../infra/docs/12-seguranca-base.md) e [../../infra/docs/09-segredos-e-configuracao.md](../../infra/docs/09-segredos-e-configuracao.md): rede, TLS, segredos.
- Alternativa a guardar o dado: delegar a provedor especializado, que vira operador na lista do passo 8.

## Decisão rápida

- **Use se:** o sistema guarda dado de pessoa no Brasil, principalmente saúde, criança ou contato para marketing.
- **Evite se:** a intenção é trocar o advogado por este doc; base legal, encarregado, termos e contratos são decisões jurídicas.
