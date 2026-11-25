# Sessão e tokens

> Depois do login, mantenha o usuário logado com sessão no servidor e cookie seguro; use JWT só quando houver motivo, com vida curta, e nunca no localStorage.

| | |
|---|---|
| **Referência** | OWASP Session Management Cheat Sheet e Cross-Site Request Forgery Prevention Cheat Sheet (cheatsheetseries.owasp.org); RFC 6265bis (cookies, SameSite); RFC 7519 (JWT); documentação oficial da biblioteca de auth de cada stack |
| **Categoria** | Segurança |
| **Tipo** | Prática de gestão de sessão |
| **Vale para** | Qualquer stack web com login; exemplo em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

O HTTP não lembra quem você é entre uma requisição e outra. A **sessão** resolve isso: depois do login o sistema entrega ao navegador um identificador, e o navegador o devolve a cada requisição.

Há duas formas:

- **Sessão no servidor:** o identificador é um valor aleatório num cookie. O servidor guarda os dados (quem é, quando entrou) no banco ou no Redis.
- **Token autocontido (JWT):** o próprio token carrega os dados e uma assinatura. O servidor confere a assinatura sem consultar nada.

Exemplo do guia: o profissional da clínica entra no sistema de agendamento e fica logado durante o expediente.

## Por que usar

- **Controle:** com sessão no servidor, você encerra qualquer sessão na hora.
- **Menos superfície:** cookie `HttpOnly` não é lido por JavaScript, então XSS (script malicioso na página) não rouba a sessão.
- **Simplicidade:** o navegador cuida do cookie sozinho.

## Quando usar

- Sempre que o sistema tem login.
- Ao decidir entre cookie e JWT: o padrão é sessão no servidor com cookie.
- JWT quando há vários serviços que precisam validar sem consultar um banco central, ou API consumida por app mobile.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Só se houver área logada |
| MVP de SaaS | ✅ Ótimo | Sessão em cookie, vinda da biblioteca de auth, sem código seu |
| SaaS em crescimento | ✅ Ótimo | Sessão com armazenamento central permite "sair de todos os aparelhos" |
| Sistema interno/corporativo | ✅ Ótimo | Expiração por inatividade exigida por política |
| API/integração | 🟡 Serve | Token de curta duração ou chave de API; sem cookie |
| App mobile | 🟡 Serve | Token com refresh guardado no cofre do aparelho (Keychain, Keystore) |
| Qualquer um com JWT de 30 dias no localStorage | ❌ Evite | Qualquer XSS rouba o token e não há como revogar |

## Quando é bom

- **Cookie de sessão com os atributos certos** (OWASP):
  - `HttpOnly`: JavaScript não lê.
  - `Secure`: só trafega por HTTPS.
  - `SameSite=Lax` ou `Strict`: o navegador não envia o cookie em pedidos vindos de outros sites. A OWASP prefere `Strict`.
  - Prefixo `__Host-`: o cookie exige `Secure`, `Path=/` e nenhum `Domain`, e não pode ser sobrescrito por subdomínio.
- **Identificador aleatório:** gerado por gerador criptográfico, com pelo menos 128 bits recomendados para tokens próprios. Nunca derive do ID do usuário.
- **Dois prazos, ambos conferidos no servidor:**
  - por inatividade: a OWASP cita 2 a 5 minutos para alto valor e 15 a 30 para baixo risco;
  - absoluto: vida máxima, mesmo com uso contínuo.
- **Renovar o identificador no login** e a cada mudança de privilégio. Isso impede fixação de sessão (o atacante planta um ID e espera você logar).
- **Logout de verdade:** invalide no servidor. Apagar só o cookie não impede quem copiou o valor.
- **Sair de todos os aparelhos:** apague todas as sessões do usuário. Faça isso também ao trocar a senha.
- **JWT com vida curta (minutos) mais refresh token** com rotação, que pode ser revogado no servidor.

## Quando é ruim

- **JWT no localStorage ou sessionStorage:** qualquer script da página lê. Prefira cookie `HttpOnly`.
- **JWT longo sem revogação:** token roubado vale até expirar. "Logout" vira só apagar do navegador.
- **Dados sensíveis dentro do JWT:** ele é assinado, não é secreto; qualquer um decodifica o conteúdo.
- **Aceitar `alg: none` ou escolher o algoritmo pelo token:** fixe o algoritmo esperado na verificação.
- **Cookie sem `SameSite`** e sem proteção CSRF.
- **Sessão sem prazo:** vale para sempre.

