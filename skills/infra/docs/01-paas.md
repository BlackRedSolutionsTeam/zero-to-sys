# PaaS (Vercel, Railway, Render e Fly.io)

> Plataformas em que você envia o código e elas cuidam de servidor, TLS, deploy e escala básica, ideais para o começo de quase todo projeto.

| | |
|---|---|
| **Site** | https://vercel.com, https://railway.com, https://render.com, https://fly.io |
| **Categoria** | Hospedagem |
| **Tipo** | Plataforma como serviço (PaaS), cobrança por plano e uso |
| **Stack** | Vercel: front-ends e funções (Next.js e similares); Railway, Render e Fly.io: qualquer app em contêiner ou buildpack |
| **Preço** | Vercel Hobby grátis, Pro US$ 20/mês por pessoa; Railway teste grátis (US$ 5 únicos, 30 dias), Hobby US$ 5/mês, Pro US$ 20/mês; Fly.io sem taxa fixa, plano Free com US$ 5 de uso/mês só com cartão cadastrado (sem cartão, US$ 1 único que expira em 7 dias; docs.fly.io/about/free-plan, conferido em 2026-11-24); Render: Hobby grátis (US$ 0/mês) e Pro a US$ 25/mês por workspace, mais a computação (instância paga de US$ 7/mês com 512 MB, ou US$ 25/mês com 1 CPU e 2 GB; página de preços, conferido em 2026-11-24) |
| **Licença** | Serviços proprietários |
| **Verificado em** | 2026-11-24 |

## O que é

Um PaaS tira do dev a parte de servidor. Você conecta o repositório (ou envia uma imagem), e a plataforma compila, publica, coloca HTTPS e reinicia o app se ele cair.

Cada uma tem um foco. **Vercel** é forte em front-end e funções, com CDN própria. **Railway** é simples para app, banco e worker no mesmo painel, com cobrança por uso. **Render** é parecido com o antigo modelo Heroku: serviço web, worker, cron e Postgres. **Fly.io** roda contêineres (Machines) perto do usuário, em várias regiões, com mais controle e mais responsabilidade.

Na Vercel, o plano Hobby não permite comprar uso extra além dos limites. No Render, a página de preços não trouxe os detalhes; a documentação diz que serviço web grátis dorme após 15 minutos sem tráfego e que o Postgres grátis expira em 30 dias.

## Por que usar

- **Sem servidor para administrar:** nada de atualizar sistema operacional ou configurar proxy.
- **Deploy pelo Git:** cada push gera uma versão, e a maioria oferece prévia por pull request.
- **Começo barato ou grátis:** dá para validar a ideia sem gastar.
- **Rollback rápido:** voltar à versão anterior leva um clique ou um comando.
- **Tempo do dev vai para o produto**, não para a infra.

## Quando usar

- MVP, protótipo e SaaS nos primeiros meses.
- Time pequeno sem ninguém dedicado a infraestrutura.
- Front-end e API que cabem em contêiner ou em funções.
- Quando velocidade de entrega vale mais que custo por unidade de consumo.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ✅ Ótimo | Vercel (e Cloudflare Pages) servem de graça ou quase |
| MVP / protótipo | ✅ Ótimo | Sobe em minutos, com plano grátis ou de US$ 5 |
| SaaS pequeno | ✅ Ótimo | Plano pago simples, com preview e rollback |
| SaaS em crescimento | 🟡 Serve | Funciona, mas a conta por uso cresce e o controle de rede é limitado |
| Sistema corporativo | ❌ Evite | Exige rede privada, auditoria e contratos que o PaaS costuma não oferecer no plano básico |
| API com tráfego alto e constante | 🟡 Serve | Pagar por uso contínuo costuma sair mais caro que VPS ou nuvem grande |
| Job pesado ou longo | 🟡 Serve | Prefira Railway, Render ou Fly.io; funções da Vercel têm limites de tempo |
| App com dados sob regra de localização | 🟡 Serve | Regiões nas páginas oficiais (2026-11-24): [Vercel](https://vercel.com/docs/regions) tem São Paulo (gru1) e UE (Frankfurt, Paris, Dublin, Estocolmo); [Fly.io](https://docs.fly.io/reference/regions) tem São Paulo (gru) e UE (Amsterdã, Frankfurt, Paris, Estocolmo); [Render](https://render.com/docs/regions) tem só Frankfurt, sem Brasil; [Railway](https://docs.railway.com/reference/deployment-regions) tem só Amsterdã, sem Brasil. Confira também o contrato de cada uma |

## Quando é bom

- **Zero operação:** o time não precisa saber de servidor.
- **Previsível no início:** planos de entrada com preço claro (Railway Hobby US$ 5; Vercel Pro US$ 20).
- **Escala simples:** subir tamanho ou número de instâncias é configuração.
- **Ecossistema:** banco, cron, domínio e logs no mesmo lugar.

## Quando é ruim

- **Custo cresce com o uso:** Railway cobra todo o uso quando passa do crédito incluído; Vercel Pro cobra por seat e por consumo acima do crédito. Defina limite de gasto.
- **Planos grátis dormem ou expiram:** Render grátis dorme após 15 min e o Postgres grátis expira em 30 dias (apaga após 14 dias de carência). Não use para usuário real.
- **Trial do Railway acaba:** com o fim do crédito, os deploys param.
- **Dependência da plataforma:** buildpacks e recursos próprios dificultam sair. Mitigação: usar Dockerfile.
- **Controle de rede limitado:** pouca ou nenhuma rede privada com a sua nuvem, sem peering.
- **Fly.io exige mais conhecimento:** o plano Free tem teto de 3 Machines, sem Machines de performance (docs.fly.io/about/free-plan, 2026-11-24), e o modelo é de baixo nível.

## Como começar

Vercel (CLI oficial):

```bash
npm i -g vercel
vercel
```

Fly.io (CLI `flyctl`; `fly launch` e `fly deploy` constam na referência oficial, conferido em 2026-11-24):

```bash
fly launch
fly deploy
```

Railway e Render: conecte o repositório pelo painel e escolha o Dockerfile ou o buildpack. Configure limite de gasto e alerta de orçamento antes do primeiro deploy.

## Combina com / alternativas

- [Postgres gerenciado](05-postgres-gerenciado.md): banco fora da plataforma ou dentro dela.
- [Cloudflare](08-cloudflare.md): DNS, WAF e cache na frente.
- [Segredos e configuração](09-segredos-e-configuracao.md): variáveis de ambiente por ambiente.
- Alternativas: [VPS com Coolify ou Dokploy](02-vps-coolify-dokploy.md) para custo fixo; [nuvem grande](03-nuvem-grande.md) para escala e conformidade.

## Decisão rápida

- **Use se:** o projeto está no começo ou é pequeno, o time não tem quem opere infra e o custo mensal ainda é baixo.
- **Evite se:** o tráfego é alto e constante, há exigência de rede privada ou auditoria, ou o orçamento não admite conta variável.
