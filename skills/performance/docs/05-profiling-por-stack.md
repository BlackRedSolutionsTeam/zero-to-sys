# Profiling por stack

> Quando o banco está bem e o processo ainda gasta CPU ou memória demais, o profiler mostra qual função consome o tempo, sem adivinhar.

| | |
|---|---|
| **Referência** | Node.js, Profiling (nodejs.org/en/learn/getting-started/profiling) e CLI `--cpu-prof`; Microsoft Learn, dotnet-trace (learn.microsoft.com/dotnet/core/diagnostics/dotnet-trace); py-spy (github.com/benfred/py-spy); Go blog, "Profiling Go Programs" (go.dev/blog/pprof) e pacote `net/http/pprof` |
| **Categoria** | Desempenho |
| **Tipo** | Prática de diagnóstico |
| **Vale para** | Node, .NET, Python e Go (Java e PHP ficam em "Quando a lista não cobre" da SKILL) |
| **Verificado em** | 2026-11-25 |

## O que é

**Profiler** é uma ferramenta que amostra o programa enquanto ele roda e diz onde o tempo foi gasto. O resultado costuma ser um **flame graph** (gráfico de chamas): cada barra é uma função, a largura é o tempo total, e as barras mais largas no topo são os candidatos a otimizar.

Dois tipos de perfil:

- **CPU:** onde o processador gasta tempo. Serve quando o processo está em 100% de CPU ou a requisição é lenta sem esperar o banco.
- **Memória (heap):** o que está alocado. Serve para vazamento e para pausas longas do coletor de lixo.

## Por que usar

- **Acha a função certa** em vez de reescrever o módulo inteiro.
- **Funciona em produção** com sobrecarga baixa nas ferramentas de amostragem.
- **Prova o ganho:** o gráfico antes e depois mostra a barra encolhendo.

## Quando usar

- A CPU do app está alta e o banco está tranquilo (conferido no [doc 01](01-medir-primeiro.md)).
- O traço do APM mostra tempo "no código", não em consulta nem em chamada externa.
- A memória cresce até o processo ser morto (vazamento) ou há travadas periódicas.
- Depois de um teste de carga ([doc 04](04-teste-de-carga-com-k6.md)) em que o app satura antes do banco.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | O gargalo costuma estar em imagens e cache, não em CPU do servidor |
| MVP de SaaS | 🟡 Serve | Quase sempre o banco explica a lentidão; use o profiler se não explicar |
| SaaS em crescimento | ✅ Ótimo | Serialização, validação e cálculo pesado aparecem com o volume |
| Sistema interno/corporativo | ✅ Ótimo | Relatórios e importações em código costumam ser CPU puro |
| API/integração | ✅ Ótimo | Serialização JSON e criptografia dominam em alta vazão |
| App mobile com backend | 🟡 Serve | Vale para o back; o app tem profiler próprio (Xcode Instruments, Android Studio Profiler) |
| Perfil sem sintoma | ❌ Evite | Sem problema medido, não há o que procurar |

## Quando é bom

- **Amostragem** custa pouco e não exige alterar o código.
- **Mesmo fluxo em todas as stacks:** coletar, abrir no visualizador (speedscope, DevTools, pprof), achar a barra larga.
- **Ferramentas oficiais** (Node, .NET, Go) vêm com a plataforma.

## Quando é ruim

- **Perfil em máquina de desenvolvimento** com dados pequenos engana; reproduza a carga ([doc 04](04-teste-de-carga-com-k6.md)) enquanto coleta.
- **Código assíncrono** em Node e Python pode mostrar a espera como "tempo parado"; o perfil de CPU não enxerga a espera de I/O. Use o traço do APM para isso.
- **Ferramenta de depuração exposta** dá controle total do processo. Nunca deixe a porta do inspetor do Node ou o `pprof` do Go abertos à internet.
- **Mudar sem medir de novo:** otimizar a função mais larga e não repetir o perfil.

## Como começar

Fluxo igual em todas as stacks: suba carga com o k6, colete 30 a 60 segundos de perfil, abra o resultado, mexa na maior barra, repita e compare.

### Node

Perfil de CPU embutido, executado no Node v26.13.1 em 2026-11-25 (gerou `CPU.<data>.<hora>.<pid>.0.001.cpuprofile` dentro da pasta de `--cpu-prof-dir`). Ao encerrar o processo, grava um arquivo `.cpuprofile`:

```bash
node --cpu-prof --cpu-prof-dir=./perfis dist/server.js
```

Abra o arquivo no Chrome DevTools (aba Performance, "Load profile") ou no speedscope. Alternativa embutida mais antiga, o `--prof`, gera um log processado por `node --prof-process isolate-*.log > processado.txt`; a seção `[Bottom up (heavy) profile]` mostra quem chama a função quente. Para ver ao vivo, `node --inspect dist/server.js` escuta em `127.0.0.1:9229` e abre em `chrome://inspect`. Em servidor remoto, acesse por túnel SSH, nunca com `--inspect=0.0.0.0`.

