---
type: repository
aliases:
  - "PARTICIPA-DF — repositórios"
system: PARTICIPA-DF
repository:
  - participa-df-backend
  - participa-df-frontend
  - participa-df-ouv-frontend
  - participa-df-sic-frontend
status: pendente
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
updated: 2026-10-28
---
# PARTICIPA-DF — repositórios

Voltar: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|PARTICIPA-DF]]

## Objetivo
Relacionar os repositórios do sistema Participa DF, o estado da análise e o commit de referência.

## Evidências
- `participa-df-backend`: `git rev-parse HEAD` = `4901ad501a86773f40dcd36fb90470a3ba5c0c96` (branch `master`, commit de 2026-09-15; 1395 commits). Sem README nem documentação no repositório.
- `participa-df-frontend`: `git rev-parse HEAD` = `d250804ce5208995296da23ccfb2c444f91da8cc` (branch `master`, commit de 2026-07-03; 723 commits). Associação ao sistema confirmada pela responsável (2026-10-18) e coerente com `applicationName: 'Participa-DF'` e com os 66 caminhos de API consumidos, todos presentes no catálogo do backend (correspondência textual).
- A responsável informou que o Participa tem **3 front-ends**. 🔶 Os outros dois seriam os de Ouvidoria e SIC (`SistemaOuvDF`, `SistemaSicDF` em `configuration/front-end-urls`); os três repositórios já foram identificados.
- `participa-df-ouv-frontend`: `git rev-parse HEAD` = `9d8ecdb6b027b5283d71cee49bc40aa452be6afe` (branch `master`, commit de 2026-09-09; 197 commits). O README o descreve como "Frontend AngularJS do módulo de Ouvidoria do Participa DF"; consome `servico-ouvidoria/*`, `operador-so/*` e `security/*` do backend. Associação autorizada ao aprovar o plano (2026-10-18); correspondência com `SistemaOuvDF` 🔶 não confirmada.
- `participa-df-sic-frontend`: `git rev-parse HEAD` = `5518a8141d83784eab17ebe61d84331d842add2c` (branch `master`, commit de 2026-10-14; 225 commits). Sem README. SPA AngularJS 1.5 + Gulp 3 do SIC (título "SIC-DF"), *fork* do front de Ouvidoria (módulo `Ouv-DF`, pacote `OuvCidadania.Ui`); consome `operador-sic/*` e `acesso-informacao/*` do backend. Nome do app em `.jenkins-pipelines/deployment.params.yml`: `Participa DF Sic Frontend`. Associação autorizada ao aprovar o plano (2026-10-18); correspondência com `SistemaSicDF` 🔶 não confirmada.
- Endereços dos remotos omitidos (infraestrutura interna).
- Arquivo não versionado `src/Directory.Build.props` presente na cópia local (apenas exclui `artifacts\**` da compilação).

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `participa-df-backend` | ✅ API ASP.NET Core (.NET 5), solução `OuvDF.sln` com projetos em `src/` e de teste em `tests/` | analisado: lotes 0 a 8, 33 notas no backend (30 técnicas); cobertura parcial (SDK interno, cadastros e valores de configuração não lidos) | `4901ad5` | [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] |
| `participa-df-frontend` | ✅ SPA Angular 13 voltada ao cidadão (rótulo provisório `Frontend-Cidadao`); consome o backend | analisado: lotes 0 a 5, 17 notas; cobertura parcial | `d250804` | [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] |
| `participa-df-ouv-frontend` | ✅ SPA AngularJS 1.x + Gulp para operadores de ouvidoria (rótulo provisório `Frontend-Ouvidoria`); consome o backend | analisado: lotes 0 a 5; cobertura parcial | `9d8ecdb` | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] |
| `participa-df-sic-frontend` | ✅ SPA AngularJS 1.5 + Gulp 3 para operadores do SIC (rótulo provisório `Frontend-SIC`); consome o backend | analisado: lotes 0 a 5; cobertura parcial | `5518a81` | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] |

## Inferências e limitações
- ✅ Backend: há `FrontEndURLs` e `CorsOrigins` nas chaves de configuração.
- `OuvDF.BCadastro.Client` e `OuvDF.GovBr.Client` só têm `bin/` e `obj/` (sem código-fonte; ausentes do Dockerfile).

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Confirmar os nomes dos componentes `Frontend-Cidadao`, `Frontend-Ouvidoria` e `Frontend-SIC` e a correspondência de cada front-end com `SistemaOuvDF`/`SistemaSicDF`.
- Para atualizar o frontend SIC: `git diff 5518a81..HEAD --stat` (skill `atualizar-documentacao`).
- Para atualizar o frontend de Ouvidoria: `git diff 9d8ecdb..HEAD --stat` (skill `atualizar-documentacao`).
- Para atualizar o frontend: `git diff d250804..HEAD --stat` (skill `atualizar-documentacao`).
- Para atualizar o backend: `git diff 820666c..HEAD --stat` (skill `atualizar-documentacao`). Última atualização: 2026-10-23 (`4901ad5..820666c`, ver [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Registro-de-Analise|Registro-de-Analise]]).

## Histórico do catálogo (até 2026-10-28)
Texto original das colunas do `Catalogo-de-Sistemas.md`, antes da simplificação (melhorias do cofre, lote 6):
- **Sistema:** Participa DF (nome do app no pipeline; namespace `OuvDF`; nome oficial a validar; validar permissão antes de publicar)
- **Repositórios:** `participa-df-backend`, `participa-df-frontend` (Cidadão), `participa-df-ouv-frontend` (Ouvidoria), `participa-df-sic-frontend` (SIC); 3 de 3 front-ends identificados
- **Estado:** Backend analisado (commit `4901ad5`; lotes 0 a 8 concluídos, cobertura parcial); frontend `participa-df-frontend` analisado (commit `d250804`; lotes 0 a 5, cobertura parcial); frontend `participa-df-ouv-frontend` (AngularJS, Ouvidoria) analisado (commit `9d8ecdb`; lotes 0 a 5, cobertura parcial); frontend `participa-df-sic-frontend` (AngularJS, SIC) em análise (commit `5518a81`; lotes 0 a 5, cobertura parcial)
