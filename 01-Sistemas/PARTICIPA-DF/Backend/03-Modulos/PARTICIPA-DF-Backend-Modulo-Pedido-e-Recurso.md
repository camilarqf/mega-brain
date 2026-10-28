---
type: module
aliases:
  - "Módulo Pedido e Recurso (SIC)"
  - "Pedido-e-Recurso"
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
sources:
  - src/OuvDF.Api/Controllers/ServicoInformacaoCidadao
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Entities/Pedido.cs
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Entities/SituacaoPedido.cs
  - src/OuvDF.ServicoInformacaoCidadao/Domain/Commands
  - src/OuvDF.ServicoInformacaoCidadao/Infra/Queries/ConsultarPermissaoPedido/ConsultarPermissaoPedidoHandler.cs
---

# Módulo Pedido e Recurso (SIC)

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Pedido|Fluxo-Registro-de-Pedido]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Fluxo-Omissao-de-Resposta]], [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-do-SIC|Regras-de-Prazo-do-SIC]], [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

## Objetivo
Visão do módulo de Serviço de Informação ao Cidadão: o que é um pedido, quais controllers e comandos existem e como o sistema decide **quem pode fazer o quê** em cada pedido.

## Evidências
Controllers `Controllers/ServicoInformacaoCidadao/*` (10), entidade `Pedido`, `SituacaoPedido`, comandos (35 pastas de `Domain/Commands`), `ConsultarPermissaoPedido`; commit `4901ad5`.

## Informações confirmadas

### Ciclo geral
Cidadão (ou operador em nome dele) registra um pedido para uma ou mais unidades → cada unidade recebe seu pedido (`Recebido`) → um operador assume (`EmAnalise`) e responde (`Respondido`) → o cidadão pode recorrer em até três instâncias → se a unidade não responde, há prorrogação automática e, depois, notificações de omissão ("reclamação") ao órgão e à CGDF → o pedido é concluído por resposta, decisão ou vencimento do prazo de recurso.

### Controllers e capacidades
| Controller | Rota base | Capacidades observadas |
|---|---|---|
| `PedidoController` | `acesso-informacao/pedido` (`[Authorize]`) | registrar (autor) e `por-operador`, consultas por lote/unidade/manifestante/termo, detalhar (unidade e manifestante), itens de filtro, registrar resposta e resposta definitiva (`OperadorSIC`), ações do operador e do autor, remover operador atual, reencaminhar, prorrogar prazo, registrar pedido no SEI, em recurso de 3ª instância e em notificação CGDF, detalhar evento, unidades (anônimo), tipos de sigilo, permite-detalhar, exportar (autor, operador, pedido-usuário) |
| `RecursoController` | `…/recurso` | registrar recurso de 1ª, 2ª e 3ª instâncias (autor), responder 1ª e 2ª, resposta preliminar e decisão da 3ª, tipos de decisão, justificativas |
| `NotificacaoController` | `…/notificacao` (**sem `[Authorize]`**) | registrar omissão de resposta, omissão de resposta CGDF, resposta e decisão da omissão CGDF |
| `FormularioSICController` | `…/formulario` | cadastrar formulário (operador), consultar, atributos, formatos, por assunto (anônimo) |
| `ArquivoController`, `AssuntoController`, `ClassificacaoController`, `FeriadoController`, `QuestionarioController`, `SituacaoController` | — | anexos, assuntos, classificações de resposta, feriados, questionário/pesquisa de satisfação e situações de resposta |

### Comandos de domínio (35)
Registro e fluxo: `RegistrarPedido`, `AtribuirPedidoParaOperador`, `RemoverOperadorAtual`, `ReencaminharPedido`, `ProrrogarPrazoPedido`, `ProrrogarPrazoPedidosVencidos`, `RegistrarRespostaPedido`, `RegistrarRespostaDefinitivaPedido`. Recursos: `RegistrarRecursoPrimeira/Segunda/TerceiraInstancia`, `RegistrarRespostaRecursoPrimeira/SegundaInstancia`, `RegistrarRespostaPreliminarRecursoTerceiraInstancia`, `RegistrarDecisaoRecursoTerceiraInstancia`, `ProrrogarPrazoRecursoNaoRespondido`, `ConcluirPedidosRespondidosComPrazoDeRecursoExpirado`. Omissão: `RegistrarNotificacaoOmissaoResposta`, `RegistrarNotificacaoOmissaoRespostaCGDF`, `RegistrarRespostaPreliminarNotificacaoOmissaoResposta`, `RegistrarDecisaoNotificacaoOmissaoResposta`. SEI: `SolicitarVinculoSei`, `VincularPedidoSei`. Outros: `AnexarArquivo`, `RegistrarArquivo`, `ExcluirArquivoPorOperador`, `EfetuarDownload`, `ValidarArquivoAnexo`, `ChecarVolumeTotalDeArquivos`, `ExportarPedidoEmHtml`, `GravarFeriado`, `GravarFormularioSIC`, `ResponderPesquisa`, `MoverPedidosParaContaLGPD`.

### Permissões por ação (`ConsultarPermissaoPedido`, 21 ações)
Quem age? Operador SIC (`OperadorSIC`) ou o autor (usuário). Abreviações vêm de `AcaoPedidoEnum`.
| Ação | Quem | Condições (resumo) |
|---|---|---|
| Detalhar `DTL_PDD` | operador / autor | operador na unidade do pedido com `ConsultarPedidoDetalhado`, **ou** `ConsultarTodosPedidos`; ou o autor |
| Responder pedido `RPT_PDD` | operador | na unidade, operador atual do pedido, `ResponderPedido`; e (no prazo vigente e situação EmAnalise, ReclamacaoOrgao, ReclamacaoCgdf ou Prorrogado) **ou** situação ReclamacaoOrgao, ReclamacaoCgdf, RespostaPreliminarReclamacaoCGDF ou DecisaoReclamacaoCGDF |
| Responder recurso 1ª / 2ª `RPT_RPI` / `RPT_RSI` | operador | na unidade, operador atual, situação EmRecurso da instância, prazo do recurso vigente, funcionalidade `ResponderRecurso1aInstancia` / `…2a…` |
| Resposta preliminar recurso 3ª `RPP_RTI` | operador | `ResponderRecurso3aInstancia`, operador atual, situação EmRecursoDeTerceiraInstancia |
| Resposta preliminar omissão `RPP_NOR` | operador | operador atual, situação ReclamacaoCgdf, unidade atual do tipo `UnidadeSicSuperior`, `ResponderOmissaoResposta` |
| Resposta definitiva órgão `RPD_PDD` | operador | operador atual na unidade, situação RespondidoTerceiraInstancia, decisão da 3ª instância Deferido/ParcialmenteDeferido, `RegistrarRespostaDefinitivaOrgao` |
| Decisão 3ª instância `DCS_RTI` | operador | `ManifestarRecurso3aInstanciaCGDF`, operador atual, unidade SIC superior, sem decisão ainda, situação EmAnaliseCGDF |
| Decisão omissão `DCS_NOR` | operador | `ManifestarOmissaoRespostaCGDF`, operador atual, unidade SIC superior, situação RespostaPreliminarReclamacaoCGDF |
| Registrar recurso 1ª `RGS_RPI` | autor | sem recurso de 1ª; pedido Respondido e dentro do prazo vigente |
| Registrar recurso 2ª `RGS_RSI` | autor | sem recurso de 2ª e com 1ª; (1ª respondida e no prazo) ou (1ª não respondida e no prazo) |
| Registrar recurso 3ª `RGS_RTI` | autor | com 2ª e sem 3ª; (2ª respondida e no prazo) ou (2ª não respondida, no prazo e prazo da 2ª anterior ao prazo vigente) |
| Imprimir `MPR_PDD` | operador / autor | operador na unidade ou na unidade SIC superior; ou autor |
| Invalidar `NVD_PDD` | operador | na unidade do pedido |
| Remover operador atual `RMV_PRD` | — | **sempre verdadeiro** |
| Anexar (manifestante / unidade) `NXR_RQM` / `NXR_RQN` | autor / operador | autor com situação Respondido, RespondidoPrimeira ou RespondidoSegunda; operador atual na unidade |
| Registrar no SEI `RGS_SEI` | operador | pedido com recurso de 3ª, `ResponderRecurso3aInstancia`, situação RespostaPreliminarRegistradaPelaCGDF |
| Reencaminhar `RRE_PDD` | operador | na unidade, operador atual, situação EmAnalise, no prazo vigente, `ReencaminharPedido` |
| Remover anexo `RMV_RQV` | operador | na unidade, operador atual, no prazo vigente |
| Prorrogar `PRG_PDD` | operador | na unidade, operador atual, sem prorrogação anterior, no prazo vigente, situação EmAnalise ou Recebido |

### Regras de entidade
- ✅ `Pedido`: `Texto` com 3 a 8.000 caracteres; assunto, usuário e tipo de entrada obrigatórios.
- ✅ Um pedido registrado para várias unidades vira **vários pedidos** (clones com o mesmo `Lote`), um por unidade.
- ✅ `ProrrogarPrazo`: só uma vez ("O prazo já foi prorrogado").
- ✅ `EmFluxoTerceiraInstancia` agrupa as situações da 3ª instância e da reclamação CGDF.

## Inferências e limitações
- 🔶 `Reencaminhar` (`ReencaminharPedidoHandler`) não consulta `RRE_PDD`: depende só do papel `OperadorSIC` do endpoint; um operador de qualquer unidade poderia reencaminhar qualquer pedido pelo identificador.
- 🔶 `PermiteRemoverOperadorAtual` retorna `true` sempre.
- 🔶 `NotificacaoController` não tem `[Authorize]`: os quatro endpoints de omissão de resposta ficam acessíveis a anônimos se o SDK não exigir autenticação global (❓).
- 🔶 `RPT_PDD` aceita responder em `ReclamacaoOrgao`/`ReclamacaoCgdf` mesmo fora do prazo, para não deixar pedido sem resposta.
- 🔶 Comentários `todo` nas regras de recurso ("verificar essa regra para todos os recursos"): regras incompletas.
- ❓ Cadastros (formulário, assunto, feriado), pesquisa de satisfação, exportações e `MoverPedidosParaContaLGPD` não lidos.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]]

## Pendências e próximo passo
- Catálogo de endpoints (lote 6); integrações SEI e e-mail (lote 7).
