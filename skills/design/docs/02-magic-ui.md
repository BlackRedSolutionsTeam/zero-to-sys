# Magic UI

> Biblioteca open source de componentes React animados, no estilo do shadcn/ui, pensada para landing pages e sites de marketing.

| | |
|---|---|
| **Site** | https://magicui.design |
| **Categoria** | Linha 2 — Componentes, templates e assets |
| **Tipo** | Biblioteca de componentes (copiar e colar) + templates pagos |
| **Stack** | React, TypeScript, Tailwind CSS, Motion (Framer Motion), Next.js, CLI do shadcn |
| **Preço** | Componentes grátis. Magic UI Pro: US$ 199 pagamento único (licença individual, acesso vitalício) |
| **Licença** | MIT (componentes). Pro: uso comercial permitido, revenda do código proibida |
| **Verificado em** | 2026-11-24 |

## O que é

Magic UI é uma coleção de mais de 150 componentes e efeitos animados em React, TypeScript, Tailwind e Motion. O site se apresenta como uma biblioteca "para Design Engineers" e como companheira do shadcn/ui. O repositório tem cerca de 23,5 mil estrelas no GitHub.

Não é um pacote npm fechado. Você usa o CLI do shadcn para copiar o código do componente para dentro do seu projeto. Depois disso o código é seu e você edita à vontade. Os componentes são organizados por categorias como animações de texto, efeitos especiais, botões, fundos e mockups de dispositivos (ex.: Globe, Marquee, Shimmer Button).

Há também o Magic UI Pro, vendido à parte: mais de 50 blocos/seções e 9+ templates (SaaS, startup, agente de IA, ferramenta de dev) em Next.js e Tailwind. A documentação ainda menciona um servidor MCP para uso com assistentes de IA.

## Por que usar

Animações de marketing (texto que revela, bordas luminosas, grids, marquees) levam horas para ficar boas e consistentes. Aqui elas já vêm prontas, no mesmo padrão de código do shadcn/ui, em Tailwind.

O ganho real é tempo: uma landing page com cara de produto moderno sai em um dia, não em uma semana. Como o código é copiado, não há dependência de versão da biblioteca nem custo por componente.

## Quando usar

- Landing page de produto SaaS, startup ou ferramenta de IA.
- Projeto que já usa Next.js, Tailwind e shadcn/ui.
- Seção hero que precisa de um efeito de destaque (fundo animado, texto animado, globo).
- Prova social com marquee de logos e depoimentos.
- Prototipar rápido uma página de lançamento para validar uma ideia.
- Quando o time tem dev front-end para ajustar o código copiado.

## Para que tipo de site

| Tipo de site/projeto | Encaixe | Por quê |
|---|---|---|
| Landing page / site de marketing | ✅ Ótimo | É o foco da biblioteca: efeitos e seções de conversão. |
| Site institucional | 🟡 Serve | Dá para usar em hero e destaques, mas animação demais passa pouca seriedade. |
| Portfólio | 🟡 Serve | Bom para efeitos pontuais; o risco é o visual ficar igual ao de outros sites. |
| Blog/conteúdo | ❌ Evite | Foco é leitura e velocidade; animações só pesam. |
| E-commerce | 🟡 Serve | Útil na home e em páginas de campanha; evite no checkout e na listagem. |
| SaaS / app web | 🟡 Serve | Ótimo na página pública; dentro do app faltam componentes funcionais (tabelas, formulários complexos). |
| Dashboard / painel admin | ❌ Evite | Animações atrapalham densidade e produtividade; use shadcn/ui puro. |
| MVP / protótipo | ✅ Ótimo | Visual polido rápido, sem custo e sem lock-in. |
| Sistema interno corporativo | ❌ Evite | Efeitos de marketing não agregam e aumentam manutenção. |
| App mobile | ❌ Evite | É web (React DOM + Tailwind); não serve para apps nativos. |

## Quando é bom

