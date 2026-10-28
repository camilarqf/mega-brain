---
type: integration
aliases:
  - "Frontend Cidadão — integrações"
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
sources:
  - src/app/core/services/api.service.ts
  - src/app/layout/components/ol-map/ol-map.component.ts
  - src/app/app.component.ts
  - src/index.html
  - src/environments/environment.ts
  - web.config
---

# Frontend Cidadão — integrações

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Mapa: [[Mapa-de-Integracoes|Mapa de integrações]]

## Visão geral
Nota canônica das integrações em que o `participa-df-frontend` é o consumidor (vários provedores, como na nota do backend; por isso `consumer`/`provider` ficam fora do cabeçalho). Endereços omitidos.

| Provedor | Direção | Tecnologia | Contrato / uso | Confirmação |
|---|---|---|---|---|
| `PARTICIPA-DF` (`participa-df-backend`) | saída | HTTP JSON (REST), `Bearer` JWT | 66 caminhos: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API\|Chamadas-de-API]] | ✅ |
| `Servico-Localizacao-CGDF` | saída | HTTP POST JSON direto do navegador (`lat-long`, `endereco`, `ra`) | busca de endereço, endereço por coordenada e região administrativa por coordenada | ✅ chamada; ❓ dono |
| `Google-Analytics` | saída | `gtag.js` (Google Tag) | evento `config` com `page_path` a cada `NavigationEnd` | ✅ |
| `Perto-Digital` | entrada (script) | plugin JS de acessibilidade carregado de CDN | injeção no `<head>` | ✅ |
| OSM (tiles) | saída | OpenLayers `OSM` | camada base do mapa de local do fato | ✅ |
| CDNs (jsDelivr, Google Fonts) | entrada | CSS/fontes | Bootstrap 5.0.2 e fontes no `index.html` | ✅ |
| front-ends `SistemaOuvDF` e `SistemaSicDF` | saída (redirecionamento do navegador) | `window.location` com `#/auth/<sessionId>` após `security/notify` | login assistido | ✅ redirecionamento; ❓ repositórios dos destinos |

## Evidências
Arquivos em `sources`, commit `d250804`.

## Informações confirmadas
- ✅ **Backend:** toda chamada passa por `Api`; em `homolog` o `apiUrl` é `/api` e o `web.config` (IIS) reescreve `api/*` para o backend; em `production` o endereço é absoluto.
- ✅ **Localização:** `ol-map.component.ts` usa `Api.POST_E` com `environment.apiCgdfLocalization` — chamadas **diretas** do navegador, não pelo proxy do backend. O `JwtInterceptor` anexa o `Bearer` do Participa a essas chamadas (a URL é externa ao backend).
- ✅ **Analytics:** o identificador da propriedade está no código (omitido aqui).
- ✅ **Login assistido:** o frontend calcula `MD5(token)` como `sessionId`, avisa o backend (`security/notify`) e redireciona; quem consome o `sessionId` é o front de destino ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/08-Seguranca/PARTICIPA-DF-Frontend-Cidadao-Seguranca-e-Sessao|Seguranca-e-Sessao]]).

## Falhas e dependências
- `status 0` → "A conexão com o servidor falhou" (interceptor); `400`/`500` → modais do backend.
- ✅ Busca de endereço falha em silêncio (`catchError` devolve lista vazia).
- Plugin de acessibilidade: carrega com tempo-limite de 700 ms e cai para um segundo endereço; falha não bloqueia a página.
- Dependência de CDNs externas em produção (Bootstrap via jsDelivr, Google Fonts): indisponibilidade degrada o estilo.

## Inferências e limitações
- 🔶 `Servico-Localizacao-CGDF` pode ser o mesmo serviço que o backend consome por proxy como `Servico-Geocodificacao` (o proxy expõe `localidade/pesquisa` e `localidade/posicao`, caminhos diferentes dos chamados aqui). **Não confirmado**: IDs mantidos separados.
- 🔶 O token do Participa é enviado ao serviço de localização por efeito do interceptor global; se o serviço não precisa dele, é exposição desnecessária (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/09-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Debitos-Tecnicos|Débitos técnicos]]).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[Catalogo-de-Sistemas|Catálogo]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas do Backend]]

## Pendências e próximo passo
- Identificar o dono de `Servico-Localizacao-CGDF` e confirmar se é o mesmo de `Servico-Geocodificacao`.
- Identificar os repositórios dos front-ends de Ouvidoria (OuvDF) e SIC ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]]).
