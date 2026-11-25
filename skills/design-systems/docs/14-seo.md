# SEO técnico

> Para a página aparecer no Google, deixe cada URL com título e descrição próprios, um h1, HTML que o robô lê sem esforço, sitemap e dados estruturados corretos.

| | |
|---|---|
| **Referência** | Google Search Central (developers.google.com/search/docs): título e snippets, dados estruturados, robots.txt, sitemaps, JavaScript SEO; Open Graph (ogp.me); schema.org; WCAG 2.2 |
| **Categoria** | Design |
| **Tipo** | Prática de SEO técnico |
| **Vale para** | Site de conteúdo, landing page e partes públicas de SaaS; exemplos em HTML |
| **Verificado em** | 2026-11-24 |

## O que é

SEO (otimização para mecanismos de busca) é fazer o Google encontrar, entender e mostrar bem suas páginas. Esta prática cobre a parte técnica, que o time controla no código. Escrever bom conteúdo continua sendo o principal.

## Por que usar

- Tráfego orgânico (sem anúncio) é o canal mais barato de uma clínica, de um blog ou de uma landing.
- Link compartilhado com imagem e título certos recebe mais cliques.
- Quase tudo é feito uma vez, no modelo da página.

## Quando usar

- Em toda página pública que deve ser achada na busca.
- Antes de publicar, e de novo depois de trocar domínio, rotas ou framework.

Páginas atrás de login (painel, agenda interna) não precisam de SEO: o Google não entra nelas. Bloqueie com autenticação, não com robots.txt.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | A busca é o principal canal de entrada |
| MVP de SaaS | 🟡 Serve | Só a landing, a página de preços e o blog |
| SaaS em crescimento | ✅ Ótimo | Páginas de conteúdo e de comparação trazem clientes |
| Sistema interno/corporativo | ❌ Evite | Está atrás de login; ninguém deve achá-lo no Google |
| API/integração | ❌ Evite | Não tem página para indexar |
| App mobile | ❌ Evite | Site de divulgação do app, sim; o app em si, não |

## Quando é bom

- Cada página responde a uma busca clara ("dentista em Campinas").
- O HTML já traz o texto, sem depender de JavaScript para aparecer.

## Quando é ruim

- Mesmo título em todas as páginas.
- Conteúdo só visível depois de login ou de clique.

## Como começar

### Cabeçalho de cada página

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Limpeza dental em Campinas | Clínica Sorriso</title>
  <meta name="description" content="Agende limpeza dental com a Clínica Sorriso. Atendimento de segunda a sábado, perto do centro de Campinas.">
  <link rel="canonical" href="https://www.clinicasorriso.example/servicos/limpeza-dental">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Limpeza dental em Campinas">
  <meta property="og:description" content="Agende online em poucos minutos.">
  <meta property="og:url" content="https://www.clinicasorriso.example/servicos/limpeza-dental">
  <meta property="og:image" content="https://www.clinicasorriso.example/og/limpeza.jpg">
  <meta name="twitter:card" content="summary_large_image">
</head>
<body>
  <h1>Limpeza dental em Campinas</h1>
</body>
</html>
```

### Checklist por página

| Item | Regra |
|---|---|
| `title` | Único, descreve a página, sem repetir palavra; marca no começo ou no fim. O Google não impõe limite, mas corta para caber na tela |
| `meta description` | Única por página, resume o conteúdo; o Google pode reescrevê-la |
| `h1` | Um por página, igual à ideia do título |
| URL | Limpa e legível: `/servicos/limpeza-dental`, sem `?id=123` |
| Canonical | Aponta para a URL preferida e evita duplicata (com e sem `www`, com parâmetros) |
| Open Graph e Twitter card | Controlam título e imagem ao compartilhar em redes e mensageiros |
| Imagens | `alt` descritivo, dimensões declaradas |

### sitemap.xml e robots.txt

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.clinicasorriso.example/servicos/limpeza-dental</loc>
    <lastmod>2026-11-24</lastmod>
  </url>
</urlset>
```

