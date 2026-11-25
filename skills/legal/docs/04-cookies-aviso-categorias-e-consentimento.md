# Cookies: aviso, categorias e gestão de consentimento

> Classifique cada cookie, carregue só o que for necessário antes do aceite e deixe a pessoa recusar e mudar de ideia com a mesma facilidade com que aceita.

| | |
|---|---|
| **Referência** | Guia Orientativo Cookies e Proteção de Dados Pessoais, ANPD, versão 1.0, out/2022 (PDF oficial em gov.br/anpd, 40 páginas); LGPD, arts. 7, 8, 9, 14 e 18; Resolução CD/ANPD nº 18/2024, nº 2/2022 e nº 19/2024; Lei nº 15.211/2025 (ECA Digital) |
| **Categoria** | Jurídico |
| **Tipo** | Prática de classificação de cookies e consentimento |
| **Vale para** | Sites e apps web; exemplos em TypeScript |
| **Verificado em** | 2026-11-25 |

> Não substitui advogado. Conferência de 2026-11-25: o PDF oficial do guia foi baixado de gov.br/anpd e lido inteiro (40 páginas, texto extraído). As regras do banner abaixo citam a página do guia (p.). O guia se declara "guia de boas práticas" que "poderá ser atualizado" (p. 37), não é regulamento: descumprir uma boa prática não é infração automática, mas mostra como a ANPD enxerga a LGPD. O arquivo baixado traz "Versão 1.0, outubro/2022" e data de criação e modificação de 14/10/2022 nos metadados; a página da ANPD indica modificação em 23/01/2025, mas não há marca de revisão no texto. Se a ANPD publicar versão nova, reconfira. Fontes de cada norma na seção "Outras normas".

## O que é

**Cookies** são "arquivos instalados no dispositivo de um usuário que permitem a coleta de determinadas informações, inclusive de dados pessoais em algumas situações" (guia, p. 8). Quando a informação identifica a pessoa direta ou indiretamente, ou forma perfil comportamental, é dado pessoal e a LGPD vale (guia, p. 8-9; LGPD, art. 12, § 2º).

O guia classifica por quatro eixos, e "um mesmo cookie pode ser incluído em mais de uma categoria" (p. 9):

| Eixo | Categorias | Página |
|---|---|---|
| Quem gere | Próprios (primários) e de terceiros | 9 |
| Necessidade | Necessários e não necessários | 10 |
| Finalidade | Analíticos ou de desempenho, de funcionalidade, de publicidade | 10-11 |
| Retenção | De sessão (temporários) e persistentes | 11-12 |

O eixo que decide a base legal é o da necessidade: necessário é o que se restringe "ao essencial para prestar o serviço solicitado pelo titular", sem contemplar "finalidades não essenciais, que atendam a outros interesses do controlador" (p. 10). Analítico, de publicidade e rastreio de comportamento são não necessários (p. 10).

O guia vale também para "tecnologias similares de rastreamento, incluindo em dispositivos móveis" (p. 6), então SDKs de apps seguem a mesma lógica.

## Por que usar

- **Transparência:** informações "claras, precisas e facilmente acessíveis" sobre forma do tratamento, retenção e finalidades específicas (guia, p. 15; LGPD, art. 9).
- **Consentimento com prova:** cabe ao controlador provar que obteve o consentimento conforme a lei (LGPD, art. 8º, § 2º; guia, p. 19, que recomenda registrar e documentar os requisitos).
- **Evita rastreio sem base legal:** "não são compatíveis com a LGPD práticas que impliquem a coleta indiscriminada de dados pessoais" sem finalidade clara (guia, p. 16).

## Quando usar

- O site ou app usa analytics, pixel de anúncio, chat, vídeo incorporado ou mapa de terceiros.
- Antes de colocar qualquer tag nova no site.
- Só cookies necessários: ainda assim informe quais são e para quê, no banner e na política (exemplo 3 do guia, p. 25-26).

## Base legal por categoria

