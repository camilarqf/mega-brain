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
  - convenios
sources:
  - src/main/java/br/gov/df/transparencia/api/convenio
  - src/main/java/br/gov/df/transparencia/servico/convenio
  - src/main/java/br/gov/df/transparencia/modelo/convenio
  - src/main/resources/sql/convenio
---
# Módulo Convênios

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Rotas: [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (seção Convênios)

## Objetivo
Documentar a consulta de convênios de receita (transferências recebidas), de despesa (repasses) e de entidades beneficiadas.

## Evidências
Leitura da lista de métodos de `ConvenioService` (243 linhas) e `ConvenioRelatorioService`, dos controllers e das tabelas dos 23 SQL.

## Informações confirmadas
- ✅ `ConvenioController` (`/convenio`, 18 rotas) e `ConvenioRelatorioController` (`/convenio/relatorio`, 4).
- ✅ Três visões: **receita** (`Convenio.Transferencia_Recebida`), **despesa** (`Convenio.Repasse`) e **entidades beneficiadas**, com listas de espécie, concedente e anos, execução de receita/despesa, extrato do convênio e detalhamento do valor pago à entidade beneficiada (junção com `Despesa.TF_PAGAMENTO_EMPENHO`, `TF_NOTA_EMPENHO`, `TD_CREDOR`, `TD_UG`, `TD_GESTAO` e demais dimensões de despesa).
- ✅ Relatórios: receita, despesa, entidades beneficiadas e detalhamento (templates `convenio/templateDetalhamentoEntidadesBeneficiadas.vm`).
- ✅ **Mascaramento**: `pesquisarReceita` (`CONVENIOS_RECEITA`, campo `GESTOR`), `pesquisarDespesa` (`CONVENIOS_DESPESA`, `GESTOR`) e `listarDetalhamentoEntidadesBeneficiadas` (`ENTIDADES_BENEFICIADAS`, `DIRIGENTE`); ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]].
- ✅ Modelo: `Convenio`, `EntidadeBeneficiada`, `DetalhamentoEntidadeBeneficiada`; 🔶 `recuperarRelatoriosConvenio` provavelmente lê documentos do catálogo `Servidor.Relatorio` (categoria `CONVENIOS`; tabela citada em 1 SQL de convênio; ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Documentos publicados]]).

## Inferências e limitações
- ❓ Regras de cálculo (valores repassados × pagos) e filtros fixos nos `.vm` não lidos.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

## Pendências e próximo passo
- Ler `convenio/*.vm` e `ConvenioService`.
