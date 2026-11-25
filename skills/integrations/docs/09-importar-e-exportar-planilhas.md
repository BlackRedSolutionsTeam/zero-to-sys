# Importar e exportar planilhas

> Importação é upload, job em fila, validação linha a linha e relatório de erros; exportação grande é streaming ou job, sempre protegida contra injeção de fórmula.

| | |
|---|---|
| **Referência** | OWASP "CSV Injection"; RFC 4180 (CSV); documentação oficial de Papa Parse, SheetJS, ExcelJS, pandas, openpyxl, ClosedXML, MiniExcel, EPPlus e Laravel Excel |
| **Categoria** | Integrações |
| **Tipo** | Prática de importação e exportação de dados |
| **Vale para** | Node, Python, .NET, Java, Laravel, Go |
| **Verificado em** | 2026-11-24 |

## O que é

Importar é ler um CSV ou XLSX enviado pelo usuário e gravar as linhas no sistema. Exportar é gerar um arquivo com os dados para baixar. CSV é texto com valores separados por vírgula ou ponto e vírgula; XLSX é o formato do Excel.

## Por que usar

- **Migração fácil:** a clínica traz a lista de pacientes da planilha antiga.
- **Sistema não trava:** o trabalho pesado roda em segundo plano.
- **Usuário sabe o que deu errado:** o relatório diz a linha e o motivo.

## Quando usar

- Carga inicial de pacientes, profissionais ou tabela de preços.
- Relatórios que o financeiro abre no Excel.
- Qualquer lista maior que algumas centenas de linhas.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Raramente precisa |
| MVP de SaaS | ✅ Ótimo | Importar a base do cliente tira a barreira de entrada |
| SaaS em crescimento | ✅ Ótimo | Volume cresce; job e streaming viram obrigação |
| Sistema interno/corporativo | ✅ Ótimo | Planilha é o formato que o negócio já usa |
| API/integração | 🟡 Serve | Entre sistemas, prefira a API; planilha é para humanos |
| App mobile | 🟡 Serve | Exportar costuma ser por e-mail ou link de download |

## Quando é bom

- **Upload para storage e job em fila:** a requisição só registra a importação e responde `202`; veja [armazenamento](./07-armazenamento-de-arquivos.md) e [filas](./05-filas-e-jobs.md).
- **Pré-visualização:** valide as primeiras linhas e mostre "42 válidas, 3 com erro" antes de confirmar.
- **Relatório por linha:** `linha`, `coluna`, `motivo` (ex.: `7, cpf, CPF inválido`), baixável como CSV.
- **Idempotência por chave natural:** use CPF do paciente (por clínica) como chave e faça `insert ... on conflict (clinic_id, cpf) do update`. Reenviar o mesmo arquivo não duplica.
- **Decisão: importar as válidas e reportar as inválidas.** É melhor para listas grandes, onde uma linha ruim não deve travar 5 mil boas. Use tudo-ou-nada (uma transação só, [09 de dados](../../data/docs/09-transacoes-e-concorrencia.md)) quando as linhas dependem umas das outras, como lançamentos contábeis que precisam fechar a soma.
- **Processar em lotes** (ex.: 500 linhas por transação) e guardar o progresso na tabela `imports`.

## Quando é ruim

- **Ler o arquivo inteiro na memória** e validar dentro da requisição HTTP.
- **Confiar na planilha:** valide tipo, tamanho e conteúdo como qualquer entrada ([segurança de upload](../../security/docs/07-upload-de-arquivos.md)).
- **Falha silenciosa:** pular linhas sem avisar.
- **Exportar tudo na requisição** quando são milhões de linhas.
- **Gravar valor do usuário no CSV sem tratar** começo `=`, `+`, `-`, `@`.

## Como começar

Tabelas de controle:

```sql
create table imports (
  id uuid primary key,
  clinic_id uuid not null references clinics(id),
  file_id uuid not null references files(id),
  status text not null default 'queued',
  total_rows int,
  ok_rows int not null default 0,
  error_rows int not null default 0,
  created_at timestamptz not null default now()
);

create table import_errors (
  import_id uuid not null references imports(id),
  line int not null,
  column_name text,
  reason text not null
);
```

Bibliotecas por stack, com a licença conferida nos repositórios oficiais e nos registros em 2026-11-25 (confirme de novo antes de adotar, pois licenças mudam):

