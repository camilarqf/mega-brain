---
type: architecture
aliases:
  - "SCI Frontend — arquitetura"
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
sources:
  - src/app/app.module.ts
  - src/app/app-routing.module.ts
  - src/app/store
  - src/app/core
  - src/app/components
---
# SCI Frontend — arquitetura

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Descrever a organização do código, a navegação e o uso de NgRx do `sci-frontend`.

## Evidências
- `src/app/app.module.ts`, `app-routing.module.ts` e as pastas `core`, `store`, `components`, `pages`, `auth`, `public`.
- 162 arquivos `*.component.ts`, 165 templates HTML e cerca de 460 arquivos `.ts` em `src`.

## Informações confirmadas
### Estrutura de pastas
| Pasta | Conteúdo |
|---|---|
| `src/app/auth` | login e acesso negado (`AuthModule`, rota `/auth`) |
| `src/app/pages` | telas por área: `home`, `demanda`, `denuncias`, `jad`, `pip`, `encaminhados`, `gerenciador`, `gestao`, `administracao` (`PagesModule`, rota `/pages`, carregamento sob demanda) |
| `src/app/public` | rota pública `/validacao` (`PublicModule`) |
| `src/app/components` | `layout` (sidenav, modais, botões, uploads, filtros e cabeçalhos de caixa de entrada), `semantic` (contêineres) e `shared` (busca de envolvidos, editor de texto, contador de caracteres) |
| `src/app/core` | enums, fábricas de `HttpParams` (`factory/build-filtro-*`), guards, interceptors, modelos, view-models, serviços utilitários (`toast`, `download`, `global-error`, `uuid`) e validadores |
| `src/app/store` | `actions`, `effects`, `reducers`, `selectors` e `services` (clientes HTTP) |

### Padrões
- ✅ Um `NgModule` com roteamento próprio por área, carregado com `loadChildren`. Rotas e perfis: [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Rotas-e-Telas|Rotas e telas]].
- ✅ Clientes HTTP em `store/services/*.service.ts` (25 serviços), todos com `environment.apiUrl` como base. Lista: [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas de API]].
- ✅ NgRx registrado em `AppModule` com reducers e efeitos para usuário, JAD, demanda, assunto, unidade, pessoa (física e jurídica), análise, arquivo, assinatura, conduta, origem da denúncia, recomendação, situação funcional, tipificação, tipo de documento e processos da pessoa. `StoreDevtools` só quando `environment.production` é falso.
- ✅ `clearStateMetaReducer` zera todo o estado NgRx na ação `logoutSuccess`.
- ✅ Três interceptors em `HTTP_INTERCEPTORS`: `AuthInterceptor` (cabeçalho `Authorization: Bearer`), `LoadingInterceptor` (spinner com contador de requisições pendentes) e `ErrorInterceptor` (normaliza o erro; trata 401/403). Detalhe em [[01-Sistemas/SCI/Frontend/08-Seguranca/SCI-Frontend-Seguranca-e-Sessao|Segurança e sessão]].
- ✅ Nem toda tela passa pela store: `denuncias` e a maior parte do PIP chamam os serviços diretamente.
- ✅ Filtros das caixas de entrada ficam em `sessionStorage` (`caixa-entrada-filtro.service.ts`).
- ✅ Avisos por `ToastService` (PrimeNG) e `NotificacaoService`; erros globais por `GlobalErrorService` e `GlobalErrorComponent`.

## Inferências e limitações
- 🔶 A mistura de NgRx e chamadas diretas indica padrão não uniforme; decisão de projeto não registrada.
- Templates HTML, SCSS e a maior parte dos formulários foram lidos por amostragem.

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Stack-e-Dependencias|Stack]] · [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Perfis-e-Ambientes|Perfis e ambientes]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
