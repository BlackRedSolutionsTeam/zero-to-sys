# As 5 melhores VPS do Brasil

> Escolha a VPS pelo datacenter no Brasil, pelo preço em reais e pelo que a página oficial realmente promete; todos os números abaixo foram conferidos em 2026-11-25.

| | |
|---|---|
| **Referência** | Páginas oficiais de VPS de Hostinger, HostGator Brasil, Locaweb, KingHost e HostDime Brasil (links em cada seção) |
| **Categoria** | Servidor |
| **Tipo** | Prática de escolha de provedor |
| **Vale para** | Quem precisa de um servidor próprio com latência baixa para usuários no Brasil |
| **Verificado em** | 2026-11-25 |

## O que é

VPS (servidor virtual privado) é uma fatia de um servidor físico só sua, com CPU e RAM reservadas e acesso root (administrador). Você instala o que quiser, mas cuida de segurança, atualização e backup. Este doc compara 5 provedores com planos em reais.

Exemplo: sistema de agendamento de clínica em clinica-exemplo.com.br. "Não informado na página" = a página oficial não trouxe o dado em 2026-11-25.

## Por que usar

- **Latência:** datacenter no Brasil deixa a resposta mais rápida para o paciente que abre o app.
- **Reais e nota fiscal:** sem câmbio e com documento para o contador.
- **Controle:** root permite Docker, Coolify e nginx.

## Quando usar

- Quando o usuário final está no Brasil e a latência importa.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Funciona, mas hospedagem compartilhada ou CDN costuma bastar |
| MVP de SaaS | ✅ Ótimo | Um plano de 4 GB com Docker roda app e banco por pouco |
| App mobile com backend | 🟡 Serve | Serve no começo; escala pede mais recursos |
| Sistema interno/corporativo | ✅ Ótimo | Nota fiscal e suporte nacional ajudam na compra |
| API/integração | ✅ Ótimo | Root e IP dedicado; confira o limite de tráfego |
| Alta disponibilidade com autoescala | ❌ Evite | VPS única é ponto único de falha |

## Dados conferidos por fornecedor

Plano de entrada = o menor plano listado na página no dia. "Promo" é preço de contrato longo; "renovação" é o que a página mostra depois do contrato.


### 1. Hostinger
Página: https://www.hostinger.com/br/servidor-vps

| Item | Conferido em 2026-11-25 |
|---|---|
| Plano de entrada | KVM 1: R$ 29,99/mês promo de 24 meses (total R$ 719,76); renovação R$ 59,99/mês; preço mensal sem contrato: não informado na página |
| vCPU / RAM / disco | 1 vCPU / 4 GB / 50 GB NVMe |
| Tráfego | 4 TB (rede de 1 Gbps) |
| Datacenter | Brasil listado entre as localizações; cidade: não informado na página |
| Gerenciada | Autogerenciada, com assistente de IA no terminal web |
| Root | Sim |
| Snapshot/backup | Backup semanal grátis; snapshot: só citado na FAQ, sem detalhes |
| Pagamento | Cartão em até 12x; PIX e boleto: não informado na página |
| Nota fiscal | não informado na página |
| SLA | não informado na página (sem percentual) |
| Suporte | 24h, com agente de IA e atendimento humano quando a IA não resolve |

### 2. HostGator Brasil
Página: https://www.hostgator.com.br/servidor-vps

| Item | Conferido em 2026-11-25 |
|---|---|
| Plano de entrada | VPS NVMe 2: R$ 20,99/mês promo de 3 anos (total R$ 755,64); preço mensal sem contrato: não informado na página |
| vCPU / RAM / disco | 1 vCPU / 2 GB DDR5 / 50 GB NVMe |
| Tráfego | Ilimitado |
| Datacenter | Brasil (a página cita o datacenter da OCI em São Paulo na nota de latência); também México, Chile, Colômbia e EUA |
| Gerenciada | não informado na página ("controle total") |
| Root | Sim |
| Snapshot/backup | Backup semanal automático grátis; snapshot: não informado na página |
| Pagamento | não informado na página (a cobrança aparece via Asaas, sem listar meios) |
| Nota fiscal | não informado na página |
| SLA | Sem SLA formal; cita "uptime de 99,9%" e "disponibilidade superior a 99,95%" na infraestrutura OCI |
| Suporte | 24h, todos os dias, em português, chat e ticket, com fila prioritária |

### 3. Locaweb
Página: https://www.locaweb.com.br/servidor-vps/

