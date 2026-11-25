# WAF, rate limit e bots na Cloudflare

> Ligue o WAF gerenciado, proteja `/admin` e `/login` com regras personalizadas e limite de taxa, use Bot Fight Mode e Turnstile contra robôs, e valide o Turnstile sempre no servidor.

| | |
|---|---|
| **Referência** | developers.cloudflare.com/waf (managed rules, custom rules, rate limiting rules), /bots (Bot Fight Mode), /fundamentals (Under Attack mode), /turnstile (validação no servidor) |
| **Categoria** | Borda |
| **Tipo** | Prática de proteção na borda |
| **Vale para** | Qualquer site ou API com domínio na Cloudflare e proxy ligado (nuvem laranja); plano Free como base |
| **Verificado em** | 2026-11-25 |

## O que é

WAF (Web Application Firewall) é um filtro que olha cada requisição antes de ela chegar ao seu servidor e decide: deixar passar, desafiar, limitar ou bloquear. Na Cloudflare ele tem quatro peças:

- **Managed rules:** conjuntos de regras prontos, mantidos pela Cloudflare.
- **Custom rules:** regras suas, escritas com uma expressão (ex.: caminho começa com `/admin`).
- **Rate limiting rules:** regras que contam requisições por período.
- **Bots e Turnstile:** detecção de robôs e um "captcha" sem quebra-cabeça.

Exemplo do doc: sistema de agendamento de clínica, com `app.clinica-exemplo.com.br`, API em `api.clinica-exemplo.com.br` e staging em `staging.clinica-exemplo.com.br`.

## Por que usar

- **Barra o volume longe do servidor:** o ataque morre na borda e não gasta CPU da VPS.
- **Fecha portas óbvias:** `/admin` e `/login` são os alvos de robôs.
- **Sem custo no Free** para o essencial (limites abaixo).
- **Complementa a aplicação:** a borda não conhece o usuário logado; veja [Rate limit](../../security/docs/06-rate-limit.md).

## Quando usar

- Sempre que o domínio estiver com proxy ligado (veja [DNS e proxy](02-dns-e-proxy.md)).
- Painel administrativo, login, recuperação de senha e formulário público.
- Durante ataque: Under Attack como último recurso.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Managed rules e Bot Fight Mode bastam; Turnstile no formulário de contato |
| MVP de SaaS | ✅ Ótimo | Regra no `/login` e `/admin` no primeiro dia, sem custo |
| SaaS em crescimento | ✅ Ótimo | Precisa de mais regras e de limite por rota; avalie plano pago |
| Sistema interno/corporativo | 🟡 Serve | Melhor fechar o painel com [Access](07-access-e-zero-trust.md) do que com regra de caminho |
| API/integração | 🟡 Serve | WAF e rate limit servem; Bot Fight Mode pode desafiar clientes legítimos |
| App mobile com backend | 🟡 Serve | App não resolve desafio de navegador; evite desafio na API e use limite na aplicação |
| Origem acessível sem passar pela Cloudflare | ❌ Evite | O atacante vai direto ao IP e ignora tudo; feche a origem ([doc 06](06-tunnel-e-protecao-da-origem.md)) |

## Quando é bom

- **Camadas:** borda para volume, aplicação para regra de negócio.
- **Ação gradual:** começar com Managed Challenge (o visitante prova que é humano) e só bloquear depois de medir.
- **Turnstile** troca captcha chato por uma checagem quase invisível.

## Quando é ruim

- **Regra ampla demais** bloqueia paciente real; teste antes de bloquear.
- **Bloquear país inteiro** pega quem viaja, usa VPN ou roda um serviço fora do país.
- **Bot Fight Mode em API ou app mobile** pode desafiar tráfego legítimo, e não aceita exceção por regra do WAF.
- **Só o widget do Turnstile, sem validar no servidor:** o robô envia o formulário direto e ignora o widget.
- **Limite do Free é curto:** 1 regra de rate limit, janela de 10 s, chave só por IP.

