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
  - ordem-servico
sources:
  - api/ordemServico/OrdemServicoController.java
  - application/service/ordemServico/OrdemServicoServiceImpl.java
  - application/usecase/ordemServico/*
  - application/usecase/coordenador/SubstituirCoordenador.java
  - domain/model/OrdemServico.java
  - infrastructure/persistence/repository/AuditorOrdemServicoRepository.java
  - infrastructure/persistence/repository/CoordenadorRepository.java
---

# Ordem de Serviço (OS de Ação de Controle)

Voltar: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] · Fluxo: [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Ciclo-de-Vida-OS|Fluxo-Ciclo-de-Vida-OS]] · Relacionado: [[01-Sistemas/SICI/Backend/03-Modulos/Prorrogacao-e-Cancelamento|Prorrogacao-e-Cancelamento]], [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]], [[01-Sistemas/SICI/Backend/02-Dominio/Enums-e-Estados|Enums-e-Estados]], [[01-Sistemas/SICI/Backend/02-Dominio/Modelo-de-Dominio|Modelo-de-Dominio]], [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]]

> Uma OS formaliza um ato sobre uma [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]]: abertura, designação ou exclusão de membros, prorrogação de fases, substituição de coordenador ou cancelamento. A OS só produz efeito sobre equipe e situação da ação **quando é assinada** (ver "Efeitos na assinatura").

## Endpoints — `/os-acao-controle` ✅
Fonte: `api/ordemServico/OrdemServicoController.java`

| Método | Rota | Roles (`@PreAuthorize`) | Delegação |
|---|---|---|---|
| POST | `/salvar-os/{acaoControleId}` | COORDENADOR, AUDITOR, SUBCI, DIRETOR | `OrdemServicoServiceImpl.salvarOsi` → `SalvarOrdemServico.salvarPorAcaoControle` |
| GET | `/listar` (paginado) | SUBCI | `ListarOrdemServico` |
| GET | `/listar-os/{idAcaoControle}` | SUBCI, COORDENADOR, AUDITOR, DIRETOR | `PesquisarOrdemServicoPorAcaoControle` |
| GET | `/pesquisar?id=` | SUBCI, DIRETOR | `PesquisarOrdemServico` |
| PUT | `/atualizar/{id}` | COORDENADOR, AUDITOR, SUBCI, DIRETOR | `AtualizarOrdemServico` |
| PUT | `/alterarStatusOs/{id}` | SUBCI, COORDENADOR, AUDITOR, DIRETOR | `AlterarStatusOrdemServico` |
| DELETE | `/excluir/{id}` | SUBCI, COORDENADOR, DIRETOR | `ExcluirOrdemServico` |
| POST | `/{id}/fases` | **nenhuma** (só autenticado) | `SalvarFaseOrdemServico` |
| POST | `/{idOrdemServicoBase}/prorrogacoes` | **nenhuma** | `CriarProrrogacaoOrdemServico` — ver [[01-Sistemas/SICI/Backend/03-Modulos/Prorrogacao-e-Cancelamento|Prorrogacao-e-Cancelamento]] |
| PUT | `/{idOrdemServico}/prorrogacoes` | **nenhuma** | `AtualizarProrrogacaoOrdemServico` |
| POST | `/cancelar-os/{id}` (`id` = ação de controle) | SUBCI, COORDENADOR, DIRETOR | `CancelarOrdemServico` |
| PUT | `/cancelamento/{idOrdemServico}/{idCancelamento}` | **nenhuma** | `OrdemServicoServiceImpl.atualizarJustificativaCancelamento` |
| GET | `/gerar-pdf?id=` | **nenhuma** | PDF assinado armazenado ou minuta gerada no próprio controller |
| GET | `/validar-data-prorrogacao` | **nenhuma** | consulta direta ao `ProrrogacaoOrdemServicoRepositoryPort` pelo controller |

## Criação — `SalvarOrdemServico.salvarPorAcaoControle` ✅
Fluxo (método anotado com `@Transactional`):

1. Recebe uma **lista** de `OrdemServicoRequest`, mas usa **apenas `requests.getFirst()`**; os demais itens são ignorados.
2. Carrega a ação de controle e o `TipoOrdemServico` (`ResourceNotFoundException` se não existirem) e as OS já existentes da ação.
3. `validarPermissaoSalvarOrdemServico`: CANCELAMENTO exige SUBCI, COORDENADOR ou DIRETOR; os demais modelos também aceitam AUDITOR.
4. Resolve o coordenador: em SUBSTITUICAO é o `coordSubstituto`; nos demais, o `coordenador` do request.
5. `OrdemServico.validarCriacao` → abertura única, designação/exclusão sem coordenador e membros juntos, coordenador obrigatório na abertura (ver [[01-Sistemas/SICI/Backend/02-Dominio/Modelo-de-Dominio|Modelo-de-Dominio]]).
6. SUBSTITUICAO: `SubstituirCoordenador.verificarSubstituicao` exige um coordenador ativo na ação e que o coordenador atual informado esteja vinculado a uma OS da ação.
7. Cria a OS com status **CRIADA** e `dtCriacao = now()`.
8. Vínculos (todos **pendentes** até a assinatura):
   - **EXCLUSAO** → `marcarExclusao`: grava `ID_OS_EXCLUSAO` e `DT_INICIO_EXCLUSAO` nos vínculos ativos do auditor em OS da mesma ação que não sejam de exclusão.
   - **demais** → `AuditorOrdemServico.criar(..., ativo = false, ...)` para cada auditor.
   - **SUBSTITUICAO** → `registrarSubstituicaoTemporaria` + coordenador gravado com `ativo = false`.
   - Coordenador (exceto SUBSTITUICAO) gravado com `ativo = true`.
9. Grava as fases (`FaseOrdemServico`: fase, descrição, datas e duração).

## Efeitos na assinatura ✅
Fonte: `AssinarOrdemServico.executar` (detalhe em [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]])

| Modelo | Efeito ao assinar |
|---|---|
| ABERTURA | ação → `ESituacao.OSI_EMITIDA`; `efetivarDesignacao` (`IN_ATIVO = 1` nos auditores da OS) |
| DESIGNACAO | `efetivarDesignacao` |
| EXCLUSAO | `efetivarExclusao` (`IN_ATIVO = 0` nos vínculos marcados com essa OS de exclusão) |
| SUBSTITUICAO | `efetivarSubstituicaoCoordenador`: inativa o coordenador ativo e ativa o substituto |
| CANCELAMENTO | todas as outras OS da ação que não estejam canceladas → CANCELADA (`OrdemServico.cancelar`) |
| PRORROGACAO | nenhum efeito extra; as datas prorrogadas já estão em `TB_PRORROGACAO_ORDEM_SERVICO` |

Em todos os casos: status → ASSINADA, numeração oficial, PDF com QR Code e código verificador.

## Atualização — `AtualizarOrdemServico.atualizar` ✅
- Bloqueia se já existe assinatura com data ou se o status é ASSINADA (`OsAssinadaNaoPodeSerAtualizadaException`).
- O `idTipoOrdemServico` vem do request, então **o modelo da OS pode ser trocado** na atualização.
- EXCLUSAO exige `dtInicioExclusao`; DESIGNACAO exige `dtInicioDesignacao`.
- EXCLUSAO: compara os excluídos atuais com o request, remove vínculos que saíram (`removerVinculoExclusaoAtualizacao`) e marca exclusão para os novos.
- DESIGNACAO: compara os designados atuais com o request, apaga vínculos que saíram (`DELETE` em `TB_AUDITOR_TB_ORDEM_SERVICO`) e cria os novos com `ativo = false`.
- ABERTURA: auditores adicionados recebem `DT_INICIO_DESIGNACAO = hoje`.
- Ao final, `AtualizarDatasAuditorOrdemServico` regrava as datas de designação/exclusão do request.

## Mudança de status — `AlterarStatusOrdemServico` ✅
- Delegação direta para `OrdemServico.alterarStatusOs` (máquina de estados de [[01-Sistemas/SICI/Backend/02-Dominio/Enums-e-Estados|Enums-e-Estados]]).
- Contém um `if` vazio (tipo 1 + status 4) sem efeito.
- ⚠️ Não há regra de quem pode aplicar cada transição: qualquer um dos 4 perfis pode enviar `status = ASSINADA` para uma OS ENVIADA. A OS fica **ASSINADA sem documento, assinatura nem numeração**, e isso satisfaz as checagens baseadas em `isAssinada()`, como a pré-condição de prorrogação.

## Exclusão — `ExcluirOrdemServico.excluir` ✅
- Bloqueia se há assinatura no documento da OS (`OsAssinadaNaoPodeSerExcluidaException`).
- EXCLUSAO → `removerVinculoExclusao`; SUBSTITUICAO → `excluirOsSubstituicao`; PRORROGACAO → apaga as prorrogações da OS-base (abertura ou última prorrogação assinada).
- Exclusão física (`ordemServicoRepositoryPort.excluir`).
- O construtor recebe `ProrrogacaoOrdemServicoRepositoryPort` duas vezes.

## Fases ✅
- Criadas junto com a OS (`SalvarOrdemServico.salvarFases`) ou pelo endpoint `/{id}/fases` (`SalvarFaseOrdemServico`).
- ⚠️ `/{id}/fases` não verifica status nem assinatura: aceita fases em OS já assinada ou cancelada.
- Descrição de fase vem de `TB_DESCRICAO_FASE_ACAO` (fase × tipo de ação × natureza) — `BuscarDescricaoFaseAcao`, `DescricaoFaseAcaoController` (`/fase/descricao-fase`).

## Consulta e montagem da resposta ✅
- `OrdemServicoServiceImpl.toResponseEnriquecido` agrega auditores (designados ou excluídos, conforme o modelo), assinatura, numeração e fases prorrogadas (`montarFasesProrrogadas`, `obterIdOsReferenciaProrrogacao`).
- `OrdemServicoServiceImpl` usa `java.lang.module.ResolutionException` (exceção do sistema de módulos da JVM) para "OS não encontrada" e regras de cancelamento. Ela não tem handler em `GlobalExceptionHandler`. 🔶 O status HTTP resultante depende do handler genérico (verificar no lote 6).

## Lacunas de regra identificadas
| # | Lacuna | Evidência | Status |
|---|---|---|---|
| 1 | `OrdemServico.validarCriacaoComBaseNasOrdens` (exige ABERTURA assinada antes de outras OS) **nunca é chamado**. DESIGNACAO, EXCLUSAO e SUBSTITUICAO podem ser criadas sem abertura assinada. | grep sem chamadores; `SalvarOrdemServico` chama só `validarCriacao` | ✅ |
| 2 | Status ASSINADA atingível sem assinatura via `/alterarStatusOs` | `AlterarStatusOrdemServico`, `EStatusOrdemServico.statusPermitidos` | ✅ |
| 3 | Atualização pode trocar o modelo e não reaplica `validarCriacao` (abertura única etc.) | `AtualizarOrdemServico.atualizar` | ✅ |
| 4 | Lista no `POST /salvar-os` processa só o primeiro item; lista vazia → `NoSuchElementException` | `requests.getFirst()` | ✅ |
| 5 | Atualização não bloqueia OS **CANCELADA** (só ASSINADA) | `validarAtualizacaoPermitida` | ✅ |
| 6 | Vários endpoints de escrita sem `@PreAuthorize` | tabela acima | ✅ |
| 7 | `validar-data-prorrogacao` → `NullPointerException` se a fase não tiver data vigente | `novaDataFim.isAfter(dataVigente)` | 🔶 |
| 8 | `SUPER_USUARIO` não aparece em nenhum `hasAnyRole`, então o bypass só acessa endpoints sem `@PreAuthorize` | `JwtAuthenticationConverterCustom`; grep de `SUPER_USUARIO` | ✅ (detalhar no lote 6) |

Registradas também em [[01-Sistemas/SICI/Backend/99-Controle/Pendencias|Pendencias]] e, depois, em [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Debitos-Tecnicos]].
