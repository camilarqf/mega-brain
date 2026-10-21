---
type: api
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
tags:
  - portal-transparencia
  - backend
  - api
  - endpoints
sources:
  - src/main/java/br/gov/df/transparencia/api
  - src/main/java/br/gov/df/transparencia/api/comum/StorageController.java
---
# Catálogo de endpoints

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Objetivo
Listar as rotas HTTP expostas pelo `portal-transparencia-backend`, por área e controller.

## Evidências
Extração automática (script de leitura estática) das anotações `@RequestMapping`/`@GetMapping`/`@PostMapping` em `src/main/java/br/gov/df/transparencia/api` no commit `9434e58f`, ignorando código comentado; atualizada para `e98fcc38` com o `StorageController` (+2 rotas, +3 linhas de anotação: 631 linhas, 72 de classe, 631 − 72 = 559). Caminho = mapeamento de classe + de método. Conferência por contagem: 628 linhas de anotação de mapeamento no diretório, das quais 71 são de classe (70 controllers e a classe `Healthcheck`, que é `@Component`); 628 − 71 = 557, igual ao total extraído no commit `9434e58f`.

## Informações confirmadas
- ✅ **559 rotas em 70 controllers com rota ativa** (`FormularioContatoController` não tem rota: o código está comentado). Verbos: `GET` 545, `POST` 9 e 5 mapeamentos **sem verbo** (`@RequestMapping` sem `method`, aceitam qualquer verbo, marcados `ANY`).
- ✅ Todas as requisições (exceto `OPTIONS`, `/healthcheck` e `/prometheus`) exigem o cabeçalho `x-client-id` (ver segurança). Não há autenticação.
- ✅ Filtros chegam como parâmetros de query (bean de modelo + `Pageable`: `page`, `size`, `sort`). Respostas JSON (`application/json;charset=UTF-8`), `Page`/`CustomPage` na maioria das listagens; os `*RelatorioController` devolvem **arquivo** (PDF ou CSV; ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]]).
- ✅ Rotas operacionais não contadas acima: `GET /prometheus` (`config/prometheus/PrometheusMetricsController`) e `/healthcheck`, que é o endpoint `health` do Actuator com id `healthcheck` (`endpoints.health.id`); a classe `api/comum/Healthcheck` é um `HealthIndicator` que **sempre retorna UP** (não consulta banco nem dependências), e o `@RequestMapping` dela não tem efeito por ser `@Component`.
- ✅ `api/comum/PesquisaSatisfacaoController` está **totalmente comentado** (não expõe rotas); a pesquisa ativa é `v2/pesquisa-satisfacao`.
- 🔶 Os 5 mapeamentos `ANY` provavelmente se destinam a `GET`; sem `method`, `POST`/`PUT`/`DELETE` também são aceitos (verbos não restringidos).
- Payloads e códigos de erro específicos **não** foram detalhados (ver pendências).

### Resumo por área
| Área | Rotas | Controllers |
|---|---|---|
| Comum (arquivos, cache, contato, e-mail, analytics, integração, pesquisa, storage, textos) | 30 | 11 |
| Convênios | 22 | 2 |
| Data de atualização | 62 | 1 |
| Despesa | 141 | 10 |
| Licitações e contratos (v1) | 15 | 2 |
| Orçamento | 17 | 2 |
| Patrimônio (v1) | 14 | 2 |
| Prestação de contas | 107 | 16 |
| Receita | 40 | 3 |
| Servidor e remuneração | 74 | 9 |
| API v2 | 37 | 13 |

## Rotas por área

### Comum (arquivos, cache, contato, e-mail, analytics, integração, pesquisa, storage, textos)

**ArquivoController** — base `/arquivos` (3)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/arquivos` | `listarArquivosPorCategoria` |
| GET | `/arquivos/url-ultimo-arquivo-categoria/{codCategoria}` | `getAndamentoProcessosCorreicionaisCgdf` |
| GET | `/arquivos/url-ultimo-arquivo-categoria-exercicio/{codCategoria}/{exercicio}` | `getAndamentoProcessosCorreicionaisCgdf` |

**CacheControlController** — base `/cache-expire` (3)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/cache-expire/valores-mascarados` | `expireValoresMascarados` |
| GET | `/cache-expire/remuneracao` | `expireRemuneracao` |
| GET | `/cache-expire/despesa-filtros` | `expireDespesaFiltros` |

**DownloadController** — base `/download` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/download/arquivos/{nome_arquivo:.+}` | `getFile` |

**FormularioContatoController** — base `/contato` (0)

| Verbo | Caminho | Método Java |
|---|---|---|

**IntegracaoSistemasController** — base `/integracao` (8)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/integracao/funcao-servidor` | `verificarFuncaoServidor` |
| GET | `/integracao/verificar-sutcs` | `verificarSutcs` |
| GET | `/integracao/consultar-servidor` | `retornarServidores` |
| GET | `/integracao/nome-servidor` | `recuperarNomeServidor` |
| GET | `/integracao/nota-empenho/{codigoGestao}/{codigoUnidadeGestora}/{numeroNotaEmpenho}` | `recuperarNotaEmpenho` |
| GET | `/integracao/consultar-servidor-ativo` | `recuperarServidoresAtivos` |
| GET | `/integracao/pesquisar-servidor` | `pesquisarServidorPorNome` |
| GET | `/integracao/listar-nl-ob/{codigoUgLiq}/{codigoGestaoLiq}/{numeroNotaEmpenho}` | `listarNlOb` |

**PesquisaSatisfacaoGraficoController** — base `/pesquisa/grafico` (4)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/pesquisa/grafico/ocupacao` | `recuperarOcupacao` |
| GET | `/pesquisa/grafico/faixa-etaria` | `recuperarFaixaEtaria` |
| GET | `/pesquisa/grafico/nivel-satisfacao` | `recuperarRegistros` |
| GET | `/pesquisa/grafico/total-respostas` | `totalDeRespostas` |

**PortalAnalyticsController** — base `/analytics` (6)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/analytics/paginas-populares` | `recuperarPaginasPopulares` |
| GET | `/analytics/usuarios-ativos` | `recuperarNumeroUsuariosAtivos` |
| GET | `/analytics/total-visualizacoes` | `recuperarNumeroTotalVisualizacoes` |
| GET | `/analytics/total-sessoes` | `recuperarNumeroTotalSessoes` |
| GET | `/analytics/categoria-dispositivos` | `recuperarCategoriasDispotivos` |
| GET | `/analytics/visitas` | `recuperarVisitas` |

**SendMailController** — base `(sem base)` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/send-email` | `sendEmail` |

**TextoExplicativoController** — base `/texto-explicativo` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/texto-explicativo/beneficiario/programa-social` | `textoBeneficiarioProgramaSocial` |

**TextosConsultasController** — base `/textos-consultas` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/textos-consultas` | `recuperarTextosConsultas` |

**StorageController** — base `/storage` (2) — adicionado em `feat/servico-minio`; incluído à mão a partir da leitura do arquivo, sem reexecutar o script de extração

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/storage/health` | `teste` |
| GET | `/storage/url` | `gerarUrl` |

### Convênios

