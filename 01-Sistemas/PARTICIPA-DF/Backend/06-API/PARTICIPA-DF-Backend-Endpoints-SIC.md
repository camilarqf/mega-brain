---
type: api
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
  - api
  - endpoints
  - sic
sources:
  - src/OuvDF.Api/Controllers/ServicoInformacaoCidadao
---

# Endpoints do SIC (62)

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]] · Índice: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Backend]] · Módulo: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Pedido-e-Recurso|Pedido-e-Recurso]]

## Objetivo
Listar os endpoints dos 10 controllers de `Controllers/ServicoInformacaoCidadao`. Legenda e advertências estão no catálogo geral.

## Evidências
Extração por script dos atributos dos controllers, commit `4901ad5`; acesso **declarado**.

## Informações confirmadas
- ✅ 62 endpoints; 2 anônimos (`pedido/unidades`, `formulario/por-assunto`), 32 autenticados, 18 `OperadorSIC` e **10 sem atributo** de autorização.
- ✅ Sem atributo: `arquivo/download`, `arquivo/validar`, `assunto` (3 `GET`), `notificacao/*` (4) e `situacao/situacao-resposta`.
- ✅ O autor do pedido usa endpoints só `[Authorize]` (registro, recursos, consultas), com a regra de autor aplicada nos handlers (`ConsultarPermissaoPedido`).

## Lista

### Arquivo (4)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `acesso-informacao/arquivo/anexar` | autenticado | audit 40MB | `AnexarArquivo` |
| POST | `acesso-informacao/arquivo/download` | sem atributo |  | `EfetuarDownload` |
| POST | `acesso-informacao/arquivo/excluir-por-operador` | OperadorSIC | audit | `ExcluirArquivoPorOperador` |
| POST | `acesso-informacao/arquivo/validar` | sem atributo |  | `ValidarArquivoAnexo` |

### Assunto (5)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `acesso-informacao/assunto` | sem atributo |  |  |
| GET | `acesso-informacao/assunto/com-formulario` | sem atributo |  |  |
| GET | `acesso-informacao/assunto/registrado-na-unidade` | OperadorSIC |  |  |
| GET | `acesso-informacao/assunto/sem-formulario` | sem atributo |  |  |
| POST | `acesso-informacao/assunto/sub-assuntos` | autenticado |  | `ConsultarSubAssuntos` |

### Classificacao (1)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `acesso-informacao/classificacao/por-situacao` | autenticado |  | `ConsultarClassificacaoPorSituacaoPedido` |

### Feriado (3)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `acesso-informacao/feriado` | autenticado |  | `ConsultarFeriados` |
| POST | `acesso-informacao/feriado/get-feriado-por-id` | autenticado |  | `ConsultarFeriadoPorId` |
| POST | `acesso-informacao/feriado/gravar-feriado` | autenticado | audit | `GravarFeriado` |

### FormularioSIC (6)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `acesso-informacao/formulario/formato` | autenticado |  |  |
| POST | `acesso-informacao/formulario` | OperadorSIC |  | `ConsultarFormulariosSIC` |
| POST | `acesso-informacao/formulario/atributo` | autenticado |  | `RecuperarAtributo` |
| POST | `acesso-informacao/formulario/cadastrar` | OperadorSIC | audit | `GravarFormularioSIC` |
| POST | `acesso-informacao/formulario/consultar-por-id` | autenticado |  | `ConsultarFormularioSICPorId` |
| POST | `acesso-informacao/formulario/por-assunto` | anônimo |  | `ConsultarFormularioSICPorAssunto` |

### Notificacao (4)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `acesso-informacao/notificacao/omissao-resposta-cgdf/registrar-decisao` | sem atributo | audit 40MB | `RegistrarDecisaoNotificacaoOmissaoResposta` |
| POST | `acesso-informacao/notificacao/omissao-resposta-cgdf/registrar-resposta` | sem atributo | audit 40MB | `RegistrarRespostaPreliminarNotificacaoOmissaoResposta` |
| POST | `acesso-informacao/notificacao/registrar-omissao-resposta` | sem atributo | audit 40MB |  |
| POST | `acesso-informacao/notificacao/registrar-omissao-resposta-cgdf` | sem atributo | audit 40MB |  |

