---
type: technical-debt
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - debitos
  - riscos
sources:
  - app/token-auth-interceptor.js
  - app/token-storage-service.js
  - app/nav/nav-ctrl.js
  - app/app.routes.js
  - app/registro/por-operador/pedido-por-operadorCtrl.js
  - app/conta/pessoa-juridica/atualizar-cadastro-pessoa-juridica-ctrl.js
  - app/super-busca/super-busca.ctrl.js
  - app/upload/upload-arquivos-directive.js
  - app/upload/upload-pedido-directive.js
  - app/caixa-entrada/caixa-entrada-unidade-ctrl.js
  - app/caixa-entrada/detalhamento-pedido-ctrl.js
  - app/gerencial/unidade/grid-unidade.ctrl.js
  - gulpfile.js
  - Dockerfile
  - nginx.conf
  - package.json
  - api.config.json
---

# Frontend SIC — débitos técnicos e riscos

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Testes: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/06-Qualidade/PARTICIPA-DF-Frontend-SIC-Testes-e-Cobertura|Testes-e-Cobertura]]

## Objetivo
Listar débitos e riscos **observados no código**, separados das recomendações. Severidade: 🔴 alta · 🟠 média · 🟡 baixa. Nada foi executado; "defeito" indica falha evidente pela leitura do código.

## Evidências
Arquivos em `sources`, commit `5518a81`.

## Informações confirmadas (fatos)

### Segurança
| # | Sev. | Fato | Onde |
|---|---|---|---|
| S1 | 🔴 | A `application-key` está fixa em texto no JavaScript entregue ao navegador (valor omitido). | `app/token-auth-interceptor.js` |
| S2 | 🟠 | Dados pessoais (nome, nome da mãe, data de nascimento, CPF, razão social, CNPJ) trafegam **no caminho da rota** e CPF/CNPJ em *query string* (`security/check`, `count-try`, `check-cpf-vinculado-pj`). | `app/app.routes.js`; `pedido-por-operadorCtrl.js`; `atualizar-cadastro-pessoa-juridica-ctrl.js` |
| S3 | 🟠 | Token em `localStorage`; AngularJS 1.5.8, jQuery 1.11.1 e Bootstrap 3.3.6 estão fora de suporte. | `app/token-storage-service.js`; `assets/lib` |
| S4 | 🟡 | Rotas sem guarda (`resolve`); proteção só pelo backend (401/403). | `app/app.routes.js` |
| S5 | 🟡 | `GET security/check-cpf-vinculado-pj` envia o aceite de responsabilidade como parâmetro de URL. | `pedido-por-operadorCtrl.js` |

### Defeitos funcionais
| # | Sev. | Fato | Onde |
|---|---|---|---|
| D1 | 🟠 | Após erro de desafio na atualização de PJ, `extrairCaracteres(vm.cpf)` recebe `undefined` (`vm.cpf` não existe; o CPF está em `vm.cpfVinculado`) → `TypeError`. | `atualizar-cadastro-pessoa-juridica-ctrl.js` |
| D2 | 🟠 | O mesmo controller usa `$ngConfirm` (`tentativasEsgotadasFim`) sem injetá-lo → `ReferenceError` ao esgotar as tentativas. | idem |
| D3 | 🟠 | `visualizaArquivo` em `uplArquivos`: o *case* `jpeg` usa `blobJpg`, declarado com `const` no *case* `jpg` (mesmo bloco `switch`) → erro de referência para `.jpeg`. Outras extensões (`txt`, `csv`, `zip`...) não abrem. | `upload-arquivos-directive.js` |
| D4 | 🟠 | Remoção de anexo em `uplPedido` usa `grupoSituacao.Arquivo.splice(arquivo, 1)`: passa o **objeto** no lugar do índice (vira índice 0), removendo o primeiro item do grupo da lista local, não necessariamente o removido no servidor. | `upload-pedido-directive.js` |
| D5 | 🟡 | `pesquisarCnpj` chama `pessoa-juridica/existe` duas vezes (dentro e fora do retorno de `security/check`). | `pedido-por-operadorCtrl.js` |
| D6 | 🟡 | `detalharPedido` dispara `permite-detalhar` uma vez por linha de resultado, sempre para o mesmo pedido. | `super-busca.ctrl.js` |
| D7 | 🟡 | `nav-ctrl.js` escuta `acessoNegadoEvt` e chama `verificarToken()`, **não definida**; o evento não é emitido. | `app/nav/nav-ctrl.js` |
| D8 | 🟡 | `$scope.$on('alternarUnidade')` nunca é disparado (a troca usa `$route.reload()`). | `caixa-entrada-unidade-ctrl.js` |
| D9 | 🟡 | Rota `/bloquear-usuario` sem controller nem template. | `app/app.routes.js` |
| D10 | 🟡 | Variáveis globais implícitas (`Evento`, `paramImprimir`, `grupoSituacao`, `ano`, `createModel`, `listaUnidadesId`) por falta de `var`/`let`. | `detalhamento-pedido-ctrl.js`, `upload-pedido-directive.js`, `grid-*.ctrl.js`, `form-*.ctrl.js` |
| D11 | 🟡 | `authCtrl` espera 3 s fixos (`setTimeout`) e não trata falha de `token-retrieve`. | `app/auth/auth-ctrl.js` |
| D12 | 🟡 | `uplArquivos` calcula o volume inicial dividindo por 1024 (GB) e depois soma MB; a checagem de 25 MB mistura unidades. | `upload-arquivos-directive.js` |

