# Caixa de entrada / atendimento

> Três colunas para atender com rapidez: quem está esperando, a conversa aberta e tudo o que se sabe sobre o contato.

| | |
|---|---|
| **Tipo de sistema** | Central de atendimento, caixa de entrada compartilhada, chat de suporte e vendas |
| **Exemplo** | [08-inbox-chat.html](../examples/08-inbox-chat.html) (marca fictícia "Ponte Atendimento") |
| **Layout base** | Três colunas: lista de conversas, conversa aberta, painel de contexto do contato |
| **Referências reais** | Front https://front.com · Intercom https://www.intercom.com · Help Scout https://www.helpscout.com · Missive https://missiveapp.com (exemplos de produtos do segmento; sites conferidos em 2026-11-24) |
| **Componentes** | shadcn/ui (ScrollArea, Avatar, Badge, Tabs, Textarea, Sheet, Skeleton, Tooltip) e Lucide para os ícones. Fontes: ui.shadcn.com/docs/components e lucide.dev, conferidas em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

Uma tela de trabalho para quem responde pessoas o dia todo. À esquerda, a fila de conversas, com busca, filtros e contador de não lidas. No centro, a conversa aberta com mensagens, anexos e a caixa de resposta. À direita, o contexto do contato: dados, etiquetas e histórico. O atendente não troca de tela para saber quem é o cliente nem o que ele já pediu.

## Por que este layout

- A fila fica sempre à vista ao lado da conversa aberta (340 px e flexível, no exemplo).
- O contexto do contato fica numa terceira coluna de 320 px.
- A caixa de resposta fica fixa no rodapé da conversa.
- Notas internas têm aba, cor e rótulo próprios, separados da resposta.

## Quando usar

- Atendimento por chat, WhatsApp ou e-mail com mais de uma pessoa na equipe.
- Fila com prioridade, atribuição e etiquetas.
- Quando o histórico do cliente muda a resposta.
- Quando o tempo de primeira resposta é uma métrica do negócio.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Central de atendimento / suporte | ✅ Ótimo | É o caso central |
| Atendimento comercial (pré-venda) | ✅ Ótimo | Conversa e contexto lado a lado |
| E-mail compartilhado de equipe | ✅ Ótimo | Fila, atribuição e notas internas |
| Chat dentro de um marketplace | 🟡 Serve | Use só lista e conversa; o contexto vira painel opcional |
| CRM de funil | 🟡 Serve | Combine com o quadro de [07-crm-kanban.md](07-crm-kanban.md) |
| Rede social / mensageiro pessoal | ❌ Evite | O foco é conversa íntima, sem fila, etiqueta nem atribuição |
| Painel de métricas | ❌ Evite | Use [02-dashboard-analytics.md](02-dashboard-analytics.md) |

## Anatomia do layout

```
┌────────────────┬─────────────────────────────────┬───────────────┐
│ Caixa de entr. │ (HP) Helena Prado   [ Resolver ] │ Contato       │ 56 px
│ [Buscar...]    ├─────────────────────────────────┤   (HP)        │
│ Todas Minhas.. │        Hoje, 24 de novembro      │ Helena Prado  │
├────────────────┤ ( msg do cliente )               │ Dados         │
│ ● Helena   09:41│              ( msg da equipe )  │ Etiquetas     │
│   Pedido...  2 │ [ nota interna ]                 │ Histórico     │
│ ○ Otávio   09:12│ [ anexo.pdf ]                   │ ...           │
│ ○ Larissa  Ont.│ ( digitando... )                 │               │
│ ...            ├─────────────────────────────────┤               │
│ Ver estado: .. │ [Responder|Nota] caixa de texto  │               │
│                │ anexo  rápidas  emoji   [Enviar] │               │
└────────────────┴─────────────────────────────────┴───────────────┘
   340 px               flexível                         320 px
```

- **Lista:** 340 px. Cabeçalho de 56 px, busca de 36 px, filtros em pílulas (Todas, Minhas, Não lidas) com contagem. Cada conversa tem padding de 12 x 16 px, avatar de 40 px, nome, hora, assunto, prévia de uma linha, etiqueta e canal. Não lida: assunto em negrito e selo com a contagem. Selecionada: fundo suave e faixa de 3 px na cor da marca.
- **Conversa:** coluna flexível. Cabeçalho de 56 px com contato, canal, responsável e o botão "Resolver". Mensagens com largura máxima de 72% (até 520 px), 4 px entre mensagens do mesmo autor, 16 px de margem lateral. A rolagem abre sempre na mensagem mais recente.
- **Caixa de resposta:** campo de 56 px de altura mínima, com abas Responder e Nota interna, anexo, respostas rápidas, emoji, dica do `Enter` e botão Enviar.
- **Contexto:** 320 px. Perfil, dados, etiquetas, histórico e nota do contato.
- **Tablet (até 1180 px):** a lista passa a 320 px e o contexto sai da grade: abre como painel sobreposto pelo botão de informação do cabeçalho da conversa.
- **Celular (até 760 px):** uma coluna por vez, em pilha: lista, conversa, contexto. Botão de voltar no cabeçalho de cada tela; a mensagem ocupa até 86% da largura.

## Tokens do exemplo

