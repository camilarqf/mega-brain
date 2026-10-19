---
type: module
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - backend
  - modulo
  - pip
  - diligencia
sources:
  - src/SCI.Domain/GestaoPIP/Entities/PIP.cs
  - src/SCI.Domain/GestaoPIP/Rules
  - src/SCI.Application/UseCases/GestaoPip
  - src/SCI.Application/UseCases/AssinarMinuta
  - src/SCI.Application/UseCases/CriarDiligencia
  - src/SCI.Application/EventHandlers/MinutaAssinadaPorAutoridadeEventHandler.cs
  - src/SCI.Application/EventHandlers/ProcessoAdmissibilidadeConcluidoEventHandler.cs
  - src/SCI.Api/Controllers/PipController.cs
  - src/SCI.Api/Controllers/DiligenciaController.cs
---
# SCI Backend — módulo PIP (Processo Investigativo Preliminar)

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Documentar o PIP: criação, ato de instauração (minuta), diligências, análise, revisões, relatório e finalização.

## Evidências
- `PIP` (herda `Processo`), regras `GestaoPIP/Rules/*`, handlers em `UseCases/GestaoPip/*`, `PipController`, `DiligenciaController`.

## Informações confirmadas
### Criação
- ✅ Automática, ao concluir um processo de admissibilidade cuja análise aprovada recomenda `PIP` ou `IPF` para algum envolvido e cuja unidade tem configuração de PIP — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Admissibilidade]]. Estado inicial: `AguardandoDesignacaoInvestigadores`.
- ✅ `PipFeatures.Criar` (`Pip.Criar`) existe como constante e flag `false` em `appsettings.json`, mas **não encontrei uso** dela (nenhum `IFeatureManager` nem `FeatureGate`).

### Ato de instauração
| Passo | Efeito | Regra |
|---|---|---|
| Designar relatoria (`POST /pip/designar-relatoria`, GestorPip) | `ACM` (aguardando conclusão da minuta) | só em `AguardandoDesignacaoInvestigadores` ("O status atual do PIP não permite designação de relatoria"); ao menos um relator |
| Redistribuir relatoria | evento `RelatoriaPipRedistribuida` | GestorPip/Apoio/Autoridade, com justificativa |
| Atualizar minuta (ApoioCorrecional) | `ADA` (aguardando despacho da autoridade); atualiza `AtoCompetenciaAutoridade` | |
| Assinar minuta | assinatura da AutoridadeCorrecional; evento `MinutaAssinadaPorAutoridade` | |
| Handler da minuta assinada | `ARS` (aguardando registro no SEI) | `MinutaAptaParaEnviarSei`: tem assinatura da autoridade e estado `ADA` |
| Atualizar dados do SEI | grava `NumeroProcessoSei` e `DataDodf`; vai para `EC` (em cadastro) | |
| Concluir ato de instauração (AutoridadeCorrecional) | evento `AtoInstauracaoConcluido` | |

### Cadastro, análise e revisão
- ✅ Cadastro: atualizar (`PUT atualizar-cadastro`), concluir (`EC` → `EA`, evento `CadastroProcessoInvestigativoPreliminarConcluido`, que cria a `AnalisePip`), reabrir (`EC`). Perfil InvestigadorPip.
- ✅ `AnalisePip` com itens por envolvido elegível, notas (AssessorAutoridade), conclusão e revisão: `TipoRevisaoPip` = Preliminar (RevisorPip, `ERR`), Técnica (GestorPip, `ERG`), Final (AutoridadeCorrecional, `ERA`).
- ✅ **Diligências**: criar, atualizar, listar por PIP, vincular/desvincular da "matriz" (`DiligenciaAptaParaVinculoMatriz` / `DesvinculoMatriz`, `DiligenciaComDadosBasicosValidos`); endpoints exigem só autenticação.

### Relatório e finalização
- ✅ Fim da revisão: `FinalizarRevisaoPip` aprova a análise e o PIP vai a `AAI` (assinatura do investigador).
- ✅ Assinatura em cadeia (`OrquestrarAssinatura`): `AAI` (investigador) → `AAR` (revisor) → `AAG` (gestor) → `AAA` (autoridade), conforme as revisões ativas da configuração; depois `AF`. Só o perfil do estado atual assina ("Usuário não é o próximo revisor a assinar"); para o investigador, valida que ele pertence à relatoria ativa e que todos os relatores assinem (`PossuiInvestigadorPendenteParaAssinar`).
- ✅ Concluir (InvestigadorPip) → `PC`; finalizar (Apoio/Autoridade) → `FES` e evento `ProcessoInvestigativoPreliminarFinalizado`.

## Inferências e limitações
- 🔶 O papel da "matriz" de diligências (vínculo) não está explicado no código; ver entidade `Diligencia.Vinculada`.
- 🔶 Regras `UsuarioPodeConcluirProcessoInvestigativo` e `UsuarioPodeConcluirRevisao` lidas só por nome.
- Visões por perfil (`visao-*`) são consultas SQL não detalhadas.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Ciclo-do-PIP|Ciclo do PIP]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Documentos-e-Assinaturas|Documentos e assinaturas]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Estados]]

## Pendências e próximo passo
- Ler as regras de usuário (conclusão) e as consultas das visões; confirmar o significado de "matriz".
