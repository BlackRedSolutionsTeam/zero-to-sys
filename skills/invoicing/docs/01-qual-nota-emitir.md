# Qual nota emitir

> Serviço é NFS-e, produto é NF-e, venda presencial ao consumidor é NFC-e; o regime tributário muda o imposto e a obrigação, não o tipo da nota.

| | |
|---|---|
| **Referência** | https://www.gov.br/nfse, https://www.nfe.fazenda.gov.br, https://www.gov.br/empresas-e-negocios/pt-br/empreendedor |
| **Categoria** | Decisão |
| **Tipo** | Escolha do documento fiscal e do regime |
| **Vale para** | SaaS, sistema interno, loja virtual e agência no Brasil, MEI a Lucro Real |
| **Verificado em** | 2026-11-25 |

## O que é

Nota fiscal eletrônica é um arquivo XML assinado com certificado digital e autorizado por um órgão do governo. Cada tipo tem um órgão diferente:

- **NFS-e (serviço):** autorizada pela prefeitura, ou pelo padrão nacional do gov.br ([doc 03](03-nfse-nacional-e-padroes-municipais.md)).
- **NF-e (produto, modelo 55):** autorizada pela SEFAZ do estado. Vale para venda entre empresas e para venda ao consumidor com entrega.
- **NFC-e (produto, modelo 65):** autorizada pela SEFAZ, para venda presencial ao consumidor final.

**Regime tributário** é o enquadramento da empresa (MEI, Simples Nacional, Lucro Presumido, Lucro Real). Ele define alíquotas, o que vai na nota e quem é obrigado a emitir. O contador escolhe; o sistema só aplica.

## Por que usar

- **Evita multa:** vender sem nota quando é obrigatório gera autuação.
- **Cliente pede:** empresa compradora precisa da nota para abater a despesa.
- **Define o fluxo:** o tipo escolhido muda emissor, cadastro e prazo de cancelamento.

## Quando usar

- No início do projeto, junto com o contador, antes de desenhar o checkout.
- Ao adicionar um novo tipo de venda (assinatura de software, produto físico, mensalidade).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS (assinatura de software) | ✅ NFS-e | Cobrança recorrente de licença de uso é serviço na maioria dos municípios; o contador confirma o item da lista |
| Loja virtual com produto físico | ✅ NF-e | Entrega ao consumidor exige NF-e, com transporte |
| Loja física ou balcão | ✅ NFC-e | Venda presencial ao consumidor final |
| Clínica, escola, agência | ✅ NFS-e | Prestação de serviço por profissional ou empresa |
| Produto digital (curso, ebook) | 🟡 Depende | A classificação (serviço ou produto) varia; o contador decide |
| Marketplace | 🟡 Depende | Quem emite é cada vendedor ou o marketplace, conforme o contrato; consulte o contador |
| MEI que só presta serviço | ✅ NFS-e nacional | Emissor gratuito do gov.br |
| Ferramenta interna sem venda | ❌ Evite | Sem operação de venda não há nota |

## Quando é bom

- **Decisão cedo:** o tipo escolhido define os campos do cadastro e do checkout.
- **Um tipo por item do catálogo:** cada produto ou serviço guarda como é tributado.
- **Mesmo emissor para vários tipos:** emissores por API cobrem NFS-e, NF-e e NFC-e juntos ([doc 02](02-emissor-via-api.md)).

## Quando é ruim

- **Escolher o tipo pelo que parece:** a mesma venda pode ser serviço ou produto conforme a lei do município e do estado.
- **Misturar serviço e produto numa nota só:** são documentos diferentes; ao vender os dois, emita duas notas.
- **Decidir o regime no código:** muda com o faturamento e com a lei; deixe configurável por empresa.

## Como começar

### O que muda por regime

| Regime | Quem emite | O que pesa no sistema |
|---|---|---|
| MEI | NFS-e nacional (serviço a pessoa jurídica é obrigatório); NF-e e NFC-e conforme a atividade | Limite de faturamento anual e DAS fixo; poucos campos fiscais |
| Simples Nacional | NFS-e, NF-e e NFC-e | Imposto sobre o faturamento por anexo; na NF-e vai o código de regime (CRT 1) e o CSOSN no lugar do CST |
| Lucro Presumido | Todas | Imposto por percentual de presunção; ISS, PIS, COFINS retidos conforme o tomador |
| Lucro Real | Todas | Apuração real; crédito de PIS e COFINS; cadastro fiscal mais detalhado |

### Perguntas para o contador

Leve esta lista e registre as respostas no `README` (ou onde a skill `product`, doc 07, indica):

1. Qual o regime tributário e o CNAE principal e secundários?
2. Cada item vendido é serviço (qual item da LC 116) ou produto (qual NCM e CFOP)?
3. Em qual município é recolhido o ISS?
4. Há retenção de imposto na fonte quando o cliente é pessoa jurídica?
5. Quem emite se for marketplace ou revenda?

### Modelo mínimo no banco

```sql
create table empresa_fiscal (
  empresa_id uuid primary key references empresas(id),
  cnpj char(14) not null,
  regime text not null check (regime in ('mei', 'simples', 'presumido', 'real')),
  inscricao_municipal text,
  inscricao_estadual text,
  codigo_municipio_ibge char(7) not null,
  ambiente text not null default 'homologacao' check (ambiente in ('homologacao', 'producao'))
);
```

O regime fica em tabela, não em constante; trocar de regime é uma atualização, não um deploy. Dinheiro e auditoria: skill `data`, docs 02 e 07.

## Decisão rápida

| Se você vende... | Emita |
|---|---|
| Hora, projeto, assinatura de software, consulta | NFS-e |
| Mercadoria que será enviada | NF-e |
| Mercadoria no balcão para pessoa física | NFC-e |
| Serviço e mercadoria juntos | Duas notas |
| Não sabe | Pergunte ao contador antes de codificar |