**ConvenioController** — base `/convenio` (18)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/convenio/relatorio` | `pequisarQuadro` |
| GET | `/convenio/receita` | `pesquisarReceita` |
| GET | `/convenio/despesa` | `pesquisarDespesa` |
| GET | `/convenio/receita/especie` | `listarEspecieReceita` |
| GET | `/convenio/despesa/especie` | `listarEspecieDespesa` |
| GET | `/convenio/receita/concedente` | `listarConcedenteReceita` |
| GET | `/convenio/despesa/concedente` | `listarConcedenteDespesa` |
| GET | `/convenio/entidade-beneficiada/concedente` | `listarConcedenteEntidadeBeneficiada` |
| GET | `/convenio/receita/anos` | `listarAnosReceita` |
| GET | `/convenio/despesa/anos` | `listarAnosDespesa` |
| GET | `/convenio/receita/execucao` | `pequisarExecucaoReceita` |
| GET | `/convenio/despesa/execucao` | `pequisarExecucaoDespesa` |
| GET | `/convenio/despesa/extrato-convenio` | `pequisarExtratoConvenioDespesa` |
| GET | `/convenio/receita/extrato-convenio` | `pequisarExtratoConvenioReceita` |
| GET | `/convenio/entidades-beneficiadas` | `pequisarEntidadesBeneficiadas` |
| GET | `/convenio/entidades-beneficiadas/anos` | `listarAnosEntidadesBeneficiadas` |
| GET | `/convenio/entidades-beneficiadas/detalhamento-entidades/{anoOrdemBancaria}/{codigoCredor}/{codigoUnidadeGestora}` | `listDetalhamentoConvenioEntidadeBeneficiada` |
| GET | `/convenio/entidade-beneficiada/valor-pago` | `pesquisarDetalhamentoValorPagoEntidadeBeneficiada` |

**ConvenioRelatorioController** — base `/convenio/relatorio` (4)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/convenio/relatorio/receita` | `relatorioReceita` |
| GET | `/convenio/relatorio/despesa` | `relatorioDespesa` |
| GET | `/convenio/relatorio/entidades-beneficiadas` | `relatorioEntidadesBeneficiadas` |
| GET | `/convenio/relatorio/entidades-beneficiadas/detalhamento-entidade/{anoOrdemBancaria}/{codigoCredor}/{codigoUnidadeGestora}` | `relatorioDetalheEntidadesBeneficiadas` |

### Data de atualização

**DataAtualizacaoController** — base `/dataAtualizacao` (62)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/dataAtualizacao/painel-receitas` | `buscarDataAtualizacaoPainelReceitas` |
| GET | `/dataAtualizacao/multas-transito` | `buscarDataAtualizacaoMultasTransito` |
| GET | `/dataAtualizacao/receitas-por-orgao` | `buscarDataAtualizacaoOrgao` |
| GET | `/dataAtualizacao/receitas-consulta-dinamica` | `buscarDataAtualizacaoReceitasConsultaDinamica` |
| GET | `/dataAtualizacao/receitas-transferencia-uniao` | `buscarDataAtualizacaoReceitasUniao` |
| GET | `/dataAtualizacao/painel-despesas` | `buscarDataAtualizacaoPainelDespesas` |
| GET | `/dataAtualizacao/nota-empenho` | `buscarDataAtualizacaoNotaEmpenho` |
| GET | `/dataAtualizacao/nota-lancamento` | `buscarDataAtualizacaoNotaLancamento` |
| GET | `/dataAtualizacao/ordem-bancaria` | `buscarDataAtualizacaoOrdemBancaria` |
| GET | `/dataAtualizacao/detalhamento` | `buscarDataAtualizacaoDetalhamento` |
| GET | `/dataAtualizacao/emendas-parlamentares` | `buscarDataAtualizacaoEmendasParlamentares` |
| GET | `/dataAtualizacao/execucao-emendas` | `buscarDataAtualizacaoExecucaoEmendas` |
| GET | `/dataAtualizacao/execucao-oca` | `buscarDataAtualizacaoExecucaoOCA` |
| GET | `/dataAtualizacao/diarias-passagens` | `buscarDataAtualizacaoDiariasPassagens` |
| GET | `/dataAtualizacao/restos-a-pagar` | `buscarDataAtualizacaoRestosPagar` |
| GET | `/dataAtualizacao/despesas-consulta-dinamica` | `buscarDataAtualizacaoConsultaDinamicaDespesas` |
| GET | `/dataAtualizacao/detalhamentos/saiba-mais` | `buscarDataAtualizacaoDespesasDetalhamentosSaibaMais` |
| GET | `/dataAtualizacao/painel-servidores` | `buscarDataAtualizacaoPainelServidores` |
| GET | `/dataAtualizacao/remuneracao-servidores` | `buscarDataAtualizacaoRemuneracaoServidores` |
| GET | `/dataAtualizacao/servidores-por-orgao` | `buscarDataAtualizacaoServidoresPorOrgao` |
| GET | `/dataAtualizacao/tabela-remuneracao` | `buscarDataAtualizacaoTabelaRemuneracao` |
| GET | `/dataAtualizacao/expulsoes-servidores` | `buscarDataAtualizacaoExpulsoesServidores` |
| GET | `/dataAtualizacao/cargo-comissionado` | `buscarDataAtualizacaoCargoComissionado` |
| GET | `/dataAtualizacao/cargo-efetivo` | `buscarDataAtualizacaoCargoEfetivo` |
| GET | `/dataAtualizacao/quadro-servidores` | `buscarDataAtualizacaoQuadroServidores` |
| GET | `/dataAtualizacao/perfil-servidores` | `buscarDataAtualizacaoPerfilServidores` |
| GET | `/dataAtualizacao/painel-licitacao-contratos` | `buscarDataAtualizacaoPainelLicitacaoContratos` |
| GET | `/dataAtualizacao/contratos` | `buscarDataAtualizacaoContratos` |
| GET | `/dataAtualizacao/licitacao` | `buscarDataAtualizacaoLicitacao` |
| GET | `/dataAtualizacao/itens-licitados` | `buscarDataAtualizacaoItensLicitados` |
| GET | `/dataAtualizacao/convenio-receita` | `buscarDataAtualizacaoConvenioReceita` |
| GET | `/dataAtualizacao/convenio-despesa` | `buscarDataAtualizacaoConvenioDespesa` |
| GET | `/dataAtualizacao/relatorio-convenio` | `buscarDataAtualizacaoRelatorioConvenio` |
| GET | `/dataAtualizacao/programas-sociais` | `buscarDataAtualizacaoProgramasSociais` |
| GET | `/dataAtualizacao/material-escolar` | `buscarDataAtualizacaoMaterialEscolar` |
| GET | `/dataAtualizacao/empresas-punidas` | `buscarDataAtualizacaoEmpresasPunidas` |
| GET | `/dataAtualizacao/hora/empresas-punidas` | `horaAtualizacaoEmpresasPunidas` |
| GET | `/dataAtualizacao/gastos-publicidade` | `buscarDataAtualizacaoGastosPublicidade` |
| GET | `/dataAtualizacao/processos-administrativos-disciplinares` | `buscarDataAtualizacaoPADs` |
| GET | `/dataAtualizacao/processos-investigacoes-preliminares` | `buscarDataAtualizacaoPIPs` |
| GET | `/dataAtualizacao/beneficiarios-auxilio-emergencial` | `buscarDataBeneficiariosAuxilioEmergencial` |
| GET | `/dataAtualizacao/beneficiarios-prato-cheio` | `buscarDataBeneficiariosPratoCheio` |
| GET | `/dataAtualizacao/beneficiarios-artistico-cultural` | `buscarDataBeneficiariosArtisticoCultural` |
| GET | `/dataAtualizacao/beneficiarios-mobilidade-cidada` | `buscarDataBeneficiariosMobilidadeCidada` |
| GET | `/dataAtualizacao/orgaos-deliberativos` | `buscarDataAtualizacaoOrgaosDeliberativos` |
| GET | `/dataAtualizacao/shows-eventos` | `buscarDataAtualizacaoShowsEventos` |
| GET | `/dataAtualizacao/outros-relatorios` | `buscarDataAtualizacaoOutrosRelatorios` |
| GET | `/dataAtualizacao/empresa-programa-integridade` | `buscarHoraAtualizacaoProgramaIntegridade` |
| GET | `/dataAtualizacao/beneficiarios-bolsa-alimentacao` | `buscarHoraAtualizacaoBeneficiariosBolsaAlimentacao` |
| GET | `/dataAtualizacao/militares-cedidos` | `buscarHoraAtualizacaoMilitaresCedidos` |
| GET | `/dataAtualizacao/ppa` | `buscarDataAtualizacaoPPA` |
| GET | `/dataAtualizacao/ldo` | `buscarDataAtualizacaoLDO` |
| GET | `/dataAtualizacao/loa` | `buscarDataAtualizacaoLOA` |
| GET | `/dataAtualizacao/responsabilidade-fiscal` | `buscarDataAtualizacaoResponsabilidadeFiscal` |
| GET | `/dataAtualizacao/relatorios-gerenciais` | `buscarDataAtualizacaoRelatoriosGerenciais` |
| GET | `/dataAtualizacao/bens-moveis` | `buscarDataAtualizacaoBensMoveis` |
| GET | `/dataAtualizacao/bens-imoveis` | `buscarDataAtualizacaoBensImoveis` |
| GET | `/dataAtualizacao/patrimonio-por-orgao` | `buscarDataAtualizacaoPatrimonioPorOrgao` |
| GET | `/dataAtualizacao/relatorios` | `buscarDataAtualizacaoRelatorios` |
| GET | `/dataAtualizacao/materialescolar-saibamais` | `buscarDataAtualizacaoSaibaMaisMaterialEscolar` |
| GET | `/dataAtualizacao/organizacoes-sociais-saude` | `buscarDataAtualizacaoOrganizacoesSociaisSaude` |
| GET | `/dataAtualizacao/prospera-df` | `buscarDataAtualizacaoProsperaDF` |

### Despesa

**DespesaController** — base `/despesa` (48)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/lista-programa-trabalho` | `recuperarListaProgramaTrabalho` |
| GET | `/despesa/nota-empenho` | `pesquisarEmpenhado` |
| GET | `/despesa/nota-lancamento` | `pesquisarNotaLancamento` |
| GET | `/despesa/ordem-bancaria` | `pesquisarOrdemBancaria` |
| GET | `/despesa/ordem-bancaria/gestoes-nl` | `listarObGestoesNl` |
| GET | `/despesa/ob-por-credor` | `pesquisarObPorCredor` |
| GET | `/despesa/ob-por-credor-detalhamento` | `pesquisarDetalhamentoObPorCredor` |
| GET | `/despesa/consulta-dinamica` | `consultaDinamica` |
| GET | `/despesa/filtros` | `listarFiltros` |
| GET | `/despesa/filtrosCovid` | `listarFiltrosCovid` |
| GET | `/despesa/filtrosCovidAuxUni` | `listarFiltrosCovidAuxUni` |
| GET | `/despesa/unidadeGestora` | `listarUnidadeGestora` |
| GET | `/despesa/gestao` | `listarGestao` |
| GET | `/despesa/esfera` | `listarEsfera` |
| GET | `/despesa/funcao` | `listarFuncao` |
| GET | `/despesa/subfuncao` | `listarSubFuncao` |
| GET | `/despesa/programa` | `listarPrograma` |
| GET | `/despesa/modalidadeLicitacao` | `listarModalidadeLicitacao` |
| GET | `/despesa/categoria-economica` | `listarCategoriaEconomica` |
| GET | `/despesa/grupo-natureza` | `listarGrupoNatureza` |
| GET | `/despesa/modalidade-aplicacao` | `listarModalidadeAplicacao` |
| GET | `/despesa/elemento` | `listarElemento` |
| GET | `/despesa/nota-empenho/extrato` | `listarNotasDeEmpenhoFilhas` |
| GET | `/despesa/nota-empenho/subitem` | `listarNotasDeEmpenhoSubitem` |
| GET | `/despesa/nota-empenho/notas-lancamento` | `listarNotasDeLancamentoPorNeOriginal` |
| GET | `/despesa/nota-empenho/ordem-bancaria` | `listarOrdemBancariaPorNeOriginal` |
| GET | `/despesa/anos` | `listarAnos` |
| GET | `/despesa/pagamentos-por-credor/anos` | `recuperarAnos` |
| GET | `/despesa/nota-empenho/{anoNotaEmpenho}/{codigoGestao}/{codigoUnidadeGestora}/{numeroNotaEmpenho}` | `recuperarNotaEmpenho` |
| GET | `/despesa/nota-lancamento/{ano}/{codigoGestao}/{codigoUnidadeGestora}/{notaLancamento}/{numeroNotaEmpenho}` | `recuperarNotaLancamento` |
| GET | `/despesa/nota-lancamento-ob/{ano}/{codigoGestao}/{codigoUnidadeGestora}/{notaLancamento}` | `recuperarNotaLancamentoOB` |
| GET | `/despesa/ordem-bancaria/{ano}/{codigoGestao}/{codigoUnidadeGestora}/{ordemBancaria}` | `recuperarOrdemBancaria` |
| GET | `/despesa/nota-empenho/por-ordem-bancaria` | `listarNotaEmpenhoPorOrdemBancaria` |
| GET | `/despesa/nota-lancamento/por-ordem-bancaria` | `listarNotasLancamentoPorOrdemBancaria` |
| GET | `/despesa/nota-empenho/por-nota-lancamento` | `listarNotaEmpenhoPorNotaLancamento` |
| GET | `/despesa/nota-empenho/por-nota-lancamento-detalhe-nl` | `listarNotaEmpenhoPorNotaLancamentoDetalheNL` |
| GET | `/despesa/descricao` | `listarDescricaoNotaEmpenho` |
| GET | `/despesa/nota-fiscal` | `listarNotaFiscalNotaEmpenho` |
| GET | `/despesa/nota-lancamento/eventos` | `listarEventoNotaLancamento` |
| POST | `/despesa/diarias-passagens/subitemPorElemento` | `listarSubitemPorElemento` |
| POST | `/despesa/ordens-cancelamento` | `listarOrdemCancelamentoPorOB` |
| GET | `/despesa/adm-regionais` | `admregionais` |
| GET | `/despesa/liquidado-adm` | `liquidadoadm` |
| GET | `/despesa/despesa-anual` | `listarDespesasAnuais` |
| GET | `/despesa/prioridades` | `listarPrioridades` |
| GET | `/despesa/covid-por-itens` | `listarDespesasCovidPorItem` |
| GET | `/despesa/saiba-mais` | `listarSaibaMais` |
| GET | `/despesa/saiba-mais-obras` | `listarSaibaMaisObras` |