## Como começar

**Limites do plano Free** (conferido em 2026-11-25 nas páginas oficiais; recheque antes de depender):

| Recurso | Free |
|---|---|
| Managed rules | Só o Cloudflare Free Managed Ruleset; o Cloudflare Managed Ruleset e o OWASP Core Ruleset não estão no Free |
| Custom rules | 5 regras; todas as ações, exceto Log |
| Rate limiting rules | 1 regra; período de contagem 10 s; bloqueio de 10 s; contagem por IP |
| Bot Fight Mode | Gratuito, liga e desliga em Security > Settings > Bot traffic |

A página não diz se o Free Managed Ruleset vem ligado por padrão: confira em Security > WAF e ative se estiver desligado.

**Custom rules.** Painel: Security > WAF > Custom rules > Create rule. Expressões prontas:

```
(http.host eq "app.clinica-exemplo.com.br" and starts_with(http.request.uri.path, "/admin"))
```

```
(http.host eq "api.clinica-exemplo.com.br" and http.request.uri.path eq "/login" and http.request.method eq "POST")
```

Ação sugerida: Managed Challenge. Para o `/admin`, melhor ainda é restringir por IP:

```
(starts_with(http.request.uri.path, "/admin") and not ip.src in {203.0.113.10 203.0.113.11})
```

Ação: Block. Os IPs acima são de exemplo (faixa de documentação).

**Bloquear país ou ASN** (ASN é o número da rede de um provedor):

```
(ip.src.country eq "RU")
```

```
(ip.src.asnum in {64496 64497})
```

`ip.src.country` usa código de 2 letras (ISO 3166-1 Alpha 2); `ip.geoip.country` está obsoleto. `ip.src.asnum` é numérico. Prefira Managed Challenge a Block em país.

**Rate limiting.** Security > WAF > Rate limiting rules. No Free há uma só regra: use-a no login.

```
(http.request.uri.path eq "/login" and http.request.method eq "POST")
```

Contagem por IP, período de 10 s, limite pequeno (ex.: 5 requisições), ação Block. A contagem por e-mail e a janela de 1 minuto ficam na aplicação ([Rate limit](../../security/docs/06-rate-limit.md)).

**Under Attack.** Mostra uma tela de verificação a todo visitante. Pausa o acesso normal e afeta análises, então use só durante ataque. Painel: Quick Actions na visão geral da zona. Para um caminho só, crie uma Configuration Rule com `(starts_with(http.request.uri.path, "/admin"))` e ligue "I'm Under Attack". Clientes sem JavaScript (APIs) podem não passar.

**Turnstile.** Crie o widget em Turnstile no painel, ponha a chave pública (site key) no formulário e guarde a chave secreta no servidor. Valide sempre no servidor:

```ts
const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    secret: process.env.TURNSTILE_SECRET_KEY,
    response: token,
    remoteip: ip
  })
})
const result = await res.json()
if (!result.success) throw new Error('Verificação falhou')
```

O token vale 300 segundos e só pode ser usado uma vez (reuso volta `timeout-or-duplicate`). Confira também `hostname` na resposta.

## Combina com / alternativas

- [Rate limit na aplicação](../../security/docs/06-rate-limit.md): a borda corta volume, a aplicação limita por usuário e e-mail.
- [Proteção da origem](06-tunnel-e-protecao-da-origem.md): sem ela, o WAF pode ser contornado.
- [Access e Zero Trust](07-access-e-zero-trust.md): melhor opção para painéis internos.
- Alternativas: hCaptcha e reCAPTCHA no lugar do Turnstile; WAF da nuvem grande.

## Decisão rápida

- **Use se:** o domínio está na Cloudflare e há login, painel ou formulário público.
- **Evite se:** a origem continua aberta ao mundo, ou se você bloquearia sem testar antes em Managed Challenge.
