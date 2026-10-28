---
type: api
aliases:
  - "Endpoints da Ouvidoria (108)"
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
sources:
  - src/OuvDF.Api/Controllers/ServicoOuvidoria
---

# Endpoints da Ouvidoria (108)

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]] · Índice: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Backend]] · Módulo: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Manifestacao|Manifestacao]]

## Objetivo
Listar os endpoints dos 22 controllers de `Controllers/ServicoOuvidoria`. Legenda e advertências estão no catálogo geral; aqui só a lista.

## Evidências
Extração por script dos atributos dos controllers, commit `4901ad5`; o acesso é o **declarado** (ver ressalvas do catálogo geral).

## Informações confirmadas
- ✅ 108 endpoints; 33 anônimos, 36 autenticados, 35 `OperadorSO` e 4 `OperadorWS` (nenhum sem atributo).
- ✅ Anônimos: registro de manifestação (`manifestacao`, `manifestacao/integrada`), `resumo`, cadastros públicos (assuntos, classificações, coleções, regiões, tipos de entrada, formulário por assunto), `ia/*`, `metro/*`, `servicos/*`.
- ✅ `IntegracaoController` (`v1/manifestacao…`) exige `OperadorWS`; contém duas ações `GET v1/manifestacao` (🔶 conflito).
- ✅ `DashboardController` mantém só 2 endpoints ativos (produtividade por operador e por unidade); 12 estão comentados.

## Lista

### ApiMetro (4)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `metro/classificacao` | anônimo |  |  |
| GET | `metro/manifestacao/cidadao` | autenticado |  |  |
| GET | `metro/ra` | anônimo |  |  |
| POST | `metro/assunto` | anônimo |  | `ConsultarAssuntosPorClassificacao` |

### Arquivo (5)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `servico-ouvidoria/arquivo/download` | autenticado |  | `EfetuarDownload` |
| POST | `servico-ouvidoria/arquivo/download-manifestante` | autenticado |  | `EfetuarDownloadManifestante` |
| POST | `servico-ouvidoria/arquivo/enviar` | autenticado | audit 40MB | `AnexarArquivo` |
| POST | `servico-ouvidoria/arquivo/excluir-por-operador` | OperadorSO | audit | `ExcluirArquivoPorOperador` |
| POST | `servico-ouvidoria/arquivo/validar` | anônimo |  | `ValidarArquivoAnexo` |

### Assunto (10)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/assunto/com-formulario` | autenticado |  |  |
| GET | `servico-ouvidoria/assunto/por-palavra-chave/{palavraChave}` | anônimo |  |  |
| GET | `servico-ouvidoria/assunto/por-unidade` | autenticado |  |  |
| GET | `servico-ouvidoria/assunto/sem-formulario` | autenticado |  |  |
| POST | `servico-ouvidoria/assunto` | autenticado | audit | `GravarAssunto` |
| POST | `servico-ouvidoria/assunto/filtrar-por-palavra-chave-e-classificacao` | anônimo |  | `ConsultarAssuntoPorPalavraChaveClassificacao` |
| POST | `servico-ouvidoria/assunto/id` | anônimo |  | `CommandIDSensitive<long>` |
| POST | `servico-ouvidoria/assunto/listar` | OperadorSO |  | `ConsultarAssuntos` |
| POST | `servico-ouvidoria/assunto/por-classificacao` | autenticado |  | `ConsultarAssuntosPorClassificacao` |
| POST | `servico-ouvidoria/assunto/top10` | anônimo |  | `ConsultarAssuntoTop10` |

### AvaliacaoPorOperador (4)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `avaliacao-por-operador/manifestacoes-para-avaliacao` | OperadorSO |  |  |
| POST | `avaliacao-por-operador/avaliar-atendimento` | OperadorSO | audit | `AvaliarAtendimentoPorOperador` |
| POST | `avaliacao-por-operador/registrar-pesquisa-de-satisfacao` | OperadorSO | audit | `RegistrarPesquisaDeSatisfacaoPorOperador` |
| POST | `avaliacao-por-operador/registrar-solicitacao-de-avaliacao` | OperadorSO | audit | `RegistrarSolicitacaoDeAvaliacao` |

