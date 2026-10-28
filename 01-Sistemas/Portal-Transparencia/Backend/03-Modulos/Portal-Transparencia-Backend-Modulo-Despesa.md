---
type: module
aliases:
  - "Módulo Despesa"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
sources:
  - src/main/java/br/gov/df/transparencia/api/despesa
  - src/main/java/br/gov/df/transparencia/api/v2/despesa
  - src/main/java/br/gov/df/transparencia/servico/despesa
  - src/main/java/br/gov/df/transparencia/modelo/despesa
  - src/main/resources/sql/despesa
---
# Módulo Despesa

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seção Despesa e API v2)

## Objetivo
Documentar a maior área do portal: consulta pública da execução da despesa do GDF (empenho, liquidação, pagamento), com detalhamentos, emendas, diárias e passagens, restos a pagar, gráficos, painéis e relatórios.

## Evidências
Leitura de `servico/despesa/*` (11 classes, ~2,8 mil linhas; `DespesaService` com 1.351), de trechos de `consultaDinamica`/`pesquisarNotaEmpenho`/`RestosAPagarService`, dos controllers e do levantamento automático de métodos, anotações e tabelas dos 149 arquivos de `resources/sql/despesa`. Regras só foram lidas onde indicado; o conteúdo dos `.vm` não foi lido linha a linha.

## Informações confirmadas
### Estrutura
| Parte | Controllers (rotas) | Serviço | SQL |
|---|---|---|---|
| Consulta e detalhe de empenho, nota de lançamento (NL), ordem bancária (OB) | `DespesaController` (48), `DetalhamentoController` (6) | `DespesaService` | `listDespesa*.vm`, `pesquisaAgrupada/` (33), `listQddUgGestao*.vm` |
| Gráficos | `DespesaGraficoController` (11) | `DespesaGraficosService` | `graficos/` (8) |
| Relatórios PDF/CSV | `DespesaRelatorioController` (27) | `DespesaRelatorioService` (≈27 relatórios) | templates em `resources/relatorios/despesa` |
| Diárias e passagens | `DiariasPassagensController` (19) | `DiariasPassagensService` | `diariasPassagens/` (23) |
| Emendas parlamentares (distritais) | `EmendasParlamentaresController` (17), `ExecucaoEmendasController` (2) | `EmendasParlamentaresService` | `emendas-parlamentares/` (11) |
| Emendas parlamentares federais | `EmendaParlamentarFederalController` (3) | `EmendaParlamentarFederalService` | `emendas-parlamentares-federais/` (6) |
| Execução OCA | `ExecucaoOcaController` (5) | `ExecucaoOCAService` | `execucao-oca/` (2) |
| Restos a pagar | `RestosAPagarController` (3) | `RestosAPagarService` | `restosAPagar/` (3) |
| v2: dashboard, painéis, RAs | `DashboardExecucaoDasDepesasController` (2), `PaineisDespesaController` (4), `DespesasRAsControllers` (1) em `/v2/...` | `DashboardExecucaoDespesaService`, `PaineisDespesaService`, `DespesaRAsService` | `execucao-despesa/`, `paineis-despesa/`, `listDespesasRAs.sql` |

### Dados
- ✅ Tabelas mais usadas (schema `Despesa`): `TF_NOTA_EMPENHO` (84 referências), `TD_UG`, `TD_GESTAO`, `TD_FUNCAO`, `TD_CREDOR`, `TD_FONTE_RECURSO`, `TD_SUBFUNCAO`, `TD_TIPO_LICITACAO`, `TD_PROGRAMA`, `TD_ELEMENTO`, `TD_ACAO`, `TD_GRUPO_DESPESA`, `TF_NOTA_EMPENHO_SUBITEM`, `TD_PROGRAMA_TRABALHO`, `TD_MODALIDADE_APLICACAO`, `TD_ESFERA`, `TD_SUBTITULO`, `QDD_UG_GESTAO`, `TF_NOTA_LANCAMENTO`, `TF_PAGAMENTO_EMPENHO`, `TF_NOTA_LANCAMENTO_X_NOTA_EMPENHO`, `EMENDA_PARLAMENTAR`, `TF_ORDEM_BANCARIA`, `TF_ORDEM_BANCARIA_X_NOTA_EMPENHO`, `TD_SUBITEM`. Há ainda os schemas `Emendas_Fundo_Fundo` e `Emendas_Pix` para emendas.
- ✅ Modelo (28 classes em `modelo/despesa`): `NotaEmpenho`, `NotaLancamento`, `NotaFiscal`, `OrdemBancaria`, `OrdemCancelamento`, `RestoAPagar`, `DiariasPassagens`, `EmendaParlamentar*`, `PagamentoCredor*`, `DespesaConsultaDinamica`, `DespesaCovidPorItem`. Uma entidade JPA: `NotaLancamentoEvento` (`Despesa.TF_NOTA_LANCAMENTO_EVENTO`, repositório Spring Data).
- ✅ Cadeia navegável: nota de empenho (NE) → notas de lançamento (NL) e ordens bancárias (OB); métodos como `listarNotaLancamentoPorNeOriginal`, `listarOrdemBancariaPorNeOriginal`, `listarNotaEmpenhoPorOrdermBancaria`, `listarNotasLancamentoPorOrdemBancaria`, `listarOrdemCancelamentoPorOB`, `listarEventosNotaLancamento`, `listarNotaFiscalEmpenho`.

