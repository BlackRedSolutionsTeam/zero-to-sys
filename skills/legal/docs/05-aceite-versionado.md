# Aceite versionado

> Guarde quem aceitou qual versão de qual documento, quando e por qual canal, em linhas que nunca são editadas.

| | |
|---|---|
| **Referência** | LGPD, art. 8, caput e §§ 1 a 5 (consentimento por escrito ou outro meio, cláusula destacada, ônus da prova do controlador, finalidade determinada, revogação) e art. 37 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); CDC, art. 46; Decreto 7.962/2013, art. 4 |
| **Categoria** | Jurídico |
| **Tipo** | Prática de modelagem e registro de aceite |
| **Vale para** | Qualquer sistema com cadastro, termos, política ou consentimento; exemplos em SQL (PostgreSQL) e TypeScript |
| **Verificado em** | 2026-11-25 |

> Não substitui advogado. O que vale como prova de aceite em juízo e quanto tempo guardar são decisões jurídicas.

## O que é

Aceite versionado é o registro de que **uma pessoa (ou conta) aceitou uma versão específica de um documento em um momento**. Cabe ao controlador provar o consentimento (LGPD, art. 8, § 2). A [skill `security`](../../security/docs/09-lgpd-na-pratica.md) mostra a tabela de consentimentos por finalidade; aqui estão os documentos (termos, política, contrato) e o fluxo de nova versão.

## Por que usar

- **Prova:** "aceitou os termos v3 em 12/03 pelo cadastro web".
- **Mudança de termos sem dor:** só quem não aceitou a versão nova é chamado de volta.
- **Resposta a cliente B2B e a auditoria.**

## Quando usar

- Cadastro e checkout com termos e política.
- Toda mudança relevante de termos, política ou contrato.
- Consentimentos específicos (marketing, compartilhamento), que seguem a tabela da skill `security`.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS B2C | ✅ Ótimo | Muitos usuários, mudança de termos frequente |
| SaaS B2B | ✅ Ótimo | Aceite pela conta, por quem tem poder de aceitar |
| Loja online | ✅ Ótimo | Aceite no checkout, guardado com o pedido |
| App mobile | ✅ Ótimo | Versão do app e da tela junto do registro |
| Site de conteúdo | 🟡 Serve | Só cookies e newsletter |
| Sistema interno | 🟡 Serve | Aceite da política de uso no primeiro acesso |

## Quando é bom

- **Tabela só de inserção:** aceitar é uma linha; retirar é outra.
- **Versão com conteúdo guardado** (hash do texto), não só número.
- **Bloqueio gentil:** após nova versão, a pessoa vê o texto e aceita antes de continuar.
- **Quem aceitou** claro: usuário e, em B2B, a conta e o cargo.

## Quando é ruim

- **Guardar só `accepted = true`** na tabela de usuários: perde versão e data.
- **Editar o texto sem mudar a versão.**
- **Caixa pré-marcada** ou aceite embutido em "ao continuar".
- **IP e agente do navegador em claro** sem necessidade: são dados pessoais; prefira hash ou tempo limitado de guarda.
- **Forçar novo aceite em mudança de vírgula:** cansa e perde valor; reserve para mudança relevante.

## Como começar

**1. Documentos e versões.**

```sql
CREATE TABLE legal_documents (
  id uuid PRIMARY KEY,
  kind text NOT NULL,
  version text NOT NULL,
  content_hash text NOT NULL,
  published_at timestamptz NOT NULL,
  requires_reacceptance boolean NOT NULL DEFAULT false,
  UNIQUE (kind, version)
);

CREATE TABLE legal_acceptances (
  id uuid PRIMARY KEY,
  user_id uuid NOT NULL,
  account_id uuid,
  document_id uuid NOT NULL REFERENCES legal_documents (id),
  accepted_at timestamptz NOT NULL DEFAULT now(),
  channel text NOT NULL,
  ip_hash text,
  user_agent text
);

CREATE INDEX legal_acceptances_user_idx ON legal_acceptances (user_id, document_id);
```

`kind` pode ser `terms`, `privacy`, `dpa`. `content_hash` é o hash do texto publicado, calculado no deploy.

**2. Publicar versão.** O texto fica no repositório com a versão no nome do arquivo; o deploy insere a linha.

```
legal/terms/2026-11-25.md
legal/privacy/2026-11-25.md
```

```ts
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";

export async function publishDocument(kind: string, version: string, path: string, requiresReacceptance: boolean) {
  const content = await readFile(path, "utf8");
  const contentHash = createHash("sha256").update(content).digest("hex");
  await db.exec(
    "INSERT INTO legal_documents (id, kind, version, content_hash, published_at, requires_reacceptance) VALUES ($1, $2, $3, $4, now(), $5) ON CONFLICT (kind, version) DO NOTHING",
    [newId(), kind, version, contentHash, requiresReacceptance],
  );
}
```

**3. Registrar aceite** com a versão que a pessoa de fato viu.

```ts
app.post("/legal/accept", requireAuth, async (c) => {
  const { documentId } = await c.req.json<{ documentId: string }>();
  await db.exec(
    "INSERT INTO legal_acceptances (id, user_id, account_id, document_id, channel, ip_hash, user_agent) VALUES ($1, $2, $3, $4, 'web', $5, $6)",
    [newId(), c.get("userId"), c.get("accountId"), documentId, hashIp(c.req.header("x-forwarded-for")), c.req.header("user-agent")],
  );
  return c.body(null, 201);
});
```

**4. Quem precisa aceitar de novo.**

```sql
SELECT d.kind, d.version
FROM legal_documents d
WHERE d.requires_reacceptance
  AND d.published_at = (SELECT max(published_at) FROM legal_documents WHERE kind = d.kind)
  AND NOT EXISTS (
    SELECT 1 FROM legal_acceptances a WHERE a.document_id = d.id AND a.user_id = $1
  );
```

Se a consulta devolver linhas, o middleware leva a pessoa à tela de aceite antes do restante.

**5. Fluxo de nova versão:**

1. Advogado aprova o texto.
2. Texto entra no repositório com data na versão.
3. Deploy publica o documento e decide `requires_reacceptance`.
4. E-mail avisa com antecedência, quando a mudança piora a posição do usuário.
5. A tela de aceite mostra o que mudou.
6. Quem não aceitar: política do contrato (doc [03](03-termos-de-uso-e-contrato-de-saas.md)).

**6. Retirada de consentimento** é nova linha na tabela de consentimentos da skill `security`, não apagar o aceite.

**7. Retenção:** o aceite é prova e costuma ser guardado enquanto a relação durar mais o prazo de eventual disputa; o prazo é decisão do advogado e entra no mapa de dados (doc [02](02-politica-de-privacidade-e-o-mapa-de-dados.md)).

## Combina com / alternativas

- Consentimento por finalidade (marketing, WhatsApp): [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md).
- Histórico e auditoria: [../../data/docs/07-auditoria-historico-soft-delete.md](../../data/docs/07-auditoria-historico-soft-delete.md).
- Tela de aceite e rolagem do texto: skill `design-systems`.
- Regras de plano: skill `product`.
- Cookies: [04](04-cookies-aviso-categorias-e-consentimento.md).

## Decisão rápida

- **Use se:** o produto tem termos, política ou contrato que mudam com o tempo.
- **Evite se:** o produto não tem cadastro nem consentimento; a tabela não resolve falta de documento.
