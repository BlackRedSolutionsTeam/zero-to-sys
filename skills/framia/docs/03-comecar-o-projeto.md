# Começar o projeto

> Criar o projeto de um modelo ou em branco, escolher o design system inicial e fixar como as telas se organizam.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/start-from-template e https://framia.com.br/pt-br/docs/screen-layout |
| **Categoria** | Projeto |
| **Ferramentas do MCP** | `list_workspaces`, `list_projects`, `list_templates`, `get_template`, `create_project`, `get_project`, `set_project_layout`, `create_screen`, `organize_layout` |
| **Verificado em** | 2026-11-26 |

## Como o Framia se organiza

Uma equipe (workspace) guarda projetos. Um projeto tem branches: a **Principal** e as outras. Cada branch guarda o documento inteiro: páginas, frames e camadas, fluxo, banco, enums, vínculos, perfis de acesso, rotas, requisitos, biblioteca e memória. O que o agente edita aparece ao vivo para quem está no editor.

## Passo a passo

1. `list_workspaces`: escolha a equipe dona. Confirme com o usuário se houver mais de uma.
2. `list_projects`: veja se o projeto já existe antes de criar outro. Projeto conta no plano.
3. Compare o negócio com `list_templates`. Bateu com um modelo, proponha partir dele; não bateu, projeto em branco.
4. Mostre ao usuário: equipe, nome, modelo ou em branco, design system. Espere o ok.
5. `create_project` com `workspaceId`, `name`, `description`, e `templateSlug` e `designSystem` quando houver modelo.
6. `get_project`: guarde o id do projeto, a branch e o `layout`.
7. Ajuste a organização das telas, se a padrão não servir.

## Modelos

Um modelo é um projeto completo copiado: telas de desktop e celular ligadas num protótipo, fluxos, banco, enums, rotas, requisitos, perfis, biblioteca e memória. Nada é gerado por IA na criação, e uma versão nova do modelo não altera projeto já criado.

| Slug | Modelo | Design system padrão | Traz |
|---|---|---|---|
| `agendamento` | Agendamento de serviços | `warm` | 31 telas, 23 tabelas, 75 rotas |
| `loja-virtual` | Loja virtual | `light` | 36 telas, 26 tabelas, 77 rotas |
| `cursos-online` | Cursos online e área de membros | `dark` | 32 telas, 26 tabelas, 80 rotas |
| `crm-vendas` | CRM de vendas | `light` | 28 telas, 27 tabelas, 76 rotas |
| `delivery` | Delivery e cardápio digital | `warm` | 29 telas, 32 tabelas, 72 rotas |
| `clinica` | Clínica e consultório | `light` | 26 telas, 30 tabelas, 70 rotas |
| `assinaturas` | Assinaturas e cobrança recorrente | `light` | 26 telas, 26 tabelas, 69 rotas |
| `atendimento` | Atendimento (help desk) | `dark` | 26 telas, 29 tabelas, 68 rotas |

A lista muda: chame `list_templates` antes de propor, e `get_template` para ver o que o modelo traz.

### Modelo ou em branco

| Situação | Escolha | Por quê |
|---|---|---|
| O negócio é um dos modelos, com poucas diferenças | Modelo | Chega com telas, banco, API e requisitos; o trabalho é cortar e ajustar |
| O negócio lembra um modelo, mas o fluxo principal é outro | Em branco | Desmontar um modelo custa mais que desenhar o que o escopo pede |
| Plano Starter | Em branco | Os modelos passam de 10 tabelas e de 10 páginas |
| API ou worker, sem tela | Em branco | Só banco, rotas, fluxos e requisitos |

Partindo de um modelo, a primeira tarefa é cortar: apague as telas, tabelas, rotas e requisitos que estão fora do MVP aprovado na `product`. Modelo não é escopo.

## Design system inicial

`designSystem` aceita `light` (Claro), `warm` (Caloroso) e `dark` (Escuro). É o ponto de partida dos tokens, não a marca do cliente: a marca entra no [doc 04](04-design-system.md). Sem marca definida, escolha pelo público e diga qual assumiu.

## Organização das telas

O `layout` de `get_project` diz como o projeto arruma as telas e quais formatos tem.

| Arranjo | `mode` | Quando |
|---|---|---|
| Tela por página | `page-per-screen` | Padrão de projeto novo; uma página por tela, um frame por formato |
| Fluxo por página | `page-per-flow` | Muitas telas com limite de páginas apertado; uma página por jornada |
| Formato por página | `page-per-device` | Desktop e celular trabalhados em separado |
| Tudo em uma página | `single-page` | Sistema bem pequeno ou plano Starter |
| Canvas livre | `free` | Projeto antigo; evite em projeto novo |

Formatos: Desktop (1440 × 900), Tablet (768 × 1024) e Mobile (390 × 844). Escolha os formatos pelo que a skill `user-experience` definiu: só o que o sistema vai ter de verdade.

- `set_project_layout` devolve uma prévia; só vale depois de `confirm`. Mostre a prévia ao usuário antes de confirmar em projeto que já tem telas.
- `create_screen` cria a tela no arranjo do projeto: a página e um frame por formato, com nome como `Login · Desktop`. Passe `flowName` para agrupar por jornada e `states` para já criar os estados.
- `organize_layout` devolve os frames ao lugar do arranjo; `dryRun` mostra antes.

## Quando é ruim

- **Criar o projeto sem escopo aprovado:** o protótipo vira o lugar onde o escopo é discutido, e cresce sem corte.
- **Aceitar o modelo inteiro:** o cliente vê 30 telas e passa a esperar todas.
- **Frames com `x` e `y` soltos:** saem do arranjo e bagunçam o canvas de quem abre o editor.
- **Um projeto por tela ou por módulo:** um sistema é um projeto; módulos são pastas e fluxos.

## Combina com

- [Conta, equipe e planos](01-conta-equipe-e-planos.md): o limite decide modelo e arranjo.
- [Design system](04-design-system.md): o passo seguinte.
- [Escopo do MVP](../../product/docs/02-escopo-do-mvp.md): o que fica e o que sai do modelo.
- [Experiência do usuário](../../user-experience/SKILL.md): quais formatos o projeto precisa.
