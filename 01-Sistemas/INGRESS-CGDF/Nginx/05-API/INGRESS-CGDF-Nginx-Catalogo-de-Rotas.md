---
type: api
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: confirmado
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
tags:
  - ingress
  - nginx
  - rotas
sources:
  - locations/common/health-check.conf
  - locations/prod/
  - locations/nonprod/
---
# INGRESS-CGDF — catálogo de rotas

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Objetivo
Listar os prefixos de path expostos pelo ingress e o serviço de destino de cada um, por ambiente.

## Evidências
- Um `location` por variante em `locations/prod/*.conf` (18 arquivos) e `locations/nonprod/*.conf` (19 arquivos). Nomes de serviço são DNS internos do Swarm, não endereços.

## Informações confirmadas
**Convenção** (✅, igual em todos os arquivos):
- **Produção** (porta 8080): `/<app>/` → instância principal; `/<app>-test/` → instância de teste (também no cluster de produção).
- **Nonprod** (porta 80): `/staging/<app>/` e `/sandbox/<app>/`.
- O prefixo é removido por `rewrite ^/<prefixo>/(.*)$ /$1 break`; a aplicação recebe a requisição na raiz.
- Cabeçalhos repassados: `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`. Limite de corpo `client_max_body_size 50M`, exceto MinIO (`5G`).

**Rotas HTTP** (serviço e porta de destino; nonprod = mesmo nome com sufixo `-staging`/`-sandbox`, salvo a coluna "Observação"):

| App (prefixo) | Serviço de produção : porta | Serviço de teste (prod) | Observação |
|---|---|---|---|
| `api-super-busca` | `api-super-busca-backend:3000` | `…-test` | |
| `app-transparencia` | `app-portal-transparencia-back-end:8080` | `…-test` | |
| `cgdf-email-legacy` | `cgdf-microservicos-email-legacy:80` | `…-test` | |
| `cgdf-iza` | `iza-api:8000` | `iza-api-test` | |
| `cgdf-localization` | `cgdf-localization:80` | `…-test` | |
| `gerenciador-portal-transparencia` | `gerenciador-portal-transparencia-backend:8080` | `…-test` | |
| `html-to-pdf` | `html-to-pdf:3005` | `…-test` | |
| `identity-broker-service` | `identity-broker-service-prod:8080` | `identity-broker-service-prod-test` | nonprod usa `Host: $http_host` e `X-Forwarded-Proto: http` fixo |
| `integra` | `integra-backend-prod:8080` | `…-test` | |
| `keycloak` | `keycloak-prod:8080` | `keycloak-prod-test` | ver rota de health abaixo |
| `mail-service` | `mail-service-backend:8080` | `…-test` | |
| `minio` | `production-minio-stack_minio:9000` | `…_minio-test` | limite 5G; staging: `minio-infra-staging:9000`; sandbox: `sandbox-minio-stack_minio:9000` |
| `painel-ouvidoria` | `painel-ouvidoria:80` | `painel-ouvidoria-test` | path `/painel-ouvidoria/api/`; repassa `Upgrade`/`Connection` (WebSocket) |
| `participa-df` | `participa-df-backend:80` | `…-test` | |
| `peoples-check-api` | `peoples-check-api:8080` | `…-test` | |
| `portal-transparencia` | `portal-transparencia-backend:8080` | `…-test` | |
| `sci` | `sci-backend-prod:8080` | `…-test` | nonprod: `sci-backend-staging`/`-sandbox` |
| `sisconep-client` | `sisconep-client-backend-prod:8080` | `…-test` | arquivo `sisconep-client.conf` em prod e `sisconep.conf` em nonprod; nonprod usa `sisconep-client-backend-staging`/`-sandbox` |
| `sedoc` | não existe em produção | — | só nonprod: `sedoc-backend-staging`/`-sandbox:8080` |

**Health check do Keycloak** (`keycloak.conf`, commit `ed0dcea`):
- `location = /keycloak/health/` e `/keycloak-test/health/` (prod), `/staging/keycloak/health/` e `/sandbox/keycloak/health/` (nonprod) enviam para a porta `9000` do Keycloak, no caminho `/health/`.
- Em nonprod esses dois blocos usam o nome do serviço direto no `proxy_pass` (sem variável `$upstream`).

**Rota local**: `GET /healthcheck` → `200 ok`, em ambas as configurações.

## Inferências e limitações
- 🔶 Os sufixos `-test`, `-staging` e `-sandbox` seguem padrão de nome; a existência dos serviços não foi verificada.
- ❓ Se as rotas devem ser as mesmas em todos os ambientes (por exemplo `sedoc` ausente em produção) não está documentado.

## Relacionamentos
- [[01-Sistemas/INGRESS-CGDF/Nginx/04-Fluxos/INGRESS-CGDF-Nginx-Fluxo-de-Roteamento-de-Requisicao|Fluxo de roteamento]] · [[01-Sistemas/INGRESS-CGDF/Nginx/07-Integracoes/INGRESS-CGDF-Nginx-Integracoes-com-Upstreams|Integrações com upstreams]] · [[01-Sistemas/INGRESS-CGDF/Nginx/08-Qualidade/INGRESS-CGDF-Nginx-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
