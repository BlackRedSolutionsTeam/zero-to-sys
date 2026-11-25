# Experiência por dispositivo

Um documento por tema, cada um com a tabela comparativa de celular, tablet e desktop, regras com números e fonte, erros comuns e código. Os dados foram conferidos nas fontes oficiais em 2026-11-24.

## Base

| Documento | O que responde |
|---|---|
| [01-contexto-de-uso.md](01-contexto-de-uso.md) | O que muda de fato entre os três: como se segura, com o que se aponta, por quanto tempo, onde |

## Por dispositivo

| Documento | O que responde |
|---|---|
| [02-mobile.md](02-mobile.md) | Uma coluna, zona do polegar, uma tarefa por tela, teclado virtual, área segura |
| [03-tablet.md](03-tablet.md) | Retrato e paisagem, lista + detalhe, tela dividida, tablet como dispositivo principal |
| [04-desktop.md](04-desktop.md) | Mouse e teclado, hover, atalhos, densidade, vários painéis, telas largas |

## Por tema

| Documento | O que responde |
|---|---|
| [05-breakpoints-e-layout.md](05-breakpoints-e-layout.md) | Pontos de quebra, container queries, grade fluida, unidades de viewport |
| [06-navegacao.md](06-navegacao.md) | Barra inferior, trilho, barra lateral, hambúrguer, voltar |
| [07-toque-mouse-teclado.md](07-toque-mouse-teclado.md) | Alvo de toque, hover, gestos, atalhos, foco |
| [08-formularios.md](08-formularios.md) | Teclado certo, validação, etapas, seletores |
| [09-tabelas-e-dados.md](09-tabelas-e-dados.md) | Tabela no celular, filtros, paginação, gráficos |
| [10-modais-folhas-e-paineis.md](10-modais-folhas-e-paineis.md) | Modal, folha inferior, drawer, popover, tooltip, toast |
| [11-tipografia-e-densidade.md](11-tipografia-e-densidade.md) | Fonte base, comprimento de linha, densidade confortável e compacta |
| [12-desempenho-e-rede.md](12-desempenho-e-rede.md) | Core Web Vitals, imagens, offline, movimento reduzido |

## Por plataforma

| Documento | O que responde |
|---|---|
| [13-ios-android-web.md](13-ios-android-web.md) | Diferenças entre iOS, Android e web; site responsivo, PWA, híbrido ou nativo |
| [14-acessibilidade.md](14-acessibilidade.md) | Checklist WCAG 2.2 AA: contraste, foco, teclado, rótulos, leitor de tela |
| [15-internacionalizacao.md](15-internacionalizacao.md) | Preparar texto, data, número e moeda para outros idiomas |

## Qual escolher

- **Começando um sistema:** [contexto de uso](01-contexto-de-uso.md) para decidir o dispositivo principal, depois o documento dele.
- **"Deixa responsivo":** [breakpoints e layout](05-breakpoints-e-layout.md) e [navegação](06-navegacao.md); depois o tema de cada parte difícil da tela.
- **A tela tem tabela:** [tabelas e dados](09-tabelas-e-dados.md). É onde a adaptação mais dá errado.
- **A tela tem formulário:** [formulários](08-formularios.md).
- **Algo abre por cima da tela:** [modais, folhas e painéis](10-modais-folhas-e-paineis.md).
- **"No celular está ruim de clicar":** [toque, mouse e teclado](07-toque-mouse-teclado.md).
- **"No celular está lento":** [desempenho e rede](12-desempenho-e-rede.md).
- **"Acessível para todos?":** [Acessibilidade](14-acessibilidade.md).
- **"Vai ter outro idioma?":** [Internacionalização](15-internacionalizacao.md).
- **"Site ou app?":** [iOS, Android e web](13-ios-android-web.md), e a skill `stacks` para a tecnologia.
- **Sistema usado no balcão, no campo ou no leito:** [tablet](03-tablet.md).

## O que ficou fora e por quê

| Tema | Motivo |
|---|---|
| TV e telas de 10 pés | Navegação por controle remoto e distância grande; diretrizes próprias de cada plataforma |
| Relógio e vestíveis | Interações de segundos, tela mínima; diretrizes próprias (watchOS, Wear OS) |
| Carro | Regras de segurança e de distração definidas pela plataforma |
| Realidade mista | Entrada por olhar e mãos; ainda sem padrão comum entre plataformas |
| Interface por voz | Não tem tela; outro conjunto de princípios |
| Totem e autoatendimento | Parecido com tablet, mas com uso em pé, público e sem conta; pede estudo próprio |
| Pesquisa com usuários e testes de usabilidade | É método de trabalho, não diferença entre dispositivos |
| Acessibilidade completa (leitor de tela, WCAG ponto a ponto) | Os documentos cobrem o que muda por dispositivo; a norma inteira merece guia próprio |
