# Teste de carga com k6

> Descubra quantas requisições o sistema aguenta antes de os usuários descobrirem, com um cenário realista, uma meta em número e a leitura certa do resultado.

| | |
|---|---|
| **Referência** | Grafana k6 docs (grafana.com/docs/k6/latest): Thresholds, Scenarios e executors, Install k6, End-of-test summary; releases em github.com/grafana/k6 |
| **Categoria** | Desempenho |
| **Tipo** | Prática de teste de carga |
| **Vale para** | Qualquer API ou site HTTP; o roteiro é em JavaScript e roda em qualquer stack |
| **Verificado em** | 2026-11-25 |

## O que é

O **k6** é uma ferramenta de código aberto da Grafana Labs para teste de carga. Você escreve o roteiro em JavaScript, define quantos usuários virtuais (VUs) ou quantas requisições por segundo e o k6 dispara contra o sistema e mede. Versão atual conferida em 2026-11-25: v2.4.0 (lançada em 2026-11-12).

Termos usados abaixo:

- **VU (usuário virtual):** uma "pessoa" repetindo o roteiro em laço.
- **Iteração:** uma execução do roteiro.
- **Cenário (scenario):** a forma de gerar carga; cada um usa um **executor**.
- **Threshold:** limite que, se violado, faz o k6 terminar com código de saída diferente de zero e quebrar o CI.
- **Check:** verificação por resposta (status, conteúdo). Não afeta o código de saída, a menos que você crie um threshold sobre a métrica `checks`.

## Por que usar

- **Acha o limite antes do pico:** quantas requisições por segundo até o p95 estourar a meta.
- **Prova o efeito de uma otimização** com o mesmo roteiro antes e depois.
- **Vira regra do CI:** um teste curto contra o ambiente de staging barra regressão ([quality gates](../../quality/docs/07-quality-gates-no-ci.md)).

## Quando usar

- Antes de lançar e antes de uma campanha ou data de pico.
- Depois de uma mudança grande em banco, cache ou infraestrutura.
- Para escolher o tamanho do servidor ou do pool ([doc 02](02-banco-explain-n-mais-1-e-pool.md) e [doc 07](07-escalar-vertical-horizontal-e-replica.md)).
- Em rotina: teste curto de fumaça (30 segundos, poucos VUs) a cada deploy em staging.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Atrás de CDN o gargalo é a origem; teste só as rotas sem cache |
| MVP de SaaS | ✅ Ótimo | Um roteiro de login e listagem já mostra o limite do servidor |
| SaaS em crescimento | ✅ Ótimo | Cenários por perfil de uso e limites automáticos no CI |
| Sistema interno/corporativo | 🟡 Serve | Poucos usuários; vale para relatórios e importações pesadas |
| API/integração | ✅ Ótimo | Clientes que disparam rajadas; use taxa de chegada fixa |
| App mobile com backend | ✅ Ótimo | Pico de abertura do app ou de notificação empurrada |
| Produção com dados reais e sem aviso | ❌ Evite | Carga em produção derruba o sistema de verdade; use staging |

## Quando é bom

- **Código em JavaScript**, versionado no repositório junto do projeto.
- **Thresholds** transformam a meta do [doc 01](01-medir-primeiro.md) em passa/falha.
- **Executor de taxa de chegada** (`arrival-rate`) mantém a carga constante mesmo se o sistema ficar lento, como no mundo real. Com executores de VUs, um sistema lento recebe menos requisições e o teste "melhora" sozinho.
- **Saída para Grafana e Prometheus** se quiser acompanhar o teste ao vivo.

## Quando é ruim

- **Ambiente diferente da produção:** banco vazio e máquina folgada dão número bonito e inútil. Use dados em volume parecido.
- **Gerador de carga limitado:** um notebook em Wi-Fi não gera milhares de requisições por segundo; o gargalo pode ser o seu lado. Rode de uma máquina ou VPS em rede boa.
- **Roteiro irreal:** bater sempre na mesma URL com o mesmo usuário acerta o cache e esconde o problema. Varie IDs e usuários.
- **`sleep` no fim da iteração com `arrival-rate`:** a doc diz para não usar; o ritmo vem da taxa.
- **Testar terceiros:** não dispare carga contra gateway de pagamento ou e-mail; use um servidor simulado.

## Como começar

Instalar (comandos da doc oficial, conferidos em 2026-11-25):

```bash
brew install k6
```

