# iOS, Android e web

> Cada plataforma tem convenções próprias de navegação, gestos, tipografia e permissões; seguir a do aparelho faz o sistema parecer familiar e evita surpresas.

| | |
|---|---|
| **Tema** | Diferenças de plataforma (iOS, Android, web, desktop) e escolha entre site responsivo, PWA, app híbrido e nativo pela experiência |
| **Vale para** | Web responsiva, PWA, app nativo |
| **Referências oficiais** | Apple HIG https://developer.apple.com/design/human-interface-guidelines · Material Design 3 https://m3.material.io · web.dev PWA https://web.dev/learn/pwa · WebKit, Web Push no iOS https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/ · MDN `env()` https://developer.mozilla.org/en-US/docs/Web/CSS/env · WCAG 2.2 · NN/g |
| **Verificado em** | 2026-11-24 |

## O que é

iOS (Apple), Android (Google) e a web têm guias de design próprios. Eles diferem no botão de voltar, na barra de navegação, nas folhas, nos seletores, no pedido de permissões e nos gestos do sistema.

Em desktop, Windows e macOS também diferem: atalhos (Ctrl x Cmd), barras de rolagem, posição dos botões da janela. A pergunta de projeto é: seguir o sistema ou ter um visual único em todos? A boa prática é manter a identidade visual e respeitar o comportamento do sistema.

## Por que importa

- Usuário leva hábitos de um aparelho: deslizar da borda para voltar no iOS, botão/gesto Voltar no Android.
- Ignorar a convenção gera erro de toque, gesto conflitante e sensação de "app estranho".
- A tecnologia escolhida limita o que a experiência consegue (push, câmera, offline, loja).

## Quando aplicar

- Ao decidir se o sistema será site, PWA, híbrido ou nativo (a escolha técnica é da skill stacks).
- Ao definir navegação e componentes que mudam de cara por plataforma.
- Ao testar em aparelhos reais.

## Celular, tablet e desktop

Colunas desta tabela: iOS, Android e web/desktop.

| Aspecto | iOS | Android | Web / desktop |
|---|---|---|---|
| Voltar | Ver HIG, Gestures | Gesto/botão Voltar do sistema (previsão de voltar: opção de desenvolvedor no Android 13 e 14, animações do sistema por padrão no Android 15; developer.android.com/guide/navigation/custom-back/predictive-back-gesture) | Botão voltar do navegador; mantenha histórico (`pushState`) coerente |
| Navegação principal | Barra de abas na parte de baixo no iPhone; no iPad fica perto do topo e pode virar barra lateral (HIG, Tab bars) | Barra de navegação inferior (3 a 5 destinos) em janelas compactas; em médias, barra ou trilho; em expandidas e maiores, trilho (Material 3, Navigation bar) | Menu superior ou barra lateral |
| Tipografia | San Francisco; body 17 pt por padrão (HIG, Typography); Dynamic Type | Roboto é o padrão do Material 3 (m3.material.io/styles/typography/type-scale-tokens); body large 16 sp (Material Components Android, docs/theming/Typography.md); tamanhos em sp | `system-ui`; zoom do navegador |
| Folhas e diálogos | Ver HIG, Sheets | Bottom sheet e diálogos (Material 3, Breakpoints) | `<dialog>`, drawer |
| Permissões | Push na web só após toque do usuário (WebKit) | Android 13 (API 33) ou mais pede a permissão `POST_NOTIFICATIONS` em tempo de execução, de preferência no contexto de uso (developer.android.com/develop/ui/views/notifications/notification-permission) | Pedir só após ação do usuário (WebKit, para push) |
| Notificações | Push nativo; web push só em app adicionado à Tela de Início (iOS e iPadOS 16.4 ou mais; WebKit) | Push nativo | Web Push (Push API, MDN) |
| Área segura | Respeitar a área segura e a Dynamic Island (HIG, Layout) | — | `env(safe-area-inset-*)` (MDN) |

## Para que tipo de projeto

| Tipo | Melhor encaixe | Por quê |
|---|---|---|
| Landing page | ✅ Site responsivo | Só precisa de link e velocidade; app é exagero. |
| E-commerce | ✅ Site responsivo, 🟡 PWA | Aquisição por busca e anúncio; PWA ajuda no retorno. App nativo se a recompra for alta. |
| SaaS | ✅ Site responsivo / PWA | Uso no desktop; PWA para quem quer instalar. |
| Dashboard | ✅ Site responsivo | Leitura, sem hardware. |
| Sistema interno | ✅ Site responsivo, 🟡 PWA | Sem loja, atualização imediata. |
| App de campo | ✅ PWA offline ou nativo/híbrido | Offline, câmera, GPS e sincronização em segundo plano; nativo se precisar de recursos que o navegador não dá. |
| App de consumo com push, câmera, sensores | ✅ Híbrido ou nativo | Acesso total a hardware e presença na loja. |

## Regras práticas

