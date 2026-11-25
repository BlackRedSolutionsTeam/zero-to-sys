# Ações perigosas no painel

> Toda ação difícil de desfazer pede confirmação clara, tenta ser reversível, tem limite de lote e pode ser desligada de uma vez.

| | |
|---|---|
| **Referência** | OWASP Authorization Cheat Sheet (cheatsheetseries.owasp.org); padrões de confirmação em design de interface (Nielsen Norman Group, nngroup.com, citado de memória e não reconferido nesta data) |
| **Categoria** | Segurança e experiência |
| **Tipo** | Prática de proteção contra erro |
| **Vale para** | Qualquer painel com ações de escrita |
| **Verificado em** | 2026-11-25 (fontes não reabertas nesta data) |

## O que é

Ações perigosas: apagar, estornar, bloquear, trocar plano de muitos clientes, reenviar e-mail em massa, reprocessar fila, mudar flag para todos. O custo do erro é alto ou o desfazer é difícil.

## Por que usar

- A maioria dos desastres internos é cliquei no registro errado ou apliquei no lote errado.
- Confirmação bem desenhada reduz erro; confirmação genérica ("Tem certeza?") vira hábito de clicar.

## Quando usar

- Em toda ação que altera dinheiro, acesso, dado de muitos registros ou dado que não volta.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Apagar página pede lixeira |
| MVP de SaaS | ✅ Ótimo | Soft delete e confirmação com texto |
| SaaS em crescimento | ✅ Ótimo | Limite de lote e modo somente leitura |
| Sistema interno/corporativo | ✅ Ótimo | Reversão e aprovação |
| API/integração | ✅ Ótimo | Revogar chave pede confirmação |
| App mobile com backend | ✅ Ótimo | Igual ao SaaS |
| Botão "Excluir" que apaga na hora | ❌ Evite | Sem volta |

## Camadas de proteção

| Camada | Como |
|---|---|
| Confirmação específica | Diga o efeito: "Reembolsar R$ 120,00 para Maria (fatura 345)". Para risco alto, peça para digitar o nome da empresa |
| Soft delete | Marque como apagado e só remova de verdade depois do prazo de retenção ([data, doc 07](../../data/docs/07-auditoria-historico-soft-delete.md)) |
| Prévia | Mostre quantos registros serão afetados e uma amostra antes de rodar |
| Limite de lote | Máximo por execução (por exemplo 100); acima disso, aprovação em duas pessoas ([doc 03](03-quem-acessa-papeis-e-menor-privilegio.md)) |
| Reversão | Guarde o estado anterior e ofereça "desfazer" por um tempo |
| Idempotência | Repetir o pedido não duplica estorno ([integrations, doc 01](../../integrations/docs/01-pagamentos.md)) |
| Modo somente leitura | Chave global que bloqueia toda escrita do painel durante incidente ou migração |
| Reautenticação | Pedir 2FA de novo ([doc 04](04-autenticacao-forte-do-painel.md)) |

## Quando é bom

- **Verbo no botão** ("Reembolsar"), nunca "OK".
- **Cor e posição** diferentes para o botão destrutivo ([design-systems, doc 03](../../design-systems/docs/03-admin-crud.md)).
- **Limite por papel**: suporte reembolsa até R$ 100; acima, financeiro.

## Quando é ruim

- **Confirmação em tudo:** a pessoa para de ler.
- **Soft delete sem filtro** nas consultas: o "apagado" aparece de novo.
- **Desfazer que só existe na tela:** feche a aba e some.

## Como começar

Modo somente leitura e limite de lote (TypeScript):

```ts
export const bloqueiaEscritaSeLeitura = async (c, next) => {
  const leitura = await config.get("painel.somente_leitura");
  if (leitura && c.req.method !== "GET") {
    return c.json({ erro: "Painel em modo somente leitura." }, 503);
  }
  await next();
};

export function limitaLote<T>(ids: T[], max = 100) {
  if (ids.length > max) throw new Erro(`Máximo de ${max} por execução.`);
  return ids;
}
```

## Combina com / alternativas

- [Auditoria](06-auditoria-do-que-a-equipe-faz.md): cada ação perigosa deixa registro com motivo.
- [Quem acessa](03-quem-acessa-papeis-e-menor-privilegio.md): aprovação para o que passa do limite.
- [Operations](../../operations/docs/04-atender-um-incidente.md): modo somente leitura em incidente.

## Decisão rápida

- **Use** confirmação específica, soft delete, limite de lote e chave de somente leitura.
- **Evite** "Tem certeza?" genérico e exclusão definitiva por clique.
