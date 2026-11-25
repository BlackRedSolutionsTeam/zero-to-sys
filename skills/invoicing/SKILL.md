---
name: invoicing
description: 'Emite nota fiscal (NFS-e, NF-e, NFC-e) por API sem implementar a SEFAZ: qual nota por regime, emissores com preço, certificado, guarda do XML, reforma tributária (IBS/CBS) e integração com ERP. Use quando pedirem "emitir nota fiscal", "NFS-e" ou "integrar com o Bling".'
---

# invoicing

Guia para quem precisa emitir nota fiscal no Brasil sem virar especialista em SEFAZ e em 5.500 prefeituras. A regra é simples: use um emissor via API, trate a nota como um estado do pedido que muda por webhook e guarde o XML. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e exemplos prontos.

## Como usar esta skill

1. **Descubra o que vende e o regime da empresa** ([doc 01](docs/01-qual-nota-emitir.md)). Serviço é NFS-e, produto é NF-e, venda presencial ao consumidor é NFC-e. Quem decide o regime e o enquadramento é o contador, não o código.
2. **Escolha o emissor** ([doc 02](docs/02-emissor-via-api.md)). Implementar SEFAZ e prefeituras direto só se justifica em volume muito alto.
3. **Veja se o município emite pelo padrão nacional** ([doc 03](docs/03-nfse-nacional-e-padroes-municipais.md)); isso muda a integração de serviço.
4. **Monte o cadastro fiscal** ([doc 04](docs/04-cadastro-fiscal.md)): dados do cliente e, para produto, NCM, CFOP e tributação, validados antes de emitir.
5. **Implemente o fluxo** ([doc 05](docs/05-fluxo-pagamento-emissao-webhook.md)): pagamento aprovado, emissão assíncrona, webhook, PDF e XML por e-mail.
6. **Trate o erro** ([doc 06](docs/06-cancelamento-correcao-e-contingencia.md)): cancelamento, carta de correção, rejeição e contingência.
7. **Guarde o XML** ([doc 07](docs/07-guarda-de-xml-e-lgpd.md)) em armazenamento próprio, além do emissor.
8. **Se o cliente usa ERP ou contabilidade**, integre em vez de duplicar ([doc 08](docs/08-integrar-com-erp-e-contabilidade.md)).

## Qual emissor por perfil

| Perfil | Opção | Por quê |
|---|---|---|
| SaaS que emite serviço e produto, volume baixo | Focus NFe (Solo ou Start) | API única para NFS-e, NF-e e NFC-e, teste de 30 dias, preço por documento publicado |
| Só NFS-e, poucas notas por mês | NFE.io | Planos de NFS-e com franquia publicada |
| Loja física com NFC-e e contingência offline | Focus NFe Retail ou PlugNotas | NFC-e com preço por nota baixo (Focus) ou módulo offline (PlugNotas) |
| Plataforma com muitos CNPJs de clientes | Focus NFe Growth ou Enterprise, ou PlugNotas | CNPJs ilimitados no plano ou preço sob contato |
| Cliente já usa ERP | Emitir pelo ERP (Omie, Bling, Conta Azul) | Evita duas fontes de verdade; doc 08 |
| MEI com poucas notas de serviço | Emissor nacional do gov.br | Gratuito; sem integração por API para o MEI |

Preços e planos estão no [doc 02](docs/02-emissor-via-api.md), conferidos em 2026-11-25.

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Qual nota emitir | [docs/01-qual-nota-emitir.md](docs/01-qual-nota-emitir.md) | NFS-e, NF-e, NFC-e e regime tributário |
| Emissor via API | [docs/02-emissor-via-api.md](docs/02-emissor-via-api.md) | Focus NFe, eNotas, NFE.io, PlugNotas com preço |
| NFS-e nacional | [docs/03-nfse-nacional-e-padroes-municipais.md](docs/03-nfse-nacional-e-padroes-municipais.md) | Padrão nacional, municípios, IBS e CBS |
| Cadastro fiscal | [docs/04-cadastro-fiscal.md](docs/04-cadastro-fiscal.md) | Cliente, produto, NCM, CFOP, CNAE, alíquotas |
| Fluxo de emissão | [docs/05-fluxo-pagamento-emissao-webhook.md](docs/05-fluxo-pagamento-emissao-webhook.md) | Pagamento, emissão, webhook, PDF e XML |
| Cancelar e corrigir | [docs/06-cancelamento-correcao-e-contingencia.md](docs/06-cancelamento-correcao-e-contingencia.md) | Cancelamento, carta de correção, contingência |
| Guarda e LGPD | [docs/07-guarda-de-xml-e-lgpd.md](docs/07-guarda-de-xml-e-lgpd.md) | Prazo de guarda, armazenamento, dados pessoais |
| ERP e contabilidade | [docs/08-integrar-com-erp-e-contabilidade.md](docs/08-integrar-com-erp-e-contabilidade.md) | Omie, Bling, Conta Azul |

## Checklist

- [ ] Tipo de nota e regime tributário confirmados com o contador e anotados no `README`.
- [ ] Emissor escolhido, com ambiente de homologação separado do de produção (tokens diferentes).
- [ ] Certificado digital A1 (quando exigido) enviado ao emissor, fora do Git, com a data de vencimento monitorada.
- [ ] Emissão assíncrona: o pedido guarda `ref`, status e chave; a tela nunca presume que a nota saiu.
- [ ] Webhook do emissor com resposta rápida, fila e idempotência pela `ref` e pelo status.
- [ ] Campos fiscais validados antes de emitir (CPF/CNPJ, endereço, NCM, CFOP, código do serviço).
- [ ] Cancelamento e carta de correção respeitam prazo e ficam registrados com quem pediu.
- [ ] XML e PDF copiados para armazenamento próprio com retenção definida.
- [ ] Alerta quando a nota fica rejeitada ou parada em processamento.
- [ ] Campos de IBS e CBS previstos no cadastro, mesmo que o emissor ainda os preencha sozinho.

## Regras de uso

- **Regra fiscal é do contador.** O agente implementa o que o contador decidiu; não invente alíquota, CFOP ou enquadramento.
- **Prazos e datas só conferidos.** A reforma tributária mudou o cronograma várias vezes; diga a data da conferência e peça para confirmar na fonte antes de afirmar um prazo.
- **Homologação antes de produção.** Nota autorizada em produção tem valor fiscal e só se desfaz por cancelamento dentro do prazo.
- **O emissor é a fonte da verdade** da autorização; a volta da chamada ou a tela não é prova de nota emitida.
- **Dinheiro em centavos, XML sem edição.** O XML autorizado nunca é alterado nem reconstruído; guarde o original.
- **Certificado é segredo.** Arquivo e senha ficam no cofre do ambiente (skill `security` e `infra`, doc 09).
- **Fronteiras.** Pagamento e webhook são da `integrations`; valores, auditoria e dados pessoais da `data`; fluxo e regra da `product`; certificado e segredos da `security`.

## Quando a lista não cobre

Conhecimento de transporte (CT-e), manifesto (MDF-e), nota de energia e telecom, emissão de nota de entrada (devolução, importação), SPED e obrigações acessórias, cálculo de imposto próprio e apuração ficam fora desta skill. Diga isso ao usuário e cubra com o contador e a documentação oficial.

## Validade dos dados

Preços, planos, prazos e cronograma da reforma tributária foram conferidos em 2026-11-25 nas fontes oficiais e mudam com frequência. Cada documento tem a linha "Verificado em". Onde a fonte não publicou o valor, o texto diz isso em vez de estimar.
