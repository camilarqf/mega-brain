---
type: module
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - sici
  - modulo
  - auditor
  - perfil
  - coordenador
sources:
  - api/auditor/AuditorController.java
  - api/auditor/AuditorPerfilController.java
  - api/auditor/AuditorPerfilConsultaController.java
  - api/coordenador/CoordenadorController.java
  - api/perfil/PerfilController.java
  - application/usecase/auditor/*
  - application/usecase/coordenador/*
  - infrastructure/persistence/repository/AuditorRepository.java
---

# Auditores, coordenadores e perfis

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]], [[01-Sistemas/SICI/Backend/06-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]], [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]]

> O **auditor** é o usuário do sistema: o login no Keycloak (`preferred_username`) precisa bater com `TB_AUDITOR.DS_LOGIN` de um auditor **ativo**. Os **perfis** do auditor (`TB_AUDITOR_PERFIL`) viram as roles da aplicação.

## Endpoints ✅
| Método | Rota | Roles | Função |
|---|---|---|---|
| GET | `/auditor/listar` | — | `ListarAuditor` |
| GET | `/auditor/listar-por-acao/{acaoControleId}` | — | auditores vinculados à ação |
| GET | `/auditor/listar-nao-relacionados-por-acao/{acaoControleId}` | — | candidatos à designação |
| GET | `/auditores/com-perfil` | SUBCI (na classe) | `ListarAuditoresComPerfilUseCase` |
| PUT | `/auditores/{idAuditor}/vincular-perfis` | SUBCI (na classe) | `AtualizarPerfisAuditorUseCase` |
| GET | `/perfis` | — | lista de perfis |
| GET | `/coordenador/listar` | — | `ListarCoordenador` |
| GET | `/coordenador/listar-por-coordenador/{acaoControleId}` | — | coordenadores da ação |
| GET | `/coordenador/listar-nao-relacionados/{acaoControleId}` | — | candidatos |

## Perfis → roles ✅
`JwtAuthenticationConverterCustom`: o nome de cada perfil vai para maiúsculas, espaços viram `_`, e recebe o prefixo `ROLE_`. Roles usadas em `@PreAuthorize`: **SUBCI**, **COORDENADOR**, **DIRETOR**, **AUDITOR**. Detalhes em [[01-Sistemas/SICI/Backend/06-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]].

## Vincular perfis — `AtualizarPerfisAuditorUseCase` ✅
- Substitui **toda** a lista de perfis do auditor pelos ids informados (`perfilRepository.findAllById`).
- Ids inexistentes são **ignorados em silêncio**; lista vazia remove todos os perfis.
- ⚠️ Usa `AuditorRepository`/`PerfilRepository` e entidades JPA direto no use case (desvio de camada).
- Auditor inexistente → `RuntimeException` genérica.
- Mudança de perfil vale na **próxima requisição**: as roles são recalculadas a cada token convertido, sem cache.

## Coordenador ✅
- Vínculo por OS em `TB_COORDENADOR_TB_ORDEM_SERVICO` (`IN_ATIVO`, `ID_OS_SUBSTITUICAO`).
- "Coordenador da ação" = coordenador **ativo** em alguma OS da ação (`existeCoordenadorAtivoParaAcaoControle`).
- A substituição é feita por OS SUBSTITUICAO — ver [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]] e [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Ciclo-de-Vida-OS|Fluxo-Ciclo-de-Vida-OS]].

## Observações
- ✅ Não há cadastro, edição nem inativação de auditor por API. 🔶 A carga de `TB_AUDITOR` vem de seeder ou de processo externo.
- ✅ Consultas de auditor e coordenador não têm restrição de perfil e retornam nome e matrícula (dado pessoal funcional) a qualquer autenticado.
