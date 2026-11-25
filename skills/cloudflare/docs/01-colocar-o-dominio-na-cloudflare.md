# Colocar o domínio na Cloudflare

> Adicione o domínio na Cloudflare, confira os registros que ela importou, troque os servidores de nome no Registro.br (com o DNSSEC desligado antes) e só então ligue o proxy.

| | |
|---|---|
| **Referência** | developers.cloudflare.com (Add a site, DNS full setup, Import and export records); registro.br |
| **Categoria** | Borda |
| **Tipo** | Prática de configuração de DNS e borda |
| **Vale para** | Qualquer domínio público, de .com.br a .com; exemplo com clinica-exemplo.com.br |
| **Verificado em** | 2026-11-25 |

## O que é

Colocar o domínio na Cloudflare é delegar a ela o DNS (o sistema que traduz nome em endereço IP). Você cria uma conta, adiciona o domínio e troca os **nameservers** (servidores de nome: os dois endereços que dizem à internet quem responde pelo DNS do domínio) no lugar onde o domínio foi registrado.

Esse modo se chama "full setup" (configuração completa): a Cloudflare passa a ser a fonte do DNS inteiro. O registro do domínio continua no Registro.br.

Exemplo do doc: sistema de agendamento de clínica com `clinica-exemplo.com.br`, app em `app.`, API em `api.` e staging em `staging.`.

## Por que usar

- **Porta de entrada:** sem trocar os nameservers, nada de proxy, cache, WAF ou SSL da Cloudflare funciona.
- **DNS com painel e API:** o IaC controla os registros (veja [DNS e proxy](02-dns-e-proxy.md)).
- **Reversível:** voltar os nameservers antigos desfaz a mudança.
- **Um só lugar:** DNS, SSL e regras da borda ficam no mesmo painel.

## Quando usar

- Domínio público de qualquer projeto que vai usar a borda.
- Antes de pôr o sistema no ar, quando ainda não há tráfego a perder.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | CDN e SSL entram na hora |
| MVP de SaaS | ✅ Ótimo | DNS, TLS e proteção sem custo |
| SaaS em crescimento | ✅ Ótimo | Regras, cache e limites por rota |
| Sistema interno/corporativo | 🟡 Serve | Vale se o painel tem domínio público; senão veja Tunnel e Access |
| API/integração | ✅ Ótimo | DNS e proteção na frente da API |
| App mobile com backend | ✅ Ótimo | A API pública ganha WAF e rate limit |
| Domínio que a empresa exige manter em DNS próprio | ❌ Evite | Delegar o DNS inteiro contraria a regra; avalie o modo parcial (CNAME) com a Cloudflare |

## Quando é bom

- **Troca sem queda** se os registros forem conferidos antes de mudar os nameservers.
- **Registros de e-mail** (MX, SPF, DKIM, DMARC) importados e revisados no mesmo passo.

## Quando é ruim

- **Registro esquecido:** o scan automático pode não achar tudo. A documentação manda revisar apex, subdomínios como `www` e registros de e-mail. Faltando registro, o visitante vê `DNS_PROBE_FINISHED_NXDOMAIN`.
- **DNSSEC ligado:** trocar nameservers com ele ativo pode deixar o domínio fora do ar (aviso da documentação).
- **Troca em horário de pico:** a propagação pode levar até 24 horas, segundo a documentação.

## Como começar

**Pelo painel**

1. Crie a conta em dash.cloudflare.com e ative a verificação em duas etapas.
2. Em Domains, escolha Onboard a domain, informe `clinica-exemplo.com.br` e escolha como trazer os registros (scan automático ou arquivo).
3. Escolha o plano (o Free serve para começar).
4. Revise os registros: apex, `www`, `app`, `api`, `staging` e todos os de e-mail. Em A, AAAA e CNAME, escolha Proxied (nuvem laranja) ou DNS only (cinza).
5. Anote os dois nameservers que a Cloudflare atribuiu ao domínio.
6. No Registro.br, desligue o DNSSEC do domínio, se estiver ligado.
7. No painel do Registro.br, abra o domínio, altere os servidores DNS, remova os atuais e coloque os dois da Cloudflare, escrevendo os nomes exatamente como aparecem.
8. Volte à Cloudflare: o domínio fica em Pending Nameserver Update até a troca valer. Ao ficar Active, chega um e-mail.
9. Reative o DNSSEC pela Cloudflare e copie os dados que ela mostra para o Registro.br.

Os cliques exatos do painel do Registro.br não foram conferidos (a página da ferramenta não carregou na verificação). Siga a página oficial registro.br/tecnologia/ferramentas/dns-ou-ns/.

**Importar registros de um arquivo BIND**

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/import" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -F "file=@clinica-exemplo.com.br.zone" \
  -F "proxied=false"
```

Limites da documentação: arquivo de até 256 KiB, e a API de importação aceita 3 requisições por minuto por usuário. O token precisa da permissão DNS Write. Nomes de CNAME, MX, NS, PTR e SRV terminam com ponto (`api.clinica-exemplo.com.br.`).

Para decidir o proxy por registro, marque no arquivo `cf-proxied:true` ou `cf-proxied:false`; a tag vale mais que o campo `proxied` da chamada.

**Conferir a delegação**

```bash
dig NS clinica-exemplo.com.br +short
```

Quando a resposta listar só os nameservers da Cloudflare, a troca valeu.

**O que o plano Free inclui**

Conferido nas páginas oficiais em 2026-11-25: DNS, CDN, Universal SSL e proteção DDoS sem medição de tráfego. Upload de até 100 MB por requisição (developers.cloudflare.com/cache). Regras de WAF, número de regras e demais limites mudam por plano; a página de planos não listou a coluna Free de rede e CDN na verificação. Consulte cloudflare.com/plans e [WAF, rate limit e bots](05-waf-rate-limit-e-bots.md) antes de contar com um recurso.

Serviços de computação do Free (conferido em cloudflare.com/plans, 2026-11-25): Workers com 100 mil requisições por dia, R2 com 10 GB-mês, KV com 1 GB, D1 com 5 GB.

## Combina com / alternativas

- [DNS e proxy](02-dns-e-proxy.md): próximo passo, decidir laranja ou cinza.
- [SSL/TLS e HSTS](03-ssl-tls-e-hsts.md): configure antes de ligar o proxy na origem.
- [Cloudflare na infra](../../infra/docs/08-cloudflare.md) e [VPS com Coolify ou Dokploy](../../infra/docs/02-vps-coolify-dokploy.md).
- Registro e migração de DNS: [escolher e registrar o domínio](../../domains/docs/01-escolher-e-registrar-o-dominio.md) e [migrar DNS sem queda](../../domains/docs/07-migrar-dns-sem-queda.md).
- Alternativa: manter o DNS no Registro.br e usar só a hospedagem; perde proxy, cache e WAF.

## Decisão rápida

- **Use se:** o domínio é público e você quer DNS, cache, WAF e DDoS sem custo inicial.
- **Evite se:** você não pode delegar o DNS inteiro a um terceiro ou não tem acesso para desligar o DNSSEC e trocar os nameservers.
