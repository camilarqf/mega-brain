---
type: reference
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - stack
  - dependencias
sources:
  - package.json
  - package-lock.json
  - Dockerfile
  - gulpfile.js
  - index.html
  - app/app.module.js
  - assets/lib
---

# Frontend SIC — stack e dependências

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Arquitetura: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Arquitetura|Arquitetura]]

## Objetivo
Listar tecnologias, bibliotecas e ferramentas de build do `participa-df-sic-frontend`.

## Evidências
Arquivos em `sources`, commit `5518a81`. Cabeçalhos de versão de `assets/lib/*` lidos só para AngularJS, `angular-route` e Bootstrap (cobertura `parcial`).

## Informações confirmadas
| Item | Valor | Evidência |
|---|---|---|
| Framework | ✅ AngularJS **1.5.8** (módulo `Ouv-DF`) | cabeçalho de `assets/lib/angular.min.js`; `app/app.module.js` |
| Roteamento | ✅ `angular-route` 1.3.15 (rotas por hash, `hashPrefix('')`) | `assets/lib/angular-route.min.js`; `app/app.routes.js` |
| UI | ✅ Bootstrap 3.3.6, jQuery 1.11.1, Material (ripples), Font Awesome, icofont | `assets/lib`, `assets/css` |
| Módulos AngularJS | ✅ `ngRoute`, `spinner`, `720kb.tooltips`, `ui.mask`, `checklist-model`, `ngSanitize`, `angularUtils.directives.dirPagination`, `angularTreeview`, `ui.multiselect`, `ngAutocomplete`, `ngCookies`, `exception`, `toastr`, `chart.js`, `ngFileUpload`, `infinite-scroll`, `cp.ngConfirm` | `app/app.module.js` |
| Bibliotecas versionadas em `assets/lib` | ✅ 40 arquivos `.js` (inclui `ol.js`, `gmaps.js`, `highcharts*`, `Chart.js`, `signalr.js`) copiados à mão, sem gerenciador de pacotes | `assets/lib` |
| Dependência npm de runtime | ✅ `@microsoft/signalr` `^6.0.0-preview` — 🔶 sem uso em `app/` | `package.json` |
| Build | ✅ Gulp **3** (`gulp-*`, `run-sequence`, `browser-sync`, `gulp-ng-config`, `gulp-rev`) | `package.json`, `gulpfile.js` |
| Scripts npm | ✅ `dev`, `homolog`, `prod`, `gulpv`; `test` é *stub* (`echo "Error: no test specified"`) | `package.json` |
| Imagem de build | ✅ `node:10.17.0` (estágio `builder`, `npm install` + `gulp ${profile}`, padrão `prod`) | `Dockerfile` |
| Imagem de execução | ✅ `nginx:alpine` com `nginx.conf` como *template* | `Dockerfile` |
| Linting | ✅ `htmlhint` em `devDependencies`, sem script nem configuração | `package.json` |
| Gráficos/mapas | 🔶 `Chart.js`/`angular-chart`, `highcharts`, `ol.js` e `gmaps` estão carregados mas sem uso encontrado em `app/` (`grep` por `ol.`, `gmaps`, `Chart`, `highcharts` não retornou código do SIC) | `assets/lib`, `app/` |

## Inferências e limitações
- 🔶 Gulp 3 e Node 10 estão fora de suporte; a execução do build em Node mais novo provavelmente falha (não testado).
- 🔶 O nome do pacote `OuvCidadania.Ui` e o módulo `Ouv-DF` indicam origem no front de Ouvidoria (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Stack-e-Dependencias|Stack do Frontend Ouvidoria]]).
- ❓ Versões das demais bibliotecas de `assets/lib` não foram lidas.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Perfis-e-Ambientes|Perfis-e-Ambientes]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/06-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Confirmar a versão de Node usada pelo time (o `Dockerfile` usa 10.17.0) e se as bibliotecas sem uso podem ser removidas. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
