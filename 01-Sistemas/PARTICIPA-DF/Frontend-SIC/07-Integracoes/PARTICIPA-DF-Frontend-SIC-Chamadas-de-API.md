---
type: api
aliases:
  - "Frontend SIC — chamadas de API ao backend"
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
sources:
  - app/api.service.js
  - app/token-auth-interceptor.js
  - app/spinner/spinner.js
  - app/nav/nav-ctrl.js
  - app/auth/auth-ctrl.js
  - app/caixa-entrada/caixa-entrada-unidade-ctrl.js
  - app/caixa-entrada/detalhamento-pedido-ctrl.js
  - app/registro/por-operador
  - app/conta
  - app/gerencial
  - app/super-busca/super-busca.ctrl.js
  - app/upload
---

# Frontend SIC — chamadas de API ao backend

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Integração: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Integracoes-Externas|Integracoes-Externas]] · Contrato: [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Endpoints-SIC|Endpoints-SIC]] · [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]]

## Objetivo
Listar os endpoints do `participa-df-backend` consumidos pelo `participa-df-sic-frontend`, por área, e como são chamados.

## Evidências
- Extração por `grep` das chamadas `Api.GET/POST(...)` (97 ocorrências em `app/`) mais 10 caminhos montados em *strings* dos controllers (editores de resposta e decisão, SEI e a *view* da caixa de entrada). Total: **77 caminhos distintos** (18 `GET`, 59 `POST`), commit `5518a81`.
- Comparação **textual** com `Backend/05-API` (commit `4901ad5`): 76 caminhos presentes; `v2/usuario/true/false` só tem o prefixo `v2/usuario` no catálogo (parcial). **Payloads, parâmetros e códigos de retorno não foram conferidos.**

## Informações confirmadas

### Como as chamadas são feitas
- ✅ Serviço `Api`: `GET(endpoint, params)` e `POST(endpoint, data)` com `configService.urlApi + endpoint`; `GETe`/`POSTe` (URL absoluta) **não são usados**.
- ✅ Em 400 os erros vêm em `Notifications` (ou `error`) e são exibidos por `custom-exception`; 500 abre modal com `Message`; 401/403 redireciona ao login. Sem *retry* nem *timeout*.
- ✅ `noSpinner`: em `GET` é enviado como **parâmetro de query** (`?noSpinner=true`) e suprime o modal de carregamento. Em `POST`, `{ noSpinner: true }` aparece **no corpo** de `pedido/unidade/itens-filtro` (como dados) e como 3º argumento (ignorado por `Api.POST`, que só usa 2 parâmetros) em `pedido/acoes-operador`; nesses casos o *spinner* não é suprimido.

### Sessão e usuário
| Verbo | Caminho | Uso |
|---|---|---|
| GET | `security/token-retrieve/{sessionId}` | troca o `sessionId` pelo token ([[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Autenticacao\|Fluxo-Autenticacao]]) |
| GET | `security/is-auth` | valida a sessão |
| GET | `configuration/front-end-urls` | endereços `Login` e `Principal` (redirecionamentos) |
| GET | `v2/usuario/true/false` | dados do usuário logado |
| GET | `operador-sic/consultar-permissoes` | permissões de gerenciamento e `IsUnidadeAtualSuperioSic` |
| GET | `operador-sic/unidades` | unidades do operador |
| POST | `operador-sic/alterar-unidade-atual` | troca a unidade atual |

