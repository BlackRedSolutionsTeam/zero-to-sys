# Observabilidade (OpenTelemetry, Grafana e Sentry)

> Enxergar o que o sistema está fazendo em produção: erros, métricas, logs e rastros, para descobrir problemas antes do cliente.

| | |
|---|---|
| **Site** | https://opentelemetry.io, https://grafana.com, https://sentry.io |
| **Categoria** | Monitoramento |
| **Tipo** | Padrão de instrumentação (OpenTelemetry) e plataformas de análise (Grafana, Sentry) |
| **Stack** | OpenTelemetry tem SDKs para várias linguagens; Grafana e Sentry recebem dados de quase qualquer stack |
| **Preço** | Grafana Cloud: grátis (10 mil séries de métricas, 50 GB de logs, traços e perfis por mês, retenção de 14 dias), Pro a partir de US$ 19/mês mais uso. Sentry: Developer grátis (1 usuário, 5 mil erros), Team US$ 29/mês, Business US$ 89/mês |
| **Licença** | OpenTelemetry: Apache 2.0, projeto da CNCF. Grafana: AGPLv3. Sentry: FSL-1.1-Apache-2.0 (uso concorrente proibido; cada release vira Apache 2.0 após 2 anos). Os dois também são serviços pagos (arquivos LICENSE no GitHub, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

**OpenTelemetry** é um conjunto de ferramentas e padrões para gerar e exportar três sinais: traços, métricas e logs. Ele não guarda nem mostra os dados; isso fica para um destino (backend). A vantagem é trocar de destino sem reescrever a instrumentação.

**Grafana Cloud** guarda e mostra métricas, logs e traços em painéis e alertas. **Sentry** é focado em erros e desempenho do aplicativo: agrupa exceções, mostra a pilha e avisa quando algo novo quebra.

## Por que usar

- **Descobrir antes do cliente:** erro e lentidão geram alerta.
- **Diagnóstico mais rápido:** traços mostram onde uma requisição demorou.
- **Sem amarração:** OpenTelemetry permite trocar de ferramenta.
- **Começo grátis:** os dois planos grátis cobrem projetos pequenos.
- **Base para metas de confiabilidade** (tempo de resposta, taxa de erro).

## Quando usar

- Sentry: já no MVP, assim que houver usuário real.
- OpenTelemetry e Grafana: quando houver mais de um serviço ou necessidade de ver latência e carga.
- Alertas de disponibilidade e de custo em qualquer porte.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | 🟡 Serve | Um monitor de disponibilidade basta |
| MVP / protótipo | ✅ Ótimo | Sentry grátis resolve; mais que isso é exagero |
| SaaS pequeno | ✅ Ótimo | Sentry mais métricas básicas do provedor |
| SaaS em crescimento | ✅ Ótimo | OpenTelemetry com Grafana para traços e métricas |
| Sistema corporativo | ✅ Ótimo | Observabilidade completa e retenção maior |
| Sistema com vários serviços | ✅ Ótimo | Traço distribuído mostra a cadeia inteira |
| Time sem tempo para alertas | 🟡 Serve | Painel sem alerta ninguém olha; comece com poucos e úteis |
| Dados pessoais nos logs | ❌ Evite | Mascare dados antes de enviar para terceiros |

## Quando é bom

- **Padrão aberto:** OpenTelemetry é neutro quanto a fornecedor.
- **Grafana:** painel, alerta e logs no mesmo lugar, com plano grátis permanente.
- **Sentry:** agrupa erros iguais e liga o erro à versão publicada.
- **Escala com o projeto:** começa grátis e cresce por uso.

## Quando é ruim

- **Custo por volume:** logs, métricas e traços cobram por quantidade; defina amostragem e retenção. Os preços de uso do Sentry e do Grafana aparecem por unidade; cheque a calculadora.
- **Dados sensíveis vazam para o terceiro:** senhas, tokens e dados pessoais não devem entrar em logs nem em eventos.
- **Alerta demais vira ruído** e passa a ser ignorado.
- **Instrumentar tudo desde o dia um** consome tempo; comece por erros e requisições principais.
- **Retenção curta no grátis:** 14 dias no Grafana e 30 dias de histórico no Sentry Developer.
- **Autohospedar custa operação:** guardar traços e logs próprios exige armazenamento e cuidado; avalie antes de recusar o plano gerenciado.

## Como começar

Sentry: crie o projeto, copie o DSN para as variáveis de ambiente ([segredos](09-segredos-e-configuracao.md)) e instale o SDK da sua linguagem pelo guia do painel.

OpenTelemetry (exemplo em Node; confira os pacotes na documentação):

```bash
npm i @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node
```

Aponte o exporter para o endpoint OTLP do Grafana Cloud usando as variáveis padrão `OTEL_EXPORTER_OTLP_ENDPOINT` e `OTEL_EXPORTER_OTLP_HEADERS`. Crie alertas para taxa de erro, latência e indisponibilidade.

## Combina com / alternativas

- [GitHub Actions](07-github-actions.md): marque a versão (release) no Sentry a cada deploy.
- [Cloudflare](08-cloudflare.md) e [PaaS](01-paas.md): métricas e logs da borda e da plataforma.
- [Backup e recuperação](11-backup-e-recuperacao.md): alerta de backup que falhou.
- Alternativas: Datadog e New Relic (completos; Datadog: plano grátis com até 5 hosts básicos e 1 dia de retenção, Infrastructure Pro a partir de US$ 15 por host/mês no anual; New Relic: 100 GB de ingestão grátis por mês e 1 usuário completo, depois US$ 0,40 por GB; datadoghq.com/pricing e newrelic.com/pricing, conferido em 2026-11-24), Prometheus e Loki autohospedados, GlitchTip como alternativa a Sentry.

## Decisão rápida

- **Use se:** o sistema tem usuário real. Comece com Sentry e alertas simples, e adicione OpenTelemetry com Grafana quando houver mais de um serviço.
- **Evite se:** a ideia é guardar todo log e traço sem limite, ou enviar dados pessoais a um terceiro sem mascarar.
