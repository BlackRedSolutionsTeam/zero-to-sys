# Upload de arquivos

> Arquivo enviado pelo usuário é entrada hostil: valide pelo conteúdo, limite o tamanho, troque o nome, guarde fora da pasta pública e entregue por URL assinada de curta duração.

| | |
|---|---|
| **Referência** | OWASP, "File Upload Cheat Sheet" (cheatsheetseries.owasp.org); OWASP Top 10, A01 Broken Access Control; documentação oficial do Amazon S3 (URLs pré-assinadas), Cloudflare R2, Supabase Storage e ClamAV (docs.clamav.net) |
| **Categoria** | Segurança |
| **Tipo** | Prática de proteção de entrada de dados |
| **Vale para** | Qualquer stack; exemplo em TypeScript com armazenamento compatível com S3 (S3, Cloudflare R2) |
| **Verificado em** | 2026-11-24 |

## O que é

Upload é qualquer arquivo que o usuário manda para o sistema: foto de perfil, exame de paciente, anexo, planilha. O risco é o arquivo ser algo diferente do que diz ser (um script disfarçado de imagem), ser enorme, ter nome malicioso ou ser lido por quem não devia.

Termos usados aqui:

- **Magic bytes:** os primeiros bytes do arquivo, que identificam o formato de verdade (um PNG começa com uma assinatura fixa). A extensão e o `Content-Type` vêm do cliente e podem mentir.
- **URL pré-assinada:** link temporário, gerado pelo seu servidor, que autoriza uma única operação (enviar ou baixar) direto no armazenamento.
- **Path traversal:** nome de arquivo como `../../etc/passwd` que faz o servidor gravar ou ler fora da pasta prevista.

## Por que usar

- **Evita execução de código:** arquivo enviado nunca roda no servidor.
- **Evita vazamento:** exame de paciente não fica numa URL pública adivinhável.
- **Evita custo e queda:** o limite de tamanho protege disco e memória.

## Quando usar

- Em todo campo de arquivo.
- Quando o arquivo contém dado pessoal ou de saúde (veja [LGPD na prática](./09-lgpd-na-pratica.md)).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Upload quase só no painel do editor; as regras valem igual |
| MVP de SaaS | ✅ Ótimo | Anexos e fotos aparecem cedo; comece certo |
| SaaS em crescimento | ✅ Ótimo | Volume alto pede upload direto e varredura |
| Sistema interno/corporativo | ✅ Ótimo | Documentos sensíveis e usuários com acessos diferentes |
| API/integração | ✅ Ótimo | Quem chama a API também pode mandar arquivo malicioso |
| App mobile com backend | ✅ Ótimo | Upload direto com URL pré-assinada poupa banda do servidor |
| Qualquer um, gravando em `public/` com o nome original | ❌ Evite | Abre caminho para execução de código e sobrescrita |

## Quando é bom

- **Tipo pelo conteúdo:** lista de formatos permitidos conferida nos magic bytes.
- **Nome gerado por você:** UUID mais a extensão que você decidiu, nunca o nome do usuário.
- **Armazenamento separado:** bucket privado (S3, R2, Supabase Storage), sem acesso público.
- **Entrega por URL assinada** que expira em minutos, gerada só depois de checar a permissão (veja [papéis e permissões](./04-papeis-e-permissoes.md)).
- **Upload direto do navegador** para o bucket: o arquivo não passa pelo seu servidor.

## Quando é ruim

- **Confiar na extensão ou no `Content-Type`:** o cliente controla os dois.
- **Guardar na pasta pública do app** ou no disco do servidor (some a cada deploy e pode ser executado).
- **Usar o nome original** no caminho: path traversal e colisão entre usuários.
- **Servir inline** arquivo do usuário no seu domínio: um HTML ou SVG com script roda com a sua origem.
- **Sem limite de tamanho** (incluindo arquivo compactado que expande demais, o zip bomb).
- **Bucket com link público** para dado pessoal.

## Como começar

### 1. Limites e lista de formatos

```ts
export const UPLOAD_RULES = {
  exam: { maxBytes: 10 * 1024 * 1024, mimes: ['application/pdf', 'image/jpeg', 'image/png'] },
  avatar: { maxBytes: 2 * 1024 * 1024, mimes: ['image/jpeg', 'image/png', 'image/webp'] },
} as const
```

### 2. Pedir a URL pré-assinada (servidor)

O servidor checa quem é o usuário e a regra, gera a chave com UUID e assina só aquela chave, com tempo curto.

```ts
import { randomUUID } from 'node:crypto'
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'

const s3 = new S3Client({ region: 'auto', endpoint: process.env.S3_ENDPOINT })

export async function createUploadUrl(clinicId: string, kind: keyof typeof UPLOAD_RULES, mime: string) {
  const rule = UPLOAD_RULES[kind]
  if (!rule.mimes.includes(mime as never)) throw new Error('Formato não permitido')
  const key = `clinics/${clinicId}/pending/${randomUUID()}`
  const command = new PutObjectCommand({ Bucket: process.env.S3_BUCKET, Key: key, ContentType: mime })
  const url = await getSignedUrl(s3, command, { expiresIn: 300 })
  return { url, key }
}
```

