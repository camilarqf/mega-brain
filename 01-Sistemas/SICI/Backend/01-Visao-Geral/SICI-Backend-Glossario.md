---
type: reference
aliases:
  - "Glossário"
system: SICI
repository: sici-backend
status: pendente
coverage: parcial
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
created: 2026-10-16
updated: 2026-10-18
---

# Glossário

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Enums-e-Estados|Enums-e-Estados]], [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

> ✅ = termo e uso confirmados no código · 🔶 = expansão da sigla inferida (o código não define) · ❓ = significado não identificado.

| Termo | Significado | Status | Onde aparece |
|---|---|---|---|
| **SICI** | Sistema de controle interno; expansão oficial da sigla não consta no código | ❓ | `pom.xml` (`artifactId`), pacote raiz |
| **CGDF** | Controladoria-Geral do DF; sufixo da numeração oficial das OS | ✅ uso / 🔶 expansão | `AssinarOrdemServico.executar` → `"%06d/%d - %s/CGDF"` |
| **Ação de Controle** | Trabalho de auditoria, consultoria ou inspeção planejado para um ano, ligado a POAC, unidade de auditoria interna, área executora, unidades auditadas e programa/objetivos do PPA | ✅ | `domain/model/AcaoControle` |
| **Tipo de ação** | Auditoria, Consultoria, Inspeção | ✅ | `ETipoAcao` |
| **Natureza da ação** | Conformidade, Desempenho, Governança, Gestão de Riscos, Programa de Integridade | ✅ | `ENaturezaAcao` |
| **Classificação da ação** | Programada, Reserva, Não programada | ✅ | `EClassificacaoAcao` |
| **POAC** | Plano anual que agrupa ações de controle (pesquisa por ano) | ✅ uso / 🔶 expansão "Plano Operacional Anual de Controle" | `domain/model/Poac`, `PoacController` `/pesquisar-ano`, migration V24 |
| **OS** | Ordem de Serviço: documento que formaliza abertura, designação, exclusão, prorrogação, cancelamento ou substituição em uma ação | ✅ | `OrdemServico`, `EModeloOrdemServico` |
| **OSI** | Variante usada em tabelas e situações (`tb_assinatura_osi`, `OSI_EMITIDA`) | ✅ uso / ❓ expansão (OS Interna? de Inspeção?) | migrations V13, V20, V21; `ESituacao` |
| **OS Genérica** | OS não vinculada a ação de controle, com artigos, descrições de fase e anexos livres | ✅ | `OrdemServicoGenerica`, migrations V26–V31, V50–V51 |
| **Fase / Descrição de fase** | Etapas da ação (planejamento, execução etc.) com datas e duração na OS | ✅ | `Fase`, `FaseOrdemServico`, `DescricaoFaseAcao` |
| **Prorrogação** | OS que estende prazo de uma fase de uma OS de abertura assinada | ✅ | `ProrrogacaoOrdemServico`, `CriarProrrogacaoOrdemServico` |
| **SUBCI** | Papel/perfil do titular que assina as OS; tem substitutos com vigência | ✅ uso / 🔶 expansão "Subcontrolador(ia) de Controle Interno" | `Subci`, `SubciSubstituto`, role `ROLE_SUBCI` |
| **UAI** | Unidade de Auditoria Interna; sua sigla compõe o número oficial da OS. ⚠️ Apesar do nome do método, o sequencial é calculado só **por ano** (ver [[01-Sistemas/SICI/Backend/02-Dominio/SICI-Backend-Banco-e-Migrations|Banco-e-Migrations]]) | ✅ | `UnidadeAuditoriaInterna`, `NumeracaoRepositoryPort.obterProximoSequencialPorUaiEAno`, `NumeracaoRepository.findMaxSequencialByAno` |
| **Unidade auditada** | Órgão/unidade objeto da ação | ✅ | `UnidadeAuditada` |
| **Área executora** | Área da UAI que executa a ação | ✅ | `AreaExecutora`, `ListarAreaExecPorAuditInterna` |
| **PPA** | Programa de governo e objetivos associados à ação | ✅ uso / 🔶 expansão "Plano Plurianual" | `ProgramaGoverno`, `ObjetivosPPA` |
| **Perfis / roles** | SUBCI, COORDENADOR, DIRETOR, AUDITOR (+ `SUPER_USUARIO` técnico) | ✅ | `@PreAuthorize` nos controllers, `JwtAuthenticationConverterCustom` |
| **Código verificador** | HMAC-SHA256 que permite validar um documento assinado | ✅ | `application/utils/VerifyCode`, `/assinaturas/validacao` |
| **RP, RPM, RM** | Marcos da situação da ação (`RP_EMITIDO`, `RPM_EMITIDO`, `FINALIZADO_COM_RM`) | ✅ uso / ❓ expansão (relatório preliminar / de monitoramento?) | `ESituacao` |

Siglas a confirmar com o time estão listadas em [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Pendencias|Pendencias]].
