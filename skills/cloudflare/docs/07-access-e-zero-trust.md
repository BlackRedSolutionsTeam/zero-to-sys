# Cloudflare Access e Zero Trust

> Uma porta de login na frente de painéis internos, para que só pessoas autorizadas cheguem neles.

| | |
|---|---|
| **Referência** | https://developers.cloudflare.com/cloudflare-one/ |
| **Categoria** | Borda |
| **Tipo** | Prática de controle de acesso na borda (Zero Trust) |
| **Vale para** | Painéis e ambientes internos com domínio: Coolify, Grafana, staging, documentação privada |
| **Verificado em** | 2026-11-25 |

## O que é

Zero Trust é a ideia de nunca confiar numa conexão só porque ela vem de "dentro". Toda pessoa precisa provar quem é antes de entrar.

O **Cloudflare Access** aplica isso: ele fica na frente de um site (uma "aplicação") e exige login antes de repassar a requisição para a origem. Quem não está na política vê a tela de bloqueio e a sua origem nem recebe o pedido.

No exemplo do plugin, a clínica de clinica-exemplo.com.br tem `coolify.clinica-exemplo.com.br`, `grafana.clinica-exemplo.com.br` e `staging.clinica-exemplo.com.br`. Os três ficam atrás do Access.

## Por que usar

- **Painel sem senha própria exposta:** o login passa a ser da Cloudflare, não do painel.
- **Sem VPN:** a pessoa abre o endereço e se autentica no navegador.
- **Lista de quem entra em um só lugar:** tirar uma pessoa da equipe é remover um e-mail.
- **Automação separada de pessoas:** a CI usa service token, não a conta de alguém.
- **Painéis como o Coolify** dão controle total do servidor; uma camada extra reduz o risco de um login fraco.

## Quando usar

- Painel de administração de infraestrutura exposto na internet.
- Ambiente de staging que não deve ser público nem indexado.
- Ferramenta interna sem login próprio decente.
- Ao usar [Tunnel](06-tunnel-e-protecao-da-origem.md), para que o serviço publicado exija login.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Só para o painel e o staging; o site é público |
| MVP de SaaS | ✅ Ótimo | Protege staging e painéis de graça, sem montar VPN |
| SaaS em crescimento | ✅ Ótimo | Centraliza o acesso da equipe e dos painéis de operação |
| Sistema interno/corporativo | ✅ Ótimo | Login por e-mail ou provedor de identidade da empresa |
| API/integração | 🟡 Serve | Protege a documentação e o staging; a API pública não deve usar |
| App mobile com backend | ❌ Evite | O app não faz login no navegador; não ponha a API de produção atrás do Access |

## Quando é bom

- **Configuração rápida:** poucos minutos para proteger um hostname.
- **Logs de acesso:** você vê quem entrou e quando.
- **Políticas claras:** por e-mail, por domínio de e-mail ou por grupo.
- **Service tokens** permitem que a CI e scripts passem sem login interativo.

## Quando é ruim

- **Depende da Cloudflare:** se o Zero Trust cair, o painel fica fechado para todos. Guarde um acesso de emergência (SSH).
- **Não serve para público aberto:** cliente final não deve passar por ele.
- **Webhooks de terceiros** (pagamento, e-mail) não fazem login: exclua o caminho deles da aplicação ou use service token quando o remetente permitir mandar cabeçalhos.
- **Origem ainda exposta:** se o IP do servidor responde direto, o Access é contornado. Feche a origem como em [Tunnel e proteção da origem](06-tunnel-e-protecao-da-origem.md).
- **Limite de usuários do plano grátis:** o número exato não foi conferido nesta verificação (as páginas de plano não mostraram o valor). Consulte https://www.cloudflare.com/plans/zero-trust-services/ e a página de preços do Zero Trust antes de contar com ele.

## Como começar

Pelo painel (nomes de menu podem mudar; confira em developers.cloudflare.com/cloudflare-one):

1. Abra o Zero Trust da conta e escolha o plano grátis, se for a primeira vez.
2. Em controle de acesso, crie uma aplicação do tipo self-hosted com o hostname `coolify.clinica-exemplo.com.br`.
3. Crie uma política com a ação **Allow** e a regra de quem entra (e-mails da equipe).
4. Escolha o método de login. O **One-time PIN** vem pronto: a pessoa digita o e-mail e recebe um código por e-mail.
5. Teste em uma janela anônima.

Sobre o One-time PIN (conferido em 2026-11-25):

- O código expira em 10 minutos e vale uma vez só.
- Pedir um código novo invalida o anterior.
- O e-mail só é enviado a quem a política permite. Quem não está na lista vê a mesma mensagem, mas nada chega.
- Se aparecer "já foi usado", um filtro de e-mail provavelmente abriu o link antes. Peça outro código.

Login por Google ou outro provedor de identidade é configurado na lista de métodos de login do Zero Trust. Confira o provedor na documentação antes de depender dele. Para permitir um domínio inteiro (todos de `@clinica-exemplo.com.br`), procure na documentação de políticas o seletor de e-mail por domínio.

### Service token para a CI

Um service token é um par de credenciais para máquinas. Conferido em 2026-11-25:

- Crie o token no Zero Trust. O Client Secret aparece uma única vez; guarde no cofre de segredos da CI.
- A política da aplicação precisa ter a ação **Service Auth**. Com **Allow**, o Access ainda pede login.
- A expiração é definida na criação. Renovar reinicia o prazo a partir de agora.
- Girar o segredo mantém o Client ID e aceita um período de tolerância configurável.

A CI manda os dois cabeçalhos:

```sh
curl -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
     -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
     https://staging.clinica-exemplo.com.br/saude
```

No GitHub Actions, guarde os dois valores em secrets do repositório e leia-os como variáveis de ambiente. Veja segredos em [infra](../../infra/docs/).

Antes de ligar o Access ao staging, confirme que a CI passa pelo token; senão o deploy de teste quebra.

## Combina com / alternativas

- [Tunnel e proteção da origem](06-tunnel-e-protecao-da-origem.md): publica o painel sem abrir porta e o Access exige login.
- [WAF, rate limit e bots](05-waf-rate-limit-e-bots.md): proteção para o que é público.
- [VPS com Coolify](../../infra/docs/02-vps-coolify-dokploy.md): o painel que mais precisa dessa camada.
- Alternativas: VPN (WireGuard, Tailscale), lista de IPs no nginx, autenticação básica no proxy. Mais simples, mas sem login por pessoa nem logs.

## Decisão rápida

- **Use se:** há um painel ou staging na internet e você quer login por pessoa, sem VPN e sem custo inicial.
- **Evite se:** o destino é o público geral ou um app que não abre navegador, ou se você não pode depender da Cloudflare para entrar na sua infraestrutura.
