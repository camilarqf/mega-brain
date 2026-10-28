---
type: quality
aliases:
  - "Frontend SIC — testes e cobertura"
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: completa
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
sources:
  - package.json
  - Dockerfile
  - .jenkins-pipelines/deployment.params.yml
  - gulpfile.js
---

# Frontend SIC — testes e cobertura

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Débitos: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]]

## Objetivo
Registrar a estratégia de testes e a verificação automática existentes no repositório.

## Evidências
Listagem completa de arquivos do repositório e arquivos em `sources`, commit `5518a81`. Nada foi executado.

## Informações confirmadas
- ✅ **Não há testes automatizados**: nenhum arquivo `*.spec.*`, `*.test.*`, pasta de testes, configuração de Karma/Jasmine/Jest/Protractor/Cypress nem dependência de teste em `package.json`.
- ✅ O script `npm test` é um *stub*: `echo "Error: no test specified" && exit 1` (falha sempre).
- ✅ `htmlhint` está em `devDependencies`, mas não há script que o chame nem arquivo `.htmlhintrc`.
- ✅ O `Dockerfile` só executa `npm install` e `gulp <perfil>`; não roda testes nem lint. O repositório não contém Jenkinsfile; `.jenkins-pipelines` traz apenas parâmetros de implantação e variáveis por ambiente (as etapas de CI ficam fora do repositório, ❓).
- ✅ A única verificação de compilação é o próprio `gulp` (concatenação/minificação); erros de JavaScript só aparecem em execução.
- ✅ Validações de formulário ficam nos templates e nas diretivas `dir*Form` (sem testes).

## Inferências e limitações
- 🔶 Os defeitos listados em [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]] (referências não definidas, variáveis globais implícitas, `$ngConfirm` não injetado) seriam detectáveis por lint e por testes de controller.
- ❓ Se o pipeline externo executa algum teste ou análise estática (SonarQube etc.).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Stack-e-Dependencias|Stack-e-Dependencias]] · Equivalente: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Testes-e-Cobertura|Testes do Frontend Ouvidoria]]

## Pendências e próximo passo
- Confirmar com o time se há etapas de teste/lint no pipeline. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
