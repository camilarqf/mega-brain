---
type: reference
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - sici
  - api
  - endpoints
  - rest
sources:
  - src/main/java/br/gov/df/cg/sici/api
---

# Catálogo de endpoints

Voltar: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/06-Seguranca/Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]], [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Autenticacao|Fluxo-Autenticacao]]

> Fonte: anotações `@*Mapping` e `@PreAuthorize` dos 19 controllers em `api/`.
> **Roles**: S = SUBCI · C = COORDENADOR · D = DIRETOR · A = AUDITOR · `—` = só autenticado · `público` = sem token.
> Documentação interativa: Swagger UI (`/swagger-ui.html`, springdoc; título configurado em `OpenSwagger`).

## Autenticação — `AuthController`
| Método | Rota | Roles | Nota |
|---|---|---|---|
| POST | `/auth/login` | público | proxy ROPC → Keycloak |
| GET | `/auth/account` | — | userinfo do Keycloak |
| GET | `/me` | — | username + roles da aplicação |

## Planejamento
| Método | Rota | Roles | Nota |
|---|---|---|---|
| POST | `/poac/cadastrar` | — | [[01-Sistemas/SICI/Backend/03-Modulos/POAC|POAC]] |
| GET | `/poac/listar` · `/poac/pesquisar` · `/poac/pesquisar-ano` | — | |
| POST | `/acao-controle/cadastrar` | S C D | [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]] |
| GET | `/acao-controle/listar` · `/pesquisar` · `/pesquisar-poac/{idPoac}` · `/validar/{id}` | — | |
| PUT | `/acao-controle/atualizar/{id}` | S C D | |
| DELETE | `/acao-controle/inativar?id=` | S C | bloqueia se houver OS |

## Ordem de Serviço — `/os-acao-controle` ([[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]])
| Método | Rota | Roles |
|---|---|---|
| POST | `/salvar-os/{acaoControleId}` | S C D A (cancelamento: S C D, checado no use case) |
| GET | `/listar` | S |
| GET | `/listar-os/{idAcaoControle}` | S C D A |
| GET | `/pesquisar?id=` | S D |
| PUT | `/atualizar/{id}` | S C D A |
| PUT | `/alterarStatusOs/{id}` | S C D A |
| DELETE | `/excluir/{id}` | S C D |
| POST | `/{id}/fases` | — |
| POST | `/{idOrdemServicoBase}/prorrogacoes` | — |
| PUT | `/{idOrdemServico}/prorrogacoes` | — |
| POST | `/cancelar-os/{idAcaoControle}` | S C D |
| PUT | `/cancelamento/{idOrdemServico}/{idCancelamento}` | — |
| GET | `/gerar-pdf?id=` | — |
| GET | `/validar-data-prorrogacao` | — |

## OS Genérica — `/ordem-servico-generica` ([[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]])
| Método | Rota | Roles |
|---|---|---|
| POST | `/salvar-os` | — |
| GET | `/listar` · `/pesquisar` · `/gerar-pdf` | — |
| PUT | `/atualizar/{id}` · `/alterarStatusOs/{id}` | — |
| DELETE | `/excluir/{id}` | — |

## Assinatura — `/assinaturas` ([[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]])
| Método | Rota | Roles | Nota |
|---|---|---|---|
| POST | `/assinar-os/{idOrdemServico}` | — | só o SUBCI titular ou o substituto vigente (checado no use case) |
| POST | `/assinar-os-generica/{idOrdemServicoGenerica}` | — | idem |
| GET | `/{idDocumentoAssinado}/download` | — | PDF + headers de hash |
| GET | `/{idDocumentoAssinado}/download-generica` | — | |
| GET | `/validacao?codigo=` | — | exige token |

## Pessoas e papéis
| Método | Rota | Roles | Nota |
|---|---|---|---|
| POST | `/subci/cadastrar` | — ⚠️ | [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]] |
| GET | `/subci/listar` | S | |
| GET | `/subci/pesquisar` | — | |
| POST | `/subci/{idSubci}/substitutos` | — ⚠️ | |
| GET | `/subci/{idSubci}/substitutos` | — | |
| GET | `/auditor/listar` · `/listar-por-acao/{id}` · `/listar-nao-relacionados-por-acao/{id}` | — | [[01-Sistemas/SICI/Backend/03-Modulos/Auditores-Coordenadores-Perfis|Auditores-Coordenadores-Perfis]] |
| GET | `/auditores/com-perfil` | S | |
| PUT | `/auditores/{idAuditor}/vincular-perfis` | S | |
| GET | `/perfis` | — | |
| GET | `/coordenador/listar` · `/listar-por-coordenador/{id}` · `/listar-nao-relacionados/{id}` | — | |

## Cadastros auxiliares ([[01-Sistemas/SICI/Backend/03-Modulos/Cadastros-Auxiliares|Cadastros-Auxiliares]])
`GET /unidade-auditoria/listar` · `GET /area-executora/listar/{id}` · `GET /programa-governo/listar` · `GET /objetivo-ppa/listar/{codigo}` · `GET /unidade-auditada/listar` · `GET /fase/listar` · `GET /fase/descricao-fase` — todos `—`.

## Operação
| Rota | Acesso |
|---|---|
| `/healthcheck` (actuator health, com detalhes; inclui `HealthCheckController` com uptime e `KeycloakHealthIndicator`) | público |
| `/prometheus`, `/actuator/prometheus` | público |
| `/swagger-ui.html`, `/v3/api-docs` | público |

## Convenções observadas
- Verbos misturados no caminho (`/cadastrar`, `/listar`, `/salvar-os`, `/alterarStatusOs`) em vez de recursos REST.
- Mistura de kebab-case e camelCase (`/alterarStatusOs`).
- `DELETE /acao-controle/inativar?id=` (exclusão lógica por query param).
- Paginação só em `GET /os-acao-controle/listar`.
