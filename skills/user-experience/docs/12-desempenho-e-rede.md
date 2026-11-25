# Desempenho e rede

> Celular tem CPU mais fraca, rede instável e bateria limitada: a mesma página que voa no desktop pode travar no campo, então meça e projete para o pior caso.

| | |
|---|---|
| **Tema** | Desempenho percebido, Core Web Vitals, imagens, JavaScript, esqueletos, interface otimista, offline, economia de dados, animação, testes |
| **Vale para** | Web responsiva, PWA (app nativo só em parte) |
| **Referências oficiais** | web.dev Core Web Vitals https://web.dev/articles/vitals · web.dev Optimize LCP https://web.dev/articles/optimize-lcp · MDN `prefers-reduced-data` https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-data · MDN `prefers-reduced-motion` https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion · web.dev PWA https://web.dev/learn/pwa · WCAG 2.2 (2.3.3, 2.2.2) · NN/g (tempos de resposta) |
| **Verificado em** | 2026-11-24 |

## O que é

Desempenho percebido é quão rápida a tela parece para quem usa, não só o tempo medido. Inclui a primeira imagem aparecer, a resposta ao toque e a ausência de saltos no layout.

No celular três fatores pesam mais: processador (parsing de JavaScript custa), rede (3G/4G fraca, oscilante, túnel, elevador) e bateria (animação e rede gastam).

## Por que importa

- Usuário de campo está em rede ruim; página lenta vira app inutilizável.
- Core Web Vitals são as métricas de experiência de página da web.dev e aparecem no relatório do Search Console; a web.dev não informa peso no ranking (web.dev/articles/vitals, 2026-11-24).
- Animação demais gasta bateria e incomoda quem tem sensibilidade a movimento.

## Quando aplicar

- Desde o início: orçamento de peso por página, imagens corretas e pouco JavaScript.
- Antes de lançar: teste com CPU e rede limitadas e em aparelho real de entrada.
- Em app de campo: planejar offline e reenvio desde o desenho.

## Celular, tablet e desktop

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Hardware de teste | Aparelho Android de entrada, rede 4G lenta | Tablet intermediário | CPU e rede típicas |
| Imagens | Menor largura via `srcset`/`sizes`, AVIF/WebP | Largura intermediária | Largura maior, 2x só onde há tela densa |
| JavaScript | Mínimo; divide por rota, adia o resto | Idem | Pode ser maior, mas dividido |
| Carregamento | Esqueleto + `loading="lazy"` abaixo da dobra | Idem | Idem; pré-busca ao passar o mouse (hover) |
| Rede | Assuma queda; fila local, repetição e aviso | Idem | Normalmente estável; ainda avise ao cair |
| Offline | PWA com cache do essencial e fila de envio | Idem | Opcional |
| Dados | Respeite economia de dados; evite vídeo automático | Idem | Menos restrição |
| Animação | Curta, só em `transform`/`opacity`; respeita redução de movimento | Idem | Idem |
| Verificação | Lighthouse móvel + aparelho real | Idem | Lighthouse desktop |

## Para que tipo de projeto

| Tipo | Prioridade | Por quê |
|---|---|---|
| Landing page | Alta | LCP e CLS decidem a primeira impressão e o anúncio pago; poucos scripts. |
| E-commerce | Alta | Imagens de produto pesadas e conversão ligada à velocidade. |
| SaaS | Média | Usuário recorrente tolera mais, mas INP (resposta ao clique) importa. |
| Dashboard | Média | Dados pesados: paginar, virtualizar e usar esqueleto. |
| Sistema interno | Média | Rede boa na maior parte; cuide de tabelas grandes. |
| App de campo | Alta | Rede ruim e offline são regra; fila de envio e reconexão são requisito. |
| Blog/conteúdo | Alta | Páginas leves e imagens corretas; quase nada de JS. |

## Regras práticas

