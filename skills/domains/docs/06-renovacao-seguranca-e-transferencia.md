# Renovação, segurança e transferência do domínio

> Domínio no nome do cliente, com auto-renovação, 2FA, lock e alerta de expiração, não cai por esquecimento nem por golpe.

| | |
|---|---|
| **Referência** | registro.br (ajuda e tecnologia/DNSSEC), ICANN (Expired Registration Recovery Policy), documentação do registrar usado |
| **Categoria** | Domínios |
| **Tipo** | Prática de operação e segurança de domínio |
| **Vale para** | Todo projeto com domínio próprio, em especial na entrega ao cliente |
| **Verificado em** | 2026-11-25 |

## O que é

É a rotina que mantém o domínio vivo e seguro: renovar a tempo, proteger a conta onde ele está registrado, impedir transferência indevida e passar a titularidade ao cliente quando o projeto é entregue.

Termos: **registrar** é a empresa onde você registra e paga o domínio. **Titular** é quem consta como dono. **Lock de transferência** é um bloqueio que impede mover o domínio para outro registrar sem sua autorização. **DNSSEC** assina as respostas de DNS para que ninguém as falsifique no caminho.

## Por que usar

- **Domínio vencido tira site, API e e-mail do ar** de uma vez.
- **Conta do registrar invadida** permite apontar o domínio para outro servidor.
- **Domínio no nome do freelancer** prende o cliente a quem entregou o projeto.
- **Custo baixo:** quase tudo é configuração única.

## Quando usar

- Ao registrar o domínio e ao entregar o sistema.
- A cada troca de pessoa na equipe ou de e-mail de contato.
- Uma vez por trimestre, revisando a lista de domínios.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | O domínio é o negócio; vencer é perder o tráfego |
| MVP de SaaS | ✅ Ótimo | Auto-renovação e 2FA custam minutos |
| SaaS em crescimento | ✅ Ótimo | Lock, DNSSEC e alertas viram padrão |
| Sistema interno/corporativo | ✅ Ótimo | Titular deve ser a empresa, com e-mail de grupo |
| API/integração | ✅ Ótimo | Clientes têm o domínio da API gravado |
| App mobile com backend | ✅ Ótimo | App publicado não troca de domínio facilmente |
| Domínio no CPF do desenvolvedor, sem contrato | ❌ Evite | Risco jurídico e de bloqueio para o cliente |

## Quando é bom

- **Auto-renovação ligada** evita o esquecimento.
- **2FA** barra o roubo de senha.
- **Alerta de expiração** funciona como segunda rede de segurança.
- **Titularidade clara** simplifica sucessão e venda da empresa.

## Quando é ruim

- **Auto-renovação com cartão vencido** falha igual a não ter. Atualize o cartão.
- **E-mail de contato antigo** faz os avisos irem para ninguém.
- **DNSSEC mal desativado** na troca de DNS deixa o domínio sem resolver em resolvedores que validam.
- **Lock esquecido** atrasa uma transferência legítima; lembre de liberar na hora certa.

## Prazos do Registro.br

Conferido em 2026-11-25 em registro.br (páginas "Pagamento de domínio", "Domínio congelado" e "Processo de liberação"):

- O aviso de cobrança vai por e-mail para os contatos do domínio no registro e **30 dias antes de cada expiração**. Não há boleto pelo correio: e-mail de contato desatualizado é a causa mais comum de domínio perdido.
- Sem pagamento, o domínio é **congelado** (sai do ar) e, depois de um período, entra no **processo de liberação** para novo registro. Os processos são mensais (próximos: 09/12/2026 e 13/01/2027) e, se houver mais de um interessado, o domínio pode ir a leilão (processo competitivo, ofertas a partir de R$ 50,00).
- Domínio congelado pode ser publicado de novo por pouco tempo com a **extensão de pagamento**, que só pode ser usada uma vez, em emergência.
- Quem fica devendo a primeira manutenção de um domínio não consegue registrar outros.
- A duração exata de cada fase não aparece nessas páginas; fontes de terceiros (Locaweb, HomeHost) falam em cerca de 14 dias até o congelamento e até 90 dias congelado. Confirme no registro.br antes de prometer prazo.
- Valores de renovação: os mesmos do registro (R$ 40,00 por ano, R$ 364,00 por 10 anos). Renovar por vários anos reduz o risco de esquecer.

Em registrars de `.com` e `.app` o ciclo é outro (renovação, resgate, exclusão) e muda por empresa. Leia a política do seu registrar.

## Como começar

Checklist para o domínio de produção:

- [ ] Titular é o cliente ou a empresa (CPF/CNPJ dele), não o desenvolvedor.
- [ ] E-mail de contato é um endereço de grupo (por exemplo ti@clinica-exemplo.com.br em outro domínio de reserva), não pessoal.
- [ ] Auto-renovação ligada e forma de pagamento válida.
- [ ] 2FA ativo na conta do registrar, de preferência com app autenticador ou chave de segurança.
- [ ] Lock de transferência ativo no registrar (confira como funciona para `.br` no painel do Registro.br).
- [ ] Alerta de expiração em 60, 30 e 7 dias, em calendário ou monitor.
- [ ] DNSSEC avaliado e, se ativado, documentado.
- [ ] Documento "onde está cada coisa" (registrar, DNS, e-mail, quem tem acesso).

Para checar o vencimento por linha de comando:

```
whois clinica-exemplo.com.br | grep -i -E "expire|expires|status"
```

Alerta simples com cron, avisando quando faltar menos de 30 dias:

```
0 9 * * 1 /usr/local/bin/checa-dominio.sh clinica-exemplo.com.br 30
```

DNSSEC no `.br`: o Registro.br tem página de ajuda dedicada (registro.br/tecnologia/dnssec). O fluxo geral é gerar a chave no provedor de DNS e cadastrar o registro **DS** no painel do Registro.br. Se o DNS estiver na Cloudflare, ela mostra o DS pronto para copiar. O passo a passo exato do painel não pôde ser conferido; siga a ajuda oficial. Vale a pena em domínio de alto valor (financeiro, saúde); para um MVP, é opcional.

Transferir a titularidade ao cliente (`.com.br`): no painel do Registro.br, em Ajuda, há o processo administrativo de transferência de titularidade. Fontes de terceiros relatam que o processo exige formulário, documentos do novo titular e, em alguns casos, carta com firma reconhecida. Confirme os requisitos atuais no site antes de prometer prazo ao cliente.

Transferir para `.com` ou outro registrar: libere o lock, peça o código de autorização no registrar atual, inicie a transferência no novo e aprove. Desative o DNSSEC antes e reative depois, para não quebrar a resolução.

Na entrega ao cliente, registre num documento: titular, registrar, onde está o DNS, quem paga, data de vencimento e quem recebe os avisos.

## Combina com / alternativas

- [Escolher e registrar o domínio](01-escolher-e-registrar-o-dominio.md): defina o titular certo desde o início.
- [Certificados e HTTPS](05-certificados-e-https.md): domínio vencido derruba o certificado.
- [Migrar DNS sem queda](07-migrar-dns-sem-queda.md): cuidado com DNSSEC e lock na mudança.
- Alternativa: gerenciador de senhas com 2FA compartilhado da empresa.

## Decisão rápida

- **Use se:** o domínio sustenta um sistema em produção ou será entregue a um cliente.
- **Evite se:** o domínio é só um teste descartável; ainda assim, não o registre no seu nome se for do cliente.