**DespesaGraficoController** — base `/despesa/grafico` (11)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/grafico/funcao/{ano}` | `graficoFuncaoExercicio` |
| GET | `/despesa/grafico/grupo/{ano}` | `graficoGrupoExercicio` |
| GET | `/despesa/grafico/tipodespesa/{ano}` | `graficoTipoDespesaExercicio` |
| GET | `/despesa/grafico/evolucao` | `graficoEvolucaoAnual` |
| GET | `/despesa/grafico/percentual/categoria-economica` | `recuperarPercentualDespesasCorrentes` |
| GET | `/despesa/grafico/receitas-despesas` | `listarEvolucaoReceitasDespesa` |
| GET | `/despesa/grafico/grupo-despesa` | `listarEvolucaoGrupoDespesa` |
| GET | `/despesa/grafico/evolucao-funcao` | `listarEvolucaoFuncao` |
| GET | `/despesa/grafico/treemap/{ano}` | `graficoTreemap` |
| GET | `/despesa/grafico/treemap/subfuncao` | `graficoTreemapSubfuncao` |
| GET | `/despesa/grafico/dataAtualizacao` | `buscarDataAtualizacaoPainel` |

**DespesaRelatorioController** — base `/despesa/relatorio` (27)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/relatorio/consulta-dinamica` | `relatorioConsultaDinamica` |
| GET | `/despesa/relatorio/exerciciosAnteriores` | `relatorioExerciciosAnteriores` |
| GET | `/despesa/relatorio/obrasInstalacoes` | `relatorioObrasInstalacoes` |
| GET | `/despesa/relatorio/ressarcimento-requisitado` | `relatorioRessarcimentoRequisitado` |
| GET | `/despesa/relatorio/acao` | `relatorioPesquisaPorAcao` |
| GET | `/despesa/relatorio/credor` | `relatorioPesquisaPorCredor` |
| GET | `/despesa/relatorio/orgao` | `relatorioPesquisaPorOrgao` |
| GET | `/despesa/relatorio/covidorgao` | `relatorioPesquisaCovidPorOrgao` |
| GET | `/despesa/relatorio/suprimento` | `relatorioPesquisaPorSuprimento` |
| GET | `/despesa/relatorio/covidAuxilioUniao` | `relatorioPesquisaCovidAuxilioUniao` |
| GET | `/despesa/relatorio/nota-empenho` | `relatorioEmpenho` |
| GET | `/despesa/relatorio/nota-lancamento` | `relatorioLancamento` |
| GET | `/despesa/relatorio/nota-lancamento-emendas` | `relatorioLancamentoEmendas` |
| GET | `/despesa/relatorio/ordem-bancaria` | `relatorioOrdemBancaria` |
| GET | `/despesa/relatorio/ordem-bancaria-emendas` | `relatorioOrdemBancariaEmendas` |
| GET | `/despesa/relatorio/ob-por-credor` | `relatorioOrdemBancariaPorCredor` |
| GET | `/despesa/relatorio/ob-por-credor-detalhamento` | `relatorioOrdemBancariaPorCredor` |
| GET | `/despesa/relatorio/detalhamento` | `relatorioDetalhamento` |
| GET | `/despesa/relatorio/emendas-parlamentares` | `relatorioEmendasParlamentares` |
| GET | `/despesa/relatorio/emendas-parlamentares-federais` | `relatorioEmendasParlamentaresFederais` |
| GET | `/despesa/relatorio/execucao-emendas` | `relatorioExecucaoEmendas` |
| GET | `/despesa/relatorio/execucao-oca` | `relatorioExecucaoOca` |
| GET | `/despesa/relatorio/diarias-passagens` | `relatorioExecucaoOca` |
| GET | `/despesa/relatorio/detalhe-detalhamento` | `relatorioDetalhamentoDespesa` |
| GET | `/despesa/relatorio/execucao-oca-detalhe` | `relatorioExecucaoOcaDetalhe` |
| GET | `/despesa/relatorio/execucao-emendas-detalhe` | `relatorioExecucaoEmendaDetalhe` |
| GET | `/despesa/relatorio/covid-por-itens` | `relatorioDespesaCovidPorItem` |

