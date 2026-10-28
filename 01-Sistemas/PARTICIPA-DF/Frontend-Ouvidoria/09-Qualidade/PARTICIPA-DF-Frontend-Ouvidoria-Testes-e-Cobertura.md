---
type: quality
aliases:
  - "Frontend Ouvidoria — testes e cobertura"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: completa
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
sources:
  - package.json
  - gulpfile.js
  - .jenkins-pipelines/Jenkinsfile.prod
  - Dockerfile
---

# Frontend Ouvidoria — testes e cobertura

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Débitos: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Debitos-Tecnicos]]

## Objetivo
Registrar o que existe de teste e verificação de qualidade no repositório.

## Evidências
Busca por arquivos de teste, scripts e configuração de lint/CI no commit `9d8ecdb`. A cobertura desta nota é `completa` quanto à **existência** de testes (nenhum); não houve execução.

## Informações confirmadas
- ✅ **Nenhum teste automatizado**: sem arquivos `*.spec.*`/`*.test.*`, sem Karma/Jasmine/Protractor/Cypress em `package.json`; o script `test` é `echo "Error: no test specified" && exit 1`.
- ✅ **Sem lint**: não há `.eslintrc`, `.htmlhintrc` nem `.editorconfig`. `htmlhint` consta como dependência de desenvolvimento, mas nenhuma tarefa Gulp o usa (🔶).
- ✅ **Pipeline sem etapa de teste ou análise**: os Jenkinsfiles só constroem a imagem, copiam `public/dist` e publicam. O Dockerfile executa apenas `gulp <perfil>`.
- ✅ `app/upload/teste-upload.html` é uma página de demonstração, não um teste automatizado.
- ✅ Cobertura de testes medida: **0** (não há ferramenta).
- ❓ Não há evidência de testes manuais/roteiros de homologação no repositório.

## Inferências e limitações
- 🔶 Sem testes, regras do frontend (filtros da caixa de entrada, prazo restante, normalização de nome de arquivo, máscaras de atributos) não têm proteção contra regressão; o código usa muito `$scope`, jQuery e modais, o que dificulta testes unitários.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Debitos-Tecnicos]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Pendências e próximo passo
- Definir com o time a estratégia mínima (ex.: testes dos serviços e das funções puras). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
