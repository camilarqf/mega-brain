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
  - orcamento
sources:
  - src/app/index.route.js
  - src/app/components/orcamento
  - src/app/components/planejamento-orcamento
---

# Frontend — módulo Orçamento e Planejamento

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Publicação de documentos orçamentários (PPA, LDO, LOA, LRF e relatórios gerenciais).

## Evidências
Commit `dca3e933`. `index.route.js`; `components/orcamento/**` (3 JS, 4 HTML); `components/planejamento-orcamento/` (apenas 1 HTML); `orcamento.service.js` (10 chamadas).

## Informações confirmadas
| Caminho | Controller | Rótulo |
|---|---|---|
| `/orcamento/ppa` | `PpaController` | Plano Plurianual – PPA |
| `/orcamento/:tipo` | `OrcamentoController` | `{{tipo}}` (rota parametrizada: `ldo`, `loa`, `lrf`, `relatorios-gerenciais` … conforme anos/assuntos devolvidos) |

- ✅ `OrcamentoService`: `GET /orcamento/{relatorios-gerenciais,ldo,loa,lrf}/anos`, `GET /orcamento/assuntosLRF`, `/assuntosRelatoriosGerenciais`, `/orcamento/{tipo}`, `/orcamento/listarDataReferenciaPorAssunto`; `POST /orcamento/categorias` e `/orcamento/data-referencias`.
- ✅ `OrcamentoController` usa `ArquivoUrlService.ARQUIVOS` (`vm.urlArquivos`) para montar os links dos documentos (ver [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas|Integrações externas]]).
- ✅ Sem testes automatizados neste módulo.

## Inferências e limitações
- 🔶 `planejamento-orcamento` contém só um HTML e não tem rota própria identificada.
- Valores aceitos em `:tipo` não foram enumerados a partir do código (depende dos dados).

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Backend: Orçamento e documentos publicados]] · [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