**DetalhamentoController** — base `/despesa/detalhamento` (6)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/detalhamento` | `pesquisar` |
| GET | `/despesa/detalhamento/{anoExercicio}/{codigoUnidadeGestora}` | `listarDetalhamentoDespesaPorProjeto` |
| GET | `/despesa/detalhamento/subitem` | `listaDetalhamentoDespesaSubitem` |
| GET | `/despesa/detalhamento/unidade-gestora` | `listarDestalhamentoDespesaUnidadegestora` |
| GET | `/despesa/detalhamento/gestao` | `listarDestalhamentoDespesaGestao` |
| GET | `/despesa/detalhamento/ano` | `listarDestalhamentoDespesaAno` |

**DiariasPassagensController** — base `/despesa/diarias-passagens` (19)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/diarias-passagens` | `pesquisar` |
| GET | `/despesa/diarias-passagens/saiba-mais` | `pequisarDiariasEPassagensSaibaMais` |
| GET | `/despesa/diarias-passagens/anos` | `listarAnos` |
| GET | `/despesa/diarias-passagens/unidades-gestoras` | `listarUnidades` |
| GET | `/despesa/diarias-passagens/elementos` | `listarElementos` |
| GET | `/despesa/diarias-passagens/sub-elementos` | `listarSubelementos` |
| GET | `/despesa/diarias-passagens/gestoes` | `listarGestoes` |
| GET | `/despesa/diarias-passagens/esferas` | `listarEsferas` |
| GET | `/despesa/diarias-passagens/tipos-despesa` | `listarTiposDespesa` |
| GET | `/despesa/diarias-passagens/funcoes` | `listarFuncoes` |
| GET | `/despesa/diarias-passagens/subfuncoes` | `listarSubfuncoes` |
| GET | `/despesa/diarias-passagens/programas` | `listarProgramas` |
| GET | `/despesa/diarias-passagens/categorias-economicas` | `listarCategoriasEconomicas` |
| GET | `/despesa/diarias-passagens/grupos-despesa` | `listarGruposDespesa` |
| GET | `/despesa/diarias-passagens/modalidades-aplicacoes` | `listarModalidadesAplicacoes` |
| GET | `/despesa/diarias-passagens/fontes-recurso` | `listarFontesRecurso` |
| GET | `/despesa/diarias-passagens/nota-empenho` | `pesquisarEmpenhadoDiariasEPassagens` |
| GET | `/despesa/diarias-passagens/nota-lancamento` | `pesquisarNotaLancamentoDiariasEPassagens` |
| GET | `/despesa/diarias-passagens/ordem-bancaria` | `pesquisarOrdemBancariaDiariasEPassagens` |

**EmendaParlamentarFederalController** — base `/despesa/emenda-parlamentar-federal` (3)

| Verbo | Caminho | Método Java |
|---|---|---|
| ANY | `/despesa/emenda-parlamentar-federal` | `pesquisar` |
| GET | `/despesa/emenda-parlamentar-federal/parlamentares` | `listarParlamentares` |
| GET | `/despesa/emenda-parlamentar-federal/orgaos-executores` | `listarOrgaosExecutores` |

**EmendasParlamentaresController** — base `/despesa/emendas-parlamentares` (17)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/emendas-parlamentares` | `pesquisar` |
| GET | `/despesa/emendas-parlamentares/anos` | `listarAnosEmendasParlamentares` |
| GET | `/despesa/emendas-parlamentares/autor` | `listarAutor` |
| GET | `/despesa/emendas-parlamentares/filtros` | `listarFiltros` |
| GET | `/despesa/emendas-parlamentares/categoria` | `listaCategoriasQdd` |
| GET | `/despesa/emendas-parlamentares/elemento` | `listaElementoQdd` |
| GET | `/despesa/emendas-parlamentares/fonte` | `listaFontesQdd` |
| GET | `/despesa/emendas-parlamentares/fonteEmendas` | `listarFontesEmendas` |
| GET | `/despesa/emendas-parlamentares/funcao` | `listaFuncoesQdd` |
| GET | `/despesa/emendas-parlamentares/subfuncao` | `listaSubfuncoesQdd` |
| GET | `/despesa/emendas-parlamentares/grupo` | `listaGruposQdd` |
| GET | `/despesa/emendas-parlamentares/modalidade-aplicacao` | `listaModalidadeAplicacaoQdd` |
| GET | `/despesa/emendas-parlamentares/programa` | `listaProgramaQdd` |
| GET | `/despesa/emendas-parlamentares/dataAtualizacao` | `buscarDataAtualizacaoEmendasParlamentares` |
| GET | `/despesa/emendas-parlamentares/nota-empenho` | `retornarNotasEmpenhoEmendas` |
| GET | `/despesa/emendas-parlamentares/nota-lancamento` | `retornarNotasLancamentoEmendas` |
| GET | `/despesa/emendas-parlamentares/ordem-bancaria` | `pesquisarOrdemBancariaEmendas` |

**ExecucaoEmendasController** — base `/despesa/execucao-emendas` (2)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/execucao-emendas` | `pesquisar` |
| GET | `/despesa/execucao-emendas/{anoExercicio}/{codigoUnidadeGestora}` | `listarDestalhamentoExecucaoEmendas` |

**ExecucaoOcaController** — base `/despesa/oca` (5)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/oca` | `pesquisar` |
| GET | `/despesa/oca/{anoExercicio}/{codigoUnidadeGestora}` | `listarDestalhamentoExecucaoOca` |
| GET | `/despesa/oca/anos` | `listarAnosOca` |
| GET | `/despesa/oca/unidades-gestoras` | `listarUnidadesGestorasOCA` |
| GET | `/despesa/oca/gestoes` | `listarGestoesOCA` |

**RestosAPagarController** — base `/despesa/restos-a-pagar` (3)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/despesa/restos-a-pagar` | `pesquisar` |
| GET | `/despesa/restos-a-pagar/anos` | `listarAnos` |
| GET | `/despesa/restos-a-pagar/relatorio` | `relatorioConsultaDinamica` |

### Licitações e contratos (v1)

**LicitacoesContratosController** — base `/licitacoes-contratos` (14)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/licitacoes-contratos/contrato` | `pesquisarContrato` |
| GET | `/licitacoes-contratos/nota-empenho/extrato` | `listarNotasDeEmpenhoFilhas` |
| GET | `/licitacoes-contratos/licitacao/modalidade` | `listarLicitacaoModalidade` |
| GET | `/licitacoes-contratos/licitacao/propostas` | `listarLicitacaoPropostas` |
| GET | `/licitacoes-contratos/licitacao/processo-orgao` | `listarLicitacaoProcessoOrgao` |
| GET | `/licitacoes-contratos/licitacao/vencedores` | `listarLicitacaoVencedores` |
| GET | `/licitacoes-contratos/contrato/aditivos` | `listarContratoAditivos` |
| GET | `/licitacoes-contratos/contrato/fonte-recurso` | `listarFonteRecurso` |
| GET | `/licitacoes-contratos/funcao` | `listarFuncao` |
| GET | `/licitacoes-contratos/gestao` | `listarGestao` |
| GET | `/licitacoes-contratos/modalidade-licitacao` | `listarModalidadeLicitacao` |
| GET | `/licitacoes-contratos/unidade-gestora` | `listarUnidadeGestora` |
| GET | `/licitacoes-contratos/grafico/evolucao-modalidade` | `graficoEvolucaoModalidade` |
| GET | `/licitacoes-contratos/contrato/anos` | `listarAnosLicitacoesContratos` |

**LicitacoesContratosRelatorioController** — base `/licitacoes-contratos/relatorio` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/licitacoes-contratos/relatorio/contrato` | `relatorioContrato` |

