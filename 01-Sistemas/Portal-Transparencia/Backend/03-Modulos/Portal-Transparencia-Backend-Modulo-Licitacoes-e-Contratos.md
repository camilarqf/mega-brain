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
  - licitacoes
  - contratos
sources:
  - src/main/java/br/gov/df/transparencia/api/licitacoesContratos
  - src/main/java/br/gov/df/transparencia/api/v2/licitacoesContratos
  - src/main/java/br/gov/df/transparencia/servico/licitacoesContratos
  - src/main/java/br/gov/df/transparencia/modelo/licitacoesContratos
  - src/main/java/br/gov/df/transparencia/dto/licitacoesContratos
  - src/main/resources/sql/licitacoes-contratos
---
# Módulo Licitações e Contratos

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/05-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seções Licitações e contratos v1 e API v2)

## Objetivo
Documentar a consulta de contratos (v1), licitações e itens licitados (v2).

## Evidências
Leitura da lista de métodos dos 6 serviços e dos controllers; análise de tabelas dos 37 `.sql/.vm`. O commit mais recente do repositório (`9434e58f`) é o merge da `feature/novoFiltroLicitacao`, cujo nome sugere relação com esta área; o diff **não** foi lido.

## Informações confirmadas
| Versão | Controller (rotas) | Serviço |
|---|---|---|
| v1 | `LicitacoesContratosController` (`/licitacoes-contratos`, 14), `LicitacoesContratosRelatorioController` (1) | `LicitacoesContratosService` (contratos, propostas, processo por órgão, vencedor, aditivos, extrato de nota de empenho, gráfico de evolução por modalidade) |
| v2 licitações | `LicitacoesController` (`/v2/licitacoes`, 6), `LicitacoesRelatorioController` (1) | `LicitacoesService` (listagem, anos, órgãos, tipos, situações, fornecedores por pregão) |
| v2 itens licitados | `ItensLicitadosController` (`/v2/itens-licitados`, 6), `ItensLicitadosRelatorioController` (1) | `ItensLicitadosService` (listagem, detalhe, órgãos, UFs, modalidades) |

- ✅ Tabelas: schema `Compras` (`TF_ITEM_COMPRA`, `Principal`, `TD_FORNECEDOR`, `TD_UNIDADE`, `TD_ITEM_COMPRA`, `TD_UNIDADE_FORNECIMENTO`, `TD_MODALIDADE_LICITACAO`, `TD_MATERIAL_SERVICO`, `TD_SITUACAO_COMPRA`, `TD_TIPO_MATERIAL_SERVICO`, `TD_OBJETO_COMPRA`, `ProcessoOrgao`, `Proposta`), schema `Contrato` (`Principal`, `Especie`, `Aditivo`) e, para ligação com a despesa, `Despesa.TF_NOTA_EMPENHO`, `TD_TIPO_LICITACAO`, `TD_EVENTO`, `TD_PROGRAMA_TRABALHO`, `TD_FONTE_RECURSO`, `TD_FUNCAO`, `TD_SUBITEM`, `TD_ELEMENTO`.
- ✅ Modelo (`modelo/licitacoesContratos`, 8 classes): `Licitacao`, `Contrato`, `Aditivo`, `ItemLicitado`, `Proposta`, `Vencedor`, `FornecedorPregao`, `ProcessoOrgao`; DTOs `FornecedorDTO` e `ItemLicitadoDetalhamentoDTO`.
- ✅ **Mascaramento**: só `pesquisarContratos` (`CONTRATOS`, campo `NOME`). As rotas v2 (licitações e itens licitados) **não** usam `@Mascaravel`.
- ✅ O v2 é a versão nova: convive com o v1; o frontend (não identificado) define qual usa.
- ✅ Datas de atualização para painel, contratos, licitações e itens licitados em `DataAtualizacaoController`.

## Inferências e limitações
- 🔶 Os filtros novos da última feature (`novoFiltroLicitacao`) podem estar em `LicitacoesService`/`.vm` de v2; não identificados.
- ❓ Regras de modalidade, situação e cálculo de valores estão nos `.vm`, não lidos.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]] (extrato de nota de empenho) · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]]

## Pendências e próximo passo
- Ler o diff da `feature/novoFiltroLicitacao` e os `.vm` de `licitacoes-contratos` para documentar filtros e regras.
