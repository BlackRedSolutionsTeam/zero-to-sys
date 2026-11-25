# Windows: pacote, Microsoft Store e assinatura de código

> Na Microsoft Store, prefira MSIX (a Store assina por você); MSI/EXE e qualquer download direto precisam de certificado de uma CA confiável, e o Azure Artifact Signing não atende o Brasil.

| | |
|---|---|
| **Referência** | https://learn.microsoft.com/en-us/windows/apps/publish/get-started, https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-package-requirements, https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options, https://learn.microsoft.com/en-us/azure/artifact-signing/quickstart, https://v2.tauri.app/distribute/microsoft-store/ |
| **Categoria** | Publicação desktop |
| **Tipo** | Formato de pacote e assinatura |
| **Vale para** | Microsoft Store, download direto e winget |
| **Verificado em** | 2026-11-25 |

## O que é

| Formato | Loja aceita | Quem assina |
|---|---|---|
| MSIX | ✅ recomendado | A Store reassina depois da certificação |
| MSI ou EXE | ✅ desde 2021 | Você, com certificado de CA do Microsoft Trusted Root Program; autoassinado não serve |
| PWA | ✅ (PWABuilder) | A Store |
| Download direto | — | Você (OV, EV ou Artifact Signing) |

## Por que usar

- Instalador sem assinatura cai no SmartScreen ("O Windows protegeu o computador") e muita gente desiste.
- Na Store, MSI/EXE fora das regras é reprovado na hora.

## Quando é bom

- **MSIX** empacota qualquer app, inclusive Win32, e tira o trabalho do certificado na Store.
- **Regras do MSI/EXE na Store:** URL HTTPS versionada que não muda depois do envio, instalação silenciosa, instalador offline (não um stub que baixa), sem bundleware, desinstalação limpa e entrada em Adicionar/Remover Programas. Cada atualização é uma nova URL enviada ao Partner Center.
- **Tauri:** gera EXE (NSIS) e MSI. Para a Store: `/S` ou `/quiet`, WebView2 com `offlineInstaller`, publisher diferente do nome do produto e instalador assinado.
- **winget:** manifesto YAML num PR para o repositório `winget-pkgs`, com a URL do seu próprio release.

## Assinatura de código

| Opção | Custo | Para quem |
|---|---|---|
| Azure Artifact Signing (antes Trusted Signing) | Basic US$ 9,99/mês (5.000 assinaturas), Premium US$ 99,99/mês (100.000); US$ 0,005 por assinatura além da cota (azure.microsoft.com/pricing/details/artifact-signing, 2026-11-25) | Empresas de EUA, Canadá, UE, Reino Unido, Austrália, Nova Zelândia, Japão, Coreia do Sul, Singapura, Suíça, Noruega e Israel; pessoa física só EUA e Canadá. **Brasil não entra** |
| Certificado OV | US$ 150 a 300/ano, chave em token ou HSM desde 2023 | Caminho do Brasil |
| Certificado EV | US$ 400+/ano | Sem vantagem de reputação desde 2024 |
| SignPath Foundation | Gratuito | Projetos open source aprovados |

Desde 2024 o EV não passa direto pelo SmartScreen: EV e OV ganham reputação do mesmo jeito, assinando versões seguidas com a mesma identidade.

## Quando é ruim

- **Token físico do OV** complica o CI. Prefira um provedor com chave em HSM na nuvem (Azure Key Vault com `relic` ou o serviço da própria CA).
- **Guias antigos** do Electron ainda dizem que só EV evita o alerta; a Microsoft já desmentiu.

## Como começar

1. Escolha o formato: MSIX se der; MSI/EXE se a stack só gera isso (Tauri, Electron).
2. Compre o certificado OV no nome do CNPJ ou da pessoa física do Partner Center.
3. Configure a assinatura no CI (Tauri: `signCommand` em `tauri.conf.json`; Electron: `electron-builder` ou Forge com `signtool`).
4. Rode o Windows App Certification Kit antes de enviar.
5. Envie pelo Partner Center, pela CLI ou por GitHub Actions; a certificação leva até 3 dias úteis.

## Decisão rápida

- **Só Store:** MSIX, sem comprar certificado.
- **Store com MSI/EXE ou download direto:** certificado OV desde o primeiro build de teste.
