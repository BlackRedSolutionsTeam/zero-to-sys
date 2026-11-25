# Impersonação: entrar como cliente

> Deixe o suporte ver o que o cliente vê, mas só com motivo, por pouco tempo, com banner visível, sem acesso a senha ou dados de pagamento e com cada clique registrado.

| | |
|---|---|
| **Referência** | OWASP Logging Cheat Sheet e Authorization Cheat Sheet (cheatsheetseries.owasp.org); LGPD, Lei 13.709/2018, arts. 6 (princípios de finalidade e necessidade) e 46 (segurança), conforme o doc de LGPD da skill `security` |
| **Categoria** | Segurança e suporte |
| **Tipo** | Prática de acesso delegado |
| **Vale para** | SaaS com suporte que precisa reproduzir o problema do cliente |
| **Verificado em** | 2026-11-25 (artigos da LGPD não reabertos nesta data; confira com a skill `legal`) |

## O que é

"Entrar como" é a equipe abrir o produto como se fosse o cliente, sem pedir a senha dele. Não é login: é uma sessão especial, ligada ao funcionário que a abriu.

## Por que usar

- Reproduz o bug exatamente como o cliente vê.
- Evita pedir senha por e-mail ou chat, que é pior para a segurança.

## Quando usar

- Quando descrever o problema por escrito ou compartilhar a tela não resolve.
- Nunca como atalho para editar dado: para isso existe a ação própria no painel.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem conta de cliente |
| MVP de SaaS | ✅ Ótimo | Suporte rápido sem pedir senha |
| SaaS em crescimento | ✅ Ótimo | Com todas as travas abaixo |
| Sistema interno/corporativo | 🟡 Serve | Só se houver suporte separado dos usuários |
| API/integração | 🟡 Serve | Prefira ver logs e chamadas a entrar como |
| App mobile com backend | 🟡 Serve | Sessão de impersonação na web, não no app |
| Saúde, financeiro ou dado muito sensível | 🟡 Serve | Exija consentimento do cliente por ticket |

## Quando é bom

- **Motivo obrigatório** e número do ticket gravados.
- **Tempo limitado** (por exemplo 15 minutos) e fim automático.
- **Banner fixo** no topo: "Você está vendo como fulano, empresa X. Sair."
- **Aviso ao cliente** (e-mail ou notificação) de que a equipe acessou, com data e motivo, ou autorização prévia no ticket.
- **Somente leitura por padrão**; escrita só com permissão extra.
- **Bloqueios:** trocar senha, e-mail, 2FA, ver dados de cartão, exportar, apagar conta, ligar outra impersonação.
- **Trilha:** cada requisição leva o ator real (funcionário) e o ator exibido (cliente) ([doc 06](06-auditoria-do-que-a-equipe-faz.md)).

## Quando é ruim

- **Impersonar com a sessão normal do cliente**, sem marca: o log mostra o cliente agindo.
- **Sem limite de tempo.**
- **Sem aviso** nem base clara: é o acesso da equipe a dado pessoal (ver [legal](../../legal/docs/02-politica-de-privacidade-e-o-mapa-de-dados.md) para a finalidade na política).
- **Super admin impersonando sem aprovação** em conta de grande cliente.

## Como começar

Emissão do token de impersonação (TypeScript):

```ts
export async function iniciarImpersonacao(staff: Staff, alvoId: string, motivo: string, ticket: string) {
  if (!staff.pode("impersonate.start")) throw new Erro("Sem permissão.");
  if (!motivo.trim() || !ticket.trim()) throw new Erro("Motivo e ticket obrigatórios.");
  const sessao = await db.impersonation.create({
    data: {
      staffId: staff.id,
      alvoId,
      motivo,
      ticket,
      readOnly: true,
      expiraEm: new Date(Date.now() + 15 * 60 * 1000),
    },
  });
  await auditar({ ator: staff.id, acao: "impersonate.start", alvo: alvoId, depois: { motivo, ticket } });
  await notificarCliente(alvoId, { staff: staff.nomePublico, motivo });
  return assinar({ sid: sessao.id, imp: true }, "15m");
}
```

Middleware que trava ações (TypeScript):

```ts
export const bloqueiaSeImpersonando = async (c, next) => {
  const s = c.get("sessao");
  if (s.imp && (s.readOnly || BLOQUEADAS.has(c.req.path))) {
    return c.json({ erro: "Ação indisponível durante a impersonação." }, 403);
  }
  await next();
};
```

O banner é renderizado no produto quando `sessao.imp` é verdadeiro e mostra quem está de fato operando.

## Combina com / alternativas

- [Auditoria](06-auditoria-do-que-a-equipe-faz.md) e [papéis](03-quem-acessa-papeis-e-menor-privilegio.md).
- Alternativa mais segura: "ver como" somente leitura dentro do painel, sem abrir o produto.
- [Suporte ao cliente](../../operations/docs/07-suporte-ao-cliente.md).

## Decisão rápida

- **Use** com motivo, ticket, 15 minutos, banner, leitura por padrão, aviso ao cliente e auditoria.
- **Evite** pedir a senha ao cliente ou impersonar sem rastro.
