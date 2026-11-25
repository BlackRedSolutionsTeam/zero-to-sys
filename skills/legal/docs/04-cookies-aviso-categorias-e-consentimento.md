# Cookies: aviso, categorias e gestão de consentimento

> Classifique cada cookie, carregue só o que for necessário antes do aceite e deixe a pessoa recusar e mudar de ideia com a mesma facilidade com que aceita.

| | |
|---|---|
| **Referência** | Guia Orientativo Cookies e Proteção de Dados Pessoais, ANPD, publicado em 18/10/2022 (gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf); LGPD, arts. 7, 8 e 9 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) |
| **Categoria** | Jurídico |
| **Tipo** | Prática de classificação de cookies e consentimento |
| **Vale para** | Sites e apps web; exemplos em TypeScript |
| **Verificado em** | 2026-11-25 |

> Não substitui advogado. Conferência: a página oficial da ANPD foi aberta e confirmou o guia (criado em 18/10/2022, arquivo modificado em 23/01/2025). O texto integral não pôde ser lido nesta conferência; as regras do banner abaixo seguem resumos de escritórios de advocacia sobre o guia. Leia o PDF oficial antes de fechar o desenho do banner.

## O que é

**Cookie** é um pequeno arquivo guardado no navegador, usado para manter sessão, lembrar preferência ou medir uso. Pelo guia da ANPD, eles podem ser classificados por **finalidade** (necessários, de funcionalidade, analíticos, de publicidade), por quem os coloca (próprio ou de terceiro) e por tempo de vida (sessão ou persistente). O guia é documento interpretativo da autoridade, não regulamento.

## Por que usar

- **Obrigação de transparência:** o titular tem de saber o que é coletado e para quê (LGPD, art. 9).
- **Consentimento precisa de prova** (art. 8, § 2), de finalidade determinada (art. 8, § 4) e de revogação facilitada (art. 8, § 5).
- **Evita rastreio sem base legal**, o ponto mais fiscalizado em sites.

## Quando usar

- O site ou app usa analytics, pixel de anúncio, chat, vídeo incorporado ou mapa de terceiros.
- Antes de colocar qualquer tag nova no site.
- Cookie só de sessão e de segurança: ainda assim, informe na política de cookies.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo com anúncios | ✅ Ótimo | Muitos cookies de terceiros; consentimento por finalidade |
| Loja online | ✅ Ótimo | Pixel, remarketing, carrinho e pagamento |
| SaaS com área logada | 🟡 Serve | Cookies necessários na área logada; banner só no site público com analytics |
| Site institucional sem ferramentas de terceiros | 🟡 Serve | Informar na política basta; sem banner |
| App mobile | ✅ Ótimo | O equivalente são SDKs e identificadores de dispositivo |
| Site com analytics sem cookie, auto-hospedado | ❌ Evite o banner | Menos coleta, menos obrigação (confirme com o advogado) |

## Quando é bom

- **Bloqueio prévio:** nenhuma tag não necessária roda antes do aceite.
- **Duas camadas:** primeira com as opções principais; segunda, por categoria, onde a pessoa consente por finalidade (resumos do guia).
- **Recusar tão fácil quanto aceitar**, sem caixa pré-marcada.
- **Mudar a escolha depois**, em link permanente no rodapé.

## Quando é ruim

- **"Ao continuar navegando você aceita":** não é manifestação de vontade (LGPD, art. 8).
- **Tags de anúncio disparando antes do aceite** com o banner só enfeitando.
- **Cookie wall** que bloqueia o conteúdo para quem recusa o que não é necessário, sem alternativa; avalie com advogado.
- **Banner que esconde o recusar** em texto pequeno ou em duas telas.
- **Categorias vagas** como "melhorar a experiência" sem dizer o que se coleta.

## Como começar

**1. Inventário de cookies** (parte do mapa de dados, doc [02](02-politica-de-privacidade-e-o-mapa-de-dados.md)).

| Nome | Categoria | Próprio ou terceiro | Duração | Finalidade | Base |
|---|---|---|---|---|---|
| `session` | Necessário | Próprio | Sessão | Manter login | Execução de contrato |
| `csrf` | Necessário | Próprio | Sessão | Proteger formulários | Segurança |
| `_analytics` | Analítico | Terceiro | 13 meses | Medir uso | Consentimento (ou legítimo interesse, conforme o advogado) |
| `_ads` | Publicidade | Terceiro | 90 dias | Remarketing | Consentimento |

**2. Descubra os cookies reais.** Abra o site em janela anônima, aceite tudo e liste em Application > Cookies; repita sem aceitar e compare. Ou pelo terminal:

```bash
curl -sI https://example.com | grep -i set-cookie
```

**3. Modelo de estrutura da política de cookies:** o que são; tabela por categoria com nome, finalidade, duração e quem coloca; como mudar a escolha; como bloquear no navegador; contato.

**4. Estrutura do banner.**

1. Primeira camada: aviso curto, botões "Aceitar", "Recusar" e "Personalizar", com o mesmo destaque, e link para a política.
2. Segunda camada: uma chave por categoria não necessária, todas desligadas por padrão; as necessárias aparecem como "sempre ativas".
3. Link "Preferências de cookies" no rodapé, sempre visível.

**5. Guarde a escolha e carregue por categoria.**

```ts
type CookieConsent = {
  version: string;
  analytics: boolean;
  advertising: boolean;
  decidedAt: string;
};

const KEY = "cookie_consent";

export function readConsent(): CookieConsent | null {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as CookieConsent) : null;
  } catch {
    return null;
  }
}

export function saveConsent(consent: CookieConsent): void {
  localStorage.setItem(KEY, JSON.stringify(consent));
  applyConsent(consent);
}

export function applyConsent(consent: CookieConsent | null): void {
  if (consent?.analytics) loadScript("https://analytics.example.com/script.js");
  if (consent?.advertising) loadScript("https://ads.example.com/pixel.js");
}

function loadScript(src: string): void {
  const el = document.createElement("script");
  el.src = src;
  el.defer = true;
  document.head.appendChild(el);
}
```

**6. Revogação:** ao desligar uma categoria, pare de carregar a tag e apague os cookies dela; recarregue a página para garantir.

**7. Prova do consentimento** para quem tem conta: grave também no servidor, com versão do texto, data e escolha (doc [05](05-aceite-versionado.md)). Para visitante anônimo, o registro local com versão e data costuma ser o que existe; o advogado diz se basta.

**8. Reavisar** quando mudar categoria ou fornecedor: suba `version` e peça a escolha de novo.

## Combina com / alternativas

- Desenho do banner e das chaves: skill `design-systems`.
- Analytics e registro de acesso: [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md).
- Aceite versionado: [05](05-aceite-versionado.md).
- Alternativa: ferramenta de gestão de consentimento (CMP); confira se bloqueia as tags de verdade e guarda prova.
- Alternativa que reduz o problema: analytics sem cookie e sem identificar a pessoa.

## Decisão rápida

- **Use se:** o site carrega qualquer coisa além dos cookies necessários.
- **Evite se:** a ideia é um banner só de "OK"; ele não cria consentimento válido.