### Caixa de entrada e pedido (prefixo `acesso-informacao/`)
| Verbo | Caminho | Uso |
|---|---|---|
| POST | `pedido/unidade` | lista paginada, filtros, ordenação e exportação CSV (mesmo endpoint) |
| POST | `pedido/unidade/itens-filtro` | opções de assunto e situação |
| POST | `pedido/detalhar-por-unidade` | detalhe do pedido |
| POST | `pedido/acoes-operador` | ações permitidas (`Acoes`) |
| POST | `pedido/detalhar-evento-pedido` | detalhe de um evento do histórico |
| POST | `pedido/exportar-operador` | PDF do pedido (base64) |
| POST | `pedido/prorrogar-prazo`, `pedido/reencaminharPedido`, `pedido/remover-operador-atual` | ações administrativas |
| POST | `pedido/registrar-resposta`, `pedido/registrar-resposta-definitiva` | respostas do pedido |
| POST | `recurso/primeira-instancia/registrar-resposta`, `recurso/segunda-instancia/registrar-resposta`, `recurso/terceira-instancia/registrar-resposta-preliminar` | respostas de recurso |
| POST | `recurso/terceira-instancia/registrar-decisao` | decisão de 3ª instância |
| POST | `notificacao/omissao-resposta-cgdf/registrar-resposta`, `.../registrar-decisao` | omissão de resposta |
| POST | `pedido/registrar-pedido-sei` | envio ao SEI (retorna o número do processo) |
| POST | `situacao/situacao-resposta`, `classificacao/por-situacao` | opções do editor de resposta |
| GET | `pedido/tipos-de-sigilo`, `recurso/terceira-instancia/tipo-decisao` | domínios |
| POST | `pedido/consultar-por-termo`, `pedido/permite-detalhar` | super-busca |
| POST | `arquivo/validar`, `arquivo/download`, `arquivo/excluir-por-operador` | anexos |

### Registro por operador
| Verbo | Caminho | Uso |
|---|---|---|
| POST | `acesso-informacao/pedido/por-operador` | registra o pedido |
| POST | `acesso-informacao/pedido/consultar-por-lote` | lista pedidos do lote |
| GET | `acesso-informacao/assunto` | assuntos |
| POST | `unidade/ouvidorias-ativas` | unidades (`AtivoModuloSIC` true/false) |

### Identificação e conta do solicitante
| Verbo | Caminho | Uso |
|---|---|---|
| POST | `pessoa-fisica/existe`, `pessoa-juridica/existe`, `usuario/id` | localizar solicitante |
| GET | `security/check`, `security/count-try`, `security/check-cpf-vinculado-pj` | desafio e tentativas |
| POST | `security/challenge` | resposta do desafio |
| POST | `pessoa-fisica/desbloquear-dados-inconsistentes`, `pessoa-juridica/desbloquear-dados-inconsistentes` | desbloqueio |
| POST | `pessoa-fisica/por-operador`, `pessoa-fisica/atualizar/por-operador`, `pessoa-juridica/por-operador`, `pessoa-juridica/atualizar/por-operador` | cadastro/atualização |
| POST | `pessoa-juridica/atualizar-responsavel`, `pessoa-juridica/historico-responsavel-por-operador` | CPF vinculado da PJ |
| POST | `pessoa-fisica/por-cpf` | busca PF (cadastro de operador) |
| GET | `necessidade-especial`, `pessoa-juridica/tipo-entidade` | domínios |

### Gerencial
| Verbo | Caminho | Uso |
|---|---|---|
| POST/GET | `operador-sic` (lista), `operador-sic/{cadastrar,atualizar,ativar,desativar,consultar-por-id,consultar-por-cpf}`, `GET operador-sic/operador-existe` | operadores |
| POST/GET | `acesso-informacao/perfil-sic` (grava), `.../get-perfis`, `.../get-perfil-por-id`, `GET .../ativos`, `GET .../funcionalidade` | perfis |
| POST/GET | `unidade/sic/{listar,id,ativar,desativar}`, `GET unidade/subordinadasSIC` | unidades |
| POST | `acesso-informacao/feriado` (lista), `.../get-feriado-por-id`, `.../gravar-feriado` | feriados |

## Inferências e limitações
- 🔶 `notificacao/omissao-resposta-cgdf/registrar-resposta` e `.../registrar-decisao` constam no backend (`4901ad5`) como "sem atributo" de autorização; o front os expõe sob `RPP_NOR`/`DCS_NOR`. Convém confirmar no backend. Ver [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Endpoints-SIC|Endpoints-SIC]].
- 🔶 O limite de corpo do backend para os endpoints de anexo é "audit 40MB"; o `nginx` do front limita a **25M** e o front a 25 MB de arquivos somados, mas o conteúdo vai em base64 (~33% maior). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]].
- ❓ Payloads, nomes de propriedades (inclusive o erro de grafia `prorragacaoPrazo` apenas interno) e códigos de retorno não conferidos com os controllers.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Caixa-de-Entrada-e-Detalhamento|Caixa de entrada]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Registro-por-Operador|Registro por operador]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Gerencial|Gerencial]] · Equivalente: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas de API do Frontend Ouvidoria]]

## Pendências e próximo passo
- Confrontar payloads e códigos de retorno com os controllers do backend. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
