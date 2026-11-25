# Cache: HTTP, aplicação e Redis

> Guarde a resposta pronta no lugar mais perto de quem pede, com prazo de validade claro e um plano para invalidar.

| | |
|---|---|
| **Referência** | MDN, Cache-Control (developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control); Redis docs: Key eviction (redis.io/docs/latest/develop/reference/eviction) e SET (redis.io/docs/latest/commands/set) |
| **Categoria** | Desempenho |
| **Tipo** | Prática de cache em camadas |
| **Vale para** | Qualquer back-end HTTP; exemplos com Redis |
| **Verificado em** | 2026-11-25 |

## O que é

Cache é uma cópia de um resultado caro guardada para a próxima vez. Há três camadas, da mais próxima do usuário para a mais próxima do banco:

1. **HTTP:** o navegador e a CDN guardam a resposta, controlados pelo cabeçalho `Cache-Control`.
2. **Aplicação:** memória do processo ou um serviço como o Redis guardam o resultado de uma consulta ou cálculo.
3. **Banco:** o cache de páginas do PostgreSQL já existe e não precisa de ação sua.

**Invalidar** é descartar ou atualizar a cópia quando o dado de origem muda. É a parte difícil: cache sem plano de invalidação serve dado velho.

## Por que usar

- **Latência:** servir de memória ou da CDN leva milissegundos.
- **Menos carga no banco:** a mesma consulta deixa de rodar mil vezes por minuto.
- **Custo:** um Redis pequeno costuma sair mais barato que um banco maior.

## Quando usar

- Dado lido muito mais do que escrito (catálogo, configurações, perfil público, lista de especialidades).
- Resultado caro de calcular (relatório, agregação, chamada a API externa com limite).
- Arquivos estáticos e respostas públicas: sempre.
- Depois de [medir e ajustar o banco](02-banco-explain-n-mais-1-e-pool.md); cache em cima de consulta ruim só esconde o problema.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Cache HTTP e CDN resolvem quase tudo |
| MVP de SaaS | 🟡 Serve | Cabeçalhos nos estáticos; Redis só quando houver dor medida |
| SaaS em crescimento | ✅ Ótimo | Cache de configuração e de leituras pesadas por empresa; Redis também serve a filas e limite de taxa |
| Sistema interno/corporativo | 🟡 Serve | Poucos usuários; cache de relatórios pesados |
| API/integração | ✅ Ótimo | `Cache-Control` e ETag em respostas públicas reduzem o tráfego |
| App mobile com backend | ✅ Ótimo | Menos dados trafegados em rede ruim |
| Dado que muda a cada segundo e precisa estar exato | ❌ Evite | Saldo, estoque final e status de pagamento leem da fonte |

## Quando é bom

- **HTTP com URL versionada** (`app.3f9a1c.js`) pode ser guardado por um ano sem risco.
- **`stale-while-revalidate`** serve o dado antigo enquanto atualiza em segundo plano.
- **Cache-aside** (a aplicação consulta o cache e, se faltar, busca no banco e grava) é simples e funciona com qualquer banco.
- **Redis** é rápido, tem TTL por chave e políticas de remoção quando a memória enche.

## Quando é ruim

- **Dado velho:** o usuário atualiza o cadastro e continua vendo o antigo.
- **Dado de uma pessoa servido a outra:** resposta personalizada com `public` pode ser guardada na CDN e entregue a outro usuário. Use `private` ou `no-store`.
- **Chave sem o escopo:** `appointments:list` sem o `company_id` mistura dados entre empresas (veja [multiempresa](../../data/docs/06-multiempresa.md)).
- **Debandada (cache stampede):** quando uma chave quente expira, centenas de requisições vão ao banco ao mesmo tempo.
- **Mais uma peça para operar:** Redis precisa de memória, monitoramento e plano para quando cair; a aplicação deve funcionar (mais lenta) sem ele.

## Como começar

### HTTP

Valores de `Cache-Control` (semântica conferida no MDN em 2026-11-25):

| Caso | Cabeçalho |
|---|---|
| JS, CSS e imagens com hash no nome | `Cache-Control: public, max-age=31536000, immutable` |
| HTML que aponta para esses arquivos | `Cache-Control: no-cache` |
| API pública que muda de vez em quando | `Cache-Control: public, max-age=60, s-maxage=300, stale-while-revalidate=300, stale-if-error=86400` |
| Dado de usuário logado | `Cache-Control: private, no-cache` |
| Dado sensível (conta, pagamento) | `Cache-Control: no-store` |

