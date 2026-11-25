# DNS: registros e propagação

> DNS traduz o nome do domínio em endereços e serviços; cada tipo de registro tem uma função e uma mudança leva tempo para valer.

| | |
|---|---|
| **Referência** | developers.cloudflare.com/dns, RFC 1034 e RFC 1035, registro.br |
| **Categoria** | Domínios |
| **Tipo** | Prática de configuração de DNS |
| **Vale para** | Qualquer domínio que aponte para site, API ou e-mail |
| **Verificado em** | 2026-11-25 |

## O que é

DNS (Domain Name System) é a agenda da internet: quando alguém digita `app.clinica-exemplo.com.br`, o DNS responde qual servidor atende. Cada linha da agenda é um **registro**. O conjunto de registros do domínio se chama **zona**, e fica nos **servidores de nome** (nameservers) que o registrar aponta.

O **apex** (ou raiz) é o domínio sem prefixo, `clinica-exemplo.com.br`. Nas ferramentas aparece como `@`.

## Por que usar

- **Trocar de servidor** sem mudar o endereço: basta mudar o registro.
- **Separar serviços** em subdomínios.
- **E-mail e certificados** dependem de registros MX, TXT e CAA.
- **Diagnóstico:** saber ler o DNS resolve metade dos "o site não abre".

## Quando usar

- Ao apontar o domínio para o primeiro deploy.
- Ao configurar e-mail, certificado ou verificação de domínio.
- Ao migrar de hospedagem.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Poucos registros: apex, `www` e e-mail |
| MVP de SaaS | ✅ Ótimo | `app.`, `api.` e verificação de e-mail transacional |
| SaaS em crescimento | ✅ Ótimo | Vários ambientes e subdomínios, com CAA e e-mail |
| Sistema interno/corporativo | 🟡 Serve | Pode usar DNS interno ou subdomínio já existente |
| API/integração | ✅ Ótimo | `api.` com A ou CNAME e TTL curto no começo |
| App mobile com backend | 🟡 Serve | Só a API e links do app precisam de registro |
| Servidor sem nome, só por IP | ❌ Evite | Sem DNS, não há HTTPS válido nem troca fácil de servidor |

## Quando é bom

- **Cloudflare como DNS:** painel simples e, conferido em 2026-11-25, o CNAME flattening permite CNAME no apex.
- **Registros claros e documentados** na zona.
- **TTL baixo antes de mudar** deixa a troca rápida.

## Quando é ruim

- **CNAME no apex em DNS comum:** o padrão do DNS não permite, e quebra o e-mail do domínio.
- **TTL alto na hora da migração:** o endereço antigo continua valendo por horas.
- **Apagar registros sem copiar:** MX e TXT esquecidos derrubam o e-mail.
- **DNS espalhado em vários painéis:** ninguém sabe onde mudar.

## Como começar

### Tipos de registro

| Tipo | Para que serve | Exemplo |
|---|---|---|
| A | Aponta um nome para um IPv4 | `api` para `203.0.113.10` |
| AAAA | Aponta um nome para um IPv6 | `api` para `2001:db8::10` |
| CNAME | Apelido: aponta um nome para outro nome | `app` para `cname.provedor.example` |
| ALIAS/ANAME/flattening | Faz o papel de CNAME no apex | `@` para `provedor.example` |
| TXT | Texto livre: verificação de domínio, SPF, DKIM, DMARC | `"v=spf1 ..."` |
| MX | Servidor que recebe o e-mail do domínio | prioridade `10` e `mx.provedor.example` |
| CAA | Quais autoridades podem emitir certificado | `0 issue "letsencrypt.org"` |

Conferido em 2026-11-25 na documentação da Cloudflare: CNAME proxied precisa terminar em um host com A ou AAAA; o CNAME flattening devolve o IP final no lugar do CNAME, o que permite um CNAME no apex; o TTL "Auto" de registros proxied equivale a 300 segundos. O flattening pode quebrar verificação de domínio de terceiros quando ativado para todos os CNAMEs, pois o CNAME deixa de ser devolvido.

### Zona de exemplo da clínica

Valores com IPs de documentação (RFC 5737) e nomes fictícios:

```
@         A      203.0.113.10
www       CNAME  clinica-exemplo.com.br
app       A      203.0.113.10
api       A      203.0.113.20
staging   A      203.0.113.30
@         MX     10 mx.provedor-de-email.example
@         TXT    "v=spf1 include:_spf.provedor-de-email.example ~all"
@         CAA    0 issue "letsencrypt.org"
```

Os valores reais de MX e SPF vêm do provedor de e-mail. O doc de e-mail do domínio detalha SPF, DKIM e DMARC.

### Onde fica o DNS

O DNS fica nos servidores de nome informados no registrar. Há três lugares comuns:

- **No registrar** (Registro.br, por exemplo): serve para o básico.
- **Na Cloudflare** (padrão do plugin): você troca os nameservers no registrar e passa a editar tudo lá. Veja [../../infra/docs/08-cloudflare.md](../../infra/docs/08-cloudflare.md).
- **No provedor de nuvem:** bom quando tudo vive nele; cria dependência.

Mudar os nameservers move a zona inteira. Copie todos os registros antes.

### TTL e propagação

**TTL** (time to live) é o tempo, em segundos, que os resolvedores guardam a resposta. TTL de 3600 significa até uma hora com o valor antigo. **Propagação** é essa espera até todo mundo enxergar o valor novo. Não é um envio: é o cache expirando.

- Antes de uma mudança planejada, baixe o TTL (300 segundos) e espere o TTL antigo passar.
- Depois de estável, suba o TTL.
- Troca de nameservers pode levar mais tempo, pois depende do TTL do registro de delegação no TLD.

### Conferir com dig

`dig` é a ferramenta de linha de comando que consulta o DNS.

```
dig api.clinica-exemplo.com.br A +short
dig clinica-exemplo.com.br MX +short
dig clinica-exemplo.com.br TXT +short
dig clinica-exemplo.com.br CAA +short
dig clinica-exemplo.com.br NS +short
dig @1.1.1.1 api.clinica-exemplo.com.br A +short
dig @ns-do-provedor.example api.clinica-exemplo.com.br A
```

A última consulta vai direto ao servidor autoritativo e mostra o valor atual, sem cache. Compare com a de `@1.1.1.1` para saber se falta só propagar.

## Combina com / alternativas

- **Escolher e registrar:** [01-escolher-e-registrar-o-dominio.md](01-escolher-e-registrar-o-dominio.md).
- **Cloudflare:** [../../infra/docs/08-cloudflare.md](../../infra/docs/08-cloudflare.md).
- **E-mail transacional:** [../../integrations/docs/02-email-transacional.md](../../integrations/docs/02-email-transacional.md).
- **Alternativa:** DNS no próprio registrar, quando o projeto é pequeno e sem proxy.

## Decisão rápida

- **Use se:** o domínio atende serviços reais e você precisa trocar de servidor ou configurar e-mail sem dor.
- **Evite se:** o sistema roda só em rede interna sem nome público; use o DNS da rede.