- **Código é seu:** o CLI copia o fonte para o projeto, então você altera sem esperar o mantenedor e sem quebrar com upgrade.
- **Mesmo fluxo do shadcn/ui:** quem já usa shadcn instala com o mesmo comando, sem aprender ferramenta nova.
- **Licença MIT nos componentes:** uso comercial sem custo e sem atribuição obrigatória.
- **Grande catálogo de efeitos:** economiza o trabalho de animar na mão com Motion e CSS.
- **Pro com preço único:** US$ 199 uma vez, com atualizações futuras incluídas, evita assinatura mensal (na data da verificação).
- **Boa base para IA:** como é código simples em Tailwind, ferramentas como Cursor e v0 editam bem (o site também oferece MCP).

## Quando é ruim

- **Performance:** efeitos pesados (Globe, fundos animados, partículas) podem prejudicar o mobile e o LCP em conexões lentas. Meça Core Web Vitals depois de adicionar.
- **Acessibilidade varia por componente:** a página de docs (magicui.design/docs, 2026-11-24) não menciona acessibilidade nem `prefers-reduced-motion`. No código do repositório (magicuidesign/magicui, `apps/www/registry/magicui/`, branch main, 2026-11-24), dos 80 componentes, só 6 consultam `prefers-reduced-motion` (`dia-text-reveal`, `dither-field`, `floating-3d-particles`, `icon-cloud`, `retro-grid` e `scroll-based-velocity`); os demais animados, como `marquee`, `globe`, `blur-fade`, `number-ticker` e `particles`, não (leitura de todos os arquivos `.tsx` da pasta no commit `d13c610`). Teste teclado, leitor de tela e movimento reduzido em cada componente que usar.
- **Manutenção manual:** como o código é copiado, correções do projeto original não chegam sozinhas. Você precisa recopiar e mesclar.
- **Dependência de Motion e Tailwind:** o projeto precisa dessas bibliotecas. Em stack sem React/Tailwind (Vue, Angular, WordPress puro) não serve.
- **Excesso de animação:** usar muitos efeitos juntos deixa a página lenta e com cara de "template de IA", igual a muitos outros sites.
- **Só marketing:** faltam componentes funcionais de app (tabelas de dados, formulários complexos). Isso o shadcn/ui cobre melhor.
- **Pro tem custo e termos:** US$ 199 por licença individual, e revenda do código é proibida. Leia o contrato antes de usar em projetos de clientes (a página de preços e a licença conferidas em 2026-11-24 não citam agências nem projetos de clientes; proíbem revender, compartilhar ou transferir os produtos a terceiros. Em dúvida, pergunte ao Magic UI).
- **Sem Figma:** reviews apontam ausência de arquivos de design; o designer depende do dev para ver o resultado.

## Como começar

Em um projeto Next.js com Tailwind:

```bash
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add @magicui/globe
```

```tsx
import { Globe } from "@/components/ui/globe"

export default function Home() {
  return <Globe />
}
```

O mesmo vale com npm, yarn ou bun (a página tem abas para cada um). Catálogo e exemplos em https://magicui.design/docs. O Pro está em https://pro.magicui.design.

## Combina com / alternativas

- Base obrigatória na prática: [shadcn/ui](01-shadcn-ui.md), de onde vem o fluxo de instalação.
- Concorrente direto, mais visual e 3D: [Aceternity UI](03-aceternity-ui.md).
- Para ícones: [Lucide](05-lucide.md).
- Alternativas de fora: Framer (editor visual), Tailwind UI/Catalyst, daisyUI.

## Decisão rápida

- **Use se:** a stack é React + Tailwind (de preferência Next.js) e o objetivo é uma landing page ou página de produto com visual moderno e animado, rápido e sem custo.
- **Evite se:** o projeto é dashboard, sistema interno, blog ou app mobile, ou se performance e acessibilidade são críticas e o time não vai testar o impacto das animações.