`no-cache` não significa "não guardar": significa guardar e revalidar com a origem antes de reusar. Quem proíbe guardar é `no-store`. `s-maxage` vale só para caches compartilhados (CDN), e `max-age` para o navegador. A configuração no servidor está na skill [nginx](../../nginx/SKILL.md) e na [Cloudflare](../../cloudflare/SKILL.md).

### Aplicação com Redis

Redis Open Source está na versão 8.12.0 (2026-11-22) e, a partir da 8.0, é licenciado em RSALv2, SSPLv1 ou AGPLv3 à escolha (README oficial, 2026-11-25). Para uso em servidor próprio isso costuma bastar; confira se a licença serve ao seu caso. O Valkey, fork mantido pela Linux Foundation, é a alternativa compatível.

Subir com limite de memória e remoção automática, preso ao `127.0.0.1` (o Docker ignora o `ufw` nas portas publicadas, como diz a skill [vps](../../vps/SKILL.md)):

```bash
docker run -d --name redis --restart unless-stopped -p 127.0.0.1:6379:6379 redis:8 redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

Executado em 2026-11-25 com a imagem `redis:8`, que baixou a versão 8.12.0: `CONFIG GET maxmemory-policy` devolveu `allkeys-lru`, `SET chave valor NX EX 10` respondeu `OK` e `INFO stats` listou `keyspace_hits`, `keyspace_misses` e `evicted_keys`. A etiqueta `redis:8` acompanha a série 8; para travar a versão em produção use a completa, como `redis:8.12.0`.

`allkeys-lru` é o padrão recomendado pela doc quando há "subconjunto quente" de chaves. `noeviction` devolve erro quando a memória enche (serve para filas, não para cache). Se o mesmo Redis guarda cache e dado que não pode sumir, a doc recomenda usar duas instâncias.

Cache-aside em TypeScript, com TTL e chave que inclui a empresa:

```ts
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL!);

export async function listarEspecialidades(companyId: number) {
  const key = `company:${companyId}:specialties:v1`;
  const hit = await redis.get(key);
  if (hit) return JSON.parse(hit);

  const rows = await db.specialty.findMany({ where: { companyId } });
  await redis.set(key, JSON.stringify(rows), 'EX', 300);
  return rows;
}

export async function atualizarEspecialidade(companyId: number, id: number, data: object) {
  await db.specialty.update({ where: { id }, data });
  await redis.del(`company:${companyId}:specialties:v1`);
}
```

A sintaxe `SET chave valor EX segundos` e a opção `NX` (só grava se não existir) estão na doc do comando `SET`. Para evitar a debandada, use `SET trava:chave token NX EX 10`: só quem conseguir a trava recalcula, e os outros esperam ou servem o dado antigo. A doc do Redis chama esse padrão de simples e o desencoraja para casos que exigem garantia forte; para cache, basta.

Medir se o cache ajuda, na saída de `INFO stats`:

```bash
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses|evicted_keys"
```

Taxa de acerto = `keyspace_hits / (keyspace_hits + keyspace_misses)`. Se a taxa for baixa e `evicted_keys` alto, a memória é pouca ou a política não combina com o acesso.

### Regras de invalidação

| Estratégia | Quando usar |
|---|---|
| TTL curto | Aceita dado atrasado por alguns minutos; é a mais simples |
| Apagar a chave ao escrever | Dado que o próprio sistema altera, como no exemplo acima |
| Chave versionada (`:v2`) | Mudou o formato do dado; as chaves antigas expiram sozinhas |
| Purgar na CDN | Página pública que mudou; use a API da CDN |

## Combina com / alternativas

- [Banco](02-banco-explain-n-mais-1-e-pool.md) primeiro; [filas](06-trabalho-pesado-fora-da-requisicao.md) quando o Redis também serve de broker.
- [Desempenho no cliente](../../user-experience/docs/12-desempenho-e-rede.md) para cache do navegador e Service Worker.
- [Cloudflare](../../cloudflare/SKILL.md) para cache de borda.
- Alternativas ao Redis: cache em memória do processo (uma instância só), cache na tabela do banco, ou o cache de framework (Django, Laravel, Spring) com Redis por trás.

## Decisão rápida

- **Sempre:** `Cache-Control` correto nos estáticos e `no-store` ou `private` no dado de usuário.
- **Cache de aplicação** quando uma consulta já ajustada continua pesando por ser repetida.
- **Evite:** cache sem TTL, chave sem escopo de empresa e cache de dado que precisa estar exato.
