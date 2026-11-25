# Dados pessoais no painel

> A equipe vê só o que precisa para o trabalho, com CPF e e-mail mascarados por padrão, e cada exportação sai com motivo, limite e registro.

| | |
|---|---|
| **Referência** | LGPD, Lei 13.709/2018 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm), princípios de finalidade, adequação e necessidade (art. 6) e segurança (art. 46); orientações da ANPD (gov.br/anpd) |
| **Categoria** | Privacidade |
| **Tipo** | Prática de minimização de acesso |
| **Vale para** | Qualquer painel que mostre dado de pessoa física no Brasil |
| **Verificado em** | 2026-11-25 (artigos citados de acordo com o doc de LGPD da skill `security`; a lei não foi reaberta nesta data. Não é parecer jurídico: veja a skill `legal`) |

## O que é

O modelo de LGPD do sistema está em [security, doc 09](../../security/docs/09-lgpd-na-pratica.md) e [data, doc 10](../../data/docs/10-dados-pessoais-e-lgpd.md). Aqui: como o painel mostra, deixa buscar e exporta esses dados.

## Por que usar

- A equipe é um dos principais pontos de vazamento (curiosidade, erro, conta invadida).
- O acesso da equipe precisa de finalidade e base legal ([legal, doc 02](../../legal/docs/02-politica-de-privacidade-e-o-mapa-de-dados.md)).

## Quando usar

- Em toda tela do painel que mostre nome, CPF, e-mail, telefone, endereço, saúde ou dado financeiro.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucos dados pessoais |
| MVP de SaaS | ✅ Ótimo | Máscara resolve a maior parte |
| SaaS em crescimento | ✅ Ótimo | Revelação sob demanda com registro |
| Sistema interno/corporativo | ✅ Ótimo | Dado de funcionário é sensível |
| API/integração | 🟡 Serve | Pouco dado pessoal, muitos tokens |
| App mobile com backend | ✅ Ótimo | Igual ao SaaS |
| Planilha de clientes exportada sem controle | ❌ Evite | Vaza e ninguém sabe de quem |

## Quando é bom

- **Máscara por padrão:** `***.456.789-**`, `m***@gmail.com`; "revelar" é uma ação com motivo e registro ([doc 06](06-auditoria-do-que-a-equipe-faz.md)).
- **Busca por dado completo, exibição mascarada:** o suporte digita o CPF inteiro e vê o cliente, sem ver o número depois.
- **Acesso por necessidade:** o papel de operação não vê dado financeiro; o suporte não vê documento.
- **Exportação controlada:** só papel autorizado, limite de linhas, só as colunas necessárias, arquivo com expiração, registro do pedido e de quem baixou.
- **Dado sensível** (saúde, biometria) em tela separada com permissão própria.
- **Cópias fora do controle** (print, planilha): oriente a equipe e use marca d'água com o nome de quem vê, se o risco justificar.

## Quando é ruim

- **Mascarar só no front:** a API ainda devolve o CPF inteiro.
- **Exportação livre** em CSV com tudo.
- **Log de busca com dado completo** no log da aplicação.
- **Falta de prazo:** acesso concedido "para sempre" a quem mudou de função.

## Como começar

Máscara no servidor (TypeScript):

```ts
export const mascararCpf = (cpf: string) => cpf.replace(/^(\d{3})\.?(\d{3})\.?(\d{3})-?(\d{2})$/, "***.$2.$3-**");

export const mascararEmail = (email: string) => {
  const [usuario, dominio] = email.split("@");
  return `${usuario[0]}***@${dominio}`;
};

export function visaoDoCliente(c: Cliente, pode: (p: string) => boolean) {
  return {
    id: c.id,
    nome: c.nome,
    cpf: pode("cliente.cpf.revelar") ? c.cpf : mascararCpf(c.cpf),
    email: pode("cliente.email.revelar") ? c.email : mascararEmail(c.email),
  };
}
```

Revelar com motivo:

```ts
app.post("/painel/clientes/:id/revelar-cpf", exige("cliente.cpf.revelar"), async (c) => {
  const { motivo } = await c.req.json();
  if (!motivo) return c.json({ erro: "Informe o motivo." }, 422);
  const cliente = await db.cliente.findUniqueOrThrow({ where: { id: c.req.param("id") } });
  await auditar({ ator: c.get("staffId"), acao: "cliente.cpf.revelar", alvo: cliente.id, motivo });
  return c.json({ cpf: cliente.cpf });
});
```

## Combina com / alternativas

- [Legal, doc 06](../../legal/docs/06-direitos-do-titular-e-canal-do-encarregado.md): atender pedidos de acesso e exclusão do titular pelo painel.
- [Security, doc 09](../../security/docs/09-lgpd-na-pratica.md): base técnica de LGPD.
- Alternativa: não ter o dado no painel (mostrar apenas um identificador).

## Decisão rápida

- **Use** máscara no servidor, revelação com motivo e exportação com limite e registro.
- **Evite** máscara só no front e exportação livre.
