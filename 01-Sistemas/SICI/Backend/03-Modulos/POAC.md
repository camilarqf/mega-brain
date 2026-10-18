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
  - poac
  - planejamento
sources:
  - api/poac/PoacController.java
  - application/usecase/poac/CriarPoac.java
  - application/service/poac/PoacServiceImpl.java
  - domain/model/Poac.java
---

# POAC

Voltar: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/Glossario|Glossario]]

> Plano anual que agrupa as ações de controle (🔶 provável "Plano Operacional Anual de Controle"). Ligação: `TB_ACAO_CONTROLE.ID_POAC` (V24).

## Endpoints — `/poac` ✅
| Método | Rota | Roles | Função |
|---|---|---|---|
| POST | `/cadastrar` | **nenhuma** (autenticado) | `CriarPoac.salvar` |
| GET | `/listar` | — | lista todos |
| GET | `/pesquisar` | — | por id |
| GET | `/pesquisar-ano` | — | por ano |

## Modelo ✅
`Poac`: `nomePoac`, `anoPoac`, `dataCadastroPoac`, `dataInicioPoac`, `dataFimPoac` (`Poac.criar`).

## Regras ✅
- `CriarPoac` só monta e salva: **não valida** datas (início ≤ fim), unicidade por ano, nem coerência entre ano e datas.
- Não há endpoints de atualização ou exclusão de POAC.
- ⚠️ Qualquer usuário autenticado pode cadastrar um POAC.
- 🔶 `PoacServiceImpl` importa `infrastructure` (desvio de camada listado em [[01-Sistemas/SICI/Backend/01-Visao-Geral/Arquitetura-Hexagonal|Arquitetura-Hexagonal]]).
