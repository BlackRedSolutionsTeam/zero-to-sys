# Estados de tela

> Toda tela tem mais estados do que o "feliz": vazio, carregando, erro, sem permissão, offline, parcial e sucesso. Desenhe todos antes de codar.

| | |
|---|---|
| **Referência** | Material Design 3 (m3.material.io), Apple Human Interface Guidelines (developer.apple.com/design/human-interface-guidelines), WCAG 2.2 (w3.org/TR/WCAG22), RFC 9110 (códigos 401, 403 e 503), MDN (`aria-busy`, `prefers-reduced-motion`, `navigator.onLine`) |
| **Categoria** | Design |
| **Tipo** | Prática de design de interface |
| **Vale para** | Qualquer tela que busca ou grava dados; exemplos em HTML e CSS |
| **Verificado em** | 2026-11-24 |

## O que é

Estado de tela é a aparência da tela em cada situação possível dos dados. A tela de agendamentos da clínica, por exemplo, pode estar com consultas, sem nenhuma consulta, esperando a API, com a API fora do ar ou com o usuário sem permissão. São cinco telas diferentes para o mesmo endereço.

## Por que usar

- **O usuário real passa tempo nos estados "ruins":** rede lenta, primeiro uso, erro. É onde ele decide continuar ou abandonar.
- **Evita tela em branco**, que parece quebrada e não diz o que fazer.
- **Evita retrabalho:** estado esquecido vira bug em produção.

## Quando usar

- Em toda tela que lê ou grava dados.
- Já no desenho do fluxo: os estados nascem junto com os passos, como em [03-fluxos-e-jornadas.md](../../product/docs/03-fluxos-e-jornadas.md).
- Na revisão de PR, como checklist.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas telas dinâmicas; vale para busca e formulário de contato |
| MVP de SaaS | ✅ Ótimo | Primeiro uso e erro decidem a ativação |
| SaaS em crescimento | ✅ Ótimo | Permissões, planos e dados parciais aumentam os estados |
| Sistema interno/corporativo | ✅ Ótimo | Perfis diferentes veem telas diferentes (403, vazio por filtro) |
| API/integração | ❌ Evite | Não tem tela; o equivalente é o [formato de erro](../../api/docs/03-formato-de-erro.md) |
| App mobile | ✅ Ótimo | Rede instável torna offline e carregando rotineiros |

## Quando é bom

- Cada estado diz o que aconteceu e o que fazer a seguir.
- O layout não pula quando os dados chegam.
- O erro vem em linguagem humana, com saída (tentar de novo, voltar, falar com o suporte).

## Quando é ruim

- Spinner infinito sem tempo-limite nem mensagem.
- "Erro 500" ou "Something went wrong" sem ação.
- Tabela vazia sem explicação: o usuário acha que perdeu os dados.
- Usar o mesmo texto para "ainda não tem nada" e "o filtro não achou nada".

## Como começar

### Estado, o que mostrar e componente

| Estado | O que mostrar | Componente |
|---|---|---|
| Vazio, primeiro uso | O que a tela guarda, por que está vazia e um botão para criar o primeiro item | Estado vazio com ícone, título, texto e botão |
| Vazio, busca ou filtro | "Nada encontrado para X" e ação para limpar filtros | Estado vazio com link "Limpar filtros" |
| Carregando, forma conhecida | Silhueta do conteúdo final | Skeleton |
| Carregando, ação curta (botão) | Botão desabilitado com indicador | Spinner dentro do botão |
| Erro recuperável | O que falhou, em palavras simples, e "Tentar de novo" | Alerta inline com botão |
| Erro fatal | Explicação, saída segura (voltar ao início) e canal de suporte | Página de erro |
| Sem permissão (403) | Que o acesso não é do perfil dele e a quem pedir | Página ou bloco de aviso |
| Offline | Aviso persistente; o que ainda funciona | Faixa no topo |
| Parcial | O que carregou aparece; o que falhou ganha erro só no seu bloco | Erro por cartão |
| Sucesso | Confirmação do que foi feito e próximo passo | Toast (aviso temporário) ou tela de confirmação |
| Confirmação antes de agir | O que será feito e que é irreversível, com botão de ação nomeado ("Cancelar consulta") | Diálogo de confirmação |

