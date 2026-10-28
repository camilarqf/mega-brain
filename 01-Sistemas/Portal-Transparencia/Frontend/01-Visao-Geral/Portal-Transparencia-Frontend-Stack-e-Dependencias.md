---
type: reference
aliases:
  - "Frontend — stack e dependências"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
sources:
  - package.json
  - bower.json
  - Dockerfile
  - nginx.conf
  - src/app/index.module.js
---

# Frontend — stack e dependências

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Registrar a stack e as dependências relevantes do `portal-transparencia-frontend` (pasta local `PT2016_FrontEnd`).

## Evidências
Repositório `portal-transparencia-frontend`, branch `master`, commit `dca3e933`. Arquivos: `package.json`, `bower.json`, `Dockerfile`, `nginx.conf`, `src/app/index.module.js`.

## Informações confirmadas
| Item | Valor | Evidência |
|---|---|---|
| Framework | AngularJS **1.4.x** (`~1.4.2`); módulo raiz `portal` | `bower.json`, `index.module.js` |
| Roteamento | `ngRoute` (`$routeProvider`) nas rotas da aplicação; `ui-router` 0.2 também é carregado (`ui.router`) mas não é usado em `index.route.js` | `index.route.js` |
| UI | Bootstrap 3 (sass), `angular-strap`, `ui.bootstrap`, `font-awesome` 4.7, Material Design Iconic Font, `animate.css` | `bower.json` |
| Gráficos e mapas | `c3-angular`, `highcharts-dist` 4.2.7, Leaflet (`src/assets/scriptsleaflet`), `angularjs-gauge`, `gauge.js` | `bower.json`, pasta `src/assets` |
| Tabelas e formulários | `ng-table`, `ui-select`, `select2`, `ui-mask`/`ngMask`, `textAngular`, `ng-file-upload`, `angular-file-saver` | `bower.json`, `index.module.js` |
| Analítica | `angulartics` + `angulartics.google.analytics`; Google Tag (`gtag.js`) no `index.html` | `index.module.js`, `src/index.html` |
| Build | gulp 3.9 (o Dockerfile instala o gulp 4.0.2 global), `gulp-sass`, `gulp-ng-config`, `gulp-angular-templatecache`, `gulp-uglify`, `gulp-htmlmin` | `package.json`, `gulp/*.js`, `Dockerfile` |
| Testes | Karma 0.13 + Jasmine + `karma-phantomjs-launcher`; e2e com Protractor | `package.json`, `karma.conf.js`, `protractor.conf.js` |
| Lint | ESLint com `eslint-plugin-angular` (`.eslintrc`) | `.eslintrc`, `package.json` |
| Imagem de build | `node:6.11.3` | `Dockerfile` |
| Servidor estático | nginx: `try_files` com *fallback* para `/index.html` (SPA) | `nginx.conf` |
| Dependências npm de runtime | `angular-bootstrap-datetimepicker`, `angular-date-time-input`, `angularjs-gauge`, `owl.carousel` | `package.json` |

Outros fatos:
- O `Dockerfile` termina executando `gulp --profile ${profile} --skip-lint`; o perfil entra como `ARG profile`.
- O `.bowerrc` define registro interno (endereço omitido) e `strict-ssl: false`.

## Inferências e limitações
- 🔶 Versões de runtime (AngularJS 1.4, Node 6, PhantomJS 2, gulp 3) estão fora de suporte; riscos em [[01-Sistemas/Portal-Transparencia/Frontend/09-Qualidade/Portal-Transparencia-Frontend-Debitos-Tecnicos|Débitos técnicos]].
- ❓ O processo de empacotamento/implantação (pipeline) não está versionado: `Jenkinsfile.prod` foi removido no commit `2e8298ac` (2026-10-14) e não há outro arquivo de pipeline na árvore.
- Versões efetivamente instaladas (`bower_components/`, `node_modules/`) não foram comparadas com os manifestos.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Arquitetura-AngularJS|Arquitetura AngularJS]] · [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Build-e-Perfis-de-Ambiente|Build e perfis de ambiente]]
- Backend: [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Stack-e-Dependencias|Stack do Backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
