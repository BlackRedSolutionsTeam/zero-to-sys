# Escolha do login

> Escolha o método de login pelo público do sistema, use uma biblioteca ou serviço de identidade em vez de escrever autenticação própria e nunca invente criptografia de senha.

| | |
|---|---|
| **Referência** | OWASP Authentication Cheat Sheet e Password Storage Cheat Sheet (cheatsheetseries.owasp.org); OpenID Connect Core 1.0 (openid.net); W3C WebAuthn (passkeys); documentação oficial do Better Auth, Auth.js, ASP.NET Core Identity, Django, Laravel Fortify, Spring Security, Supabase Auth e Keycloak |
| **Categoria** | Segurança |
| **Tipo** | Prática de decisão de autenticação |
| **Vale para** | Better Auth, Auth.js, ASP.NET Core Identity, Django auth, Laravel (Fortify), Spring Security, Supabase Auth, Keycloak |
| **Verificado em** | 2026-11-24 |

## O que é

Autenticação responde "quem é você?". O login é a forma de provar isso. As formas mais comuns:

- **E-mail e senha:** o usuário cria uma senha e o sistema guarda uma versão protegida dela.
- **Link mágico:** o sistema manda um link de uso único por e-mail; clicar nele faz o login.
- **Login social:** "Entrar com Google". O Google confirma quem é a pessoa (protocolo OpenID Connect, OIDC).
- **Passkey:** o login usa chave criptográfica guardada no aparelho (WebAuthn), com biometria ou PIN. Não há senha para vazar.
- **SSO da empresa:** a empresa cliente já tem um cadastro central de pessoas (Entra ID, Okta, Google Workspace). Seu sistema confia nele via OIDC ou SAML (um protocolo mais antigo, baseado em XML).

Exemplo do guia: sistema de agendamento de clínica, com pacientes, profissionais e agendamentos.

## Por que usar

- **Menos risco:** quem não guarda senha não vaza senha.
- **Menos suporte:** link mágico e login social reduzem o "esqueci minha senha".
- **Venda para empresas:** clientes grandes exigem SSO.
- **Menos código seu para errar:** autenticação tem muitos detalhes (tempo constante, tokens de uso único, bloqueio).

## Quando usar

- Ao começar o projeto, antes de criar a tabela de usuários.
- Ao receber o primeiro cliente corporativo que pede SSO.
- Ao ver que o suporte vive resetando senha.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Quase sempre não precisa de login; se precisar, social ou link mágico bastam |
| MVP de SaaS | ✅ Ótimo | E-mail e senha mais Google, com biblioteca pronta, em um dia |
| SaaS em crescimento | ✅ Ótimo | Acrescente passkey e SSO por plano; considere serviço de identidade |
| Sistema interno/corporativo | ✅ Ótimo | SSO via OIDC ou SAML evita senha nova para o funcionário |
| API/integração | 🟡 Serve | O "login" é chave de API ou OAuth entre sistemas, não usuário digitando senha |
| App mobile | ✅ Ótimo | Login social e passkey têm ótima experiência no celular |
| Qualquer um com autenticação escrita à mão | ❌ Evite | Hash caseiro e token caseiro são a causa clássica de vazamento |

## Quando é bom

- **E-mail e senha:** todo mundo entende, funciona sem terceiros. Exige recuperação e 2FA (veja [03-recuperacao-e-2fa.md](03-recuperacao-e-2fa.md)).
- **Link mágico:** bom para público leigo, como o paciente da clínica que entra uma vez por mês. A segurança é a do e-mail dele.
- **Login social:** conversão alta. Ofereça só se o público tem conta Google.
- **Passkey:** o método mais resistente a phishing. Ofereça junto com outro, não no lugar, no começo.
- **SSO:** obrigatório para clientes corporativos; cobre desligamento (a pessoa sai da empresa e perde o acesso).

| Público | Comece com |
|---|---|
| Pacientes (leigos) | Link mágico ou Google |
| Profissionais da clínica | E-mail e senha, mais 2FA |
| Administradores | E-mail e senha com 2FA obrigatório, ou SSO |
| Cliente corporativo | SSO (OIDC ou SAML) |

## Quando é ruim