### Classificacao (4)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/classificacao` | anônimo |  |  |
| GET | `servico-ouvidoria/classificacao/listar-para-registro-interno/{manifestacaoIdentificada}` | anônimo |  |  |
| POST | `servico-ouvidoria/classificacao/id` | anônimo |  | `CommandIDSensitive<long>` |
| POST | `servico-ouvidoria/classificacao/listar-para-reclassificacao-seccional` | anônimo |  | `ConsultarClassificacoesParaReclassificacaoSeccional` |

### Colecoes (9)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/colecoes/acao-para-remover-notificacao` | anônimo |  |  |
| GET | `servico-ouvidoria/colecoes/formacao` | anônimo |  |  |
| GET | `servico-ouvidoria/colecoes/raca-cor` | anônimo |  |  |
| GET | `servico-ouvidoria/colecoes/renda` | anônimo |  |  |
| GET | `servico-ouvidoria/colecoes/sexo` | anônimo |  |  |
| GET | `servico-ouvidoria/colecoes/situacao` | anônimo |  |  |
| GET | `servico-ouvidoria/colecoes/tema` | anônimo |  |  |
| GET | `servico-ouvidoria/colecoes/tempo-residencia` | anônimo |  |  |
| GET | `servico-ouvidoria/colecoes/tipo-telefone` | anônimo |  |  |

### Complementacao (4)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/complementacao/listar` | autenticado |  | `ConsultarComplementacoesPorManifestante` |
| POST | `servico-ouvidoria/complementacao/pro-ativa` | autenticado | audit | `RegistrarComplementacaoProAtiva` |
| POST | `servico-ouvidoria/complementacao/responder` | autenticado | audit | `ResponderEsclarecimento` |
| POST | `servico-ouvidoria/complementacao/solicitar` | OperadorSO | audit | `SolicitarEsclarecimento` |

### Dashboard (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `dashboard/produtividade-operador-so` | OperadorSO |  | `ConsultarProdutividadeOperador` |
| POST | `dashboard/produtividade-unidade` | OperadorSO |  | `ConsultarProdutividadeUnidade` |

### Formulario (6)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/formulario/atributo` | autenticado |  |  |
| GET | `servico-ouvidoria/formulario/formato` | autenticado |  |  |
| POST | `servico-ouvidoria/formulario` | OperadorSO | audit | `GravarFormulario` |
| POST | `servico-ouvidoria/formulario/id` | OperadorSO |  | `CommandIDSensitive<long>` |
| POST | `servico-ouvidoria/formulario/listar` | OperadorSO |  | `ConsultarFormularios` |
| POST | `servico-ouvidoria/formulario/por-assunto` | anônimo |  | `ConsultarFormularioPorAssunto` |

### IA (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `servico-ouvidoria/ia/assunto` | anônimo |  | `ConsultarModeloAssuntoIARequest` |
| POST | `servico-ouvidoria/ia/classificacao` | anônimo |  | `ConsultarModeloClassificacaoIA` |

### Integracao (4)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `v1/manifestacao` | OperadorWS |  | `ConsultarManifestacaoDetalhadaUnidade` |
| GET | `v1/manifestacao` | OperadorWS | audit |  |
| POST | `v1/manifestacao` | OperadorWS | audit |  |
| POST | `v1/manifestacao/por-manifestante` | OperadorWS |  | `ConsultarManifestacoesCaixaEntradaManifestante` |