### Regras de negócio verificadas no código (`DespesaService`)
- ✅ **Consulta dinâmica** (`consultaDinamica`/`consultaDinamicaConsumer`): rejeita períodos em que `dataInicio` ou `dataFim` seja anterior a **01/01/2009** (a consulta não é executada).
- ✅ Quando `dataInicio` e `dataFim` vêm juntos, o `anoExercicio` é **anulado** e o período é decomposto em mês/ano inicial e final; `dataFim` é ajustada para o **último dia do mês**.
- ✅ Filtros booleanos que mudam a consulta: `ressarcimento`, `consultaCovid`, `consultaCovidAuxUni` (auxílio da União, covid), `consultaExerciciosAnteriores`, `consultaObrasInstalacoes`.
- ✅ **Credor**: o código pode chegar codificado em Base64 (`codigoCredorCodificado`), sobrepondo o código em texto; os separadores `.`, `-` e `/` são removidos antes da consulta; o nome do credor passa por tratamento de texto/máscara (`tratarStringRecebida`/`tratarStringMascaradaRecebida`).
- ✅ **Mascaramento**: 12 métodos de `DespesaService`, mais diárias/passagens (1) e emendas (3), usam `@Mascaravel(DESPESA)`, que remove registros cujo credor/código do credor esteja em medida protetiva (ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]]).
- ✅ **Cache** de listas de filtros por exercício (`listFiltros`, `listFiltrosCovid`, `listFiltrosCovidAuxUni`; chave `método:exercício`; 200 entradas, 1 dia; limpo por `/cache-expire/despesa-filtros`).
- ✅ Integração com outros sistemas: `recuperarNotaEmpenhoIntegracao` e `listarOrdemBancariaIntegracao` alimentam `/integracao/nota-empenho` e `/integracao/listar-nl-ob` ([[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]]).
- ✅ Relatórios: `DespesaRelatorioService` gera por consulta dinâmica, exercícios anteriores, obras e instalações, ressarcimento de requisitados, por ação/credor/órgão/suprimento, empenho, NL, OB (inclusive de emendas e por credor), detalhamento, emendas (distritais e federais), execução de emendas e de OCA, diárias e passagens e três relatórios Covid; ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]].
- ✅ Gráficos: evolução anual, por função, grupo e tipo de despesa, correntes × capital, evolução receita × despesa, por grupo e por função, treemap por função/subfunção.
- ✅ `RestosAPagarService`: filtros `exercicio`, `nomeCredor`, `codigoCredor`, `tipoResto`, `numeroProcesso`, entre outros.

## Inferências e limitações
- 🔶 **Defeito provável**: se o período da consulta dinâmica for inválido, `consultaDinamica` faz `(Page) Collections.emptyList()`; uma `List` vazia não é `Page`, então deve lançar `ClassCastException` (→ resposta 500) em vez de página vazia. Não testado.
- 🔶 O parâmetro `nomeCredor` e outros textos são interpolados nos `.vm`; ver risco de injeção de SQL em [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]].
- ❓ Significado de **OCA**, de "QDD" e das regras de cálculo dos totalizadores (`executarComTotalizador*`) não está no código lido; as siglas aparecem nos nomes (QDD = quadro de detalhamento de despesa é interpretação).
- ❓ Cálculos dentro dos `.vm` (joins, filtros fixos, ressarcimento, covid) não foram lidos.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Despesa-Consultas-e-Calculos|Despesa: consultas e cálculos]] · [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão de injeção de SQL]]
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Receita|Receita]] (gráficos receita × despesa) · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Convenios|Convênios]] (usa tabelas de despesa) · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Apoio-e-Atualizacao-de-Dados|Apoio-e-Atualizacao-de-Dados]] (datas de atualização) · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

## Pendências e próximo passo
- Cálculos e filtros dos templates principais: ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Despesa-Consultas-e-Calculos|Despesa: consultas e cálculos]]. Falta ler os `.vm` de diárias e passagens, emendas, QDD por UG e execução OCA; confirmar o defeito do `ClassCastException`.
