---
type: module
aliases:
  - "Frontend SIC — módulo gerencial"
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
sources:
  - app/gerencial/operadorSIC/grid-operador.ctrl.js
  - app/gerencial/operadorSIC/form-operador.ctrl.js
  - app/gerencial/operadorSIC/alterarCadastroOperadorCtrl.js
  - app/gerencial/perfilSIC/grid-perfil.ctrl.js
  - app/gerencial/perfilSIC/form-perfil.ctrl.js
  - app/gerencial/unidade/grid-unidade.ctrl.js
  - app/gerencial/unidade/form-unidade.ctrl.js
  - app/gerencial/feriado/grid-feriado.ctrl.js
  - app/gerencial/feriado/form-feriado.ctrl.js
  - app/nav/nav-ctrl.js
---

# Frontend SIC — módulo gerencial

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Rotas: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Rotas-e-Telas|Rotas-e-Telas]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Modulo-Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]]

## Objetivo
Documentar o CRUD de operadores, perfis, unidades e feriados do SIC.

## Evidências
Arquivos em `sources`, commit `5518a81`. Os itens do menu "Gerenciar" vêm do backend (`PermissoesDeGerenciamento`); o front só os lista.

## Informações confirmadas
Padrão comum: tela de listagem (`grid-*`) com filtros, paginação por `PageNumber` e `FiltroAplicado`, e tela de formulário (`form-*`); sucesso mostra `toastr` ("ParticipaDF") e volta à listagem.

### Operadores (`/operador`, `/operador/:id`, `/alterar-cadastro-operador/:id`)
- ✅ Listagem: `POST operador-sic` (filtros: nome, ativo, unidade, CPF); colunas Nome, CPF, Perfil, Unidade Atual, Ativo. `id == 0` abre cadastro novo; outro `id` abre `alterar-cadastro-operador`. Unidades do filtro: `GET unidade/subordinadasSIC`.
- ✅ Cadastro (`formOperadorCtrl`): o operador informa o CPF.
  1. `GET operador-sic/operador-existe?cpf=`; se já existe, `POST operador-sic/consultar-por-cpf` e exibe erro "Operador cadastrado na unidade: … Contate a ouvidoria geral".
  2. Se não existe, `POST pessoa-fisica/por-cpf` busca a pessoa; `404` permite cadastrar nova pessoa (`PessoaFisica = {CPF, Unidades:[]}`).
  3. Escolhe-se **perfil** (`GET acesso-informacao/perfil-sic/ativos`), **unidades** (`GET unidade/subordinadasSIC`) e a unidade atual; `POST operador-sic/cadastrar` com `{Perfil, Unidades, UnidadeAtual, PessoaFisica}`.
  4. Se o usuário logado **não** está em unidade superior do SIC (`Permissoes.IsUnidadeAtualSuperioSic == false`), a unidade atual passa a ser a primeira unidade adicionada, e remover uma unidade zera a atual.
- ✅ Alteração (`alterarCadastroOperadorCtrl`): `POST operador-sic/consultar-por-id` (se falhar, `visualizacaoPermitida=false`); `POST operador-sic/atualizar` (`Id, Perfil, Unidades, UnidadeAtual, Ativo`); `POST operador-sic/ativar` e `operador-sic/desativar` (`{Operador:{Id}}`).

### Perfis (`/perfil`, `/perfil/:id`)
- ✅ Listagem: `POST acesso-informacao/perfil-sic/get-perfis`. Cadastro/edição: `POST acesso-informacao/perfil-sic/` (grava) e `POST .../get-perfil-por-id`; as funcionalidades selecionáveis vêm de `GET acesso-informacao/perfil-sic/funcionalidade`.

### Unidades (`/unidade`, `/unidade/:id`)
- ✅ Listagem: `POST unidade/sic/listar` (descrição, ativo). Na tela de formulário, `id == 0` lista as unidades **ainda não ativas no módulo SIC** (`POST unidade/ouvidorias-ativas` com `{AtivoModuloSIC:false}`) para ativar uma delas; outro `id` carrega `POST unidade/sic/id`. Ativar: `POST unidade/sic/ativar`; desativar: `POST unidade/sic/desativar` (`{Unidade:{Id}}`). Não há criação de unidade, só ativação/desativação do módulo SIC em unidades já existentes.

### Feriados (`/feriado`, `/feriado/:id`)
- ✅ Listagem: `POST acesso-informacao/feriado/`; edição: `POST .../get-feriado-por-id` e `POST .../gravar-feriado`. Um feriado sem `Ano` é **recorrente** (caixa "ano recorrente" limpa o ano). A data exibida usa `Dia`, `Mes` e `Ano` (o ano corrente quando recorrente).
- 🔶 Os feriados alimentam o cálculo de prazos de pedidos (ver [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Prazo-do-SIC|Regras-de-Prazo-do-SIC]]), que é feito no backend.

## Inferências e limitações
- ✅ `grid-perfil` transforma `Ativo == false` em `null` antes de filtrar, então não é possível filtrar apenas perfis inativos.
- ✅ `gridUnidadeCtrl` define `getDataUnidade` (cópia de `getDataFeriado`, que monta a data de um feriado); parece resíduo de cópia.
- 🔶 `gridFeriadoCtrl` declara `Ativo` no filtro, mas as colunas exibidas são só Descrição e Data.
- ❓ Perfis/funcionalidades concretas e as regras de autorização por perfil estão no backend.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/08-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]] · Equivalente: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Gerencial|Gerencial do Frontend Ouvidoria]]

## Pendências e próximo passo
- Conferir no backend o efeito de `IsUnidadeAtualSuperioSic` e as funcionalidades de cada perfil. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
