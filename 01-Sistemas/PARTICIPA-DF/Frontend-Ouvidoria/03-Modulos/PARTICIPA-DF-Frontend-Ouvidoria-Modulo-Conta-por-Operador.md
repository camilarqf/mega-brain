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
  - conta
  - pessoa-fisica
  - pessoa-juridica
sources:
  - app/conta/pessoa-fisica
  - app/conta/pessoa-juridica
  - app/conta/visualizar-conta
  - app/manifestacao/registro/por-operador/manifestacao-por-operadorCtrl.js
  - app/app.routes.js
---

# Frontend Ouvidoria — conta do manifestante feita por operador

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Origem: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Registro-por-Operador|Registro-por-Operador]] · Equivalente do cidadão: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Cadastro-de-Conta|Cadastro-de-Conta (Cidadão)]]

## Objetivo
Documentar o cadastro e a atualização de contas de pessoa física (PF) e jurídica (PJ) feitos pelo operador durante o atendimento.

## Evidências
Arquivos em `sources`, commit `9d8ecdb`. Cobertura `parcial`: lidos os controllers de cadastro PF, atualização PF e atualização PJ; templates não lidos campo a campo.

## Informações confirmadas

| Operação | Rota | Controller | Chamada |
|---|---|---|---|
| Cadastrar PF | `/cadastrar-pessoa-fisica/:nomeUsuario/:dataNascimentoUsuario/:nomeMaeUsuario/:cpf/:returnRoute?` | `cadastrarPessoaFisicaCtrl` | `POST pessoa-fisica/por-operador` |
| Atualizar PF | `/atualizar-pessoa-fisica/:id/:returnRoute?` | `atualizarCadastroPessoaFisicaCtrl` | `POST usuario/id`; `POST pessoa-fisica/atualizar/por-operador` |
| Cadastrar PJ | `/cadastrar-pessoa-juridica/:razaoSocial/:nomeFantasia?/:tipoEntidade/:cnpj/:cpfVinculado/:returnRoute?` | `cadastrarPessoaJuridicaCtrl` | `POST pessoa-juridica/por-operador` |
| Atualizar PJ | `/atualizar-pessoa-juridica/:id/:returnRoute?` | `atualizarCadastroPessoaJuridicaCtrl` | `POST usuario/id`; `POST pessoa-juridica/atualizar/por-operador`; `POST pessoa-juridica/atualizar-responsavel`; `GET pessoa-juridica/tipo-entidade` |

- ✅ **Dados que vêm do desafio** (nome, nome da mãe, data de nascimento, CPF; razão social, nome fantasia, tipo de entidade, CNPJ, CPF vinculado) chegam como **parâmetros de rota**, com `|` no lugar de `/` (data e CNPJ). O campo fica pré-preenchido; ver o risco de PII na URL em [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/08-Seguranca/PARTICIPA-DF-Frontend-Ouvidoria-Seguranca-e-Sessao|Seguranca-e-Sessao]].
- ✅ Combo de necessidade especial: `GET necessidade-especial` (o primeiro item é o padrão).
- ✅ **Tipo de telefone**: o controller deduz `comercial` quando o telefone tem 13 caracteres e `celular` caso contrário; trocar o tipo limpa o campo.
- ✅ Após cadastrar PF, o operador pode seguir ao registro de manifestação com `/manifestacaoPorOperador/registrar/{Id}`.
- ✅ **Atualização de PJ — troca de CPF vinculado** (etapas `AtualizarPJ`, `ValidarCpf`, `Desafio`): exige validar o CPF novo (`security/check-cpf-vinculado-pj`), aceitar a declaração de responsabilidade e passar pelo desafio, com limite de tentativas igual ao do registro. Atualizar responsável: `pessoa-juridica/atualizar-responsavel`.
- ✅ Retorno: `returnRoute` (URL codificada) leva o operador de volta à tela de origem após salvar.
- ✅ `400` do backend rola a tela ao topo para exibir `customException`.
- ❓ `visualizar-conta` (`visualizarContaCtrl`) existe mas não tem rota.

## Inferências e limitações
- 🔶 O frontend não valida CPF/CNPJ por algoritmo nos controllers lidos; a verificação acontece no backend (`security/check`).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas-de-API]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario|Bloqueio-de-Usuario]]

## Pendências e próximo passo
- Ler os templates de conta (campos e máscaras). Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
