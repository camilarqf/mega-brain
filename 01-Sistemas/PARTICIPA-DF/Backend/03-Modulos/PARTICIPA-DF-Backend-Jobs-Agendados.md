---
type: module
aliases:
  - "Jobs agendados"
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
sources:
  - src/OuvDF.Api/Controllers/Shared/JobController.cs
  - src/OuvDF.Api/Startup.cs
  - src/OuvDF.Shared/JobManager/IJob.cs
  - src/OuvDF.Shared/JobManager/JobRegister.cs
  - src/OuvDF.Shared/Jobs
  - src/OuvDF.ServicoOuvidoria/Jobs
  - src/OuvDF.ServicoInformacaoCidadao/Jobs
  - src/OuvDF.ServicoOuvidoria/Infra/Queries/ConsultarManifestacoesVencidas/ConsultarManifestacoesVencidasHandler.cs
  - src/OuvDF.ServicoInformacaoCidadao/Infra/Queries/_Extensions/PedidoQueryExtensions.cs
  - src/OuvDF.Shared/Infra/Queries/ConsultarUsuariosFalecidos/ConsultarUsuariosFalecidosHandler.cs
---

# Jobs agendados

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Glossario|Glossário]]

## Objetivo
Documentar as 10 rotinas automáticas (jobs): como são acionadas, o que consultam e o efeito que produzem.

## Evidências
`Startup.ConfigureServices` (`AddJob<…>` ×10), `JobController`, classes `*Job` e handlers das consultas citadas em `sources`. Commit `4901ad5`.

## Informações confirmadas

### Mecanismo
- ✅ Contrato `IJob { string Name; Task Execute(); }`; `AddJob<T>` registra `T` como `IJob` transiente.
- ✅ Disparo: `GET /jobs/v2/{jobName}` executa o job cujo `Name` coincide (`JobController.NewProcessNotification`). Não há agendador no código: nenhum `IHostedService`/Timer e `Cronos` não é usado (🔶 o disparo vem de um agendador externo, não identificado ❓).
- ✅ Cada job consulta os alvos por MediatR, registra a contagem em log (nível *Warning*) e envia um comando por item, em sequência.
- 🔶 `GET /jobs/{jobName}` (v1) usa um dicionário `_jobs` criado vazio e nunca preenchido: qualquer chamada resultaria em `KeyNotFoundException`.
- 🔶 Job com nome inexistente: `FirstOrDefault` devolve `null` e `job.Execute()` lança `NullReferenceException` (resposta `500`).
- ❓ O `JobController` não tem `[Authorize]` na classe nem nas ações. Se a autenticação é exigida globalmente (SDK `UseCgdfSecurity`) não foi verificado. Registrar no lote 2.

