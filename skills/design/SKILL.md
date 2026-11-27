---
name: design
description: 'Escolhe e aplica UI kits e ícones gratuitos para um visual profissional (shadcn/ui, Magic UI, Aceternity UI, HyperUI, Lucide, Phosphor, Tabler). Use ao criar ou redesenhar uma interface ou quando pedirem "deixar bonito", "qual UI kit" ou "qual biblioteca de ícones".'
---

# design

Guia de decisão para montar interfaces web com visual profissional, usando só UI kits e ícones gratuitos. Cada ferramenta tem um documento em `docs/` com quando usar, para que tipo de site, pontos fortes, limitações, instalação e decisão rápida.

## Como usar esta skill

1. **Descubra o tipo de projeto e a stack** antes de escolher qualquer coisa: tipo de site (landing page, institucional, SaaS, dashboard…), se usa React, se tem Tailwind e se o projeto já tem um UI kit ou set de ícones instalado. Veja o `package.json` e os componentes existentes. O que já está no projeto tem prioridade sobre esta lista.
2. **Escolha as ferramentas pela tabela abaixo.**
3. **Leia o documento de cada ferramenta escolhida** em `docs/` antes de instalar ou escrever código. Confira principalmente "Para que tipo de site", "Quando é ruim" e "Como começar".
4. **Instale pelos comandos de "Como começar"** do documento. Confira a versão na documentação oficial da ferramenta antes de rodar.
5. **Aplique as regras de uso** desta skill ao montar as telas.
6. **Explique a escolha ao usuário em uma ou duas frases**: quais ferramentas e por quê, para aquele tipo de site.

## Qual ferramenta usar

| Projeto | Componentes | Ícones |
|---|---|---|
| SaaS, app web, dashboard, painel admin, sistema interno (React) | shadcn/ui | Lucide; Tabler Icons se faltar ícone |
| Landing page ou site de marketing (React + Tailwind) | shadcn/ui na base, Magic UI para seções animadas, Aceternity UI para um ou dois efeitos de destaque | Lucide ou Phosphor |
| Portfólio (React + Tailwind) | Magic UI ou Aceternity UI, com shadcn/ui na base | Phosphor ou Lucide |
| Site institucional, blog ou landing sem React (HTML, Astro, Laravel, Vue com Tailwind) | HyperUI | Phosphor (CDN ou pacote) ou Tabler Icons |
| MVP ou protótipo rápido | HyperUI sem React; shadcn/ui com React | Lucide |

| Ferramenta | Documento | Papel |
|---|---|---|
| shadcn/ui | [docs/01-shadcn-ui.md](docs/01-shadcn-ui.md) | Base de componentes funcionais e acessíveis em React |
| Magic UI | [docs/02-magic-ui.md](docs/02-magic-ui.md) | Seções e componentes animados para marketing |
| Aceternity UI | [docs/03-aceternity-ui.md](docs/03-aceternity-ui.md) | Efeitos visuais de destaque (hero, fundos, cards) |
| HyperUI | [docs/04-hyperui.md](docs/04-hyperui.md) | Blocos Tailwind em HTML, para qualquer framework |
| Lucide | [docs/05-lucide.md](docs/05-lucide.md) | Ícones padrão, traço único |
| Phosphor | [docs/06-phosphor.md](docs/06-phosphor.md) | Ícones com seis pesos, incluindo fill e duotone |
| Tabler Icons | [docs/07-tabler-icons.md](docs/07-tabler-icons.md) | Catálogo grande de ícones, para telas densas |

## Checklist de toda interface montada com UI kit e ícones

