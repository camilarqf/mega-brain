---
type: reference
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
tags:
  - participa-df
  - frontend-ouvidoria
  - rotas
  - telas
sources:
  - app/app.routes.js
  - app/nav/nav-ctrl.js
  - index.html
---

# Frontend Ouvidoria — rotas e telas

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Arquitetura: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Arquitetura|Arquitetura]]

## Objetivo
Catalogar as rotas `ngRoute` (modo hash, `hashPrefix('')`) e relacionar cada uma à tela e ao controller, destacando rotas com problema.

## Evidências
`app/app.routes.js` e verificação da existência dos `templateUrl` e controllers no repositório, commit `9d8ecdb`. `otherwise` redireciona para `/`. Nenhuma rota tem `resolve` nem guarda de acesso.

## Informações confirmadas

### Manifestações
| Rota | Controller | Tela | Nota |
|---|---|---|---|
| `/` | `caixaDeEntradaCtrl` | caixa de entrada | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Caixa-de-Entrada-e-Detalhamento|Fluxo]] |
| `/detalhar-manifestacao/:id` | `detalheManifestacaoCtrl` | detalhe e tratamento | idem |
| `/prorrogacao-prazo` | `prorrogacaoDePrazoCtrl` | solicitações de prorrogação | [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Prorrogacao-de-Prazo|Fluxo]] |
| `/super-busca` | `superBuscaCtrl` | busca por termo | caixa de entrada |
| `/painel-avaliacao` | `painelAvaliacaoCtrl` | avaliação/pesquisa de satisfação | ⚠️ depende de serviços não definidos |
| `/exportar-pdf/:id` | `visualizacaoImpressaoCtrl` | impressão (`exportar-pdf-operador.html`, 143 bytes) | ⚠️ depende de `manifestacaoAPI` não definido |
| `/acesso-negado` | `acessoNegadoCtrl` | aviso de acesso negado | — |

### Registro por operador
| Rota | Controller |
|---|---|
| `/manifestacaoPorOperador` | `manifestacaoPorOperadorCtrl` (identificação do manifestante) |
| `/manifestacaoPorOperador/registrar` e `/registrar/:usuarioId` | `registrarManifestacaoPorOperadorCtrl` |
| `/manifestacaoPorOperador/finalizar/:id?` | `finalizarManifestacaoPorOperadorCtrl` |

Detalhe em [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Registro-por-Operador|Fluxo-Registro-por-Operador]].

### Conta do manifestante (feita pelo operador)
`/cadastrar-pessoa-fisica/:nomeUsuario/:dataNascimentoUsuario/:nomeMaeUsuario/:cpf/:returnRoute?`, `/atualizar-pessoa-fisica/:id/:returnRoute?`, `/cadastrar-pessoa-juridica/:razaoSocial/:nomeFantasia?/:tipoEntidade/:cnpj/:cpfVinculado/:returnRoute?`, `/atualizar-pessoa-juridica/:id/:returnRoute?`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Conta-por-Operador|Modulo-Conta-por-Operador]].

⚠️ Os dados pessoais (nome, nome da mãe, data de nascimento, CPF) trafegam **na URL** nessas rotas de cadastro.

### Gerencial
`/assunto`, `/assunto/:id`, `/usuario`, `/usuario/:id`, `/alterar-cadastro-usuario/:id`, `/unidade`, `/unidade/:id`, `/perfil`, `/perfil/:id`, `/formulario`, `/formulario/:id`, `/bloquear-usuario`, `/listaDeNotificacao`, `/criarFormulario`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Gerencial|Modulo-Gerencial]]. O menu "Gerenciar" é montado a partir de `PermissoesDeGerenciamento[].URL` devolvido pelo backend.

### Dashboards e autenticação
- `/dashboard/rel_operacoes_de_atendente`, `/dashboard/rel_operacoes_unidade` ([[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Dashboards-e-Relatorios|Dashboards]]).
- `/auth/:sessionId` → `authCtrl` ([[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Autenticacao|Fluxo-Autenticacao]]).

### Menu (`index.html`, `navCtrl`)
Itens: Nova Manifestação (`/manifestacaoPorOperador`), caixa de entrada, super busca (permissão `PesquisarManifestacao`), Produtividade por operador e por unidade (`VisualizarPaineis`), Gerenciar (`GerenciarSistema`), e o menu do usuário com "Trocar Unidade" e "Sair".

## Rotas com problema (verificadas)
| Rota | Problema |
|---|---|
| `/bloquear-usuario` | registrada **duas vezes**: a primeira aponta para `app/conta/bloqueio-usuario.html`, que não existe; a segunda, para `app/gerencial/bloqueio-usuario/bloqueio-usuario.html`. 🔶 No `ngRoute` a última definição prevalece (não executado). |
| `/listaDeNotificacao` | `templateUrl` `lista-notificacao-de-prazo.html` não existe (o arquivo existente é `lista-de-notificacao-de-prazo.html`) e o controller `navegacaoCtrl` não está definido. |
| `/criarFormulario` | `cadastrar-formulario.html` e `criarFormularioCtrl` não existem. |
| `/painel-avaliacao`, `/exportar-pdf/:id` | controllers injetam `avaliacaoPorOperadorAPI`, `manifestacaoAPI`, `questionarioAPI`, que não são definidos em nenhum arquivo do repositório. |
| `grid-prazo`/`form-prazo` | controllers e templates existem, mas **nenhuma rota** os usa (idem `perfilCtrl`, `unidadeCtrl`, `usuarioCtrl`, `questionarioCtrl`, `loginCtrl`, `rel_*` exceto 2). |

## Inferências e limitações
- 🔶 As rotas com problema podem estar mortas ou servidas por outra versão do código; não foi executada a aplicação. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas-de-API]]

## Pendências e próximo passo
- Confirmar com o time quais telas estão em uso em produção. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
