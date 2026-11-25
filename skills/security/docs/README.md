# Segurança

Um documento por prática, explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com exemplos prontos. Aqui vai a segurança no nível da aplicação; rede, TLS, WAF e segredos do ambiente ficam na skill `infra`. Padrões e versões foram conferidos em 2026-11-24.

## Quem entra

| Prática | O que entrega | Doc |
|---|---|---|
| Escolha do login | Senha, link mágico, social, passkeys, SSO | [01-escolha-do-login.md](01-escolha-do-login.md) |
| Sessão e tokens | Cookie, JWT, expiração e revogação | [02-sessao-e-tokens.md](02-sessao-e-tokens.md) |
| Recuperação e 2FA | Recuperar conta e segundo fator | [03-recuperacao-e-2fa.md](03-recuperacao-e-2fa.md) |

## O que cada um pode fazer

| Prática | O que entrega | Doc |
|---|---|---|
| Papéis e permissões | Autorização no servidor, RBAC, ownership | [04-papeis-e-permissoes.md](04-papeis-e-permissoes.md) |

## Proteger o código

| Prática | O que entrega | Doc |
|---|---|---|
| OWASP no código | Ataques comuns e a defesa de cada um | [05-owasp-no-codigo.md](05-owasp-no-codigo.md) |
| Rate limit | Limitar tentativas e abuso | [06-rate-limit.md](06-rate-limit.md) |
| Upload de arquivos | Receber arquivo sem abrir brecha | [07-upload-de-arquivos.md](07-upload-de-arquivos.md) |
| Dependências vulneráveis | Auditar e atualizar pacotes | [08-dependencias-vulneraveis.md](08-dependencias-vulneraveis.md) |

## Lei

| Prática | O que entrega | Doc |
|---|---|---|
| LGPD na prática | Consentimento, exportar e apagar dados | [09-lgpd-na-pratica.md](09-lgpd-na-pratica.md) |

## Por onde começar

- **Sistema novo:** 01 → 02 → 04 antes da primeira rota protegida; 05 como checklist; 03, 06 e 08 antes de ir para produção.
- **Sistema com dado pessoal:** 09 e o doc de LGPD da skill `data`.
- **Vão receber arquivo:** 07.
- **Alguém acessou dado de outra empresa:** 04 e o isolamento da skill `data`.
- **Muitas tentativas de login:** 06 e 03.