| Item | Conferido em 2026-11-25 |
|---|---|
| Plano de entrada | VPS 1 GB: R$ 15,90/mês promo de 24 meses; renovação R$ 23,92/mês; preço mensal sem contrato: não informado na página |
| vCPU / RAM / disco | 2 vCPU / 1 GB / 40 GB SSD |
| Tráfego | Ilimitado |
| Datacenter | "Infraestrutura no Brasil"; cidade: não informado na página |
| Gerenciada | não informado na página ("customização total") |
| Root | Sim (a página define VPS como máquina virtual com acesso root) |
| Snapshot/backup | 1 imagem instantânea (snapshot) grátis; backup automático: não informado na página |
| Pagamento | Cartão em até 12x sem juros nos planos anual e bienal (parcela mínima R$ 15); PIX e boleto: não informado na página |
| Nota fiscal | não informado na página |
| SLA | não informado na página para o VPS (o 99,9% citado é do Locaweb Cloud) |
| Suporte | Técnico 24h por telefone, 7 dias; chat; vendas e cobrança de segunda a sexta, 8h às 18h |

### 4. KingHost
Página: https://king.host/servidor-vps

| Item | Conferido em 2026-11-25 |
|---|---|
| Plano de entrada | VPS 4 GB: R$ 32,90/mês sem contrato; valores de plano anual e bienal: não informado na página |
| vCPU / RAM / disco | 2 vCPU / 4 GB / 70 GB SSD |
| Tráfego | Ilimitado |
| Datacenter | Infraestrutura brasileira; cidade: não informado na página |
| Gerenciada | não informado na página (cita acesso root e painel próprio) |
| Root | Sim |
| Snapshot/backup | não informado na página |
| Pagamento | Cartão, com 12x sem juros nos planos anual e bienal (parcela mínima R$ 15); PIX e boleto: não informado na página |
| Nota fiscal | não informado na página |
| SLA | 99,9% |
| Suporte | 24/7 em português, humano, por chat e WhatsApp |

### 5. HostDime Brasil
Páginas: https://www.hostdime.com.br/cloud-server/ e https://www.hostdime.com.br/servidor-dedicado/

| Item | Conferido em 2026-11-25 |
|---|---|
| Plano de entrada | não informado na página: configurador sem planos nomeados nem preço mensal; só crédito mínimo de R$ 75,00 |
| vCPU / RAM / disco | configuráveis; cloud em SSD corporativo; dedicados de 4 cores (Intel E3-1230v5) a 2x AMD EPYC 7K62 |
| Tráfego | Brasil: 10 TB de saída e 5 TB de entrada grátis; excedente R$ 0,04/GB de saída. A página também diz "ilimitado": confirme com a HostDime |
| Datacenter | São Paulo (SP) e João Pessoa (PB); também Orlando, México e Colômbia |
| Gerenciada | Opcional em 4 níveis (Padrão, Avançado, Full, Premium); base: não informado na página |
| Root | Sim no cloud ("Acesso Root completo"); no dedicado: não informado na página |
| Snapshot/backup | Backup opcional (agente Acronis); snapshot: não informado na página |
| Pagamento | Cartão, boleto e Bitcoin; PIX: não informado na página |
| Nota fiscal | não informado na página |
| SLA | 99,9% no cloud; no gerenciamento Padrão, resposta inicial em até 60 minutos para 90% dos chamados |
| Suporte | 24x7x365, telefone e painel |

## Comparação

| Provedor | Entrada (R$/mês) | Condição do preço | Config. de entrada | Datacenter no Brasil | PIX/boleto/cartão | SLA |
|---|---|---|---|---|---|---|
| Hostinger | 29,99 | contrato de 24 meses | 1 vCPU, 4 GB, 50 GB | sim, cidade não informada | só cartão informado | não informado |
| HostGator | 20,99 | contrato de 3 anos | 1 vCPU, 2 GB, 50 GB | sim, São Paulo (OCI) | não informado | sem SLA formal |
| Locaweb | 15,90 | contrato de 24 meses | 2 vCPU, 1 GB, 40 GB | sim, cidade não informada | só cartão informado | não informado |
| KingHost | 32,90 | mensal, sem contrato | 2 vCPU, 4 GB, 70 GB | sim, cidade não informada | só cartão informado | 99,9% |
| HostDime | não informado | crédito mínimo R$ 75,00 | configurável | sim, São Paulo e João Pessoa | cartão e boleto | 99,9% |

