---
type: architecture
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - arquitetura
  - ngrx
sources:
  - src/main.ts
  - src/app/app.module.ts
  - src/app/app-routing.module.ts
  - src/app/pages/pages.module.ts
  - src/app/pages/pages-routing.module.ts
  - src/app/components/layout/layout.module.ts
  - src/core/store/reducers/index.ts
  - src/core/services/interceptor/*.ts
---

# Arquitetura — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Stack-e-Dependencias|Stack-e-Dependencias]], [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]], [[01-Sistemas/SICI/Frontend/05-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]], [[01-Sistemas/SICI/Frontend/04-API-e-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]]

## Objetivo
Descrever a estrutura de pastas, a composição de módulos, o estado global (NgRx) e a cadeia de interceptors do frontend.

## Evidências
Arquivos listados em `sources`. Leitura estática; componentes de tela grandes (por exemplo `ordem-servico-cadastrar`, 1607 linhas) foram lidos por trechos.

## Informações confirmadas ✅
### Estrutura
| Pasta | Conteúdo |
|---|---|
| `src/app/auth` | módulo lazy `AuthModule` com a tela de login |
| `src/app/pages` | telas por área: `acao-controle`, `ordem-servico`, `gestao-subci`, `home`, `acesso-negado`; cada área é um módulo lazy com roteamento próprio |
| `src/app/components/layout` | componentes de apresentação reutilizáveis (`LayoutModule`): barra superior, sidenav, header, botões, modais de envio, devolução, cancelamento e exclusão, `collapse-fase`, `assinatura-autenticacao`, pipe `enum-label` |
| `src/app/components/shared` | `SharedModule`: `ckeditor`, `contador-caracteres`, `template-editor`, diretiva `autosize-textarea` |
| `src/core/services` | serviços HTTP, autenticação (`auth/`), interceptors (`interceptor/`), assinatura em popup, utilitário de hash do PDF |
| `src/core/store` | `actions`, `effects`, `reducers`, `selectors` por área (ação de controle, cadastros auxiliares, OS, OS genérica, gestão SUBCI, auditor-perfil, auth) |
| `src/core/models`, `src/core/view-models`, `src/core/enums` | contratos de dados, formas do estado NgRx e enums (status/modelo de OS, tipo e natureza de ação) |
| `src/environments`, `src/styles` | configuração por ambiente e estilos SCSS por área |

### Composição
- `main.ts` inicializa `AppModule` (NgModule). `AppComponent` contém só `router-outlet`, `p-toast` (PrimeNG) e `ngx-spinner`.
- `AppRoutingModule` define rotas públicas, redirecionamentos de URLs antigas para `pages/home/**` e `pages` com lazy load protegido por `AuthGuard` (detalhe em [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]]).
- `HomeComponent` é um *shell* (`app-sidenav` + `app-barra-superior` + `router-outlet`); as áreas entram como rotas filhas de `pages/home`.
- A camada visual usa PrimeNG (tabelas, diálogos via `DialogService`), Angular Material (snack bar, ícones) e Bootstrap.

### Estado global (NgRx)
- `provideStore` em `AppModule` registra 13 chaves: `acoesControle`, `acaoControle`, `areaExecutora`, `unidadeAuditoriaInterna`, `unidadesAuditadas`, `programaGoverno`, `objetivoPpa`, `ordemServico`, `auditor`, `auth`, `gestaoSubci`, `assinatura`, `ordemServicoGenerica`. As chaves `acoesControle` e `acaoControle` usam o **mesmo** reducer.
- Efeitos registrados em `provideEffects`: `AcaoControle`, `OrdemServico`, `Auditor`, `AreaExecutora`, `UnidadeAuditoriaInterna`, `UnidadesAuditadas`, `ProgramaGoverno`, `ObjetivoPpa`, `GestaoSubci` e `OrdemServicoGenerica`. `AssinaturaEffects` (validação de assinatura) está registrado só em `EffectsModule.forRoot`.
- Padrão: componente despacha *action* → *effect* chama o serviço HTTP → reducer atualiza o estado → seletor alimenta a tela. Parte das telas também chama serviços diretamente (por exemplo `alterarStatusOs` em `acao-controle-os`, `visualizar-pdf`).
- O perfil do usuário (`auth`) é preenchido pelo `AuthService` ([[01-Sistemas/SICI/Frontend/02-Fluxos/SICI-Frontend-Fluxo-Autenticacao|Fluxo-Autenticacao]]).

### Interceptors (ordem de registro em `AppModule`)
1. `HttpTokenService`: anexa `Authorization: Bearer` quando há token válido e a URL é da própria origem ou da API; ignora `/auth/login` e `/assets/`.
2. `AuthErrorInterceptor`: `401` → `logout(false)` e navegação para `/login`; no `POST /auth/login`, converte erros em mensagens (`Credenciais inválidas.` / `Não foi possível autenticar no momento.`).
3. `GlobalErrorInterceptor`: só registra no console falhas de rede e status HTTP.
4. `LoadingInterceptor`: mostra/oculta o spinner global por contador de requisições (cabeçalho `skip-spinner` desativa).

## Inferências e limitações
- 🔶 `AppModule` também importa `StoreModule.forRoot(reducers)` (que declara só `ordemServico`) e `EffectsModule.forRoot([...])`, além de `provideStore`/`provideEffects`: registro duplicado do mesmo reducer/efeitos. Efeito em dobro não foi observado (nenhuma execução). Registrado em [[01-Sistemas/SICI/Frontend/06-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]].
- Cobertura parcial: templates HTML e SCSS foram lidos só por amostragem; lógica interna de `ordem-servico-cadastrar`/`atualizar` e dos reducers não foi lida linha a linha.

## Relacionamentos
- Segurança: [[01-Sistemas/SICI/Frontend/05-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]] · Módulos: [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Acao-de-Controle|Acao-de-Controle]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-OS-Generica|OS-Generica]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Gestao-SUBCI-e-Perfis|Gestao-SUBCI-e-Perfis]]
- Backend (hexagonal): [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Arquitetura-Hexagonal|Arquitetura do Backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
