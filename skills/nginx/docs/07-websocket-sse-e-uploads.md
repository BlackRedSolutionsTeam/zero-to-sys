# WebSocket, SSE e uploads grandes no nginx

> Para WebSocket repasse `Upgrade` e `Connection` com um `map`, para SSE desligue o buffering, e para upload ajuste `client_max_body_size` e `proxy_request_buffering` de forma consciente.

| | |
|---|---|
| **Referência** | nginx.org/en/docs: WebSocket proxying (http/websocket.html), ngx_http_proxy_module, ngx_http_core_module, ngx_http_map_module |
| **Categoria** | Servidor |
| **Tipo** | Prática de configuração de proxy reverso |
| **Vale para** | nginx 1.31.10 (versão atual da página CHANGES em 2026-11-25); aplicação Node, .NET, Python ou outra atrás do proxy |
| **Verificado em** | 2026-11-25 |

## O que é

Três situações em que o proxy padrão do nginx não basta:

- **WebSocket:** conexão que começa como HTTP e "vira" um canal aberto nos dois sentidos (chat, painel ao vivo).
- **SSE (Server-Sent Events):** o servidor mantém uma resposta HTTP aberta e vai mandando eventos, só do servidor para o navegador.
- **Upload grande:** o corpo da requisição (arquivo) é maior que o limite padrão.

Exemplo do doc: sistema de agendamento de clínica, com `app.clinica-exemplo.com.br`, API em `api.clinica-exemplo.com.br`, WebSocket de avisos da recepção em `/ws/` e envio de exames em `/exames/`.

## Por que usar

- **WebSocket não conecta sem isso:** `Upgrade` e `Connection` são cabeçalhos "hop-by-hop" (valem só entre dois nós vizinhos), então o nginx não os repassa sozinho.
- **SSE trava com buffering:** o nginx guarda a resposta em memória antes de entregar; o navegador recebe os eventos todos de uma vez, tarde demais.
- **Upload dá 413:** o limite padrão de `client_max_body_size` é `1m`.

## Quando usar

- A aplicação tem WebSocket, SSE ou envio de arquivos.
- O erro aparece só atrás do nginx e some ao acessar a porta da aplicação direto.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Só se tiver formulário com anexo |
| MVP de SaaS | ✅ Ótimo | Upload de arquivo e notificações em tempo real aparecem cedo |
| SaaS em crescimento | ✅ Ótimo | Tempo real e upload grande pedem timeouts e limites por rota |
| Sistema interno/corporativo | ✅ Ótimo | Anexos e painéis ao vivo são comuns |
| API/integração | 🟡 Serve | Upload em lote e streaming de eventos |
| App mobile com backend | ✅ Ótimo | Envio de foto e push em canal aberto |
| Arquivos enormes (vídeo de GB) | ❌ Evite | Passar pelo proxy e pela aplicação; use URL pré-assinada direto no storage |

## Quando é bom

- **Uma config por rota:** o limite alto de upload vale só em `/exames/`; o resto do site fica com limite baixo.
- **`map` reaproveitável:** declarado uma vez em `http {}`, serve a todos os sites.
- **Ping do aplicativo:** a aplicação manda ping de WebSocket, e a conexão não cai por inatividade.

## Quando é ruim

- **`client_max_body_size 0` global:** desliga a checagem e deixa qualquer um enviar arquivo sem fim. Defina um valor.
- **`proxy_read_timeout` de horas em tudo:** conexões travadas ficam abertas e consomem recursos. Aumente só na rota de tempo real.
- **`proxy_buffering off` em rota comum:** o nginx deixa de proteger a aplicação de clientes lentos.
- **Vários servidores na aplicação sem afinidade:** o WebSocket de uma sessão pode cair em outra instância; veja `ip_hash` ou Redis na aplicação.

## Como começar

**1. WebSocket.** O `map` vai fora do `server`, no contexto `http`. Se `Upgrade` vier vazio, `Connection` vira `close`:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 443 ssl;
    server_name api.clinica-exemplo.com.br;

    location /ws/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 1h;
    }
}
```

Por padrão a conexão fecha se a aplicação ficar 60 segundos sem enviar dados (`proxy_read_timeout 60s`). Aumente o tempo ou faça a aplicação enviar ping periódico. Conferido em 2026-11-25: desde a 1.29.7 o padrão de `proxy_http_version` é `1.1`; em versão anterior, adicione `proxy_http_version 1.1;`.

**2. SSE.** Desligue o buffering só na rota de eventos:

```nginx
location /eventos/ {
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;
    proxy_read_timeout 1h;
}
```

A aplicação também pode pedir isso sozinha com o cabeçalho de resposta `X-Accel-Buffering: no`, sem mexer no nginx. Para o `curl` testar: `curl -N https://api.clinica-exemplo.com.br/eventos/` (`-N` desliga o buffer do próprio curl).

**3. Upload grande.** Limite por rota:

```nginx
server {
    client_max_body_size 1m;

    location /exames/ {
        client_max_body_size 50m;
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_request_buffering off;
        proxy_read_timeout 300s;
    }
}
```

Como funciona:

- Passou do `client_max_body_size`, o nginx responde `413 Request Entity Too Large` (o navegador pode não mostrar a mensagem direito).
- Com `proxy_request_buffering on` (padrão), o nginx lê o arquivo inteiro antes de entregar à aplicação. Protege contra cliente lento, mas usa disco e adia o início.
- Com `off`, o corpo vai à aplicação conforme chega (bom para streaming de arquivo grande). Em troca, o nginx não pode tentar outro servidor do `upstream` se já começou a enviar.
- Se a aplicação também limita (Express, Kestrel, Django), ajuste lá o mesmo valor. Regras de segurança do arquivo (tipo, vírus, nome) ficam em [upload de arquivos](../../security/docs/07-upload-de-arquivos.md).

**Testar:**

```bash
sudo nginx -t && sudo systemctl reload nginx
head -c 60M /dev/zero > /tmp/grande.bin
curl -i -F "arquivo=@/tmp/grande.bin" https://api.clinica-exemplo.com.br/exames/
```

Esperado: `413` acima do limite configurado.

## Combina com / alternativas

- [Proxy reverso para a aplicação](03-proxy-reverso-para-a-aplicacao.md): cabeçalhos básicos e `upstream`.
- [Limites, headers e hardening](08-limites-headers-e-hardening.md): `limit_conn` em rotas de longa duração.
- [Logs e diagnóstico](09-logs-e-diagnostico.md): como ler 413, 499 e 504.
- Alternativa para arquivos grandes: URL pré-assinada do storage (veja a skill `infra`) para o arquivo nem passar pelo nginx.
- Alternativa para tempo real: serviço gerenciado de WebSocket, se a aplicação não aguenta milhares de conexões abertas.

## Decisão rápida

- **Use se:** a aplicação tem WebSocket, SSE ou upload; configure por rota, com `map`, timeouts e limites explícitos.
- **Evite se:** o arquivo passa de centenas de MB (use URL pré-assinada) ou se a ideia é liberar tudo com `client_max_body_size 0` e timeouts de horas no site inteiro.
