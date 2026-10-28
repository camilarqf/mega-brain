---
type: module
aliases:
  - "Cadastros auxiliares (somente leitura)"
  - "Cadastros-Auxiliares"
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
sources:
  - api/acaoControle/AreaExecutoraController.java
  - api/acaoControle/ObjetivoPPAController.java
  - api/acaoControle/ProgramaGovernoController.java
  - api/acaoControle/UnidadeAuditadaController.java
  - api/acaoControle/UnidadeAuditoriaInternaController.java
  - api/ordemServico/fase/FaseController.java
  - api/ordemServico/fase/DescricaoFaseAcaoController.java
  - application/usecase/{areaExecutora,objetivoPPA,programaGoverno,unidadeAuditada,unidadeAuditoriaInterna,ordemServico/fase}/*
---

# Cadastros auxiliares (somente leitura)

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Acao-de-Controle|Acao-de-Controle]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Banco-e-Migrations|Banco-e-Migrations]]

> Tabelas de referência populadas por **seeders** (V2, V55 — não lidos) e migrations. A API só **consulta** esses dados: não há endpoints de escrita. Nenhum endpoint tem `@PreAuthorize`.

| Método | Rota | Retorno | Use case / porta |
|---|---|---|---|
| GET | `/unidade-auditoria/listar` | UAIs (nome, sigla) | `ListarUnidadeAuditoriaInterna` |
| GET | `/area-executora/listar/{id}` | áreas executoras **da UAI** `{id}` | `ListarAreaExecPorAuditInterna` → `buscarAreaExecutoraPorAuditInterna` |
| GET | `/programa-governo/listar` | programas de governo (código, descrição) | `ListarProgramaGoverno` |
| GET | `/objetivo-ppa/listar/{codigo}` | objetivos PPA **do programa** `{codigo}` | `ListarObjetivoPorPrograma` → `buscarPorProgramaGoverno` |
| GET | `/unidade-auditada/listar` | unidades auditadas | `ListarUnidadeAuditada` → `buscarLista` |
| GET | `/fase/listar` | fases | `ListarFase` |
| GET | `/fase/descricao-fase` | descrição padrão por fase × tipo de ação × natureza | `BuscarDescricaoFaseAcao` |

## Observações
- ✅ Hierarquias usadas pelo formulário da ação: **UAI → áreas executoras** e **programa de governo → objetivos PPA**. A consistência programa × objetivos é validada na criação da ação ([[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Acao-de-Controle|Acao-de-Controle]]).
- ✅ Registros **"A DEFINIR"** com id `999` em programa de governo e unidade auditada servem de placeholder e são checados por `GET /acao-controle/validar/{id}`.
- ❓ Não foi verificado se `/unidade-auditada/listar` filtra `IN_ATIVO = 1` (coluna criada na V54).
- ✅ `TB_DESCRICAO_FASE_ACAO` passou de textos para ids (fase/tipo/natureza) nas V4–V6. A descrição gerada entra na fase da OS e no PDF.
