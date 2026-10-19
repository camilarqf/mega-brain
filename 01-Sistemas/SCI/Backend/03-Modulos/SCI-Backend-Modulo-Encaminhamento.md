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
  - encaminhamento
sources:
  - src/SCI.Domain/GestaoAdmissibilidade/Entities/Encaminhamento.cs
  - src/SCI.Domain/GestaoAdmissibilidade/Rules/Encaminhamento
  - src/SCI.Application/UseCases/GestaoEncaminhamento
  - src/SCI.Application/EventHandlers/EncaminhamentoAceitoEventHandler.cs
  - src/SCI.Api/Controllers/EncaminhamentoController.cs
---
# SCI Backend — módulo Encaminhamento

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Documentar o envio do processo de admissibilidade a outras unidades e as respostas do destinatário.

## Evidências
- `ProcessoAdmissibilidade.{Encaminhar, EnviarEncaminhamentos, AceitarEncaminhamento, DevolverEncaminhamento, RejeitarDevolucaoEncaminhamento, ReprovarEncaminhamento, Reencaminhar}`, entidade `Encaminhamento`, `EncaminhamentoAceitoEventHandler`, regras `Encaminhamento*Apto*`.

## Informações confirmadas
- ✅ **Pré-condição**: só processo em `AF` (aguardando finalização) pode ser encaminhado (`ProcessoAdmissibilidadeAptoParaEncaminhamento`: "Este processo de admissibilidade não está apto para encaminhamento").
- ✅ **Encaminhar** (`POST /encaminhamento`, AnalistaAdmissibilidade): processo → `AE`; para cada unidade destino cria `Encaminhamento` ou reencaminha o existente (mesmo destinatário, não excluído).
- ✅ **Enviar** (`/enviar`, ApoioCorrecional): cada encaminhamento em andamento → `EO` (aguardando ciência da autoridade); em seguida `FinalizarEncaminhamento` → processo `PC` e evento `ProcessoAdmissibilidadeConcluido`.
- ✅ **Reprovar** (`/reprovar`, ApoioCorrecional): encaminhamentos em andamento → `RE` (com observação); processo volta a `AF`.
- ✅ **Aceitar** (`/aceitar`, AutoridadeCorrecional): só se `EO` ("deve estar 'Enviado' para ser confirmado") → `AP`; evento `EncaminhamentoAceito` → `EncaminhamentoAceitoEventHandler` cria um **novo processo de admissibilidade na unidade destino** (`CriarProcessoAdmissibilidadeOrgaoDestino`) a partir da mesma demanda e o vincula ao encaminhamento (`ProcessoDestino`).
- ✅ **Devolver** (`/devolver`, AutoridadeCorrecional): só se `EO` → `AD` com justificativa.
- ✅ **Rejeitar devolução** (`/rejeitar-devolucao`): encaminhamento → `RE` e novo encaminhamento pendente é criado com a justificativa.
- ✅ Consultas: devolvidos, recebidos, enviados pela unidade, por processo.
- ✅ Anexos de encaminhamento (`AnexoEncaminhamento`, `TB_ANEXOS_ENCAMINHAMENTO`).

## Inferências e limitações
- 🔶 Regras `EncaminhamentoAptoParaAprovar*` e `ReprovarEncaminhamento` foram lidas por nome/uso; o caso de uso `AprovarEncaminhamento` não foi lido.
- 🔶 A diferença exata entre `Reprovar` (RE por observação) e `RejeitarDevolucao` (também RE) deve ser validada com o time.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Processo de Admissibilidade]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Enums e estados]]

## Pendências e próximo passo
- Ler `AprovarEncaminhamento` e `ConfirmarEncaminhamento`.