```
User-agent: *
Disallow: /painel/

Sitemap: https://www.clinicasorriso.example/sitemap.xml
```

O robots.txt controla o que o robô rastreia, e não o que entra no índice: a página bloqueada ainda pode aparecer se outros sites linkarem para ela. Para tirar do Google, use `<meta name="robots" content="noindex">` (e não bloqueie no robots.txt, senão o robô nem lê o `noindex`).

### Dados estruturados (JSON-LD)

JSON-LD é um bloco de JSON no HTML que descreve a página com o vocabulário do schema.org. O Google pede o tipo mais específico de `LocalBusiness`, e `address` e `name` são obrigatórios para rich result (aparência melhorada na busca).

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MedicalClinic",
  "name": "Clínica Sorriso",
  "telephone": "+55-19-0000-0000",
  "url": "https://www.clinicasorriso.example",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua Exemplo, 100",
    "addressLocality": "Campinas",
    "addressRegion": "SP",
    "postalCode": "13000-000",
    "addressCountry": "BR"
  }
}
</script>
```

Conferido na documentação do Google em 2026-11-24: Local business, Organization, Breadcrumb e Article estão na galeria de rich results. **FAQPage não gera mais rich result:** o Google informou que o recurso deixou de aparecer na busca (a partir de 7 de maio de 2026), então não gaste tempo com ele. O Google lista `LocalBusiness` e não cita `MedicalClinic`; o tipo é válido no schema.org, mas a elegibilidade do subtipo para rich result não foi confirmada. Valide com o Teste de Rich Results.

### Renderização

O Google executa JavaScript, mas na fila e com atraso, e nem todo robô de busca ou de rede social faz isso. Entregue o conteúdo no HTML:

| Abordagem | SEO |
|---|---|
| SSG (HTML gerado no build) | Melhor para conteúdo que muda pouco; ver [01-astro-conteudo.md](../../stacks/docs/01-astro-conteudo.md) |
| SSR (HTML gerado a cada pedido) | Bom para páginas dinâmicas; ver [02-nextjs-saas.md](../../stacks/docs/02-nextjs-saas.md) |
| SPA (só JavaScript no navegador) | Arriscado para páginas públicas; use só atrás de login |

### Velocidade e acessibilidade

- Core Web Vitals (LCP, INP e CLS) fazem parte da experiência de página; medidas e correções em [12-desempenho-e-rede.md](../../user-experience/docs/12-desempenho-e-rede.md).
- Boa acessibilidade ajuda o robô: `h1` a `h6` em ordem, `alt` nas imagens, texto de link que faça sentido ("ver horários", não "clique aqui"), `lang` correto.

### Ferramentas grátis

| Ferramenta | Para quê |
|---|---|
| Google Search Console | Enviar o sitemap, ver o que está indexado e os erros |
| Lighthouse (no Chrome DevTools) | Auditoria de SEO, desempenho e acessibilidade |
| Teste de Rich Results (Google) | Validar o JSON-LD |

## Combina com / alternativas

- [05-landing-saas.md](05-landing-saas.md): estrutura da landing que recebe este SEO.
- [01-fundamentos.md](01-fundamentos.md): contraste e acessibilidade.
- [13-estados-de-tela.md](13-estados-de-tela.md): página 404 amigável.
- [../../stacks/docs/01-astro-conteudo.md](../../stacks/docs/01-astro-conteudo.md) e [02-nextjs-saas.md](../../stacks/docs/02-nextjs-saas.md): renderização.
- [../../user-experience/docs/12-desempenho-e-rede.md](../../user-experience/docs/12-desempenho-e-rede.md): Core Web Vitals.

## Decisão rápida

- **Use se:** a página pública precisa ser achada por busca.
- **Evite se:** a página fica atrás de login ou o conteúdo é interno.
