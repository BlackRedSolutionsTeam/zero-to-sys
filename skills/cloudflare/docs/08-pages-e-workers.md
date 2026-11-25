# Cloudflare Pages e Workers

> Pages hospeda site estático com deploy pelo Git; Workers roda funções pequenas na borda, perto do usuário.

| | |
|---|---|
| **Referência** | https://developers.cloudflare.com/pages/ e https://developers.cloudflare.com/workers/ |
| **Categoria** | Borda |
| **Tipo** | Prática de hospedagem estática e computação na borda |
| **Vale para** | Sites estáticos, redirecionamentos e lógica leve na frente da origem |
| **Verificado em** | 2026-11-25 |

## O que é

**Pages** publica arquivos estáticos (HTML, CSS, JS) numa rede global. Você liga um repositório do GitHub, e cada push gera um deploy.

**Workers** executa código JavaScript ou TypeScript na borda, sem servidor para cuidar. Cada requisição roda num "isolate", um ambiente leve e isolado. Serve para redirecionar, reescrever, validar um cabeçalho ou montar uma resposta curta.

O **Wrangler** é a ferramenta de linha de comando que cria, testa e publica Workers (e projetos Pages).

## Por que usar

- **Sem servidor para manter** e sem custo inicial no site estático.
- **Deploy por push**, com um endereço de pré-visualização por branch.
- **Perto do usuário:** resposta rápida em qualquer região.
- **Tudo na mesma conta** do DNS e da proteção.

## Quando usar

- Site institucional ou blog da clínica em clinica-exemplo.com.br, gerado como estático.
- Funções curtas: redirecionar por país, checar um token antes da origem, responder um webhook simples.
- Documentação pública e landing pages.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Estático com deploy pelo Git, rápido e barato |
| MVP de SaaS | 🟡 Serve | Bom para o site de marketing; o app costuma precisar de servidor |
| SaaS em crescimento | 🟡 Serve | Workers para pontos específicos na borda, não como núcleo |
| Sistema interno/corporativo | 🟡 Serve | Páginas estáticas atrás do [Access](07-access-e-zero-trust.md) |
| API/integração | 🟡 Serve | Funções leves sim; API grande com banco e bibliotecas Node, não |
| App mobile com backend | ❌ Evite | Backend com filas, conexões longas e bibliotecas pesadas cabe melhor em servidor |

## Quando é bom

- **Estático é simples:** build no Git, arquivos na borda.
- **Previews por branch:** cada branch fora da produção ganha um deploy próprio e atualiza o pull request.
- **Workers para o que é pequeno:** inicia rápido e escala sozinho.
- **Segredos e variáveis** pelo Wrangler.

## Quando é ruim

- **Runtime diferente do Node:** Workers não é um servidor Node completo. Módulos como `node:child_process`, `node:worker_threads` e `node:vm` não funcionam (podem ser importados, mas não operam). A compatibilidade com Node é por flag e por data: confira a página de compatibilidade antes de portar uma biblioteca.
- **Acoplamento:** usar KV, D1, Durable Objects e as APIs específicas deixa o código preso à Cloudflare. Mantenha a regra de negócio em módulos puros e use a borda só como casca.
- **CPU baixa no grátis:** 10 ms de CPU por requisição. Trabalho pesado (imagem, PDF, criptografia grande) estoura.
- **Cota diária:** passou de 100 mil requisições por dia, o Worker deixa de atender até a virada; um pico pode derrubar a função.
- **Depuração mais difícil** do que um servidor comum; use `wrangler tail`.
- **API de produção** com banco relacional exige cuidado com conexões vindas da borda; considere servidor tradicional.

## Como começar

### Limites do plano grátis (conferido em 2026-11-25 em developers.cloudflare.com)

| Workers Free | Valor |
|---|---|
| Requisições por dia | 100.000 (zera à meia-noite UTC) |
| CPU por requisição HTTP | 10 ms |
| Memória por isolate | 128 MB |
| Subrequisições por invocação | 50 |
| Tamanho do Worker (sem compactar) | 64 MiB |
| Workers por conta | 100 |
| Cron Triggers por conta | 5 |

| Pages Free | Valor |
|---|---|
| Builds por mês | 500 |
| Arquivos por site | 20.000 |
| Tamanho máximo por arquivo | 25 MiB |
| Domínios próprios por projeto | 100 |
| Projetos por conta | 100 |

As Functions do Pages contam na cota dos Workers. Preço dos planos pagos: consulte a página oficial.

### Pages com Git

1. No painel, abra Workers & Pages, depois Create application, Pages, Connect to Git.
2. Autorize o GitHub e escolha o repositório (público ou privado).
3. Informe a branch de produção, o comando de build (vazio se não houver) e a pasta de saída.
4. Em monorepo, preencha o diretório raiz.
5. Salve e faça o deploy. Depois, adicione o domínio próprio em `www.clinica-exemplo.com.br` pela aba de domínios.

### Worker com Wrangler

Instale na pasta do projeto e crie:

```sh
npm install --save-dev wrangler
npx wrangler init clinica-borda
```

Rode local, publique, guarde segredo e veja logs:

```sh
npx wrangler dev
npx wrangler deploy
npx wrangler secret put WEBHOOK_TOKEN
npx wrangler tail
```

Exemplo mínimo que redireciona o caminho antigo, em `src/index.ts`:

```ts
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/agenda") {
      return Response.redirect("https://app.clinica-exemplo.com.br/agenda", 301);
    }
    return fetch(request);
  },
};
```

Para redirecionamento simples, prefira as regras de redirecionamento da Cloudflare (sem código). Use Worker só quando houver lógica.

Mantenha as chaves de API fora do código: use `wrangler secret put`. A autenticação do Wrangler com a conta e o token de escopo mínimo estão em [Cloudflare com IaC](10-cloudflare-com-iac.md).

## Combina com / alternativas

- [DNS e proxy](02-dns-e-proxy.md): o domínio aponta para o Pages ou para a rota do Worker.
- [Cache e performance](04-cache-e-performance.md): Pages já cacheia o estático.
- [Access](07-access-e-zero-trust.md): protege previews e áreas internas.
- [PaaS](../../infra/docs/01-paas.md) e [VPS](../../infra/docs/02-vps-coolify-dokploy.md): para API e app com banco.
- Alternativas ao Pages: Vercel, Netlify, GitHub Pages.

## Decisão rápida

- **Use se:** o site é estático ou você precisa de lógica curta na borda, e quer deploy pelo Git sem servidor.
- **Evite se:** a aplicação depende de bibliotecas Node completas, processos longos ou conexões persistentes, ou se você não quer ficar preso às APIs da Cloudflare.