### Capacidade e configuração
| # | Sev. | Fato | Onde |
|---|---|---|---|
| C1 | 🟠 | O front limita a soma dos anexos a 25 MB, mas envia o conteúdo em **base64** dentro do JSON (~33% maior) e o `nginx` aceita no máximo `25M` por requisição; o backend aceita até 40 MB nos endpoints de anexo (notas do backend). Anexos próximos de 25 MB podem ser recusados pelo `nginx`. (o commit `6527d15`, 2026-08-20, acrescentou `client_max_body_size 25M` ao `nginx.conf`.) | `upload-arquivos-directive.js`; `nginx.conf` |
| C2 | 🟡 | `noSpinner` é enviado como parâmetro/corpo à API em vez de ser filtrado pelo *spinner*. | `app/spinner/spinner.js`; `caixa-entrada-unidade-ctrl.js` |
| C3 | 🟡 | Dois arquivos versionados definem a mesma constante `configService` (`api.config.js`, `api-dist.config.js`); `gulp dev` concatena `app/**/*.js` (os dois entram); a precedência depende da ordem. `api-dist.config.js` tem endereço de ambiente. | `app/api*.config.js`; `gulpfile.js` |
| C4 | 🟡 | `views-dist.js` (gerado) e `api*.config.js` (gerados) estão versionados. | `app/` |
| C5 | 🟡 | `ENVIRONMENT` do pipeline não é lida pelo `Dockerfile`; o perfil do build depende de `--build-arg profile` (padrão `prod`). | `Dockerfile`; `.jenkins-pipelines` |
| C6 | 🟡 | `gulpfile.js` copia `Web.config`, `Web.Producao.config` e `auth.html`, que não existem no repositório (herança de IIS). Regras fixas para `/participa-df-sic-test/` em `nginx.conf`. | `gulpfile.js`; `nginx.conf` |

### Manutenção
| # | Sev. | Fato | Onde |
|---|---|---|---|
| M1 | 🟠 | Sem testes automatizados; `npm test` falha por definição. | `package.json` |
| M2 | 🟠 | Build em Node 10 e Gulp 3 (fora de suporte). | `Dockerfile`; `package.json` |
| M3 | 🟡 | Dependências e bibliotecas sem uso no SIC: `@microsoft/signalr`, `ol.js`, `gmaps`, `highcharts`, `Chart.js` (carregadas em todas as telas). | `package.json`; `assets/lib` |
| M4 | 🟡 | Código herdado do front de Ouvidoria: nome `OuvCidadania.Ui`, módulo `Ouv-DF`, `getDataUnidade` (cópia de `getDataFeriado`). | vários |
| M5 | 🟡 | Erros de grafia em nomes (`prorragacaoPrazo`, `visualizar-contra-ctrl.js`). | vários |
| M6 | 🟡 | `libs-dev` referencia `signalr.min.js`, mas o arquivo é `signalr.js`; `libs-dist` omite o SignalR. | `gulpfile.js` |
| M7 | 🟡 | Controllers chamam `Api` direto (97 chamadas), com lógica de negócio e de apresentação misturadas; controllers de 400 a 450 linhas (`caixa-entrada-unidade-ctrl.js`, `detalhamento-pedido-ctrl.js`, `pedido-por-operadorCtrl.js`). | `app/` |

## Recomendações (não são fatos do código)
1. S1: tratar a `application-key` como configuração do ambiente (ou confirmar que não é segredo) e rever o histórico do Git.
2. S2/S5: trocar o transporte de CPF/CNPJ de `GET` com *query string* por `POST` com corpo e remover dados pessoais da URL das rotas (usar estado/serviço).
3. D1–D4: corrigir os quatro defeitos (baixo custo) e cobrir com testes de controller.
4. C1: alinhar `client_max_body_size` com o limite efetivo (considerar o acréscimo do base64) ou migrar para `multipart/form-data`.
5. M1–M2: introduzir lint (JSHint/ESLint) e testes mínimos no pipeline; planejar a atualização de Node/Gulp e das bibliotecas.
6. Remover resíduos (rota `/bloquear-usuario`, bibliotecas sem uso, evento `acessoNegadoEvt`, arquivos gerados do versionamento).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Perfis-e-Ambientes|Perfis-e-Ambientes]] · Equivalente: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/06-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Débitos do Frontend Ouvidoria]]

## Pendências e próximo passo
- Priorizar S1, D1–D4 e C1 com o time. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
