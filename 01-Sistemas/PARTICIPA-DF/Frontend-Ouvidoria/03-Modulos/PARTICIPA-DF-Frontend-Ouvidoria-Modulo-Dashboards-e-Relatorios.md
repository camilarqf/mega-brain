---
type: module
aliases:
  - "Frontend Ouvidoria — dashboards e relatórios"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
sources:
  - app/dashboard
  - app/manifestacao/painel-avaliacao
  - app/app.routes.js
  - app/nav/nav-ctrl.js
---

# Frontend Ouvidoria — dashboards e relatórios

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Rotas: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Rotas-e-Telas|Rotas-e-Telas]]

## Objetivo
Registrar os painéis de produtividade ativos e os relatórios legados que existem no código sem rota.

## Evidências
Arquivos em `sources`, commit `9d8ecdb`. Cobertura `parcial`: lidos os dois controllers ativos e amostras dos demais; os gráficos não foram executados.

## Informações confirmadas

### Ativos (com rota e item de menu "Produtividade", permissão `VisualizarPaineis`)
| Rota | Controller | Chamadas | Conteúdo |
|---|---|---|---|
| `/dashboard/rel_operacoes_de_atendente` | `rel_operacoes_de_atendente_ctrl` | `GET operador-so/consultar-por-unidade`; `POST dashboard/produtividade-operador-so` (filtro: operador e período) | série mensal de manifestações registradas; respostas definitivas, complementares e preliminares; trâmites; reclassificações; invalidações; indicador de resolutividade (gauge) |
| `/dashboard/rel_operacoes_unidade` | `rel_operacoes_unidade_ctrl` | `GET unidade/subordinadasSO`; `POST dashboard/produtividade-unidade` (filtro: unidade e período; botão "Enviar" só habilitado com unidade) | visão equivalente por unidade |

- ✅ Gráficos com Highcharts (área, pizza, gauge); cada bloco recebe `Labels`, `Values` e `Total` do backend.

### Legados (controllers e templates existentes, **sem rota**)
`rel_total_man`, `rel_assuntos`, `rel_carta_de_servicos`, `rel_man_anonima`, `rel_man_tipoEntrada`, `rel_man_vencidas`, `rel_man_vinculada`, `rel_satisfacao_resolutividade` e `painel-interativo` (`paineiInterativoCtrl`, com mapa interativo).
- ✅ Dependem de serviços `dashboardAPI`, `manifestacaoAPI`, `regiaoAdministrativaAPI`, `classificacaoAPI`, `usuarioAPI`, `colecoesAPI` e `assuntoAPI`, que **não estão definidos** no repositório; mesmo que ganhassem rota, falhariam na injeção.
- 🔶 São resquícios de uma versão anterior com outro camada de acesso à API.

### Painel de avaliação (`/painel-avaliacao`)
- ✅ Rota existe (`painelAvaliacaoCtrl`), mas o controller depende de `avaliacaoPorOperadorAPI`, `manifestacaoAPI` e `questionarioAPI` (não definidos). Pelo código, o propósito é o operador registrar uma solicitação de avaliação do atendimento e conduzir a pesquisa de satisfação em nome do manifestante (`registrarSolicitacaoDeAvaliacao`, `confirmarAvaliacaoAtendimento`, `registrarPesquisaDeSatisfacaoPorOperador`). Permissão no template: `GerenciarPainelAvaliacao`. Funcionamento atual: ❓ não confirmado.

## Inferências e limitações
- 🔶 A caixa de entrada oferece indicadores rápidos (em análise, fora do prazo, resolvida etc.) que cobrem parte dos relatórios legados; ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Caixa-de-Entrada-e-Detalhamento|Caixa-de-Entrada-e-Detalhamento]].
- Os 11 painéis/relatórios (22 arquivos `.js`/`.html`) não foram todos lidos linha a linha.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas-de-API]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Decidir com o time se os relatórios legados e o painel de avaliação devem ser removidos ou restaurados. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
