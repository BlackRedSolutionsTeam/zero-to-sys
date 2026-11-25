# Guarda de XML e LGPD

> Guarde o XML autorizado por 11 anos em armazenamento seu, com acesso restrito: é o prazo que o fisco adotou para a própria cópia e cobre com folga o mínimo que a lei tributária exige do contribuinte (5 anos contados a partir do exercício seguinte). Trate os dados pessoais da nota como obrigação legal, não como cadastro livre.

| | |
|---|---|
| **Referência** | Ajuste SINIEF nº 2/2025 (CONFAZ), Código Tributário Nacional (arts. 150, §4º, 173 e 195, parágrafo único), Resolução CGNFS-e nº 3/2023 (art. 6º), Resposta à Consulta SP 31869/2025, Lei 13.709/2018 (LGPD, arts. 7º e 16) |
| **Categoria** | Conformidade |
| **Tipo** | Prática de guarda de documento fiscal eletrônico |
| **Vale para** | Quem emite ou recebe NF-e, NFC-e e NFS-e |
| **Verificado em** | 2026-11-25 |

## O que é

O **XML autorizado** é o documento fiscal; o PDF (DANFE ou DANFSe) é só uma representação. Emitente e destinatário precisam guardar o XML e apresentá-lo ao fisco quando pedido.

### O que cada norma diz (texto lido em 2026-11-25)

| Norma | O que diz | Quem obriga |
|---|---|---|
| Ajuste SINIEF nº 2, de 11/04/2025 (DOU 16/04/2025, efeitos desde 1º/05/2025), cláusula primeira | "Os Estados, o Distrito Federal e a Secretaria Especial da Receita Federal do Brasil acordam em padronizar o prazo mínimo em 132 (cento e trinta e dois) meses, contados da data de autorização do documento, de guarda e expurgo dos arquivos [...] XML" de NF-e, CT-e, MDF-e, NFC-e, BP-e, NF3e, CT-e OS, GTV-e, DC-e e NFCom | Os signatários, isto é, as administrações tributárias. O texto não menciona contribuinte. NFS-e não está na lista |
| Resposta à Consulta SP 31869/2025 | O ajuste "é norma aplicável apenas às Administrações Tributárias das Unidades Federadas" e "o prazo de guarda da documentação fiscal, para os contribuintes, não foi alterado". Para SP, o RICMS (art. 202) mantém 5 anos, e mais enquanto houver processo pendente | Entendimento de uma única Secretaria da Fazenda (SP) |
| CTN, art. 173 | O direito de constituir o crédito "extingue-se após 5 (cinco) anos", contados, em regra, do primeiro dia do exercício seguinte ao em que o lançamento poderia ter sido feito | Todos os contribuintes |
| CTN, art. 150, §4º | Nos tributos lançados por homologação, sem prazo legal, são 5 anos contados do fato gerador, salvo dolo, fraude ou simulação | Todos os contribuintes |
| CTN, art. 195, parágrafo único | Os livros obrigatórios de escrituração comercial e fiscal e os comprovantes dos lançamentos devem ser conservados "até a prescrição dos créditos tributários decorrentes das operações a que se referem" | Todos os contribuintes |
| Resolução CGNFS-e nº 3/2023, art. 6º (NFS-e nacional) | O emitente mantém a NFS-e em arquivo digital, sob sua guarda e responsabilidade, "pelo prazo estabelecido na legislação tributária"; o destinatário se sujeita à mesma regra (§ 1º), e quem não é contribuinte credenciado pode guardar só o DANFSe (§ 2º) | Emitente e destinatário de NFS-e nacional; a resolução não fixa número de anos |

### Conclusão por papel

- **Emitente de NF-e e NFC-e:** o Ajuste SINIEF 2/2025 não é obrigação sua pelo texto, e a Secretaria da Fazenda de SP confirma isso para SP. O piso legal vem do CTN e do regulamento do ICMS do estado: 5 anos, que na prática correm do 1º de janeiro do ano seguinte à nota (nota de março de 2026 pede guarda até o fim de 2031, quase 6 anos), e por mais tempo se houver processo pendente, fraude ou o prazo de prescrição do art. 195.
- **Destinatário de NF-e:** a mesma lógica do emitente. O artigo do Ajuste SINIEF 7/2005 e do regulamento estadual que obriga o destinatário não foi lido para esta revisão.
- **Prestador de NFS-e:** o prazo vem da legislação do município (NFS-e municipal) ou da "legislação tributária" (NFS-e nacional, Resolução CGNFS-e 3/2023). Nenhuma lei municipal foi lida; o número exato muda por município.
- **Prazo recomendado: 11 anos (132 meses) a partir da autorização, para todos os tipos.** Não é exigência legal do contribuinte; é a escolha que cobre o piso do CTN com sobra, coincide com o prazo em que o fisco mantém a própria cópia e evita ter de calcular um prazo por município e por estado.

### O que continua ambíguo

- **Se outros estados interpretam o ajuste como o de SP:** só a resposta de SP foi lida. Nada impede que outro estado exija 132 meses do contribuinte na própria legislação.
- **Prazo de prescrição citado no art. 195:** o artigo remete à prescrição sem número; o prazo da prescrição (art. 174 do CTN) não foi lido aqui. Por isso o piso de 5 anos é o da decadência, e o 11 cobre o resto.
- **NFS-e municipal:** depende de cada município.

Se o contador do cliente pedir prazo maior (por exemplo, por processo em andamento), o dele prevalece.

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

const ANOS_DE_GUARDA = 11;

export async function guardarXml(nota: NotaFiscal, xml: Buffer) {
  const hash = createHash("sha256").update(xml).digest("hex");
  const caminho = `notas/${nota.emitidaEm.getFullYear()}/${String(nota.emitidaEm.getMonth() + 1).padStart(2, "0")}/${nota.chave}.xml`;
  await armazenamento.salvar(caminho, xml);

  const guardarAte = new Date(nota.emitidaEm);
  guardarAte.setFullYear(guardarAte.getFullYear() + ANOS_DE_GUARDA);
  await notas.marcar(nota.referencia, { caminho_xml: caminho, hash_xml: hash, guardar_ate: guardarAte });
}
```

O `hash_xml` prova que o arquivo não mudou. O `guardar_ate` usa o prazo recomendado acima (11 anos); se o contador definir outro, troque só a constante.

### LGPD na prática

- **Base legal registrada:** guarda por obrigação legal, no inventário de dados (skill `data`, doc 10, e `security`, doc 09).
- **Acesso mínimo:** só financeiro e fiscal veem a nota; o cliente vê só as dele.
- **Eliminação:** vencido o prazo, apague o arquivo e o dado pessoal da nota; antes dele, o pedido de exclusão do titular recebe a resposta "retemos por obrigação legal".
- **Log de acesso:** quem baixou a nota e quando (skill `data`, doc 07).

## Decisão rápida

| Situação | Ação |
|---|---|
| Nota autorizada | Baixar XML e PDF e copiar para o armazenamento próprio |
| Quanto tempo guardar | 11 anos a partir da autorização; o piso legal do contribuinte é 5 anos contados do exercício seguinte, e o contador pode exigir mais |
| Titular pede exclusão | Responder que há retenção legal; eliminar depois do prazo |
| Troca de emissor | Exportar todos os XML antes de encerrar |
| Nota de homologação | Não guardar como fiscal |
