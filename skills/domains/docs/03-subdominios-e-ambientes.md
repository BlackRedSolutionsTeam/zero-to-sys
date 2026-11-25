# Subdomínios e ambientes

> Dê a cada parte do sistema o seu subdomínio (`app.`, `api.`, `staging.`, `admin.`, `status.`), escolha um endereço canônico entre `www` e apex e use wildcard só quando precisar.

| | |
|---|---|
| **Referência** | RFC 1034 e RFC 1035 (DNS); documentação da Cloudflare (Redirect Rules, proxy de DNS); Google Search Central (URL canônica e `noindex`); documentação do Let's Encrypt |
| **Categoria** | Domínios |
| **Tipo** | Prática de organização de DNS |
| **Vale para** | Qualquer sistema com domínio próprio; exemplos com `clinica-exemplo.com.br` |
| **Verificado em** | 2026-11-25 |

## O que é

Subdomínio é o prefixo na frente do domínio: em `app.clinica-exemplo.com.br`, o `app` é o subdomínio. O apex (ou raiz) é o domínio sem prefixo: `clinica-exemplo.com.br`. Cada subdomínio tem seus próprios registros DNS e pode apontar para um servidor diferente.

Exemplo do doc: sistema de agendamento de clínica. O site de apresentação fica no apex, o sistema em `app.`, a API em `api.` e o teste em `staging.`.

## Por que usar

- **Separação:** site, sistema e API podem ficar em hospedagens diferentes e mudar sem afetar os outros.
- **Segurança:** cookie e política de acesso ficam presos a cada parte. Um painel `admin.` pode ter regras de acesso próprias.
- **Ambientes claros:** `staging.` deixa testar sem mexer em produção.
- **Troca fácil:** mudar de servidor vira trocar um registro, não reconfigurar o cliente.

## Quando usar

- Quando o sistema tem mais de uma parte (site, app, API, painel).
- Quando existe ambiente de teste.
- Quando uma parte vai para outro provedor (status page, ajuda, blog).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Basta apex e `www`; subdomínio só para blog ou loja externa |
| MVP de SaaS | ✅ Ótimo | Apex para o site, `app.` para o sistema e `api.` desde o início |
| SaaS em crescimento | ✅ Ótimo | `staging.`, `admin.` e `status.` separam risco e responsabilidade |
| Sistema interno/corporativo | ✅ Ótimo | Um subdomínio da empresa (`sistema.empresa.com.br`) evita comprar domínio novo |
| API/integração | ✅ Ótimo | `api.` fixo permite trocar a hospedagem sem avisar clientes |
| App mobile com backend | ✅ Ótimo | O app guarda a URL da API; um `api.` estável evita nova versão na loja |
| Página única sem backend | ❌ Evite | Subdomínios extras só criam registros para manter |

## Quando é bom

- **Nomes previsíveis:** `app.` para o sistema, `api.` para a API, `admin.` para o painel interno, `status.` para a página de status.
- **Um apontamento por parte:** cada subdomínio aponta para o seu serviço.
- **Staging parecido com produção:** mesmo tipo de hospedagem, dados fictícios.

## Quando é ruim

- **Subdomínio demais:** cada um é mais um certificado, um registro e uma coisa para esquecer.
- **Wildcard sem necessidade:** o registro `*` responde por qualquer nome, inclusive os que ninguém criou. Isso esconde erro de digitação e aumenta o risco de takeover (alguém reivindicar um serviço que o registro ainda aponta).
- **CNAME para serviço que você apagou:** o nome fica apontando para um recurso que outra pessoa pode registrar. Apague o registro junto com o serviço.
- **Staging aberto:** o Google indexa e o teste aparece na busca ao lado da produção.

## Como começar

Registros de exemplo (a coluna Valor muda conforme a hospedagem; a Cloudflare permite CNAME no apex por flattening, veja [DNS, registros e propagação](02-dns-registros-e-propagacao.md)):

| Tipo | Nome | Valor | Uso |
|---|---|---|---|
| A ou CNAME | `@` | IP ou host do site | Apex (endereço canônico) |
| CNAME | `www` | `clinica-exemplo.com.br` | Redireciona para o apex |
| CNAME | `app` | host do sistema | Produção |
| CNAME | `api` | host da API | Produção |
| CNAME | `staging` | host do teste | Homologação |
| CNAME | `status` | host da página de status | Serviço externo |

**www x apex.** Escolha um só como endereço canônico (o oficial) e redirecione o outro com status 301 (permanente). Para site novo, o apex é curto e comum; `www` facilita quando o DNS do provedor não aceita CNAME no apex. Qualquer um serve, desde que o outro redirecione e o HTTPS cubra os dois. Na Cloudflare use uma Redirect Rule (regra de redirecionamento); em outros provedores, o painel da hospedagem costuma ter a opção.

Conferir o redirecionamento:

```bash
curl -sI https://www.clinica-exemplo.com.br | grep -i -E "^(HTTP|location)"
```

A resposta deve trazer `301` e `location: https://clinica-exemplo.com.br/`.

**Staging fora do Google.** Use três camadas juntas:

1. Senha na frente (autenticação básica ou o acesso da Cloudflare). É a única que impede de verdade a leitura.
2. Cabeçalho `X-Robots-Tag: noindex, nofollow` em todas as respostas.
3. `robots.txt` com `Disallow: /`. Sozinho não basta: o Google pode indexar a URL sem ler a página, e `noindex` só funciona se o robô puder ler.

```nginx
add_header X-Robots-Tag "noindex, nofollow" always;
auth_basic "Staging";
auth_basic_user_file /etc/nginx/.htpasswd;
```

**Wildcard.** Use `*.clinica-exemplo.com.br` quando cada cliente ganha um subdomínio automático (`clinica-a.app...`) ou quando previews de PR criam nomes dinâmicos. O certificado wildcard exige validação DNS-01 (veja [Certificados e HTTPS](05-certificados-e-https.md)). Com poucos subdomínios fixos, crie um registro por nome.

Dica: registros específicos vencem o wildcard, então `app` continua apontando para o seu destino mesmo com `*` criado.

**Painel `admin.` e `status.`.** Deixe o `admin.` atrás de login forte e, se possível, de uma camada de acesso (IP ou identidade). O `status.` fica em serviço externo de página de status, para continuar no ar quando o seu sistema cair: não hospede a página de status no mesmo servidor que ela monitora.

Checklist de fechamento: todo subdomínio tem dono, destino e HTTPS válido; nome sem uso foi apagado; staging tem senha e `noindex`.

## Combina com / alternativas

- [DNS, registros e propagação](02-dns-registros-e-propagacao.md): como criar cada registro.
- [Certificados e HTTPS](05-certificados-e-https.md): um certificado por nome ou um wildcard.
- [Cloudflare](../../infra/docs/08-cloudflare.md): redirecionamento, proxy e acesso protegido ao staging.
- [E-mail do domínio](04-email-do-dominio-spf-dkim-dmarc.md): o e-mail transacional ganha o próprio subdomínio.
- Alternativa: caminhos (`clinica-exemplo.com.br/app`) em vez de subdomínios, com um proxy na frente. Mais simples no DNS, mas mistura cookies e deploy.

## Decisão rápida

- **Use se:** o sistema tem site, app e API, ou precisa de ambiente de teste separado.
- **Evite se:** é uma página única; ou se o plano é wildcard "para garantir", sem cliente por subdomínio nem preview dinâmico.
