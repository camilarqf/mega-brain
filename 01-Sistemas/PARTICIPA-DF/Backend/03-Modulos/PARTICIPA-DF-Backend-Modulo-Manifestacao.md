---
type: module
aliases:
  - Manifestacao
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - backend
  - ouvidoria
  - manifestacao
  - permissoes
sources:
  - src/OuvDF.Api/Controllers/ServicoOuvidoria
  - src/OuvDF.ServicoOuvidoria/Domain/Entities/Manifestacao.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Entities/SituacaoManifestacao.cs
  - src/OuvDF.ServicoOuvidoria/Domain/Commands
  - src/OuvDF.ServicoOuvidoria/Infra/Queries
  - src/OuvDF.ServicoOuvidoria/Infra/Queries/ConsultarPermissaoEmManifestacao/ConsultarPermissaoEmManifestacaoHandler.cs
---

# Módulo Manifestação (Ouvidoria)

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Fluxo-Registro]], [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Fluxo-Tramitacao-e-Resposta]], [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-e-Prorrogacao|Regras-de-Prazo-e-Prorrogacao]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Reclassificacao-e-Invalidacao|Reclassificacao-e-Invalidacao]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Atribuicao-e-Bloqueio-Externo|Atribuicao-e-Bloqueio-Externo]], [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

## Objetivo
Visão do módulo de Ouvidoria: o que é uma manifestação, quais controllers e comandos existem e como o sistema decide **o que cada operador pode fazer** em cada manifestação.

## Evidências
Controllers `Controllers/ServicoOuvidoria/*` (22), entidade `Manifestacao`, comandos de `ServicoOuvidoria/Domain/Commands` (35 pastas), consultas de `Infra/Queries` (cerca de 70 pastas), commit `4901ad5`. Não foram lidos todos os cadastros e consultas (listados abaixo apenas pelo nome).

## Informações confirmadas

### Ciclo geral
Cidadão (identificado ou anônimo, conforme a classificação) ou operador registra uma manifestação → ela nasce `Recebida` na unidade de tramitação inicial, com prazo → operadores tramitam, registram providências e respondem → o cidadão avalia (resolvida ou não) e pode receber/enviar complementações → casos especiais: prorrogação, reclassificação, invalidação, bloqueio externo. Cada passo está nas notas de fluxo e regra linkadas acima.

### Controllers (22) e capacidades
| Controller | Rota base | Capacidades observadas |
|---|---|---|
| `ManifestacaoController` | `servico-ouvidoria/manifestacao` | registrar (anônimo), por operador, integrada (anônimo), buscar por protocolo/usuário/login/id, detalhe da unidade e do manifestante, invalidar, avaliar, remover atribuição, caixas de entrada (manifestante e unidade), consulta por termo, ações permitidas, permite detalhar, exportar PDF (manifestante, operador, operador com dados do usuário), histórico de visualização, resumo (anônimo) |
| `TramiteController` | `…/tramite` | tramitar, unidades de destino, ações, tramitação seccional |
| `RespostaController` | `…/resposta` | definitiva, preliminar, complementar |
| `ProrrogacaoController` | `…/prorrogacao-prazo` | solicitar, deferir, indeferir, listar, situações, contar |
| `ReclassificacaoController` | `…/reclassificacao` | reclassificar, reclassificação seccional, unidades |
| `ComplementacaoController` | `…/complementacao` | pró-ativa, responder, solicitar, listar |
| `ProvidenciaController` | `…/providencia` | registrar providência |
| `ArquivoController` | `…/arquivo` | anexar, baixar, excluir (6 ações) |
| `AvaliacaoPorOperadorController` | — | solicitações de avaliação de atendimento por operador |
| `AssuntoController`, `ClassificacaoController`, `TipoEntradaController`, `RegiaoAdministrativaController`, `FormularioController`, `QuestionarioController`, `ColecoesController` | — | cadastros e consultas de apoio |
| `DashboardController` | — | painéis e produtividade (15 ações, não detalhadas) |
| `IAController`, `ApiMetroController`, `ServicosExternosController`, `IntegracaoController`, `NotificacaoController` | — | integrações e notificações (lote 7) |

### Comandos de domínio (35)
`RegistrarManifestacao`, `TramitarManifestacao`, `TramitarManifestacaoSeccional`, `RegistrarRespostaPreliminar/Definitiva/Complementar`, `RegistrarProvidencia`, `SolicitarEsclarecimento`, `ResponderEsclarecimento`, `RegistrarComplementacaoProAtiva`, `SolicitarProrrogacaoDePrazo`, `DeferirSolicitacaoDeProrrogacaoDePrazo`, `IndeferirSolicitacaoDeProrrogacaoDePrazo`, `ReclassificarManifestacao`, `RegistrarReclassificacaoSeccional`, `InvalidarManifestacao`, `AvaliarAtendimento`, `RegistrarSolicitacaoDeAvaliacao`, `RegistrarPesquisaDeSatisfacaoPorOperador`, `ResponderPesquisaDeSatisfacao`, `AtribuirParaOperador`, `RemoverAtribuicaoOperador`, `AplicarBloqueioExterno`, `RemoverBloqueioExterno`, `AtualizarManifestacaoParaVencida` e `…AposProrrogacao`, `MoverManifestacoesParaContaLGPD`, `AnexarArquivo`, `ExcluirArquivoPorOperador`, `EfetuarDownload`, `EfetuarDownloadManifestante`, `ValidarArquivoAnexo`, `ValidarAtributoComplementar`, `GravarAssunto`, `GravarFormulario`, `GravarNotificacaoDePrazo`.

### Permissões por ação (`ConsultarPermissaoEmManifestacao`)
Uma única consulta decide 19 ações (por ação ou em lote), combinando estado da manifestação, unidade e perfil do operador:
| Ação | Sigla | Condições (resumo) |
|---|---|---|
| Detalhar | `DTL_MNF` | na unidade do operador (e, se há manifestação bloqueante, exige `DetalharManifestacaoBloqueada`) **ou** na hierarquia inferior **ou** criada na unidade **ou** Controle de Qualidade para manifestações que não sejam denúncia; e a regra do usuário (abaixo) |
| Resposta definitiva | `RPT_DFN` | sem definitiva; na unidade; em atendimento; é o operador corrente; unidade é a `ResponsavelPorResposta`; não bloqueada externamente; não bloqueada pela unidade (ou `TratarBloqueadas`); funcionalidade `ResponderDefinitivo` |
| Resposta preliminar | `RPT_PRL` | sem preliminar; mesmas condições, sem exigir ser a responsável; funcionalidade `ResponderPreliminar` |
| Resposta complementar | `RPT_CMP` | sem complementar; **não** em atendimento e não inválida; operador corrente na unidade; `ResponderComplementar` |
| Providência | `RGT_PRV` | em atendimento, operador corrente; `RegistrarProvidencia` |
| Tramitar | `TRM_MNF` | em atendimento, operador corrente; se vencida, só se o último trâmite foi `Apurar` ou `EncaminharRespostaApuracao` (ou `TratarBloqueadas`); `Tramitar` |
| Tramitar seccional | `TRM_SEC` | em atendimento; prazo restante > 9 dias; `TramitarEntreSeccionais` |
| Prorrogar prazo | `PRG_PRZ` | classificação permite prorrogação; dentro da janela ±5 dias do vencimento; em atendimento; `ProrrogarPrazo` |
| Complementar (solicitar esclarecimento) | `CMP_MNF` | `SolicitarComplementacao`, operador corrente, em atendimento |
| Anexar / remover anexo | `ANX_RQV` / `RMV_RQV` | operador corrente; remoção exige `RemoverArquivo` |
| Devolver à caixa de entrada | `DVL_MNF` | operador corrente **ou** `DevolverParaCaixaDeEntrada`; na unidade; não bloqueada externamente |
| Invalidar | `NVL_MNF` | operador corrente; não inválida; `InvalidarManifestacao` |
| Reclassificar integral / parcial / seccional | `RCL_INT` / `RCL_PAR` / `RCL_SEC` | em atendimento, operador corrente; `ReclassificarManifestacao` / `ReclassificarAssunto` / `ReclassificacaoSeccional` |
| Imprimir | `MPR_MNF` | `ImprimirManifestacao` |
| Download de anexo | `DWL_RQV` | operador corrente na unidade |
| Ver dados do manifestante | `VSL_DMT` | `VisualizarManifestante` |

- ✅ **Manifestação bloqueada pela unidade**: `ManifestacaoEstaBloqueada` é verdadeira quando a manifestação está em atendimento e existe **outra** manifestação "bloqueante" na mesma unidade (`ConsultarManifestacaoBloqueante`); só `TratarBloqueadas` ignora isso. A bloqueante vem do mecanismo de prazos que bloqueiam a caixa de entrada ([[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-e-Prorrogacao|Regras-de-Prazo-e-Prorrogacao]]).
- ✅ **Usuário bloqueado**: se o manifestante está bloqueado (`Usuario.IsBloqueado()`), detalhar exige a funcionalidade específica (`DetalharManifestacaoDeUsuarioInconsistente`, `…Inexistente` ou `…Falecido`).
- ✅ **Bloqueio externo** (`BloqueadaExternamente`) impede quase todas as ações de operador ([[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Atribuicao-e-Bloqueio-Externo|Atribuicao-e-Bloqueio-Externo]]).

### Regras gerais da entidade
- ✅ `Relato` com 3 a 13.000 caracteres; manifestação identificada exige usuário; classificação sem anonimato exige identificação.
- ✅ `Protocolo` recebe prefixo a partir da classificação (`AlterarPrefixoDoProtocolo` troca os 2 primeiros caracteres ao reclassificar).
- ✅ `Vencimento` é gravado na criação (data final do prazo calculado).
- ✅ `EmAtendimento` = Recebida, EmAnálise, Prorrogada, Vencida ou Vencida_após_prorrogação.

## Inferências e limitações
- 🔶 Várias ações (`InvalidarManifestacao`, `DeferirSolicitacao…`, `SolicitarProrrogacao…`) checam a funcionalidade, mas só algumas passam por `ConsultarPermissaoEmManifestacao`; ver pontos de atenção nas notas de fluxo e regra.
- 🔶 `ManifestacaoEstaBloqueada` chama `_mediator.Send(...).Wait()` (bloqueio síncrono) a cada ação consultada; em modo lote isso se repete 19 vezes.
- 🔶 `POST …/manifestacao/resumo` é anônimo; não foi lido o que devolve (risco de exposição, a confirmar).
- ❓ `DashboardController`, cadastros (assunto, classificação, formulário), `ColecoesController`, exportações e `MoverManifestacoesParaContaLGPD` (usado na exclusão de conta?) ficaram como visão geral.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Workflows-e-Consumidores|Workflows-e-Consumidores]]

## Pendências e próximo passo
- Ler `resumo`, `Dashboard`, `Colecoes`, cadastros e exportações no lote 6 (catálogo de endpoints).
- Lote 7: IA, ApiMetro, ServicosExternos e MailService.
