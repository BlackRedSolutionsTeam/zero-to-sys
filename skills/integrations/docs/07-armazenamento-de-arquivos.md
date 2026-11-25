# Armazenamento de arquivos

> Arquivo vai para um object storage por URL pré-assinada, e o banco guarda só os metadados (tabela `files`), nunca o arquivo.

| | |
|---|---|
| **Referência** | Documentação oficial do Amazon S3 (presigned URLs), Cloudflare R2, Supabase Storage e Backblaze B2; páginas de preço oficiais conferidas em 2026-11-24; OWASP File Upload Cheat Sheet |
| **Categoria** | Integrações |
| **Tipo** | Prática de armazenamento de arquivos |
| **Vale para** | Node, Python, .NET, Java, Laravel, Go com qualquer storage compatível com S3 |
| **Verificado em** | 2026-11-24 |

## O que é

Object storage é um serviço que guarda arquivos (objetos) em "baldes" (buckets), cada um com uma chave (o caminho). Você grava e lê por HTTP. Não é um disco: não tem pastas de verdade nem edição parcial.

URL pré-assinada é um link temporário, assinado pelo seu servidor, que dá permissão de enviar ou baixar um único arquivo. O arquivo vai direto do navegador para o storage, sem passar pela sua API.

## Por que usar

- **Servidor sem estado:** o disco de servidores em PaaS e containers é efêmero; o arquivo some no próximo deploy.
- **API leve:** upload de 50 MB não ocupa memória nem conexão da sua API.
- **Escala e durabilidade:** o provedor replica e cuida do espaço.
- **Banco enxuto:** arquivo no banco incha o backup e deixa tudo lento.

## Quando usar

- Foto de perfil, exames e laudos em PDF, anexos, comprovantes, exportações geradas.
- Qualquer arquivo enviado por usuário.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Imagens costumam ficar no CDN do host; storage só se houver upload |
| MVP de SaaS | ✅ Ótimo | Anexos e avatar desde o início, plano grátis cobre |
| SaaS em crescimento | ✅ Ótimo | Ciclo de vida e CDN reduzem custo |
| Sistema interno/corporativo | ✅ Ótimo | Documentos com retenção e auditoria |
| API/integração | 🟡 Serve | Só se a API recebe ou devolve arquivos |
| App mobile | ✅ Ótimo | Upload direto do celular economiza dados e servidor |
| Servidor com disco local como "storage" | ❌ Evite | Perde arquivos no deploy e não escala em várias instâncias |

## Quando é bom

- **Upload direto por URL pré-assinada:** a API só assina e registra.
- **Chave sem dado pessoal:** `clinics/{clinicId}/patients/{patientId}/{uuid}.pdf`; nunca o nome original do usuário na chave.
- **Bucket privado por padrão**, com download por URL pré-assinada de validade curta.
- **CDN na frente** para arquivo público (imagens do site): cache perto do usuário e menos leitura no storage.
- **Ciclo de vida:** regra que apaga ou move para classe mais barata (ex.: temporários após 1 dia, exportações após 7).
- **Versionamento e backup:** ative versionamento do bucket ou replique para outro provedor; o backup do banco não cobre os arquivos.

## Quando é ruim

- **Arquivo em coluna `bytea`/`blob`** ou em disco do servidor.
- **Bucket público** com documento de paciente.
- **URL pré-assinada longa** (dias): vira link vazado permanente.
- **Confiar no nome e no tipo informados pelo cliente:** valide no servidor (veja [segurança de upload](../../security/docs/07-upload-de-arquivos.md)).
- **Esquecer o egress:** saída de dados é cobrada em vários provedores.

## Como começar

Comparação (preços conferidos nas páginas oficiais em 2026-11-24; confirme antes de contratar):

| Serviço | Plano grátis | Egress (saída) |
|---|---|---|
| Cloudflare R2 | 10 GB/mês, 1 milhão de operações de escrita (Classe A), 10 milhões de leitura (Classe B) | Grátis para a internet via API S3, Workers e `r2.dev` |
| Amazon S3 | Créditos de até US$ 200 para contas novas (6 meses no plano grátis) | Cobrado; veja a página de preços |
| Supabase Storage | 1 GB, arquivo de até 50 MB no plano grátis | Veja a página de preços |
| Backblaze B2 | 10 GB sempre grátis | Grátis até 3x o armazenado por mês; excedente US$ 0,01/GB |

R2, B2 e Supabase falam o protocolo S3, então o mesmo cliente serve para todos; muda só o endpoint.

Tabela de metadados (exemplo: clínica):

```sql
create table files (
  id uuid primary key,
  clinic_id uuid not null references clinics(id),
  owner_type text not null,
  owner_id uuid not null,
  storage_key text not null unique,
  original_name text not null,
  content_type text not null,
  size_bytes bigint,
  status text not null default 'pending',
  created_at timestamptz not null default now()
);
```

Fluxo: 1) cliente pede `POST /files` com nome, tipo e tamanho; 2) API valida, cria a linha `pending` e devolve a URL de upload; 3) cliente faz `PUT` no storage; 4) cliente avisa `POST /files/{id}/complete`, a API confere o objeto e marca `ready`. Um job limpa `pending` antigos.

```ts
import { S3Client, PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({
  region: "auto",
  endpoint: process.env.S3_ENDPOINT,
  credentials: {
    accessKeyId: process.env.S3_KEY_ID!,
    secretAccessKey: process.env.S3_SECRET!,
  },
});

export function uploadUrl(key: string, contentType: string) {
  const cmd = new PutObjectCommand({ Bucket: process.env.S3_BUCKET, Key: key, ContentType: contentType });
  return getSignedUrl(s3, cmd, { expiresIn: 300 });
}

export function downloadUrl(key: string) {
  const cmd = new GetObjectCommand({ Bucket: process.env.S3_BUCKET, Key: key });
  return getSignedUrl(s3, cmd, { expiresIn: 60 });
}
```

Imagens: gere versões menores (miniatura, tamanho de tela) em um job em fila ([05](./05-filas-e-jobs.md)), não na requisição.

| Stack | Cliente S3 | Redimensionar imagem |
|---|---|---|
| Node | `@aws-sdk/client-s3` | sharp |
| Python | boto3 | Pillow |
| .NET | AWSSDK.S3 | ImageSharp (Apache 2.0 só em projeto open source ou com receita abaixo de US$ 1 milhão por ano; fora disso, licença comercial paga da Six Labors, conferido em 2026-11-25) |
| Java | AWS SDK for Java v2 | Thumbnailator ou ImageIO |
| Laravel | Flysystem S3 (`Storage::temporaryUrl`) | Intervention Image |
| Go | aws-sdk-go-v2 | disintegration/imaging |

## Combina com / alternativas

- [Filas e jobs](./05-filas-e-jobs.md) para miniaturas e varredura de vírus.
- [Importar e exportar planilhas](./09-importar-e-exportar-planilhas.md): o arquivo enviado e o gerado ficam aqui.
- [Segurança de upload](../../security/docs/07-upload-de-arquivos.md): tipo real, tamanho, vírus.
- [Dados pessoais e LGPD](../../data/docs/10-dados-pessoais-e-lgpd.md): retenção e exclusão de documentos de pacientes.
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md) para o passo de "complete".
- Alternativa: Supabase Storage se você já usa Supabase (regras de acesso integradas ao login).

## Decisão rápida

- **Use se:** o sistema recebe ou gera arquivos e roda em mais de uma instância ou em PaaS.
- **Evite se:** são poucos arquivos fixos do próprio site; coloque-os no repositório ou no CDN do host.