- [ ] Há um único set de ícones no projeto (`grep -E 'lucide|phosphor|tabler' package.json`).
- [ ] Ícones são importados pelo nome, não o pacote inteiro (`grep -rn 'import \* as' src`).
- [ ] A stack tem React e Tailwind quando o kit pede; sem React, o kit é o HyperUI (`grep -E 'react|tailwind' package.json`).
- [ ] shadcn/ui é a base em React e Magic UI ou Aceternity UI só entram por cima (`ls components.json`).
- [ ] Efeito decorativo do Magic UI e do Aceternity UI só está em páginas de marketing ou portfólio, não em dashboard nem painel admin (`grep -rln 'magicui\|aceternity' src`).
- [ ] As transições de entrada e saída que os componentes do kit trazem (diálogo, menu, folha, acordeão, toast) continuam ligadas, e o que o projeto monta por fora também transiciona (abrir e fechar cada um).
- [ ] No máximo dois efeitos do Aceternity UI por página (`grep -rc 'aceternity' src`).
- [ ] `prefers-reduced-motion` é respeitado nos componentes animados (`grep -rn 'prefers-reduced-motion' src`).
- [ ] Cores, fontes, raios e espaçamentos dos componentes copiados foram trocados pelos tokens da marca (`grep -rnE '#[0-9a-fA-F]{3,6}' components`).
- [ ] Nenhum item pago foi usado (`grep -rni 'pro' components.json package.json`).

## Regras de uso

- **Um set de ícones por projeto.** Misturar Lucide, Phosphor e Tabler deixa traços e proporções inconsistentes. Se o projeto usa shadcn/ui, o padrão é Lucide; só troque o set inteiro, nunca ícone a ícone.
- **Sempre importe ícones pelo nome** (`import { Camera } from "lucide-react"`), nunca o pacote inteiro, para não inflar o bundle.
- **shadcn/ui é a base em React.** Magic UI e Aceternity UI entram por cima dela, pela mesma CLI. Não use os dois como substituto de formulários, tabelas, diálogos e navegação.
- **Efeito decorativo só onde vende.** Magic UI e Aceternity UI são para páginas de marketing e portfólio. Não use em dashboard, painel admin ou sistema interno: atrapalham a leitura e pesam.
- **Exceção: movimento funcional vale em toda tela.** A regra acima corta enfeite (fundo animado, spotlight, texto que revela), não transição. Troca de tela, diálogo, menu, folha, aba, toast, hover e conteúdo que carrega entram e saem suaves em qualquer sistema, inclusive dashboard e painel admin. Mantenha as animações que o shadcn/ui já traz e siga [user-experience, documento 16](../user-experience/docs/16-movimento-e-transicoes.md).
- **Efeito de destaque com moderação.** No máximo um ou dois efeitos do Aceternity UI por página, de preferência no hero. Mais que isso deixa o site com cara de template e piora a performance.
- **Respeite `prefers-reduced-motion`** e teste o desempenho em celular sempre que adicionar componentes animados.
- **Adapte, não só cole.** Troque cores, fontes, raios e espaçamentos para os tokens da marca do projeto. Componente colado sem ajuste é o que faz o site parecer genérico.
- **Só o que é grátis.** Não use nem sugira itens pagos (Magic UI Pro, Aceternity UI Pro, pacotes pagos do Tabler) sem o usuário pedir.
- **Stack errada, ferramenta errada.** shadcn/ui, Magic UI e Aceternity UI exigem React e Tailwind. Sem React, use HyperUI. App mobile nativo está fora do escopo de todas.
- **O código copiado passa a ser do projeto.** shadcn/ui, Magic UI, Aceternity UI e HyperUI não atualizam por versão de pacote; quem mantém os componentes é o time.

## Quando a lista não cobre

Se o projeto pede algo fora destas sete ferramentas (ilustrações, animações Lottie, templates prontos, outro framework de componentes), diga isso ao usuário em vez de forçar uma delas. O `docs/README.md` registra o que foi avaliado e saiu da lista, com o motivo.

## Validade dos dados

Preços, licenças e números dos documentos foram verificados em 2026-11-24. Antes de afirmar um preço ou licença ao usuário, confira no site oficial se a informação for decisiva.
