---
type: integration
aliases:
  - "Frontend Ouvidoria — integrações"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
sources:
  - app/api.service.js
  - app/api.config.js
  - api.config.json
  - app/open-street-map/map-open-street-directive.js
  - app/open-street-map/map-service.js
  - app/open-street-map/map-ol-service.js
  - app/auth/auth-ctrl.js
  - app/nav/nav-ctrl.js
  - package.json
---

# Frontend Ouvidoria — integrações

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Mapa: [[Mapa-de-Integracoes|Mapa de integrações]] · API: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas-de-API]]

## Visão geral
Nota canônica das integrações em que o `participa-df-ouv-frontend` é o consumidor (vários provedores; por isso `consumer`/`provider` ficam fora do cabeçalho). Endereços omitidos.

| Provedor | Direção | Tecnologia | Contrato / uso | Confirmação |
|---|---|---|---|---|
| `PARTICIPA-DF` (`participa-df-backend`) | saída | HTTP JSON, `Bearer` + cabeçalho de aplicação | 107 caminhos distintos: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API\|Chamadas-de-API]] | ✅ (99 conferidos por texto com o backend) |
| `Servico-Localizacao-CGDF` | saída | HTTP POST JSON direto do navegador (`/lat-long`, `/endereco`, `/ra`) | busca de endereço, endereço por coordenada e região administrativa no registro por operador | ✅ chamada; ❓ dono |
| `OpenStreetMap` | saída | tiles OSM via OpenLayers (`ol.source.OSM`) | camada base dos mapas de registro e de detalhe | ✅ |
| `Servico-WMS-Ortofoto-DF` | saída | WMS (`ol.source.TileWMS`) direto do navegador | ortofoto sobre o mapa de detalhe da manifestação | ✅ chamada; ❓ dono |
| outros servidores WMS (cartografia/transporte do DF) | saída | WMS | camadas do mapa do `painel-interativo`, que **não tem rota** | 🔶 inativo |
| front-end de login | saída (redirecionamento do navegador) | `window.location` para `Login` e `Principal` de `configuration/front-end-urls`; entrada em `/#/auth/{sessionId}` | login assistido e logout | ✅ redirecionamento; ❓ repositório do destino |
| SignalR | — | `@microsoft/signalr` em `package.json` | nenhum uso encontrado em `app/` | 🔶 sem uso |

## Evidências
Arquivos em `sources`, commit `9d8ecdb`.

## Informações confirmadas

### Backend `participa-df-backend`
- ✅ `Api` prefixa `configService.urlApi`; o interceptor adiciona cabeçalhos de aplicação/autorização apenas para URLs que contêm a `urlApi` (portanto **não** envia o token ao serviço de localização nem aos WMS).
- ✅ Direção: o frontend inicia todas as chamadas; não há *push* (SignalR sem uso).
- ✅ Falhas: 400 → `customException`; 500 → modal com código de rastreamento; 401/403 → redireciona ao login. Não há *retry* nem tratamento de *timeout*.

### Serviço de localização (`Servico-Localizacao-CGDF`)
- ✅ Configurado em `api.config.json` (`urlApiCgdfLocalization`), por ambiente; chamado com `Api.POSTe` (URL absoluta): `/lat-long` (`{Localidade}`), `/endereco` e `/ra` (`{Lat, Long}` como texto).
- ✅ Mesmo serviço já registrado para o [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas|Frontend Cidadão]]. Dono e SLA: ❓.
- ⚠️ Nos perfis `local` e `homologacao` o endereço é HTTP (sem TLS); em produção, HTTPS.
- ✅ A lista de regiões administrativas vem do backend (`servico-ouvidoria/regiao-administrativa`, `mapInfo.regioes`).

### Mapas
- ✅ Mapa de registro: `ol.source.OSM`. Mapa de detalhe (`MapService.getMapInterno`): camada OSM + ortofoto WMS. As camadas do `painel-interativo` (vias, linhas e estações) usam outros servidores WMS, mas a tela está sem rota.
- ✅ `mapOLService` define chamadas ao backend (`servicos/siturb/`, `servicos/ra/`, `servicos/localidade/...`) como proxy de camadas; 🔶 sem uso encontrado (resquício).

### Login assistido
- ✅ Entrada por `/#/auth/{sessionId}` e saída por `Login`/`Principal` vindos do backend; os endereços dos outros front-ends não constam neste repositório. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Autenticacao|Fluxo-Autenticacao]].

## Inferências e limitações
- 🔶 O serviço de IA para sugestão de assunto (`servico-ouvidoria/ia/assunto`) é acessado **pelo backend** (integração `Iza`); o frontend só chama o backend. Ver [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas do Backend]].
- ❓ Donos de `Servico-Localizacao-CGDF` e `Servico-WMS-Ortofoto-DF`.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[Catalogo-de-Sistemas|Catálogo]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/08-Seguranca/PARTICIPA-DF-Frontend-Ouvidoria-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Pendências e próximo passo
- Identificar os donos dos serviços de localização e de ortofoto e o repositório do front-end de login. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
