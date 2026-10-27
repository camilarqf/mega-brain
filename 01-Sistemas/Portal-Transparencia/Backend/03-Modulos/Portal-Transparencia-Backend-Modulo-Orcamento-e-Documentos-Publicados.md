---
type: module
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
tags:
  - portal-transparencia
  - backend
  - modulo
  - orcamento
  - documentos
sources:
  - src/main/java/br/gov/df/transparencia/api/orcamento
  - src/main/java/br/gov/df/transparencia/servico/orcamento/OrcamentoService.java
  - src/main/java/br/gov/df/transparencia/servico/receita/RelatorioService.java
  - src/main/java/br/gov/df/transparencia/modelo/ServidorRelatorio.java
  - src/main/resources/sql/orcamento
  - src/main/resources/sql/relatorio
---
# Módulo Orçamento e documentos publicados

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seção Orçamento)

## Objetivo
Documentar o **catálogo de documentos publicados** (PDFs e links por categoria, ano e data de referência) e as consultas de orçamento (PPA, LDO, LOA, Lei de Responsabilidade Fiscal e relatórios gerenciais), que são servidas por ele. O mesmo catálogo é usado por outras áreas.

## Evidências
Leitura de `OrcamentoService` (lista de métodos e trechos), `RelatorioController` (orçamento), `RelatorioService` (receita), `ServidorRelatorio` (campos e enum de categorias), `listCategoriasDeRelatoriosPorTipo.vm` e `listDataReferenciaPorCategoria.vm`; análise de tabelas de 14 SQL de orçamento.

## Informações confirmadas
- ✅ **Catálogo**: tabelas `Servidor.Relatorio` (documentos) e `Servidor.CategoriaRelatorio` (categorias). O modelo `ServidorRelatorio` mapeia `ID_ARQUIVO`, `NM_ARQUIVO`, `DS_ARQUIVO`, `TX_URL_ARQUIVO` (URL do arquivo), `NR_ANO`, `CD_CATEGORIA`, `DT_REFERENCIA` (texto), `NM_ORIGEM_ARQUIVO`, `TX_ASSUNTO`, `DT_CARGA` e `TP_RELATORIO`. A API entrega **metadados e URL**; o arquivo em si não passa por este backend (exceto `/download/arquivos/{nome}`).
- ✅ **Categorias** (enum `ServidorRelatorio.CategoriaRelatorioEnum`, com ids fixos no código): PPA 1, LDO 2, LOA 3, convênios 4, outros de prestação de contas 7, avaliação de resultados 8, tabelas de remuneração 9, quadro de servidores do GDF 10, relatórios gerenciais 11, gastos com publicidade 13, Lei de Responsabilidade Fiscal 14, legislação de beneficiários de programas sociais 15, balanço geral 16, desempenho físico-financeiro por programa de trabalho 17, execução orçamentária 18, prestação de contas anual 19, gestão fiscal 19, gestão orçamentária 20, prestação de contas 21, investimentos 23, desempenho 24, patrimônio 27, creche/PAC 28, cartão material escolar 38, remuneração "saiba mais" 43, diárias e passagens "saiba mais" 44, organizações sociais de saúde 48, ações emergenciais 64, artístico-cultural 66, mobilidade cidadã 67, obras e instalações 68 e despesas 65. Há **ids duplicados** por apelido (ex.: `PRESTACAO_CONTAS_ANUAL` e `GESTAO_FISCAL` = 19; `GESTAO_ORCAMENTARIA` e `RELATORIO_INVESTIMENTO_DISPENDIO_ESTATAIS` = 20; `AVALIACAO_RESULTADOS_EFICIENCIA_EFICACIA` e `AVALIACAO_RESULTADOS` = 8).
- ✅ **Grupos por tipo** (`getIdCategoriaPorTipo`, usado por `POST /orcamento/categorias`): `relatorios-gerenciais` (prestação de contas, execução orçamentária, investimentos, desempenho, avaliação de resultados, balanço geral), `responsabilidade-fiscal` (gestão fiscal e gestão orçamentária), `prestando-contas-outros-relatorios` (id 7) e `organizacoes-sociais-saude`.
- ✅ **Rotas de orçamento** (`/orcamento`, 14): `ldo`, `loa`, `ppa`, `responsabilidade-fiscal`, `relatorios-gerenciais`, anos de relatórios gerenciais, LDO, LOA e LRF, assuntos de LRF e de relatórios gerenciais, `listarDataReferenciaPorAssunto`, `POST categorias` e `POST data-referencias`; mais `/relatorio/loa|ldo|relatorios-gerenciais/ultimo-ano` (3) com `RelatorioService.ultimoAnoDisponivel(categoria)`.
- ✅ Os filtros fixam a categoria no serviço (ex.: `pesquisarLoa` seta `ORCAMENTO_LOA`), então as rotas LDO/LOA/PPA/LRF são o mesmo catálogo com categoria diferente.
- ✅ Outras áreas que leem o mesmo catálogo: remuneração (tabelas, quadro, "saiba mais"), servidores (relatórios e pendências), patrimônio (demonstrativos), prestação de contas (legislação, publicidade, outros relatórios), diárias e passagens ("saiba mais") e convênios.

## Inferências e limitações
- ✅ **Risco confirmado no fluxo**: `POST /orcamento/data-referencias` coloca o corpo bruto em `rel.CD_CATEGORIA in ( $codigos )` sem validação (ver [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]). `POST /orcamento/categorias` usa um `switch` sobre `tipo`; com corpo vazio (`required=false`) o `switch` sobre `null` lança `NullPointerException` (→ 500).
- 🔶 `DT_REFERENCIA` é texto; a ordenação `order by DT_REFERENCIA desc` pode não seguir a ordem cronológica.
- 🔶 Os ids são números mágicos acoplados à carga do banco; alterar a tabela de categorias exige mudar o código.
- ❓ Quem publica os arquivos e carrega `Servidor.Relatorio` (e onde ficam as URLs) não está neste repositório.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Servidores-e-Remuneracao|Servidores e Remuneração]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Patrimonio|Patrimônio]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Prestacao-de-Contas|Prestação de Contas]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Convenios|Convênios]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

## Pendências e próximo passo
- Confirmar o processo de carga de `Servidor.Relatorio` e se os ids duplicados são intencionais.
