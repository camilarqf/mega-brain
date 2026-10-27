---
type: reference
system: SICI
repository: sici-frontend
status: confirmado
coverage: completa
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - stack
  - dependencias
sources:
  - package.json
  - angular.json
  - tsconfig.json
  - tsconfig.app.json
  - tsconfig.spec.json
  - .docker/Dockerfile
---

# Stack e dependências — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]], [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Perfis-e-Ambientes|Perfis-e-Ambientes]] · Backend: [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Stack-e-Dependencias|Stack do Backend]]

## Objetivo
Registrar a stack e as dependências declaradas do `sici-frontend`.

## Evidências
`package.json` (versões **declaradas**, em faixas `^`/`~`; as versões instaladas dependem do `package-lock.json`, não lido linha a linha) e `angular.json`.

## Informações confirmadas ✅
| Área | Tecnologia (faixa declarada) | Uso |
|---|---|---|
| Framework | Angular `^18.2` (CLI `^18.2.1`), TypeScript `~5.5.2`, RxJS `~7.8`, Zone.js `~0.14` | SPA com NgModules; componentes `standalone` só em parte (ex.: `ValidarAssinaturaOsComponent`) |
| Estado | `@ngrx/store`, `@ngrx/effects`, `@ngrx/store-devtools` `^18.1` | estado global e efeitos de chamadas HTTP |
| UI | `primeng ^17.18`, `primeicons`, `@angular/material ^18.2`, `@angular/cdk`, `bootstrap ^5.3`, `bootstrap-icons`, `@popperjs/core`, `@ng-select/ng-select` | tabelas, diálogos, toasts, selects, ícones |
| Editor de texto | `ckeditor5 ^44.1`, `ckeditor5-premium-features`, `@ckeditor/ckeditor5-angular ^9.1` | campo de texto rico (`CkeditorComponent`); a chave de licença no código é do tipo `GPL` |
| PDF | `ng2-pdf-viewer ^10.4` | visualização do PDF da OS |
| Autenticação | `@auth0/angular-jwt ^5.2`, `keycloak-js ^25.0` | leitura/expiração de JWT; `keycloak-js` só em código sem uso (ver [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]) |
| Formulários | `ngx-mask ^18` | máscaras de entrada |
| Feedback | `ngx-spinner ^17` | indicador global de carregamento |
| Testes | Karma `~6.4`, Jasmine `~5.2`, `karma-coverage` | ver [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]] |
| Build | `@angular-devkit/build-angular ^18.2` | `ng build`, configuração padrão `production` |
| Imagem de build | `node:20.19.2` (estágio de build) e `nginx:alpine` (execução), `npm ci --legacy-peer-deps` | `.docker/Dockerfile` |

Scripts npm: `start` (`ng serve`), `build`, `watch`, `test`.

## Inferências e limitações
- 🔶 `npm ci --legacy-peer-deps` indica conflitos de *peer dependencies* entre pacotes (não investigado). Ver [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]].
- Versões efetivamente instaladas e vulnerabilidades (`npm audit`) não foram verificadas.
- `ng build`/`ng test` não foram executados.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]] · [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
