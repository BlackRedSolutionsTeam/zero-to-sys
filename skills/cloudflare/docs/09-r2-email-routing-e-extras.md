# R2, Email Routing e extras da Cloudflare

> Armazenamento de arquivos sem taxa de saída, e-mail do domínio encaminhado, redirecionamentos e limites que pegam de surpresa.

| | |
|---|---|
| **Referência** | developers.cloudflare.com (R2, Email Routing, Rules, Fundamentals) |
| **Categoria** | Borda |
| **Tipo** | Prática de serviços complementares da Cloudflare |
| **Vale para** | Projetos com domínio na Cloudflare que guardam arquivos, recebem e-mail ou precisam redirecionar URLs |
| **Verificado em** | 2026-11-25 |

## O que é

Reúne os serviços menores que quase todo projeto acaba usando depois de colocar o domínio na Cloudflare:

- **R2:** armazenamento de objetos (arquivos) compatível com a API do S3.
- **Email Routing:** recebe e-mail do seu domínio (`contato@clinica-exemplo.com.br`) e encaminha para uma caixa existente, como um Gmail. Também pode entregar a um Worker.
- **Redirect Rules e Bulk Redirects:** redirecionam URLs na borda, sem passar pela aplicação.
- **Páginas de erro** personalizadas e **Web Analytics** (métricas de visitas sem cookie).
- **Limites do proxy:** tamanho máximo de upload e tempo máximo de espera pela origem.

## Por que usar

- **R2 sem taxa de saída:** baixar arquivos não gera cobrança de egress (dados que saem do armazenamento).
- **E-mail do domínio sem servidor de e-mail:** nada para manter.
- **Redirecionamento na borda:** mais rápido e sem código na aplicação.
- **Analytics sem banner de cookie** para métricas básicas.

## Quando usar

- Uploads de usuários (fotos, exames em PDF) em vez de gravar no disco da VPS.
- Endereços `contato@` e `suporte@` encaminhados para a caixa de quem atende.
- Troca de domínio, mudança de URLs ou `www` para o domínio principal.
- Antes de estranhar um erro 413 (arquivo grande) ou 524 (origem demorou).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Redirects, Web Analytics e e-mail de contato sem custo |
| MVP de SaaS | ✅ Ótimo | R2 e Email Routing no plano grátis cobrem o início |
| SaaS em crescimento | ✅ Ótimo | R2 evita custo de saída; Bulk Redirects para migrações |
| Sistema interno/corporativo | 🟡 Serve | Útil para anexos; e-mail corporativo costuma ser outro produto |
| API/integração | 🟡 Serve | R2 para arquivos gerados; o resto pouco se aplica |
| App mobile com backend | ✅ Ótimo | R2 com URL assinada para foto e anexo |
| Envio de e-mail em massa ou transacional | ❌ Evite | Email Routing só recebe e encaminha; use serviço de envio |

## Quando é bom

- **R2:** plano grátis conferido em 2026-11-25 na página de preços: 10 GB-mês de armazenamento, 1 milhão de operações Classe A (escrita e listagem) e 10 milhões de Classe B (leitura) por mês, só no armazenamento Standard. Acima disso: US$ 0,015 por GB-mês, US$ 4,50 por milhão de Classe A e US$ 0,36 por milhão de Classe B.
- **Egress grátis** quando os dados saem pela API de Workers, pela API S3 ou por `r2.dev`. Outros serviços ligados ao bucket podem cobrar à parte.
- **Acesso S3:** bibliotecas e o código de [armazenamento de arquivos](../../integrations/docs/07-armazenamento-de-arquivos.md) funcionam trocando só o endpoint.
- **Email Routing** disponível nos planos Workers Free e Paid; encaminha para endereços de destino verificados.
- **Bulk Redirects** são estáticos e valem para a conta inteira, bons para listas longas de URLs antigas.

## Quando é ruim

