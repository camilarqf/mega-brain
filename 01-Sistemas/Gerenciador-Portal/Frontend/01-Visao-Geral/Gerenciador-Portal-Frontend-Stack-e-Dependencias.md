---
type: reference
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - frontend
  - stack
  - angularjs
sources:
  - package.json
  - bower.json
  - .bowerrc
  - .tool-versions
  - Dockerfile
  - src/app/index.module.js
---
# Stack e dependências — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Registrar a tecnologia, as bibliotecas e o ferramental de build do `gerenciador-portal-frontend`.

## Evidências
`package.json`, `bower.json`, `.bowerrc`, `.tool-versions`, `Dockerfile`, `src/app/index.module.js`. Nada foi instalado nem executado; as versões são as declaradas, não as resolvidas.

## Informações confirmadas
| Item | Valor declarado |
|---|---|
| Framework | AngularJS `~1.6.3` (módulo raiz `gerenciadorPortal`), `angular-route` `~1.4.2` e `angular-ui-router` `~0.2.15`; o roteamento ativo usa `$routeProvider` |
| UI | Bootstrap 3 (`bootstrap` e `bootstrap-sass`), `angular-strap` 2.2.1 (modais `$modal`), `angular-material`, `ng-table`, `angularUtils-pagination`, `ui-select`, `textAngular`, `AngularJS-Toaster` (avisos), `angular-loading-bar` |
| Upload | `ng-file-upload` 12.2.13 (serviço `Upload`) e `angular-file-upload` (módulo `angularFileUpload`) |
| Armazenamento no navegador | `ngStorage` (`$localStorage`) e `angular-local-storage` |
| Outras | jQuery 2.1, lodash e underscore, moment, Highcharts e c3, `angulartics`, `ngMask`, `angular-ui-mask`, ~70 dependências Bower no total |
| Build | Gulp 3 (`gulp-ng-config`, `gulp-sass`, `gulp-uglify`, `gulp-angular-templatecache`…) e Bower (`bower_components`) |
| Runtime de build | Node `6.11.3` (`.tool-versions` e `FROM node:6.11.3` no `Dockerfile`) |
| Testes | Karma + Jasmine + PhantomJS (ver [[01-Sistemas/Gerenciador-Portal/Frontend/07-Qualidade/Gerenciador-Portal-Frontend-Testes-e-Cobertura|Testes]]) |
| Dependências de `package.json` em runtime | `angular-bootstrap-datetimepicker`, `angular-date-time-input`, `fancy-log` |

- ✅ O `.bowerrc` desliga a verificação de TLS (`strict-ssl: false`) e aponta o registro Bower público.
- ✅ Várias dependências Bower são URLs Git sem versão fixa (`angular-cookies`, `angular-touch`, `angular-sanitize`, `angular-messages`, `angular-aria`, `angular-resource`, `angular-material` com `^`), e o `Dockerfile` executa `bower update`.
- ✅ O `angular-bootstrap` está em `^2.4.0` enquanto o código usa `$modal` do `angular-strap` (o módulo `ui.bootstrap` está comentado em `index.module.js`).

## Inferências e limitações
- 🔶 AngularJS e Node 6 saíram de suporte há muito tempo; isso é fato externo ao repositório, e o risco está em [[01-Sistemas/Gerenciador-Portal/Frontend/07-Qualidade/Gerenciador-Portal-Frontend-Debitos-Tecnicos|Débitos técnicos]].
- ❓ Versões efetivamente instaladas (sem `bower_components` no repositório).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Build-e-Perfis-de-Ambiente|Build e perfis]] · [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Stack-e-Dependencias|Stack do Backend]]

## Pendências e próximo passo
- Nenhum além das pendências do [[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Pendencias|controle]].
