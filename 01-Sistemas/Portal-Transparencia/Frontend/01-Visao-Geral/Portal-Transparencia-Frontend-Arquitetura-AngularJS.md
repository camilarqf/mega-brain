---
type: architecture
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
tags:
  - portal-transparencia
  - frontend
  - arquitetura
  - angularjs
sources:
  - src/app/index.module.js
  - src/app/index.route.js
  - src/app/index.config.js
  - src/app/index.run.js
  - src/app/token-interceptor.js
  - src/app/components/compartilhado
---

# Frontend — arquitetura AngularJS

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Descrever a organização da SPA AngularJS: módulos, roteamento, camadas e pontos de configuração.

## Evidências
Commit `dca3e933`. Arquivos: `src/app/index.module.js`, `index.route.js`, `index.config.js`, `index.run.js`, `token-interceptor.js`, `config.js`, pasta `src/app/components/*` e `src/app/template/*`.

## Informações confirmadas
**Módulos.** O módulo raiz `portal` depende de `portal.config` (constantes por perfil), de módulos por área (`portal.despesa`, `portal.receita`, `portal.patrimonio`, `portal.convenio`, `portal.licitacao-contrato`, `portal.prestando-contas`), de `portal.acessibilidade`, `portal.pagina-inicial`, `portal.breadcrumb` e de bibliotecas (`ngRoute`, `ngResource`, `ui.bootstrap`, `mgcrea.ngStrap`, `ngTable`, `angulartics`, `ngFileUpload`, `textAngular`, `ngStorage`, `LocalStorageModule`, entre outras). Na prática quase tudo (225 declarações) é registrado em `angular.module('portal')`; os módulos por área têm poucas declarações próprias (22, 7, 5 …).

**Roteamento.** `index.route.js` (2170 linhas) usa `$routeProvider`: 103 rotas com `templateUrl` + `controller` (`controllerAs: "vm"`), 11 rotas `noLink` que redirecionam para `/` (só servem de rótulo ao *breadcrumb*) e `otherwise → /`. Há rotas comentadas (por exemplo `/servidores/tabela`, `/despesas/restos-a-pagar`, `/despesas/execucao-emendas`, `/despesas/acao`) cujos controllers continuam no repositório. Muitas rotas usam `resolve` para carregar dados antes da tela (listas de anos, filtros e `DataAtualizacaoService.buscarDataAtualizacao(<chave>)`). Catálogo de rotas por área: notas de módulo em [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice]].

**Camadas.**
- *Controllers* por tela (`components/<área>/*.controller.js`), com `controllerAs: vm` e injeção por `/** @ngInject */`.
- *Services* por área (`<área>.service.js`) que montam a requisição `$http` para `api.url + <caminho>`; ver [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]].
- *Diretivas e serviços compartilhados* em `components/compartilhado` (tabelas, filtros, cabeçalho, gráficos, topbar, rodapé, mapa de regiões administrativas, busca, pesquisa de satisfação, `RelatorioService` de exportação PDF/CSV, `PagingService`, `Util`).
- *Templates* HTML em `components/**` e `template/**`; o `gulp-angular-templatecache` gera `views.js` (módulo `portal`, raiz `app`).

**Configuração e execução.**
- `index.config.js`: *logs* de depuração ligados (`$logProvider.debugEnabled(true)`), barra de carregamento, formato de data `dd/MM/yyyy`, alertas no canto superior direito, `jcs-autoValidate` em `pt-br`.
- `index.module.js` (bloco `config`): zera os cabeçalhos *default* de `$http` e registra o interceptador `tokenInterceptor`.
- `token-interceptor.js`: gera um UUID por carga da página e o envia no cabeçalho `x-client-id` nas requisições cujo URL começa com `api.url`; expõe `window.PortalTransparenciaClient`.
- `index.run.js`: atualiza o *breadcrumb* em `$routeChangeSuccess`.
- `index.constants.js`: `moment` e `APP = { version: '1.0' }`.
- Constantes por perfil em `portal.config` (`api`, `apisuperbusca`, `apiGerenciador`, `caminhoImagens`, `caminhoArquivos`, `caminhoDadosAbertos`); ver [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Build-e-Perfis-de-Ambiente|Build e perfis]].

**Estado no cliente.** `localStorageService` guarda o tema e dados dos widgets de enquete/*todo*; `sessionStorage` controla o aviso (modal) para telas pequenas (< 1023 px). Não há login nem sessão de usuário no frontend.

## Inferências e limitações
- 🔶 O módulo `portal.config` é gerado por `gulp-ng-config` a partir de `config.json`, mas `src/app/config.js` **está versionado**; a versão do arquivo no commit analisado reflete o último perfil gerado, não necessariamente o de produção.
- 🔶 Existem controllers e templates de telas antigas (`/old` → `DashboardController`, `todo-widget`, `upload.controller.js` com `url: '#'`) que parecem herança do *template* original; sem evidência de uso em produção.
- Cobertura parcial: templates HTML, SCSS e diretivas de gráfico/mapa foram lidos por amostragem.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Stack-e-Dependencias|Stack]] · [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API do Backend]]
- Backend: [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura do Backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