| Categoria | Base mais apropriada segundo o guia | Página |
|---|---|---|
| Necessário | Legítimo interesse (art. 7º, IX); consentimento "não é apropriado", porque a pessoa não tem escolha real | 20, 24 |
| Analítico ou de medição de audiência | Legítimo interesse "em determinados contextos": finalidade só de padrões e tendências, dados agregados, sem cruzar com outro rastreamento nem formar perfil, sem compartilhar com terceiros (exemplo 4) | 24, 26-27 |
| Publicidade | Consentimento; o legítimo interesse "dificilmente será" a base mais apropriada, em especial com cookies de terceiros, perfil comportamental ou rastreio entre sites | 25 |
| Qualquer outro não necessário | Consentimento é "mais apropriado", pois há opção genuína de aceitar ou recusar | 20 |

O guia diz que não há hierarquia entre bases (p. 20) e que o legítimo interesse exige teste de balanceamento antes do tratamento e direito de oposição (p. 23, LGPD art. 18, § 2º). Quem usa legítimo interesse para analytics informa isso e oferece oposição (exemplo 4, p. 26). Um analytics que cruza dados, usa terceiro que reutiliza os dados ou cria perfil sai desse enquadramento e cai em consentimento.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo com anúncios | ✅ Ótimo | Cookies de publicidade e de terceiros: consentimento por finalidade |
| Loja online | ✅ Ótimo | Pixel e remarketing pedem consentimento; carrinho e pagamento são necessários |
| SaaS com área logada | 🟡 Serve | Necessários na área logada; banner com escolha só no site público com analytics ou pixel |
| Site institucional sem ferramentas de terceiros | 🟡 Serve | Só necessários: aviso informativo e política, sem caixa de escolha (guia, p. 20, 25) |
| App mobile | ✅ Ótimo | O equivalente são SDKs e identificadores de dispositivo (guia, p. 6) |
| Site com analytics de medição agregada, sem perfil e sem terceiro | 🟡 Serve | Pode apoiar-se em legítimo interesse, com informação e oposição (guia, p. 24, 26-27); o advogado valida o teste de balanceamento |

## Quando é bom

Itens do guia para o banner (p. 30-32):

- **Primeiro nível:** botão que permita rejeitar todos os cookies não necessários, "de fácil visualização", nos banners de primeiro e segundo nível; link fácil para exercer direitos (saber mais, retenção, eliminar, opor-se, revogar).
- **Segundo nível:** cookies classificados em categorias, descritas por uso e finalidade, com informação simples e consentimento por finalidade específica, quando couber; cookies baseados em consentimento desativados por padrão.
- **Bloqueio pelo navegador:** informar como bloquear nas configurações; se o rastreador não puder ser desabilitado assim, avisar a pessoa.
- **Revogação:** procedimento "simplificado e gratuito", "de forma similar ao procedimento utilizado para obtê-lo" (p. 19; LGPD, art. 8º, § 5º).

Regra de implementação decorrente: nenhuma tag não necessária baseada em consentimento roda antes do aceite. Cookies necessários e analytics apoiado em legítimo interesse podem rodar, mas com informação prévia.

## Quando é ruim

Lista "o que evitar" do guia (p. 33):

- Um único botão no primeiro nível ("concordo", "aceito", "ciente") quando a base é consentimento.
- Dar destaque só ao aceitar, dificultando ver ou entender "rejeitar" e "configurar".
- Impossibilitar ou dificultar a rejeição de todos os não necessários.
- Não necessários ativados por padrão, exigindo desativar à mão; também "não é recomendável" caixa pré-selecionada nem consentimento tácito por "continuar navegando" (p. 19).
- Sem banner de segundo nível.
- Sem mecanismo direto e próprio para revogar e opor-se, além do bloqueio no navegador (o navegador é complemento, p. 15).
- Gestão difícil: sem opção específica para finalidades distintas.
- Política de cookies só em idioma estrangeiro.
- Lista de cookies granular demais, que gera fadiga e impede manifestação clara.
- Amarrar o consentimento ao aceite integral das condições, sem opção real (p. 18, 33).
- Finalidade genérica, como aceite de "termos e condições gerais" sem dizer a finalidade de cada cookie (p. 14-15; LGPD, art. 8º, § 4º).