## Como começar

### Cookie de sessão

```typescript
import { serialize } from "cookie";
import { randomBytes } from "node:crypto";

export function novaSessao() {
  const id = randomBytes(32).toString("base64url");
  const cookie = serialize("__Host-sessao", id, {
    httpOnly: true,
    secure: true,
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 8,
  });
  return { id, cookie };
}
```

### Tabela de sessões (expiração e revogação)

```sql
create table sessoes (
  id_hash text primary key,
  usuario_id uuid not null references usuarios (id),
  criada_em timestamptz not null default now(),
  ultimo_uso_em timestamptz not null default now(),
  expira_em timestamptz not null
);

create index on sessoes (usuario_id);
```

Guarde o hash do identificador, não o valor puro: se o banco vazar, as sessões não servem.

```typescript
const INATIVIDADE_MS = 30 * 60 * 1000;

export function sessaoValida(s: { ultimoUsoEm: Date; expiraEm: Date }, agora = new Date()) {
  const inativa = agora.getTime() - s.ultimoUsoEm.getTime() > INATIVIDADE_MS;
  return !inativa && agora < s.expiraEm;
}
```

Sair de todos os aparelhos: `delete from sessoes where usuario_id = $1`.

### JWT, quando for necessário

```typescript
import { SignJWT, jwtVerify } from "jose";

const segredo = new TextEncoder().encode(process.env.JWT_SEGREDO);

export const emitir = (usuarioId: string) =>
  new SignJWT({}).setProtectedHeader({ alg: "HS256" }).setSubject(usuarioId).setExpirationTime("10m").sign(segredo);

export const verificar = (token: string) => jwtVerify(token, segredo, { algorithms: ["HS256"] });
```

O segredo vem do ambiente (veja `../../infra/docs/09-segredos-e-configuracao.md`).

### CSRF e SameSite

CSRF é quando outro site faz o navegador do usuário enviar um pedido ao seu sistema, com o cookie junto. Defesas, segundo a OWASP:

- **Token anti-CSRF** (synchronizer token): valor imprevisível, conferido em todo pedido que altera dados. É a defesa recomendada para sistemas com estado.
- **Origin e Sec-Fetch-Site:** rejeite pedidos POST, PUT, PATCH e DELETE vindos de outro site.
- **SameSite:** camada extra, não defesa única. `Lax` ainda envia o cookie em navegações GET de outro site, então nunca altere dados em GET.

SameSite sozinho só basta se tudo isto for verdade: nenhum subdomínio fora do seu controle, nenhum GET altera estado, cookie `Strict` (ou `Lax` com `__Host-`), conferência de Origin e aceitar o risco de navegadores antigos. Na dúvida, adicione token.

### Em cada stack

| Stack | Sessão e CSRF |
|---|---|
| Better Auth, Auth.js | Sessão em cookie pela biblioteca; confira a opção de cookies seguros |
| ASP.NET Core | Cookie de autenticação mais antiforgery integrado |
| Django | Sessões e `CsrfViewMiddleware` ligados por padrão |
| Laravel | Sessão e middleware CSRF por padrão |
| Spring Security | Sessão e CSRF ativos por padrão |

## Combina com / alternativas

- [01-escolha-do-login.md](01-escolha-do-login.md): o login que abre a sessão.
- [03-recuperacao-e-2fa.md](03-recuperacao-e-2fa.md): trocar senha encerra as outras sessões.
- [05-owasp-no-codigo.md](05-owasp-no-codigo.md): XSS e CSRF no código.
- [06-rate-limit.md](06-rate-limit.md): limite no endpoint de refresh.
- `../../api/docs/03-formato-de-erro.md`: resposta 401 quando a sessão expira.
- `../../infra/docs/12-seguranca-base.md`: HTTPS obrigatório.

## Decisão rápida

- **Use se:** o sistema tem login e quer revogar acessos na hora (sessão no servidor com cookie `HttpOnly`).
- **Evite se:** pensa em guardar token de longa duração no localStorage ou usar JWT só por costume.
