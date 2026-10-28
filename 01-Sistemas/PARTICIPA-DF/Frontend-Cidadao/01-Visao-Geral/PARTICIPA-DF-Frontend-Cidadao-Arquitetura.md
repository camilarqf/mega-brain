---
type: architecture
aliases:
  - "Frontend Cidadão — arquitetura"
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
sources:
  - src/app/app.module.ts
  - src/app/app-routing.module.ts
  - src/app/pages/pages.module.ts
  - src/app/core/services/api.service.ts
  - src/app/core/interceptors/request.interceptor.ts
  - src/app/core/interceptors/jwt.interceptor.ts
  - src/app/core/interceptors/loading.interceptor.ts
  - src/app/core/interceptors/exception-interceptor.ts
  - src/app/layout/components/layout.module.ts
---

# Frontend Cidadão — arquitetura

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]]

## Objetivo
Descrever a estrutura da SPA Angular: módulos, carregamento, camada de acesso à API, interceptors e padrões de estado.

## Evidências
Arquivos em `sources`, commit `d250804`. Cobertura `parcial`: lidos os módulos raiz, o `core` e amostras de páginas; nem todo componente foi lido.

## Informações confirmadas

### Estrutura
```
src/app
├── core/        enums, interceptors, models, pipes, services (Api, auth, usuário, loading, eventsFromException)
├── layout/      componentes visuais reutilizáveis (botão, input, modal, upload, mapa OpenLayers, mensagens)
├── pages/       telas por área (module + routing por área, com lazy loading)
└── static-pages/ páginas informativas (FAQ, termos de uso, "o que é", orientações)
```
- ✅ O `AppModule` importa `LayoutModule`, `HttpClientModule`, `NgbModule` e `AppRoutingModule`. Os dois grupos de rotas raiz (`''` e `pages`) carregam `PagesModule`; `static` carrega `StaticPagesModule`, ambos por `loadChildren`.
- ✅ Cada área de `pages/` tem módulo e routing próprios, carregados sob demanda (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-Modulos/PARTICIPA-DF-Frontend-Cidadao-Rotas-e-Telas|Rotas-e-Telas]]).
- ✅ O `RouterModule.forRoot` usa `anchorScrolling: 'enabled'` e `scrollOffset: [0, 64]`; roteamento sem `useHash` (URLs de path).

### Acesso à API
- ✅ Toda chamada ao backend passa pela classe `Api` (`core/services/api.service.ts`), com `GET`, `POST`, `Download` (POST com `Accept: application/pdf` e `arraybuffer`) e `GET_E`/`POST_E` para URLs externas (usadas só pelo mapa). O prefixo vem de `environment.apiUrl`.
- ✅ O parâmetro `spinner` vira o cabeçalho HTTP `spinner: "true|false"`, lido pelo `LoadingInterceptor`.
- ✅ Catálogo das chamadas: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas-de-API]].

### Interceptors registrados no `AppModule` (ordem)
| Ordem | Classe | Efeito |
|---|---|---|
| 1 | `RequestInterceptor` | Limpa as mensagens de erro anteriores. Em erro: status `0` → mensagem "A conexão com o servidor falhou"; `400` → monta `BadRequest` (`ExceptionType`, `Notifications`, `ExceptionDetails`) e emite; `500` → emite `Message` para o modal de erro e registra `response.error` no console. |
| 2 | `JwtInterceptor` | Se há `_userData` no `localStorage`, adiciona `Authorization: Bearer <token>`. |
| 3 | `LoadingInterceptor` | Liga/desliga o indicador de carregamento por URL, salvo se `spinner: false`. |

- ✅ `ExceptionInterceptor` existe, mas **não** está registrado em nenhum módulo (código morto; só registra `err.error.Errors` no console).

### Estado entre telas
- ✅ Rascunhos e credenciais ficam em `localStorage`, por serviços "state manager": `manifestacao-store`, o rascunho do pedido e `usuario-store`; ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/08-Seguranca/PARTICIPA-DF-Frontend-Cidadao-Seguranca-e-Sessao|Seguranca-e-Sessao]].
- ✅ Passagem de dados entre telas do fluxo de conta por serviços em memória (`TrocaDadosService`, `UsuarioService.setLoginUsuario`) e por `queryParams` (`returnUrl`, `modoValidacao`, `token`).
- ✅ Comunicação de mensagens de erro por `EventsExceptions` (EventEmitter) e do menu de registro por `RegistroManifestacaoNavigateManager`.

### Shell da aplicação (`AppComponent`)
- ✅ No início chama `security/is-auth`; se autenticado, lê `configuration/front-end-urls` e `v2/usuario` (`OperadorSicAtivo`, `OperadorSoAtivo`).
- ✅ Métodos `navigateToOuv` e `navigateToSic` (login assistido por sessão) e `setUpAnalytics` (envia `page_path` ao `gtag` a cada navegação). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/08-Seguranca/PARTICIPA-DF-Frontend-Cidadao-Seguranca-e-Sessao|Seguranca-e-Sessao]].

## Inferências e limitações
- 🔶 `PagesModule` é carregado em `''` e em `pages`; por isso as mesmas telas respondem com e sem o prefixo `/pages`. Há links nos dois formatos no código.
- ❓ Não foi lida a lógica de todos os componentes de `layout/`.

## Relacionamentos
- Backend: [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura do Backend]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Stack-e-Dependencias|Stack-e-Dependencias]]

## Pendências e próximo passo
- Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]].