### Orçamento

**OrcamentoController** — base `/orcamento` (14)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/orcamento/ldo` | `pesquisarLdo` |
| GET | `/orcamento/loa` | `pesquisarLoa` |
| GET | `/orcamento/ppa` | `pesquisarPpa` |
| GET | `/orcamento/responsabilidade-fiscal` | `pesquisarResponsabilidadeFiscal` |
| GET | `/orcamento/relatorios-gerenciais` | `pesquisarRelatoriosGerenciais` |
| GET | `/orcamento/relatorios-gerenciais/anos` | `listarAnosRelatoriosGerenciais` |
| GET | `/orcamento/ldo/anos` | `listarAnosLdo` |
| GET | `/orcamento/loa/anos` | `listarAnosLoa` |
| GET | `/orcamento/lrf/anos` | `listarAnosLrf` |
| GET | `/orcamento/assuntosLRF` | `listarAssuntosLRF` |
| GET | `/orcamento/assuntosRelatoriosGerenciais` | `listaAssuntosRelatoriosGerenciais` |
| GET | `/orcamento/listarDataReferenciaPorAssunto` | `listarDataReferenciaPorAssunto` |
| POST | `/orcamento/categorias` | `getCategorias` |
| POST | `/orcamento/data-referencias` | `getDataReferencia` |

**RelatorioController** — base `/relatorio` (3)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/relatorio/loa/ultimo-ano` | `ultimoAnoDisponivelLoa` |
| GET | `/relatorio/ldo/ultimo-ano` | `ultimoAnoDisponivelLdo` |
| GET | `/relatorio/relatorios-gerenciais/ultimo-ano` | `ultimoAnoDisponivelRelatoriosGerenciais` |

### Patrimônio (v1)

**PatrimonioController** — base `/patrimonio` (12)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/patrimonio/demonstrativos/datas-referencia` | `listarDatasReferenciasDemonstrativos` |
| GET | `/patrimonio/demonstrativos/anos` | `listarAnosReceita` |
| GET | `/patrimonio/bens-moveis` | `pesquisarBensMoveis` |
| GET | `/patrimonio/localizacao` | `pesquisarLocalizacao` |
| GET | `/patrimonio/localizacao/orgaos` | `listarOrgaoLocalizacao` |
| GET | `/patrimonio/bens-moveis/unidades-gestoras` | `listarUnidadeGestoraBensMoveis` |
| POST | `/patrimonio/bens-moveis/unidades-gestoras` | `listarUnidadeGestoraBensMoveisPorAno` |
| GET | `/patrimonio/bens-moveis/gestoes` | `listarGestao` |
| POST | `/patrimonio/bens-moveis/gestoes` | `listarGestaoPorUnidadeGestora` |
| GET | `/patrimonio/bens-moveis/anos` | `listarAnosBensMoveis` |
| GET | `/patrimonio/bens-moveis/ultimo-ano` | `ultimoAnoBensMoveis` |
| GET | `/patrimonio/relatorio` | `pesquisarDemonstrativos` |

**PatrimonioRelatorioController** — base `/patrimonio/relatorio` (2)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/patrimonio/relatorio/bens-moveis` | `relatorioBensMoveis` |
| GET | `/patrimonio/relatorio/localizacao` | `relatorioPorOrgaoLocalizacao` |

### Prestação de contas

**BeneficiariosAuxilioEmergencialController** — base `/prestando-contas` (10)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/beneficiarios-auxilio-emergencial` | `listarBeneficiariosAuxilioEmergencial` |
| GET | `/prestando-contas/beneficiarios-auxilio-emergencial/meses-referencia` | `listarMesesReferenciaBeneficiarioAuxilioEmergencial` |
| GET | `/prestando-contas/beneficiarios-prato-cheio` | `listarBeneficiariosPratoCheio` |
| GET | `/prestando-contas/beneficiarios-prato-cheio/anos-referencia` | `listarAnosReferenciaBeneficiarioPratoCheio` |
| GET | `/prestando-contas/beneficiarios-prato-cheio/meses-referencia` | `listarMesesReferenciaBeneficiarioPratoCheio` |
| GET | `/prestando-contas/beneficiarios-artistico-cultural` | `listarBeneficiariosArtisticoCultural` |
| GET | `/prestando-contas/beneficiarios-artistico-cultural/anos-referencia` | `listarAnosReferenciaBeneficiarioArtisticoCultural` |
| GET | `/prestando-contas/beneficiarios-mobilidade-cidada` | `listarBeneficiariosMobilidadeCidada` |
| GET | `/prestando-contas/beneficiarios-mobilidade-cidada/concessoes` | `listarConcessoesBeneficiarioMobilidadeCidada` |
| GET | `/prestando-contas/beneficiarios-mobilidade-cidada/exercicios` | `listarExerciciosBeneficiarioMobilidadeCidada` |

**BeneficiariosAuxilioEmergencialRelatorioController** — base `/prestando-contas/relatorios` (4)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/relatorios/beneficiarios-auxilio-emergencial` | `gerarRelatorioBeneficiariosAuxilioEmergencial` |
| GET | `/prestando-contas/relatorios/beneficiarios-prato-cheio` | `gerarRelatorioBeneficiariosPratoCheio` |
| GET | `/prestando-contas/relatorios/beneficiarios-artistico-cultural` | `gerarRelatorioBeneficiariosArtisticoCultural` |
| GET | `/prestando-contas/relatorios/beneficiarios-mobilidade-cidada` | `gerarRelatorioBeneficiariosMobilidadeCidada` |

**BeneficiariosBolsaAlimentacaoController** — base `/prestando-contas/beneficiarios-bolsa-alimentacao` (5)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/beneficiarios-bolsa-alimentacao` | `listarBeneficiarios` |
| GET | `/prestando-contas/beneficiarios-bolsa-alimentacao/ano` | `listarAnosBeneficiariosBolsaAlimentacao` |
| GET | `/prestando-contas/beneficiarios-bolsa-alimentacao/mes` | `listarMesBeneficiariosBolsaAlimentacao` |
| GET | `/prestando-contas/beneficiarios-bolsa-alimentacao/regime` | `listarRegimeBeneficiariosBolsaAlimentacao` |
| GET | `/prestando-contas/beneficiarios-bolsa-alimentacao/nome-escola` | `listarNomeEscolaBeneficiariosBolsaAlimentacao` |

**BeneficiariosBolsaAlimentacaoRelatorioController** — base `/prestando-contas/beneficiarios-bolsa-alimentacao/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/beneficiarios-bolsa-alimentacao/relatorios` | `relatorioBeneficiariosBolsaAlimentacao` |

**ConselheiroController** — base `/prestando-contas` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/conselheiros` | `pesquisarConselheiros` |

**EmpresaProgramaIntegridadeController** — base `/prestando-contas/empresas-programa-integridade` (7)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/empresas-programa-integridade` | `listarEmpresas` |
| GET | `/prestando-contas/empresas-programa-integridade/situacoes` | `listarSituacoesEmpresaProgramaIntegridade` |
| GET | `/prestando-contas/empresas-programa-integridade/orgao-contratante` | `listarOrgaoContratanteEmpresaProgramaIntegridade` |
| GET | `/prestando-contas/empresas-programa-integridade/ano-data-apresentacao` | `listarAnoDataApresentacaoProgramaIntegridade` |
| GET | `/prestando-contas/empresas-programa-integridade/mes-data-apresentacao` | `listarMesDataApresentacaoProgramaIntegridade` |
| GET | `/prestando-contas/empresas-programa-integridade/ano-data-avaliacao` | `listarAnoDataAvaliacaoProgramaIntegridade` |
| GET | `/prestando-contas/empresas-programa-integridade/mes-data-avaliacao` | `listarMesDataAvaliacaoProgramaIntegridade` |

**EmpresaProgramaIntegridadeRelatorioController** — base `/prestando-contas/empresas-programa-integridade/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/empresas-programa-integridade/relatorios` | `relatorioEmpresa` |

**EmpresaPunidaController** — base `/empresa-punida` (6)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/empresa-punida/anos` | `listaAnos` |
| GET | `/empresa-punida/sancao` | `listarTipoSancao` |
| GET | `/empresa-punida/orgao` | `listarOrgao` |
| GET | `/empresa-punida/uf` | `listarUnidadesFederacao` |
| GET | `/empresa-punida/tipo-pessoa` | `listarTiposPessoa` |
| GET | `/empresa-punida/origem-informacoes` | `listarOrigemInformacoes` |