Cookie wall (bloquear o conteúdo de quem recusa): o guia não o trata pelo nome. Ele exige consentimento "livre", sem "consequências negativas", e avalia caso a caso se há "alternativa real e satisfatória" (p. 18). Trate como risco e leve ao advogado.

## Como começar

**1. Inventário de cookies** (parte do mapa de dados, doc [02](02-politica-de-privacidade-e-o-mapa-de-dados.md)). Os valores de duração abaixo são exemplos; o guia não fixa prazo, pede só que a retenção seja compatível com a finalidade, "limitando-se ao estritamente necessário", e que cookie persistente tenha duração limitada "tanto quanto possível" (p. 12, 17).

| Nome | Categoria | Próprio ou terceiro | Duração | Finalidade | Base |
|---|---|---|---|---|---|
| `session` | Necessário | Próprio | Sessão | Manter login | Legítimo interesse ou execução de contrato |
| `csrf` | Necessário | Próprio | Sessão | Proteger formulários | Legítimo interesse (segurança) |
| `_analytics` | Analítico | Terceiro | 13 meses (exemplo) | Medir uso | Legítimo interesse se agregado e sem perfil; senão consentimento |
| `_ads` | Publicidade | Terceiro | 90 dias (exemplo) | Remarketing | Consentimento |

**2. Descubra os cookies reais.** Abra o site em janela anônima, aceite tudo e liste em Application > Cookies; repita sem aceitar e compare. Ou pelo terminal:

```bash
curl -sI https://example.com | grep -i set-cookie
```

**3. Política de cookies.** O guia recomenda uma política com finalidades específicas, período de retenção e compartilhamento com terceiros, entre outros itens do art. 9º (p. 28). Pode ser seção do aviso de privacidade, página própria ou o próprio banner, desde que as informações essenciais apareçam (p. 29). Só na política de privacidade "pode não ser suficiente"; use também banner de segundo nível (exemplo 7, p. 36). Estrutura: o que são; tabela por categoria com nome, finalidade, duração e quem coloca; como mudar a escolha; como bloquear no navegador; contato.

**4. Estrutura do banner** (guia, p. 30-32 e exemplos 2 e 6):

1. Primeira camada: aviso curto com "Aceitar todos", "Rejeitar cookies não necessários" e "Gerenciar", no mesmo formato e destaque (exemplo 2, p. 22), e link para a política.
2. Segunda camada: uma chave por categoria não necessária, desligadas por padrão; as necessárias aparecem como "sempre ativas".
3. Link "Preferências de cookies" sempre visível (por exemplo no rodapé), como mecanismo próprio de revogação. O guia pede o mecanismo (p. 33); o rodapé é a forma sugerida aqui.

**5. Guarde a escolha e carregue por categoria.**

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

**6. Revogação:** ao desligar uma categoria, pare de carregar a tag e apague os cookies dela; recarregue a página para garantir. O ato de revogar é unilateral e deve ser atendido sempre que pedido (guia, p. 19).

**7. Prova do consentimento** para quem tem conta: grave também no servidor, com versão do texto, data e escolha (doc [05](05-aceite-versionado.md)). Para visitante anônimo, o registro local com versão e data é o que costuma existir; o guia recomenda "o registro e a documentação de todos os requisitos" (p. 19) e não define formato. O advogado diz se basta.

**8. Reavisar** quando mudar categoria, finalidade ou fornecedor: "qualquer alteração das premissas adotadas para a obtenção do consentimento" exige novo consentimento ou outra base (guia, p. 18). Suba `version` e peça a escolha de novo.

## Outras normas conferidas

Conferidas em 2026-11-25 pelo texto oficial, no que importa para cookies.

