---
type: module
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
tags:
  - portal-transparencia
  - frontend
  - modulo
  - receitas
sources:
  - src/app/index.route.js
  - src/app/components/receitas
  - src/app/components/compartilhado/services/imposto.service.js
---

# Frontend — módulo Receitas

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Consulta pública de receitas do GDF e de transferências da União.

## Evidências
Commit `dca3e933`. Rotas em `index.route.js`; `components/receitas/**` (8 JS, 13 HTML); `receitas.service.js` (30 chamadas); `ImpostoService` (`/receita/grafico/arrecadacao-imposto`).

## Informações confirmadas
| Caminho | Controller | Rótulo |
|---|---|---|
| `/receitas/dashboard` | `ReceitaDashboardController` | Painel |
| `/receitas/impostos` | `ImpostosController` | — |
| `/receitas/consulta-dinamica` | `ReceitaConsultaDinamicaController` | Consulta Dinâmica |
| `/receitas/multas-transito` | `MultasTransitoController` | Multas de trânsito |
| `/receitas/por-orgao` | `ReceitaController` | Receitas por órgão |
| `/receitas/receita-covid19-auxilio-uniao` | `ReceitaAuxilioUniaoController` | Receita – Auxílio União |
| `/receita-uniao/transferencia` | `ReceitaControllerUniao` | Transferências da União |

- ✅ `ReceitasService` consulta `/receita/*` (anos, gestão, unidade gestora, categoria, fonte, subfonte, rubrica, alínea, subalínea, `grafico/*`, `multas`, `por-orgao`) e `/receita-uniao/*`.
- ✅ Teste: `receitas.controller.spec.js`.
- ✅ Exportação PDF/CSV via `RelatorioService.exportar` em 5 controllers: `/receita/relatorio/{consulta-dinamica,multas,fonte-recurso,por-orgao,uniao}`.

## Inferências e limitações
- ✅ Chamada sem rota no Backend: `GET /receita/multas/total`.
- 🔶 Semântica das receitas e dos gráficos de impostos está no Backend: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Receita|Módulo Receita]].
- Cobertura parcial (templates e lógica de gráficos lidos por amostragem).

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Receita|Backend: Receita]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