### Manifestacao (25)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/manifestacao/id/{manifestacaoId}` | OperadorSO |  |  |
| GET | `servico-ouvidoria/manifestacao/por-login` | autenticado |  |  |
| POST | `servico-ouvidoria/manifestacao` | anônimo | audit 40MB | `RegistrarManifestacaoRequest` |
| POST | `servico-ouvidoria/manifestacao/acoes` | OperadorSO |  | `ConsultarAcoesManifestacao` |
| POST | `servico-ouvidoria/manifestacao/avaliar` | autenticado | audit | `AvaliarAtendimento` |
| POST | `servico-ouvidoria/manifestacao/caixa-entrada-manifestante` | autenticado |  | `ConsultarManifestacoesCaixaEntradaManifestante` |
| POST | `servico-ouvidoria/manifestacao/consultar-por-termo` | autenticado |  | `ConsultarPorTermoRequest` |
| POST | `servico-ouvidoria/manifestacao/dados-manifestacao-integrada` | autenticado |  | `ConsultarDadosManifestacaoIntegrada` |
| POST | `servico-ouvidoria/manifestacao/exportar-pdf-manifestante` | autenticado |  | `ExportarManifestacaoPDF` |
| POST | `servico-ouvidoria/manifestacao/exportar-pdf-operador` | autenticado |  | `ExportarManifestacaoOperadorPDF` |
| POST | `servico-ouvidoria/manifestacao/exportar-pdf-operador-dados-usuario` | autenticado |  | `ExportarManifestacaoOperadorPdfDadosUsuario` |
| POST | `servico-ouvidoria/manifestacao/historico-visualizacao` | autenticado |  | `ConsultarHistoricoVisualizacaoManifestacaoQuery` |
| POST | `servico-ouvidoria/manifestacao/integrada` | anônimo | audit 40MB | `RegistrarManifestacaoIntegradaRequest` |
| POST | `servico-ouvidoria/manifestacao/invalidar` | OperadorSO | audit | `InvalidarManifestacao` |
| POST | `servico-ouvidoria/manifestacao/manifestante/detalhe` | autenticado |  | `ConsultarManifestacaoDetalhadaManifestante` |
| POST | `servico-ouvidoria/manifestacao/manifestante/itens-filtro` | autenticado |  | `ConsultarItensFiltrosCaixaEntradaManifestante` |
| POST | `servico-ouvidoria/manifestacao/na-unidade` | OperadorSO |  | `ConsultarManifestacoesNaUnidadeAtual` |
| POST | `servico-ouvidoria/manifestacao/permite-detalhar` | autenticado |  | `ConsultarPermissaoDetalhamentoManifestacao` |
| POST | `servico-ouvidoria/manifestacao/por-operador` | autenticado | audit 40MB | `RegistrarManifestacaoOperadorRequest` |
| POST | `servico-ouvidoria/manifestacao/por-protocolo` | OperadorSO |  | `ConsultarManifestacaoPorProtocolo` |
| POST | `servico-ouvidoria/manifestacao/por-usuario` | autenticado |  | `ConsultarManifestacoesPorManifestante` |
| POST | `servico-ouvidoria/manifestacao/registrada-na-unidade` | OperadorSO |  | `ConsultarManifestacoesRegistradasNaUnidade` |
| POST | `servico-ouvidoria/manifestacao/remover-atribuicao-operador` | OperadorSO | audit | `RemoverAtribuicaoOperador` |
| POST | `servico-ouvidoria/manifestacao/resumo` | anônimo |  | `ConsultarManifestacaoResumidaPorId` |
| POST | `servico-ouvidoria/manifestacao/unidade/detalhe` | OperadorSO |  | `ConsultarManifestacaoDetalhadaUnidade` |

### Notificacao (1)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `notificacao/por-unidade` | autenticado |  |  |