- Alvo de toque: 44 pt padrão e 28 pt mínimo no iOS (Apple HIG, Accessibility, 2026-11-24), 48 dp no Android (support.google.com/accessibility/android/answer/7101858), 24 x 24 CSS px no mínimo na web (WCAG 2.5.8). Fontes divergem; use o maior no celular.
- Barra de navegação inferior no Android: de 3 a 5 destinos; acima de 5 não use a barra (Material 3, m3.material.io/components/navigation-bar/guidelines, 2026-11-24). A HIG pede evitar abas que viram "Mais" (Tab bars) e não fixa um máximo para o iPhone.
- Use `viewport-fit=cover` e `env(safe-area-inset-*)` para não colocar controles sob o notch ou a barra Início.
- Em iOS, push web exige o site adicionado à Tela de Início com manifesto `display: standalone` ou `fullscreen`, e a permissão só é pedida após toque do usuário (WebKit). O artigo do WebKit (iOS e iPadOS 16.4) descreve push só para web apps na Tela de Início e não diz nada sobre aba comum do Safari. Mudanças posteriores a esse artigo não foram conferidas aqui; veja as notas de versão do Safari (developer.apple.com/documentation/safari-release-notes) antes de prometer push.
- PWA no Android (Chrome) pode oferecer instalação; no iOS a instalação é manual ("Adicionar à Tela de Início"). Suporte atual de cada recurso: confira em web.dev e caniuse; só conferi Web Bluetooth e Web NFC (abaixo).
- Câmera e GPS funcionam na web com permissão (`getUserMedia`, Geolocation), mas Bluetooth, NFC e execução em segundo plano têm suporte desigual (caniuse em 2026-11-24: Web Bluetooth só no Chrome/Android e desktop Chromium, sem Firefox nem Safari/iOS; Web NFC só no Chrome para Android, MDN/BCD `NDEFReader`).
- Atalhos: use `event.metaKey` no macOS e `event.ctrlKey` nos demais; mostre o rótulo correto (⌘S ou Ctrl+S).
- Nunca esconda função só atrás de gesto: ofereça botão equivalente (WCAG 2.5.1 gestos de caminho; 2.5.7 arrastar, nível AA).
- Segue a plataforma no comportamento (voltar, seletores, permissões) e a marca na aparência (cor, forma, tom).

## Erros comuns

- **Botão Voltar do Android fecha o app/ sai da página:** trate o histórico; em PWA use `pushState` por tela.
- **Barra de abas no topo no iOS ou menu hambúrguer escondendo tudo:** use barra inferior com ícone e rótulo.
- **Conteúdo sob o notch ou a barra Início:** use `env(safe-area-inset-*)`.
- **Pedir permissão no primeiro segundo:** peça no momento em que faz sentido e explique antes.
- **Atalho só com Ctrl em macOS:** adapte para Cmd.
- **Prometer push no iOS sem instalar:** avise o usuário para adicionar à Tela de Início.
- **Escolher nativo sem precisar:** custo de duas lojas e atualizações lentas.

## Como aplicar

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="manifest" href="/manifest.webmanifest">
```

```json
{ "name": "Meu Sistema", "short_name": "Sistema", "start_url": "/", "display": "standalone",
  "theme_color": "#0b5fff", "background_color": "#ffffff",
  "icons": [{ "src": "/i-192.png", "sizes": "192x192", "type": "image/png" },
            { "src": "/i-512.png", "sizes": "512x512", "type": "image/png" }] }
```

```css
.barra-inferior { padding-bottom: env(safe-area-inset-bottom); }
.cabecalho { padding-top: env(safe-area-inset-top); }
```

```js
const mac = /Mac|iPhone|iPad/.test(navigator.platform); // detecção de plataforma é aproximada; teste nos aparelhos reais
addEventListener('keydown', e => { if ((mac ? e.metaKey : e.ctrlKey) && e.key === 's') { e.preventDefault(); salvar(); } });
```

Escolha pela experiência (a decisão técnica é da skill stacks):

| Opção | Consegue | Não consegue ou limita |
|---|---|---|
| Site responsivo | Link, busca, sem instalação, atualização imediata | Push limitado, offline fraco, sem loja |
| PWA | Instalar, offline, push (com limites no iOS), ícone | Hardware restrito; iOS tem menos recursos; sem loja por padrão |
| Híbrido | Loja, push, câmera e sensores via plugins, uma base de código | Desempenho e aparência podem ficar abaixo do nativo |
| Nativo | Tudo do sistema, melhor desempenho e gestos | Dois códigos (ou multiplataforma), custo, revisão das lojas |

## Combina com / alternativas

- [01-contexto-de-uso.md](01-contexto-de-uso.md), [02-mobile.md](02-mobile.md), [03-tablet.md](03-tablet.md), [04-desktop.md](04-desktop.md).
- [06-navegacao.md](06-navegacao.md): barra inferior, trilho, menu lateral.
- [07-toque-mouse-teclado.md](07-toque-mouse-teclado.md): gestos e atalhos.
- [10-modais-folhas-e-paineis.md](10-modais-folhas-e-paineis.md): folhas por plataforma.
- [12-desempenho-e-rede.md](12-desempenho-e-rede.md): PWA e offline.
- Skills vizinhas: stacks (escolha da tecnologia), design-systems, design.

## Decisão rápida

**Faça**
- Comece com site responsivo; suba para PWA se precisar de instalar/offline; vá a nativo se precisar de hardware ou loja.
- Siga a plataforma no comportamento e a marca na aparência; trate área segura.
- Teste em iPhone, Android de entrada, iPad e dois navegadores desktop.

**Evite**
- Gesto sem botão equivalente, atalho só com Ctrl, permissão pedida cedo demais.
- Prometer push ou offline sem conferir o que cada plataforma permite.
