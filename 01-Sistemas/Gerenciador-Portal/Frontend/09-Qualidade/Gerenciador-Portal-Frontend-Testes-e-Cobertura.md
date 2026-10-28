---
type: quality
aliases:
  - "Testes e cobertura — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
sources:
  - karma.conf.js
  - gulp/test.js
  - gulp/scripts.js
  - package.json
---
# Testes e cobertura — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Registrar a estratégia de testes e a análise estática do frontend.

## Evidências
`karma.conf.js`, `gulp/test.js`, `gulp/scripts.js`, `package.json`; busca por `describe(` em `src/` (sem resultados). Nada foi executado.

## Informações confirmadas
- ✅ **Infraestrutura existe**: `npm test` = `gulp test` → Karma (`singleRun`), Jasmine, `karma-jasmine-matchers`, `angular-mocks` e PhantomJS; relatórios HTML e de cobertura configurados.
- ✅ **Não há testes**: nenhum arquivo `*.spec.js` nem chamada `describe(` em `src/`; a cobertura efetiva é **nula**.
- ✅ **Análise estática**: `gulp lint` (`codeStaticAnalysis`, ESLint com `eslint-plugin-angular`) roda antes de `scripts` e de `test`, exceto com `--skip-lint`; o `Dockerfile` e o `npm run dev` usam `--skip-lint`. Vários controllers começam com `/*eslint-disable */`. Não há arquivo `.eslintrc` na raiz (❓ onde a configuração é lida).
- ✅ Não há teste e2e (Protractor aparece só como dependência `gulp-protractor`).

## Falhas e dependências
- PhantomJS e Karma 0.13 são antigos; não verificado se ainda rodam.
- Sem testes, o contrato com o backend (ver [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]) só é verificado à mão.

## Inferências e limitações
- 🔶 Os testes do backend também estão incompletos ([[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Testes-e-Cobertura|Testes do Backend]]).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Frontend/09-Qualidade/Gerenciador-Portal-Frontend-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Se o time quiser testes, começar pelos serviços `*Api.js` (puros, sem DOM).
