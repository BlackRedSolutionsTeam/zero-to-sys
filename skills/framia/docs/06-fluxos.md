# Fluxos

> Desenhar o fluxograma de cada jornada do sistema, com decisões e caminhos de erro, ligado às telas.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/flows |
| **Categoria** | Fluxo |
| **Ferramentas do MCP** | `get_flow_page`, `create_flow_node`, `update_flow_node`, `delete_flow_node`, `create_flow_edge`, `update_flow_edge`, `delete_flow_edge`, `create_page` (`kind: flow`) |
| **Verificado em** | 2026-11-26 |

## O que é

Cada página de design tem a sua página de fluxo: no editor, o botão **Fluxo** no alto alterna com **Design**. O fluxo é um diagrama de cartões e setas. Ele não é o protótipo: o protótipo mostra o que o usuário clica; o fluxo mostra a regra, inclusive o que acontece fora da tela (pagamento confirmado, e-mail enviado, rotina agendada).

Apagar a página apaga o fluxo dela; duplicar a página copia só o design.

## Formas

| Forma | Use para |
|---|---|
| Início, Fim | Onde a jornada começa e onde termina (pode ter mais de um fim) |
| Etapa | Uma ação do usuário ou do sistema |
| Decisão | Uma pergunta com ramos (Sim / Não) |
| Link de frame | Uma etapa que é uma tela; abre o frame |
| Entrada / saída, Banco de dados, Preparação | Dado que entra ou sai, gravação, passo de sistema |
| Nota, Texto, Seção | Explicar uma regra e agrupar um trecho |

## Passo a passo

1. Parta do fluxo escrito na `product` ([fluxos e jornadas](../../product/docs/03-fluxos-e-jornadas.md)): um diagrama por jornada, não um diagrama do sistema inteiro.
2. `get_flow_page` com o `pageId` da página de design da jornada.
3. `create_flow_node` para cada passo, com `shape`, `text`, posição e tamanho. Etapa que é tela leva `frameId`.
4. `create_flow_edge` entre os cartões, com `label` nas saídas de decisão ("Sim", "Não", "Pagamento recusado").
5. Desenhe os caminhos de erro e os que voltam: horário ocupado, pagamento recusado, sem permissão, sessão expirada.
6. Confira no editor ou peça à pessoa para usar **Organizar como fluxograma** se os cartões ficaram embolados.

Regras de desenho:

- Leitura de cima para baixo ou da esquerda para a direita, uma direção por diagrama.
- Texto do cartão com verbo e nas palavras do cliente: "Escolhe o horário", não "Seleção de slot".
- Toda decisão tem todos os ramos saindo, com rótulo.
- Regra de negócio citada pelo id (`RN-04`) numa nota ao lado do passo.
- Linha tracejada para o que é assíncrono ou do sistema (webhook, fila, e-mail).

## Encaixe por tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS e sistema interno com aprovações e papéis | ✅ Ótimo | Mostra quem faz o quê e os desvios |
| API, integração, worker | ✅ Ótimo | O fluxo é a sequência de chamadas e eventos; substitui as telas |
| App mobile | ✅ Ótimo | Offline e notificação entram como ramos |
| Landing | 🟡 Serve | Um fluxo curto até a conversão |
| CRUD simples de uma tela | ❌ Evite | O protótipo já diz tudo |

## Quando é bom

- **Mostra o que a tela não mostra:** o que o sistema faz entre um clique e outro.
- **Acha buraco cedo:** ramo sem destino é funcionalidade que faltou no backlog.
- **Liga com o resto:** o requisito aponta para o fluxo (`flowPageIds`), e o cartão aponta para a tela.

## Quando é ruim

- **Um fluxo gigante:** ninguém lê. Divida por jornada.
- **Só o caminho feliz:** o fluxo existe justamente para os desvios.
- **Repetir o protótipo:** cartão por tela, sem decisão nem regra, não acrescenta nada.

## Combina com

- [Telas e protótipo](05-telas-e-prototipo.md): cada link de frame abre a tela.
- [Requisitos e vínculos](09-requisitos-e-vinculos.md): **Ligar um fluxo** no requisito.
- [Regras de negócio](../../product/docs/05-regras-de-negocio.md): a máquina de estados que o fluxo percorre.
