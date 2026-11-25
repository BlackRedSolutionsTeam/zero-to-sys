# Autenticação forte do painel

> O painel é o alvo mais valioso do sistema: exija 2FA para toda a equipe, use SSO quando houver e deixe a sessão curta e a porta fechada para quem não precisa estar lá.

| | |
|---|---|
| **Referência** | OWASP Authentication Cheat Sheet e Multifactor Authentication Cheat Sheet (cheatsheetseries.owasp.org); documentação do Cloudflare Access (developers.cloudflare.com/cloudflare-one/policies/access/) |
| **Categoria** | Segurança |
| **Tipo** | Prática de autenticação |
| **Vale para** | Qualquer painel acessível pela internet |
| **Verificado em** | 2026-11-25 (limite de 50 usuários do plano grátis do Cloudflare Access conferido pela skill `cloudflare`; o resto desta página é prática geral sem nova conferência de fonte nesta data) |

## O que é

Camadas, da mais externa para a interna:

1. **Borda:** só quem passou pelo Cloudflare Access ou pela VPN chega ao painel ([doc 11](11-painel-separado-do-produto.md)).
2. **Login:** e-mail e senha ou SSO.
3. **Segundo fator (2FA):** app autenticador, chave de segurança (passkey ou FIDO2). Evite SMS.
4. **Sessão curta:** expira por inatividade e por tempo total.

## Por que usar

- Senha vazada de funcionário vale mais que a de cliente: dá acesso a todos os clientes.
- 2FA obrigatório corta a maioria dos ataques por credencial reaproveitada.
- SSO centraliza a saída da pessoa: desligou no provedor, perdeu o acesso.

## Quando usar

- Sempre no painel. Não deixe 2FA como opção para a equipe.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Painel de CMS é alvo comum |
| MVP de SaaS | ✅ Ótimo | Passkey ou app autenticador, sem custo |
| SaaS em crescimento | ✅ Ótimo | Some SSO e Access |
| Sistema interno/corporativo | ✅ Ótimo | SSO do provedor da empresa |
| API/integração | ✅ Ótimo | Painel com chaves exige 2FA |
| App mobile com backend | ✅ Ótimo | Igual ao SaaS |
| Painel só com senha na internet aberta | ❌ Evite | É o primeiro alvo de ataque |

## Quando é bom

- **2FA obrigatório no primeiro login**, não adiável.
- **Passkey ou chave de segurança** resiste a phishing; app autenticador é o mínimo.
- **Cloudflare Access na frente** ([cloudflare, doc 07](../../cloudflare/docs/07-access-e-zero-trust.md)): a origem nem recebe a requisição de quem não passou.
- **Sessão do painel menor que a do produto**: sugestão de 15 a 30 minutos de inatividade e 8 horas no total (valores de prática, ajuste ao seu risco).
- **Reautenticar** (pedir senha ou 2FA de novo) antes de ação perigosa.

## Quando é ruim

- **SMS como segundo fator**: troca de chip derruba.
- **Códigos de recuperação sem controle**: sem fluxo de reset, a pessoa fica fora; com fluxo fraco, o atacante entra. Reset de 2FA da equipe passa por outro admin.
- **Sessão longa em computador compartilhado.**
- **IP fixo como única defesa**: quem trabalha de casa muda de IP; use Access com identidade.

## Como começar

Exigir 2FA no servidor, para toda rota do painel (TypeScript):

```ts
export const exigeSessaoForte = async (c, next) => {
  const s = c.get("sessao");
  if (!s?.mfaVerificado) return c.json({ erro: "Segundo fator obrigatório." }, 403);
  if (Date.now() - s.autenticadoEm > 8 * 60 * 60 * 1000) return c.json({ erro: "Sessão expirada." }, 401);
  await next();
};
```

Reautenticação antes de ação crítica:

```ts
export const reautenticado = (minutos: number) => async (c, next) => {
  const s = c.get("sessao");
  if (Date.now() - s.reautenticadoEm > minutos * 60 * 1000) {
    return c.json({ erro: "Confirme sua identidade de novo." }, 403);
  }
  await next();
};
```

Detalhes de 2FA, recuperação e sessão: [security, doc 03](../../security/docs/03-recuperacao-e-2fa.md) e [doc 02](../../security/docs/02-sessao-e-tokens.md).

## Combina com / alternativas

- [Painel separado](11-painel-separado-do-produto.md): domínio próprio e borda.
- [Papéis](03-quem-acessa-papeis-e-menor-privilegio.md): quem entra e o que faz.

## Decisão rápida

- **Use** 2FA obrigatório, Access na frente e sessão curta.
- **Evite** SMS, sessão longa e painel exposto sem camada de borda.