- **R2 público de verdade:** o domínio `r2.dev` serve para teste; em produção ligue um domínio próprio ao bucket.
- **Arquivo privado:** não deixe o bucket público; gere URL assinada pelo backend.
- **Email Routing não envia como você.** A Cloudflare tem outro produto, o Email Sending (em beta na data da consulta), mas para e-mail do sistema veja [e-mail transacional](../../integrations/docs/02-email-transacional.md).
- **Regra de e-mail desativada** até o endereço de destino ser verificado pelo clique no e-mail de confirmação.
- **Bulk Redirects não aceitam regex** nem substituição de texto; para isso use Redirect Rules.
- **Limites de plano mudam:** a cota de regras e de entradas de redirecionamento por plano não foi conferida; consulte a página de cada recurso.

## Limites do proxy (conferido em 2026-11-25)

| Limite | Valor | Observação |
|---|---|---|
| Upload máximo por requisição | Free e Pro 100 MB; Business 200 MB; Enterprise até 5 GB | Acima disso a Cloudflare recusa; envie direto para o R2 com URL assinada |
| Arquivo máximo em cache | 512 MB (Free, Pro, Business) | Enterprise 5 GB por padrão |
| Espera pela resposta da origem | 125 s na página de limites de conexão | Passou disso, erro 524. Só Enterprise altera. A documentação do provider ainda cita 100 s como valor histórico |
| Escrita para a origem | 30 s | Erro 524 |
| Conexão ociosa | 900 s | Erro 520 |

Com Tunnel, vale o menor timeout entre o da borda e o do túnel. Tarefa longa (relatório, importação) vai para fila e a tela consulta o resultado depois; veja o doc de segundo plano na skill de integrações.

## Como começar

R2 pelo Wrangler (CLI da Cloudflare):

```bash
npx wrangler login
npx wrangler r2 bucket create clinica-exemplo-anexos
npx wrangler r2 bucket list
```

Para o app usar a API S3, crie no painel um token de API do R2 (Object Read & Write, restrito ao bucket) e use o endpoint da conta:

```bash
export S3_ENDPOINT="https://<account_id>.r2.cloudflarestorage.com"
export S3_BUCKET="clinica-exemplo-anexos"
export S3_REGION="auto"
aws s3 ls "s3://$S3_BUCKET" --endpoint-url "$S3_ENDPOINT"
```

Email Routing, no painel do domínio:

1. Abra Email, depois Email Routing, e ative. A Cloudflare propõe criar os registros MX e SPF; aceite.
2. Crie o endereço `contato` com destino na caixa real e confirme o e-mail de verificação.
3. Opcional: ative o catch-all para receber qualquer endereço do domínio.

Se o domínio já usa outro serviço de e-mail, não troque os MX sem planejar: o e-mail passa a chegar só pela Cloudflare.

Redirect de `www` para o domínio principal (Redirect Rule), pelo painel em Rules, Redirect Rules:

- Expressão: `http.host eq "www.clinica-exemplo.com.br"`
- Ação: URL dinâmica `concat("https://clinica-exemplo.com.br", http.request.uri.path)`, status 301, preservando a query string.

A mesma regra em código está em [Cloudflare com IaC](10-cloudflare-com-iac.md). Para páginas de erro personalizadas e Web Analytics, ative no painel (Custom Error Rules e Web Analytics) e confirme os passos na documentação, que muda de tela com frequência.

## Combina com / alternativas

- [Armazenamento de arquivos](../../integrations/docs/07-armazenamento-de-arquivos.md): URL assinada, validação de tipo e tamanho.
- [E-mail transacional](../../integrations/docs/02-email-transacional.md): para enviar, não só receber.
- [Cloudflare com IaC](10-cloudflare-com-iac.md): redirects e DNS em código.
- Alternativas: S3, Backblaze B2 ou Supabase Storage; Google Workspace para caixa de e-mail completa; Plausible para analytics.

## Decisão rápida

- **Use se:** o domínio está na Cloudflare e você quer arquivos com saída grátis, e-mail de contato e redirects sem manter servidor.
- **Evite se:** precisa enviar e-mail do sistema por aqui, ou o limite de upload do seu plano não comporta os arquivos sem envio direto ao R2.
