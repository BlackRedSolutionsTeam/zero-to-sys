# DNS e proxy

> Deixe laranja (proxied) só o que é tráfego web em A, AAAA e CNAME; e-mail, SSH e verificações ficam cinza (só DNS).

| | |
|---|---|
| **Referência** | developers.cloudflare.com (Proxy status, CNAME flattening, HTTP headers, Network ports, WebSockets, Connection limits) |
| **Categoria** | Borda |
| **Tipo** | Prática de configuração de DNS e proxy |
| **Vale para** | Qualquer zona na Cloudflare; exemplos com clinica-exemplo.com.br |
| **Verificado em** | 2026-11-25 |

## O que é

Cada registro A, AAAA ou CNAME tem um **proxy status** (estado do proxy):

- **Proxied (nuvem laranja):** o DNS responde com IPs da Cloudflare, o visitante fala com ela, e ela repassa à sua origem. Cache, WAF e DDoS só valem aqui.
- **DNS only (nuvem cinza):** o DNS devolve o IP real do seu servidor e a Cloudflare não toca no tráfego.

Segundo a documentação, só A, AAAA e CNAME podem ser proxied. Os outros tipos são sempre só DNS.

## Por que usar

- **Esconde a origem:** com laranja, quem consulta o DNS não vê o IP do servidor.
- **Proteção e cache** só existem no tráfego que passa pelo proxy.
- **Menos erro:** regra clara por tipo evita quebrar e-mail e SSH.

## Quando usar

- Ao criar qualquer registro novo.
- Ao investigar "o site abre sem a Cloudflare e dá erro com ela" (ou o contrário).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Apex e `www` laranja, cache ligado |
| MVP de SaaS | ✅ Ótimo | `app` e `api` laranja, e-mail cinza |
| SaaS em crescimento | ✅ Ótimo | Proxy com regras por host |
| Sistema interno/corporativo | 🟡 Serve | Painel interno melhor atrás de Tunnel ou Access |
| API/integração | ✅ Ótimo | Limite e WAF na frente; atenção ao timeout |
| App mobile com backend | ✅ Ótimo | API laranja; sem cache de resposta logada |
| Servidor de e-mail ou SSH no mesmo nome do site | ❌ Evite | Tráfego não web não passa pelo proxy; use um nome cinza separado |

## Quando é bom

- **Registro por função:** `app`, `api` e `staging` laranja; `mail`, `ssh` e verificações cinza.
- **TTL (tempo de vida do cache do DNS):** registros proxied têm TTL fixo Auto de 300 segundos, que não se edita (documentação).

## Quando é ruim

- **MX e TXT** nunca são proxied. SPF, DKIM e DMARC são TXT: ficam como estão.
- **Registro cinza expõe o IP.** Se `ssh.clinica-exemplo.com.br` é cinza e aponta para o mesmo IP do site, o atacante acha a origem. Use [proteção da origem](06-tunnel-e-protecao-da-origem.md).
- **CNAME de verificação de domínio** (Google, provedor de e-mail) não deve ser proxied, diz a documentação.
- **Vários A com o mesmo nome:** se um for proxied, todos são tratados como proxied.
- **Certificado da origem** precisa ser válido com o proxy ligado; veja [SSL/TLS e HSTS](03-ssl-tls-e-hsts.md).

## Como começar

**Tabela de decisão**

| Registro | Exemplo | Proxy |
|---|---|---|
| A, apex | `clinica-exemplo.com.br` | Laranja |
| CNAME `www` | `www` para o apex | Laranja |
| A `app` | IP do servidor | Laranja |
| A `api` | IP do servidor | Laranja |
| A `staging` | IP do staging | Laranja (proteja com Access) |
| MX | `mail` do provedor | Só DNS (sempre) |
| TXT (SPF, DKIM, DMARC) | `v=spf1 ...` | Só DNS (sempre) |
| A `ssh` ou `db` | IP do servidor | Cinza, e feche a porta para o mundo |
| CNAME de verificação | `_dominio` do provedor | Cinza |

**Criar registro pela API**

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"api","content":"203.0.113.10","proxied":true,"ttl":1}'
```

`ttl` igual a 1 significa Auto. O IP 203.0.113.10 é de documentação, troque pelo seu.

**CNAME flattening**

CNAME não pode ficar no apex pelo DNS padrão. A Cloudflare resolve isso: ela busca o IP final do alvo e devolve esse IP no lugar do CNAME. Conferido: no apex isso é automático em todos os planos. A opção de "achatar todos os CNAMEs" é de planos pagos; no Free vale só o apex. Ativar para todos pode quebrar verificação de domínio de terceiros, e CNAME para outra conta Cloudflare gera o erro 1014.

**IP real do visitante**

Com proxy, o IP que chega na origem é o da Cloudflare. O IP do visitante vem no cabeçalho `CF-Connecting-IP`, enviado só entre a Cloudflare e a origem. A documentação recomenda esse cabeçalho (ou `True-Client-IP`, exclusivo do Enterprise) em vez de `X-Forwarded-For`, que acumula vários IPs.

Regra de segurança: só confie em `CF-Connecting-IP` se a origem aceitar conexões apenas da Cloudflare; senão qualquer um envia o cabeçalho falso. Isso vale também para o [rate limit](../../security/docs/06-rate-limit.md). A configuração no servidor está em [nginx atrás da Cloudflare](../../nginx/docs/05-atras-da-cloudflare.md).

**Portas que o proxy aceita**

Conferido em 2026-11-25 (developers.cloudflare.com/fundamentals/reference/network-ports):

| Protocolo | Portas |
|---|---|
| HTTP | 80, 8080, 8880, 2052, 2082, 2086, 2095 |
| HTTPS | 443, 2053, 2083, 2087, 2096, 8443 |

Qualquer outra porta não é proxied; a documentação cita o SSH (porta 22), que precisa de registro cinza ou do produto Spectrum.

**WebSocket**

Conferido: WebSocket funciona em todos os planos, mas a documentação manda confirmar que a opção WebSockets está ligada em Network nas configurações da zona. O WAF inspeciona só a requisição inicial de upgrade. A Cloudflare fecha conexões sem dados por um tempo; envie ping e pong a cada poucos segundos e reconecte no cliente. O tempo exato de ociosidade não foi conferido. Limites de proxy até a origem: leitura de 125 s (erro 524) e conexão de 19 s (erro 522); a página não confirmou o "100 s" que circula por aí.

## Combina com / alternativas

- [Colocar o domínio na Cloudflare](01-colocar-o-dominio-na-cloudflare.md) e [Cloudflare na infra](../../infra/docs/08-cloudflare.md).
- [E-mail transacional](../../integrations/docs/02-email-transacional.md): registros MX e TXT ficam cinza.
- [DNS, registros e propagação](../../domains/docs/02-dns-registros-e-propagacao.md).
- Alternativa para SSH e bancos: Tunnel ou VPN, sem registro público.

## Decisão rápida

- **Use se:** o registro é A, AAAA ou CNAME que serve site ou API por HTTP/HTTPS em porta suportada.
- **Evite se:** o tráfego não é web (SSH, banco, e-mail) ou a porta não está na lista; deixe cinza e proteja de outro jeito.