**PADController** — base `/prestando-contas/processos-administrativos-disciplinares` (6)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/processos-administrativos-disciplinares` | `listarPADs` |
| GET | `/prestando-contas/processos-administrativos-disciplinares/tipos` | `listarTiposPADs` |
| GET | `/prestando-contas/processos-administrativos-disciplinares/orgaos` | `listarOrgaosPADs` |
| GET | `/prestando-contas/processos-administrativos-disciplinares/fases` | `listarFasesPADs` |
| GET | `/prestando-contas/processos-administrativos-disciplinares/{codigoDocumento}/acoes` | `listarAcoesPAD` |
| GET | `/prestando-contas/processos-administrativos-disciplinares/{codigoDocumento}/fases` | `listarFasesPAD` |

**PADRelatorioController** — base `/prestando-contas/processos-administrativos-disciplinares/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/processos-administrativos-disciplinares/relatorios` | `relatorioPAD` |

**PIPController** — base `/prestando-contas/processos-investigacoes-preliminares` (6)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/processos-investigacoes-preliminares` | `listarPIPs` |
| GET | `/prestando-contas/processos-investigacoes-preliminares/tipos` | `listarTiposPIPs` |
| GET | `/prestando-contas/processos-investigacoes-preliminares/orgaos` | `listarOrgaosPIPs` |
| GET | `/prestando-contas/processos-investigacoes-preliminares/fases` | `listarFasesPIPs` |
| GET | `/prestando-contas/processos-investigacoes-preliminares/{codigoDocumento}/acoes` | `listarAcoesPIP` |
| GET | `/prestando-contas/processos-investigacoes-preliminares/{codigoDocumento}/fases` | `listarFasesPIP` |

**PIPRelatorioController** — base `/prestando-contas/processos-investigacoes-preliminares/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/processos-investigacoes-preliminares/relatorios` | `relatorioPIP` |

**PrestandoContasController** — base `/prestando-contas` (39)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/orgaos-deliberativos/saiba-mais` | `pesquisarSaibaMaisOrgaosDeliberativos` |
| GET | `/prestando-contas/relatorio-gerencial` | `pesquisarRelatoriosGerenciais` |
| GET | `/prestando-contas/gastos-publicidade` | `pesquisarGastosComPublicidade` |
| GET | `/prestando-contas/outros-relatorios` | `pesquisarResponsabilidadeFiscal` |
| GET | `/prestando-contas/outros-relatorios/anos` | `listarAnosOutrosRelatorios` |
| GET | `/prestando-contas/outros-relatorios/categorias` | `listarCategoriasOutrosRelatorios` |
| GET | `/prestando-contas/beneficiario/cartao` | `pesquisarBeneficiariosCartaoMaterialEscolar` |
| GET | `/prestando-contas/beneficiario/cartao/anos` | `listarAnosCartaoMaterialEscolar` |
| GET | `/prestando-contas/beneficiario/cartao/lotes` | `listarLoteCartaoMaterialEscolar` |
| GET | `/prestando-contas/beneficiario/programa-social` | `pesquisarBeneficiariosProgramasSociais` |
| GET | `/prestando-contas/beneficiario/programa-social/ultimo-mes-ano` | `ultimoMesAnoBeneficiarioProgramaSocial` |
| GET | `/prestando-contas/beneficiario/programa-social/anos` | `listarAnosBeneficiarioProgramaSocial` |
| GET | `/prestando-contas/beneficiario/programa-social/programas` | `listarProgramasBeneficiarioProgramaSocial` |
| GET | `/prestando-contas/orgao-deliberativo` | `pesquisarOrgaoDeliberativo` |
| GET | `/prestando-contas/orgao-deliberativo-detalhe` | `pesquisarListaOrgaoDeliberativo` |
| GET | `/prestando-contas/orgao-deliberativo-tipo` | `pesquisarListaTipoOrgaoDeliberativo` |
| GET | `/prestando-contas/orgao-deliberativo-vinculacao` | `pesquisarListaOrgaoDeliberativoVinculacao` |
| GET | `/prestando-contas/orgao-deliberativo-titularidade` | `pesquisarListaTitularidades` |
| GET | `/prestando-contas/orgao-deliberativo-representacoes` | `pesquisarListaRepresentacoes` |
| GET | `/prestando-contas/orgao-deliberativo-grau` | `pesquisarListaGrau` |
| GET | `/prestando-contas/shows-eventos` | `pesquisarShowEventos` |
| GET | `/prestando-contas/valor-total` | `valorTotal` |
| GET | `/prestando-contas/shows-eventos/orgao` | `listarOrgaosShowsEventos` |
| GET | `/prestando-contas/shows-eventos/anos` | `listarAnosShowsEventos` |
| GET | `/prestando-contas/gastos-publicidade/anos` | `listarAnosGastosComPublicidade` |
| GET | `/prestando-contas/beneficiario/programa-social/legislacao` | `pequisarBeneficiariosProgramasSociaisLegislacao` |
| GET | `/prestando-contas/beneficiario/cartao/saiba-mais` | `pequisarBeneficiariosCartaoMaterialEscolarSaibaMais` |
| POST | `/prestando-contas/categorias` | `getCategorias` |
| POST | `/prestando-contas/data-referencias` | `getDataReferencia` |
| GET | `/prestando-contas/orgao-deliberativo-especie-conselhos` | `listarEspeciesDeConselho` |
| GET | `/prestando-contas/detalhamento-conselho` | `listarDetalhamentoConselho` |
| GET | `/prestando-contas/organizacoes-sociais-saude` | `pesquisarOrganizacoesSociaisSaude` |
| GET | `/prestando-contas/organizacoes-sociais-saude/anos` | `listarAnosOrganizacoesSociaisSaude` |
| GET | `/prestando-contas/organizacoes-sociais-saude/nomes` | `listarNomesOrganizacoesSociaisSaude` |
| GET | `/prestando-contas/organizacoes-sociais-saude/relatorios` | `listarRelatoriosOrganizacoesSociaisSaude` |
| GET | `/prestando-contas/prestacao-contas-anual/anos` | `listarAnosPrestacaoContaAnual` |
| GET | `/prestando-contas/beneficiario/acoes-emergenciais/saiba-mais` | `listarSaibaMaisBeneficiariosAcoesEmergenciais` |
| GET | `/prestando-contas/beneficiario/artistico-cultural/saiba-mais` | `listarSaibaMaisBeneficiariosArtistico` |
| GET | `/prestando-contas/beneficiario/mobilidade-cidada/saiba-mais` | `listarSaibaMaisBeneficiariosMobilidadeCidada` |

**PrestandoContasRelatorioController** — base `/prestando-contas/relatorio` (7)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/relatorio/empresa-punida/detalhamento` | `relatorioDetalhamentoEmpresaPunida` |
| GET | `/prestando-contas/relatorio/empresa-punida` | `relatorioEmpresaPunida` |
| GET | `/prestando-contas/relatorio/orgaos-deliberativos` | `relatorioOrgaosDeliberativos` |
| GET | `/prestando-contas/relatorio/beneficiario/programa-social` | `relatorioBeneficiariosProgramasSociais` |
| GET | `/prestando-contas/relatorio/beneficiario/cartao` | `relatorioBeneficiariosProgramasSociais` |
| GET | `/prestando-contas/relatorio/shows-eventos` | `relatorioBeneficiariosProgramasSociais` |
| GET | `/prestando-contas/relatorio/conselheiros` | `relatorioConselheiros` |

