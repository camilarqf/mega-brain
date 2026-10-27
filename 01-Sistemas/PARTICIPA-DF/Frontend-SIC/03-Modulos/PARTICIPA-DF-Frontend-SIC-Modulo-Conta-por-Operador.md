---
type: module
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - modulo
  - conta
  - pessoa-fisica
  - pessoa-juridica
sources:
  - app/conta/pessoa-fisica/cadastrar-pessoa-fisica-ctrl.js
  - app/conta/pessoa-fisica/atualizar-cadastro-pessoa-fisica.js
  - app/conta/pessoa-juridica/cadastrar-pessoa-juridica-ctrl.js
  - app/conta/pessoa-juridica/atualizar-cadastro-pessoa-juridica-ctrl.js
  - app/conta/visualizar-conta/visualizar-contra-ctrl.js
  - app/app.routes.js
---

# Frontend SIC — conta do solicitante por operador

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Fluxo de origem: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Registro-por-Operador|Fluxo-Registro-por-Operador]]

## Objetivo
Documentar o cadastro e a atualização de contas de pessoa física (PF) e jurídica (PJ) feitos pelo operador do SIC em nome do solicitante.

## Evidências
Arquivos em `sources`, commit `5518a81`. Os formulários `.html` não foram detalhados campo a campo.

## Informações confirmadas

### Pessoa física
- ✅ **Cadastro** (`cadastrarPessoaFisicaCtrl`): recebe, pela rota, nome, nome da mãe, data de nascimento (`|` → `/`) e CPF (dados que vieram do desafio de identidade) e `returnRoute`. Carrega `GET necessidade-especial` (padrão: primeiro item). `salvar` → `POST pessoa-fisica/por-operador`; em sucesso mostra a confirmação e permite seguir para `/pedidoPorOperador/registrar/{Id}`; em 400 rola ao topo.
- ✅ **Atualização** (`atualizarCadastroPessoaFisicaCtrl`): `POST usuario/id` (junta `Usuario` e `PessoaFisica`, formata a data `dd/MM/yyyy`) e `POST pessoa-fisica/atualizar/por-operador`; mostra "Dados atualizados com sucesso" e volta a `returnRoute` decodificado. O tipo de telefone é inferido pelo tamanho: **13 caracteres → comercial**, senão celular.

### Pessoa jurídica
- ✅ **Cadastro** (`cadastrarPessoaJuridicaCtrl`): recebe razão social, nome fantasia, tipo de entidade, CNPJ (`|` → `/`) e CPF vinculado; `AceiteDeclaracaoResponsabilidade` já vai como `true`. Carrega `GET pessoa-juridica/tipo-entidade`. `salvar` → `POST pessoa-juridica/por-operador`.
- ✅ **Atualização** (`atualizarCadastroPessoaJuridicaCtrl`): `usuario/id` + `POST pessoa-juridica/atualizar/por-operador`. Em três etapas (`AtualizarPJ`, `ValidarCpf`, `Desafio`) permite **alterar o CPF vinculado**: consulta tentativas (`security/count-try`), valida o CPF e o aceite (`security/check-cpf-vinculado-pj`) e resolve o desafio (`security/challenge`); só depois grava o novo vínculo (`pessoa-juridica/atualizar-responsavel`).

### Visualização
- ✅ `visualizarContaCtrl` (`usuario/id`) existe, mas **não há rota** que a use.

## Inferências e limitações
- 🔶 O número de tentativas de desafio é por documento, controlado no backend (`security/count-try`); o front apenas exibe o resultado.
- ✅ Defeitos em `atualizarCadastroPessoaJuridicaCtrl` (ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/09-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]]): (1) após erro de desafio, a consulta de tentativas usa `extrairCaracteres(vm.cpf)`, mas `vm.cpf` **não é definido** no controller (o CPF está em `vm.cpfVinculado`), o que lança `TypeError` ao chamar `.replace`; (2) `tentativasEsgotadasFim` usa `$ngConfirm`, que **não está injetado** no controller (assinatura: `$routeParams, $location, toastr, Api`), gerando `ReferenceError` ao esgotar as tentativas.
- ❓ Validações de campos (máscaras, obrigatoriedade) estão nos templates e nas diretivas `dir*Form`; não analisadas.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/08-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]] (dados pessoais na URL) · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]] · Equivalente: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Conta-por-Operador|Conta por operador na Ouvidoria]]

## Pendências e próximo passo
- Ler os templates de conta e as diretivas `shared/` (lote 6 sugerido). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
