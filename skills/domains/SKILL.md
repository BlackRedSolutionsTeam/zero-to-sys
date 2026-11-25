---
name: domains
description: Cuida do domínio do sistema do registro até a migração — escolher e registrar (Registro.br para .com.br, registrars para .com, .app, .dev), configurar o DNS (A, AAAA, CNAME, TXT, MX, CAA, TTL), organizar subdomínios por ambiente (app, api, staging, www x apex), publicar o e-mail do domínio (MX, SPF, DKIM, DMARC), manter o HTTPS (certificados e renovação), proteger a conta (auto-renovação, lock, 2FA, titularidade do cliente) e trocar de DNS sem queda. Use sempre que o usuário pedir "registrar domínio", "domínio .com.br", "apontar o domínio", "criar subdomínio", "configurar SPF/DKIM/DMARC", "e-mail caindo no spam", "renovar o domínio", "transferir o domínio" ou "trocar o DNS". Não configura a Cloudflare em si (skill cloudflare), o servidor (skills vps e nginx) nem o envio de e-mail transacional (skill integrations).
---

# domains

Guia para que o domínio nunca seja o motivo de o sistema sair do ar ou de o e-mail cair no spam. Domínio parece detalhe, mas é o único item que, perdido, não se recupera com backup. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e registros prontos para copiar.

## Como usar esta skill

1. **Pergunte se já existe domínio** e em nome de quem está. Se está no CPF do freelancer ou da agência, resolva isso antes de tudo ([doc 06](docs/06-renovacao-seguranca-e-transferencia.md)).
2. **Registre, se ainda não houver** ([doc 01](docs/01-escolher-e-registrar-o-dominio.md)): `.com.br` no Registro.br; `.com`, `.app` e `.dev` num registrar. Titular é sempre o cliente.
3. **Decida onde fica o DNS.** Padrão do plugin: Cloudflare (skill `cloudflare`, doc 01). Configure os registros pelo [doc 02](docs/02-dns-registros-e-propagacao.md).
4. **Organize os subdomínios** por ambiente e defina o endereço canônico, `www` ou apex ([doc 03](docs/03-subdominios-e-ambientes.md)).
5. **Publique o e-mail do domínio:** MX, SPF, DKIM e DMARC, com o transacional num subdomínio separado ([doc 04](docs/04-email-do-dominio-spf-dkim-dmarc.md)).
6. **Garanta o HTTPS** e o registro CAA ([doc 05](docs/05-certificados-e-https.md)).
7. **Proteja a conta:** auto-renovação, lock, 2FA e alerta de expiração ([doc 06](docs/06-renovacao-seguranca-e-transferencia.md)).
8. **Para trocar de provedor ou de servidor**, siga o [doc 07](docs/07-migrar-dns-sem-queda.md) e confira com `dig`.

## Onde registrar e onde deixar o DNS

| Projeto | TLD | Onde registrar | Onde fica o DNS |
|---|---|---|---|
| Empresa ou produto brasileiro | `.com.br` | Registro.br | Cloudflare |
| Produto para fora do Brasil | `.com`, `.app`, `.dev` | Registrar (Cloudflare Registrar, Porkbun, Namecheap…) | Cloudflare |
| Marca que precisa dos dois | `.com.br` e `.com` | Cada um no seu | Cloudflare, com um redirecionando para o canônico |
| Sistema interno | Subdomínio do domínio da empresa | Já registrado | DNS da empresa |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Registrar o domínio | [docs/01-escolher-e-registrar-o-dominio.md](docs/01-escolher-e-registrar-o-dominio.md) | Registro.br, registrars, titularidade, escolher o nome |
| DNS | [docs/02-dns-registros-e-propagacao.md](docs/02-dns-registros-e-propagacao.md) | Registros, TTL, propagação, `dig` |
| Subdomínios e ambientes | [docs/03-subdominios-e-ambientes.md](docs/03-subdominios-e-ambientes.md) | app, api, staging, www x apex |
| E-mail do domínio | [docs/04-email-do-dominio-spf-dkim-dmarc.md](docs/04-email-do-dominio-spf-dkim-dmarc.md) | MX, SPF, DKIM, DMARC |
| Certificados | [docs/05-certificados-e-https.md](docs/05-certificados-e-https.md) | Validade, renovação, wildcard, CAA |
| Renovação e segurança | [docs/06-renovacao-seguranca-e-transferencia.md](docs/06-renovacao-seguranca-e-transferencia.md) | Auto-renovação, lock, 2FA, transferência |
| Migrar DNS | [docs/07-migrar-dns-sem-queda.md](docs/07-migrar-dns-sem-queda.md) | Trocar de provedor sem queda |

## Checklist

- [ ] Domínio registrado em nome do cliente ou da empresa dona do sistema (WHOIS ou painel do registro).
- [ ] Auto-renovação ligada e e-mail de contato atualizado no registrar.
- [ ] 2FA ligado na conta do registrar e na do DNS.
- [ ] Lock de transferência ativo, onde o registrar oferecer.
- [ ] Endereço canônico definido (www ou apex) e o outro redireciona com 301 (`curl -I`).
- [ ] Staging e admin fora do índice do Google (proteção por login ou `noindex`).
- [ ] SPF, DKIM e DMARC publicados e válidos (`dig TXT dominio`, `dig TXT _dmarc.dominio`).
- [ ] Registro CAA publicado para as autoridades usadas (`dig CAA dominio`).
- [ ] HTTPS válido em todos os subdomínios públicos, com renovação automática.
- [ ] Alerta de expiração do domínio e dos certificados.

## Regras de uso

- **O domínio é do cliente.** Registre no CPF ou CNPJ dele, nunca no seu. Domínio no nome errado é o problema mais difícil de desfazer na entrega.
- **Um lugar para o DNS.** Escolha um provedor e mantenha todos os registros lá, documentados.
- **Baixe o TTL antes de mudar.** Mudança de DNS com TTL alto deixa usuários no endereço antigo por horas.
- **Copie todos os registros ao migrar**, inclusive MX e TXT; esquecer o MX derruba o e-mail.
- **DMARC aos poucos.** Comece com `p=none`, leia os relatórios e só depois endureça.
- **E-mail do sistema separado do corporativo.** Um subdomínio para o transacional protege a reputação do domínio principal.
- **Nunca deixe vencer.** Auto-renovação e alerta, sempre; domínio expirado pode ser registrado por outra pessoa.
- **Fronteiras.** Proxy, cache e WAF são da `cloudflare`; o servidor é da `vps` e da `nginx`; o envio de e-mail pelo sistema é da `integrations`.

## Quando a lista não cobre

Registro de marca (INPI), disputas de domínio, DNS próprio em servidor (BIND, PowerDNS), anycast e domínios de país fora do Brasil com regras específicas ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial.

## Validade dos dados

Preços, prazos e regras do Registro.br e dos registrars mudam; foram conferidos em 2026-11-25 quando citados, e cada documento tem a linha "Verificado em". Confira na página oficial antes de afirmar um valor ou prazo ao usuário.