Sintoma típico: função síncrona pesada (criptografia, JSON gigante, regex) que bloqueia o laço de eventos e atrasa todas as requisições. A doc do Node mostra um caso em que trocar `pbkdf2Sync` pela versão assíncrona subiu a vazão de cerca de 5 para 19,5 requisições por segundo.

### .NET

Instalar as ferramentas de diagnóstico (a doc da `dotnet-trace` foi atualizada em 2026-10 e vale para a versão 9.0.661903 em diante):

```bash
dotnet tool install --global dotnet-trace
dotnet tool install --global dotnet-counters
```

Listar os processos, coletar 30 segundos e converter para o speedscope:

```bash
dotnet-trace ps
dotnet-trace collect --process-id 1234 --duration 00:00:00:30 --format Speedscope
```

Sem `--profile`, a ferramenta usa `dotnet-common` mais `dotnet-sampled-thread-time`. O perfil antigo `cpu-sampling` foi removido do `collect` porque o nome enganava. O perfil `database` captura comandos do ADO.NET e do Entity Framework, útil para ver as consultas que o ORM gerou. Para métricas ao vivo (GC, alocações, requisições por segundo):

```bash
dotnet-counters monitor --process-id 1234
```

Testado em 2026-11-25 numa imagem `mcr.microsoft.com/dotnet/sdk:10.0` (linux/arm64) com `dotnet-trace` e `dotnet-counters` 10.0.750501: `ps`, `collect --duration 00:00:00:05 --format Speedscope` (gerou `.nettrace` e `.speedscope.json`) e `monitor` (sem `--counters`, monitora `System.Runtime` por padrão) funcionaram. Rode como o mesmo usuário do processo (ou root) e, em contêiner, com o mesmo `TMPDIR`. Abra o `.speedscope.json` em speedscope.app.

### Python

O `py-spy` amostra um processo Python em execução, sem alterar o código (instalação: `pip install py-spy`):

```bash
py-spy top --pid 1234
py-spy record -o perfil.svg --pid 1234
py-spy dump --pid 1234
```

`top` mostra as funções mais quentes ao vivo, `record` gera o flame graph em SVG e `dump` imprime a pilha atual de cada thread (bom para um processo "travado"). No Linux, anexar a um processo existente costuma exigir `sudo`; no macOS sempre. Em Docker, suba o contêiner com `--cap-add SYS_PTRACE`. Para um script curto, a biblioteca padrão basta:

```bash
python -m cProfile -o perfil.prof app.py
```

`cProfile` executado com Python 3.9.6 em 2026-11-25: o `-o perfil.prof` grava o arquivo ao fim do script (leia com `python -m pstats perfil.prof`). O `py-spy` não foi executado nesta conferência; os comandos vêm do README do projeto.

Em Django e FastAPI, o banco costuma ser a causa; ligue o log de consultas antes do profiler.

### Go

Importe `net/http/pprof` com efeito colateral e sirva numa porta interna, nunca na pública:

```go
package main

import (
	"log"
	"net/http"
	_ "net/http/pprof"
)

func main() {
	go func() {
		log.Println(http.ListenAndServe("127.0.0.1:6060", nil))
	}()
	runServer()
}
```

Coletar 30 segundos de CPU e olhar a memória:

```bash
go tool pprof "http://127.0.0.1:6060/debug/pprof/profile?seconds=30"
go tool pprof http://127.0.0.1:6060/debug/pprof/heap
```

Os endpoints `/debug/pprof/profile?seconds=N` e `/debug/pprof/heap` foram executados em 2026-11-25 com Go 1.25.14 (imagem `golang:1.25`, linux/arm64) e o `pprof` baixou os dois perfis. O `profile` só traz amostras se houver carga durante os `seconds`; sem requisições, o resultado vem com 0 amostras. Dentro do `pprof`, `top10` lista as funções mais caras e `web` desenha o grafo (precisa do Graphviz). Para o flame graph no navegador: `go tool pprof -http=:8081 arquivo.pb.gz`. Em servidor, acesse a porta 6060 por túnel SSH.

## Combina com / alternativas

- [Medir primeiro](01-medir-primeiro.md) para saber se o problema é CPU; [banco](02-banco-explain-n-mais-1-e-pool.md) e [filas](06-trabalho-pesado-fora-da-requisicao.md) quando o código pesado pode sair da requisição.
- [Stacks](../../stacks/SKILL.md) para a escolha de linguagem e framework.
- Alternativas: Clinic.js (Node), PerfView e Visual Studio (Windows, .NET), Scalene e Pyroscope (Python), Grafana Pyroscope para perfil contínuo em produção em qualquer stack.

## Decisão rápida

- **Use** quando a CPU ou a memória do processo é o gargalo comprovado.
- **Comece por:** `--cpu-prof` (Node), `dotnet-trace` (.NET), `py-spy` (Python), `pprof` (Go).
- **Evite:** deixar inspetor ou `pprof` exposto fora de `127.0.0.1` e otimizar função que não aparece no gráfico.
