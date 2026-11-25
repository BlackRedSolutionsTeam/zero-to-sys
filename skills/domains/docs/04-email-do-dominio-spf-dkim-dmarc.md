# E-mail do domínio: MX, SPF, DKIM e DMARC

> Aponte o MX para o provedor de caixas, autorize quem envia com SPF e DKIM, publique DMARC começando em `none` e suba até `reject`, com o envio transacional em um subdomínio separado.

| | |
|---|---|
| **Referência** | RFC 7208 (SPF), RFC 6376 (DKIM), RFC 7489 (DMARC); requisitos de remetente do Gmail (support.google.com/a/answer/81126) e do Yahoo (senders.yahooinc.com); documentação do Google Workspace, Microsoft 365 e Zoho Mail |
| **Categoria** | Domínios |
| **Tipo** | Prática de configuração de DNS de e-mail |
| **Vale para** | Qualquer domínio que envia ou recebe e-mail; exemplos com `clinica-exemplo.com.br` |
| **Verificado em** | 2026-11-25 |

## O que é

Cinco registros de DNS decidem se o e-mail chega:

- **MX:** diz qual servidor recebe o e-mail do domínio.
- **SPF:** lista quem pode enviar em nome do domínio.
- **DKIM:** assinatura digital que prova que a mensagem não foi alterada e saiu de quem diz.
- **DMARC:** diz ao destinatário o que fazer quando SPF e DKIM falham, e envia relatórios.
- **BIMI:** exibe o logo da marca na caixa de entrada. Exige DMARC forte e certificado de marca; só vale para empresa grande, então apenas cite.

Exemplo do doc: a clínica recebe e-mail em `contato@clinica-exemplo.com.br` e o sistema envia lembretes de consulta.

## Por que usar

- **Entrega:** sem autenticação o e-mail cai no spam ou é recusado.
- **Proteção da marca:** sem DMARC, qualquer pessoa envia e-mail falso como se fosse a clínica.
- **Exigência dos grandes:** desde fevereiro de 2024 o Gmail e o Yahoo cobram autenticação de quem envia para eles.

## Quando usar

- No dia em que o domínio ganha uma caixa de e-mail.
- Antes do primeiro e-mail transacional (confirmação, lembrete, recuperação de senha).
- Mesmo em domínio que não envia e-mail: um DMARC `reject` e um SPF `-all` impedem falsificação.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Formulário de contato e caixa própria precisam de SPF, DKIM e DMARC |
| MVP de SaaS | ✅ Ótimo | Cadastro e recuperação de senha dependem de entrega |
| SaaS em crescimento | ✅ Ótimo | Subdomínio transacional protege a reputação do corporativo |
| Sistema interno/corporativo | ✅ Ótimo | Evita falsificação do domínio da empresa |
| API/integração | 🟡 Serve | Só se enviar e-mail; senão publique SPF `-all` e DMARC `reject` |
| App mobile com backend | ✅ Ótimo | Códigos de acesso por e-mail precisam chegar |
| Domínio parado, sem e-mail | ❌ Evite MX | Não crie MX; publique só o bloqueio (SPF `-all`, DMARC `reject`) |

## Quando é bom

- **Um provedor de caixas** (Google Workspace, Microsoft 365, Zoho) e um serviço transacional, cada um com o seu DKIM.
- **DMARC com relatório** (`rua`) para ver quem envia em seu nome antes de endurecer.
- **Subdomínio para o transacional:** `mail.clinica-exemplo.com.br` isola a reputação. Um erro no envio em massa não derruba a caixa dos atendentes.

## Quando é ruim

- **Dois registros SPF:** o domínio pode ter só um TXT começando com `v=spf1`. Dois geram erro e o SPF falha. Junte tudo em um.
- **Passar de 10 consultas DNS no SPF:** a RFC 7208 limita a 10 os termos `include`, `a`, `mx`, `ptr`, `exists` e o modificador `redirect`. Passou disso, o resultado é `permerror` e o SPF falha. Os `include` de cada provedor contam, e os que eles usam por dentro também. Tire os que não usa mais, prefira `ip4`/`ip6` (não contam) e mova serviços para subdomínios, cada um com o seu SPF. A mesma RFC recomenda no máximo duas consultas sem resposta.
- **`reject` sem ter visto os relatórios:** pode bloquear o seu próprio e-mail legítimo.
- **`~all` ou `+all` para sempre:** `+all` libera todo mundo. Termine com `-all` ou `~all` e não use `+all`.

## Como começar

**1. MX (conferido em 2026-11-25 nas páginas oficiais).** Troque os MX antigos pelos do provedor; não deixe MX de dois provedores com a mesma prioridade.

