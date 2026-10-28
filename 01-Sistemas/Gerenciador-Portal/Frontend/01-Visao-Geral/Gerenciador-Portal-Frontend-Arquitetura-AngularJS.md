---
type: architecture
aliases:
  - "Arquitetura AngularJS — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/app/index.module.js
  - src/app/index.route.js
  - src/app/token-interceptor.js
  - src/app/components
  - src/index.html
---
# Arquitetura AngularJS — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Descrever a estrutura da SPA: módulos, roteamento, camadas e padrões repetidos.

## Evidências
`index.module.js`, `index.route.js`, `token-interceptor.js`, `index.constants.js`, `diretivas/ngEnter.js`, `components/*` (22 arquivos `.js`, ~2,2 mil linhas) e `index.html`.

## Informações confirmadas
### Módulos
- ✅ Módulo raiz `gerenciadorPortal` depende de **um módulo por funcionalidade**: `gerenciadorPortal.arquivo`, `.carga`, `.login`, `.imagem`, `.palavra`, `.orgao`, `.textos-portal`, `.exclusoes` (medida protetiva), `.diretivas` (`ngEnter`) e `.config` (gerado, ver [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Build-e-Perfis-de-Ambiente|Build e perfis]]). Cada módulo é declarado em um arquivo `*.module(s).js` de uma linha.
- ✅ Constantes injetáveis geradas por perfil: `api`, `apiPortal`, `apiSuperbusca`, `route`, `caminhoArquivos`, `caminhoImagens`; e `APP` (`version: '1.0'`).

### Camadas por funcionalidade (padrão repetido em todas as pastas de `components/`)
| Camada | Arquivo | Papel |
|---|---|---|
| View | `*.html` | template parcial carregado pelo `ngRoute`; cada tela inclui `navbar.html` por `ng-include` |
| Controller | `*Ctrl.js` | `controllerAs: 'vm'`; estado da tela, avisos (`toaster`), modais (`$modal`/jQuery) |
| Acesso à API | `*Api.js` (`service`/`factory`) | monta o `$http` com `api.url + caminho`; devolve a *promise* |

- ✅ Os controllers chamam o serviço de API, nunca `$http` direto, exceto os **uploads**, que usam `Upload.upload` (ng-file-upload) com URL montada no controller ([[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]).
- ✅ Não há camada de *store* nem serviço de estado compartilhado: o usuário logado é lido direto de `$localStorage.usuario` nos controllers e em `exclusoesAPI`.

### Roteamento (`$routeProvider`, modo `#!`)
`/` → `LoginController`; `/arquivo`, `/carga-portal`, `/imagem-portal`, `/palavras-chave`, `/editar-palavra`, `/orgaos-lai`, `/textos-portal`, `/exclusoes-medida-protetiva`; `otherwise` → `/`. Detalhe por tela nas notas de módulo.
- ✅ **Não há guarda de rota** (nenhum `resolve`, `$routeChangeStart` de autenticação nem bloco `run`); qualquer rota abre sem login. As telas que usam `$localStorage.usuario.login` falham em tempo de execução se o usuário não existir ([[01-Sistemas/Gerenciador-Portal/Frontend/08-Seguranca/Gerenciador-Portal-Frontend-Seguranca-e-Sessao|Segurança e sessão]]).
- ✅ Existe só o `$routeProvider`; `ui.router` é carregado, mas nenhum `$stateProvider` foi lido.

### Configuração do `$http` (`index.module.js`)
- ✅ Esvazia os cabeçalhos padrão (`common`, `post`, `put`, `patch`) e registra o interceptor `tokenInterceptor` (envia `x-client-id`; ver [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Integracao-API-Backend|Integração com o Backend]]). O `responseError` só repassa a rejeição: **não trata 401/403**.
- ✅ `errorOnUnhandledRejections(false)`: rejeições sem `catch` não geram erro no console.

### Padrões de UI
- ✅ Avisos por `toaster.pop` (5 s), confirmações por `confirm()` nativo (palavras-chave, órgãos, medida protetiva), paginação por `dirPagination`, modais do `angular-strap` (imagens) e do Bootstrap por jQuery (`$('#…').modal`) nas telas de arquivo e carga.

## Inferências e limitações
- 🔶 A mistura de jQuery com AngularJS nos controllers (`$('#modal-arquivo')`, `$('.modal-backdrop').remove()`) reflete código herdado; ver [[01-Sistemas/Gerenciador-Portal/Frontend/09-Qualidade/Gerenciador-Portal-Frontend-Debitos-Tecnicos|Débitos técnicos]].
- ❓ Estilos (`index.scss`, `login.css`) e HTML não foram lidos em detalhe.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Stack-e-Dependencias|Stack]] · [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Arquitetura-em-Camadas|Arquitetura do Backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Pendencias|pendências]].
