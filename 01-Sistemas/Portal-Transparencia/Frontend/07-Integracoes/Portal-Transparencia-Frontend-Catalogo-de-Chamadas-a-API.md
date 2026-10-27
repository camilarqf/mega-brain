---
type: api
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
  - api
  - chamadas
sources:
  - src/app/components/despesas/despesas.service.js
  - src/app/components/receitas/receitas.service.js
  - src/app/components/servidores/servidores.service.js
  - src/app/components/servidores/remuneracao.service.js
  - src/app/components/servidores/cadastroexpulsoes.service.js
  - src/app/components/orcamento/orcamento.service.js
  - src/app/components/licitacoes-contratos/licitacoes-contratos.service.js
  - src/app/components/licitacoes-contratos/licitacoes/licitacoes.service.js
  - src/app/components/convenio/convenio.service.js
  - src/app/components/patrimonio/patrimonio.service.js
  - src/app/components/prestando-contas/prestando-contas.service.js
  - src/app/components/compartilhado/services
---

# Frontend — catálogo de chamadas à API

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

## Objetivo
Listar, por serviço do frontend, as chamadas feitas à API do Backend. Contrato (parâmetros e respostas) fica no Backend: [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]].

## Evidências
Commit `dca3e933`. Extração por script dos `$http`/`$http.get/post` dos arquivos `*.service.js` (359 chamadas em 38 arquivos). Não inclui chamadas de `tabela-consulta` (URL no HTML), `PagingService` (URL recebido), `RelatorioService.exportar` (61 chamadas nos controllers) nem URLs montados dinamicamente (ver observação por serviço).

## Informações confirmadas
| Serviço (arquivo) | Chamadas | Famílias de caminho (prefixo `api.url`) |
|---|---|---|
| `despesas/despesas.service.js` | 87 (85 GET, 2 POST) | `/despesa/*`: filtros, anos, `grafico/*`, `emendas-parlamentares/*`, `emenda-parlamentar-federal/*`, `diarias-passagens/*`, `detalhamento/*`, `oca/*`, `nota-empenho/*`, `nota-lancamento/*`, `ordem-bancaria/*`, `pagamentos-por-credor/*`, `restos-a-pagar/anos`, `ordens-cancelamento` (POST), `prioridades` |
| `receitas/receitas.service.js` | 30 | `/receita/*` (anos, gestão, unidade gestora, fonte, rubrica, alínea, `grafico/*`, `multas`), `/receita-uniao/*` |
| `servidores/servidores.service.js` | 53 | `/servidor/*` (órgão, cargo, carreira, quadro, status, `grafico/*`, `militares-cedidos/*`, `listarDataReferencia*`), `/remuneracao/anos`, `/remuneracao/ultimo-exercicio*`, `/pesquisa/grafico/*`, `/analytics/paginas-populares` |
| `servidores/remuneracao.service.js` | 9 | `/remuneracao/*` (órgão, cargo, função, situação, rubrica, extrato, `grafico/evolucao`) |
| `servidores/cadastroexpulsoes.service.js` | 4 | `/expulsao/*` |
| `orcamento/orcamento.service.js` | 10 (2 POST) | `/orcamento/*` (anos de LDO, LOA, LRF, relatórios gerenciais; assuntos; `categorias`/`data-referencias` por POST) |
| `licitacoes-contratos/licitacoes-contratos.service.js` | 26 | `/licitacoes-contratos/*` e `/v2/itens-licitados/*` |
| `licitacoes-contratos/licitacoes/licitacoes.service.js` | 7 | `/v2/licitacoes/*` (anos, órgãos, tipos, situações, fornecedores por pregão, itens por fornecedor, participantes) |
| `convenio/convenio.service.js` | 13 | `/convenio/*` (receita, despesa, entidades beneficiadas, extrato) |
| `patrimonio/patrimonio.service.js` | 9 (2 POST) | `/patrimonio/*` |
| `patrimonio/bens-imoveis/bens-imoveis.service.js` | 7 | `/v2/bens-imoveis/*` (incl. terrenos, edificações, obras) |
| `patrimonio/bens-moveis/bens-moveis.service.js` | 3 | `/v2/patrimonio/bens-moveis/*` |
| `prestando-contas/prestando-contas.service.js` | 59 (1 POST) | `/prestando-contas/*` (benefícios, órgãos deliberativos, conselhos, OSS, Prospera-DF, programa de integridade …), `/empresa-punida/*`, `/texto-explicativo/*`, `/dataAtualizacao/hora/empresas-punidas` |
| `prestando-contas/pads/pads.service.js`, `pips/pips.services.js` | 6 + 6 | `/prestando-contas/processos-administrativos-disciplinares/*`, `/prestando-contas/processos-investigacoes-preliminares/*` |
| `quadros-tematicos/quadros-tematicos.service.js`, `setor-desejado.service.js` | 2 + 1 | `/v2/paineis-despesa*` |
| `compartilhado/services/execucao-despesa/*` | 2 | `/v2/dashboard-execucao-despesa/listar`, `/listar-anos` |
| `compartilhado/services/estatisticas.service.js` | 6 | `/analytics/*` (visitas, categoria de dispositivos, usuários ativos, total de sessões/visualizações, páginas populares) |
| `compartilhado/services/*` (outros) | ~14 | `/gestao`, `/unidadeGestora`, `/textos-consultas`, `/arquivos?codCategoria=`, `/v2/despesas-ras?exercicio=`, `/v2/imagens/imagens-slideshow`, `/v2/pesquisa-satisfacao/` (POST), `/contato/registro` (POST), `/receita/grafico/arrecadacao-imposto` |
| `acesso-informacao/acesso-informacao.service.js` | 1 | `/v2/orgaos-lai` |
| `template/partials/topnav.service.js` | 2 | `/arquivos/url-ultimo-arquivo-categoria/{cod}` e `…-exercicio/{cod}/{ano}` |
| `data.atualizacao.service.js` | 1 | `/dataAtualizacao/{chave}` |
| `super-busca/super-busca.service.js` | 1 (host `apisuperbusca`) | `/indice`, `/indice-cpf`, `/indice-cod-credor` (outra integração) |

Também no `RelatorioService.exportar`: rotas `/despesa/relatorio/*`, `/convenio/relatorio/*`, `/licitacoes-contratos/relatorio/contrato`, `/patrimonio/relatorio/*`, `/v2/itens-licitados/relatorios`, `/v2/licitacoes/relatorios`, `/v2/bens-imoveis/relatorios`, `/despesa/restos-a-pagar/relatorio`.

## Inferências e limitações
- 🔶 Os serviços de Despesas, Prestando Contas e Servidores concentram mais da metade das chamadas (199 de 359); reflete a quantidade de filtros dinâmicos, não necessariamente uso.
- ❓ Não há chamadas de gravação (exceto `POST` de consulta com corpo, pesquisa de satisfação e contato).
- ❓ O caminho `GET /convenio/relatorio//entidades-beneficiadas` (barra dupla) existe no controller de entidades beneficiadas; depende da tolerância do Backend.
- Caminhos sem rota correspondente no Backend: ver [[01-Sistemas/Portal-Transparencia/Frontend/07-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API]].

## Relacionamentos
- Módulos: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]] (cada módulo lista seus serviços).

## Pendências e próximo passo
- Comparar parâmetros e DTOs campo a campo e verificar quais das chamadas sem rota estão em telas ativas (ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Registro-de-Analise|Registro de análise]]).