### Os 10 jobs
| Nome (`/jobs/v2/…`) | Classe | Alvo (consulta) | Efeito (comando) |
|---|---|---|---|
| `atualizar-manifestacao-para-vencida` | `AtualizarSituacaoManifestacaoParaVencidaJob` | manifestações em situações `SituacaoManifestacao.NoPrazo()` cujo vencimento (ou a maior data de prazo pendente que marca vencida) é menor que `DateTime.Today` | `AtualizarManifestacaoParaVencida` |
| `atualizar-manifestacao-para-vencida-apos-prorrogacao` | `AtualizarSituacaoManifestacaoParaVencidaAposProrrogacaoJob` | mesma consulta, situação `Prorrogada` | `AtualizarManifestacaoParaVencidaAposProrrogacao` |
| `prorrogar-prazo-pedidos-vencidos` | `ProrrograrPrazoPedidoVencidoJob` | pedidos com `PrazoVigente` não nulo, fora do prazo vigente (`DataTermino < DateTime.Now`) e não respondidos | `ProrrogarPrazoPedidoVencido` |
| `prorrogar-prazo-recursos-nao-respondidos` | `ProrrogarPrazoRecursosNaoRespondidosJob` | pedidos fora do prazo vigente em recurso de 1ª ou 2ª instância | `ProrrogarPrazoRecursoNaoRespondido` |
| `concluir-pedidos-respondidos-com-prazo-recurso-expirado` | `ConcluirPedidoRespondidoComPrazoDeRecursoExpiradoJob` | pedidos com prazo vigente expirado e em situação de conclusão (`EmSituacaoDeConclusao`) | `ConcluirPedidoRespondidoComPrazoDeRecursoExpirado` |
| `registrar-notificacao-omissao-resposta` | `RegistrarNotificacaoDeOmissaoDeRespostaJob` | pedidos `Prorrogado` com prazo final menor que a data | `RegistrarNotificacaoOmissaoResposta` por pedido; depois `NotificarOperadoresDaUnidadeAcercaDeOmissaoResposta` **por unidade** |
| `registrar-notificacao-omissao-resposta-cgdf` | `RegistrarNotificacaoDeOmissaoDeRespostaCGDFJob` | pedidos `ReclamacaoOrgao` com prazo final menor que a data | `RegistrarNotificacaoOmissaoRespostaCGDF` por pedido; depois uma única `NotificarOperadoresDaUnidadeSuperiorAcercaDeOmissaoResposta` |
| `desabilitar-operadores-sic-com-acesso-expirado` | `DesabilitarOperadoresSicComAcessoExpiradoJob` | operadores SIC **ativos** com `DataUltimoLogin` anterior a hoje − 90 dias (`DiasSemAcesso = 90` fixo) | `DesabilitarOperadorSicComAcessoExpirado` |
| `desabilitar-operadores-so-com-acesso-expirado` | `DesabilitarOperadoresSoComAcessoExpiradoJob` | operadores SO com 90 dias sem acesso (`DiasSemAcesso = 90`); handler SO não lido (🔶 análogo ao SIC) | `DesabilitarOperadorSoComAcessoExpirado` |
| `bloquear-usuario-falecido` | `BloquearUsuariosFalecidosJob` | até 100 pessoas físicas sem nenhum `BloqueioUsuario` e cujo CPF consta em `UsuarioFalecido` | `BloquearUsuario` (motivo `FALECIMENTO`, operador = `SharedSettings.IdOperadorSistema`) |

### Situação resultante nos jobs de pedidos (lote 5)
`prorrogar-prazo-pedidos-vencidos` → `Prorrogado`; `registrar-notificacao-omissao-resposta` → `ReclamacaoOrgao`; `…-cgdf` → `ReclamacaoCgdf`; `prorrogar-prazo-recursos-nao-respondidos` → `NaoRespondidoPrimeira/SegundaInstancia`; `concluir-pedidos-respondidos-…` → `Concluido*`/`Vencido*`. Ver [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Fluxo-Omissao-de-Resposta]] e [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]].

### Regras observáveis (ver o código para confirmar a cada alteração)
- ✅ Inatividade de operadores: **90 dias** fixos no código (não configurável).
- ✅ Limite de **100** usuários por execução no bloqueio de falecidos.
- ✅ Um usuário que já teve **qualquer** bloqueio deixa de ser candidato (`WhereNotExists BloqueioUsuario`).

## Inferências e limitações
- 🔶 Datas inconsistentes: os jobs de pedidos recebem `IApplicationDateTime.Current` em `Data`, mas `ForaDoPrazoVigente()` compara com `DateTime.Now`; o job de manifestação usa `DateTime.Today`. Em ambientes com `ApplicationDateTime` forçada o comportamento difere por job.
- 🔶 `GetIdUsuarioComCPFFalecidoAtualizadoHoje` não filtra por data apesar do nome.
- 🔶 O `.Result` em tarefa assíncrona no job de falecidos pode bloquear a thread.
- ❓ Periodicidade dos disparos e identidade do agendador.
- ❓ Regras dos comandos de efeito (ex.: duração da prorrogação, destinatários de e-mail) ficam nos lotes 4 e 5.
- ❓ Predicados `NaoRespondido`, `EmSituacaoDeConclusao`, `SituacaoManifestacao.NoPrazo()` não foram lidos.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Workflows-e-Consumidores|Workflows-e-Consumidores]]

## Pendências e próximo passo
- Lotes 4 e 5: detalhar as regras de prazo, prorrogação e omissão em notas de fluxo e regra.
- Lote 2: confirmar a exigência de autenticação em `/jobs/*`.