O navegador envia com `PUT` direto para `url`. O `PUT` pré-assinado não limita o tamanho sozinho; para limitar no armazenamento use a política de `POST` do S3 (`content-length-range`; o Cloudflare R2 não suporta `POST` pré-assinado) ou a regra do seu provedor, e confira também o tamanho no passo 3.

### 3. Validar de verdade depois do envio

Marque o arquivo como pendente, leia só o começo dele e confira os magic bytes com a biblioteca `file-type`.

```ts
import { fileTypeFromBuffer } from 'file-type'

export async function confirmUpload(key: string, kind: keyof typeof UPLOAD_RULES) {
  const rule = UPLOAD_RULES[kind]
  const { size, head } = await readHead(key, 4100)
  if (size > rule.maxBytes) return reject(key, 'Arquivo grande demais')
  const detected = await fileTypeFromBuffer(head)
  if (!detected || !rule.mimes.includes(detected.mime as never)) return reject(key, 'Conteúdo não confere')
  return moveTo(key, key.replace('/pending/', '/files/'))
}
```

`readHead`, `reject` e `moveTo` são funções suas sobre o SDK do armazenamento (ler os primeiros bytes com `Range`, apagar e mover). Arquivo `pending` nunca é entregue a ninguém.

### 4. Imagens: reprocessar

Decodificar e gravar de novo descarta scripts embutidos e metadados (EXIF, que pode ter a localização do celular). Com a biblioteca `sharp`, o resultado não carrega os metadados por padrão.

```ts
import sharp from 'sharp'

export const cleanImage = (input: Buffer) =>
  sharp(input).rotate().resize({ width: 2000, withoutEnlargement: true }).webp().toBuffer()
```

### 5. Baixar por URL assinada

```ts
import { GetObjectCommand } from '@aws-sdk/client-s3'

export const createDownloadUrl = (key: string) =>
  getSignedUrl(s3, new GetObjectCommand({
    Bucket: process.env.S3_BUCKET, Key: key,
    ResponseContentDisposition: 'attachment',
  }), { expiresIn: 120 })
```

Antes de chamar, confira que o usuário pode ver aquele paciente. O `attachment` força o download em vez de abrir no navegador.

### 6. Antivírus e regras fixas

- **ClamAV (gratuito):** use o `clamd` rodando como serviço e o cliente `clamdscan` (ou o envio por `--stream`). Vale quando outros usuários baixam o arquivo (anexos entre pessoas, documentos de clientes). Para foto reprocessada de avatar, costuma ser exagero.
- Nunca execute, importe ou interprete o arquivo enviado. Nunca monte caminho com o nome do usuário. Se precisar exibir o nome original, guarde-o no banco como texto e mostre escapado.
- Armazene o `Content-Type` que você detectou, não o que o cliente disse.

### Em cada stack

| Stack | Onde fazer |
|---|---|
| Node (Hono, Fastify, NestJS) | `@aws-sdk/s3-request-presigner` mais `file-type`, como acima |
| Next.js | Route Handler que devolve a URL pré-assinada |
| ASP.NET Core | `IFormFile` só com limite de tamanho; prefira URL pré-assinada do SDK do provedor |
| Django / Laravel | Validação do framework para tamanho; detecção do tipo pelo conteúdo no servidor |
| Supabase Storage | Bucket privado e `createSignedUploadUrl` / `createSignedUrl` com política (RLS) |

O armazenamento em si (criar bucket, CORS, ciclo de vida) fica na skill de integrações, ainda a escrever, em `../../integrations`. Segredos do bucket: [infra, segredos](../../infra/docs/09-segredos-e-configuracao.md).

## Combina com / alternativas

- [Papéis e permissões](./04-papeis-e-permissoes.md): quem pode baixar o exame de qual paciente.
- [OWASP no código](./05-owasp-no-codigo.md) e [rate limit](./06-rate-limit.md): limite quantos uploads por minuto.
- [LGPD na prática](./09-lgpd-na-pratica.md) e [dados pessoais](../../data/docs/10-dados-pessoais-e-lgpd.md): arquivo de saúde é dado sensível.
- [Formato de erro](../../api/docs/03-formato-de-erro.md): como responder 413 e 415.
- [Segurança base da infra](../../infra/docs/12-seguranca-base.md).
- Alternativa para conteúdo realmente público (logo, imagem de blog): bucket público com CDN.

## Decisão rápida

- **Use se:** o sistema recebe qualquer arquivo de usuário; aplique tipo pelo conteúdo, limite, nome novo, bucket privado e URL assinada.
- **Evite se:** a ideia é gravar na pasta pública com o nome original ou confiar na extensão; nesse caso, não aceite upload.
