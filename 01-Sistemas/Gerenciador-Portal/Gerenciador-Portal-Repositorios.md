---
type: repository
aliases:
  - "Gerenciador-Portal — repositórios"
system: Gerenciador-Portal
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
---
# Gerenciador-Portal — repositórios

Voltar: [[01-Sistemas/Gerenciador-Portal/Gerenciador-Portal-Index|Gerenciador-Portal]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `gerenciador-portal-frontend`: `git rev-parse HEAD` = `d6a737a3a0e5cf1b245aa35c81321638dd0cbecc`, branch `master`, commit de 2026-10-22 ("Merge branch 'fix/roteamento-imagens-arquivos' into 'master'"). Arquivo **não versionado** `src/app/sessao-sso.service.js`, fora do escopo por decisão do usuário.
- `gerenciador-portal-backend` (nome do remoto `origin`, GitLab interno; endereço omitido): `git rev-parse HEAD` = `14b185feeac4f5889a0ce8041a3b5baaead0334b`, branch `fix/corrige-usuario-logado`, commit de 2026-10-22 ("fix: corrige usuário logado para admin"). 339 commits no histórico.
- Árvore de trabalho com dois diretórios **não versionados** de teste (`src/test/java/br/gov/df/cgdf/gerenciador/comum/` e `.../config/`): **fora do escopo** por decisão do usuário em 2026-10-27; os fatos abaixo valem para o commit, não para eles.
- Arquivos como `gerenciador.log`, `target/` e `jh` existem no disco; `*.log` e `target/` são ignorados pelo Git.

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `gerenciador-portal-backend` | API REST Spring Boot 1.5 (Java 8) de administração de conteúdo do Portal da Transparência | analisado, cobertura parcial | `14b185f` | [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]] |
| `gerenciador-portal-frontend` | SPA AngularJS 1.6 de administração (login, arquivos, imagens, cargas, palavras-chave, órgãos LAI, medida protetiva) | analisado, cobertura parcial | `d6a737a` | [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]] |

## Inferências e limitações
- ✅ O cliente web (frontend) que consome esta API é o `gerenciador-portal-frontend` (identificado em 2026-10-27; os caminhos e parâmetros que ele usa coincidem com o catálogo do backend).
- ❓ Nome oficial do sistema e dono: não constam no código.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]
- [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Repositorios|Repositórios do Portal-Transparencia]] (relação informada pelo usuário)

## Pendências e próximo passo
- Para atualizar o backend: `git diff 14b185feeac4f5889a0ce8041a3b5baaead0334b..HEAD --stat` (skill `atualizar-documentacao`).
- Para atualizar o frontend: `git diff d6a737a3a0e5cf1b245aa35c81321638dd0cbecc..HEAD --stat`.
