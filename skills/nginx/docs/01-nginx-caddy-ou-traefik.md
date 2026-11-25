# nginx, Caddy ou Traefik

> Escolha o proxy pelo seu cenário: nginx quando você quer controle e já o conhece, Caddy quando quer HTTPS pronto com pouca config, Traefik quando o Docker manda na infraestrutura.

| | |
|---|---|
| **Referência** | nginx.org/en/docs, caddyserver.com/docs, doc.traefik.io, coolify.io/docs, docs.dokploy.com, developers.cloudflare.com/cloudflare-one |
| **Categoria** | Servidor |
| **Tipo** | Prática de escolha de proxy reverso |
| **Vale para** | VPS própria, servidor com vários sites, aplicações em Docker ou no host |
| **Verificado em** | 2026-11-25 |

## O que é

Proxy reverso é o programa que recebe o tráfego da internet (portas 80 e 443), cuida do HTTPS e repassa cada requisição para a aplicação, que fica escondida atrás dele. Quatro caminhos comuns:

- **nginx:** servidor web e proxy muito usado, configurado em arquivos de texto. Conferido em 2026-11-25: mainline 1.31.10 e stable 1.30.8 (nginx.org/en/download.html).
- **Caddy:** servidor com HTTPS automático. Segundo a documentação, obtém certificados de autoridades ACME (como Let's Encrypt), renova sozinho e redireciona HTTP para HTTPS.
- **Traefik:** proxy que descobre as rotas sozinho, lendo labels (etiquetas) de contêineres Docker.
- **Cloudflare Tunnel:** o programa `cloudflared` abre conexões só de saída até a Cloudflare, então o servidor não precisa de porta aberta nem de IP público.

## Por que usar

- **Um ponto único** de entrada, HTTPS e logs.
- **Várias aplicações** no mesmo servidor, cada uma num domínio.
- **Aplicação simples:** ela só escuta em `127.0.0.1` e não lida com certificado.

## Quando usar

- Ao subir uma VPS sem painel e precisar de um proxy.
- Ao decidir entre trocar o proxy ou manter o que a plataforma já traz.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | nginx serve estáticos e cache muito bem; Caddy também |
| MVP de SaaS | 🟡 Serve | Caddy ou o proxy do painel (Coolify/Dokploy) dão menos trabalho |
| SaaS em crescimento | ✅ Ótimo | nginx com upstream, limites e logs afinados |
| Sistema interno/corporativo | ✅ Ótimo | nginx é comum em times de infraestrutura e tem muita documentação |
| API/integração | ✅ Ótimo | Proxy, rate limit e timeouts bem controlados |
| App mobile com backend | 🟡 Serve | Só a API precisa de proxy; o mais simples basta |
| Servidor com Coolify ou Dokploy | ❌ Evite | O painel já traz o Traefik; um nginx na frente briga pelas portas 80 e 443 |

## Quando é bom

- **nginx:** muito material, desempenho alto em estáticos, controle fino de cache, limites e logs. Boa escolha se o time já o conhece.
- **Caddy:** config de poucas linhas e certificado sem Certbot. Pede portas 80 e 443 abertas e pasta de dados persistente (documentação do HTTPS automático).
- **Traefik:** sobe um contêiner novo e a rota aparece, sem editar arquivo.
- **Tunnel:** esconde o IP da origem; o firewall pode bloquear toda a entrada.

## Quando é ruim

- **nginx não emite certificado sozinho:** precisa de Certbot ou `acme.sh` (doc 04).
- **Caddy:** menos material de exemplo em português e menos módulos prontos que o nginx no ecossistema de tutoriais.
- **Traefik:** a configuração por labels espalha o roteamento pelos arquivos Compose; difícil de ler com poucos serviços.
- **Tunnel:** a Cloudflare vira dependência do acesso; não resolve cache, limites finos nem logs do seu lado.

## Quando o nginx NÃO é a melhor escolha

- **Servidor com Coolify ou Dokploy:** o painel já cuida do proxy e dos certificados.
- **Uma ou duas apps e pouca experiência:** o Caddy tira de cena Certbot, renovação e arquivos de certificado.
- **Dezenas de contêineres que sobem e descem:** o Traefik acompanha o Docker sem `reload` manual.
- **Sem abrir porta alguma:** o Cloudflare Tunnel dispensa até o proxy no host (a aplicação fala com `cloudflared`).
- **Time sem ninguém que queira manter a config:** menos config é menos erro.

## Erros comuns de escolha

- Instalar nginx em servidor que já tem Traefik e brigar pelas portas 80 e 443.
- Trocar o proxy do Coolify por Caddy sem saber que as rotas padrão são substituídas.
- Achar que o Tunnel substitui o resto: ele leva o tráfego até o servidor, mas as regras de aplicação continuam suas.
- Escolher por moda em vez de pelo que o time sabe operar às 3 da manhã.

## Comparação lado a lado

| Critério | nginx | Caddy | Traefik | Tunnel |
|---|---|---|---|---|
| HTTPS automático | Não, usa Certbot ou `acme.sh` | Sim | Sim, via resolvedor ACME | Sim, na Cloudflare |
| Configuração | Arquivos, mais longos | Arquivo curto | Labels ou arquivos | Painel ou arquivo do túnel |
| Descoberta de contêineres | Não | Não por padrão | Sim | Não |
| Cache e limites finos | Muito bons | Básicos | Por middlewares | Na Cloudflare |
| Precisa de porta aberta | Sim | Sim | Sim | Não |

A linha de HTTPS do Caddy vem da documentação oficial; as demais refletem o uso comum, confira na página de cada ferramenta antes de decidir.

## Como começar

O proxy do painel já existe: o Coolify usa o Traefik como padrão e aceita Caddy como alternativa, mas trocar apaga o roteamento padrão e exige recriar as regras na sintaxe do Caddy (coolify.io/docs). O Dokploy usa o Traefik e emite Let's Encrypt ao ativar HTTPS no domínio (docs.dokploy.com). Conferido em 2026-11-25. Com painel, use o proxy dele.

Exemplo mínimo em Caddy, para comparar com o nginx do doc 03:

```
api.clinica-exemplo.com.br {
    reverse_proxy 127.0.0.1:3000
}
```

Escolha por perfil:

| Perfil | Recomendação |
|---|---|
| Dev sozinho, uma ou duas apps | Caddy, ou o proxy do painel |
| Time com Docker e muitos serviços | Traefik, ou o painel que já o traz |
| Servidor com vários sites, regras de cache e limite | nginx |
| Sem IP público ou sem querer abrir portas | Cloudflare Tunnel |

Ficou com nginx? Siga para o [doc 02](02-instalacao-e-estrutura.md).

## Combina com / alternativas

- [Coolify e Dokploy](../../infra/docs/02-vps-coolify-dokploy.md) quando você quer painel em vez de proxy manual.
- [Cloudflare](../../infra/docs/08-cloudflare.md) na frente de qualquer um dos três (spec e doc 05 desta skill).
- [Rate limit](../../security/docs/06-rate-limit.md) para os limites que o nginx aplica.

## Decisão rápida

- **Use nginx se:** o time já conhece, há vários sites no mesmo servidor, você quer cache e limites finos, ou precisa servir estáticos pesados.
- **Evite nginx se:** o servidor já tem Coolify/Dokploy, você quer HTTPS sem Certbot e config mínima (Caddy), ou todo o roteamento nasce de contêineres (Traefik).
