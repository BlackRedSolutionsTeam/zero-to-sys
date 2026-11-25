# Cancelamento, carta de correção e contingência

> Cancele rápido, corrija só o que a carta de correção permite e deixe o emissor cuidar da contingência quando a SEFAZ ou a prefeitura cair.

| | |
|---|---|
| **Referência** | https://doc.focusnfe.com.br (Cancelar NF-e, Carta de Correção, Contingência automática SVC, Contingência offline NFC-e), https://www.nfe.fazenda.gov.br, legislação estadual do ICMS |
| **Categoria** | Operação |
| **Tipo** | Prática de correção de erro em nota fiscal |
| **Vale para** | NF-e, NFC-e e NFS-e emitidas por API |
| **Verificado em** | 2026-11-25 |

## O que é

- **Cancelamento:** anula a nota. Exige justificativa e vale só dentro de um prazo.
- **Carta de correção eletrônica (CC-e):** corrige campos que não alteram valor, imposto, destinatário nem data (por exemplo, dado do transportador). Existe para NF-e.
- **Inutilização:** declara que uma numeração foi pulada e não será usada.
- **Contingência:** meio alternativo de emitir quando o serviço principal da SEFAZ está fora; para NF-e é o **SVC** (SVC-AN ou SVC-RS, conforme o estado) e para NFC-e há emissão offline.

## Por que usar

- **Evita multa:** nota errada sem cancelar ou corrigir gera diferença de imposto.
- **Venda não para:** a contingência deixa emitir com a SEFAZ fora.
- **Rastro:** o evento fica no XML e na SEFAZ.

## Quando usar

- Venda desfeita, valor errado ou cliente errado: cancelar.
- Erro em dado acessório da NF-e: carta de correção.
- Queda da SEFAZ ou internet: contingência.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Loja virtual | ✅ Ótimo | Pedido cancelado ou devolvido exige cancelamento ou nota de devolução |
| SaaS com NFS-e | ✅ Ótimo | Erro de valor ou tomador exige cancelamento no município |
| Loja física | ✅ Ótimo | NFC-e com prazo curto e contingência offline |
| Sistema interno | 🟡 Serve | Poucos casos; tela simples de cancelamento |
| Venda a prazo com mercadoria já enviada | 🟡 Serve | Passado o prazo, o caminho é outro (nota de devolução); consulte o contador |

## Quando é bom

- **Tela com motivo obrigatório:** a justificativa vira o texto enviado ao fisco.
- **Evento síncrono:** no Focus NFe, cancelar NF-e, NFC-e, NFS-e e emitir carta de correção respondem na hora.
- **Contingência automática:** o Focus NFe tem mecanismo de SVC automático para NF-e.

## Quando é ruim

- **Cancelar depois do prazo:** a SEFAZ rejeita; o caminho é outro (nota de devolução, estorno, conforme o contador).
- **Usar carta de correção para valor ou imposto:** não é permitido.
- **Deixar qualquer usuário cancelar:** é ação fiscal; restrinja por papel e registre quem fez (skill `security`, doc 04, e `data`, doc 07).
- **Cancelar sem estornar o pagamento:** os dois lados precisam andar juntos.

## Como começar

### Prazos

| Documento | Prazo de cancelamento | Observação |
|---|---|---|
| NF-e | Até 24 horas após a autorização na documentação do Focus NFe | Os estados podem fixar prazos diferentes (há casos de 2 horas e de prazo maior com multa); confira a legislação do estado do emitente |
| NFC-e | Até 30 minutos na documentação do Focus NFe | Confira o estado |
| NFS-e | Definido pelo município ou pelo padrão nacional | Consulte o município; cancelar muda a apuração do ISS |
| Carta de correção | Até 20 por NF-e, texto entre 15 e 1.000 caracteres (fontes secundárias; confirme no manual da NF-e) | Não corrige valor, imposto, destinatário nem data de emissão |

Datas conferidas em 2026-11-25; os prazos estaduais mudam, então trate esta tabela como ponto de partida.

### Cancelar e corrigir

```bash
curl -u "$FOCUS_TOKEN:" -X DELETE "https://api.focusnfe.com.br/v2/nfe/pedido-123" \
  -H "Content-Type: application/json" \
  -d '{"justificativa":"Pedido cancelado a pedido do cliente antes da saida da mercadoria"}'
```

```bash
curl -u "$FOCUS_TOKEN:" -X POST "https://api.focusnfe.com.br/v2/nfe/pedido-123/carta_correcao" \
  -H "Content-Type: application/json" \
  -d '{"correcao":"Corrigido o nome da transportadora para Transportes Exemplo Ltda"}'
```

Confira rota, método e tamanho mínimo da justificativa na página "Cancelar" e "Emitir Carta de Correção" da documentação antes de ir a produção.

### Serviço de cancelamento no sistema

```ts
export async function cancelarNota(notaId: string, usuarioId: string, justificativa: string) {
  if (justificativa.trim().length < 15) throw new Error("Justificativa curta demais");

  const nota = await notas.buscar(notaId);
  if (nota.estado !== "autorizada") throw new Error("Só nota autorizada pode ser cancelada");
  if (!dentroDoPrazo(nota)) throw new Error("Prazo de cancelamento vencido");

  await emissor.cancelar(nota.referencia, justificativa);
  await notas.marcar(nota.referencia, { estado: "cancelada" });
  await auditoria.registrar({ acao: "nota.cancelada", notaId, usuarioId, justificativa });
}
```

`dentroDoPrazo` lê o prazo configurado por tipo de nota e estado, não uma constante.

### Rejeição

Rejeição não é erro do sistema: a nota não foi autorizada. Guarde a mensagem do emissor, mostre ao operador, corrija o cadastro ([doc 04](04-cadastro-fiscal.md)) e reemita com a mesma `ref`, se o emissor permitir, ou com nova `ref`, se o número foi consumido. Em NF-e, número consumido sem uso é inutilizado.

### Contingência

- **NF-e:** o emissor faz a troca para SVC sozinho quando a SEFAZ do estado cai e depois regulariza (Focus NFe, "Contingência automática (SVC)"). Seu sistema só enxerga o status demorar.
- **NFC-e:** a operação offline grava a nota localmente e envia depois; no Focus NFe isso passa por um comunicador offline com rotas para listar e efetivar as pendentes; a PlugNotas tem o módulo NeverStop. A nota em contingência precisa ser transmitida dentro do prazo do estado.
- **NFS-e:** prefeitura fora do ar não tem contingência universal; o job tenta de novo ([filas e jobs](../../integrations/docs/05-filas-e-jobs.md)).

## Decisão rápida

| Situação | Ação |
|---|---|
| Erro de valor, cliente ou item, dentro do prazo | Cancelar e emitir outra |
| Erro em dado acessório da NF-e | Carta de correção |
| Prazo de cancelamento vencido | Nota de devolução ou procedimento do contador |
| Numeração pulada | Inutilizar |
| SEFAZ fora do ar | Contingência (SVC na NF-e, offline na NFC-e) |
| Prefeitura fora do ar | Retry na fila e alerta |
