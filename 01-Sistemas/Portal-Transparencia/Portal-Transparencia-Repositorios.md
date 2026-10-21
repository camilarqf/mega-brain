---
type: repository
system: Portal-Transparencia
repository:
  - portal-transparencia-backend
  - portal-transparencia-frontend
status: pendente
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-21
tags:
  - portal-transparencia
  - repositorios
---
# Portal-Transparencia — repositórios

Voltar: [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Index|Portal-Transparencia]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `portal-transparencia-backend` (nome do remoto `origin`; pasta local `PT2016_BackEnd`): `git rev-parse HEAD` = `9434e58f35284618d236f25b3ed2f2b307a7e345`, branch `master`, commit de 2026-09-24 (merge da `feature/novoFiltroLicitacao`). Remoto GitLab interno; endereço omitido.
- Árvore de trabalho com arquivos não versionados (quatro `RELATORIO_*_LEGADO.md`, `logback-spring.xml`, testes em `src/test/.../servico/pesquisa/`); **fora do escopo** por decisão do usuário em 2026-10-19.
- Arquivos de log e `hs_err_pid*.log` na raiz da pasta existem no disco, mas não são versionados.
- `portal-transparencia-frontend` (nome do remoto `origin`; pasta local `PT2016_FrontEnd`): `git rev-parse HEAD` = `dca3e933ffd7e5bbfd173133e88d14f94304cb52`, branch `master`, commit de 2026-10-21 (merge de `feature/refatoracao-acesso-minio`); árvore de trabalho limpa. Remoto GitLab interno; endereço omitido. Pertencimento ao sistema confirmado pelo usuário em 2026-10-21.

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `portal-transparencia-backend` | API REST em Spring Boot 1.3 (Java 8) sobre SQL Server, para consultas públicas de transparência | analisado, cobertura parcial | `9434e58f` | [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] |
| `portal-transparencia-frontend` | SPA AngularJS 1.4 ("Portal 2016") que consome a API do Backend; sem login | analisado, cobertura parcial | `dca3e933` | [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]] |

## Inferências e limitações
- ❓ Outros componentes (como o ETL que alimenta as tabelas de carga, o serviço de busca `apisuperbusca` e o "gerenciador") não foram identificados.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Para atualizar o backend: `git diff 9434e58f35284618d236f25b3ed2f2b307a7e345..HEAD --stat` (skill `atualizar-documentacao`).
- Para atualizar o frontend: `git diff dca3e933ffd7e5bbfd173133e88d14f94304cb52..HEAD --stat`.
