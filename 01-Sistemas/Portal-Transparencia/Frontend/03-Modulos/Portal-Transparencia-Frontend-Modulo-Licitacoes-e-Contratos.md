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
  - licitacoes
  - contratos
sources:
  - src/app/index.route.js
  - src/app/components/licitacoes-contratos
---

# Frontend — módulo Licitações e Contratos

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Consulta pública de licitações (pregões), fornecedores, itens licitados e contratos.

## Evidências
Commit `dca3e933`. `index.route.js`; `components/licitacoes-contratos/**` (7 JS, 12 HTML); `licitacoes-contratos.service.js` (26 chamadas) e `licitacoes/licitacoes.service.js` (7 chamadas).

## Informações confirmadas
| Caminho | Controller | Rótulo |
|---|---|---|
| `/licitacoes-contratos/dashboard` | `LicitacoesContratosDashboardController` | Painel |
| `/licitacoes-contratos/contratos` | `ContratosController` | Contratos |
| `/licitacoes-contratos/licitacoes` | `LicitacoesController` | Licitações |
| `/licitacoes-contratos/licitacoes/fornecedores` | `FornecedoresController` | Fornecedores |
| `/licitacoes-contratos/itens-licitados` | `ItensLicitadosController` | Itens licitados |

- ✅ Duas gerações de API: `/licitacoes-contratos/*` (contratos, propostas, vencedores, aditivos, gráficos) e `/v2/licitacoes/*`, `/v2/itens-licitados/*` (pregões, fornecedores por pregão, itens por fornecedor, participantes).
- ✅ Exportação: `/licitacoes-contratos/relatorio/contrato`, `/v2/itens-licitados/relatorios`, `/v2/licitacoes/relatorios`.
- ✅ A tela de fornecedores recupera parâmetros guardados por `ScopeService.getStored()` (estado temporário entre telas).
- ✅ Sem testes automatizados neste módulo.

## Inferências e limitações
- ✅ Chamadas sem rota no Backend (busca textual): `/licitacoes-contratos/anos`, `/licitacao/orgao`, `/licitacao/situacao`, `/grafico/{especie,objeto,situacao,orgaos-contratos}`. Podem estar ligadas a gráficos do painel ou a código remanescente (uso não verificado).
- 🔶 Regras de situação/modalidade são do Backend: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Licitacoes-e-Contratos|Licitações e Contratos]].

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]] · [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
