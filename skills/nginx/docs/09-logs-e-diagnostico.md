# Logs e diagnóstico do nginx

> Registre cada requisição com um `$request_id` e os tempos do upstream, rotacione os arquivos e use uma tabela de sintoma, causa e correção para 502, 504, 413, redirect infinito e IP errado.

| | |
|---|---|
| **Referência** | nginx.org/en/docs: ngx_http_log_module, ngx_http_upstream_module, ngx_http_core_module (variáveis), Controlling nginx (control.html), Command-line parameters (switches.html), ngx_http_proxy_module |
| **Categoria** | Servidor |
| **Tipo** | Prática de observabilidade e diagnóstico |
| **Vale para** | nginx 1.31.10 (versão atual da página CHANGES em 2026-11-25); servidor Linux com systemd |
| **Verificado em** | 2026-11-25 |

## O que é

O nginx escreve dois logs:

- **`access.log`:** uma linha por requisição (quem pediu, o que, status, tempo).
- **`error.log`:** problemas do próprio nginx (conexão recusada pela aplicação, arquivo não achado, config).

O `$request_id` é um identificador único de 32 caracteres hexadecimais gerado a cada requisição (desde a 1.11.0). Repassado à aplicação, liga a linha do nginx à linha do log da aplicação.

Exemplo do doc: sistema de agendamento de clínica em `app.clinica-exemplo.com.br`, API Node na porta 3000.

## Por que usar

- **Achar a causa rápido:** um 502 pode ser aplicação fora do ar, porta errada ou timeout; o log diz qual.
- **Saber se o lento é o nginx ou a aplicação:** `$request_time` contra `$upstream_response_time`.
- **Rastrear um erro de cliente:** o usuário informa o `request_id` da tela de erro e você acha tudo.

## Quando usar

- Desde o primeiro deploy, antes do primeiro problema.
- Ao investigar erro que "só acontece em produção".

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Log padrão e logrotate bastam |
| MVP de SaaS | ✅ Ótimo | `$request_id` evita adivinhar qual erro é qual |
| SaaS em crescimento | ✅ Ótimo | Formato JSON alimenta a ferramenta de logs |
| Sistema interno/corporativo | ✅ Ótimo | Auditoria de acesso por IP e usuário |
| API/integração | ✅ Ótimo | Tempo do upstream mostra rota lenta |
| App mobile com backend | ✅ Ótimo | Cliente reporta o `request_id` do erro |
| Servidor sem rotação e disco pequeno | ❌ Evite | O log enche o disco e derruba o servidor |

## Quando é bom

- **Formato com tempos:** `$request_time`, `$upstream_connect_time`, `$upstream_response_time` e `$upstream_status`.
- **Log por site:** cada `server` com seu `access_log`.
- **Mesmo id nos dois lados:** o header `X-Request-ID` chega à aplicação e volta ao cliente.

## Quando é ruim

- **Log com dado sensível:** `$request` inclui a URL; token ou e-mail em query string vai para o arquivo. Mande segredo no corpo ou no header.
- **`error_log` em `debug` em produção:** gera volume enorme; use só por pouco tempo.
- **`access_log off` para "economizar":** perde a única prova do que aconteceu.

## Como começar

**1. Formato com `$request_id` e tempos** (em `http {}`):

```nginx
log_format principal '$remote_addr [$time_local] "$request" $status $body_bytes_sent '
                     'rid=$request_id rt=$request_time '
                     'uct=$upstream_connect_time urt=$upstream_response_time us=$upstream_status '
                     'host=$host';

access_log /var/log/nginx/clinica-access.log principal;
error_log /var/log/nginx/clinica-error.log warn;
```

Dentro do `location` do proxy, passe e devolva o id:

```nginx
proxy_set_header X-Request-ID $request_id;
add_header X-Request-ID $request_id always;
```

Leitura: `rt` é o tempo total da requisição; `urt` é o tempo que a aplicação levou. Se `rt` é alto e `urt` baixo, o problema é rede ou cliente lento; se os dois são altos, é a aplicação. Com buffer, `access_log ... principal buffer=32k flush=5s;` reduz escrita em disco.

**2. Rotação com logrotate.** O pacote oficial já instala `/etc/logrotate.d/nginx`; confira se cobre seus arquivos. Exemplo:

```
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        [ -f /run/nginx.pid ] && kill -USR1 $(cat /run/nginx.pid)
    endscript
}
```

Pela documentação, para rotacionar é preciso renomear o arquivo e enviar o sinal `USR1` ao processo mestre, que reabre os logs. Teste: `sudo logrotate -d /etc/logrotate.d/nginx` (simula) e `sudo logrotate -f /etc/logrotate.d/nginx` (força). O caminho do PID varia por distro (`nginx.conf` ou `/run/nginx.pid`).

**3. Comandos de diagnóstico:**