### Skeleton sem pulo de layout

O skeleton reserva a mesma altura do conteúdo final. Assim a página não se mexe quando os dados chegam (esse pulo se mede como CLS, ver [12-desempenho-e-rede.md](../../user-experience/docs/12-desempenho-e-rede.md)).

```html
<ul class="lista" aria-busy="true" aria-label="Carregando agendamentos">
  <li class="linha skeleton"></li>
  <li class="linha skeleton"></li>
  <li class="linha skeleton"></li>
</ul>
```

```css
.linha {
  height: 56px;
  border-radius: 8px;
  margin-bottom: 8px;
}
.skeleton {
  background: linear-gradient(90deg, #eceff3 25%, #f6f8fa 50%, #eceff3 75%);
  background-size: 200% 100%;
  animation: brilho 1.2s linear infinite;
}
@keyframes brilho {
  to { background-position: -200% 0; }
}
@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; }
}
```

Skeleton para listas e cartões; spinner só quando não se sabe a forma do resultado ou em ação curta. Se a espera passar de alguns segundos, mostre uma mensagem de que está demorando.

### Estado vazio

```html
<section class="vazio" role="status">
  <h2>Nenhuma consulta marcada</h2>
  <p>Quando um paciente agendar, a consulta aparece aqui.</p>
  <a class="botao" href="/agendamentos/novo">Agendar primeira consulta</a>
</section>
```

```css
.vazio {
  display: grid;
  justify-items: center;
  gap: 8px;
  padding: 48px 16px;
  text-align: center;
}
.vazio p { color: #5b6470; max-width: 40ch; }
```

### Na tela de agendamento da clínica

| Situação | Mensagem |
|---|---|
| Clínica nova, sem consultas | "Nenhuma consulta marcada. Agendar primeira consulta" |
| Filtro "Dra. Ana, sexta" sem resultado | "Nenhuma consulta para Dra. Ana na sexta. Limpar filtros" |
| API caiu ao carregar a agenda | "Não conseguimos carregar a agenda. Tentar de novo" |
| Horário escolhido foi ocupado por outro | "Esse horário acabou de ser ocupado. Escolha outro." com os horários livres |
| Recepcionista abre a tela financeira | "Você não tem acesso a esta área. Peça ao administrador da clínica." |
| Sem internet | Faixa: "Você está offline. Os dados podem estar desatualizados." |
| Consulta marcada | Toast: "Consulta marcada para 12/12, 14h" |

O erro da API vira mensagem pelo `code` estável do [formato de erro](../../api/docs/03-formato-de-erro.md), nunca pelo texto técnico. 401 manda para o login; 403 mostra o bloco de permissão; 503 aceita "Tentar de novo" (RFC 9110).

### Regras rápidas

- Anuncie mudanças a leitores de tela com `role="status"` (informação) ou `role="alert"` (erro urgente), WCAG 4.1.3.
- Nunca comunique o erro só pela cor (WCAG 1.4.1); use ícone e texto.
- Em formulário, mantenha o que a pessoa digitou quando der erro.
- Offline: `navigator.onLine` só indica se há conexão com alguma rede, não se a API responde. Trate também a falha da requisição.

## Combina com / alternativas

- [01-fundamentos.md](01-fundamentos.md): cores de estado, contraste e acessibilidade.
- [03-admin-crud.md](03-admin-crud.md): lista com quatro estados (dados, carregando, vazio, erro).
- [10-agendamento.md](10-agendamento.md): a tela usada de exemplo.
- [../../product/docs/03-fluxos-e-jornadas.md](../../product/docs/03-fluxos-e-jornadas.md): estados já no fluxo.
- [../../api/docs/03-formato-de-erro.md](../../api/docs/03-formato-de-erro.md): de onde vem o `code` do erro.
- [../../user-experience/docs/12-desempenho-e-rede.md](../../user-experience/docs/12-desempenho-e-rede.md): CLS e rede lenta.

## Decisão rápida

- **Use se:** a tela lê ou grava dados, tem mais de um perfil de usuário ou roda em rede instável.
- **Evite se:** não há tela (API pura) ou é um protótipo descartável de uma tela só.
