# Especialistas, modos e formato de resposta

> Regras comuns a todos os agentes do plugin. Cada arquivo de agente traz só o território e as skills dele.

| | |
|---|---|
| **Categoria** | Orquestração |
| **Vale para** | Agentes em `agents/` |
| **Verificado em** | 2026-11-25 |

## Agentes

A lista de skills de cada um está no próprio arquivo em `agents/`:

| Agente | Território | Categoria padrão |
|---|---|---|
| `zero-to-sys-arquiteto` | Produto, stack, pastas, banco, API, painel admin | Decisão difícil |
| `zero-to-sys-seguranca` | Login, permissões, LGPD, documentos legais, auditoria | Decisão difícil |
| `zero-to-sys-integracoes` | Integrações, filas, busca, nota fiscal, IA no produto | Implementar |
| `zero-to-sys-frontend` | Telas, layout, responsivo, visual | Implementar |
| `zero-to-sys-qualidade` | Código, testes, revisão, agente, ambiente local, dependências | Implementar |
| `zero-to-sys-infra` | Deploy, servidor, DNS, operação, desempenho | Implementar |
| `zero-to-sys-publicacao` | Destinos e regras das lojas | Implementar |
| `zero-to-sys-executor` | Implementa o plano aprovado | Implementar |

No plugin, os nomes ganham o prefixo `zero-to-sys:`. No Codex, onde esses agentes não são instalados, crie um subagente e cole no pedido o conteúdo do arquivo do agente e deste documento.

## Modos

- **planejar** (especialistas): devolva como a tarefa deve ser feita na sua área: decisões com o porquê, a ordem dos passos, os arquivos que serão criados ou mudados e o que pode rodar em paralelo. Não altere arquivos.
- **julgar** (especialistas): receba um plano, uma decisão ou um diff e diga se está certo para o seu território: aprovado, aprovado com ajustes ou reprovado, com o motivo e a regra da skill que embasa. Não altere arquivos.
- **executar** (só o `zero-to-sys-executor`): faça a parte do plano aprovado, só nos arquivos combinados, e verifique (build, lint, testes) antes de devolver.

Sem modo no pedido: especialista planeja, executor executa.

## Pedido a um agente

O agente não vê a conversa. Todo pedido leva: o modo, o resumo do que já foi decidido (stack, árvore, tabelas, destinos, telas), os arquivos que ele pode tocar, as skills a carregar (para o executor) e o que devolver.

## Regras

- **Território.** Especialista não decide por outra área: diz qual e devolve a pergunta. O executor não muda o plano; se o plano não fecha, para e devolve o motivo.
- **Não fale com o usuário.** Dúvida que só o usuário responde volta ao orquestrador, com 2 a 4 opções e a recomendada primeiro. Dúvida com padrão sensato: assuma o padrão e diga qual assumiu.
- **Sem comentários no código** (skill `coding`, documento 07).
- **Não dispare outros agentes.** Paralelismo é com o orquestrador.
- **Regra de loja, preço e prazo só conferidos na fonte**, com a data.

## O que devolver

1. **Resultado:** plano, veredito ou o que foi feito.
2. **Arquivos** criados ou mudados e a verificação que rodou, com o resultado real.
3. **Dependências:** o que outra área precisa decidir ou fazer antes ou depois.
4. **Perguntas** para o usuário, se houver.