| Stack | CSV | XLSX | Observação |
|---|---|---|---|
| Node | Papa Parse (MIT) | SheetJS CE (Apache 2.0), ExcelJS (MIT) | ExcelJS tem leitura e escrita em streaming. O pacote `xlsx` no npm está parado na 0.18.5; a versão atual do SheetJS CE sai pelo cdn.sheetjs.com |
| Python | pandas (BSD-3-Clause), módulo `csv` | openpyxl (MIT), pandas | pandas carrega tudo; use `chunksize` em CSV grande |
| .NET | MiniExcel (Apache 2.0), CsvHelper (MS-PL ou Apache 2.0) | ClosedXML (MIT), MiniExcel, EPPlus | Restrição comercial: EPPlus 5 em diante usa Polyform Noncommercial 1.0.0, e o uso comercial exige licença paga. Prefira ClosedXML ou MiniExcel |
| Java | Apache Commons CSV | Apache POI (Apache 2.0) | Apache Commons CSV também é Apache 2.0 |
| Laravel | Laravel Excel (MIT) | Laravel Excel (MIT) | Fila e chunks embutidos |
| Go | `encoding/csv` | excelize (BSD-3-Clause) | Biblioteca padrão e excelize têm licença permissiva |

Leitura de CSV em streaming com validação (Node):

```ts
import Papa from "papaparse";
import { createReadStream } from "node:fs";
import { z } from "zod";

const Row = z.object({
  nome: z.string().min(1),
  cpf: z.string().regex(/^\d{11}$/),
  nascimento: z.string().regex(/^\d{2}\/\d{2}\/\d{4}$/),
  valor: z.string().optional(),
});

export function parseDateBr(s: string) {
  const [d, m, y] = s.split("/").map(Number);
  return new Date(Date.UTC(y, m - 1, d));
}

export function parseDecimalBr(s: string) {
  return Number(s.replace(/\./g, "").replace(",", "."));
}

export function readCsv(path: string, onRow: (row: unknown, line: number) => Promise<void>) {
  return new Promise<void>((resolve, reject) => {
    let line = 1;
    Papa.parse(createReadStream(path, { encoding: "utf8" }), {
      header: true,
      skipEmptyLines: true,
      delimiter: "",
      step: async (r, parser) => {
        parser.pause();
        line += 1;
        await onRow(r.data, line);
        parser.resume();
      },
      complete: () => resolve(),
      error: reject,
    });
  });
}
```

Cuidados do Excel brasileiro:

- **Separador:** o Excel em português salva CSV com `;`. Deixe o parser detectar o delimitador (como acima) ou aceite os dois.
- **Codificação:** pode vir em UTF-8 com BOM (marca de ordem de bytes no início do arquivo) ou em Windows-1252. Remova o BOM e avise quando houver caracteres quebrados.
- **Datas e decimais:** `31/12/2026` e `1.234,56`. Converta explicitamente, nunca confie na detecção automática.
- **CPF e telefone:** o Excel remove zeros à esquerda; peça a coluna como texto e normalize.

Exportação:

- Volume pequeno: gere e devolva direto.
- Volume grande: faça streaming (leia do banco por cursor e escreva a resposta aos poucos) ou crie um job que gera o arquivo, grava no storage e avisa por notificação ([08](./08-tempo-real-e-notificacoes.md)) com link pré-assinado.
- Para abrir bem no Excel brasileiro: separador `;`, UTF-8 com BOM e decimais com vírgula.

Injeção de fórmula em CSV (OWASP CSV Injection): se uma célula começa com `=`, `+`, `-` ou `@`, o Excel pode executá-la como fórmula. Um paciente chamado `=HYPERLINK(...)` vira ataque contra quem abre o arquivo. A mitigação recomendada pela OWASP é prefixar o valor com apóstrofo e entre aspas:

```ts
export function safeCell(value: string) {
  return /^[=+\-@\t\r]/.test(value) ? `'${value}` : value;
}
```

Aplique em todo campo de texto vindo do usuário, em todo export.

## Combina com / alternativas

- [Armazenamento de arquivos](./07-armazenamento-de-arquivos.md) e [filas e jobs](./05-filas-e-jobs.md).
- [Tempo real e notificações](./08-tempo-real-e-notificacoes.md) para avisar "importação concluída".
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md).
- [Segurança de upload](../../security/docs/07-upload-de-arquivos.md).
- Alternativa: API em lote (`POST /patients/batch`) quando o emissor é outro sistema.

## Decisão rápida

- **Use se:** usuários trazem ou levam dados em planilha.
- **Evite se:** o outro lado é um sistema; use API ou webhook.
