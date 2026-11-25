# Recuperação de senha e 2FA

> Recuperação com token de uso único, curto e guardado só como hash; resposta igual para e-mail existente ou não; 2FA com app autenticador ou passkey, e SMS só como último recurso.

| | |
|---|---|
| **Referência** | OWASP Forgot Password Cheat Sheet; OWASP Multifactor Authentication Cheat Sheet; RFC 6238 (TOTP) e RFC 4226 (HOTP); W3C Web Authentication (WebAuthn); documentação oficial da biblioteca de auth escolhida |
| **Categoria** | Segurança |
| **Tipo** | Prática de recuperação de conta e segundo fator |
| **Vale para** | Qualquer sistema com login por e-mail e senha: Better Auth, Auth.js, ASP.NET Core Identity, Django auth, Laravel Fortify, Spring Security |
| **Verificado em** | 2026-11-24 |

## O que é

**Recuperação de senha** é o fluxo "esqueci a senha": o sistema manda um link com um token para o e-mail, e quem clicar define uma senha nova. Quem controla o e-mail controla a conta, então esse fluxo é uma segunda porta de entrada e precisa de tanto cuidado quanto o login.

**2FA** (segundo fator) exige algo além da senha:

- **TOTP** (RFC 6238): código de 6 dígitos que muda a cada 30 segundos, gerado por app autenticador.
- **Passkey / WebAuthn:** chave criptográfica guardada no aparelho ou no gerenciador de senhas, confirmada por biometria. Não dá para ser enganado por site falso.
- **Códigos de recuperação:** lista de códigos de uso único, para quem perdeu o aparelho.
- **SMS:** código por mensagem. O mais fraco, por causa de SIM swap (o golpista transfere o número para outro chip).

## Por que usar

- **Senha vaza:** o segundo fator barra quem tem só a senha.
- **Recuperação mal feita vira invasão:** token previsível ou reutilizável entrega a conta.
- **Suporte:** quem perde o aparelho precisa de caminho que não dependa de você abrir exceção.

## Quando usar

- Recuperação: em todo sistema com senha.
- Verificação de e-mail: no cadastro, antes de confiar no endereço.
- 2FA: obrigatório para admin e para quem vê dado sensível (prontuário), opcional para os demais.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Só se houver área logada; recuperação sim, 2FA raramente |
| MVP de SaaS | ✅ Ótimo | Recuperação e verificação desde o início; 2FA opcional com TOTP |
| SaaS em crescimento | ✅ Ótimo | Passkey, 2FA obrigatório para admin, auditoria de troca de senha |
| Sistema interno/corporativo | ✅ Ótimo | Dado sensível; 2FA para todos, ou login único da empresa |
| API/integração | 🟡 Serve | Máquina usa chave de API, não senha; 2FA vale só para o painel humano |
| App mobile | ✅ Ótimo | Passkey e biometria nativa são a melhor experiência |
| Qualquer um, com pergunta secreta ("nome do seu pet") | ❌ Evite | Respostas são adivinháveis ou públicas |

## Quando é bom

- **Token aleatório de verdade**, gerado com gerador criptográfico, ligado a um usuário e de uso único.
- **Expiração curta:** a OWASP não fixa o prazo; 15 a 60 minutos é uma escolha comum.
- **Guardar só o hash do token:** se o banco vazar, os links não servem.
- **Mesma resposta, mesmo tempo:** "se o e-mail existir, enviaremos o link", exista ou não, para não revelar quem tem conta.
- **Trocou a senha, derrubou as sessões** (veja [sessão e tokens](./02-sessao-e-tokens.md)) e invalide outros tokens pendentes.
- **Não logar sozinho** depois da troca: peça o login.
- **Avisar por e-mail** quando a senha ou o 2FA mudar.
- **Códigos de recuperação** mostrados uma vez, guardados como hash.

## Quando é ruim

- **Token na URL fica em log e histórico:** use `Referrer-Policy: no-referrer` na página e troque o token por sessão curta se a biblioteca permitir.
- **Bloquear a conta após pedidos de recuperação:** a OWASP avisa que isso deixa qualquer um travar a conta alheia. Limite por taxa ([rate limit](./06-rate-limit.md)), não bloqueie.
- **SMS como único segundo fator:** vulnerável a SIM swap. Melhor que nada, pior que TOTP.
- **2FA sem recuperação:** o usuário perde o celular e o suporte vira o ponto fraco.
- **E-mail que nunca foi verificado** usado para recuperar conta.