- **Só login social:** quem não tem conta Google fica de fora.
- **Link mágico sem limite de uso e validade curta:** vira senha eterna na caixa de entrada.
- **SAML escrito à mão:** use biblioteca ou serviço; XML assinado tem muitos ataques conhecidos.
- **Serviço de identidade sem plano de saída:** confira exportação de usuários antes de depender dele.

## Como começar

### Regra de ouro

Nunca escreva criptografia de senha própria. Não use MD5, SHA-1 ou SHA-256 puro para senha, nem "sal" feito à mão. Use o que a biblioteca de auth já faz, ou uma função de senha aprovada.

### Armazenamento de senha (OWASP Password Storage Cheat Sheet)

| Algoritmo | Parâmetros mínimos da OWASP |
|---|---|
| **Argon2id** (preferido) | memória 19 MiB (m=19456), 2 iterações (t=2), paralelismo 1 (p=1) |
| scrypt (sem Argon2id) | N=2^17, r=8, p=1 |
| bcrypt (sistema legado) | fator de custo 10 ou mais; limite de 72 bytes na senha |
| PBKDF2 (exigência FIPS-140) | HMAC-SHA-256 com 600.000 iterações |

O hash resultante guarda algoritmo, parâmetros e sal juntos, o que permite aumentar o custo depois e rehashar no próximo login.

```typescript
import { hash, verify } from "@node-rs/argon2";

const opcoes = { memoryCost: 19456, timeCost: 2, parallelism: 1 };

export const gerarHash = (senha: string) => hash(senha, opcoes);
export const conferir = (guardado: string, senha: string) => verify(guardado, senha);
```

Só escreva isso se a biblioteca de auth não fizer por você. Na maioria dos casos, ela já faz.

### Build ou buy: biblioteca ou serviço

- **Biblioteca na sua aplicação:** os usuários ficam no seu banco. Você controla tudo e não paga por usuário.
- **Serviço de identidade:** outro sistema guarda usuários e faz o login. Menos trabalho, mas há dependência e limites do plano.

| Stack | Opção | Observação conferida |
|---|---|---|
| TypeScript | Better Auth | Biblioteca "agnóstica de framework" com 2FA, passkeys, multi-tenant e SSO por plugins |
| TypeScript (Next.js) | Auth.js | Em 22/09/2025 o time anunciou que a manutenção passou ao time do Better Auth; quem usa continua usando, com correções de segurança e urgentes. Em projeto novo, prefira Better Auth |
| .NET | ASP.NET Core Identity | Parte do framework; senha, 2FA e bloqueio inclusos |
| Python | Django auth | Embutido; hash de senha configurável |
| PHP | Laravel Fortify | Os starter kits atuais do Laravel usam Fortify (login, cadastro, reset, 2FA por TOTP). A variante com WorkOS AuthKit oferece social, passkey, link mágico e SSO |
| Java | Spring Security | Padrão do ecossistema; OIDC e SAML via módulos |
| Qualquer | Supabase Auth | Serviço; plano Free com 50.000 usuários ativos por mês; projetos Free pausam após 1 semana sem atividade |
| Qualquer | Keycloak (self-host) | Open source, projeto incubado da CNCF; OIDC, OAuth 2.0 e SAML 2.0; você opera o servidor |
| Qualquer | Clerk | Plano Hobby com 50.000 usuários retidos por mês, mas sem MFA, passkeys e SSO nesse plano |

Escolha a biblioteca na skill `stacks` e siga a dela. Não misture duas.

## Combina com / alternativas

- [02-sessao-e-tokens.md](02-sessao-e-tokens.md): o que acontece depois do login.
- [03-recuperacao-e-2fa.md](03-recuperacao-e-2fa.md): recuperar conta e segundo fator.
- [04-papeis-e-permissoes.md](04-papeis-e-permissoes.md): o que cada pessoa pode fazer.
- [06-rate-limit.md](06-rate-limit.md): limitar tentativas de login.
- `../../stacks/docs/README.md`: biblioteca de auth por stack.
- `../../data/docs/10-dados-pessoais-e-lgpd.md`: e-mail e senha são dados pessoais.

## Decisão rápida

- **Use se:** quer login seguro rápido, com biblioteca madura e o método certo para cada público.
- **Evite se:** pretende escrever o próprio hash, token ou fluxo de SAML.
