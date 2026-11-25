# Desktop (Tauri e Electron)

> Para app de computador com tecnologia web: Tauri (webview do sistema e núcleo em Rust) ou Electron (Chromium e Node.js embutidos).

| | |
|---|---|
| **Site** | https://tauri.app e https://www.electronjs.org |
| **Categoria** | Área 7 — Desktop |
| **Tipo** | Stack de app, com duas opções |
| **Stack/composição** | Tauri: núcleo em Rust, interface em React ou outro framework web com Vite, webview do sistema, SQLite local. Electron: Node.js e Chromium embutidos, interface em React, SQLite local. Atualização automática e assinatura de código nas duas (tauri.app/plugin/updater; electronjs.org/docs/latest/tutorial/updates) |
| **Preço** | Grátis. Certificados de assinatura (Apple, Windows) são pagos; os valores mudam e dependem da loja e da certificadora; não os repetimos aqui |
| **Licença** | Electron: MIT; Tauri: Apache-2.0 ou MIT, à sua escolha (campo de licença da CLI no npm; GitHub mostra Apache-2.0; conferidos em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

As duas ferramentas empacotam uma interface web como programa de desktop. Electron embute o Chromium e o Node.js (electronjs.org), o que dá um alvo de renderização estável. Tauri usa a webview que já existe no sistema, sem embutir um motor de navegador, e um núcleo em Rust; um app mínimo pode ser pequeno (tauri.app/start).

A documentação de criação do Tauri lida aponta a linha 2.x (comando `cargo install tauri-cli --version "^2.0.0"`); a CLI `@tauri-apps/cli` está na 2.12.6 no npm (conferido em 2026-11-24). Para Electron, o pacote `electron` no npm está na 45.5.0 (Node 22.12 ou superior). O tutorial oficial (docs/tutorial no repositório electron/electron) usa `npm init` e `npm install electron --save-dev`.

## Por que usar

- **Reaproveita o front web:** HTML, CSS e JavaScript viram app (electronjs.org; tauri.app/start/frontend).
- **Tauri:** não embute navegador, então o app só leva o código e os recursos dele (tauri.app/start); permissões e escopos explícitos (tauri.app/security).
- **Electron:** o Chromium embutido dá um alvo de renderização estável (electronjs.org).

## Quando usar

- **Tauri:** app em que o tamanho importa e o time aceita Rust no núcleo.
- **Electron:** time só de JavaScript, ou app que precisa do Chromium e de módulos Node embutidos.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Ferramenta interna de desktop | ✅ Ótimo | Reaproveita o front web; Tauri e Electron têm guia de distribuição (tauri.app/distribute) |
| App de produtividade / editor | ✅ Ótimo | Acesso ao sistema de arquivos e a atalhos por APIs de cada ferramenta |
| Cliente offline de um SaaS | ✅ Ótimo | Plugin SQL do Tauri, com SQLite, MySQL e PostgreSQL via sqlx (v2.tauri.app/plugin/sql) |
| Sistema corporativo com impressoras e hardware | 🟡 Serve | Depende de código nativo: Rust no Tauri, módulos Node no Electron |
| MVP / protótipo | 🟡 Serve | Sem base oficial para comparar; assinatura de código é parte da distribuição (electronjs.org/docs/latest/tutorial/code-signing) |
| Jogos e gráficos pesados | ❌ Evite | Não é o foco das duas ferramentas |
| Site de conteúdo / blog | ❌ Evite | [Astro](01-astro-conteudo.md) é feito para sites de conteúdo |
| App mobile | ❌ Evite | Veja [mobile](11-mobile.md) |
| Sistema interno que só roda no navegador | ❌ Evite | Uma [SPA](04-spa-vite-api.md) evita instalar nos computadores |

## Quando é bom

- **Uma base de código web** reaproveitada no desktop.
- **Atualização automática:** plugin updater do Tauri (tauri.app/plugin/updater) e guia de atualizações do Electron (electronjs.org/docs/latest/tutorial/updates).
- **Tauri:** sem navegador embutido (tauri.app/start); **Electron:** Chromium embutido (electronjs.org).

## Quando é ruim

- **Electron:** cada app embute um Chromium e o Node.js (electronjs.org), o que aumenta o pacote.
- **Tauri:** a webview muda por sistema (WebView2 no Windows, WebKit no macOS e no Linux; tauri.app/reference/webview-versions), então o comportamento pode variar; o núcleo em Rust pede conhecimento da linguagem.
- **Segurança:** os dois dão acesso ao sistema; veja electronjs.org/docs/latest/tutorial/security e tauri.app/security.
- **Assinatura de código** (Windows) e **notarização** (macOS) fazem parte do guia oficial de distribuição do Electron (electronjs.org/docs/latest/tutorial/code-signing).

## Como começar

Tauri (documentação oficial):

```bash
npm create tauri-app@latest
```

Electron: `npm init` e `npm install electron --save-dev`, como no tutorial oficial (conferido em 2026-11-24); guia em https://www.electronjs.org/docs. Em ambos, a interface pode ser a mesma do [SPA com Vite](04-spa-vite-api.md). Pipeline de build e assinatura: skill infra.

## Combina com / alternativas

- [SPA com Vite](04-spa-vite-api.md): interface compartilhada com a versão web.
- Backend: [Node](05-node-api.md), [Go](10-go-api.md) e outros para sincronização.
- Alternativas de fora: Flutter desktop ([mobile](11-mobile.md)), .NET MAUI (learn.microsoft.com/dotnet/maui) e aplicativo nativo.

## Decisão rápida

- **Use Tauri se:** o tamanho do app importa e o time topa Rust no núcleo. **Use Electron se:** o time é só de JavaScript ou quer o Chromium embutido.
- **Evite se:** um site responsivo resolve, ou o app é um jogo ou gráfico pesado.
