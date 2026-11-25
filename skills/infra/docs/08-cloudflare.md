# Cloudflare

> Camada na frente do sistema com DNS, CDN, WAF e proteção contra DDoS, incluídos até no plano grátis.

| | |
|---|---|
| **Site** | https://www.cloudflare.com |
| **Categoria** | Borda, CDN e segurança de rede |
| **Tipo** | Serviço de borda (proxy reverso, DNS, CDN, WAF) |
| **Stack** | Independente de stack; funciona na frente de qualquer origem com domínio |
| **Preço** | Free US$ 0; Pro US$ 20/mês (anual) ou US$ 25 (mensal); Business US$ 200/mês (anual) ou US$ 250 (mensal). WAF e DDoS sem medição incluídos em todos. Workers: grátis (100 mil requisições por dia) ou Paid a US$ 5/mês com 10 milhões de requisições incluídas; R2: US$ 0,015 por GB-mês, 10 GB grátis e sem taxa de saída; D1: grátis com 5 GB, e no plano Paid US$ 0,75 por GB-mês acima de 5 GB (documentação da Cloudflare, conferido em 2026-11-24) |
| **Licença** | Serviço proprietário |
| **Verificado em** | 2026-11-24 |

## O que é

Você muda os servidores de nome do domínio para a Cloudflare. A partir daí o tráfego passa por ela: ela responde o DNS, guarda cópias de arquivos estáticos perto do usuário, bloqueia ataques conhecidos e esconde o IP real da origem.

Além disso há produtos de computação (Workers) e armazenamento (R2, D1), que têm cobrança própria e não foram detalhados nesta verificação.

## Por que usar

- **Proteção desde o plano grátis:** WAF e proteção contra DDoS em todos os planos listados.
- **CDN:** menos carga na origem e site mais rápido.
- **TLS e redirecionamentos** gerenciados.
- **DNS rápido** e com API, que o IaC consegue controlar.
- **Esconde a origem:** o IP do servidor não fica exposto.

## Quando usar

- Qualquer site ou API público com domínio próprio.
- Servidor único (VPS) que precisa de proteção e cache.
- Quando há tráfego malicioso ou raspagem de dados.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ✅ Ótimo | CDN e hospedagem estática baratas |
| MVP / protótipo | ✅ Ótimo | DNS, TLS e WAF sem custo |
| SaaS pequeno | ✅ Ótimo | Esconde a origem e filtra abuso |
| SaaS em crescimento | ✅ Ótimo | Regras de WAF, cache e limites por rota |
| Sistema corporativo | 🟡 Serve | Bom na borda; exigências de contrato pedem o plano Contract (preço sob consulta, cloudflare.com/plans, conferido em 2026-11-24) |
| API autenticada, sem cache | 🟡 Serve | Ganha segurança e DNS; pouco ganho de cache |
| Tráfego de vídeo em volume | 🟡 Serve | Cloudflare Stream cobra à parte: US$ 5 por mês a cada 1.000 minutos armazenados e US$ 1 por 1.000 minutos entregues, sem plano grátis (developers.cloudflare.com/stream/pricing, conferido em 2026-11-24) |
| Sistema só interno, sem domínio público | ❌ Evite | Sem exposição pública, pouco a proteger na borda |

## Quando é bom

- **Custo-benefício:** o grátis cobre o que a maioria dos projetos pequenos precisa.
- **Facilidade:** poucos passos para ficar protegido.
- **Dados de tráfego** visíveis no painel.
- **Integra com IaC:** DNS e regras em código.

## Quando é ruim

- **Ponto único na frente:** se a Cloudflare tem problema, seu site sente.
- **Cache errado serve conteúdo antigo ou de outro usuário:** nunca coloque respostas autenticadas em cache sem regras claras.
- **Origem ainda aberta:** se o IP real é acessível, o ataque pode contornar a borda. Libere a origem só para a Cloudflare.
- **Regras demais** quebram usuários legítimos; teste em modo de registro antes de bloquear.
- **Dependência do DNS deles** ao migrar o domínio.
- **Recursos avançados são pagos** (Pro e Business estão na tabela acima, conferidos em 2026-11-24; o plano Contract tem preço sob consulta).

## Como começar

1. Crie a conta e adicione o domínio.
2. Troque os servidores de nome no registrador pelos indicados.
3. Ative o modo de criptografia "Full (strict)" e o redirecionamento para HTTPS.
4. Ative o WAF com as regras gerenciadas e crie uma regra de limite de requisições para login e APIs.
5. Na origem, aceite conexões apenas dos endereços da Cloudflare.

Os nomes exatos das opções vêm do painel e da documentação oficial; não foram reconferidos aqui.

## Combina com / alternativas

- [PaaS](01-paas.md) e [VPS](02-vps-coolify-dokploy.md): na frente de qualquer um.
- [Segurança base](12-seguranca-base.md): a borda é uma camada, não a única.
- [OpenTofu ou Pulumi](06-iac-opentofu-pulumi.md): DNS e regras em código.
- Alternativas: CDN e WAF da própria nuvem ([nuvem grande](03-nuvem-grande.md)), Vercel para sites hospedados nela.

## Decisão rápida

- **Use se:** o sistema tem domínio público e você quer DNS, cache, WAF e DDoS sem custo inicial.
- **Evite se:** o sistema é só interno, ou você não pode depender de um terceiro na frente de tudo.
