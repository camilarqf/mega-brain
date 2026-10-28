---
type: flow
aliases:
  - "INGRESS-CGDF — fluxo de roteamento de requisição"
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: confirmado
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
sources:
  - nginx.conf
  - nginx-nonprod.conf
  - locations/
---
# INGRESS-CGDF — fluxo de roteamento de requisição

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Objetivo
Descrever o caminho de uma requisição HTTP pelo ingress.

## Evidências
- `nginx.conf`, `nginx-nonprod.conf` e arquivos `locations/**/*.conf`.

## Informações confirmadas
1. ✅ O cliente envia a requisição à porta do ingress (prod `8080`, nonprod `80`; publicada em `8080`).
2. ✅ O único `server` inclui o health check e as rotas do ambiente. O Nginx escolhe o `location` pelo prefixo mais longo (ou por igualdade, nas rotas `=` de health do Keycloak).
3. ✅ `GET /healthcheck` termina aqui com `200 ok`, sem tocar em upstream.
4. ✅ Nas demais rotas, `set $upstream <serviço>:<porta>` define o destino, `client_max_body_size` limita o corpo e `rewrite … break` remove o prefixo.
5. ✅ O Nginx resolve o nome do serviço pelo DNS interno do Docker (cache de 10 s) e faz `proxy_pass` em HTTP, acrescentando `Host`, `X-Real-IP`, `X-Forwarded-For` e `X-Forwarded-Proto` (no Keycloak e no IBS de nonprod: `X-Forwarded-Host`, `X-Forwarded-Proto: http` e `X-Forwarded-Port: 80` fixos).
6. ✅ A resposta do upstream volta ao cliente sem transformação (não há `sub_filter`, cache nem timeouts configurados).
7. ✅ Rota não correspondente: sem `location` padrão, vale o comportamento padrão do Nginx para a raiz (🔶 resposta `404`; não executado).

**Falhas**: ✅ não há `proxy_*_timeout`, `proxy_next_upstream` nem página de erro customizada; valem os padrões do Nginx. 🔶 Serviço inexistente no DNS resulta em erro `502` ao cliente.

## Inferências e limitações
- 🔶 `Host` e `X-Forwarded-Proto: $scheme` dependem de o Nginx receber o `Host` original; atrás de outro proxy o esquema visto é `http`.

## Relacionamentos
- [[01-Sistemas/INGRESS-CGDF/Nginx/06-API/INGRESS-CGDF-Nginx-Catalogo-de-Rotas|Catálogo de rotas]] · [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Arquitetura|Arquitetura]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
