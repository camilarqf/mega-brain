---
type: reference
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - rotas
  - telas
sources:
  - app/app.routes.js
  - index.html
  - app/nav/nav-ctrl.js
  - app/caixa-entrada
  - app/registro/por-operador
  - app/conta
  - app/gerencial
  - app/super-busca
---

# Frontend SIC — rotas e telas

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Arquitetura: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Arquitetura|Arquitetura]]

## Objetivo
Catálogo das rotas de `app/app.routes.js` e do controller/template de cada uma.

## Evidências
`app/app.routes.js` (commit `5518a81`): **23 rotas** `when(...)` + `otherwise → '/'`. Rotas por hash (`#/...`).

## Informações confirmadas
| Rota | Controller | Template | Detalhe |
|---|---|---|---|
| `/`, `/caixa-entrada` | `caixaEntradaUnidadeCtrl` | `caixa-entrada/caixa-entrada-unidade.html` | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Caixa-de-Entrada-e-Detalhamento\|Caixa de entrada]] |
| `/detalhar-pedido/:id` | `detalhamentoPedidoCtrl` | `caixa-entrada/detalhamento-pedido.html` | idem |
| `/super-busca` | `superBuscaCtrl` | `super-busca/super-busca.html` | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Super-Busca\|Super-busca]] |
| `/pedidoPorOperador` | `pedidoPorOperadorCtrl` | `registro/por-operador/pedido-por-operador.html` | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Registro-por-Operador\|Registro por operador]] |
| `/pedidoPorOperador/registrar/:usuarioId` | `registrarPedidoPorOperadorCtrl` | `.../registrar-pedido-por-operador.html` | idem |
| `/pedidoPorOperador/finalizar/:lote?` | `finalizarPedidoPorOperadorCtrl` | `.../finalizar-pedido-por-operador.html` | idem |
| `/cadastrar-pessoa-fisica/:nomeUsuario/:dataNascimentoUsuario/:nomeMaeUsuario/:cpf/:returnRoute?` | `cadastrarPessoaFisicaCtrl` | `conta/pessoa-fisica/cadastrar-pessoa-fisica.html` | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Conta-por-Operador\|Conta por operador]] |
| `/atualizar-pessoa-fisica/:id/:returnRoute?` | `atualizarCadastroPessoaFisicaCtrl` | `.../atualizar-cadastro-pessoa-fisica.html` | idem |
| `/cadastrar-pessoa-juridica/:razaoSocial/:nomeFantasia?/:tipoEntidade/:cnpj/:cpfVinculado/:returnRoute?` | `cadastrarPessoaJuridicaCtrl` | `conta/pessoa-juridica/cadastrar-pessoa-juridica.html` | idem |
| `/atualizar-pessoa-juridica/:id/:returnRoute?` | `atualizarCadastroPessoaJuridicaCtrl` | `.../atualizar-cadastro-pessoa-juridica.html` | idem |
| `/feriado`, `/feriado/:id` | `gridFeriadoCtrl`, `formFeriadoCtrl` | `gerencial/feriado/*` | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Gerencial\|Gerencial]] |
| `/perfil`, `/perfil/:id` | `gridPerfilCtrl`, `formPerfilCtrl` | `gerencial/perfilSIC/*` | idem |
| `/operador`, `/operador/:id` | `gridOperadorCtrl`, `formOperadorCtrl` | `gerencial/operadorSIC/*` | idem |
| `/alterar-cadastro-operador/:id` | `alterarCadastroOperadorCtrl` | `gerencial/operadorSIC/alterarCadastroOperador.html` | idem |
| `/unidade`, `/unidade/:id` | `gridUnidadeCtrl`, `formUnidadeCtrl` | `gerencial/unidade/*` | idem |
| `/auth/:sessionId` | `authCtrl` | `auth/auth.html` | [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Autenticacao\|Autenticação]] |
| `/acesso-negado` | `acessoNegadoCtrl` | `acesso-negado/acesso-negado.html` | página estática |
| `/bloquear-usuario` | `bloqueioUsuarioCtrl` | `conta/bloqueio-usuario.html` | ❌ **controller e template inexistentes** no repositório |

### Observações
- ✅ `visualizarContaCtrl` (`conta/visualizar-conta`) existe, mas **não tem rota**.
- ✅ Menu principal (`index.html`): **Novo Pedido** (`/pedidoPorOperador`), **Super-busca**, **Caixa de entrada**, **Gerenciar** (itens vindos do backend, `/#/<URL>`), menu do usuário (**Trocar unidade** em modal, **Sair**). Itens visíveis só com `vm.isAuth`; **Gerenciar** só com `vm.permissoes.GerenciarSistema`.
- ✅ As rotas de pessoa física/jurídica carregam **dados do cidadão no caminho** (nome, nome da mãe, data de nascimento com `|` no lugar de `/`, CPF, razão social, CNPJ com `|` no lugar de `/`). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/08-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]].

## Inferências e limitações
- 🔶 A rota `/bloquear-usuario` e a referência `app/conta/bloqueio-usuario.html` parecem herdadas do front de Ouvidoria (mesmo achado em [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências do Frontend Ouvidoria]]).
- Templates lidos só por amostra; o conteúdo de cada tela não foi detalhado.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Remover ou implementar `/bloquear-usuario`; decidir se `visualizar-conta` deve ter rota. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