- Limites "bom" dos Core Web Vitals, medidos no percentil 75 das visitas, segmentado por celular e desktop (os limites são os mesmos; web.dev/articles/vitals, 2026-11-24): LCP até 2,5 s, INP até 200 ms, CLS até 0,1.
- Não use `loading="lazy"` na imagem do LCP; use `fetchpriority="high"` nela, em no máximo uma ou duas imagens (web.dev, Optimize LCP).
- Sempre informe `width` e `height` (ou `aspect-ratio`) nas imagens para evitar mudança de layout (CLS).
- Formatos modernos: AVIF e WebP com `<picture>` e fallback JPEG. Percentual de economia varia por imagem; não adoto número fixo.
- Esqueleto em vez de spinner para listas e cartões. Respostas abaixo de 100 ms parecem instantâneas, 1 s mantém o fluxo de pensamento e 10 s é o limite de atenção (NN/g, "Response Times", baseado em Miller e Card).
- Interface otimista: atualize a tela já e reverta com aviso se falhar. Use em ações de baixo risco (curtir, marcar); em pagamento, aguarde a confirmação.
- Offline: service worker com cache do shell do app; fila local para envios (IndexedDB) e reenvio ao voltar a conexão. Background Sync é só Chromium: o caniuse mostra Chrome sim, Firefox e Safari (inclusive iOS) não (caniuse.com/background-sync, 2026-11-24); tenha reenvio manual.
- `prefers-reduced-data`: o MDN o marca como experimental e há contradição na própria página (rótulo "disponibilidade limitada" e frase "não é suportado por nenhum navegador"). O dado de compatibilidade do MDN (BCD) mostra Chrome 85 só com flag experimental, sem Firefox nem Safari. Trate como não suportado; use `navigator.connection.saveData` (só Chromium: o MDN/BCD lista Chrome 65+, sem Firefox nem Safari) ou o cabeçalho `Save-Data` como complemento.
- `prefers-reduced-motion: reduce`: remova movimento grande, parallax e autoplay (WCAG 2.3.3, AAA; a 2.2.2 exige pausar movimento automático por mais de 5 s).
- Animações em `transform` e `opacity`; durações curtas para transições de interface (mantenha curtas e respeite `prefers-reduced-motion`; WCAG 2.3.3).
- Teste: DevTools do Chrome, aba Performance com limitação de CPU (4x ou 6x) e aba Network com "Slow 4G"; Lighthouse em modo móvel; e um aparelho real barato. Lab não substitui dados de campo (CrUX, `web-vitals`).

## Erros comuns

- **Imagem de 3000 px no celular:** use `srcset` e `sizes`.
- **Carrossel gigante como LCP com lazy:** tire o `lazy` e dê prioridade.
- **Bundle único de JS:** divida por rota e adie bibliotecas pesadas.
- **Spinner que gira sem fim:** esqueleto, depois erro com botão "Tentar de novo".
- **Perde dado ao cair a rede:** salve rascunho local e mostre estado "pendente".
- **Fonte web bloqueando texto:** `font-display: swap`.
- **Só testar no notebook:** teste com limitação e aparelho real.

## Como aplicar

```html
<img src="hero-800.avif" fetchpriority="high" width="800" height="450" alt="..."
     srcset="hero-480.avif 480w, hero-800.avif 800w, hero-1600.avif 1600w"
     sizes="100vw">
<img src="item.webp" loading="lazy" decoding="async" width="400" height="300" alt="...">
<picture>
  <source type="image/avif" srcset="foto.avif"><source type="image/webp" srcset="foto.webp">
  <img src="foto.jpg" width="800" height="600" alt="...">
</picture>
```

```css
.skeleton { background: linear-gradient(90deg,#eee 25%,#f7f7f7 50%,#eee 75%); background-size: 200% 100%; animation: brilho 1.2s infinite; }
@keyframes brilho { to { background-position: -200% 0; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
```

```js
// Service worker mínimo: cache do shell
self.addEventListener('install', e => e.waitUntil(caches.open('shell-v1').then(c => c.addAll(['/', '/app.css', '/app.js']))));
self.addEventListener('fetch', e => e.respondWith(caches.match(e.request).then(r => r || fetch(e.request))));
// Reconexão
addEventListener('online', () => reenviarFila());
```

```js
// Medir em campo
import { onLCP, onINP, onCLS } from 'web-vitals';
[onLCP, onINP, onCLS].forEach(f => f(m => navigator.sendBeacon('/metrics', JSON.stringify(m))));
```

## Combina com / alternativas

- [01-contexto-de-uso.md](01-contexto-de-uso.md): rede e ambiente.
- [02-mobile.md](02-mobile.md): limites do celular.
- [11-tipografia-e-densidade.md](11-tipografia-e-densidade.md): fontes e imagens nítidas.
- [13-ios-android-web.md](13-ios-android-web.md): o que a PWA consegue em cada sistema.
- [09-tabelas-e-dados.md](09-tabelas-e-dados.md): virtualização e paginação.
- Skills vizinhas: stacks (framework e hospedagem), design-systems, design.

## Decisão rápida

**Faça**
- Meta: LCP 2,5 s, INP 200 ms, CLS 0,1 no percentil 75, no celular.
- Imagens com tamanho, formato e `lazy` certos; esqueleto; fila offline em app de campo.
- Testar com CPU 4x, "Slow 4G" e aparelho real.

**Evite**
- Lazy na imagem principal, JS em bloco único, animação sem `prefers-reduced-motion`.
- Depender de `prefers-reduced-data`.
- Bloquear a tela inteira por falta de rede.
