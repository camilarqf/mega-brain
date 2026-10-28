---
type: flow
aliases:
  - "Frontend SIC — registro de pedido por operador"
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - app/registro/por-operador/pedido-por-operadorCtrl.js
  - app/registro/por-operador/pedido-por-operador.html
  - app/registro/por-operador/registrar-pedido-por-operador-ctrl.js
  - app/registro/por-operador/registrar-pedido-por-operador.html
  - app/registro/por-operador/finalizar-pedido-por-operador.js
  - app/upload/upload-arquivos-directive.js
  - app/app.routes.js
---

# Frontend SIC — registro de pedido por operador

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Conta: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Conta-por-Operador|Conta-por-Operador]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Pedido|Fluxo-Registro-de-Pedido]]

## Objetivo
Descrever como o operador registra um pedido de acesso à informação em nome de um cidadão (pessoa física ou jurídica), incluindo a identificação e a verificação de identidade.

## Evidências
Arquivos em `sources`, commit `5518a81`. As telas foram lidas só pelo controller e pelos títulos de etapa.

## Informações confirmadas

### Identificação do solicitante (`/pedidoPorOperador`, 7 etapas)
| Etapa | Conteúdo | Chamadas |
|---|---|---|
| 1 | escolher **Pessoa Física** ou **Pessoa Jurídica** | — |
| 2 | informar CPF ou CNPJ | PF: `pessoa-fisica/existe`; PJ: `security/check` + `pessoa-juridica/existe` |
| 3 | 🔶 mensagem de bloqueio/falha ("Atenção"), exibida quando `security/check` falha | — |
| 4 | PF encontrada: dados e opções (registrar pedido, editar cadastro) | `usuario/id` |
| 5 | PJ encontrada: dados, histórico de CPF vinculado | `usuario/id`, `pessoa-juridica/historico-responsavel-por-operador` |
| 6 | **desafio** de identidade (2 perguntas + data) | `security/check`, `security/challenge`, `security/check-cpf-vinculado-pj` |
| 7 | não encontrado: iniciar cadastro | — |

Regras observadas:
1. ✅ **Tentativas**: antes do desafio, `security/count-try?data=<documento>`; se `> 2`, mostra "Você ultrapassou o número de tentativas permitidas… volte em 24 horas" e volta à raiz. Após cada erro de desafio o contador é consultado de novo.
2. ✅ **Desafio** (`security/check` devolve `responseChallenge` com `id` e `steps`): o front monta máscaras pelo tamanho dos dois primeiros itens e envia `{challenge:{id, keys:[pergunta1, pergunta2, data]}}` para `security/challenge`; a resposta traz os dados oficiais (`keys`) usados para pré-preencher o cadastro.
3. ✅ **Cinco fluxos** (`fluxoDesafioEnum`): criação de conta PF (0), desbloqueio de conta PF (1), criação de conta PJ (2), desbloqueio de conta PJ (3), alteração de CPF vinculado da PJ (4).
4. ✅ **Conta bloqueada**: `usuario/id` com `BloqueioUsuario.Motivacao.Id == 1` leva ao desbloqueio de PF; `== 5` marca "dados inconsistentes" e leva ao desbloqueio de PJ (CNPJ divergente da Receita Federal, texto da tela), com `pessoa-fisica/desbloquear-dados-inconsistentes` / `pessoa-juridica/desbloquear-dados-inconsistentes`. O significado dos ids 1 e 5 é 🔶 inferido dos textos.
5. ✅ **PJ**: exige o CPF do responsável e o aceite de declaração de responsabilidade (`security/check-cpf-vinculado-pj`, parâmetro `aceiteResponsabilidade`).
6. ✅ Para cidadão novo, vai ao cadastro (`/cadastrar-pessoa-fisica/...` ou `/cadastrar-pessoa-juridica/...`) com `returnRoute=pedidoPorOperador/registrar/`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/03-Modulos/PARTICIPA-DF-Frontend-SIC-Modulo-Conta-por-Operador|Conta-por-Operador]].

### Registro do pedido (`/pedidoPorOperador/registrar/:usuarioId`)
1. ✅ Carrega o solicitante (`usuario/id`), os assuntos (`GET acesso-informacao/assunto`) e as unidades (`POST unidade/ouvidorias-ativas` com `{AtivoModuloSIC: true}`).
2. ✅ O operador preenche o pedido (unidade, assunto, texto) e anexa arquivos (`uplArquivos`: ≤ 25 MB somados, validação por `arquivo/validar`, conteúdo em base64 no JSON).
3. ✅ `POST acesso-informacao/pedido/por-operador` → em sucesso navega para `/pedidoPorOperador/finalizar/{Lote}`; em 400 rola ao topo para mostrar os erros.

### Finalização (`/pedidoPorOperador/finalizar/:lote?`)
- ✅ `POST acesso-informacao/pedido/consultar-por-lote` (`{Lote}`) lista os pedidos criados (um registro pode gerar mais de um pedido; 🔶 provavelmente um por unidade escolhida).

## Inferências e limitações
- 🔶 O desafio é a validação de identidade do cidadão; sua origem de dados (`security/*` → `PeoplesCheck` no backend) está em [[Mapa-de-Integracoes|Mapa de integrações]].
- ✅ `pesquisarCnpj` chama `pessoa-juridica/existe` **duas vezes** (dentro e fora do retorno de `security/check`), duplicando a requisição e o tratamento; em caso de falha em `security/check`, a segunda chamada ainda ocorre.
- ✅ `desbloquearPorDadosInconsistentes` e `desbloquearPFPorDadosInconsistentes` fazem a mesma coisa.
- ❓ O texto completo das etapas 3 a 7 e do formulário de pedido não foi lido linha a linha.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/08-Seguranca/PARTICIPA-DF-Frontend-SIC-Seguranca-e-Sessao|Seguranca-e-Sessao]] · Equivalente: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Registro-por-Operador|Registro por operador na Ouvidoria]]

## Pendências e próximo passo
- Ler os templates das etapas 3 a 7 e confrontar `security/*` com o backend. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
