---
type: quality
aliases:
  - "Frontend — testes e cobertura"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
sources:
  - karma.conf.js
  - protractor.conf.js
  - e2e/main.spec.js
  - gulp/test.js
  - src/app
---

# Frontend — testes e cobertura

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Descrever a estratégia de testes existente e as áreas sem cobertura.

## Evidências
Commit `dca3e933`. `karma.conf.js`, `protractor.conf.js`, `gulp/test.js`, `e2e/main.spec.js`, 28 arquivos `*.spec.js` em `src/app`. **Os testes não foram executados** nesta análise.

## Informações confirmadas
- ✅ **Unitários**: Karma 0.13 + Jasmine + `jasmine-matchers`, executados com PhantomJS; templates via `ng-html2js`; relatórios `progress`, `verbose` e `coverage` (HTML). Comandos: `gulp test`, `gulp test:auto`.
- ✅ **28 specs** distribuídos por: acessibilidade (módulo, `fontResize`, `highContrast`), breadcrumb (2), página inicial (4, carrossel de vídeo), enquete, paginação, `DataAtualizacaoService`, `index.run`, despesas (5: consulta dinâmica, nota de empenho, nota de lançamento, ordem bancária, por agrupador), receitas (1), servidores (6), prestando contas (3).
- ✅ **E2E**: Protractor com 1 arquivo (`e2e/main.spec.js`, título da página e cliques em botões da home, com `browser.sleep(3000)` e URL fixa `localhost:3000`).
- ✅ **Sem testes** em: orçamento, licitações e contratos, convênios, patrimônio, super busca, quadros temáticos, acesso à informação, `RelatorioService`, interceptador, `ArquivoUrlService` e a maior parte dos serviços de área.
- ✅ Lint: ESLint (`eslint:recommended` + `eslint-plugin-angular`); o `Dockerfile` e `npm run dev` usam `--skip-lint`.

## Inferências e limitações
- 🔶 PhantomJS não é mais mantido e não suporta ES2015+; testes novos ficam limitados. Cobertura real ❓ (não medida).
- 🔶 O e2e apenas verifica o carregamento da home; não valida dados da API.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/09-Qualidade/Portal-Transparencia-Frontend-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Testes-e-Cobertura|Testes do Backend]]

## Pendências e próximo passo
- Executar `gulp test` em ambiente compatível e registrar cobertura (ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Registro-de-Analise|Registro de análise]]).
