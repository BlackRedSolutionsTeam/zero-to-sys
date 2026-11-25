# Emissor via API

> Contrate um emissor que fala com SEFAZ e prefeituras por você e use a API dele; escrever isso na mão só vale em volume muito alto.

| | |
|---|---|
| **Referência** | https://focusnfe.com.br/precos/, https://doc.focusnfe.com.br, https://nfe.io/precos, https://enotas.com.br/precos/, https://tecnospeed.com.br/plugdfe/plugnotas/ |
| **Categoria** | Fornecedor |
| **Tipo** | Comparação de emissores de nota fiscal por API |
| **Vale para** | Qualquer backend (Node, Python, .NET, Java, Laravel, Go) que consome REST |
| **Verificado em** | 2026-11-25 |

## O que é

Um **emissor via API** recebe os dados da venda em JSON, monta o XML, assina com o certificado da empresa, envia à SEFAZ ou à prefeitura e devolve o resultado por consulta e webhook. Você não lida com XML, schema nem com os 5.500 municípios. A emissão é **assíncrona**: a resposta imediata só diz que a nota entrou na fila.

## Por que usar

- **Muda um lado só:** o emissor acompanha as notas técnicas, a reforma tributária e as mudanças das prefeituras.
- **Uma integração para vários tipos:** NFS-e, NF-e e NFC-e pela mesma API (Focus NFe e PlugNotas).
- **Sandbox:** testa sem valor fiscal.

## Quando usar

- Para qualquer SaaS ou sistema com emissão própria e volume de até dezenas de milhares de notas por mês.
- Quando não há ERP que já emita as notas (se houver, veja o [doc 08](08-integrar-com-erp-e-contabilidade.md)).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| MVP de SaaS | ✅ Ótimo | Plano de entrada com teste grátis e emissão em poucos dias |
| SaaS em crescimento | ✅ Ótimo | Plano por volume, vários CNPJs e webhook |
| Sistema interno/corporativo | ✅ Ótimo | Um serviço central de emissão para todas as áreas |
| Plataforma com muitos CNPJs | 🟡 Serve | Confira o preço por CNPJ; planos de volume ou contato comercial |
| Site de conteúdo | ❌ Evite | Sem venda não há nota |
| Volume acima de 50 mil notas por mês | 🟡 Serve | Negocie preço; avalie emissão própria só com time fiscal dedicado |

## Quando é bom

- **Preço por documento publicado:** Focus NFe lista mensalidade, franquia e excedente.
- **Homologação separada:** mesmo código, outro token e outra URL.
- **Webhook de status:** evita consulta em loop.

## Quando é ruim

- **Contrato sem preço público:** PlugNotas e eNotas pedem contato ou plano; compare com cuidado.
- **Dependência do fornecedor:** a nota é emitida pelo emissor; guarde o XML e abstraia a integração ([doc 07](07-guarda-de-xml-e-lgpd.md)).
- **Franquia que estoura sem aviso:** o excedente é cobrado depois; monitore o volume.

## Como começar

### Comparação

Valores de 2026-11-25 nas páginas oficiais. Confirme antes de contratar.

| Emissor | Cobre | Preço publicado | Teste |
|---|---|---|---|
| Focus NFe | NFS-e, NF-e, NFC-e, CT-e, MDF-e; recebe NF-e, CT-e e NFS-e nacional | Solo R$ 94,90/mês (1 CNPJ, 100 documentos, excedente R$ 0,11); Start R$ 119,90 (3 CNPJs, 100 documentos por CNPJ, R$ 39,90 por CNPJ extra); Growth R$ 572,00 (CNPJs ilimitados, 4.000 documentos, excedente R$ 0,125); Retail R$ 62,90 (500 NFC-e e 100 NF-e) e Retail+ R$ 657,90 (9.000 NFC-e e 1.000 NF-e); Enterprise sob consulta | 30 dias |
| NFE.io | NFS-e (página de preços) | Base R$ 190/mês (250 notas), Crescimento R$ 265 (500), Escala R$ 375 (1.000); anual a partir de R$ 1.075 (Inicial, 100 notas); Enterprise sob consulta | Não informado na página |
| eNotas | NFS-e e NF-e | A página de preços não mostra os valores; há opção mensal e anual (25% de desconto no anual), excedente cobrado na fatura do mês seguinte e garantia de 30 dias com reembolso | Garantia de 30 dias |
| PlugNotas (TecnoSpeed) | NF-e, NFC-e (contingência offline), NFS-e (municipal e nacional), NFCom, MDF-e | Sem preço público; formulário e retorno comercial | Sandbox público sem cadastro, com respostas simuladas |

No Focus NFe, a franquia dos planos Solo a Enterprise inclui NFS-e, NF-e e NFC-e; Retail e Retail+ não listam NFS-e.

### Escolha pelo volume

| Volume | Emissor |
|---|---|
| Até 100 notas por mês, um CNPJ | Focus NFe Solo |
| Vários CNPJs próprios ou clientes | Focus NFe Start ou Growth |
| Só NFC-e em loja | Focus NFe Retail |
| Só NFS-e e franquia maior que 100 | NFE.io, comparando com o excedente do Focus |
| Preço negociado, muitas notas | PlugNotas ou Enterprise do Focus |

### Autenticação e ambientes (Focus NFe)

HTTP Basic: o token da empresa é o usuário e a senha fica vazia. Homologação e produção mudam a URL base e o token (página "Ambiente" da documentação).

```bash
curl -u "$FOCUS_TOKEN:" https://api.focusnfe.com.br/v2/empresas
```

### Isole o emissor em um módulo

Um adaptador deixa trocar de fornecedor sem reescrever o sistema.

```ts
export interface EmissorFiscal {
  emitirServico(pedidoId: string, dados: NotaServico): Promise<{ referencia: string }>;
  emitirProduto(pedidoId: string, dados: NotaProduto): Promise<{ referencia: string }>;
  consultar(referencia: string): Promise<StatusNota>;
  cancelar(referencia: string, justificativa: string): Promise<void>;
}
```

A `referencia` (campo `ref` no Focus) é a chave da nota no emissor e identifica a nota no seu banco; use o id do pedido ou da cobrança. Segredos do token: skill `infra`, doc 09.

## Decisão rápida

| Situação | Escolha |
|---|---|
| Quer preço claro e API única | Focus NFe |
| Só serviço e franquia média | NFE.io |
| Loja com NFC-e e queda de internet | PlugNotas (offline) ou Focus Retail com contingência |
| Já tem ERP | Emita pelo ERP (doc 08) |
| MEI com poucas notas | Emissor do gov.br, sem API |