| Token | Claro (padrão) | Escuro |
|---|---|---|
| Fundo / superfície / apoio | `#f4f6f8` / `#ffffff` / `#f1f4f7` | `#0f1418` / `#151b21` / `#1b232b` |
| Borda / borda forte | `#e2e7ec` / `#cbd3dc` | `#242e38` / `#34414e` |
| Texto / suave / apagado | `#18212b` / `#566371` / `#7a8794` | `#e6ebf0` / `#9aa7b4` / `#74828f` |
| Marca (verde-azulado) | `#0d7f73` | `#2fb5a5` |
| Balão recebido | fundo `#ffffff`, borda `#e2e7ec` | fundo `#151b21`, borda `#242e38` |
| Balão enviado | `#0d7f73` com texto branco | `#1d7f74` |
| Nota interna | fundo `#fff6dc`, borda `#ecd48a` | fundo `#2e2710`, borda `#6b5a22` |
| Etiquetas | verde, azul, âmbar e vermelho de baixa saturação | mesmas famílias em tons escuros |
| Avatares | 6 cores fixas por contato, texto branco, iniciais | igual |
| Fonte | Inter, com pilha do sistema (não carrega de CDN) | igual |
| Escala de texto | 11 (selo) · 12 (apoio) · 13 (prévia) · 14 (base) · 16 (título) · 22 (avatar grande) | igual |
| Raio | 4 px (etiqueta) · 8 px (botão, campo) · 12 px (anexo, caixa) · 16 px (balão, com 4 px no canto da cauda) | igual |
| Sombra | só no painel de contexto sobreposto | igual, mais forte |
| Espaçamento | escala de 4 / 8 px (4, 8, 12, 16, 24) | igual |

## Componentes e padrões essenciais

- **Item de conversa:** avatar com iniciais, nome, hora, assunto, prévia, etiqueta, canal e selo de não lidas.
- **Busca e filtros:** por nome, pedido ou texto; filtros Todas, Minhas, Não lidas, com contagem.
- **Balões:** recebido à esquerda com avatar, enviado à direita na cor da marca, hora e status (enviado, lido) abaixo.
- **Anexos:** arquivo com ícone, nome e tamanho; imagem com proporção reservada para não saltar a rolagem.
- **Nota interna:** visual diferente (amarelo) e aba própria na caixa de resposta.
- **Eventos do sistema:** "etiqueta adicionada", "conversa atribuída", em linha central e discreta.
- **Indicador de digitação** e separador de dia.
- **Caixa de resposta:** o exemplo mostra a dica "Enter envia", mas não implementa o envio. Atalhos como `Shift+Enter` para quebrar linha e `/` para respostas rápidas ficam por sua conta.
- **Painel de contexto:** dados, etiquetas, histórico e responsável.
- **Estado vazio:** "Tudo em dia", quando a fila está zerada (o exemplo mostra esse). Um estado "Selecione uma conversa" para quando nada está aberto não existe no exemplo.
- **Estado carregando:** linhas de esqueleto na lista, no lugar das conversas.
- **Estado de erro:** mensagem na lista com botão "Tentar de novo"; o exemplo mostra só o erro da lista. Falha de envio na própria mensagem, com opção de reenviar, não existe no exemplo.
- **Tema claro e escuro**, foco visível (WCAG 2.2, SC 2.4.7, AA) e contraste mínimo de 4,5:1 para texto normal (SC 1.4.3, AA), w3.org/WAI/WCAG22/Understanding, 2026-11-24.

## Quando é bom

- Fila, conversa e contexto do contato aparecem na mesma tela.
- Filtros (Todas, Minhas, Não lidas) e contagem ficam no topo da fila.
- Abaixo de 760 px, o exemplo troca as três colunas por uma pilha com botão de voltar.

## Quando é ruim

- **Três colunas no celular:** o exemplo usa pilha (lista, conversa, contexto) com botão de voltar abaixo de 760 px.
- **Não lida só por cor:** o WCAG 2.2, SC 1.4.1 (nível A) não aceita cor como único meio visual (w3.org/WAI/WCAG22/Understanding/use-of-color.html, 2026-11-24). O exemplo usa também negrito e o selo com número.
- **Nota interna parecida com resposta:** no exemplo, a nota tem cor, aba e rótulo próprios; a cor sozinha não basta (SC 1.4.1).

## Como começar

1. Abra [08-inbox-chat.html](../examples/08-inbox-chat.html), reduza a janela até 390 px e veja a pilha; use "Ver estado" na lista para ver carregando, vazio e erro.
2. Copie as variáveis do `:root` (e do tema escuro) e a grade `grid-template-columns: 340px 1fr 320px`.
3. Troque a marca: `--brand`, `--out-bg` e as cores de etiqueta.
4. Monte com a skill `design`: ScrollArea, Avatar, Badge, Tabs, Textarea, Sheet (contexto no tablet), Skeleton e ícones Lucide.
5. Ligue os dados reais e o tempo real: o MDN descreve a WebSocket API como sessão interativa de duas vias entre navegador e servidor, e os server-sent events como envio de dados do servidor para a página a qualquer momento (developer.mozilla.org/en-US/docs/Web/API/WebSockets_API e /Server-sent_events, 2026-11-24).

## Combina com / alternativas

- [01-fundamentos.md](01-fundamentos.md): tokens, contraste e escala de espaço.
- [07-crm-kanban.md](07-crm-kanban.md): para acompanhar a venda ou o chamado em etapas.
- [03-admin-crud.md](03-admin-crud.md): para o cadastro de contatos e de respostas rápidas.
- [04-auth-onboarding-configuracoes.md](04-auth-onboarding-configuracoes.md): para canais, equipes e permissões.
- [12-app-mobile.md](12-app-mobile.md): se o atendimento for principalmente pelo celular.

## Decisão rápida

**Use se:** várias pessoas respondem clientes em tempo quase real, e o histórico e as etiquetas do contato mudam a resposta.

**Evite se:** a conversa é pessoal e sem fila, ou o produto é só um formulário de contato com resposta por e-mail.
