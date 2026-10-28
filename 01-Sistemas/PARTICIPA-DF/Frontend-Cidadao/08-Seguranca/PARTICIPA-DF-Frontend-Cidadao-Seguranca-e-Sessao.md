---
type: security
aliases:
  - "Frontend Cidadão — segurança e sessão"
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - src/app/core/services/authentication.service.ts
  - src/app/core/services/auth.guard.ts
  - src/app/core/interceptors/jwt.interceptor.ts
  - src/app/pages/login/login.component.ts
  - src/app/pages/logout/logout.component.ts
  - src/app/pages/validacao/services/usuario-state-manager-service.ts
  - src/app/pages/validacao/gerenciar-validacao/gerenciar-validacao.component.ts
  - src/app/app.component.ts
  - src/app/core/pipes/safe-pipe.ts
---

# Frontend Cidadão — segurança e sessão

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Objetivo
Registrar como o frontend guarda e envia a identidade do usuário, protege rotas e encaminha a sessão a outros sistemas. **Nenhum token ou segredo é reproduzido.**

## Evidências
Arquivos em `sources`, commit `d250804`. Cobertura `parcial`: não foram lidos todos os componentes que manipulam dados pessoais.

## Informações confirmadas

### Guarda do token
- ✅ Após `POST security/auth` bem-sucedido, `AuthenticationService.storeUserData(token, username)` grava o objeto `Autenticacao` em `localStorage` na chave `_userData` e emite `triggerLogin`.
- ✅ `JwtInterceptor` envia `Authorization: Bearer <token>` em **todas** as requisições `HttpClient`, inclusive as `GET_E`/`POST_E` para o serviço de geolocalização (URL externa).
- ✅ O logout (`Logout`) só remove `_userData` e `usuario-store` do `localStorage` e emite `triggerLogout`; **não chama o backend**. Nenhuma chamada do frontend usa um endpoint de cancelamento de token. O backend tem um handler `CancelarToken` ([[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao do Backend]]).

### Proteção de rotas
- ✅ `AuthGuard` chama `security/is-auth` (resposta booleana). Se verdadeiro e `UsuarioStateManager.hasPermission()` (sem política LGPD pendente e sem troca de senha obrigatória, lidos de `usuario-store`), libera. Caso contrário redireciona para `pages/validacao/gerenciar-validacao` e, no mesmo ciclo, também para `pages/auth` com `returnUrl` (ver 🔶 abaixo). Quando não autenticado, vai para `pages/auth`.
- ✅ A decisão de segurança final é do backend: o frontend só decide a navegação.
- ✅ Rotas com `AuthGuard`: ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-Modulos/PARTICIPA-DF-Frontend-Cidadao-Rotas-e-Telas|Rotas-e-Telas]].

### Pendências pós-login (LGPD e senha)
- ✅ `GerenciarValidacao` chama `GET usuario`; o backend pode responder `428` com `Context.Usuario.RedefinirSenha` e `Context.IsNovaPoliticaPendenteDeAceite`. O frontend guarda os dois indicadores em `usuario-store` e abre o modal de aceite da política (`politica/vigente`, `politica/aceitar-vigente`) ou de troca de senha (`usuario/alterar-senha`).

### Login assistido para os outros sistemas
- ✅ `navigateToOuv()` e `navigateToSic()` calculam `sessionId = MD5(token)` (`ts-md5`), enviam `POST security/notify` com `{token, sessionId}` e, ao concluir, redirecionam o navegador para `<SistemaOuvDF ou SistemaSicDF>#/auth/<sessionId>`. As URLs destino vêm de `GET configuration/front-end-urls` (campos `SistemaOuvDF` e `SistemaSicDF`).
- ✅ Os botões só aparecem conforme `OperadorSoAtivo` e `OperadorSicAtivo` de `GET v2/usuario`.
- ✅ O backend do lado `notify`/`token-retrieve`: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao do Backend]].

### Conteúdo HTML
- ✅ `SafePipe` expõe `bypassSecurityTrustHtml/Style/Script/Url/ResourceUrl`.
- ✅ A tela de política LGPD usa `innerHTML="{{textCorrect}}"` (o Angular sanitiza o HTML, mas o conteúdo vem do backend).

## Inferências e limitações
- 🔶 Em `AuthGuard`, quando há pendência, o `navigate` para `gerenciar-validacao` é seguido de outro `navigate` para `auth` (não há `return` entre eles); o segundo prevalece. Comportamento a confirmar em teste manual.
- 🔶 `AuthenticationService.storeUserDataSubApplications` envia o token por `postMessage(token, '*')`, mas **não há chamadas a esse método** neste repositório (código não usado).
- ❓ Se o token expira no backend, o frontend só descobre ao chamar `is-auth`; não há tratamento global de `401`.
- ❓ Quais origens de front-end (`SistemaOuvDF`, `SistemaSicDF`) consomem o `sessionId`: repositórios não identificados.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Autenticacao|Fluxo-Autenticacao]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/09-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Debitos-Tecnicos|Débitos técnicos]]
- [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]].