### Pedido (27)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `acesso-informacao/pedido/tipos-de-sigilo` | autenticado |  |  |
| POST | `acesso-informacao/pedido` | autenticado | audit 40MB | `RegistrarPedidoAutorRequest` |
| POST | `acesso-informacao/pedido/acoes-autor` | autenticado |  | `ConsultarAcoesPedido` |
| POST | `acesso-informacao/pedido/acoes-operador` | OperadorSIC | audit | `ConsultarAcoesPedido` |
| POST | `acesso-informacao/pedido/consultar-por-lote` | autenticado |  | `ConsultarPedidosPorLote` |
| POST | `acesso-informacao/pedido/consultar-por-termo` | autenticado |  | `ConsultarPorTermoRequest` |
| POST | `acesso-informacao/pedido/detalhar-evento-pedido` | autenticado |  | `ConsultarEventoDoPedidoPorId` |
| POST | `acesso-informacao/pedido/detalhar-por-manifestante` | autenticado |  | `ConsultarPedidoDetalhadoPorManifestante` |
| POST | `acesso-informacao/pedido/detalhar-por-unidade` | OperadorSIC |  | `ConsultarPedidoDetalhadoPorUnidade` |
| POST | `acesso-informacao/pedido/em-notificacao-cgdf` | OperadorSIC |  | `ConsultarPedidosEmNotificacaoDeOmissaoDeRespostaCGDF` |
| POST | `acesso-informacao/pedido/em-recurso-terceira-instancia` | OperadorSIC |  | `ConsultarPedidosRecursoTerceiraInstancia` |
| POST | `acesso-informacao/pedido/exportar` | autenticado |  | `ExportarPedidoPDF` |
| POST | `acesso-informacao/pedido/exportar-operador` | autenticado |  | `ExportarPedidoOperador` |
| POST | `acesso-informacao/pedido/exportar-pedido-usuario` | autenticado |  | `ExportarPedidoPdfUsuario` |
| POST | `acesso-informacao/pedido/manifestante` | autenticado |  | `ConsultarPedidosManifestante` |
| POST | `acesso-informacao/pedido/manifestante/itens-filtro` | autenticado |  | `ConsultarItensFiltrosCaixaEntradaManifestante` |
| POST | `acesso-informacao/pedido/permite-detalhar` | autenticado |  | `ConsultarPermissaoDetalhamentoPedido` |
| POST | `acesso-informacao/pedido/por-operador` | autenticado | audit 40MB | `RegistrarPedidoOperadorRequest` |
| POST | `acesso-informacao/pedido/prorrogar-prazo` | autenticado | audit | `ProrrogarPrazoPedido` |
| POST | `acesso-informacao/pedido/reencaminharPedido` | OperadorSIC | audit | `ReencaminharPedido` |
| POST | `acesso-informacao/pedido/registrar-pedido-sei` | OperadorSIC | audit | `SolicitarVinculoSei` |
| POST | `acesso-informacao/pedido/registrar-resposta` | OperadorSIC | audit 40MB | `RegistrarRespostaPedido` |
| POST | `acesso-informacao/pedido/registrar-resposta-definitiva` | OperadorSIC | audit 40MB | `RegistrarRespostaDefinitivaPedido` |
| POST | `acesso-informacao/pedido/remover-operador-atual` | OperadorSIC | audit | `RemoverOperadorAtual` |
| POST | `acesso-informacao/pedido/unidade` | OperadorSIC |  | `ConsultarPedidosUnidade` |
| POST | `acesso-informacao/pedido/unidade/itens-filtro` | autenticado |  | `ConsultarItensFiltrosCaixaEntradaUnidade` |
| POST | `acesso-informacao/pedido/unidades` | anônimo |  | `ConsultarUnidadesParaPedido` |

### Questionario (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `acesso-informacao/questionario` | autenticado |  | `ConsultarQuestoesPorPedido` |
| POST | `acesso-informacao/questionario/responder-pesquisa` | autenticado | audit | `ResponderPesquisa` |

### Recurso (9)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `acesso-informacao/recurso/justificativa` | autenticado |  |  |
| GET | `acesso-informacao/recurso/terceira-instancia/tipo-decisao` | autenticado |  |  |
| POST | `acesso-informacao/recurso/primeira-instancia/registrar` | autenticado | audit 40MB | `RegistrarRecursoPrimeiraInstancia` |
| POST | `acesso-informacao/recurso/primeira-instancia/registrar-resposta` | OperadorSIC | audit 40MB | `RegistrarRespostaRecursoPrimeiraInstancia` |
| POST | `acesso-informacao/recurso/segunda-instancia/registrar` | autenticado | audit 40MB | `RegistrarRecursoSegundaInstancia` |
| POST | `acesso-informacao/recurso/segunda-instancia/registrar-resposta` | OperadorSIC | audit 40MB | `RegistrarRespostaRecursoSegundaInstancia` |
| POST | `acesso-informacao/recurso/terceira-instancia/registrar` | autenticado | audit 40MB | `RegistrarRecursoTerceiraInstancia` |
| POST | `acesso-informacao/recurso/terceira-instancia/registrar-decisao` | OperadorSIC | audit 40MB | `RegistrarDecisaoRecursoTerceiraInstancia` |
| POST | `acesso-informacao/recurso/terceira-instancia/registrar-resposta-preliminar` | OperadorSIC | audit 40MB | `RegistrarRespostaPreliminarRecursoTerceiraInstancia` |

### Situacao (1)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `acesso-informacao/situacao/situacao-resposta` | sem atributo |  | `ConsultarSituacaoResposta` |

## Inferências e limitações
- 🔴 `arquivo/download` sem atributo: se não houver autenticação global, qualquer pessoa que conheça o identificador poderia baixar anexos de pedidos (que podem ser sigilosos). O handler `EfetuarDownload` não foi lido para ver se confere o dono.
- 🔴 `notificacao/*` sem atributo: ver [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Fluxo-Omissao-de-Resposta]].
- ❓ Contratos e códigos de resposta.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Pedido|Fluxo-Registro-de-Pedido]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]]

## Pendências e próximo passo
- Ler `EfetuarDownload` (SIC e Ouvidoria) para confirmar a verificação do dono do anexo.
