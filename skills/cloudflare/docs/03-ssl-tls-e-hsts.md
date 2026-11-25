# SSL/TLS e HSTS na Cloudflare

> Use o modo Full (strict) com certificado válido na origem, redirecione tudo para HTTPS e só ligue HSTS com preload depois de ter certeza de que todo o domínio vai ficar em HTTPS.

| | |
|---|---|
| **Referência** | developers.cloudflare.com/ssl (modos de SSL/TLS, Origin CA, HSTS, Always Use HTTPS, Minimum TLS, Authenticated Origin Pulls) |
| **Categoria** | Borda |
| **Tipo** | Prática de configuração de criptografia |
| **Vale para** | Qualquer domínio com proxy da Cloudflare ligado (nuvem laranja) |
| **Verificado em** | 2026-11-25 |

## O que é

Com a Cloudflare na frente, existem duas conexões: **visitante → Cloudflare** e **Cloudflare → origem** (seu servidor). O modo de SSL/TLS define se cada uma é criptografada e se o certificado da origem é conferido.

Exemplo do doc: `clinica-exemplo.com.br`, com `app.` (front), `api.` (API) e `staging.`, todos na frente de uma VPS.

Termos:

- **Origem:** o servidor real (nginx, Coolify etc.).
- **HSTS:** cabeçalho que manda o navegador usar só HTTPS naquele domínio por um tempo.
- **Origin CA:** autoridade certificadora da Cloudflare que emite certificados que só a Cloudflare confia.

## Por que usar

- **Sem trecho aberto:** em Full (strict) o caminho todo é criptografado e a origem é validada.
- **Evita dados de pacientes em texto puro** entre a Cloudflare e o servidor.
- **Barra desvio:** a Cloudflare recomenda Full ou Full (strict) para impedir conexões maliciosas na origem.

## Quando usar

- Sempre que o domínio estiver proxied. Configure no mesmo dia em que trocar os nameservers.
- Antes de ligar HSTS, Authenticated Origin Pulls ou qualquer regra de cache.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Full (strict) com Always Use HTTPS; HSTS é opcional |
| MVP de SaaS | ✅ Ótimo | Cookie de login só trafega seguro se tudo for HTTPS |
| SaaS em crescimento | ✅ Ótimo | Adicione HSTS e Authenticated Origin Pulls |
| Sistema interno/corporativo | ✅ Ótimo | Origin CA resolve o certificado sem expor nada |
| API/integração | ✅ Ótimo | Clientes e webhooks exigem HTTPS válido |
| App mobile com backend | ✅ Ótimo | Dispensa certificado extra no app |
| Origem sem nenhum suporte a TLS, sem poder instalar certificado | ❌ Evite Flexible | Use Tunnel ([06](06-tunnel-e-protecao-da-origem.md)) em vez de abrir a origem em HTTP |

## Quando é bom

- **Certificado de origem sem renovação frequente:** o Origin CA evita o Let's Encrypt só para falar com a Cloudflare (você escolhe a validade ao criar).
- **Redirecionamento na borda:** Always Use HTTPS poupa configuração no nginx.
- **Controle de versão do TLS** na zona, inclusive no plano grátis.

## Quando é ruim

- **Flexible:** o trecho Cloudflare → origem vai em HTTP. Qualquer um no caminho lê cookies e senhas. Pior: o site parece seguro (cadeado) para o visitante.
- **Origin CA com proxy desligado:** o navegador não confia nesse certificado. Se pausar a Cloudflare ou usar nuvem cinza, o visitante vê erro.
- **Esquecer a validade:** a Cloudflare não envia aviso de expiração do Origin CA. Anote a data.
- **HSTS com preload cedo demais:** a própria Cloudflare avisa que pode deixar o site sem HTTPS totalmente inacessível.

## Como começar

### Modos de SSL/TLS (conferido em 2026-11-25)

| Modo | O que acontece | Quando usar |
|---|---|---|
| Off | Tudo em HTTP, nas duas conexões | Nunca |
| Flexible | Visitante em HTTPS, mas Cloudflare → origem em HTTP | Nunca; só como degrau temporário de uma origem sem TLS |
| Full | Usa HTTPS na origem sem validar o certificado (aceita autoassinado) | Migração rápida, enquanto o certificado correto não está pronto |
| Full (strict) | Como Full, mas valida o certificado (CA pública ou Origin CA) | Padrão recomendado |
| Strict (SSL-Only Origin Pull) | Sempre HTTPS com validação na origem, mesmo se o visitante usou HTTP | Quando nada deve chegar à origem em HTTP |

