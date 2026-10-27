---
type: module
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
updated: 2026-10-23
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
  - src/SCI.IntegrationServices/EventConsumers/DemandaCriadaPorDenunciaConsumer.cs
  - src/SCI.Application/EventHandlers/DenunciaAceitaEventHandler.cs
  - src/SCI.Domain/GestaoAdmissibilidade/Rules
  - src/SCI.Domain/Organizacional/Rules/UnidadeAptaParaCriarDemanda.cs
  - src/SCI.Infrastructure.Projections/Queries/Denuncia
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
- ✅ Nasce do consumo do evento `denuncia-registrada` ([[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Eventos|integração]]): `CriarDenunciaHandler` cria `Denuncia` com origem `ParticipaDf`, numera com sequencial + número do vínculo `PARTICIPA_DF` da unidade destino (`Identificador = <prefixo> <vínculo>.<sequencial:D5>/<ano>`) e grava os **anexos** (`AnexoDenuncia`, só o nome do arquivo; o relatório `ArquivoReferencia` e os `Anexos` do evento são reduzidos a `Path.GetFileName`).
- ✅ **Regra**: se já existe denúncia com o mesmo identificador externo, o evento é ignorado (log de aviso).
- ✅ **Regra**: se a unidade destino não tem vínculo habilitado no SCI, o consumidor publica `denuncia-recusada` com o motivo "A unidade referenciada na denúncia não está habilitada no SCI" e não cria a denúncia.
- ✅ **Sem status na entidade** (desde `29989114`): a denúncia tem `Analise` (`AnaliseDenuncia`: `Status` Aceita/Recusada, `MotivoRecusa?`, `Usuario`). Sem análise = pendente; nas consultas o filtro trata o id `0` como "pendente".
- ✅ `POST /denuncia/aceitar` e `/recusar` (perfil **ApoioCorrecional**; o `UserIdentity` atual vai no comando):
  - Aceitar exige `DenunciaAptaParaAceite` ("A denúncia já foi analisada." se `Analise` já existe) e `UnidadeAptaParaCriarDemanda` ("Não é possível criar demanda: A unidade não possui configuração de processo ativa." se não há configuração de `ProcessoAdmissibilidade`); `Aceitar(usuario)` cria a análise e dispara `DenunciaAceita`.
  - Recusar chama `Recusar(motivo, usuario)`, que cria a análise recusada e dispara `DenunciaRecusada`. O `RecusarDenunciaHandler` **não** aplica `DenunciaAptaParaAceite` (nem outra regra de "já analisada"), pelo código lido.
- ✅ **Aceite gera demanda**: `DenunciaAceitaEventHandler` publica `denuncia-aceita` e envia `CriarDemandaPorDenunciaCommand`. O `CriarDemandaPorDenunciaHandler` usa `Demanda.Criar(denuncia, unidade)` (status `CR`, `TipoDemandante` conforme `Identificada`, origem = unidade da denúncia, vínculo à denúncia), numera pelo vínculo padrão da unidade, grava e publica `demanda-criada-por-denuncia`.
- ✅ **Cópia dos anexos**: `DemandaCriadaPorDenunciaConsumer` baixa cada anexo da denúncia no S3 ([[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-S3-Anexos-de-Denuncia|integração S3]]), grava no armazenamento do SCI e adiciona `AnexoDemanda` (ignora o que já foi copiado, por nome e não excluído).
- ✅ Consultas: `GET /denuncia/get-all` (filtros por identificador, protocolo, status, período; sempre limitado à unidade do usuário), `GET /denuncia/{id}` (detalhe com status, motivo de recusa e anexos), `GET /denuncia/{denunciaId}/download?nomeArquivo=` (baixa o anexo direto do S3).

### Demanda
- ✅ Criação manual e atualização por ApoioCorrecional/Administrador (`POST/PUT /demanda`), com anexos (`adicionar-anexo`, `remover-anexo`), assunto, descrição, tipo de demandante, período e tipo de agente envolvido; estado inicial manual `AA`.
- ✅ **Demanda vinda de denúncia** nasce `CR` (Criada), com `DocumentoOrigem`, `OrigemDenuncia`, `Assunto` e `Descricao` nulos (agora opcionais no domínio e no banco). Ao atualizar, `ConcluirCadastroSeCompleta` passa `CR → AA` quando `PossuiDadosObrigatorios` (documento de origem, origem da denúncia, assunto, descrição, demandante e tipo de agente definidos).
- ✅ **Tratamento** (`POST /demanda/tratar`, AutoridadeCorrecional): `Demanda.Tratar(relatorId, tipoTratamento)` define o status final — `CPA` (processo de admissibilidade), `CM` (MPTCE) ou `CPAM` (ambos). Regra `DemandaAptaParaTratamento`: só `AA` ou `EA` ("A demanda não está disponível para ser distribuída."); logo, uma demanda em `CR` **não** pode ser tratada até ser completada.
- ✅ Listagem (`GET /demanda/get-all`): o filtro de status aceita **vários** status (`StatusIds`); a view traz `protocoloRelacionadoDenuncia` e usa `LEFT JOIN` em assunto e origem (demandas sem esses campos aparecem).
- ✅ Efeito do tratamento: `DemandaTratada` aciona `DemandaTratadaEventHandler`, que cria o processo de admissibilidade (`IProcessoAdmissibilidadeFactory.CriarProcessoAdmissibilidade`) para `CPA` e `CPAM`; para `CM` nada é criado no SCI.
- ✅ O processo nasce `AD` (sem relator) ou `AC` (com relator) — [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Processo de Admissibilidade]].

## Histórico
- **Até `8e3c8648` (2026-10-18)**: aceitar/recusar eram do perfil AutoridadeCorrecional e só mudavam `Denuncia.Status` (`AC`/`RE`) e `MotivoRecusa`; não existia ligação denúncia → demanda (o usuário não sabia se estava concluída); `Tratar` bloqueava só `CPA`/`CM`/`CPAM` por `if` no handler. Substituído pelas regras acima em `29989114` (merge de `release/integracao-sci-participa`).

## Inferências e limitações
- 🔶 A integração com o MPTCE não existe no código (apenas o status).
- 🔶 O aceite envia o comando de criar a demanda **dentro do handler do evento de domínio**, depois do `SaveChanges` do aceite: se a criação falhar, a denúncia fica aceita sem demanda (nenhuma compensação vista). O handler do aceite checa `UnidadeAptaParaCriarDemanda` antes para reduzir esse caso.
- 🔶 `DemandaCriadaPorDenunciaConsumer` não trata falha de download do S3; o comportamento de reentrega depende do SDK. Anexos já copiados não são duplicados na repetição.
- ❓ Motivo da troca de perfil (Autoridade → Apoio) em aceitar/recusar não consta no código.
- Cobertura parcial: handlers de criar/atualizar demanda lidos por nome; testes novos apenas listados (ver [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Testes-e-Cobertura|Testes]]).

## Relacionamentos
- [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo denúncia → admissibilidade]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Enums e estados]] · [[01-Sistemas/SCI/Backend/06-API/SCI-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- ✅ Resolvida em 2026-10-23 (`29989114`): a conversão denúncia aceita → demanda existe no código (ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências]]). Falta confirmar com o time o motivo da troca de perfil e o tratamento de falha na criação da demanda.
