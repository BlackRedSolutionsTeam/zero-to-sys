# Escolher e registrar o domínio

> Escolha um nome curto, registre no lugar certo para o TLD e deixe a titularidade em nome do cliente.

| | |
|---|---|
| **Referência** | registro.br, cloudflare.com/products/registrar, páginas oficiais de Porkbun, Namecheap e GoDaddy |
| **Categoria** | Domínios |
| **Tipo** | Prática de escolha e registro de domínio |
| **Vale para** | Qualquer projeto com endereço público próprio |
| **Verificado em** | 2026-11-25 |

## O que é

Domínio é o nome do seu sistema na internet, como `clinica-exemplo.com.br`. **TLD** é o final dele: `.com.br`, `.com`, `.app`, `.dev`. **Registrar** é a empresa que vende e renova o domínio para você. **Registrante** é o dono legal do domínio, quem consta no cadastro.

Registrar o domínio não é hospedar o site. O domínio só aponta para algum lugar (veja o doc 02).

## Por que usar

- **Endereço próprio** passa confiança e permite e-mail com o seu nome.
- **Independência:** você muda de servidor sem mudar de endereço.
- **Subdomínios** separam site, app, API e staging.
- **Titularidade clara** evita perder o sistema numa briga com freelancer ou agência.
- **Renovação previsível:** um custo anual fácil de pôr no orçamento do cliente.

## Quando usar

- Antes do primeiro deploy público.
- Antes de configurar e-mail do domínio ou certificado HTTPS.
- Ao entregar um projeto: o domínio precisa estar no nome do cliente.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | `.com.br` para público brasileiro, `.com` se for internacional |
| MVP de SaaS | ✅ Ótimo | Domínio barato já no começo; `.com.br` ou `.com` |
| SaaS em crescimento | ✅ Ótimo | Registre também a variação `.com` e `.com.br` para proteger o nome |
| Sistema interno/corporativo | 🟡 Serve | Pode usar subdomínio de um domínio que a empresa já tem |
| API/integração | 🟡 Serve | Costuma viver em `api.` do domínio do produto |
| App mobile com backend | 🟡 Serve | Só a API e as páginas de link precisam de domínio |
| Protótipo descartável | ❌ Evite | Use o endereço grátis da hospedagem; domínio é custo e renovação à toa |

## Quando é bom

- **Registro.br para `.com.br`:** é o registro oficial dos domínios `.br`. Conferido em 2026-11-25: a página inicial anuncia registro por R$ 40,00 por ano.
- **Cloudflare Registrar:** declara preço de custo, sem markup, e WHOIS redaction gratuita. Conferido em 2026-11-25: a página lista `.com`, `.net`, `.org`, `.ai`, `.app` e `.dev`, e não lista `.br`.
- **Domínio e DNS no mesmo lugar** (Cloudflare) simplifica a operação.
- **Titular da empresa:** o cliente consegue renovar e transferir sem depender de você.

## Quando é ruim

- **Registrar no seu CPF para o cliente:** você vira refém da renovação e, se sumir, o cliente perde o domínio.
- **Nome com hífen, número ou grafia difícil:** ninguém acerta ao ditar por telefone.
- **Promoção de primeiro ano:** a renovação costuma custar mais. Veja o preço de renovação antes de comprar.
- **Marca já registrada por outra empresa:** o domínio pode ser tomado ou gerar disputa.
- **WHOIS aberto:** dados pessoais ficam públicos em alguns registrars. Prefira quem oferece redação gratuita.

## Como começar

### 1. Escolha o nome

- Curto, de preferência até 15 letras, sem hífen e sem número.
- Fácil de ditar: se você precisa soletrar, troque.
- Consulte a disponibilidade em `.com.br` e em `.com`.
- Pesquise o nome em busca de marca. A consulta à base de marcas do INPI (Instituto Nacional da Propriedade Industrial) é feita no site do INPI; este plugin só recomenda consultar e deixa a análise jurídica com um profissional.

### 2. Decida onde registrar

| Tipo de projeto | TLD | Onde registrar | Onde fica o DNS |
|---|---|---|---|
| Público brasileiro, empresa ou clínica | `.com.br` | Registro.br | Cloudflare (padrão) |
| SaaS com visão internacional | `.com` | Cloudflare Registrar | Cloudflare |
| App ou ferramenta de dev | `.app` ou `.dev` | Cloudflare Registrar ou outro registrar | Cloudflare |
| Sistema interno | subdomínio do domínio da empresa | já existente | onde a empresa já mantém |

Exemplo do plugin: a clínica usa `clinica-exemplo.com.br` registrado no Registro.br, com `app.`, `api.` e `staging.` como subdomínios.

### 3. Registre no Registro.br

Conferido em 2026-11-25 na página inicial: R$ 40,00 por ano. O Registro.br pede cadastro com CPF ou CNPJ do titular, então use os dados do cliente. O fluxo exato de telas, os prazos de ativação e as regras de renovação mudam; siga a Central de Ajuda em registro.br/ajuda, que não consegui abrir por extenso nesta verificação.

Ordem prática:

1. Crie o cadastro do titular com o CPF ou CNPJ do cliente e o e-mail dele.
2. Pesquise o nome e escolha a extensão.
3. Informe os servidores de nome (nameservers) da Cloudflare, se o DNS ficará lá.
4. Pague e guarde o comprovante.
5. Ligue a renovação automática e confira o e-mail de contato.

### 4. Registre `.com`, `.app` ou `.dev`

No Cloudflare Registrar a compra é feita no painel da Cloudflare, pela conta do cliente. Porkbun, Namecheap e GoDaddy também vendem esses TLDs; não conferi os preços deles nesta verificação, então compare a página oficial de cada um, incluindo o valor de renovação, antes de escolher.

### 5. Registre a titularidade

Anote em um documento do projeto: titular, e-mail do contato, registrar, onde está o DNS e a data de expiração.

## Combina com / alternativas

- **DNS e registros:** [02-dns-registros-e-propagacao.md](02-dns-registros-e-propagacao.md).
- **Cloudflare como DNS:** [../../infra/docs/08-cloudflare.md](../../infra/docs/08-cloudflare.md).
- **Hospedagem:** [../../infra/docs/02-vps-coolify-dokploy.md](../../infra/docs/02-vps-coolify-dokploy.md).
- **Alternativa grátis:** o endereço que a hospedagem entrega (`*.vercel.app` e semelhantes) serve para protótipo.

## Decisão rápida

- **Use se:** o sistema vai a público e o cliente precisa de endereço próprio e e-mail com o nome da empresa.
- **Evite se:** é só um protótipo de poucos dias ou um sistema interno que cabe num subdomínio que a empresa já tem.
