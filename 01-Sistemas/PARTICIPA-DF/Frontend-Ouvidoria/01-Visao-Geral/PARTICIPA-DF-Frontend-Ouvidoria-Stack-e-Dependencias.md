---
type: reference
aliases:
  - "Frontend Ouvidoria — stack e dependências"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
sources:
  - package.json
  - package-lock.json
  - packages.config
  - gulpfile.js
  - Dockerfile
  - Dockerfile.dev
  - docker-compose.yml
  - .tool-versions
  - index.html
  - app/app.module.js
  - assets/lib
---

# Frontend Ouvidoria — stack e dependências

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Arquitetura: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Arquitetura|Arquitetura]] · Ambientes: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Objetivo
Listar linguagem, framework, bibliotecas e ferramentas de build do frontend de Ouvidoria.

## Evidências
Arquivos em `sources`, commit `9d8ecdb`. O `node_modules` não existe na cópia analisada; versões vêm de `package.json` (faixas) e do que está versionado em `assets/lib`.

## Informações confirmadas

### Aplicação
| Item | Valor | Evidência |
|---|---|---|
| Framework | AngularJS 1.x (módulo `Ouv-DF`; `ngRoute`, `ngSanitize`, `ngCookies`) | `app/app.module.js`; `assets/lib/angular.min.js` |
| Versão do AngularJS | ❓ não lida do cabeçalho do `angular.min.js`; `packages.config` lista `angularjs 1.5.8` (arquivo legado de projeto .NET) | `packages.config` |
| UI | Bootstrap 3.x (`bootstrap.min.js/css`), `ui-bootstrap-tpls-1.1.0`, jQuery 1.11.1, Material (ripples), `toastr`, `angular-confirm`, `ng-file-upload`, `dirPagination`, `ngAutocomplete`, `massautocomplete`, `mask`, `checklist-model`, `ng-infinite-scroll` | `assets/lib/*`, módulos em `app.module.js` |
| Gráficos | Highcharts (+ 3d, more, treemap, solid-gauge) e `Chart.js`/`angular-chart` | `assets/lib/*` |
| Mapas | OpenLayers (`ol.js`), `gmaps.js`, `jquery.geocomplete` | `assets/lib/*`, `app/open-street-map/*` |
| Tempo real | `@microsoft/signalr` (dependência em `package.json` e `assets/lib/signalr.js`) | 🔶 sem uso encontrado em `app/` |
| Ícones/fontes | Font Awesome 4, icofont, Linearicons | `assets/css`, `assets/webfonts` |

Bibliotecas de terceiros ficam **versionadas** em `assets/lib` e `assets/css` (não vêm de gerenciador de pacotes); só `@microsoft/signalr` é dependência de produção no `package.json`.

### Build e ferramentas
| Item | Valor |
|---|---|
| Build | Gulp 3 (`gulp ^3.9.1`) com `run-sequence`; tarefas `dev`, `homolog`, `prod` (scripts `npm run dev/homolog/prod`) |
| Plugins | `gulp-ng-config` (gera `app/api.config.js` a partir de `api.config.json`), `gulp-angular-templatecache` (gera `app/views-dist.js`), `gulp-concat`, `gulp-minify`, `gulp-clean-css`, `gulp-rev`/`gulp-rev-replace`, `gulp-html-replace`, `browser-sync`, `htmlhint` |
| Saída | `public/build` (dev) e `public/dist` (homolog/prod); `public/` está no `.gitignore` |
| Contêiner | `Dockerfile` e `Dockerfile.dev` com `node:10.17.0`, `gulp` global; `docker-compose.yml` expõe as portas 3000 e 3001 |
| Teste | nenhum (`npm test` é um `echo` de erro) — ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Testes-e-Cobertura|Testes-e-Cobertura]] |

### Versão do Node (inconsistente)
- `README.md` e `Dockerfile*`: Node 10 (`10.17.0`).
- `.tool-versions`: `nodejs 6.17.1`.
- ✅ As três fontes divergem; o build do pipeline usa o `Dockerfile` (Node 10).

## Inferências e limitações
- 🔶 `packages.config`, `Properties/AssemblyInfo.cs` e `Properties/PublishProfiles/*.pubxml` vêm de um projeto Visual Studio/.NET antigo (nome do pacote `OuvCidadania.Ui`); hoje o build real é o Gulp.
- 🔶 AngularJS 1.x está sem suporte oficial desde 2022 (conhecimento externo ao repositório); ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Débitos técnicos]].
- Cobertura `parcial`: cabeçalhos de versão dos arquivos de `assets/lib` não foram lidos.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Arquitetura|Arquitetura]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Stack-e-Dependencias|Stack do Frontend Cidadão]] (Angular 13, para comparação)

## Pendências e próximo passo
- Confirmar a versão real do AngularJS e do Node usada no pipeline; ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
