# Remover código morto e dependências sem uso

> Código e pacotes que ninguém usa só trazem risco e peso: ache-os com ferramenta, confirme com teste e histórico e apague em PR pequeno (o Git guarda o passado).

| | |
|---|---|
| **Referência** | Knip (knip.dev); Vulture (github.com/jendrikseipp/vulture); `go mod tidy` (go.dev/ref/mod); analisadores do .NET (Microsoft Learn, IDE0005, IDE0051, IDE0052); `composer` e `npm` (documentação oficial); Refactoring, 2ª ed. (M. Fowler, 2018), "Remove Dead Code" |
| **Categoria** | Manutenção |
| **Tipo** | Prática de limpeza |
| **Vale para** | TypeScript e JavaScript, Python, .NET, PHP e Go |
| **Verificado em** | 2026-11-25 |

## O que é

Código morto é o que nunca roda: função sem chamada, arquivo sem importação, rota esquecida, feature flag que ficou ligada. Dependência sem uso é um pacote declarado que nenhum arquivo importa. Os dois custam: o código morto é lido, compilado e mantido; a dependência sem uso entra na auditoria de segurança e aumenta a superfície de ataque.

## Por que usar

- **Menos para ler e para atualizar:** cada pacote a menos é um PR a menos do robô.
- **Menos risco:** o pacote vulnerável que ninguém usa também alerta (skill `security`, [doc 08](../../security/docs/08-dependencias-vulneraveis.md)).
- **Build e imagem menores.**

## Quando usar

- Trimestralmente ([doc 07](07-rotina-trimestral-de-saude.md)).
- Depois de remover uma funcionalidade ou trocar uma biblioteca.
- Antes de uma migração grande: menos código para migrar.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Temas e plugins acumulam pacotes que ninguém usa |
| MVP de SaaS | ✅ Ótimo | Experimentos abandonados deixam rastro |
| SaaS em crescimento | ✅ Ótimo | Muita gente passou pelo código |
| Sistema interno/corporativo | ✅ Ótimo | Funcionalidade antiga que ninguém lembra |
| API/integração | 🟡 Serve | Rota "sem uso" pode ter um cliente externo; confirme nos logs |
| App mobile com backend | 🟡 Serve | Endpoint velho pode ser usado por versão antiga do app |
| Código com reflexão ou carga dinâmica | 🟡 Serve | A ferramenta não enxerga: valide à mão |

## Quando é bom

- **Ferramenta primeiro, olho depois:** a ferramenta lista, uma pessoa confirma.
- **PR só de remoção,** sem outras mudanças.
- **Testes e CI verdes** antes e depois.
- **Confirmar com dados:** log de acesso da rota, métricas, busca no repositório.
- **Confiar no Git:** quem precisar do código antigo o recupera do histórico; não comente nem deixe "para depois".

## Quando é ruim

- **Apagar tudo que a ferramenta lista,** sem conferir: falso positivo em código chamado por reflexão, por arquivo de configuração, por convenção do framework ou por outro repositório.
- **Remover rota pública** sem olhar o log: um cliente externo pode depender dela.
- **Comentar o código "por segurança":** o Git já guarda (skill `coding`, [doc 07](../../coding/docs/07-comentarios-e-documentacao.md)).
- **Remover dependência de runtime que só aparece em produção** (driver de banco carregado por nome).

## Como começar

### TypeScript e JavaScript: Knip

```bash
npx knip
```

O Knip, segundo a documentação, relata dependências, exportações e arquivos sem uso. Para fixar no projeto:

```bash
npm install -D knip typescript @types/node
```

```json
{
  "scripts": {
    "knip": "knip"
  }
}
```

Configuração em `knip.json` para dizer ao Knip quais são os pontos de entrada, se o framework não for reconhecido sozinho. Remover um pacote:

```bash
npm uninstall nome-do-pacote
npm ls nome-do-pacote
```

### Python: Vulture e pip

```bash
pip install vulture
vulture src/ --min-confidence 80
```

A confiança de cada achado varia: argumentos e código inalcançável 100%, imports 90%, funções e classes 60%. Comece pelo 100 e desça. Gere uma whitelist para o que for falso positivo:

```bash
vulture src/ --make-whitelist > whitelist.py
```

Para pacotes: confira `requirements.txt` ou `pyproject.toml` contra os imports reais.

### .NET

No `.editorconfig`, deixe os avisos de IDE0005 (using desnecessário), IDE0051 (membro privado sem uso) e IDE0052 (membro privado lido nunca) como sugestão ou aviso e rode:

```bash
dotnet format analyzers --severity info --diagnostics IDE0005 IDE0051 IDE0052 --verify-no-changes
dotnet list package --outdated
```

Para um pacote NuGet sem referência no código, procure o namespace no repositório antes de remover da `.csproj`.

### PHP

```bash
composer why nome/pacote
composer remove nome/pacote
```

Quem usa pode instalar o `composer-unused` para listar pacotes que o código não referencia; confira a documentação do projeto.

### Go

```bash
go mod tidy
go vet ./...
```

O `go mod tidy` remove do `go.mod` o que o código não importa e acrescenta o que falta.

### Procedimento seguro

1. Rode a ferramenta e exporte a lista.
2. Para cada item, confirme: busca no repositório, uso por reflexão, configuração, flag, rota nos logs.
3. Remova em lotes pequenos: um módulo ou uma dependência por commit.
4. Rode testes, build e o linter.
5. Para rota pública, registre uma métrica ou log de acesso por 30 dias antes de apagar.
6. Merge; no fim, o lockfile é regenerado.

### Feature flags esquecidas

Flag ligada para todos há mais de um mês: apague o ramo "desligado" e a própria flag (skill `infra`, [doc 14](../../infra/docs/14-feature-flags-e-rollback.md)).

## Combina com / alternativas

- [Dívida técnica](05-divida-tecnica.md): o código morto vira item de baixo custo.
- Skill `coding`: [refatoração segura](../../coding/docs/10-refatoracao-segura.md).
- Skill `security`: [dependências vulneráveis](../../security/docs/08-dependencias-vulneraveis.md).
- Skill `code-indexes`: ferramentas de grafo que ajudam a ver quem chama o quê.
- Alternativa: cobertura de testes em produção (APM com cobertura por rota) para achar o que não roda; exige ferramenta paga na maioria dos casos.

## Decisão rápida

- **Use se:** o projeto tem mais de seis meses ou recebeu mais de uma pessoa.
- **Evite apagar se:** a única prova é "a ferramenta disse"; confirme.
