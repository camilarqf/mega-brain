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
  - denuncia
  - demanda
sources:
  - src/SCI.Domain/GestaoAdmissibilidade/Entities/Denuncia.cs
  - src/SCI.Domain/GestaoAdmissibilidade/Entities/Demanda.cs
  - src/SCI.Application/UseCases/GestaoIntegracao
  - src/SCI.Application/UseCases/CriarDemanda
  - src/SCI.Application/UseCases/TratarDemanda
  - src/SCI.Application/EventHandlers/DemandaTratadaEventHandler.cs
  - src/SCI.IntegrationServices/EventConsumers/DenunciaRegistradaConsumer.cs
  - src/SCI.Api/Controllers/DenunciaController.cs
  - src/SCI.Api/Controllers/DemandaController.cs
---
# SCI Backend — módulo Denúncia e Demanda

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Documentar a entrada de trabalho no SCI: denúncias recebidas e demandas tratadas.

## Evidências
- Arquivos em `sources`. Símbolos: `Denuncia.Criar/Numerar/Aceitar/Recusar`, `Demanda.Criar/Tratar`, `CriarDenunciaHandler`, `AceitarDenunciaHandler`, `RecusarDenunciaHandler`, `TratarDemandaHandler`, `DemandaTratadaEventHandler`.

## Informações confirmadas
### Denúncia
- ✅ Nasce do consumo do evento `denuncia-registrada` ([[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|integração]]): `CriarDenunciaHandler` cria `Denuncia` com origem `ParticipaDf`, `Status = AA`, numera com sequencial + número do vínculo `PARTICIPA_DF` da unidade destino (`Identificador = <prefixo> <vínculo>.<sequencial:D5>/<ano>`).
- ✅ **Regra**: se já existe denúncia com o mesmo identificador externo, o evento é ignorado (log de aviso).
- ✅ **Regra**: se a unidade destino não tem vínculo habilitado no SCI, o consumidor publica `denuncia-recusada` com o motivo "A unidade referenciada na denúncia não está habilitada no SCI" e não cria a denúncia.
- ✅ `POST /denuncia/aceitar` e `/recusar` (perfil AutoridadeCorrecional): `Aceitar()` → `AC` e evento `DenunciaAceita`; `Recusar(motivo)` → `RE`. Os handlers de evento publicam `denuncia-aceita` / `denuncia-recusada` com usuário e identificador processual.
- ✅ `GET /denuncia/get-all` lista denúncias (consulta).

### Demanda
- ✅ Criação e atualização por ApoioCorrecional/Administrador (`POST/PUT /demanda`), com anexos (`adicionar-anexo`, `remover-anexo`), assunto, descrição, tipo de demandante, período e tipo de agente envolvido; estado inicial `AA`.
- ✅ **Tratamento** (`POST /demanda/tratar`, AutoridadeCorrecional): `Demanda.Tratar(relatorId, tipoTratamento)` define o status final — `CPA` (processo de admissibilidade), `CM` (MPTCE) ou `CPAM` (ambos). Demanda já em `CPA`, `CM` ou `CPAM` não pode ser tratada de novo (`InvalidSciOperationException`: "não está disponível para ser distribuída").
- ✅ Efeito: o evento `DemandaTratada` aciona `DemandaTratadaEventHandler`, que cria o processo de admissibilidade (`IProcessoAdmissibilidadeFactory.CriarProcessoAdmissibilidade`) para `CPA` e `CPAM`; para `CM` nada é criado no SCI.
- ✅ O processo nasce `AD` (sem relator) ou `AC` (com relator) — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Processo de Admissibilidade]].

## Inferências e limitações
- ❓ Não há no código lido nenhuma ligação entre `Denuncia` aceita e `Demanda` (a demanda tem `OrigemDenuncia`, mas não referencia a denúncia; `Aceitar()` só muda o status e publica o evento). Em 2026-10-19 o usuário informou que **não sabe se a funcionalidade foi concluída**; tratar como possível funcionalidade incompleta, não como regra.
- 🔶 A integração com o MPTCE não existe no código (apenas o status).
- Cobertura parcial: handlers de criar/atualizar demanda lidos por nome.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo denúncia → admissibilidade]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Enums e estados]] · [[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Confirmar com o time se a conversão denúncia aceita → demanda está prevista/implementada (ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências]]).
