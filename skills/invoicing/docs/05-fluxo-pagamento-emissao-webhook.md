# Fluxo: pagamento aprovado, emissão, webhook e envio

> Emita a nota depois que o pagamento é confirmado, trate a emissão como assíncrona e só marque a nota como autorizada quando o webhook do emissor disser.

| | |
|---|---|
| **Referência** | https://doc.focusnfe.com.br (Utilizando webhooks, Cuidados na emissão de documentos assíncronos, Referência), documentação da PlugNotas e da NFE.io |
| **Categoria** | Fluxo |
| **Tipo** | Prática de emissão automática de nota fiscal |
| **Vale para** | Node, Python, .NET, Java, Laravel, Go; emissor por API |
| **Verificado em** | 2026-11-25 |

## O que é

O fluxo tem cinco etapas, cada uma num estado do pedido:

1. **Pagamento aprovado:** webhook do provedor de pagamento ([pagamentos](../../integrations/docs/01-pagamentos.md)).
2. **Emissão pedida:** job manda os dados ao emissor com uma **referência** única e grava `emitindo`.
3. **Processamento:** o emissor assina e envia à SEFAZ ou prefeitura; a resposta inicial só confirma a fila.
4. **Webhook do emissor:** avisa que o documento foi autorizado; rejeição e cancelamento você confirma por consulta (veja "Webhook").
5. **Entrega:** guarda XML e PDF e manda ao cliente.

A **referência** (`ref`) é o identificador da nota no emissor. Reenviar com a mesma `ref` não cria nota nova, e é isso que torna a emissão idempotente.

## Por que usar

- **Cada pagamento gera uma nota só:** a `ref` protege contra duplicata.
- **Falha da prefeitura não derruba o checkout:** a emissão corre em segundo plano.
- **Cliente recebe sem ação humana.**

## Quando usar

- Em qualquer venda com nota obrigatória e pagamento digital.
- Quando a nota é emitida depois (fim do mês), mudando só o gatilho: o job de emissão é o mesmo.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS com assinatura | ✅ Ótimo | Cada cobrança paga gera uma NFS-e |
| Loja virtual | ✅ Ótimo | Pedido pago gera NF-e com transporte |
| Clínica ou serviço avulso | ✅ Ótimo | Consulta paga gera NFS-e |
| Sistema interno | 🟡 Serve | Emissão em lote por rotina agendada |
| Venda no balcão | 🟡 Serve | NFC-e síncrona no ato |
| Sem pagamento online | 🟡 Serve | O gatilho é a ação do operador, o resto é igual |

## Quando é bom

- **Fila com retry:** falha de município vira nova tentativa, não perda ([filas e jobs](../../integrations/docs/05-filas-e-jobs.md)).
- **Webhook com consulta de reserva:** o Focus NFe reenvia com intervalos progressivos por até 48 horas, e depois disso o sistema deve consultar o status com GET na rota do documento.
- **Estado no pedido:** a tela mostra "emitindo" em vez de travar.

## Quando é ruim

- **Emitir antes do pagamento confirmado:** a nota teria de ser cancelada se o pagamento falhar.
- **Emitir dentro da requisição do checkout:** prefeitura lenta derruba a venda.
- **Assumir que a resposta inicial é a nota:** ela só confirma que entrou na fila.
- **Webhook sem verificação:** qualquer um poderia marcar nota como autorizada; use token ou segredo na URL e confirme por consulta ([webhooks](../../integrations/docs/04-webhooks.md)).

## Como começar

### Estados da nota

```
pendente -> emitindo -> autorizada | rejeitada
autorizada -> cancelada
rejeitada -> emitindo
```

```sql
create table nota_fiscal (
  id uuid primary key,
  pedido_id uuid not null references pedidos(id),
  tipo text not null check (tipo in ('nfse', 'nfe', 'nfce')),
  referencia text not null unique,
  estado text not null default 'pendente',
  chave_ou_numero text,
  caminho_xml text,
  caminho_pdf text,
  mensagem_erro text,
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);
```

A restrição `unique` na `referencia` impede duas notas do mesmo pedido.

### Job de emissão

