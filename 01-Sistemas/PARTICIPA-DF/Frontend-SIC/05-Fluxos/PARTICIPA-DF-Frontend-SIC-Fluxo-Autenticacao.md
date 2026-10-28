---
type: flow
aliases:
  - "Frontend SIC — fluxo de autenticação"
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - app/auth/auth-ctrl.js
  - app/auth/auth.html
  - app/nav/nav-ctrl.js
  - app/token-auth-interceptor.js
  - app/token-storage-service.js
  - app/app.routes.js
---

# Frontend SIC — fluxo de autenticação

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Segurança: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/08-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Objetivo
Descrever como o operador entra e sai do SIC-DF.

## Evidências
Arquivos em `sources`, commit `5518a81`. Backend: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao do Backend]] (não reconferido nesta análise).

## Informações confirmadas

### Entrada (login assistido)
1. ✅ O navegador chega em `/#/auth/{sessionId}`, vindo de outro front-end (o `Login`/`Principal` de `configuration/front-end-urls`). 🔶 O `sessionId` é emitido pelo backend após a autenticação no front de login; o repositório desse front-end não foi identificado.
2. ✅ `authCtrl`: limpa o token (`tokenStorage.clear()`) e chama `GET security/token-retrieve/{sessionId}`; grava a resposta (`obj.data`) em `localStorage` (`auth_token_sic`).
3. ✅ Após **3 segundos** (`setTimeout`), emite `authenticate` em `$rootScope`.
4. ✅ `navCtrl` (menu, fora do `ng-view`) trata `authenticate` → `validateAuth()`: `GET security/is-auth` (sem *spinner*).
   - `true`: marca `isAuth`, carrega usuário (`GET v2/usuario/true/false`) e permissões (`GET operador-sic/consultar-permissoes`) e emite `confirmAuth`.
   - `false`: vai para `/auth/0`.
5. ✅ `authCtrl` trata `confirmAuth` com `window.location.href = window.location.pathname`, **recarregando a página no caminho atual sem o hash** (cai em `/`, a caixa de entrada). Alteração do commit `5bf484a` (2026-10-14): antes o destino era `"/"`, que em ambientes servidos em subcaminho (sandbox/homologação) levava o usuário à raiz do domínio.

### Carga normal da aplicação
- ✅ Sem sessão iniciada no navegador (`#/` ou outra rota que não contenha `auth`), `navCtrl.main()` chama `validateAuth()` diretamente. Sem token, `is-auth` responde 401/403 (🔶) e o interceptor leva o navegador ao `Login`.

### Troca de unidade
- ✅ O operador pode ter várias unidades. `operador-sic/unidades` lista; `operador-sic/alterar-unidade-atual` (`{UnidadeAtual:{Id}}`) troca; depois recarrega o usuário, vai a `/caixa-entrada` e executa `$route.reload()`.

### Saída
- ✅ `logout()`: `GET configuration/front-end-urls` → `window.location.href = ${Principal}/pages/logout` e `localStorage.clear()`.
- ✅ 401/403 em qualquer chamada: `GET configuration/front-end-urls` → `window.location.href = Login`.

## Inferências e limitações
- 🔶 O `setTimeout` de 3 s é uma espera arbitrária (provavelmente para o token estar disponível); não há tratamento de falha de `token-retrieve` (sem `catch`): se falhar, a tela de `auth.html` permanece.
- ✅ `navCtrl.main()` ignora caminhos que contêm `auth`, evitando validar a sessão durante a troca do `sessionId`.
- ❓ Origem do `sessionId`, tempo de vida do token e invalidação no logout.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]] · [[Mapa-de-Integracoes|Mapa de integrações]] · Equivalente: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Autenticacao|Fluxo-Autenticacao do Frontend Ouvidoria]]

## Pendências e próximo passo
- Identificar o front-end de login e quem emite o `sessionId`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
