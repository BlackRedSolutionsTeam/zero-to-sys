# Aceternity UI

> Biblioteca de componentes React com Tailwind e Motion, focada em efeitos visuais animados para landing pages.

| | |
|---|---|
| **Site** | https://ui.aceternity.com |
| **Categoria** | Linha 2 — Componentes, templates e assets |
| **Tipo** | Biblioteca de componentes (copiar e colar) com blocos e templates pagos |
| **Stack** | React, Tailwind CSS, Motion (ex-Framer Motion), Next.js (templates), shadcn CLI |
| **Preço** | Freemium. 100+ componentes gratuitos; Pro pago uma vez: 1 ano US$ 169 (regular US$ 249), Lifetime US$ 199 (regular US$ 299), Team até 10 pessoas US$ 1.590 (regular US$ 1.990). Valores promocionais na data da verificação |
| **Licença** | Componentes gratuitos para uso em projetos React/Next.js; itens Pro sob licença própria (uso comercial ilimitado, sem revenda) |
| **Verificado em** | 2026-11-24 |

## O que é

O Aceternity UI é um catálogo de componentes React estilizados com Tailwind CSS e animados com Motion. O foco é o efeito visual: fundos animados, spotlight, cards 3D, textos que aparecem aos poucos, grids e marquees.

Você não instala um pacote fechado. Copia o código do componente para o seu projeto, ou usa o shadcn CLI, e passa a ser dono do arquivo. O site também oferece um servidor MCP para agentes de IA (Claude Code, Cursor, Codex) buscarem componentes no registro.

Além dos componentes gratuitos, há o plano Pro com blocos prontos (hero, features, pricing etc.), templates completos em Next.js e páginas inteiras.

## Por que usar

- **Tempo:** um hero com spotlight ou fundo animado leva minutos em vez de dias de CSS e animação.
- **Qualidade visual:** o resultado parece trabalho de designer, mesmo sem um no time.
- **Custo baixo:** a parte gratuita é grande e o Pro é pagamento único, não assinatura.
- **Controle:** o código fica no repositório, então dá para editar sem esperar atualização de pacote.

## Quando usar

- Landing page de produto ou lançamento que precisa causar impressão.
- Hero e seções de destaque em um site que no resto é simples.
- Páginas de campanha com prazo curto.
- Projeto com stack React + Tailwind já definida.
- Agência que entrega muitos sites e quer reaproveitar blocos (a licença Pro permite produtos ilimitados para clientes).
- Prototipar visual forte com ajuda de um agente de IA via MCP.

## Para que tipo de site

| Tipo de site/projeto | Encaixe | Por quê |
|---|---|---|
| Landing page / site de marketing | ✅ Ótimo | É o foco da biblioteca; efeitos aumentam impacto e há blocos prontos. |
| Site institucional | 🟡 Serve | Bom para home e hero, mas o excesso de efeito pode soar pouco sério. |
| Portfólio | ✅ Ótimo | Efeitos 3D e de texto ajudam a se destacar; baixo risco de manutenção. |
| Blog/conteúdo | 🟡 Serve | Útil só em capa e cabeçalho; no texto corrido animação atrapalha a leitura. |
| E-commerce | 🟡 Serve | Bom em páginas de campanha; evite no catálogo e checkout por peso e foco. |
| SaaS / app web | 🟡 Serve | Marketing do SaaS sim; telas internas do produto não. |
| Dashboard / painel admin | ❌ Evite | Animação pesada e pouca acessibilidade não combinam com uso intenso de dados. |
| MVP / protótipo | ✅ Ótimo | Visual polido rápido, com código copiado e fácil de trocar depois. |
| Sistema interno corporativo | ❌ Evite | Efeitos não agregam valor e custam performance e manutenção. |
| App mobile | ❌ Evite | É web (React DOM); não serve para app nativo. |

## Quando é bom

- **Efeitos prontos e distintos:** spotlight, cards 3D e fundos animados são difíceis de fazer do zero e aqui já vêm resolvidos.
- **Código no seu repositório:** copiar e colar evita lock-in de pacote e permite ajustar qualquer detalhe.
- **Tailwind puro:** as classes seguem o que o time já usa, então tema e cores se adaptam facilmente.
- **Pagamento único:** o Pro não vira mensalidade; a licença de 1 ano vale por um ano de atualizações (renovação opcional) e o Lifetime cobre atualizações futuras.
- **Licença amigável a agências:** permite produtos finais ilimitados para si ou clientes.
- **Integra com IA:** o MCP e o shadcn CLI deixam um agente inserir componentes sem copiar à mão.

## Quando é ruim

- **Peso de JavaScript:** as animações dependem do Motion, como o próprio site diz ("Tailwind CSS and Framer Motion components", ui.aceternity.com, 2026-11-24). Meça o peso no seu build (ex.: `vite build` ou `next build` mostram o tamanho de cada chunk). Muitos efeitos na mesma página prejudicam LCP e celulares fracos.
- **Acessibilidade:** a página de docs (ui.aceternity.com/docs, 2026-11-24) não menciona acessibilidade nem `prefers-reduced-motion`. Revise foco, contraste e teclado você mesmo.
- **Manutenção:** o código é copiado, então correções e melhorias da biblioteca não chegam sozinhas. Cada componente vira dívida do seu time.
- **Visual reconhecível:** muitos sites usam os mesmos efeitos. A marca pode ficar genérica se você não personalizar.
- **Excesso de efeito:** animação demais distrai do conteúdo e da conversão. Uma ou duas por tela bastam.
- **Fora do ecossistema React/Tailwind:** não serve para Vue, Svelte, WordPress puro ou mobile nativo.
- **Pro tem limites de licença:** não pode revender nem criar templates derivados para marketplaces. Componentes de terceiros podem ter licença própria.
- **Fontes enviesadas:** a maior parte do que se encontra online sobre comparações é publicada pelo próprio Aceternity ou por concorrentes. Teste com seu caso.

## Como começar

Os componentes podem ser copiados do site ou instalados pelo shadcn CLI (a documentação oficial confirma o uso do CLI, mas a página consultada não trazia o comando exato de cada componente; copie o comando na página do componente).

1. Crie um projeto Next.js com Tailwind:
   ```bash
   npx create-next-app@latest
   ```
2. Escolha um componente em https://ui.aceternity.com e siga o comando de instalação mostrado nele.
3. Garanta que o Motion esteja instalado (os componentes dependem dele) e que exista o utilitário `cn` (padrão do shadcn).
4. Para IA: configure o MCP conforme https://ui.aceternity.com/docs/cli#mcp-server.

Os templates oficiais usam Next.js 15, Tailwind v4 e Motion for React.

## Combina com / alternativas

- [shadcn/ui](01-shadcn-ui.md): base de componentes funcionais e acessíveis; use o Aceternity só para os efeitos de destaque.
- [Magic UI](02-magic-ui.md): concorrente direto, com efeitos animados e também foco em landing pages.
- Alternativas de fora: React Bits, Chakra UI (mais acessibilidade e tema), Framer Motion direto.

## Decisão rápida

- **Use se:** a meta é uma landing page ou portfólio que impressione, o time usa React + Tailwind e há prazo curto.
- **Evite se:** o projeto é dashboard, sistema interno, app mobile ou exige acessibilidade e performance rigorosas em todas as telas.
