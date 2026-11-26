# Framia

Um documento por etapa do protótipo no Framia, na ordem em que são usadas: entrar, conectar, criar o projeto, fechar o visual, desenhar telas, fluxos, banco e API, registrar os requisitos, aprovar e passar para o código. Passos e limites conferidos em framia.com.br/pt-br/docs em 2026-11-26.

## Entrar e conectar

| Etapa | O que entrega | Doc |
|---|---|---|
| Conta, equipe e planos | Conta criada, equipe do projeto e o plano que comporta o sistema | [01-conta-equipe-e-planos.md](01-conta-equipe-e-planos.md) |
| Conectar o MCP | Link do MCP criado e o Framia respondendo no Claude | [02-conectar-o-mcp.md](02-conectar-o-mcp.md) |

## Montar o protótipo

| Etapa | O que entrega | Doc |
|---|---|---|
| Começar o projeto | Projeto criado de um modelo ou em branco, com a organização das telas | [03-comecar-o-projeto.md](03-comecar-o-projeto.md) |
| Design system | Tokens da marca, temas, fontes, componentes e regras | [04-design-system.md](04-design-system.md) |
| Telas e protótipo | Telas em HTML com estados, conferidas e clicáveis | [05-telas-e-prototipo.md](05-telas-e-prototipo.md) |
| Fluxos | Fluxograma de cada jornada | [06-fluxos.md](06-fluxos.md) |
| Banco e enums | Diagrama de tabelas, relações e enums | [07-banco-e-enums.md](07-banco-e-enums.md) |
| API e perfis | Rotas com quem pode chamar e as telas que chamam | [08-api-e-perfis.md](08-api-e-perfis.md) |
| Requisitos e vínculos | REQ-n com critérios, ligados a telas, rotas e colunas | [09-requisitos-e-vinculos.md](09-requisitos-e-vinculos.md) |

## Aprovar e seguir

| Etapa | O que entrega | Doc |
|---|---|---|
| Aprovação e passagem para o código | Ok do cliente e os artefatos que as outras skills usam | [10-aprovacao-e-passagem-para-o-codigo.md](10-aprovacao-e-passagem-para-o-codigo.md) |

## Por onde começar

- **Nunca usou o Framia:** 01 → 02, depois o resto em ordem.
- **O MCP já responde nesta máquina:** 03 em diante.
- **O Claude não enxerga o Framia:** 02, seção "Quando não conecta".
- **Só quer decidir o visual:** 03 → 04 → 05.
- **O sistema não tem tela (API, worker):** 03 → 07 → 08 → 06 → 09 → 10.
- **O protótipo está pronto e vai começar o código:** 10.
