# Guarda de XML e LGPD

> Guarde o XML autorizado por no mínimo 5 anos em armazenamento seu, com acesso restrito, e trate os dados pessoais da nota como obrigação legal, não como cadastro livre.

| | |
|---|---|
| **Referência** | Código Tributário Nacional (art. 173 e 195), Ajuste SINIEF nº 2/2025, Lei 13.709/2018 (LGPD, arts. 7º e 16), https://www.nfe.fazenda.gov.br |
| **Categoria** | Conformidade |
| **Tipo** | Prática de guarda de documento fiscal eletrônico |
| **Vale para** | Quem emite ou recebe NF-e, NFC-e e NFS-e |
| **Verificado em** | 2026-11-25 |

## O que é

O **XML autorizado** é o documento fiscal; o PDF (DANFE ou DANFSe) é só uma representação. Emitente e destinatário precisam guardar o XML e apresentá-lo ao fisco quando pedido.

Prazo de guarda:

- **5 anos:** é o mínimo citado pela maioria das fontes, ligado ao prazo para o fisco constituir crédito tributário (CTN, art. 173).
- **11 anos (132 meses):** o Ajuste SINIEF nº 2, de 11/04/2025, mudou para 132 meses o prazo mínimo de guarda dos XML de documentos fiscais eletrônicos, com vigência desde 1º/05/2025. As fontes divergem se isso vincula o contribuinte ou só a administração tributária; confirme com o contador.

Na dúvida, o caminho conservador é guardar 11 anos. Conferido em 2026-11-25 em notícias; leia o ajuste no site do CONFAZ.

**LGPD:** a nota carrega dado pessoal (nome, CPF, endereço). A lei permite manter dados para **cumprir obrigação legal** (art. 16, I), mas só pelo tempo e para a finalidade exigida.

## Por que usar

- **Fiscalização:** perder o XML é perder a prova da operação, com multa e até crime em casos graves.
- **Independência do emissor:** se o contrato com o emissor acabar, a nota continua com você.
- **LGPD:** o prazo e a finalidade registrados mostram que há base legal.

## Quando usar

- Desde a primeira nota autorizada em produção.
- Ao trocar de emissor ou encerrar o contrato.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS que emite para clientes | ✅ Ótimo | Cópia própria e acesso do cliente aos arquivos dele |
| Loja virtual | ✅ Ótimo | Volume alto: armazenamento barato com retenção |
| Sistema interno | ✅ Ótimo | Exigência de auditoria e da contabilidade |
| MEI | 🟡 Serve | O emissor gov.br guarda a nota, mas baixe uma cópia |
| Dados de teste (homologação) | ❌ Evite | Sem valor fiscal; não misture com produção |

## Quando é bom

- **Cópia dupla:** o emissor guarda e você também.
- **Armazenamento barato e imutável:** object storage com versionamento e bloqueio de exclusão ([armazenamento](../../integrations/docs/07-armazenamento-de-arquivos.md)).
- **Chave da nota como nome do arquivo:** fácil de achar na fiscalização.

## Quando é ruim

- **Contar só com o painel do emissor:** acesso pode acabar com o contrato. Alguns emissores só mantêm os arquivos por tempo limitado; confirme o prazo do seu contrato.
- **Bucket público:** o XML tem dado pessoal; use URL assinada.
- **Apagar o cliente apagando as notas:** o pedido de eliminação da LGPD não derruba a guarda obrigatória.
- **Alterar o XML:** qualquer mudança invalida a assinatura; guarde o arquivo original.

## Como começar

### Estrutura do armazenamento

```
notas/
  2026/
    11/
      CHAVE-OU-REFERENCIA.xml
      CHAVE-OU-REFERENCIA.pdf
```

Ative versionamento e bloqueio de exclusão por tempo no bucket (compatível com S3 e R2), criptografia em repouso e acesso só por papel de serviço (skill `infra`, doc 09, e `security`).

### Registro no banco

```sql
alter table nota_fiscal
  add column hash_xml char(64),
  add column guardar_ate date;
```

```ts
import { createHash } from "node:crypto";

export async function guardarXml(nota: NotaFiscal, xml: Buffer) {
  const hash = createHash("sha256").update(xml).digest("hex");
  const caminho = `notas/${nota.emitidaEm.getFullYear()}/${String(nota.emitidaEm.getMonth() + 1).padStart(2, "0")}/${nota.chave}.xml`;
  await armazenamento.salvar(caminho, xml);

  const guardarAte = new Date(nota.emitidaEm);
  guardarAte.setFullYear(guardarAte.getFullYear() + 11);
  await notas.marcar(nota.referencia, { caminho_xml: caminho, hash_xml: hash, guardar_ate: guardarAte });
}
```

O `hash_xml` prova que o arquivo não mudou. O `guardar_ate` usa o prazo definido com o contador (aqui, o conservador).

### LGPD na prática

- **Base legal registrada:** guarda por obrigação legal, no inventário de dados (skill `data`, doc 10, e `security`, doc 09).
- **Acesso mínimo:** só financeiro e fiscal veem a nota; o cliente vê só as dele.
- **Eliminação:** vencido o prazo, apague o arquivo e o dado pessoal da nota; antes dele, o pedido de exclusão do titular recebe a resposta "retemos por obrigação legal".
- **Log de acesso:** quem baixou a nota e quando (skill `data`, doc 07).

## Decisão rápida

| Situação | Ação |
|---|---|
| Nota autorizada | Baixar XML e PDF e copiar para o armazenamento próprio |
| Quanto tempo guardar | No mínimo 5 anos; na dúvida, 11; defina com o contador |
| Titular pede exclusão | Responder que há retenção legal; eliminar depois do prazo |
| Troca de emissor | Exportar todos os XML antes de encerrar |
| Nota de homologação | Não guardar como fiscal |