## Como começar

Gerar e guardar o token (TypeScript, Node):

```ts
import { randomBytes, createHash } from "node:crypto";

export function novoTokenDeRecuperacao() {
  const token = randomBytes(32).toString("base64url");
  const hash = createHash("sha256").update(token).digest("hex");
  const expiraEm = new Date(Date.now() + 30 * 60 * 1000);
  return { token, hash, expiraEm };
}
```

SHA-256 basta aqui porque o token já é aleatório e longo. Senha de gente precisa de hash lento (veja [escolha do login](./01-escolha-do-login.md)).

Tabela:

```sql
create table password_reset_tokens (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null references users(id) on delete cascade,
  token_hash text not null unique,
  expires_at timestamptz not null,
  used_at    timestamptz,
  created_at timestamptz not null default now()
);
```

Pedido de recuperação, sempre com a mesma resposta:

```ts
app.post("/auth/esqueci-senha", async (c) => {
  const { email } = await c.req.json();
  const usuario = await buscarUsuarioPorEmail(email);
  if (usuario) {
    const { token, hash, expiraEm } = novoTokenDeRecuperacao();
    await salvarToken(usuario.id, hash, expiraEm);
    await fila.enviar("email-recuperacao", { para: usuario.email, token });
  }
  return c.json({ mensagem: "Se o e-mail estiver cadastrado, enviaremos o link." });
});
```

O envio vai para uma fila para o tempo de resposta ser igual nos dois casos.

Troca da senha:

```ts
app.post("/auth/redefinir-senha", async (c) => {
  const { token, novaSenha } = await c.req.json();
  const hash = createHash("sha256").update(token).digest("hex");
  const registro = await buscarTokenValido(hash);
  if (!registro) return c.json({ erro: "Link inválido ou expirado." }, 400);
  await db.transaction(async (tx) => {
    await atualizarSenha(tx, registro.userId, novaSenha);
    await marcarTokenComoUsado(tx, registro.id);
    await encerrarSessoes(tx, registro.userId);
  });
  return c.json({ ok: true });
});
```

`buscarTokenValido` exige `used_at is null` e `expires_at > now()`.

No cadastro, a verificação de e-mail usa o mesmo desenho: token aleatório, hash no banco, expiração, uso único.

2FA em cada stack (confirme na documentação da versão que você usa):

| Stack | Caminho |
|---|---|
| Better Auth | Plugin de 2FA da própria biblioteca (TOTP e códigos de recuperação) |
| Auth.js | Sem 2FA pronto; use passkeys (provider WebAuthn) ou monte o TOTP |
| ASP.NET Core Identity | Suporte a autenticador TOTP e códigos de recuperação embutido |
| Django | Pacote de terceiros para TOTP, por exemplo django-otp |
| Laravel | Fortify traz 2FA com TOTP e códigos de recuperação |
| Spring Security | Sem TOTP pronto; Spring Security 6.4 ou mais novo tem suporte a passkeys, confira a versão |

Se for montar TOTP, use biblioteca testada; não implemente RFC 6238 na mão. Aceite uma janela de tolerância de um passo e bloqueie reuso do mesmo código.

## Combina com / alternativas

- [Escolha do login](./01-escolha-do-login.md): login sem senha (passkey, link mágico) reduz o que recuperar.
- [Sessão e tokens](./02-sessao-e-tokens.md): derrubar sessões após a troca.
- [Rate limit](./06-rate-limit.md): limitar pedidos e tentativas.
- [Papéis e permissões](./04-papeis-e-permissoes.md): quem é obrigado a ter 2FA.
- [Dados pessoais e LGPD](../../data/docs/10-dados-pessoais-e-lgpd.md): e-mail e telefone são dados pessoais.

## Decisão rápida

- **Use se:** o sistema tem senha; faça recuperação com token único, hash e resposta igual, e ofereça TOTP ou passkey com códigos de recuperação.
- **Evite se:** a ideia é pergunta secreta, token reutilizável ou SMS como única proteção de dado sensível.
