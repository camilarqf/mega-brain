---
type: technical-debt
aliases:
  - "Frontend Ouvidoria — débitos técnicos e riscos"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
sources:
  - app/login/login-ctrl.js
  - app/token-auth-interceptor.js
  - app/app.routes.js
  - app/manifestacao/caixa-de-entrada/caixa-de-entrada-ctrl.js
  - app/manifestacao/caixa-de-entrada/detalhar-manifestacao-ctrl.js
  - app/manifestacao/registro/por-operador/manifestacao-por-operadorCtrl.js
  - app/api.config.js
  - app/views-dist.js
  - gulpfile.js
  - package.json
  - .tool-versions
  - assets/lib
---

# Frontend Ouvidoria — débitos técnicos e riscos

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Segurança: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/08-Seguranca/PARTICIPA-DF-Frontend-Ouvidoria-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Objetivo
Listar débitos e riscos, **separados dos fatos**, com severidade e recomendação. Os fatos de apoio estão nas notas linkadas; as recomendações abaixo são sugestões, não requisitos aprovados.

Severidade: 🔴 alto · 🟠 médio · 🟡 baixo.

## Evidências
Arquivos em `sources`, commit `9d8ecdb`; leitura estática. Cobertura `parcial`.

## Fatos e recomendações

### 🔴 Alto
| # | Fato (evidência) | Recomendação |
|---|---|---|
| 1 | Credenciais (login e senha) fixas em `app/login/login-ctrl.js`, versionadas no histórico do repositório. O controller não tem rota. Valores omitidos aqui. | Tratar como comprometidas: remover o arquivo, **trocar a senha** do usuário correspondente no backend e revisar o histórico do Git. |
| 2 | Chave de aplicação fixa (`application-key`) no interceptor, enviada em toda requisição (`app/token-auth-interceptor.js`). | Confirmar com o time o papel da chave; se for secreta, rotacionar e tirar do código-fonte do navegador. |
| 3 | Dados pessoais (nome, nome da mãe, data de nascimento, CPF/CNPJ) em **parâmetros de rota** e em *query string* de `GET security/*` ([[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Conta-por-Operador|Conta-por-Operador]]). | Passar os dados por estado em memória/serviço e usar `POST` com corpo. |
| 4 | **Sem testes automatizados** nem lint ([[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Testes-e-Cobertura|Testes-e-Cobertura]]). | Criar testes de caracterização das telas críticas (caixa de entrada, detalhe, registro) antes de mudanças grandes. |
| 5 | Plataforma obsoleta: AngularJS 1.x, jQuery 1.11.1, Bootstrap 3, Gulp 3, Node 10 (`Dockerfile`) e Node 6 (`.tool-versions`); bibliotecas copiadas à mão em `assets/lib`. AngularJS 1.x está fora de suporte desde 2022 (conhecimento externo). | Planejar a migração (ex.: para o Angular usado no [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Frontend Cidadão]]) ou ao menos atualizar bibliotecas com CVEs conhecidos. |