```ts
export async function emitirNota(pedidoId: string) {
  const pedido = await pedidos.buscar(pedidoId);
  const referencia = `pedido-${pedido.id}`;

  const criada = await notas.criarSeNova({ pedidoId, referencia, tipo: "nfse" });
  if (!criada) return;

  const dados = montarNotaServico(pedido);
  const resposta = await fetch(`${process.env.FOCUS_URL}/v2/nfse?ref=${referencia}`, {
    method: "POST",
    headers: {
      Authorization: `Basic ${Buffer.from(`${process.env.FOCUS_TOKEN}:`).toString("base64")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dados),
  });

  if (!resposta.ok) {
    await notas.marcar(referencia, { estado: "rejeitada", mensagem_erro: await resposta.text() });
    return;
  }

  await notas.marcar(referencia, { estado: "emitindo" });
}
```

`FOCUS_URL` é a URL base do ambiente (homologação ou produção). Erro 4xx de validação não deve ser repetido; erro 5xx e timeout entram no retry da fila.

### Webhook

Conferido em 2026-11-25 nas páginas "Webhooks", "Utilizando webhooks" e "Criar" da documentação do Focus NFe (doc.focusnfe.com.br):

- **Rotas:** `POST /v2/hooks` (cria), `GET /v2/hooks` (lista), `GET /v2/hooks/{id}` (consulta) e `DELETE /v2/hooks/{id}` (exclui). Autenticação HTTP Basic com o token como usuário e senha vazia.
- **Corpo de criação:** `event` e `url` são obrigatórios; `cnpj`, `cpf`, `authorization` e `authorization_header` são opcionais. Com os dois últimos, o Focus envia na chamada o cabeçalho que você escolheu, e seu endpoint valida a origem.
- **Um gatilho por evento.** Os eventos de documentos emitidos são `nfe`, `nfce`, `nfse` (NFS-e municipal), `nfsen` (NFS-e nacional), `cte`, `mdfe`, `nfcom`, `dce` e `inutilizacao`, disparados quando o documento é **autorizado**, com os mesmos dados da consulta `GET`. Há ainda eventos de documentos recebidos (`nfe_recebida`, `nfe_recebida_falha_consulta`, `cte_recebida`, `nfsen_recebida`) e da NFC-e (`nfce_contingencia`, `nfce_consulta_automatica`).
- **Reenvio:** cada tipo tem `POST .../{referencia}/hook` para pedir de novo a notificação (por exemplo `POST /v2/nfse/{referencia}/hook`).
- **Resposta do seu endpoint:** HTTP 200 ou 202 imediatamente; o trabalho pesado vai para fila. Em falha, o Focus reenvia com intervalos progressivos por até 48 horas.
- **Não confirmado:** a documentação lida não diz se o gatilho também dispara em rejeição (`erro_autorizacao`) ou cancelamento. Por isso o fluxo abaixo consulta o documento e a rotina de reconciliação procura notas paradas; não conte com o webhook para rejeição.

```ts
app.post("/webhooks/focus/:segredo", express.json(), async (req, res) => {
  if (req.params.segredo !== process.env.FOCUS_WEBHOOK_SEGREDO) return res.sendStatus(401);
  await fila.enfileirar("processar-retorno-nota", { corpo: req.body });
  res.sendStatus(200);
});
```

```ts
export async function processarRetornoNota({ corpo }: { corpo: RetornoEmissor }) {
  const nota = await notas.buscarPorReferencia(corpo.ref);
  if (!nota) return;

  const atual = await emissor.consultar(corpo.ref);
  if (atual.status === "autorizado") {
    const xml = await emissor.baixarXml(corpo.ref);
    const pdf = await emissor.baixarPdf(corpo.ref);
    const caminhoXml = await armazenamento.salvar(`notas/${nota.id}.xml`, xml);
    const caminhoPdf = await armazenamento.salvar(`notas/${nota.id}.pdf`, pdf);
    await notas.marcar(corpo.ref, { estado: "autorizada", caminho_xml: caminhoXml, caminho_pdf: caminhoPdf });
    await fila.enfileirar("enviar-nota-por-email", { notaId: nota.id });
  } else if (atual.status === "erro_autorizacao" || atual.status === "negado") {
    await notas.marcar(corpo.ref, { estado: "rejeitada", mensagem_erro: atual.mensagem });
  }
}
```

Valores de `status` na consulta do Focus NFe (páginas "Consultar" de NFS-e, NFS-e nacional e NF-e, lidas em 2026-11-25): `processando_autorizacao`, `autorizado`, `cancelado` e `erro_autorizacao`; a NFS-e nacional ainda lista `negado`. Em outro emissor, os valores são outros. Consultar o emissor dentro do job, em vez de confiar no corpo do webhook, deixa a ação idempotente e imune a corpo forjado.

### Envio ao cliente

O próprio emissor pode reenviar o e-mail da nota (o Focus NFe tem a operação "Reenviar email"). Se o envio é seu, use o e-mail transacional ([doc 02](../../integrations/docs/02-email-transacional.md)) com XML e PDF anexos e mostre os arquivos na área do cliente (URL assinada, [doc 07](../../integrations/docs/07-armazenamento-de-arquivos.md)).

### Rotina de reconciliação

Uma rotina diária ([rotinas agendadas](../../integrations/docs/06-rotinas-agendadas.md)) consulta as notas em `emitindo` há mais de 30 minutos e as que ficaram `rejeitada`, e alerta quem opera.

## Decisão rápida

| Situação | Ação |
|---|---|
| Pagamento aprovado | Enfileirar a emissão com `ref` única |
| Resposta inicial do emissor | Gravar `emitindo`, nada mais |
| Webhook chegou | Responder 200, enfileirar, consultar status |
| Webhook não chegou em 30 minutos | Consultar o emissor e alertar |
| Rejeição | Mostrar o motivo e permitir reenviar após corrigir (doc 06) |