| Norma | O que vale aqui | Fonte lida |
|---|---|---|
| LGPD (Lei 13.709/2018) | Art. 8º, § 2º (ônus da prova), § 4º (autorização genérica é nula), § 5º (revogação gratuita e facilitada); art. 12, § 2º (perfil comportamental é dado pessoal); art. 18, § 2º (oposição ao legítimo interesse) | Texto atualizado na Câmara dos Deputados (legin); o Planalto não respondeu nesta conferência |
| Resolução CD/ANPD nº 18/2024 (encarregado) | Arts. 8º e 9º: divulgar e manter atualizados identidade e contato do encarregado, em local de destaque e de fácil acesso no site; o contato deve viabilizar o exercício dos direitos do titular. Ponha no rodapé e na política de cookies o link para ele | DOU de 17/07/2024, Seção 1, p. 42 (in.gov.br) |
| Resolução CD/ANPD nº 2/2022 (pequeno porte) | Art. 11: pequeno porte não precisa indicar encarregado, mas deve ter canal de comunicação com o titular; art. 6º: a flexibilização não afasta bases legais, princípios nem direitos do titular, então o regime de cookies vale igual; art. 3º, I: quem faz tratamento de alto risco (inclui dado de criança e adolescente, art. 4º, II, d) não se beneficia | gov.br/anpd, texto da resolução |
| Resolução CD/ANPD nº 19/2024 (transferência internacional) | Cookie de terceiro (analytics, anúncio) pode mandar dados para fora do Brasil. Quem usa cláusulas-padrão publica em português, em linguagem simples, documento com forma, duração, finalidade, país de destino, contatos e direitos (art. 17, § 2º); a regra geral de transparência está no art. 2º, V. A coleta internacional, em si, não é transferência (art. 6º) | gov.br/anpd, texto da resolução, com retificação de 18/08/2025 |
| Lei 15.211/2025 (ECA Digital) | Vale para produto ou serviço "direcionado a crianças e a adolescentes ou de acesso provável por eles" (art. 1º). Art. 7º: configuração mais protetiva de privacidade por padrão. Art. 22: proibido perfilamento para direcionar publicidade comercial a criança e adolescente. Art. 26: proibido criar perfil comportamental deles para publicidade, inclusive com dados da verificação de idade. Em vigor desde 17/03/2026 (art. 41-A, acrescido pela Lei 15.352/2026) | Texto atualizado na Câmara dos Deputados (legin); publicação original conferida no mesmo portal |

Consequência prática: se o público provável inclui menores, não use cookie de publicidade com perfil, mesmo com consentimento do adulto (arts. 22 e 26 proíbem a finalidade, não só exigem aceite).

## O que ficou sem resolução

- **Regulamento do ECA Digital:** o texto da lei foi lido; decretos e normas da ANPD que detalham aferição de idade e supervisão parental não foram lidos. Reconfira antes de montar banner para público infantojuvenil.
- **Cookie wall:** o guia não decide; depende do caso e de decisão futura da ANPD.
- **Prazo de retenção e formato do registro de consentimento:** o guia não fixa números nem formato.
- **Versão do guia:** o PDF baixado é a v1.0 de out/2022; se a modificação de 23/01/2025 alterou o texto, ela não está marcada nele.
- **Resolução 18/2024 e Lei 15.211/2025** foram conferidas pela leitura do DOU e do portal legislativo, não pelo Planalto.

## Combina com / alternativas

- Desenho do banner e das chaves: skill `design-systems`.
- Analytics e registro de acesso: [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md).
- Aceite versionado: [05](05-aceite-versionado.md).
- Alternativa: ferramenta de gestão de consentimento (CMP); confira se bloqueia as tags de verdade e guarda prova.
- Alternativa que reduz o problema: analytics sem cookie e sem identificar a pessoa.

## Decisão rápida

- **Use se:** o site carrega qualquer coisa além dos cookies necessários.
- **Evite se:** a ideia é um banner só de "OK"; ele não cria consentimento válido.
