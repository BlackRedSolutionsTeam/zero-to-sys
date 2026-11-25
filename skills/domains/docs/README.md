# Domínios

Um documento por tópico, do registro do domínio até a migração de DNS. Preços e prazos foram conferidos em 2026-11-25.

## Ter o domínio

| Prática | O que entrega | Doc |
|---|---|---|
| Registrar o domínio | Registro.br, registrars, titularidade | [01-escolher-e-registrar-o-dominio.md](01-escolher-e-registrar-o-dominio.md) |
| Renovação e segurança | Auto-renovação, lock, 2FA, transferência | [06-renovacao-seguranca-e-transferencia.md](06-renovacao-seguranca-e-transferencia.md) |

## Configurar

| Prática | O que entrega | Doc |
|---|---|---|
| DNS | Registros, TTL e propagação | [02-dns-registros-e-propagacao.md](02-dns-registros-e-propagacao.md) |
| Subdomínios e ambientes | app, api, staging, www x apex | [03-subdominios-e-ambientes.md](03-subdominios-e-ambientes.md) |
| E-mail do domínio | MX, SPF, DKIM, DMARC | [04-email-do-dominio-spf-dkim-dmarc.md](04-email-do-dominio-spf-dkim-dmarc.md) |
| Certificados | HTTPS, renovação, CAA | [05-certificados-e-https.md](05-certificados-e-https.md) |

## Mudar

| Prática | O que entrega | Doc |
|---|---|---|
| Migrar DNS | Trocar de provedor sem queda | [07-migrar-dns-sem-queda.md](07-migrar-dns-sem-queda.md) |

## Por onde começar

- **Sistema novo:** 01 → 02 → 03 → 04 → 05, e o 06 antes de entregar ao cliente.
- **E-mail caindo no spam:** 04.
- **Trocar de DNS ou de servidor:** 07.
- **Entregar o projeto ao cliente:** 06 (transferir a titularidade).
