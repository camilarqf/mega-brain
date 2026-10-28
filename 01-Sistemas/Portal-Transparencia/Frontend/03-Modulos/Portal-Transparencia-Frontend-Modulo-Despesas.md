---
type: module
aliases:
  - "Frontend — módulo Despesas"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
sources:
  - src/app/index.route.js
  - src/app/components/despesas
  - src/app/components/dashboard-execucao-despesas
  - src/app/components/compartilhado/directives/despesas-ras
---

# Frontend — módulo Despesas

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Telas públicas de consulta de despesas do GDF: painel, consulta dinâmica, detalhamentos, notas de empenho/lançamento, ordens bancárias, emendas parlamentares, diárias e passagens, execução OCA e despesas relacionadas à COVID-19.

## Evidências
Commit `dca3e933`. Rotas em `index.route.js`; `components/despesas/**` (30 arquivos JS, 61 HTML); `despesas.service.js` (87 chamadas); `components/dashboard-execucao-despesas`; mapa de regiões em `compartilhado/directives/despesas-ras`.

## Informações confirmadas
**Rotas (26).**
| Caminho | Controller | Rótulo |
|---|---|---|
| `/despesas/dashboard` | `DespesasDashboardController` | Painel |
| `/despesas/consulta-dinamica` | `DespesaConsultaDinamicaController` | Consulta Dinâmica |
| `/despesas/por-funcao` | `PorFuncaoDespesaController` | Gráfico por Função |
| `/despesas/detalhamento` · `/despesas/detalhamentos/saiba-mais` | `DetalhamentoDespesaCtrl` · `DespesasDetalhamentosSaibaMaisController` | Detalhamento da Despesa |
| `/despesas/pagamentos-por-credor` · `…-detalhamento` | `PagamentosPorCredorCtrl` · `PagamentosPorCredorDetalhamentoCtrl` | Pagamentos |
| `/despesas/nota-empenho` · `/nota-lancamento` · `/ordem-bancaria` | `NotaEmpenhoController` · `NotaLancamentoController` · `OrdemBancariaController` | Documentos da execução |
| `/despesas/emendas-parlamentares` e variantes `…/nota-empenho/…`, `…/nota-lancamento/…`, `…/ordem-bancaria/…` | `EmendasParlamentares*Controller` | Emendas Parlamentares (5 rotas) |
| `/despesas/emenda-parlamentar-federal` | `EmendasParlamentaresFederaisController` | Emendas federais |
| `/despesas/diarias-passagens-locomocao`, `/despesa/diarias-passagens/{nota-empenho,nota-lancamento,ordem-bancaria}`, `/despesas/diarias-passagens/saiba-mais` | `DiariasPassagens*Controller` | Locomoção (5 rotas) |
| `/despesas/execucao-oca` | `ExecucaoOcaController` | Execução OCA |
| `/despesas/despesas-covid19-por-item` | `DespesasCovid19PorItemController` | — |
| `/despesas/saiba-mais`, `/despesas/saiba-mais-obras` | `DespesasSaibaMaisController` | Saiba mais |
| `/despesas/:tipo` · `/despesas/:tipo/:categoria/:codigo` | `DespesasPorAgrupadorController` · `DespesaValoresController` | Despesas agrupadas por tipo e valores por categoria |

Rotas comentadas (controllers ainda no repositório): `/despesas/restos-a-pagar`, `/despesas/execucao-emendas`, `/despesas/acao`.

**Serviço e dados.** `DespesasService` (`despesas.service.js`) concentra 87 chamadas `GET`/`POST` (famílias em [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo]]). Tabelas usam `tabela-consulta` (URL no HTML) e `PagingService`. A tela de execução de despesa usa `ExecucaoDespesaService` (`/v2/dashboard-execucao-despesa/*`) e o mapa de regiões administrativas (`/v2/despesas-ras`, `delimitacao_ras.json`, `localizacoes_ras.json`).

**Exportação.** Cerca de 25 controllers chamam `RelatorioService.exportar('/despesa/relatorio/…')` (PDF ou CSV).

**Testes.** 5 `*.spec.js` (consulta dinâmica, nota de empenho, nota de lançamento, ordem bancária, despesas por agrupador).

## Inferências e limitações
- 🔶 Os cálculos e a semântica dos valores (empenhado, liquidado, pago, covid, OCA) são do Backend: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Módulo Despesa do Backend]] e [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Despesa-Consultas-e-Calculos|Consultas e cálculos]]. O frontend não aplica regra de negócio verificável além de filtros e formatação.
- ✅ Chamada sem rota no Backend: `/despesa/porAcao/empenhado/{codigo}` (usada em `despesas.service.js`).
- ❓ Telas de ação (`despesas-por-acao`) e restos a pagar estão fora de rotas ativas; comportamento não analisado.
- Cobertura parcial: templates, SCSS e a lógica interna de cada controller foram lidos por amostragem.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API]] · [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Arquitetura-AngularJS|Arquitetura]]
- Backend: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Módulo Despesa]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