```bash
curl -fsSL https://dl.k6.io/key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/k6-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

Ou pela imagem Docker `grafana/k6`:

```bash
docker run --rm -i grafana/k6 run - < carga.js
```

Roteiro: login uma vez no `setup`, depois 50 requisições por segundo por 5 minutos na listagem, com a meta do [doc 01](01-medir-primeiro.md) em thresholds. Critério: p95 abaixo de 300 ms e menos de 1% de erro.

```js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    listagem: {
      executor: 'constant-arrival-rate',
      rate: 50,
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<300'],
    checks: ['rate>0.99'],
  },
};

const BASE = __ENV.BASE_URL;

export function setup() {
  const res = http.post(`${BASE}/login`, JSON.stringify({ email: __ENV.USER_EMAIL, password: __ENV.USER_PASSWORD }), {
    headers: { 'Content-Type': 'application/json' },
  });
  return { token: res.json('token') };
}

export default function (data) {
  const res = http.get(`${BASE}/agendamentos?limit=20`, {
    headers: { Authorization: `Bearer ${data.token}` },
  });
  check(res, {
    'status 200': (r) => r.status === 200,
    'lista presente': (r) => Array.isArray(r.json('items')),
  });
}
```

Rodar contra o staging, com credenciais por variável de ambiente (nunca no roteiro):

```bash
k6 run -e BASE_URL=https://staging.clinica-exemplo.com.br -e USER_EMAIL=carga@clinica-exemplo.com.br -e USER_PASSWORD="$K6_PASSWORD" carga.js
```

Para descobrir o limite, troque o cenário por uma rampa de taxa de chegada. O `ramping-arrival-rate` sobe a taxa linearmente entre os alvos; `preAllocatedVUs` é obrigatório e `maxVUs` limita o máximo:

```js
export const options = {
  scenarios: {
    rampa: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      preAllocatedVUs: 50,
      maxVUs: 300,
      stages: [
        { target: 50, duration: '2m' },
        { target: 100, duration: '2m' },
        { target: 200, duration: '2m' },
        { target: 0, duration: '1m' },
      ],
    },
  },
  thresholds: {
    http_req_duration: [{ threshold: 'p(95)<500', abortOnFail: true, delayAbortEval: '30s' }],
  },
};
```

`abortOnFail` interrompe o teste ao violar o limite e `delayAbortEval` espera o tempo informado antes de avaliar, para um pico inicial não abortar o teste cedo.

### Ler o resultado

Métricas do resumo final (doc oficial, 2026-11-25), com o que fazer em cada caso:

| Métrica | O que mostra | Como ler |
|---|---|---|
| `http_req_duration` | Tempo da requisição (avg, med, p90, p95, max) | Compare o p95 com a meta; a média engana |
| `http_req_failed` | Taxa de requisições com erro | Acima da meta: veja o status e o log do servidor |
| `http_reqs` | Total e taxa por segundo | É a vazão real alcançada |
| `iterations` | Iterações completas | Compare com a taxa pedida |
| `dropped_iterations` | Iterações que o k6 não conseguiu iniciar por falta de VUs | Aumente `maxVUs` ou o gerador é o gargalo |
| `vus` e `vus_max` | Usuários virtuais ativos e alocados | Perto de `maxVUs` sugere sistema lento |
| `checks` | Verificações que passaram | Falhas aqui são respostas erradas, não lentas |

Padrões comuns: o p95 sobe de forma reta com a carga (a CPU do app é o limite); sobe de repente num ponto (fila em pool de conexões ou lock no banco); `http_req_failed` sobe com timeouts (saturou). Em cada caso, observe junto o servidor (CPU, RAM, conexões do banco) e o APM ([doc 01](01-medir-primeiro.md)). Use `--summary-mode=full` para ver tudo no resumo.

No CI, o k6 encerra com código diferente de zero se qualquer threshold falhar, e isso basta para quebrar o job do GitHub Actions ([infra, doc 07](../../infra/docs/07-github-actions.md)).

## Combina com / alternativas

- [Medir primeiro](01-medir-primeiro.md) para as metas e [banco](02-banco-explain-n-mais-1-e-pool.md) para corrigir o que o teste achar.
- [Quality gates no CI](../../quality/docs/07-quality-gates-no-ci.md) e [testes de API](../../quality/docs/04-testes-de-api-e-contrato.md) (testar o contrato é outra coisa).
- Alternativas: Locust (Python), Gatling (Scala/Java), Artillery (Node), autocannon (rápido, só HTTP); wrk e hey para um teste de 1 minuto.

## Decisão rápida

- **Use k6** com `arrival-rate` e thresholds ligados às metas, contra staging com dados em volume real.
- **Rode** teste curto a cada deploy e teste de limite antes de picos.
- **Evite:** teste contra produção, contra terceiros ou com roteiro que bate sempre na mesma URL.
