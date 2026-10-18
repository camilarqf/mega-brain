---
type: architecture
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - arquitetura
  - angularjs
sources:
  - index.html
  - app/app.module.js
  - app/app.routes.js
  - app/api.service.js
  - app/token-auth-interceptor.js
  - app/exception/app-exception-module.js
  - app/spinner/spinner.js
  - app/nav/nav-ctrl.js
  - app/shared/storage-service.js
  - app/upload/upload-arquivos-directive.js
---

# Frontend SIC — arquitetura

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Stack: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Stack-e-Dependencias|Stack-e-Dependencias]]

## Objetivo
Descrever a estrutura e os padrões do código da SPA AngularJS.

## Evidências
Arquivos em `sources`, commit `5518a81`. As telas (`*.html`) foram lidas só por amostra.

## Informações confirmadas

### Estrutura
- ✅ Aplicação única `Ouv-DF` (`var app = angular.module('Ouv-DF', [...])`), sem módulos por funcionalidade: controllers, serviços e diretivas se registram direto em `app`. No build, os `app/**/*.js` são **concatenados** (`scripts.js`) e carregados por `<script>` em `index.html`; a ordem relevante é definida em `gulpfile.js` (`app.module.js`, `app.routes.js`, configuração de API, interceptor, storage, `views`).
- ✅ Pastas de `app/` (75 arquivos): `caixa-entrada`, `registro/por-operador`, `conta/{pessoa-fisica,pessoa-juridica,visualizar-conta}`, `gerencial/{feriado,operadorSIC,perfilSIC,unidade}`, `super-busca`, `auth`, `acesso-negado`, `nav`, `upload`, `shared`, `exception`, `spinner`. Cada tela é um par `*.html` + controller (`controllerAs: 'vm'` nas rotas; `$scope` em `pedido-por-operadorCtrl.js`).
- ✅ Templates em `app/**/*.html`; no build `gulp viewsCacheSetup` os embute em `app/views-dist.js` (`$templateCache`, módulo `Ouv-DF`), arquivo gerado e versionado.
- ✅ `index.html` contém a barra de navegação (`navCtrl`), o `ng-view`, três modais globais (alternar unidade, exceção 500, *spinner*) e a diretiva `custom-exception`.

### Camada de acesso à API
- ✅ Serviço `Api` (`app/api.service.js`) com `GET`, `POST` (prefixam `configService.urlApi`) e `GETe`, `POSTe` (URL absoluta). Todas as chamadas são `$http` com `Content-Type: application/json`; não há camada de serviços por domínio — **os controllers chamam `Api` direto** (97 chamadas em `app/`). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/04-API-e-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]].
- ✅ `configService` (constante `urlApi`) vem de `api.config.json` por ambiente via `gulp-ng-config`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Perfis-e-Ambientes|Perfis-e-Ambientes]].

### Interceptores `$http` (registrados em `app.module.js` e módulos auxiliares)
| Interceptor | Função | Arquivo |
|---|---|---|
| `tokenAuthInterceptor` | adiciona cabeçalho de aplicação e `Authorization: Bearer` às URLs que contêm `urlApi`; em 401/403 busca `configuration/front-end-urls` e redireciona para o `Login` | `app/token-auth-interceptor.js` |
| `exceptionInterception` | remove erros anteriores a cada requisição; em 401/403 vai para `/`; em 400 transmite `Notifications`/`error`; em 500 abre o modal de erro | `app/exception/app-exception-module.js` |
| `spinnerInterceptor` | contador de requisições abertas; mostra/oculta o modal de carregamento; `noSpinner` em `params` suprime | `app/spinner/spinner.js` |

- ✅ `app.module.js` zera `$httpProvider.defaults.headers.{common,post,put,patch}`.

### Estado e comunicação entre componentes
- ✅ Sem *store* central. Estado de sessão: token em `localStorage` (`tokenStorage`) e o usuário/permissões em `navCtrl` (`vm.currentUser`, `vm.permissoes`). Comunicação por eventos de `$rootScope` (`authenticate`, `confirmAuth`, `acessoNegadoEvt`, `badRequest`, `removeException`, `error500`, `loader_show`, `loader_hide`).
- ✅ `storageService` (`localStorage`, com *fallback* para `$cookieStore`) guarda o último filtro aplicado da caixa de entrada.
- ✅ Componentes reutilizáveis: diretivas de formulário `dirInputForm`, `dirSelectForm`, `dirMultiselectForm`, `dirTextAreaForm` (em `app/shared`), `uplArquivos` (envio de anexos) e `uplPedido` (lista, download e remoção de anexos do pedido), `ngEnter`.

### Fluxo de navegação
- ✅ O menu (`index.html`) é controlado por `vm.isAuth` e pelas permissões de `operador-sic/consultar-permissoes` (item **Gerenciar** com a lista `PermissoesDeGerenciamento`, vindas do backend). As rotas **não têm `resolve` nem guarda**: a proteção real depende do backend (401/403). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]].

## Inferências e limitações
- 🔶 Tratamento de erro misto: `tokenAuthInterceptor` e `exceptionInterception` reagem ambos ao 401/403 (redireção ao login e `$location.path('/')`); o efeito combinado não foi testado.
- 🔶 `$rootScope.$on(...)` em `customException` e `error500` é registrado sem remoção; não foi avaliado vazamento.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Rotas-e-Telas|Rotas-e-Telas]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/06-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]] · Equivalente no front de Ouvidoria: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Arquitetura|Arquitetura do Frontend Ouvidoria]]

## Pendências e próximo passo
- Ler os templates de conta/registro e as diretivas `shared/` com mais profundidade (lote 6 sugerido no [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Registro-de-Analise|Registro-de-Analise]]).