### 🟠 Médio
| # | Fato | Recomendação |
|---|---|---|
| 6 | Telas/rotas quebradas ou mortas: `/painel-avaliacao`, `/exportar-pdf/:id`, `/listaDeNotificacao`, `/criarFormulario`, `/bloquear-usuario` (primeiro registro) — ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Rotas-e-Telas|Rotas-e-Telas]]. | Confirmar uso; consertar ou remover. |
| 7 | Serviços injetados e **não definidos** no repositório: `manifestacaoAPI`, `questionarioAPI`, `avaliacaoPorOperadorAPI`, `perfilAPI`, `unidadeAPI`, `notificacaoDePrazoAPI`, `dashboardAPI`, `regiaoAdministrativaAPI`, `classificacaoAPI`, `usuarioAPI`, `colecoesAPI`, `assuntoAPI` (controllers legados e 8 dos 10 relatórios do dashboard). | Remover o código legado ou restaurar os serviços. |
| 8 | Código morto/legado: `loginCtrl`, `perfilCtrl`, `unidadeCtrl`, `usuarioCtrl`, `questionarioCtrl`, `grid-prazo`/`form-prazo`, `formOperadorCtrl`, `mapOLService`, `efetuarDownloadAnexo`, SignalR; 7 caminhos de API sem correspondência no backend. | Limpeza guiada pelas pendências. |
| 9 | Autorização só no menu: nenhuma rota tem guarda; telas gerenciais dependem inteiramente do backend. | Adicionar guarda por permissão no `$routeChangeStart` (defesa em profundidade). |
| 10 | Arquivos gerados versionados: `app/api.config.js` (perfil `local`) e `app/views-dist.js` (~427 KB) estão no Git; `Web.config`, `Web.Producao.config` e `auth.html`, exigidos pelo build, **não estão**. | Decidir o que versionar; documentar/fornecer os arquivos ausentes. |
| 11 | Tela de detalhe tem 69 KB de HTML e o controller concentra ~25 ações; telas de lista repetem o mesmo esqueleto (grid-*) em 7 controllers. | Extrair componentes/serviço de lista paginada. |
| 12 | `window.location.reload()` após anexar/remover arquivo; `setTimeout` de 3 s no login (`authCtrl`) como sincronização. | Atualizar o estado sem recarregar; usar promessas/eventos. |
| 13 | `trustAsHtml` em autocompletes com texto vindo da API (13 ocorrências de `trustAsHtml`/`ng-bind-html`). | Escapar o texto ou usar *templates* sem HTML confiável. |
| 14 | Serviço de localização por HTTP nos perfis `local`/`homologacao`; API de homologação por HTTP. | Usar HTTPS em todos os ambientes não locais. |

### 🟡 Baixo
| # | Fato | Recomendação |
|---|---|---|
| 15 | Defeitos pontuais: `onDetailById` navega para rota inexistente (`detalheManifestacao/`); `atualizarCaixaDeEntrada` chama `init()` indefinido; `exportarPDF` usa `/exportarPDF/`; `vm.arraySomaArquivos.push(...).toFixed(2)` aplica `toFixed` ao tamanho do array; `pesquisarCnpj` encadeia `.then(Api.POST(...))` (a 2ª chamada não espera a 1ª); `solicitarProrrogacaoDePrazo` e outras variáveis globais implícitas (`createModel =`, `i`, `listaUnidadesId`). | Corrigir junto com a cobertura de testes. |
| 16 | `console.log` do histórico de CPF vinculado; 51 usos de jQuery (`$('#modal…')`) dentro de controllers. | Remover o log; encapsular modais em serviço/diretiva. |
| 17 | Codificação mista (arquivos com BOM, conversão para ISO-8859-1 no build das libs); mistura de PascalCase e camelCase nos corpos de requisição. | Padronizar em UTF-8 e convenção de nomes. |
| 18 | `angular-sanitize.js` e `angular-sanitize.min.js` carregados juntos; `htmlhint` instalado e sem uso; `packages.config`, `Properties/*` e perfis `.pubxml` de um projeto .NET antigo. | Remover duplicidades e legados. |
| 19 | Texto de erro e mensagens de domínio fixos em português no código (ex.: prazo de 24 horas na mensagem de tentativas esgotadas). | Se a regra mudar no backend, o texto fica defasado; ler da resposta da API. |

## Inferências e limitações
- 🔶 A severidade é uma avaliação desta análise, sem ouvir o time. Itens 6 a 8 podem ser aceitos como "dívida conhecida" se as telas realmente não forem usadas.
- Sem execução, não foi possível reproduzir os defeitos do item 15.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/09-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Debitos-Tecnicos|Débitos do Frontend Cidadão]] · [[01-Sistemas/PARTICIPA-DF/Backend/09-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Débitos do Backend]]

## Pendências e próximo passo
- Priorizar os itens 1 a 3 (segurança) com o responsável pelo sistema; as ações são do time e fora do escopo da documentação.