**ProsperaDFController** — base `/prestando-contas/prospera-df` (11)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/prospera-df` | `listarProspera` |
| GET | `/prestando-contas/prospera-df/ano` | `listarExercicioProspera` |
| GET | `/prestando-contas/prospera-df/personalidade` | `listaPersonalidade` |
| GET | `/prestando-contas/prospera-df/regiao` | `listaRegiaoAdministrativa` |
| GET | `/prestando-contas/prospera-df/carteira` | `listaCarteira` |
| GET | `/prestando-contas/prospera-df/comite` | `listaComite` |
| GET | `/prestando-contas/prospera-df/porte` | `listaPorte` |
| GET | `/prestando-contas/prospera-df/contrato` | `listaContrato` |
| GET | `/prestando-contas/prospera-df/modalidade` | `listaModalidade` |
| GET | `/prestando-contas/prospera-df/atividade` | `listaAtividade` |
| GET | `/prestando-contas/prospera-df/subatividade` | `listaSubatividade` |

**ProsperaDFRelatorioController** — base `/prestando-contas/prospera-df/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/prestando-contas/prospera-df/relatorios` | `relatorioProspera` |

### Receita

**ReceitaController** — base `/receita` (26)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/receita/multas` | `listarMultasTransito` |
| GET | `/receita/por-orgao` | `listarPorOrgao` |
| GET | `/receita/consulta-dinamica` | `listarPorOrgao` |
| GET | `/receita/multas/anos` | `listarAnosMultasTransito` |
| GET | `/receita/anos` | `listarAnos` |
| GET | `/receita/unidade-gestora` | `listarUnidadeGestora` |
| GET | `/receita/gestao` | `listarGestao` |
| GET | `/receita/fonte` | `listarFonte` |
| GET | `/receita/sub-fonte` | `listarSubFonte` |
| GET | `/receita/rubrica` | `listarRubrica` |
| GET | `/receita/alinea` | `listarAlinea` |
| GET | `/receita/sub-alinea` | `listarSubAlinea` |
| GET | `/receita/categoria` | `listarCategoria` |
| GET | `/receita/grafico/evolucao` | `graficoEvolucaoReceita` |
| GET | `/receita/grafico/impostos` | `graficoImpostos` |
| GET | `/receita/grafico/receitas-correntes` | `graficoReceitasCorrentes` |
| GET | `/receita/grafico/receita-categoria` | `graficoReceitaCategoria` |
| GET | `/receita/grafico/receitas-correntes/detalhar` | `listarDetalhamentoReceitasCorrentes` |
| GET | `/receita/grafico/percentual/impostos` | `recuperarPercentualImpostos` |
| GET | `/receita/grafico/percentual/taxas` | `recuperarPercentualTaxas` |
| GET | `/receita/grafico/evolucao-imposto` | `listarEvolucaoImposto` |
| GET | `/receita/grafico/arrecadacao-imposto` | `recuperarReceitaImposto` |
| GET | `/receita/receita-anual` | `listarReceitasAnuais` |
| GET | `/receita/fonte-recurso` | `listarReceitaAuxilioUniao` |
| GET | `/receita/fonte-recurso/exercicio` | `listarReceitaAuxilioUniaoExercicio` |
| GET | `/receita/fonte-recurso/filtro-recurso` | `listarFonteRecurso` |

**ReceitaRelatorioController** — base `/receita/relatorio` (5)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/receita/relatorio/multas` | `relatorioMultasTransito` |
| GET | `/receita/relatorio/por-orgao` | `relatorioPorOrgao` |
| GET | `/receita/relatorio/consulta-dinamica` | `relatorioConsultaDinamica` |
| GET | `/receita/relatorio/fonte-recurso` | `relatorioFonteRecurso` |
| GET | `/receita/relatorio/uniao` | `relatorioUniao` |

**ReceitaUniaoController** — base `/receita-uniao` (9)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/receita-uniao/transferencia` | `listarPorOrigem` |
| GET | `/receita-uniao/anos` | `listarAnos` |
| GET | `/receita-uniao/unidade-gestora` | `listarUnidadeGestora` |
| GET | `/receita-uniao/rubrica` | `listarRubrica` |
| GET | `/receita-uniao/alinea` | `listarAlinea` |
| GET | `/receita-uniao/sub-alinea` | `listarSubAlinea` |
| GET | `/receita-uniao/categoria` | `listarCategoria` |
| GET | `/receita-uniao/origem` | `listarSubFonteOrigem` |
| GET | `/receita-uniao/fonte` | `listarFonte` |

### Servidor e remuneração

**ExpulsaoController** — base `/expulsao` (5)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/expulsao` | `pesquisar` |
| GET | `/expulsao/orgao` | `listarOrgao` |
| GET | `/expulsao/punicao` | `listarPunicao` |
| GET | `/expulsao/cargo` | `listarCargo` |
| GET | `/expulsao/anos` | `listarAno` |

**ExpulsaoRelatorioController** — base `/expulsao/relatorio` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/expulsao/relatorio` | `relatorio` |

**MilitaresCedidosController** — base `servidor/militares-cedidos` (4)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/servidor/militares-cedidos` | `listarMilitaresCedidos` |
| GET | `/servidor/militares-cedidos/ano` | `listarAnoMilitaresCedidos` |
| GET | `/servidor/militares-cedidos/mes` | `listarMesMilitaresCedidos` |
| GET | `/servidor/militares-cedidos/nome-cedente` | `listarNomeCedenteMilitaresCedidos` |

**MilitaresCedidosRelatorioController** — base `servidor/militares-cedidos/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/servidor/militares-cedidos/relatorios` | `relatorioMilitares` |

**RemuneracaoController** — base `/remuneracao` (13)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/remuneracao` | `pesquisar` |
| GET | `/remuneracao/servidores/saiba-mais` | `pequisarRemuneracaoSaibaMais` |
| GET | `/remuneracao/orgao` | `listarOrgao` |
| GET | `/remuneracao/cargo` | `listarCargo` |
| GET | `/remuneracao/funcao` | `listarFuncao` |
| GET | `/remuneracao/situacao` | `listarSituacao` |
| GET | `/remuneracao/anos` | `listarAnos` |
| GET | `/remuneracao/extrato/{codigoMatricula}/{anoExercicio}/{codigoOrgaoArtificial}` | `listarExtratoAnual` |
| GET | `/remuneracao/atualizacao` | `recuperarDataAtualizacao` |
| GET | `/remuneracao/grafico/evolucao` | `graficoEvolucaoRemuneracao` |
| GET | `/remuneracao/ultimo-exercicio` | `recuperarUltimoExercicio` |
| GET | `/remuneracao/ultimo-exercicio-orgao` | `recuperarUltimoExercicioServidorOrgao` |
| GET | `/remuneracao/rubrica` | `recuperarRubricaPorServidor` |