### Prorrogacao (6)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/prorrogacao-prazo/count` | autenticado |  |  |
| GET | `servico-ouvidoria/prorrogacao-prazo/situacoes` | autenticado |  |  |
| POST | `servico-ouvidoria/prorrogacao-prazo/deferir` | OperadorSO | audit | `DeferirSolicitacaoDeProrrogacaoDePrazo` |
| POST | `servico-ouvidoria/prorrogacao-prazo/indeferir` | autenticado | audit | `IndeferirSolicitacaoDeProrrogacaoDePrazo` |
| POST | `servico-ouvidoria/prorrogacao-prazo/listar` | OperadorSO |  | `ConsultarProrrogacoesDePrazo` |
| POST | `servico-ouvidoria/prorrogacao-prazo/solicitar` | OperadorSO | audit | `SolicitarProrrogacaoDePrazo` |

### Providencia (1)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `servico-ouvidoria/providencia` | OperadorSO | audit | `RegistrarProvidencia` |

### Questionario (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `questionario` | autenticado |  | `ConsultarQuestoesPesquisaSatisfacao` |
| POST | `questionario/responder` | autenticado | audit | `ResponderPesquisaDeSatisfacao` |

### Reclassificacao (3)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `servico-ouvidoria/reclassificacao/registrar-reclassificacao` | OperadorSO | audit | `ReclassificarManifestacaoRequest` |
| POST | `servico-ouvidoria/reclassificacao/registrar-reclassificacao-seccional` | OperadorSO | audit | `RegistrarReclassificacaoSeccional` |
| POST | `servico-ouvidoria/reclassificacao/unidades` | OperadorSO |  | `ConsultarUnidadesParaReclassificacao` |

### RegiaoAdministrativa (1)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/regiao-administrativa` | anônimo |  |  |

### Resposta (3)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `servico-ouvidoria/resposta/complementar` | OperadorSO | audit | `RegistrarRespostaComplementar` |
| POST | `servico-ouvidoria/resposta/definitiva` | OperadorSO | audit | `RegistrarRespostaDefinitiva` |
| POST | `servico-ouvidoria/resposta/preliminar` | OperadorSO | audit | `RegistrarRespostaPreliminar` |

### ServicosExternos (4)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servicos/localidade/pesquisa/{chavePesquisa}` | anônimo |  |  |
| GET | `servicos/localidade/posicao` | anônimo |  |  |
| GET | `servicos/ra` | anônimo |  |  |
| GET | `servicos/siturb` | anônimo |  |  |

### TipoEntrada (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/tipo-entrada/com-agrupamento` | autenticado |  |  |
| POST | `servico-ouvidoria/tipo-entrada/id` | anônimo |  | `CommandIDSensitive<string>` |

### Tramite (6)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `servico-ouvidoria/tramite/acoes` | autenticado |  |  |
| POST | `servico-ouvidoria/tramite` | OperadorSO | audit | `TramitarManifestacao` |
| POST | `servico-ouvidoria/tramite/acoes-por-manifestacao` | OperadorSO |  | `ConsultarAcoesTramiteManifestacao` |
| POST | `servico-ouvidoria/tramite/seccional` | OperadorSO | audit | `TramitarManifestacaoSeccional` |
| POST | `servico-ouvidoria/tramite/seccional/unidades` | OperadorSO |  | `ConsultarUnidadesParaTramiteSeccional` |
| POST | `servico-ouvidoria/tramite/unidades` | OperadorSO |  | `ConsultarUnidadesParaTramite` |

## Inferências e limitações
- 🔶 `metro/*` e `servicos/*` parecem fachadas para serviços externos (RA, localidades, siturb, "metro"); confirmar no lote 7.
- 🔶 `ia/*` consulta o modelo de assunto e de classificação por IA (Iza) sem autenticação.
- ❓ Códigos de resposta e contratos dos comandos.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Fluxo-Registro-de-Manifestacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Fluxo-Tramitacao-e-Resposta]]

## Pendências e próximo passo
- Lote 7: classificar `ia/*`, `metro/*` e `servicos/*` como integrações.
