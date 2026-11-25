# Certificados e HTTPS

> Todo endereço público precisa de certificado TLS válido e renovado sozinho, emitido por Let's Encrypt, pela Cloudflare ou pelo ACM da AWS.

| | |
|---|---|
| **Referência** | letsencrypt.org/docs, developers.cloudflare.com/ssl, docs.aws.amazon.com/acm |
| **Categoria** | Domínios |
| **Tipo** | Prática de HTTPS e certificados |
| **Vale para** | Qualquer sistema com domínio público (site, app, API) |
| **Verificado em** | 2026-11-25 |

## O que é

Certificado TLS é o arquivo que prova ao navegador que o servidor é mesmo o dono do domínio. Com ele, o endereço abre com `https://` e o tráfego vai criptografado. Uma **CA** (autoridade certificadora) emite o certificado depois de confirmar que você controla o domínio.

Três caminhos comuns:

- **Let's Encrypt:** CA gratuita. O servidor (Caddy, Nginx com certbot, Coolify, Dokploy) pede e renova sozinho pelo protocolo ACME.
- **Cloudflare (Universal SSL):** a Cloudflare emite e renova o certificado da borda. Ela escolhe a CA e a validade; você não mexe.
- **ACM (AWS Certificate Manager):** certificado gratuito para uso em serviços da AWS (balanceador, CloudFront). Com validação por DNS, renova sozinho.

## Por que usar

- **Obrigatório na prática:** navegadores marcam site sem HTTPS como inseguro.
- **Proteção de login e dados** contra quem está na mesma rede.
- **Exigência de recursos modernos:** HTTP/2, service workers, cookies seguros.
- **Custo zero** nos três caminhos acima.

## Quando usar

- Antes do primeiro deploy público, em app., api. e staging.
- Ao trocar de servidor ou migrar o DNS.
- Ao revisar o que vai expirar: certificado vencido derruba o site de uma vez.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Cloudflare na frente resolve sem configurar nada |
| MVP de SaaS | ✅ Ótimo | Let's Encrypt da plataforma (Coolify, Dokploy) ou Cloudflare |
| SaaS em crescimento | ✅ Ótimo | Cloudflare na borda e certificado de origem; wildcard se houver um subdomínio por cliente |
| Sistema interno/corporativo | 🟡 Serve | Domínio interno precisa de DNS-01 ou CA própria; HTTP-01 não alcança a máquina |
| API/integração | ✅ Ótimo | Certificado válido evita erro no cliente que chama a API |
| App mobile com backend | ✅ Ótimo | iOS e Android bloqueiam HTTP puro por padrão |
| Certificado autoassinado em produção | ❌ Evite | Navegador e apps recusam; ensina o usuário a ignorar alertas |

## Quando é bom

- **Renovação automática:** ninguém precisa lembrar de nada.
- **Sem custo:** Let's Encrypt, Cloudflare e ACM não cobram pelo certificado.
- **Wildcard** (`*.clinica-exemplo.com.br`) cobre vários subdomínios com um só certificado.
- **CAA** limita quem pode emitir certificado para o seu domínio.

## Quando é ruim

- **Automação quebrada vira queda:** se a renovação falha em silêncio, o site cai no dia do vencimento. Monitore.
- **Wildcard exige DNS-01** e credencial de API do DNS no servidor, o que aumenta o estrago se o servidor for invadido.
- **ACM só serve dentro da AWS:** não dá para baixar a chave privada de um certificado público para colocar em outro servidor.
- **CAA mal escrito bloqueia a emissão** da própria CA que você usa.

## Validade atual e redução planejada

Conferido em 2026-11-25. O CA/Browser Forum aprovou a ballot SC-081 (proposta pela Apple), que reduz em etapas a validade máxima de certificados públicos:

| A partir de | Validade máxima |
|---|---|
| 15/03/2026 (já em vigor) | 200 dias |
| 15/03/2027 | 100 dias |
| 15/03/2029 | 47 dias |

Let's Encrypt emite certificados de 90 dias por padrão e oferece certificados de 6 dias como opção. A página oficial diz que a validade máxima deles cai para 45 dias até fevereiro de 2028.

Na Cloudflare, o Universal SSL é controlado por ela: Let's Encrypt usa 90 dias; Google Trust Services pode usar 14, 30 ou 90. As CAs listadas pela Cloudflare são Let's Encrypt, Google Trust Services, SSL.com e Sectigo. Um CAA que bloqueia o Google faz a Cloudflare cair para o Let's Encrypt.

A conclusão prática: certificado manual deixa de ser viável. Só use automação (ACME).

## Como começar

Caminho padrão: DNS na Cloudflare, modo de criptografia Full (strict) e certificado de origem no servidor. Detalhes em [Cloudflare na infra](../../infra/docs/08-cloudflare.md).

Registro CAA que autoriza só o Let's Encrypt a emitir para o domínio:

```
clinica-exemplo.com.br.  3600  IN  CAA  0 issue "letsencrypt.org"
clinica-exemplo.com.br.  3600  IN  CAA  0 issuewild "letsencrypt.org"
clinica-exemplo.com.br.  3600  IN  CAA  0 iodef "mailto:ti@clinica-exemplo.com.br"
```

Se usar a Cloudflare Universal SSL junto, inclua também as CAs dela (confira a lista na página oficial de CAs da Cloudflare) ou não publique CAA. Sem CAA, qualquer CA pode emitir.

Certificado wildcard com certbot e DNS-01 pela Cloudflare (o token deve ter só a permissão de editar DNS da zona):

```
certbot certonly --dns-cloudflare --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini -d "*.clinica-exemplo.com.br" -d clinica-exemplo.com.br
```

Para testar a renovação sem emitir de verdade:

```
certbot renew --dry-run
```

Para ver validade e emissor de qualquer site:

```
openssl s_client -connect app.clinica-exemplo.com.br:443 -servername app.clinica-exemplo.com.br </dev/null 2>/dev/null | openssl x509 -noout -issuer -dates
```

No ACM, peça o certificado com validação por DNS e crie o CNAME que o console mostra. Com o CNAME mantido no DNS, a renovação é automática enquanto o certificado estiver em uso por outro serviço da AWS. Confira na página oficial a validade vigente.

Como o DNS-01 funciona: a CA pede que você publique um TXT em `_acme-challenge`. Só quem controla o DNS consegue. Por isso é o único método que emite wildcard.

## Combina com / alternativas

- [DNS, registros e propagação](02-dns-registros-e-propagacao.md): CAA e CNAME de validação são registros DNS.
- [Renovação, segurança e transferência](06-renovacao-seguranca-e-transferencia.md): o domínio vencido também derruba o HTTPS.
- [Cloudflare](../../infra/docs/08-cloudflare.md): certificado automático na borda.
- Alternativa paga: certificado EV/OV de CA comercial, só quando um contrato exigir.

## Decisão rápida

- **Use se:** o sistema tem domínio público; escolha Cloudflare ou Let's Encrypt automático e ACM se estiver na AWS.
- **Evite se:** pretende instalar certificado à mão e anotar a data no calendário; com validade de 200 dias hoje e 47 dias em 2029, isso não se sustenta.