**RemuneracaoRelatorioController** — base `/remuneracao/relatorio` (4)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/remuneracao/relatorio/detalhamento/{codigoIdentificacao}` | `relatorioPesquisaPorAcao` |
| GET | `/remuneracao/relatorio` | `relatorioRemuneracao` |
| GET | `/remuneracao/relatorio/extrato/{codigoMatricula}/{anoExercicio}` | `relatorioExtrato` |
| GET | `/remuneracao/relatorio/rubrica/{codigoMatricula}/{anoExercicio}/{codigoOrgaoArtificial}` | `relatorioRubrica` |

**ServidorController** — base `/servidor` (33)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/servidor` | `pesquisar` |
| GET | `/servidor/ressarcimento-requisitado/saiba-mais` | `ressarcimentoRequisitadosSaibaMais` |
| GET | `/servidor/cargo-comissionado` | `pequisarCargoComissionado` |
| GET | `/servidor/cargo-comissionado/orgaos` | `listarOrgaosCargoComissionado` |
| GET | `/servidor/ultimo-exercicio-cargo-comissionado` | `recuperarUltimoExercicio` |
| GET | `/servidor/ultimo-exercicio-cargo-efetivo` | `recuperarUltimoExercicioCargoEfetivo` |
| GET | `/servidor/carreira-cargo-efetivo` | `listarCarreiraCargoEfetivo` |
| GET | `/servidor/cargo-efetivo-descricao` | `listarDescricaoCargoEfetivo` |
| GET | `/servidor/cargo-efetivo` | `pequisarCargoEfetivo` |
| GET | `/servidor/listarAnosQuadro` | `listarAnos` |
| GET | `/servidor/simbolos` | `listarSimbolos` |
| GET | `/servidor/listarAnosTabelasRemuneracao` | `listarAnosTabela` |
| GET | `/servidor/listarArquivosRemuneracaoServidores` | `pesquisarArquivosRemuneracaoServidores` |
| GET | `/servidor/quadro` | `pequisarQuadro` |
| GET | `/servidor/tabela-remuneracao` | `pequisarTabelaRemuneracao` |
| GET | `/servidor/listarDataReferenciaPorRemuneracao` | `listarDataReferenciaPorRemuneracao` |
| GET | `/servidor/listarDataReferenciaPorPatrimonio` | `listarDataReferenciaPorPatrimonio` |
| GET | `/servidor/listarDataReferenciaPorTipo` | `listarDataReferenciaPorTipo` |
| GET | `/servidor/listarDataReferenciaPorPrestacaoContas` | `listarDataReferenciaPorGerenciais` |
| GET | `/servidor/listarDataReferenciaPorConvenio` | `listarDataReferenciaPorConvenio` |
| GET | `/servidor/listarDataReferenciaPorGdf` | `listarDataReferenciaPorGdf` |
| GET | `/servidor/funcoes` | `listarFuncoes` |
| GET | `/servidor/quadro/categoria` | `listarCategoriaRelatorio` |
| GET | `/servidor/regime` | `listarRegime` |
| GET | `/servidor/cargo` | `listarCargo` |
| GET | `/servidor/carreira` | `listarCarreira` |
| GET | `/servidor/situacao` | `listarSituacao` |
| GET | `/servidor/funcao` | `listarFuncao` |
| GET | `/servidor/orgao` | `listarOrgao` |
| GET | `/servidor/status` | `listarStatus` |
| GET | `/servidor/situacaoFuncional` | `listarSituacaoFuncional` |
| GET | `/servidor/anos` | `listarAno` |
| GET | `/servidor/url-pendencias` | `getUrlPendencias` |

**ServidorGraficoController** — base `/servidor/grafico` (12)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/servidor/grafico/carreira` | `graficoCarreira` |
| GET | `/servidor/grafico/regime` | `graficoRegime` |
| GET | `/servidor/grafico/sexo` | `graficoSexo` |
| GET | `/servidor/grafico/escolaridade` | `graficoEscolaridadeSexo` |
| GET | `/servidor/grafico/situacao` | `graficoSituacao` |
| GET | `/servidor/grafico/ativo` | `graficoAtivo` |
| GET | `/servidor/grafico/aposentado` | `graficoAposentado` |
| GET | `/servidor/grafico/pensao` | `graficoPensao` |
| GET | `/servidor/grafico/outros` | `graficoOutros` |
| GET | `/servidor/grafico/total` | `totalServidores` |
| GET | `/servidor/grafico/status` | `graficoStatus` |
| GET | `/servidor/grafico/idade` | `graficoIdade` |

**ServidorRelatorioController** — base `/servidor/relatorio` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/servidor/relatorio` | `relatorioPorOrgao` |

### API v2

**OrgaoLAIController** — base `/v2/orgaos-lai` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/orgaos-lai` | `listar` |

**DashboardExecucaoDasDepesasController** — base `v2/dashboard-execucao-despesa/` (2)

| Verbo | Caminho | Método Java |
|---|---|---|
| ANY | `/v2/dashboard-execucao-despesa/listar` | `buscarValoresDashboardExecucaoDespesa` |
| ANY | `/v2/dashboard-execucao-despesa/listar-anos` | `buscarAnosDashboardExecucaoDespesa` |

**DespesasRAsControllers** — base `/v2/despesas-ras` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/despesas-ras` | `?` |

**PaineisDespesaController** — base `v2/paineis-despesa` (4)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/paineis-despesa` | `recuperarValoresPaineisDespesa` |
| GET | `/v2/paineis-despesa/temas` | `recuperarTemas` |
| GET | `/v2/paineis-despesa/temas-anos` | `recuperarTemasAnos` |
| ANY | `/v2/paineis-despesa/listar-anos` | `buscarAnosPaineisDespesa` |

**ImagensController** — base `v2/imagens/` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| ANY | `/v2/imagens/imagens-slideshow` | `listarUrlImagensSlideshow` |

**ItensLicitadosController** — base `/v2/itens-licitados` (6)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/itens-licitados` | `listarItensLicitados` |
| GET | `/v2/itens-licitados/anos` | `listarAnosItensLicitados` |
| GET | `/v2/itens-licitados/{idItemCompra}` | `detalharItemLicitado` |
| GET | `/v2/itens-licitados/orgaos` | `listarOrgaos` |
| GET | `/v2/itens-licitados/ufs` | `listarUfs` |
| GET | `/v2/itens-licitados/modalidades` | `listarModalidades` |

**ItensLicitadosRelatorioController** — base `/v2/itens-licitados/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/itens-licitados/relatorios` | `exportarItensLicitados` |

**LicitacoesController** — base `/v2/licitacoes` (6)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/licitacoes` | `listarLicitacoes` |
| GET | `/v2/licitacoes/anos` | `listarAnosLicitacoes` |
| GET | `/v2/licitacoes/orgaos` | `listarOrgaosLicitacoes` |
| GET | `/v2/licitacoes/tipos` | `listarLicitacoesTipos` |
| GET | `/v2/licitacoes/fornecedores-por-pregao` | `listarFornecedoresPorPregao` |
| GET | `/v2/licitacoes/situacoes` | `listarSituacoes` |

**LicitacoesRelatorioController** — base `/v2/licitacoes/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/licitacoes/relatorios` | `exportarLicitacoes` |

**BensImoveisController** — base `/v2/bens-imoveis` (8)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/bens-imoveis` | `listar` |
| GET | `/v2/bens-imoveis/{tombamento}` | `detalhar` |
| GET | `/v2/bens-imoveis/{tombamento}/terrenos` | `detalharTerreno` |
| GET | `/v2/bens-imoveis/{tombamento}/edificacoes` | `detalharEdificacao` |
| GET | `/v2/bens-imoveis/{tombamento}/obras` | `detalharObras` |
| GET | `/v2/bens-imoveis/regioes-administrativas` | `listarRegioesAdministrativas` |
| GET | `/v2/bens-imoveis/orgaos` | `listarOrgaos` |
| GET | `/v2/bens-imoveis/situacoes` | `listarSituacoes` |

**BensImoveisRelatorioController** — base `/v2/bens-imoveis/relatorios` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/bens-imoveis/relatorios` | `relatorioBensImoveis` |

**BensMoveisController** — base `/v2/patrimonio/bens-moveis` (4)

| Verbo | Caminho | Método Java |
|---|---|---|
| GET | `/v2/patrimonio/bens-moveis` | `listarBensMoveis` |
| GET | `/v2/patrimonio/bens-moveis/tipos` | `listarTiposBensMóveis` |
| GET | `/v2/patrimonio/bens-moveis/orgaos` | `listarOrgaosBensMoveis` |
| GET | `/v2/patrimonio/bens-moveis/estados` | `listarEstadosBensMoveis` |

**PesquisaSatisfacaoController** — base `v2/pesquisa-satisfacao/` (1)

| Verbo | Caminho | Método Java |
|---|---|---|
| POST | `/v2/pesquisa-satisfacao` | `salvar` |

## Inferências e limitações
- 🔶 Caminhos de classes sem `/` inicial (`servidor/militares-cedidos`, `v2/...`) são resolvidos pelo Spring como se tivessem `/`; aqui foram normalizados.
- 🔶 Métodos marcados `?` não tiveram o nome extraído (nenhum caso nesta extração é relevante; ver controller).
- ❓ Parâmetros, corpos e respostas por rota não foram levantados; o frontend (não identificado) é quem define o contrato efetivo.
- ❓ A extração é textual: rotas geradas por Spring Data REST (`starter-data-rest`) para os 3 repositórios JPA não aparecem aqui e não foram verificadas.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]] · [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]]

## Pendências e próximo passo
- Detalhar parâmetros e respostas por rota. A navegação por área funcional está nas notas de módulo (ver [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]]).