| Provedor | Nome | Valor | Prioridade |
|---|---|---|---|
| Google Workspace | `@` | `smtp.google.com` | 1 |
| Microsoft 365 | `@` | valor mostrado no centro de administração | 0 |
| Zoho Mail | `@` | `mx.zoho.com`, `mx2.zoho.com`, `mx3.zoho.com` | 10, 20, 50 |

O Google informa que contas criadas antes de 2023 podem ter valores `aspmx...` e que eles continuam valendo. No Microsoft 365 o valor do MX é exclusivo do seu domínio: copie do painel. No Zoho, os valores mudam conforme o data center (veja o Admin Console). Planos: o Zoho Mail tem plano gratuito para um domínio e até cinco usuários, sem IMAP/POP (página de preços conferida na data acima); preços de Google e Microsoft mudam, consulte as páginas oficiais.

**2. SPF.** Um único TXT no apex. Os `include` abaixo são o formato; copie o valor exato do painel de cada provedor.

```
clinica-exemplo.com.br.  TXT  "v=spf1 include:spf.protection.outlook.com -all"
```

O exemplo é o do Microsoft 365, que a Microsoft publica em sua documentação. Para Google e Zoho copie o `include` do painel de cada um. Com mais de um serviço, junte no mesmo registro: `v=spf1 include:A include:B -all`.

**3. DKIM.** Cada provedor gera a chave no painel, e você publica o registro que ele mostra. No Microsoft 365 são dois CNAME (`selector1._domainkey` e `selector2._domainkey`). No Google e no Zoho é um TXT em `<seletor>._domainkey`. O Google pede chave de no mínimo 1024 bits e recomenda 2048. Se o DNS limitar o tamanho do TXT, dividir em partes entre aspas funciona na maioria dos painéis.

**4. DMARC.** TXT em `_dmarc`. Comece só observando:

```
_dmarc.clinica-exemplo.com.br.  TXT  "v=DMARC1; p=none; rua=mailto:dmarc@clinica-exemplo.com.br"
```

Suba aos poucos, esperando algumas semanas e lendo os relatórios entre cada passo:

| Etapa | Política | O que acontece com e-mail que falha |
|---|---|---|
| 1 | `p=none` | Nada; você só recebe relatórios |
| 2 | `p=quarantine; pct=25` e depois `pct=100` | Vai para a caixa de spam |
| 3 | `p=reject` | É recusado |

**5. Transacional em subdomínio.** Registre `mail.clinica-exemplo.com.br` no serviço de envio. Ele pede SPF e DKIM nesse subdomínio, o que mantém o SPF do apex pequeno. Detalhes em [e-mail transacional](../../integrations/docs/02-email-transacional.md).

**6. Requisitos do Gmail e do Yahoo (fevereiro de 2024, conferidos na data acima).**

- Todos os remetentes: SPF ou DKIM, DNS reverso válido (PTR) do IP de envio, TLS, formato RFC 5322 e taxa de spam abaixo de 0,3% (o Google recomenda abaixo de 0,10%).
- Remetentes em massa (o Google fala em mais de 5.000 mensagens por dia para Gmail; o Yahoo não publica número): SPF e DKIM juntos, DMARC no mínimo `p=none`, domínio do From alinhado com SPF ou DKIM, e cancelamento em um clique (`List-Unsubscribe` e `List-Unsubscribe-Post: List-Unsubscribe=One-Click`) mais link visível no corpo.

**7. Testar.**

```bash
dig +short MX clinica-exemplo.com.br
dig +short TXT clinica-exemplo.com.br
dig +short TXT _dmarc.clinica-exemplo.com.br
dig +short TXT google._domainkey.clinica-exemplo.com.br
```

Ferramentas gratuitas: mande um e-mail para o Gmail e abra "Mostrar original" (veja SPF, DKIM e DMARC como `PASS`); use o mail-tester.com, o MXToolbox e o Google Postmaster Tools (reputação de quem envia muito para Gmail). Confira a contagem de consultas do SPF em um verificador, como o do MXToolbox.

## Combina com / alternativas

- [DNS, registros e propagação](02-dns-registros-e-propagacao.md) e [Subdomínios e ambientes](03-subdominios-e-ambientes.md).
- [E-mail transacional](../../integrations/docs/02-email-transacional.md): o serviço de envio e o webhook de falhas.
- [Migrar DNS sem queda](07-migrar-dns-sem-queda.md): copie MX e TXT antes de trocar os nameservers.
- Alternativa: provedor brasileiro de hospedagem de e-mail. Confira o plano e se ele oferece DKIM antes de contratar.

## Decisão rápida

- **Use se:** o domínio recebe ou envia e-mail, ou você quer impedir que o falsifiquem.
- **Evite se:** quer pular o DKIM "porque o SPF basta"; ou subir direto para `reject` sem ler os relatórios do `none`.
