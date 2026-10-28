---
type: module
aliases:
  - "Frontend — módulo Convênios"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
sources:
  - src/app/index.route.js
  - src/app/components/convenio
---

# Frontend — módulo Convênios

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Consulta de convênios de receita e de despesa, entidades beneficiadas e relatórios.

## Evidências
Commit `dca3e933`. `index.route.js`; `components/convenio/**` (5 JS, 18 HTML); `convenio.service.js` (13 chamadas).

## Informações confirmadas
| Caminho | Controller | Rótulo |
|---|---|---|
| `/convenio/receita` | `ConvenioReceitaController` | Convênios de receita |
| `/convenio/despesa` | `ConvenioDespesaController` | Convênios de despesa |
| `/convenio/entidades-beneficiadas` | `ConvenioEntidadesBeneficiadasController` | Entidades beneficiadas |
| `/convenio/entidades-beneficiadas/valor-pago` | `OrdemBancariaController` (reutilizado do módulo Despesas) | Pagamentos – entidade beneficiada |
| `/convenio/relatorio` | `ConvenioRelatorioController` | Relatórios |

- ✅ `ConvenioService`: `/convenio/{receita,despesa}/{anos,concedente,especie,execucao}`, `/convenio/despesa/extrato-convenio`, `/convenio/entidade(s)-beneficiada(s)/*`.
- ✅ Exportação: `/convenio/relatorio/{despesa,receita,entidades-beneficiadas}` e detalhe de entidade; o caminho de entidades beneficiadas é montado com barra dupla (`…/relatorio//entidades-beneficiadas`).
- ✅ Sem testes automatizados neste módulo.

## Inferências e limitações
- 🔶 Regras de execução de convênios: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Convenios|Backend: Convênios]].

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Despesas|Módulo Despesas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
