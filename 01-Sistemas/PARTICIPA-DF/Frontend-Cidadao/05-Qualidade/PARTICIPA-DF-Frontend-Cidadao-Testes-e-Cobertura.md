---
type: quality
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: completa
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - participa-df
  - frontend-cidadao
  - testes
  - qualidade
sources:
  - karma.conf.js
  - tsconfig.spec.json
  - src/app/app.component.spec.ts
  - src/app/core/pipes/get-initials.pipe.spec.ts
  - src/app/core/pipes/order-by.pipe.spec.ts
  - src/app/pages/conta/historico-cpf-vinculado/historico-cpf-vinculado.component.spec.ts
  - src/app/static-pages
---

# Frontend Cidadão — testes e cobertura

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/08-Qualidade/PARTICIPA-DF-Backend-Testes-e-Cobertura|Testes do Backend]]

## Objetivo
Registrar a estratégia e a cobertura de testes automatizados do repositório.

## Evidências
Contagem de arquivos `*.spec.ts` e de `it(...)` no commit `d250804`. Testes **não foram executados** nesta análise.

## Informações confirmadas
- ✅ Ferramentas: Karma + Jasmine, `karma-coverage` configurado (relatório em `coverage/eou-df`); comando `ng test`.
- ✅ Existem **9 arquivos `.spec.ts`**, 11 casos `it(...)`: `AppComponent` (3), `GetInitialsPipe` (1), `OrderByPipe` (1), `HistoricoCpfVinculado` (1) e cinco páginas estáticas (1 cada: FAQ do Participa DF, Acesso à Informação, Participa DF, orientação de manifestação, termos de uso).
- ✅ Os títulos dos casos são os do gerador do Angular CLI: `should create` (6), `create an instance` (2, pipes) e, no `AppComponent`, `should create the app`, `should have as title 'eou-df'` e `should render title`. Cada página/pipe tem 1 expectativa.
- ✅ Nenhum teste cobre: serviços (`Api`, `AuthenticationService`), `AuthGuard`, interceptors, fluxos de registro, caixa de entrada, conta ou o mapa. Não há testes e2e (o README cita `ng e2e` sem pacote configurado).
- ✅ Não há teste de componente nos módulos `registro-manifestacao`, `registro-pedido`, `caixa-entrada`, `validacao` e `login`.

## Inferências e limitações
- 🔶 Cobertura efetiva muito baixa (percentual não medido). Os testes existentes parecem gerados e não foram mantidos junto com as mudanças (a `AppComponent` tem dependências HTTP e de modal).
- ❓ Se algum desses `.spec` ainda passa: precisa de `ng test` (Chrome).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Se aprovado, executar `ng test --watch=false --code-coverage` para medir ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]]).
