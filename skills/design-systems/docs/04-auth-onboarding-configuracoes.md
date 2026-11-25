# Login, onboarding e configurações

> As telas de borda de todo sistema: a porta de entrada, os primeiros passos e o lugar onde a pessoa ajusta a própria conta.

| | |
|---|---|
| **Tipo de sistema** | Telas transversais a qualquer produto: autenticação, primeiros passos e preferências da conta |
| **Exemplo** | [04-auth-onboarding-configuracoes.html](../examples/04-auth-onboarding-configuracoes.html) (três telas em abas) |
| **Layout base** | Login em tela dividida (formulário + painel de marca); onboarding em coluna central com passos; configurações com navegação lateral de seções + blocos |
| **Referências reais** | Clerk (https://clerk.com), Vercel (https://vercel.com/login), Notion (https://www.notion.com), Linear (https://linear.app) e GitHub (https://github.com/settings/profile, que redireciona para o login). Os URLs responderam 200 em 2026-11-24; as telas logadas não foram abertas, então o doc não descreve o design delas |
| **Componentes** | shadcn/ui: Input, Label, Button, Checkbox, Switch, RadioGroup, Dialog/AlertDialog, Progress, Toast (lista em ui.shadcn.com/docs/components, 2026-11-24), com formulários via React Hook Form (guia em ui.shadcn.com/docs/forms). Lucide para ícones |
| **Verificado em** | 2026-11-24 |

## O que é

São três telas que todo sistema precisa e que quase ninguém desenha com cuidado:

- **Login:** formulário de entrada, de um lado, e um painel de marca (frase, ilustração, depoimento), do outro.
- **Onboarding:** passos curtos, uma pergunta por tela, que deixam a conta pronta para uso.
- **Configurações:** navegação por seções à esquerda e, à direita, blocos de formulário com botão de salvar próprio, mais uma zona de perigo para ações irreversíveis.

O exemplo (marca fictícia Caju) mostra as três na mesma página, alternadas por abas, com validação visível e diálogo de confirmação.

## Por que este layout

- **Primeira impressão:** o login é a primeira tela do produto. O painel de marca dá identidade sem competir com o formulário.
- **Foco:** uma coisa por vez no onboarding. O progresso visível ("Passo 2 de 4") mostra onde a pessoa está.
- **Achar rápido:** em configurações, a lista de seções à esquerda permite ir direto ao ponto, sem rolar tudo.
- **Segurança:** a zona de perigo isola o que não tem volta, longe das ações do dia a dia.
- **Acolhimento:** textos maiores, cantos arredondados e cor quente fazem o sistema parecer um serviço, não uma planilha.

## Quando usar

- Todo produto com conta de usuário (praticamente todos).
- Produto que precisa configurar algo antes de ser útil (equipe, integrações, preferências).
- Quando o login precisa transmitir a marca ou provar confiança (depoimento, logos de clientes).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS e apps web com conta | ✅ Ótimo | As três telas são obrigatórias e definem a percepção de qualidade |
| Produto para o cliente final | ✅ Ótimo | Tom acolhedor e passos curtos combinam com público leigo |
| Sistema interno com login único (SSO) | 🟡 Serve | O login some ou vira um botão; configurações e perfil ainda valem |
| Ferramenta de uso pessoal sem conta | 🟡 Serve | Só configurações; onboarding pode ser uma única tela |
| Landing page ou site institucional | ❌ Evite | Sem conta, não há o que mostrar |
| Painel que o usuário só consulta, sem escolhas | ❌ Evite | Onboarding e configurações grandes seriam enfeite |

## Anatomia do layout

```
LOGIN                              ONBOARDING
┌────────────────┬───────────────┐ ┌──────── 720 px ────────┐
│ Marca          │ Painel de     │ │ Marca        Pular      │
│                │ marca         │ │ ▬▬▬ ▬▬▬ ▭▭▭ ▭▭▭  barra  │
│  Título 36 px  │ Frase 32 px   │ │ Passo 2 de 4            │
│  [e-mail]      │ ilustração    │ │ ┌─────────────────────┐ │
│  [senha]  👁   │               │ │ │ Título + opções     │ │
│  [ Entrar ]    │ depoimento    │ │ │ [Voltar] [Continuar]│ │
│  ou Google     │               │ │ └─────────────────────┘ │
└────────────────┴───────────────┘ └─────────────────────────┘
CONFIGURAÇÕES
┌─────────┬──────────────────────────────┐
│ Perfil  │ Título da página             │
│ Notific.│ ┌ Bloco ──────────────────┐  │
│ Equipe  │ │ Título · descrição      │  │
│ Plano   │ │ campos                  │  │
│ Seguran.│ ├─────────────────────────┤  │
│ 240 px  │ │ nota        [Salvar]    │  │
│         │ └─────────────────────────┘  │
│         │ ┌ Zona de perigo (borda ──┐  │
│         │ └ vermelha) ──────────────┘  │
└─────────┴──────────────────────────────┘
```

- **Login:** duas colunas iguais; o formulário tem largura máxima de 400 px, centrado na coluna. Campos de 52 px de altura, botão de 48 px, pílula.
- **Onboarding:** coluna única de 720 px, card com 40 px de padding, barra de progresso em segmentos de 6 px, opções em grade de 2 colunas com 12 px de espaço.
- **Configurações:** navegação de 240 px fixa ao rolar (sticky), conteúdo até 1040 px no total, blocos com 24 a 32 px de padding e rodapé com botão de salvar. Espaço de 48 px entre navegação e conteúdo.
- **Tablet (até 1023 px):** login mantém as duas colunas com menos padding; navegação de configurações cai para 200 px.
- **Celular (até 767 px):** o painel de marca do login vira uma faixa curta no topo com só a frase; onboarding usa opções em 1 coluna; a navegação de configurações vira uma fileira horizontal de botões que rola; os campos ocupam a largura toda.

## Tokens do exemplo

| Token | Claro | Escuro |
|---|---|---|
| Fundo | `#fbf8f4` | `#1a1613` |
| Superfície | `#ffffff` | `#241f1b` |
| Borda | `#e9dfd3` | `#3d352e` |
| Texto / secundário | `#2a2118` / `#6b5f51` | `#f4ede5` / `#b8ab9c` |
| Marca (laranja-coral) | `#c2410c` (texto sobre ela `#ffffff`) | `#ff8a5c` (texto sobre ela `#2a1006`) |
| Marca suave / painel do login | `#fdebdf` / `#f9d9c3` | `#3b2216` / `#3a2417` |
| Sucesso / erro | `#17673a` / `#b42318` | `#7fdca0` / `#ff8f84` |

| Item | Valor |
|---|---|
| Fonte | Inter, com pilha do sistema como fallback |
| Escala tipográfica | 14 (apoio, dicas e erros) · 15 · 16 (rótulos) · 17 (corpo; 16 até 767 px) · 18 · 20 · 24 (título de bloco) · 30 a 36 (título de tela; 30 no celular) · 32 (frase do painel de login) |
| Raio | 12 px (campos), 20 px (cards), pílula (botões) |
| Sombra | `0 1px 2px` + `0 8px 24px` com 6% de opacidade |
| Espaçamento | escala de 4/8 px: 8, 12, 16, 20, 24, 32, 48 |

## Componentes e padrões essenciais

- **Campo de texto:** rótulo sempre visível acima (não só placeholder), dica abaixo, erro no lugar da dica com ícone e texto, `aria-invalid`, que indica que o valor não bate com o formato esperado (MDN aria-invalid), e foco no primeiro erro.
- **Senha:** botão de mostrar e ocultar, `autocomplete` correto: `current-password` para a senha atual e `new-password` para criar ou trocar senha (MDN autocomplete), link "Esqueci a senha".
- **Login social:** botão secundário abaixo de um separador "ou", nunca mais forte que o botão principal.
- **Progresso do onboarding:** barra em segmentos + "Passo N de M" + nome do passo. Botão Voltar sempre disponível; "Pular" onde o passo for opcional.
- **Opções em cartão:** o cartão inteiro é clicável (radio por baixo), com estado selecionado por borda e fundo, não só cor.
- **Bloco de configuração:** título, descrição, campos e rodapé com nota ("Última alteração em…") e botões Descartar e Salvar.
- **Interruptores:** descrição curta do que muda; salvam na hora ou avisam que dependem do botão Salvar.
- **Zona de perigo:** bloco separado, borda de erro, botões contornados em vermelho, e diálogo que pede para digitar uma palavra de confirmação.
- **Estado de erro:** senha ou e-mail errados com mensagem genérica, sem revelar qual dos dois falhou (OWASP Authentication Cheat Sheet, 2026-11-24); falha de rede com "Tentar novamente".
- **Estado carregando:** botão com indicador e desativado durante o envio; blocos de configuração com skeleton.
- **Estado vazio:** em equipe ou convites, uma frase e o botão de convidar; na configuração de plano, o que acontece sem cartão.

## Quando é bom

- Dá confiança logo na entrada e reforça a marca sem esforço extra do usuário.
- Onboarding curto leva à primeira ação útil mais rápido.
- Configurações previsíveis: a pessoa aprende uma vez e acha tudo depois.
- Funciona bem no celular, pois a estrutura é linear.

## Quando é ruim

- **Onboarding longo:** passos demais, ou perguntas que o produto poderia descobrir sozinho. Corte e deixe o resto para depois.
- **Painel de marca pesado:** imagem grande, animação ou vídeo que atrasa o login. No celular, esconda.
- **Erros comuns:**
  - Usar só placeholder como rótulo (some ao digitar).
  - Erro genérico "algo deu errado" sem dizer o que corrigir.
  - Bloquear colar senha ou desativar gerenciadores de senha (reprovado pelo WCAG 3.3.8, AA, w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum; o OWASP recomenda permitir colar).
  - Contraste baixo do texto de apoio sobre o painel colorido.
  - Salvar configurações sem avisar, ou exigir um único "Salvar" no fim de uma página de 8 blocos.
  - Zona de perigo sem confirmação, ou com botão vermelho cheio chamando mais atenção que o Salvar.
  - Tela de configurações como lista única e longa, sem navegação por seção.

## Como começar

1. Abra [04-auth-onboarding-configuracoes.html](../examples/04-auth-onboarding-configuracoes.html) e use as abas do topo. Tente entrar com campos vazios, avance os passos do onboarding e abra "Excluir conta".
2. Copie as variáveis do `:root` (claro e escuro) e o padrão de campo com rótulo, dica e erro.
3. Troque a cor de marca e o texto do painel de login. Confira o contraste (mínimo 4,5:1 para texto normal, WCAG 1.4.3) do botão e do texto sobre o painel.
4. Monte com a skill design: shadcn/ui (Field, Input, Switch, RadioGroup, AlertDialog, Progress) e Lucide. Veja `design/docs/01-shadcn-ui.md`.
5. Reduza o onboarding ao mínimo que o seu produto exige antes do primeiro uso.

## Combina com / alternativas

- Fundamentos de tipografia, cor e espaçamento: [01-fundamentos.md](01-fundamentos.md)
- Telas internas que vêm depois do login: [03-admin-crud.md](03-admin-crud.md) e [02-dashboard-analytics.md](02-dashboard-analytics.md)
- Página pública que leva ao cadastro: [05-landing-saas.md](05-landing-saas.md)
- Plano e cobrança com mais detalhe: [09-financeiro.md](09-financeiro.md)
- Versão de app nativo dessas telas: [12-app-mobile.md](12-app-mobile.md)

## Decisão rápida

**Use se:** o produto tem contas de usuário, precisa de alguma configuração inicial e quer parecer confiável e acolhedor desde a primeira tela.

**Evite se:** não há conta nem escolhas a fazer, ou se o login é só um redirecionamento de SSO (nesse caso, invista só em perfil e configurações).
