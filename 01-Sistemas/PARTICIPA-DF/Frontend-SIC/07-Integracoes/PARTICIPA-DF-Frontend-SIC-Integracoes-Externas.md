---
type: integration
aliases:
  - "Frontend SIC — integrações"
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
sources:
  - app/api.service.js
  - app/api.config.js
  - app/api-dist.config.js
  - api.config.json
  - app/auth/auth-ctrl.js
  - app/nav/nav-ctrl.js
  - app/token-auth-interceptor.js
  - nginx.conf
  - package.json
  - index.html
---

# Frontend SIC — integrações

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Mapa: [[Mapa-de-Integracoes|Mapa de integrações]] · API: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]]

## Visão geral
Nota canônica das integrações em que o `participa-df-sic-frontend` é o consumidor. Endereços omitidos. Diferentemente dos outros dois front-ends, **este não chama serviços externos pelo navegador** (nenhum mapa, geocodificação, WMS, analytics ou plugin de acessibilidade): tudo passa pelo backend.

| Provedor | Direção | Tecnologia | Contrato / uso | Confirmação |
|---|---|---|---|---|
| `PARTICIPA-DF` (`participa-df-backend`) | saída | HTTP JSON; `Bearer` + cabeçalho de aplicação; em homologação/produção via *proxy* `nginx` (`api/`) | 77 caminhos distintos: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API\|Chamadas-de-API]] | ✅ (76 conferidos por texto com o backend) |
| front-end de login (🔶 outro front-end do Participa) | entrada e saída (redirecionamento do navegador) | entrada em `/#/auth/{sessionId}`; saída por `window.location` para `Login` e `Principal` de `configuration/front-end-urls` | login assistido e logout | ✅ redirecionamento; ❓ repositório do destino |
| SignalR | — | `@microsoft/signalr` em `package.json` | nenhum uso em `app/` | 🔶 sem uso |

## Evidências
Arquivos em `sources`, commit `5518a81`. Busca por URLs absolutas em `app/**/*.js` encontrou apenas as constantes de `api.config.js`/`api-dist.config.js`.

## Informações confirmadas

### Backend `participa-df-backend`
- ✅ `configService.urlApi`: absoluto em `local` (omitido); relativo (`api/`) em `homologacao` e `producao`. No contêiner, `nginx` repassa `${BASE_HREF}api/*` para `BACKEND_TARGET` (variável do pipeline, valor omitido), com `X-Real-IP`, `X-Forwarded-For` e `X-Forwarded-Proto`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Perfis-e-Ambientes|Perfis-e-Ambientes]].
- ✅ Cabeçalhos: o interceptor só adiciona `application-key` e `Authorization` a URLs que **contêm** `urlApi` (comparação por `includes`; em homologação/produção `urlApi` = `api/`).
- ✅ Direção: o front inicia todas as chamadas; não há *push*. Falhas: ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Arquitetura|Arquitetura]] (400/500/401/403).
- ✅ Uso indireto de provedores do backend: SEI (`registrar-pedido-sei`, retorna o número do processo), validação de identidade (`security/*`), geração de PDF (`exportar-operador`) e envio do CSV por e-mail (exportação da caixa de entrada). Esses provedores são do backend ([[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas do Backend]]); aqui o front só chama o endpoint.

### Login assistido
- ✅ Entrada por `/#/auth/{sessionId}` e saída por `Login`/`Principal` vindos do backend; os endereços dos outros front-ends não constam neste repositório. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Autenticacao|Fluxo-Autenticacao]].

## Inferências e limitações
- 🔶 `Principal` redireciona para o logout comum (`/pages/logout`), indicando um portal comum aos três front-ends; não confirmado.
- 🔶 `@microsoft/signalr` e `signalr.js` indicam intenção de notificações em tempo real herdada do front de Ouvidoria; sem uso no SIC.
- ❓ Dono do front-end de login e emissor do `sessionId`.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[Catalogo-de-Sistemas|Catálogo]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/08-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]] · Equivalentes: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Integracoes-Externas|Frontend Ouvidoria]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas|Frontend Cidadão]]

## Pendências e próximo passo
- Identificar o front-end de login e confirmar se `SistemaSicDF` é este repositório. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
