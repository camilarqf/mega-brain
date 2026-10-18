---
type: repository
system: PARTICIPA-DF
repository:
  - participa-df-backend
  - participa-df-frontend
status: pendente
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
updated: 2026-10-18
tags:
  - participa-df
  - repositorios
---
# PARTICIPA-DF — repositórios

Voltar: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|PARTICIPA-DF]]

## Objetivo
Relacionar os repositórios do sistema Participa DF, o estado da análise e o commit de referência.

## Evidências
- `participa-df-backend`: `git rev-parse HEAD` = `4901ad501a86773f40dcd36fb90470a3ba5c0c96` (branch `master`, commit de 2026-09-15; 1395 commits). Sem README nem documentação no repositório.
- `participa-df-frontend`: `git rev-parse HEAD` = `d250804ce5208995296da23ccfb2c444f91da8cc` (branch `master`, commit de 2026-07-03; 723 commits). Associação ao sistema confirmada pela responsável (2026-10-18) e coerente com `applicationName: 'Participa-DF'` e com os 66 caminhos de API consumidos, todos presentes no catálogo do backend (correspondência textual).
- A responsável informou que o Participa tem **3 front-ends**; só um foi identificado. 🔶 Os outros dois seriam os de Ouvidoria e SIC (`SistemaOuvDF`, `SistemaSicDF` em `configuration/front-end-urls`).
- Endereços dos remotos omitidos (infraestrutura interna).
- Arquivo não versionado `src/Directory.Build.props` presente na cópia local (apenas exclui `artifacts\**` da compilação).

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `participa-df-backend` | ✅ API ASP.NET Core (.NET 5), solução `OuvDF.sln` com projetos em `src/` e de teste em `tests/` | analisado: lotes 0 a 8, 33 notas no backend (30 técnicas); cobertura parcial (SDK interno, cadastros e valores de configuração não lidos) | `4901ad5` | [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] |
| `participa-df-frontend` | ✅ SPA Angular 13 voltada ao cidadão (rótulo provisório `Frontend-Cidadao`); consome o backend | analisado: lotes 0 a 5, 17 notas; cobertura parcial | `d250804` | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] |
| outros 2 front-ends | ❓ não identificados (🔶 Ouvidoria `SistemaOuvDF` e SIC `SistemaSicDF`, destinos do login assistido) | **não analisados** | — | — |

## Inferências e limitações
- ✅ Backend: há `FrontEndURLs` e `CorsOrigins` nas chaves de configuração.
- `OuvDF.BCadastro.Client` e `OuvDF.GovBr.Client` só têm `bin/` e `obj/` (sem código-fonte; ausentes do Dockerfile).

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Informar os repositórios dos outros dois front-ends e confirmar o nome do componente do frontend analisado.
- Para atualizar o frontend: `git diff d250804..HEAD --stat` (skill `atualizar-documentacao`).
- Para atualizar o backend: `git diff 4901ad5..HEAD --stat` (skill `atualizar-documentacao`).
