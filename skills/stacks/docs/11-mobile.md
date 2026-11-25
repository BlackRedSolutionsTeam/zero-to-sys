# Mobile (React Native com Expo, Flutter e nativo)

> Para app de celular: Expo (React Native) quando o time já sabe React, Flutter quando o time aceita Dart e quer widgets próprios, nativo quando o app depende de APIs do sistema.

| | |
|---|---|
| **Site** | https://expo.dev, https://flutter.dev |
| **Categoria** | Área 6 — Mobile |
| **Tipo** | Stack de app, com três caminhos |
| **Stack/composição** | Expo: React Native, TypeScript, Expo Router, TanStack Query, API do documento [04](04-spa-vite-api.md). Flutter: Dart, widgets próprios, Riverpod (riverpod.dev, "framework de cache reativo e data-binding") ou Bloc (bloclibrary.dev, "biblioteca de gerenciamento de estado previsível para Dart"). Nativo: Swift (iOS) e Kotlin (Android). Backend: qualquer API dos documentos 05 a 10. Testes: Jest (Expo), flutter test (Flutter), Maestro para ponta a ponta (maestro.dev) |
| **Preço** | Frameworks grátis. Contas de loja são pagas (Apple e Google); os valores mudam e estão nas páginas de preço da Apple e do Google; não os repetimos aqui |
| **Licença** | React Native: MIT; Expo: MIT; Flutter: BSD-3-Clause (LICENSE nos repositórios e registro npm, conferidos em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Expo é um conjunto de ferramentas sobre React Native: você escreve em TypeScript e React, e o resultado usa componentes nativos de cada sistema. Flutter, do Google, escreve em Dart e usa um conjunto próprio de widgets, desenhados com o Impeller, em vez dos componentes do sistema (docs.flutter.dev/resources/architectural-overview). Nativo é escrever um app para cada sistema, com as linguagens da Apple e do Google.

A documentação do Flutter lida em 2026-11-24 corresponde ao Flutter 3.50 (página atualizada em 2026-11-17). Expo é, segundo o site oficial, uma plataforma open source para apps nativos universais (Android, iOS e web) com JavaScript e React (docs.expo.dev). O pacote `expo` no npm está na 58.0.26 (conferido em 2026-11-24). O SDK de Flutter estável é o 3.50.1 (releases do Flutter).

## Por que usar

- **Um código para vários sistemas:** Expo cobre Android, iOS e web (docs.expo.dev); Flutter também cobre desktop (docs.flutter.dev/platform-integration/desktop).
- **Expo:** usa JavaScript e React; os componentes do React Native mapeiam para componentes nativos do sistema (reactnative.dev).
- **Flutter:** widgets próprios, implementados no próprio Flutter, em vez dos do sistema (docs.flutter.dev/resources/architectural-overview).
- **Nativo:** Swift (iOS) e Kotlin (Android), sem camada intermediária.

## Quando usar

- **Expo:** o time já sabe React e quer usar JavaScript e TypeScript.
- **Flutter:** equipe que aceita Dart e quer o mesmo conjunto de widgets em todas as plataformas.
- **Nativo:** quando o app depende de APIs específicas do sistema que Expo e Flutter não cobrem.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App de produto (cadastro, pedidos, feed) | ✅ Ótimo | Expo e Flutter cobrem iOS e Android com uma base de código (docs.expo.dev, docs.flutter.dev) |
| App para clientes de um SaaS | ✅ Ótimo | Consome a API existente |
| E-commerce / delivery | ✅ Ótimo | Sem recurso oficial de e-commerce; avaliar caso a caso |
| Sistema interno de campo | 🟡 Serve | Sem recurso oficial específico; avaliar caso a caso |
| MVP / protótipo | 🟡 Serve | Expo tem fluxo de build em nuvem (docs.expo.dev/build/introduction); lojas têm revisão |
| App com recursos pesados do aparelho | 🟡 Serve | Expo permite código nativo com `npx expo prebuild` (docs.expo.dev/workflow/overview); Flutter, via `dart:ffi` e platform channels |
| Dashboard / painel admin | ❌ Evite | Web ([SPA](04-spa-vite-api.md)) roda no navegador, sem loja |
| Site de conteúdo | ❌ Evite | Não é o foco |
| Dados/IA | ❌ Evite | Como cliente de API |

## Quando é bom

- **Expo:** EAS Update envia atualizações de JavaScript, sujeitas às regras das lojas (docs.expo.dev/eas-update/introduction); EAS Build compila na nuvem ou local (docs.expo.dev/build/introduction).
- **Flutter:** catálogo oficial de widgets e testes na documentação (docs.flutter.dev/testing/overview).
- **Nativo:** acesso direto às APIs do sistema.
- **Mesma linguagem do back TypeScript** (Expo).

## Quando é ruim

- **Expo:** código nativo próprio exige `npx expo prebuild` e gerar os diretórios android e ios (docs.expo.dev/workflow/overview).
- **Flutter:** Dart é uma linguagem a mais para o time; os controles são implementações próprias do Flutter, não os do sistema (docs.flutter.dev/resources/architectural-overview).
- **Nativo:** um app para cada sistema, em Swift e em Kotlin.
- **Todos:** publicação nas lojas exige conta de desenvolvedor (developer.apple.com/programs) e seguir as regras de revisão das lojas.
- **Web responsiva** pode bastar; avalie antes.

## Como começar

Expo (documentação oficial):

```bash
npx create-expo-app@latest
```

Flutter (`flutter create` cria um projeto e `flutter doctor` mostra o tooling instalado, segundo docs.flutter.dev/reference/flutter-cli):

```bash
flutter doctor
flutter create meu_app
cd meu_app && flutter run
```

Ícones para React Native: veja [Lucide](../../design/docs/05-lucide.md) na skill design. Publicação e CI de app: skill infra.

## Combina com / alternativas

- Backend: [Node](05-node-api.md), [.NET](07-dotnet-aspnet-core.md), [Laravel](09-laravel-rails.md), [Go](10-go-api.md).
- [Tauri/Electron](12-desktop.md): para desktop.
- Alternativas de fora: Kotlin Multiplatform (kotlinlang.org/multiplatform) e .NET MAUI (learn.microsoft.com/dotnet/maui).

## Decisão rápida

- **Use Expo se:** o time é de React. **Use Flutter se:** quer o mesmo conjunto de widgets em todas as plataformas e aceita Dart. **Use nativo se:** precisa de APIs do sistema que os outros não cobrem.
- **Evite app nativo ou cruzado se:** uma web responsiva resolve.
