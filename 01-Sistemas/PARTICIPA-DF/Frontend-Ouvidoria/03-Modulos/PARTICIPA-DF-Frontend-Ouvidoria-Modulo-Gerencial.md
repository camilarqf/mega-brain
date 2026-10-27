---
type: module
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
tags:
  - participa-df
  - frontend-ouvidoria
  - modulo
  - gerencial
  - cadastros
sources:
  - app/gerencial/assunto
  - app/gerencial/formulario
  - app/gerencial/operador
  - app/gerencial/perfil
  - app/gerencial/unidade
  - app/gerencial/notificacao-de-prazo
  - app/gerencial/bloqueio-usuario
  - app/app.routes.js
---

# Frontend Ouvidoria — módulo gerencial

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Rotas: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Rotas-e-Telas|Rotas-e-Telas]]

## Objetivo
Documentar as telas de cadastro e administração usadas por quem tem a permissão `GerenciarSistema`: assuntos, formulários de atributos complementares, usuários (operadores), perfis, unidades, prazos de notificação e bloqueio de usuário.

## Evidências
Arquivos em `sources`, commit `9d8ecdb`. Cobertura `parcial`: os `.html` (formulários) foram verificados só quanto à existência; os controllers de lista/cadastro foram lidos.

## Informações confirmadas

### Padrão das telas
Lista (`grid-*`) + formulário (`form-*`): a lista faz `POST <recurso>/listar` com `PageNumber` e `FiltroAplicado`, mostra colunas fixas e `onDetail(id)` navega ao formulário; o formulário carrega por `POST <recurso>/id` e salva por `POST <recurso>` (sem `PUT`/`DELETE`). Em salvamento bem-sucedido: `toastr` "Operação executada com sucesso" e volta à lista.

| Cadastro | Rotas | Endpoints (backend) | Particularidades |
|---|---|---|---|
| Assunto | `/assunto`, `/assunto/:id` | `servico-ouvidoria/assunto` (`/listar`, `/id`); combos `colecoes/tema`, `unidade/subordinadasSO`, `classificacao` | colunas: Descrição, Unidade de Trâmite Inicial, Ativo |
| Formulário (atributos complementares) | `/formulario`, `/formulario/:id` | `servico-ouvidoria/formulario` (`/listar`, `/id`); combos `assunto/sem-formulario`, `formulario/formato` | um formulário por assunto (combo só oferece assuntos **sem** formulário); cada atributo tem `Formato`, `Mascara`, `Comprimento`, `Bloquear` |
| Usuário (operador) | `/usuario`, `/usuario/:id`, `/alterar-cadastro-usuario/:id` | `operador-so` (`/listar`, `/id`, `/existe`); combos `unidade/subordinadasSO`, `perfil-so/ativos` | cadastro novo parte do **CPF**: se já é operador, erro; senão exige PF cadastrada (`pessoa-fisica/existe`) e carrega `usuario/id`; um operador tem várias unidades e perfil |
| Perfil | `/perfil`, `/perfil/:id` | `perfil-so` (`/listar`, `/id`); combo `perfil-so/funcionalidade` | funcionalidades definem as permissões do menu |
| Unidade | `/unidade`, `/unidade/:id` | `unidade/so` (`/listar`, `/id`); combos `unidade/subordinadasSO`, `unidade/so/tipo-unidade` | hierarquia por unidade superior |
| Bloqueio de usuário | `/bloquear-usuario` | `usuario/id`, `usuario/bloquear`, `usuario/desbloquear`, `usuario/motivacao-bloqueio-usuario` | consulta por CPF/CNPJ; bloquear/desbloquear exige o objeto de bloqueio e a motivação |
| Notificação de prazo | **sem rota efetiva** | `notificacao`, `notificacoes`, `acao-para-remover-notificacao` | `gridPrazoCtrl`/`formPrazoCtrl` existem mas não são alcançáveis; `/listaDeNotificacao` está quebrada (ver rotas) |

### Regras observadas no frontend
- ✅ **Formato de atributo → máscara/comprimento** (`form-formulario-ctrl.js`): `Data` → máscara `99/99/9999`, comprimento 10, `Bloquear = true`; `Hora` → `99:99`, 5, `Bloquear = true`; `Texto_com_mascara` → máscara numérica de 11 posições (padrão), comprimento 255, `Bloquear = false`; `Verdadeiro_ou_Falso` → sem máscara nem comprimento; `TextoSimples` → comprimento 255, `Bloquear = true`. O significado de `Bloquear` (campo bloqueado após preenchido? 🔶) não está no controller.
- ✅ Um novo atributo recebe `Id` temporário aleatório (`Math.floor(Math.random()*100)+10000`) para edição na lista antes de salvar.
- ✅ Operador **bloqueado** não pode ser editado (erro "Edição não permitida para usuário bloqueado").
- ✅ Menu "Gerenciar" é gerado por `PermissoesDeGerenciamento` do backend (cada item traz `URL` e `DescricaoFuncionalidade`); o frontend não decide quais cadastros existem.
- ✅ Trocar de unidade (`alternarUnidade`) recarrega as listas dependentes da unidade ativa (ex.: `unidadeCtrl`).

## Inferências e limitações
- 🔶 `perfilCtrl`, `unidadeCtrl` e `notificacoesDePrazoCtrl` são versões antigas (com `$scope` e serviços `perfilAPI`, `unidadeAPI`, `notificacaoDePrazoAPI` que **não existem** no repositório); as telas efetivas são os `grid-*`/`form-*`.
- ❓ Quais funcionalidades existem em `perfil-so/funcionalidade` e o mapeamento para as permissões do menu (`GerenciarSistema` etc.) estão no backend.

## Relacionamentos
- Backend: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas-de-API]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Registro-por-Operador|Registro-por-Operador]] (usa assuntos e formulários) · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/08-Seguranca/PARTICIPA-DF-Frontend-Ouvidoria-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Pendências e próximo passo
- Confirmar o uso e a rota da notificação de prazo e o sentido de `Bloquear`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
