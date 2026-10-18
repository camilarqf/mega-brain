---
type: repository
system: PARTICIPA-DF
repository:
  - participa-df-backend
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
- Endereço do remoto omitido (infraestrutura interna).
- Arquivo não versionado `src/Directory.Build.props` presente na cópia local (apenas exclui `artifacts\**` da compilação).

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `participa-df-backend` | ✅ API ASP.NET Core (.NET 5), solução `OuvDF.sln` com projetos em `src/` e de teste em `tests/` | analisado: lotes 0 a 8, 33 notas no backend (30 técnicas); cobertura parcial (SDK interno, cadastros e valores de configuração não lidos) | `4901ad5` | [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] |
| frontend | ❓ não identificado | **não analisado** | — | — (pasta `Frontend/` não criada, conforme `BRAIN-RULES.md`) |

## Inferências e limitações
- 🔶 Existe um frontend consumidor (há `FrontEndURLs` e `CorsOrigins` nas chaves de configuração), mas o repositório e a relação não foram confirmados.
- `OuvDF.BCadastro.Client` e `OuvDF.GovBr.Client` só têm `bin/` e `obj/` (sem código-fonte; ausentes do Dockerfile).

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Informar qual é o repositório do frontend.
- Para atualizar o backend: `git diff 4901ad5..HEAD --stat` (skill `atualizar-documentacao`).