A página oficial também descreve o SSL/TLS automático, em liberação gradual. Ele só sobe o modo, nunca desce, então o certificado da origem precisa continuar válido. Confira no painel se sua zona já o tem.

### Por que nunca Flexible

Flexible gera dois problemas: tráfego sem criptografia entre a Cloudflare e o servidor, e laços de redirecionamento quando a origem também redireciona para HTTPS. A Cloudflare recomenda não redirecionar na origem. Com Full (strict) os dois problemas somem.

### Origin CA certificate

1. No painel, abra o domínio, depois SSL/TLS, Origin Server, aba Origin Certificates, Create Certificate.
2. Deixe a Cloudflare gerar a chave (RSA ou ECC) ou envie seu CSR.
3. Mantenha o apex e o curinga de primeiro nível (`clinica-exemplo.com.br` e `*.clinica-exemplo.com.br`). O curinga cobre um nível só; o certificado aceita até 200 nomes.
4. Escolha a validade e baixe o PEM. A chave privada não aparece de novo depois dessa tela.
5. Instale o certificado e a chave na origem (veja [nginx](../../nginx/docs/)) e guarde a chave como segredo.
6. Troque o modo para Full (strict).

### Always Use HTTPS

Em SSL/TLS, Edge Certificates, ligue Always Use HTTPS. Vale para todos os hosts da zona. O modo não pode estar Off. Se só parte do sistema tem HTTPS, use uma Redirect Rule só nos caminhos certos. Ele não corrige conteúdo misto (imagem em `http://` dentro de página HTTPS); corrija os links.

### HSTS com cuidado

Em Edge Certificates, Enable HSTS. Opções: max-age de 1 a 12 meses, includeSubDomains, preload e no-sniff.

Ordem segura:

1. Confirme HTTPS em todos os subdomínios que usará (`app.`, `api.`, `staging.`).
2. Comece com max-age de 1 mês, sem includeSubDomains.
3. Depois de uma semana sem erro, suba para 6 meses.
4. includeSubDomains só quando todo subdomínio, inclusive os esquecidos, tiver HTTPS.
5. Preload (exige 12 meses) só no fim. Depois de ligar, é preciso enviar o domínio à lista de preload e sair dela é lento.

Se remover o HTTPS antes de o max-age expirar, o site fica inacessível nesse período.

### TLS mínimo

Em Edge Certificates, Minimum TLS Version. Disponível em todos os planos. A página não indica uma versão recomendada nem o padrão. Como regra do projeto: use no mínimo 1.2 e confirme que seus clientes (apps, integrações antigas) aguentam. A configuração não vale para Pages nem domínios do R2.

### Authenticated Origin Pulls

A origem passa a exigir um certificado de cliente que só a Cloudflare apresenta. Disponível em todos os planos. Há três níveis: global, por zona e por hostname.

- O global usa um certificado compartilhado por todas as contas Cloudflare: prova que veio da rede Cloudflare, não da sua conta. Para isso, prefira por zona ou por hostname com certificado seu.
- Não funciona com SSL Off ou Flexible, nem com Cloudflare Tunnel.
- A origem valida o certificado de cliente; as diretivas do nginx estão em [nginx](../../nginx/docs/) e em nginx.org (não conferidas aqui).

## Combina com / alternativas

- [Proteção da origem](06-tunnel-e-protecao-da-origem.md): Tunnel dispensa Authenticated Origin Pulls.
- [DNS e proxy](02-dns-e-proxy.md): HSTS e Origin CA dependem de a nuvem estar laranja.
- [Cloudflare na infra](../../infra/docs/08-cloudflare.md).
- Alternativa ao Origin CA: Let's Encrypt na origem, que o navegador também aceita se o proxy for desligado.

## Decisão rápida

- **Use se:** o domínio está na Cloudflare e a origem aceita HTTPS. Configure Full (strict), Origin CA, Always Use HTTPS e TLS mínimo 1.2.
- **Evite se:** pensa em Flexible por pressa, ou em ligar preload sem ter inventariado todos os subdomínios.
