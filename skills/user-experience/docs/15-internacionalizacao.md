# Internacionalização (i18n)

> Prepare o texto e os formatos para trocar de idioma sem reescrever telas; faça isso desde o início só se houver outro idioma no horizonte.

| | |
|---|---|
| **Referência** | MDN, `Intl` (developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl) · ICU MessageFormat (unicode-org.github.io/icu/userguide/format_parse/messages) · next-intl (next-intl.dev) · i18next (i18next.com) · Lingui (lingui.dev) · W3C, Internationalization (w3.org/International) |
| **Categoria** | Experiência do usuário |
| **Tipo** | Prática de preparo de texto e formatos |
| **Vale para** | Web responsiva, PWA, app híbrido e nativo (a ideia; a biblioteca muda) |
| **Verificado em** | 2026-11-24 |

## O que é

**i18n** (internacionalização, "i" + 18 letras + "n") é preparar o sistema para vários idiomas: o texto sai do código e vira **chaves** num arquivo de mensagens. **l10n** (localização) é o trabalho seguinte: traduzir e adaptar para um idioma e região (pt-BR, en-US). Em resumo: i18n é a infraestrutura; l10n é o conteúdo de cada idioma.

## Por que usar

- Adicionar um idioma vira traduzir um arquivo, e não caçar texto em 80 telas.
- Data, número e moeda saem no formato certo de cada região.
- Textos ficam em um só lugar, o que ajuda também a revisar o tom.

## Quando usar

- **Desde o início:** há outro idioma previsto em um ano, clientes no exterior ou público em espanhol e inglês. A tela já nasce com chaves de texto.
- **Só o mínimo:** produto só para o Brasil, sem plano de expandir. Mantenha pt-BR como padrão, use `Intl` para formatar e `lang="pt-BR"` no HTML. Não monte a infraestrutura de tradução.
- **Exagero:** protótipo, ferramenta interna de uma equipe só, MVP que ainda valida a ideia.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Vale se o público é multilíngue; rota por idioma ajuda a busca |
| MVP de SaaS | 🟡 Serve | Só se o mercado externo já está no plano; senão, apenas formatação com `Intl` |
| SaaS em crescimento | ✅ Ótimo | Expandir para outros países fica barato se o texto já está em chaves |
| Sistema interno/corporativo | ❌ Evite | Equipe fala um idioma; use `Intl` e `lang` e pare aí |
| API/integração | 🟡 Serve | Devolva códigos de erro estáveis; o texto traduzido fica no cliente |
| App mobile | ✅ Ótimo | As lojas e o sistema já entregam o idioma do aparelho |

## Quando é bom

- **Idioma novo sem refatorar:** só um arquivo de mensagens novo.
- **Formatos corretos:** `1.234,50` no Brasil, `1,234.50` nos EUA, sem código manual.
- **Mensagens com plural e gênero** tratadas pela biblioteca.

## Quando é ruim

- **Chaves para um produto que nunca será traduzido:** custa leitura (`t('agenda.titulo')` no lugar do texto) e ninguém aproveita.
- **Tradução automática sem revisão** em texto jurídico ou de saúde.
- **Concatenar frases:** quebra a ordem das palavras em outros idiomas.
- **RTL sem necessidade:** direção da direita para a esquerda (árabe, hebraico) só entra se esses idiomas estiverem previstos.

## Como começar

**Bibliotecas** (a escolha segue a stack; confira a documentação de cada uma):

| Stack | Opção |
|---|---|
| Next.js (App Router) | next-intl |
| React | react-i18next / i18next ou Lingui |
| Vue | vue-i18n |
| .NET | arquivos `.resx` e `IStringLocalizer` |
| Django | gettext (`gettext`, `gettext_lazy`) |
| Laravel | pasta `lang` e helper `__()` |
| Spring | `MessageSource` com `messages.properties` |

Arquivos de mensagens (pt-BR é o padrão):

```json
{
  "agenda": {
    "titulo": "Agendamentos",
    "resumo": "{nome} tem {total, plural, =0 {nenhuma consulta} one {# consulta} other {# consultas}} marcadas.",
    "confirmar": "Confirmar agendamento"
  }
}
```

**Plural e gênero:** use ICU MessageFormat (`plural`, `select`). Em português, 0 e 1 usam o singular, regra que a biblioteca resolve; não escreva `if (n === 1)` na mão. Para gênero, `{genero, select, feminino {Bem-vinda} masculino {Bem-vindo} other {Boas-vindas}}`.

**Formatos com `Intl`** (nativo do navegador e do Node, sem biblioteca):

```ts
const data = new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short', timeZone: 'America/Sao_Paulo' })
const preco = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })

data.format(new Date('2026-11-24T17:00:00Z'))
preco.format(1234.5)
```

**Fuso:** guarde horários em UTC no banco e converta para o fuso de quem vê. Agendamento de clínica é horário local da unidade: guarde o instante em UTC e o fuso da clínica.

**Não concatene frases:**

```ts
`Consulta com ${profissional} em ${dia}`
t('agenda.consulta', { profissional, dia })
```

A segunda forma deixa o tradutor reordenar: "Em {dia}, consulta com {profissional}".

**Texto que cresce:** inglês costuma ser mais curto que o português, mas alemão e outros podem ser bem maiores. Não fixe largura em botão (`min-width` e quebra de linha); teste com texto 40% mais longo.

**Rota por idioma:** `/pt-BR/agenda` e `/en/agenda`, com `<html lang>` certo e `hreflang` nas páginas públicas. O next-intl oferece roteamento por prefixo de idioma. Sem prefixo, o idioma sai do perfil do usuário ou do cabeçalho `Accept-Language`.

## Combina com / alternativas

- [08-formularios](08-formularios.md): máscaras e `autocomplete` por região.
- [11-tipografia-e-densidade](11-tipografia-e-densidade.md): fonte com suporte aos caracteres de cada idioma.
- [14-acessibilidade](14-acessibilidade.md): `lang` e leitor de tela.
- Skills vizinhas: **stacks** (qual framework), **data** (guardar UTC e fuso).

## Decisão rápida

- **Use se:** há outro idioma ou região no plano, ou o produto é SaaS que vai crescer para fora do Brasil.
- **Evite:** montar toda a infraestrutura de tradução num produto só brasileiro; concatenar frases; formatar data e moeda na mão.
