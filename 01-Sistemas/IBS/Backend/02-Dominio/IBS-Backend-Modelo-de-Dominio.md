---
type: domain
aliases:
  - "IBS Backend — modelo de domínio"
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
sources:
  - src/main/java/br/gov/df/cg/ibs/domain
---
# IBS Backend — modelo de domínio

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Listar entidades, value objects, enums e exceções do pacote `domain`.

## Evidências
- Classes em `domain/*`; testes de domínio (`FonteAutenticacaoTest`, `ServidorAutenticacaoTest`, `SufixoLoginTest`, `ContextoPesquisaTest`, `SiglaUnidadeTest`, `TextoInstitucionalTest`, `UnidadesInstitucionaisTest`, `LoginUsuarioTest`).

## Informações confirmadas
| Elemento | Tipo | Regras |
|---|---|---|
| `FonteAutenticacao` | entidade (imutável) | Órgão, descrição, sigla, sufixo (opcional), contexto, atributo, versão e ≥ 1 servidor; obrigatórios validados com `FonteAutenticacaoException` |
| `ServidorAutenticacao` | entidade | id, órgão, nome, endereço, porta 1–65535, timeout > 0 |
| `SufixoLogin` | VO | minúsculas, deve começar com `@`, sem espaços |
| `ContextoPesquisa` | VO | normaliza vírgulas; exige `DC=` |
| `AtributoFiltro` | enum | `UPN`, `DISPLAY_NAME` (`fromDatabaseValue`: `userprincipalname`, `displayname`) |
| `ResultadoAutenticacao` | sealed | `Sucesso(login, nomeFonte, latência)`, `CredencialInvalida(login, nomeFonte, código LDAP)`, `FalhaTecnica(nomeFonte, tipo)` |
| `MotivoFalhaAutenticacao` | enum | `USUARIO_SEM_VINCULO_NO_ORGAO`, `CREDENCIAL_INVALIDA`, `SERVICO_INDISPONIVEL`, `FONTE_NAO_ENCONTRADA`, `USUARIO_SEM_MATRICULA` |
| `TipoFalhaTecnica` | enum | `TIMEOUT`, `CONN_REFUSED`, `UNAVAILABLE` |
| `IdentidadeInstitucionalUsuario` | record | id, órgão, nome do órgão, pessoa, nome social, matrícula, perfil, `VinculoStatus`, unidades |
| `VinculoStatus` | enum | `ATIVO`, `INATIVO` |
| `UnidadeInstitucional` | record | `idUnidade`, `siglaUnidade`, `descricaoUnidade` |
| `SiglaUnidade` | VO | `siglaOrgao()` = trecho antes da primeira `/` |
| `UnidadesInstitucionais` | VO | `siglaOrgao()` = sigla de órgão da primeira unidade válida |
| `TextoInstitucional` | VO | `trim`; vazio ou "NULL" vira `null` |
| `LoginUsuario`, `SenhaUsuario`, `CorrelationKey` | VOs compartilhados | ver [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Autenticacao-de-Usuario|Autenticação]] |
| `LoginContextualizado`, `FonteAutenticacaoRepository`, `ResumoCarregamentoFontesAutenticacao` | VO / porta / DTO | repositório é interface de domínio implementada em `infra` |

## Inferências e limitações
- 🔶 Há dois `LoginUsuario` (um em `domain.fonteautenticacao.valueobjects`, outro em `_sharedkernel`); o do `fonteautenticacao` e `LoginContextualizado` não foram lidos em detalhe — só o do `_sharedkernel` é usado no fluxo de `/auth`.
- `VinculoStatus.INATIVO` não é produzido pela consulta atual (que filtra ativos).

## Relacionamentos
- [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Claims|Modelo de claims]] · [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Fontes-de-Autenticacao|Fontes de autenticação]]

## Pendências e próximo passo
- Confirmar o uso de `LoginContextualizado` e do segundo `LoginUsuario`.
