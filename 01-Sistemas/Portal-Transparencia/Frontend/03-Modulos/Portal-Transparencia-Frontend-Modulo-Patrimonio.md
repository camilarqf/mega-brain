---
type: module
aliases:
  - "Frontend — módulo Patrimônio"
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
sources:
  - src/app/index.route.js
  - src/app/components/patrimonio
---

# Frontend — módulo Patrimônio

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Consulta de bens móveis, bens imóveis, localização por órgão e demonstrativos patrimoniais.

## Evidências
Commit `dca3e933`. `index.route.js`; `components/patrimonio/**` (8 JS, 14 HTML); `patrimonio.service.js` (9), `bens-imoveis/bens-imoveis.service.js` (7), `bens-moveis/bens-moveis.service.js` (3).

## Informações confirmadas
| Caminho | Controller | Rótulo |
|---|---|---|
| `/patrimonio/bens-moveis` | `BensMoveisController` | Bens móveis |
| `/patrimonio/bens-imoveis` | `PatrimonioBensImoveisController` | Bens imóveis |
| `/patrimonio/localizacao` | `PatrimonioPorOrgaoController` | Por órgão e localização |
| `/patrimonio/relatorio` | `PatrimonioRelatorioController` | Demonstrativos |

- ✅ Serviços: `/patrimonio/*` (demonstrativos, localização, bens móveis por ano/UG/gestão, algumas por `POST`), `/v2/bens-imoveis/*` (regiões administrativas, órgãos, situações, detalhe por tombamento com terrenos, edificações e obras) e `/v2/patrimonio/bens-moveis/*` (órgãos, estados, tipos).
- ✅ Exportação: `/patrimonio/relatorio/{bens-moveis,localizacao}` e `/v2/bens-imoveis/relatorios`.
- ✅ Sem testes automatizados neste módulo.

## Inferências e limitações
- 🔶 Bens móveis têm duas implementações (`patrimonio-bens-moveis.controller.js` e `bens-moveis/bens-moveis.controller.js`); qual está na rota ativa não foi confirmado além do nome `BensMoveisController`.
- 🔶 Regras: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Patrimonio|Backend: Patrimônio]].

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
