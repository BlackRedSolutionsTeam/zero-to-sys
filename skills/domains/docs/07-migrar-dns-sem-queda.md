# Migrar o DNS sem queda

> Baixe o TTL, copie todos os registros, troque os nameservers, confira com dig e só então suba o TTL.

| | |
|---|---|
| **Referência** | developers.cloudflare.com/dns, RFC 1034 e RFC 2181 (TTL), registro.br (troca de servidores DNS) |
| **Categoria** | Domínios |
| **Tipo** | Prática de migração |
| **Vale para** | Mudança de DNS entre registrar, Cloudflare e provedor de nuvem |
| **Verificado em** | 2026-11-25 |

## O que é

Migrar o DNS é mudar quem responde pelos registros do domínio, por exemplo do registrar para a Cloudflare. Sem cuidado, e-mail para de chegar e o site some por horas.

Termos: **nameserver** é o servidor que responde o DNS do domínio. **TTL** (time to live) é o tempo, em segundos, que os resolvedores guardam uma resposta antes de perguntar de novo. **Propagação** é esse tempo de espera até todo mundo ver o valor novo.

O princípio: o servidor novo já deve responder tudo igual ao antigo **antes** de você trocar os nameservers. Assim, quem ainda consulta o antigo e quem já consulta o novo recebe a mesma resposta.

## Por que usar

- **Zero queda** em site, API e e-mail.
- **Reversão fácil:** com TTL baixo, voltar atrás leva minutos.
- **Registro esquecido vira incidente:** MX e TXT perdidos fazem o e-mail cair no spam ou sumir.

## Quando usar

- Ao levar o DNS para a Cloudflare.
- Ao sair de um provedor de hospedagem antigo.
- Ao trocar de registrar, quando os nameservers mudam junto.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Poucos registros; migração rápida |
| MVP de SaaS | ✅ Ótimo | Melhor fazer cedo, com poucos registros |
| SaaS em crescimento | ✅ Ótimo | Muitos subdomínios e e-mail; o roteiro evita surpresa |
| Sistema interno/corporativo | ✅ Ótimo | E-mail corporativo depende de MX, SPF, DKIM e DMARC |
| API/integração | ✅ Ótimo | Clientes têm a URL gravada; queda quebra integrações |
| App mobile com backend | ✅ Ótimo | Não dá para forçar o usuário a atualizar a URL |
| Migrar sem listar os registros antes | ❌ Evite | A causa mais comum de e-mail perdido |

## Quando é bom

- **Preparado com antecedência**, a troca em si dura minutos.
- **TTL baixo** deixa o rollback rápido.
- **Comparar os dois servidores** com `dig` prova que nada ficou para trás.

## Quando é ruim

- **Pressa:** o TTL antigo precisa expirar antes. Se estava em 86400 (24 horas), baixe com um dia de antecedência.
- **DNSSEC ativo** no domínio: remova o registro DS no registrar antes de trocar os nameservers, senão alguns resolvedores deixam de resolver.
- **Importação automática incompleta:** painéis que varrem o DNS atual podem perder registros (TXT de verificação, subdomínios sem uso aparente).
- **Registros proxied da Cloudflare** escondem o IP real; confira que a origem aceita o tráfego da borda.

## Como começar

Roteiro com datas relativas ao dia da troca:

1. **D-2:** liste todos os registros do DNS atual. Baixe o TTL de todos para 300 segundos (5 minutos).
2. **D-1:** crie a zona no destino e recrie cada registro: A, AAAA, CNAME, MX, TXT (SPF, DKIM, DMARC, verificações), CAA, SRV. Não esqueça subdomínios como `app`, `api`, `staging`, `mail`.
3. **D-1:** compare origem e destino consultando o servidor novo direto.
4. **Dia D:** troque os nameservers no registrar (no Registro.br, no painel do domínio, em DNS). Remova antes o DS se houver DNSSEC.
5. **Dia D:** acompanhe com `dig`, teste site, API e envio e recebimento de e-mail.
6. **D+2 em diante:** com tudo estável, suba o TTL para 3600 ou mais e religue o DNSSEC, se usava.
7. **D+7:** só então apague a zona antiga.

Listar os registros do DNS atual (muitos provedores bloqueiam transferência de zona, então consulte um por um):

```
for t in A AAAA CNAME MX TXT NS CAA SOA; do dig +noall +answer clinica-exemplo.com.br $t; done
dig +noall +answer _dmarc.clinica-exemplo.com.br TXT
dig +noall +answer app.clinica-exemplo.com.br
dig +noall +answer api.clinica-exemplo.com.br
dig +noall +answer staging.clinica-exemplo.com.br
```

Consultar direto o servidor novo, antes da troca (use o nameserver que o destino informou):

```
dig @anna.ns.cloudflare.com clinica-exemplo.com.br MX +short
dig @anna.ns.cloudflare.com app.clinica-exemplo.com.br A +short
```

Conferir os nameservers que o mundo enxerga depois da troca:

```
dig clinica-exemplo.com.br NS +short
dig @8.8.8.8 clinica-exemplo.com.br NS +short
dig @1.1.1.1 clinica-exemplo.com.br NS +short
```

Para e-mail, depois da troca, envie e receba uma mensagem de teste e veja o cabeçalho em busca de SPF, DKIM e DMARC com resultado `pass`.

Checklist final:

- [ ] TTL baixo antes da troca e respeitado o tempo do TTL antigo.
- [ ] Todos os tipos de registro copiados, inclusive MX e TXT.
- [ ] Comparação com `dig` entre antigo e novo sem diferença.
- [ ] DNSSEC removido antes e religado depois.
- [ ] Nameservers trocados e vistos em mais de um resolvedor público.
- [ ] Site, API, painel e e-mail testados.
- [ ] TTL alto restaurado e zona antiga mantida alguns dias.

## Combina com / alternativas

- [DNS, registros e propagação](02-dns-registros-e-propagacao.md): como cada tipo de registro funciona.
- [E-mail do domínio](04-email-do-dominio-spf-dkim-dmarc.md): o que não pode se perder na cópia.
- [Renovação, segurança e transferência](06-renovacao-seguranca-e-transferencia.md): DNSSEC e lock na troca de registrar.
- [Cloudflare na infra](../../infra/docs/08-cloudflare.md): destino mais comum da migração.
- Alternativa: manter o DNS onde está e só apontar os registros novos, quando a mudança é pequena.

## Decisão rápida

- **Use se:** o domínio já está em produção com site, API ou e-mail em uso.
- **Evite se:** o domínio é novo e sem nenhum serviço ativo; nesse caso, troque os nameservers direto.
