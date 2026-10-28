---
type: flow
aliases:
  - "SCI Backend — ciclo do PIP"
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
sources:
  - src/SCI.Domain/GestaoPIP/Entities/PIP.cs
  - src/SCI.Application/UseCases/GestaoPip
  - src/SCI.Application/EventHandlers
---
# SCI Backend — ciclo do PIP

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Sequência de estados do PIP, do nascimento à finalização.

## Evidências
- `PIP`, `Rules/*`, handlers; detalhes em [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|módulo PIP]].

## Informações confirmadas
```
(processo de admissibilidade concluído com recomendação PIP/IPF)
 → AguardandoDesignacaoInvestigadores
 → [designar relatoria — GestorPip] ACM
 → [atualizar minuta — Apoio] ADA
 → [assinar minuta — Autoridade] ARS (aguardando registro no SEI)
 → [atualizar dados do SEI] EC (em cadastro)
 → [concluir cadastro — Investigador] EA (em análise)
 → [concluir análise] revisões: ERR (Revisor) → ERG (Gestor) → ERA (Autoridade), conforme a configuração
 → [fim da revisão] AAI → AAR → AAG → AAA (assinaturas do relatório)
 → AF (aguardando finalização)
 → [concluir — Investigador] PC  →  [finalizar — Apoio/Autoridade] FES
```
- ✅ A reprovação de revisão gera o evento `RevisaoPipReprovada` (o efeito sobre o estado do PIP não foi lido).
- ✅ Reabertura do cadastro volta a `EC` (`ReabrirCadastro`).
- ✅ Diligências podem ser criadas durante o ciclo ([[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]]).

## Inferências e limitações
- 🔶 O trecho `concluir análise → revisões` foi montado a partir de `CriarRevisaoPip` e `AnalisePipConcluidaEventHandler` (lidos por nome); validar contra o código na próxima revisão.
- 🔶 Não está claro se `AF` → `PC` exige alguma regra além do perfil (`ProcessoInvestigativoPreliminarAptoParaConcluir` não foi lida).

## Relacionamentos
- [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo anterior]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Estados]]

## Pendências e próximo passo
- Ler as regras `ProcessoInvestigativoPreliminarAptoParaConcluir/Finalizar`.