```bash
sudo nginx -t
sudo nginx -T | less
curl -I https://app.clinica-exemplo.com.br
curl -sI -o /dev/null -w "%{http_code} %{time_total}\n" https://api.clinica-exemplo.com.br/saude
sudo ss -tlnp | grep -E ':(80|443|3000)\b'
sudo tail -f /var/log/nginx/clinica-error.log
grep 'rid=<id-do-erro>' /var/log/nginx/clinica-access.log
```

- `nginx -t` testa sintaxe e abertura de arquivos; `nginx -T` testa e imprime toda a configuração carregada (inclui os `include`), a forma certa de ver o que está de fato ativo (desde a 1.9.2).
- `curl -I` mostra só os cabeçalhos: status, `Location` de redirect, `Server`, HSTS.
- `ss -tlnp` lista portas em escuta e o processo dono: confirma que o nginx escuta 443 e que a aplicação escuta 3000 em `127.0.0.1`.

**4. Tabela de sintomas:**

| Sintoma | Causa provável | Como confirmar | Correção |
|---|---|---|---|
| **502 Bad Gateway** | Aplicação parada, porta ou endereço errado no `proxy_pass`, ou a aplicação escuta em outra interface | `error.log` com `connect() failed (111: Connection refused)`; `ss -tlnp` não mostra a porta | Subir a aplicação; corrigir o `proxy_pass`; `systemctl status` da aplicação |
| **502** com SELinux ativo (RHEL, Fedora) | Política bloqueia o nginx de conectar à rede | `error.log` com `Permission denied` ao conectar | Habilitar `httpd_can_network_connect` (`setsebool -P`) |
| **504 Gateway Timeout** | Aplicação demora mais que `proxy_read_timeout` (padrão 60s) | `urt` perto de 60 e `error.log` com `upstream timed out` | Otimizar a rota; subir o timeout só nela; mover tarefa longa para fila |
| **413 Request Entity Too Large** | Corpo maior que `client_max_body_size` (padrão 1m) | `error.log` com `client intended to send too large body` | Aumentar o limite na rota de upload ([doc 07](07-websocket-sse-e-uploads.md)) e na aplicação |
| **Redirect infinito** (`ERR_TOO_MANY_REDIRECTS`) | Aplicação recebe HTTP e redireciona para HTTPS sem saber que o nginx já fez isso; ou Cloudflare em SSL "Flexible" com redirect na origem | `curl -IL` mostra o mesmo `Location` repetido | Enviar `X-Forwarded-Proto $scheme`, aplicação confiar nele; na Cloudflare usar `Full (strict)` ([doc 05](05-atras-da-cloudflare.md)) |
| **IP errado nos logs** (sempre o do proxy ou da Cloudflare) | Falta restaurar o IP real | `$remote_addr` igual em todas as linhas | Módulo `realip`: `set_real_ip_from` e `real_ip_header` ([doc 05](05-atras-da-cloudflare.md)); na aplicação, confiar só no proxy conhecido |
| **WebSocket cai a cada 60s** | `proxy_read_timeout` padrão | Fecha sempre no mesmo tempo | Aumentar o timeout ou enviar ping ([doc 07](07-websocket-sse-e-uploads.md)) |
| **404 só em rota do SPA** | Falta `try_files` com fallback para `index.html` | `curl -I` na rota interna dá 404 | `try_files $uri /index.html;` ([doc 06](06-estaticos-cache-e-compressao.md)) |
| **Config nova não surte efeito** | `reload` não executado ou `include` errado | `nginx -T` não mostra a mudança | `nginx -t && systemctl reload nginx` |
| **`bind() to 0.0.0.0:443 failed (98: Address already in use)`** | Outro processo usa a porta | `ss -tlnp` | Parar o outro processo ou mudar a porta |

As mensagens do `error.log` e a linha de SELinux vêm da prática comum e não de nginx.org: confirme no seu log. Os 499 (cliente fechou a conexão antes da resposta) são código interno do nginx para logs, não erro do servidor.

## Combina com / alternativas

- [Observabilidade (infra)](../../infra/docs/10-observabilidade.md): enviar o log ao Grafana/Loki ou Sentry; o `rid` liga as camadas.
- [Limites, headers e hardening](08-limites-headers-e-hardening.md): os 429 aparecem aqui.
- [Proxy reverso para a aplicação](03-proxy-reverso-para-a-aplicacao.md): timeouts e `upstream`.
- Alternativa: log em JSON com `log_format ... escape=json` (parâmetro `escape` conferido na página do `log_format`), para ferramentas que leem estruturado.

## Decisão rápida

- **Use se:** o nginx está em produção; ative o formato com `rid` e tempos, rotacione e guarde a tabela de sintomas junto da equipe.
- **Evite se:** a ideia é depurar com `error_log debug` ligado o tempo todo ou deixar o log crescer sem rotação.
