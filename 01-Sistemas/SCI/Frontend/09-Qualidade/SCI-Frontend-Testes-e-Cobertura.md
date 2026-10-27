---
type: quality
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - sci
  - frontend
  - testes
sources:
  - angular.json
  - tsconfig.spec.json
  - package.json
---
# SCI Frontend — testes e cobertura

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Registrar a situação dos testes automatizados do frontend.

## Evidências
- Busca por `*.spec.ts` em `src`: **nenhum** arquivo. `angular.json` tem o alvo `test` (Karma, `tsconfig.spec.json`); `package.json` tem `karma`, `karma-jasmine`, `karma-coverage` e `jasmine-core`.
- `ng test` e `ng build` não foram executados nesta análise.

## Informações confirmadas
- ✅ Infraestrutura de teste configurada (Karma + Jasmine + cobertura) e nenhum teste unitário escrito.
- ✅ Não há testes de ponta a ponta no repositório (nenhuma configuração de Cypress, Playwright ou `ng e2e`); o `README.md` é o texto padrão do Angular CLI.
- ✅ Os pipelines em `.jenkins-pipelines` só constroem e publicam (sem etapa de teste identificada na leitura parcial).

## Inferências e limitações
- 🔶 Sem testes, as regras de visibilidade por perfil e status e o confronto com o backend dependem de verificação manual.
- ❓ Existência de pipeline com `ng test` não confirmada (Jenkinsfiles lidos só no cabeçalho de parâmetros).

## Relacionamentos
- [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Testes-e-Cobertura|Testes do backend]] · [[01-Sistemas/SCI/Frontend/09-Qualidade/SCI-Frontend-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