Compare planos de 4 GB: o preço promo só vale enquanto o contrato dura.

## Quando é bom e quando é ruim

Pontos fortes e fracos de cada provedor.

| Provedor | Pontos fortes | Pontos fracos |
|---|---|---|
| Hostinger | 4 GB e 4 TB no plano de entrada; backup semanal grátis; root | Renovação quase dobra; cidade, nota fiscal, PIX e SLA não informados |
| HostGator | Menor preço de 2 GB com NVMe e DDR5; tráfego ilimitado; datacenter OCI em São Paulo citado | Contrato de 3 anos; sem SLA formal; pagamento e nota não informados |
| Locaweb | Marca nacional antiga; suporte 24h por telefone; snapshot grátis | Entrada de 1 GB é pequena; renovação sobe; nota, PIX e SLA do VPS não informados |
| KingHost | Preço mensal sem contrato; SLA 99,9%; suporte humano por WhatsApp | Cidade, snapshot, PIX e nota não informados |
| HostDime | Datacenters em São Paulo e João Pessoa; dedicados grandes; boleto; SLA e resposta definidos | Sem preço na página; tráfego com cobrança de excedente; mais complexo |

## Recomendação por perfil

| Perfil | Opção | Por quê |
|---|---|---|
| MVP barato | HostGator ou Locaweb | Menores preços promo; confira a renovação antes de fechar |
| SaaS pequeno | Hostinger KVM 1 ou KingHost 4 GB | 4 GB roda app e Postgres juntos; KingHost não prende contrato |
| Agência com vários sites | KingHost ou Locaweb | Plano de 4 GB ou mais, suporte em português; confirme painel e nota |
| Cliente que exige nota e suporte nacional | Locaweb ou KingHost | Marcas nacionais; peça a nota por escrito, pois a página não informa |
| Servidor grande ou dedicado | HostDime | Dedicados configuráveis e datacenters em SP e João Pessoa |

## Estimativa mensal de uma configuração típica

App, API e Postgres no mesmo VPS de 4 GB, com Cloudflare gratuito na frente (confirme o plano em cloudflare.com).

| Item | Hostinger | Locaweb | KingHost |
|---|---|---|---|
| VPS 4 GB, ano 1 | R$ 29,99 (KVM 1) | R$ 32,90 | R$ 32,90 |
| Cloudflare Free | R$ 0 | R$ 0 | R$ 0 |
| Total ano 1 | R$ 29,99 | R$ 32,90 | R$ 32,90 |
| Depois da promo | R$ 59,99 | R$ 63,92 | não informado (preço mensal já é o de tabela) |

Sem domínio nem backup externo.

## Quando sair das brasileiras

| Opção | Conferido em 2026-11-25 | Quando vale |
|---|---|---|
| AWS Lightsail (região São Paulo) | Entrada nos EUA: US$ 5,00/mês, 2 vCPU, 0,5 GB, 20 GB, 1 TB; preço em São Paulo: não informado na página, que diz metade da franquia de transferência | Você já usa AWS ou precisa de serviços gerenciados |
| DigitalOcean | US$ 4,00/mês, 1 vCPU, 512 MiB, 10 GiB, 500 GiB; sem Brasil na lista de datacenters | Preço em dólar e API madura; latência maior |
| Hetzner | A partir de € 5,49/mês sem IVA; sem Brasil na lista (Alemanha, Finlândia, Singapura, EUA) | Mais recursos por real e aceitar latência maior |
| Oracle Cloud, Vultr | não conferido (página bloqueou a leitura) | Confira antes de decidir |

## Como começar

1. Abra a página oficial do plano e confirme no checkout o preço, a renovação e a região (cidade) do servidor.
2. Pergunte ao suporte, por escrito: nota fiscal, PIX/boleto e snapshot.
3. Dimensione ([02](02-dimensionar-o-servidor.md)), contrate Ubuntu LTS e siga o [primeiro acesso seguro](03-primeiro-acesso-seguro-ssh-e-firewall.md).

## Combina com / alternativas

- [VPS com Coolify e Dokploy](../../infra/docs/02-vps-coolify-dokploy.md) para publicar sem montar tudo à mão.
- [Backup e recuperação](../../infra/docs/11-backup-e-recuperacao.md): snapshot do provedor não substitui cópia externa.

## Decisão rápida

- **Use se:** o usuário está no Brasil e você quer root, reais e suporte em português.
- **Evite se:** precisa de autoescala ou alta disponibilidade sem montar mais de um servidor.
