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
  - servidores
  - dados-pessoais
sources:
  - src/app/index.route.js
  - src/app/components/servidores
---

# Frontend — módulo Servidores

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Consultas públicas sobre servidores: remuneração, quadro, perfil, status, cargos, expulsões, militares cedidos e ressarcimento de requisitados.

## Evidências
Commit `dca3e933`. Rotas em `index.route.js`; `components/servidores/**` (20 JS, 35 HTML); `servidores.service.js` (53 chamadas), `remuneracao.service.js` (9), `cadastroexpulsoes.service.js` (4).

## Informações confirmadas
| Caminho | Controller | Rótulo |
|---|---|---|
| `/servidores/dashboard` | `ServidoresDashboardController` | Painel |
| `/servidores/remuneracao` · `/remuneracao/saiba-mais` | `RemuneracaoController` · `ServidoresRemuneracaoSaibaMaisController` | Remuneração dos servidores |
| `/servidores/orgao` | `ServidoresController` | Servidores por órgão |
| `/servidores/perfil` | `ServidoresPerfilController` | Perfil dos servidores |
| `/servidores/expulsoes` | `CadastroExpulsoesController` | Cadastro de expulsões |
| `/servidores/quadro` | `ServidorQuadroController` | Quadro de servidores |
| `/servidores/status` | `StatusServidoresController` | Servidores por status |
| `/servidores/cargo-comissionado` · `/cargo-efetivo` | `CargoComissionadoController` · `CargoEfetivoController` (base `cargo.base.controller.js`) | Cargos |
| `/servidores/militares-cedidos` | `MilitaresCedidosController` | Militares cedidos |
| `/servidores/ressarcimento-requisitado` · `…/saiba-mais` | `RessarcimentoRequisitadoController` · `…SaibaMais…` | Ressarcimento de requisitados |

- ✅ Serviços: `ServidoresService` (`/servidor/*`, `/remuneracao/anos`, `/pesquisa/grafico/*`, `/servidor/grafico/*`), `RemuneracaoService` (`/remuneracao/*`, incl. extrato por matrícula/ano/mês), `CadastroExpulsoesService` (`/expulsao/*`). A rota de ressarcimento carrega filtros de **despesas** (`DespesasService`).
- ✅ Exportação via `RelatorioService.exportar` em 7 controllers (`/servidor/relatorio/`, `/remuneracao/relatorio/…`, `/expulsao/relatorio/`, `/servidor/militares-cedidos/relatorios` e `/despesa/relatorio/ressarcimento-requisit…`). Telas de "saiba mais" e quadros montam links de arquivos com `ArquivoUrlService.ARQUIVOS`. A rota `/url-arquivo` aceita as consultas `cedidos-policia-militar-df` e `cedidos-bombeiros-df` (categorias 61 e 62).
- ✅ Testes: 6 specs (cargo comissionado, cargo efetivo, remuneração, servidores, ressarcimento ×2).

## Inferências e limitações
- 🔶 A tela de remuneração por servidor e o extrato por matrícula exibem **dados pessoais** vindos do Backend (nome, matrícula, valores). O mascaramento é feito no Backend: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache e mascaramento]] e [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]]. O frontend não aplica máscara própria (não verificado em todos os templates).
- ✅ Chamadas sem rota no Backend: `GET /servidor/listarDataReferenciaPorOutrosOrcamento`.
- 🔶 O `ServidoresService` lê `/analytics/paginas-populares` (misturado ao módulo de servidores no painel).
- Cobertura parcial.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]] · [[01-Sistemas/Portal-Transparencia/Frontend/05-Seguranca/Portal-Transparencia-Frontend-Seguranca-e-Privacidade|Segurança e privacidade]]
- Backend: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Servidores-e-Remuneracao|Servidores e Remuneração]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
