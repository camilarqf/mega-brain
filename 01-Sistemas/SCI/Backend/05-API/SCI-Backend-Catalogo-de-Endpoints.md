---
type: api
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - backend
  - api
  - endpoints
sources:
  - src/SCI.Api/Controllers
  - src/SCI.Api/Identity/AuthorizationPolicies
---
# SCI Backend — catálogo de endpoints

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Listar os 33 controllers REST, rotas, verbos e a exigência de autorização (política = nome curto; perfis em [[01-Sistemas/SCI/Backend/06-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança e autorização]]).

## Evidências
- Atributos `[Route]`, `[Http*]` e `[Authorize]` em `src/SCI.Api/Controllers/*Controller.cs` (142 atributos HTTP). Payloads e códigos de resposta **não detalhados** (cobertura parcial); pastas `Requests/` e `Responses/` não lidas por completo.
- Legenda: **A** = só autenticação (`[Authorize]` no controller); **P:nome** = política; **anon** = anônimo.

## Informações confirmadas
### Segurança e suporte
| Rota | Acesso |
|---|---|
| `POST /security/auth` — autentica por CPF + senha, devolve token do SCI | anon |
| `GET /security/is-auth` | anon |
| `POST /support/generate-database` — recria o banco ([[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Banco-e-Migrations|Banco]]) | anon + `FeatureGate Support.GenerateDatabase` |

### Entrada: denúncia e demanda
| Rota | Acesso |
|---|---|
| `GET /denuncia/get-all` | A |
| `POST /denuncia/aceitar`, `POST /denuncia/recusar` | P:denuncia.* (AutoridadeCorrecional) |
| `GET /demanda/{id}`, `GET /demanda/get-all` | A |
| `GET /demanda/por-admissibilidade` | P:demanda.Listar |
| `POST /demanda`, `PUT /demanda` | P:demanda.Criar / Atualizar |
| `POST /demanda/tratar` | P:demanda.Tratar |
| `POST /demanda/{id}/adicionar-anexo`, `DELETE /demanda/{id}/remover-anexo/{anexoId}` | P:demanda.Atualizar |
| `GET /arquivo/download/{nomeArquivo}`, `GET /arquivo/get-por-demanda` | A |

### Processo de admissibilidade e análise
| Rota | Acesso |
|---|---|
| `GET /processo-admissibilidade/{id}`, `/nota/{id}`, `/por-relator`, `/por-demanda/{demandaId}`, `/nota-tecnica/{processoAdmissibilidadeId}` | A (`/por-relator` e `/unidade` ver política) |
| `GET /processo-admissibilidade/unidade` | P:jad.ListarProcessosPorUnidade |
| `GET /processo-admissibilidade/visao-{gestor,autoridade,assessor-autoridade,analista,apoio,revisor}` | P:jad.VisualizarVisao* (um perfil por visão) |
| `POST distribuir-para-analista`, `POST redistribuir-jad` | P:jad.Distribuir / Redistribuir |
| `PUT /processo-admissibilidade` (atualizar cadastro), `POST reabrir-jad`, `POST concluir-cadastro-jad` | P:jad.GerenciarCadastro |
| `POST assinar-nota-tecnica`, `POST invalidar-nota-tecnica` | P:jad.AssinarNotaTecnica / InvalidarNotaTecnica |
| `POST concluir`, `PUT atualizar-dados-sei` | P:jad.ConcluirProcesso / AtualizarProcessoSei |
| `GET /analise-admissibilidade/{id}`, `GET ""`, `GET /por-pip` | A |
| `PUT /analise-admissibilidade`, `POST /concluir` | P:jad.GerenciarAnalise |
| `POST criar-nota-admissibilidade`, `PUT atualizar-nota-admissibilidade`, `PUT concluir-nota-admissibilidade` | P:jad.*NotaAdmissibilidade (AssessorAutoridade) |
| `POST /revisao-admissibilidade/{concluir-revisao-admissibilidade,reprovar-revisao,atualizar-revisao}` | P:jad.Concluir/Reprovar/AtualizarRevisao |

### Encaminhamento
| Rota | Acesso |
|---|---|
| `GET /encaminhamento/{devolvidos,recebidos,enviados-pela-unidade,por-processo-admissibilidade}` | P:enc.Consultar* |
| `POST /encaminhamento` (encaminhar), `/enviar`, `/reprovar`, `/aceitar`, `/devolver`, `/rejeitar-devolucao` | P:enc.* |

### PIP
| Rota | Acesso |
|---|---|
| `GET /pip/{id}`, `/relatorio/{id}`, `/unidade`, `/por-relator`, `/minuta/{id}`, `/por-processo-admissibilidade/{id}` | A |
| `GET /pip/visao-{revisor,autoridade,assessor-autoridade,apoio,gestor,relator}` | P:pip.VisualizarVisao* |
| `PUT atualizar-cadastro`, `POST concluir-cadastro`, `POST reabrir-pip` | P:pip.GerenciarCadastro |
| `PUT atualizar-minuta`, `POST designar-relatoria`, `POST redistribuir`, `POST concluir-ato-instauracao` | P:pip.* |
| `POST assinar-minuta`, `POST assinar-relatorio`, `POST atualizar-dados-sei` | **A** (perfil validado no domínio) |
| `POST concluir`, `POST finalizar` | P:pip.Concluir / Finalizar |
| `GET /analise-pip/{id}`, `GET /analise-pip/nota/{id}` | A / P:pip.VisualizarNotaByPip |
| `PUT /analise-pip`, `POST concluir`, `POST criar-nota`, `PUT atualizar-nota`, `POST concluir-nota` | P:pip.* |
| `POST /revisao-pip/{concluir,reprovar,atualizar-revisao}` | P:pip.* |
| `POST /diligencia`, `GET por-pip`, `GET {id}`, `PUT`, `POST {id}/vincular-matriz`, `POST {id}/desvincular-matriz` | **A** |

### Organização, identidade e cadastros
| Rota | Acesso |
|---|---|
| `GET /unidade`, `/por-tipo/{id}`, `/has-gestor` | A |
| `GET /unidade/configuracao/{id}`; `POST/PUT /unidade/configuracao`; `PUT /configuracao/revisoes`; `POST /configuracao/desabilitar` | P:unidade.* (Administrador) |
| `DELETE /unidade/{id}` | **A** |
| `GET /usuario/relatores-pip`, `/analistas-para-distribuicao`, `GET /usuario`, `/permissoes`, `POST /usuario/alternar-permissao` | A |
| `GET /usuario/{id}`, `GET /usuario/visao-administrador`, `GET /perfil` | P:usuario.* (Administrador) |
| `POST /usuario` (criar) | P:CriarUsuario (Administrador) |
| `DELETE /permissao/usuario/{usuarioId}/permissao/{permissaoId}` | P:permissao.ExcluirPermissao (Administrador) |
| `GET /assunto` | P:assunto.Listar; `GET visao-administrador`, `GET {id}`, `GET categorias`, `POST`, `PUT {id}`, `DELETE {id}`, `PATCH {id}/ativar` → P:assunto.Admin |
| `GET /{cargo/por-usuario, conduta, origem-denuncia, recomendacao, situacao-funcional, tipificacao-admissibilidade, tipo-diligencia, tipo-documento-demanda, tipo-processo, tipo-revisao, tipo-vinculo}` | A |
| `GET /status/{demanda,processo-admissibilidade,pip}`; `GET /pessoa/pesquisar`; `GET /servidor/pesquisar`; `POST /documento/validar` | A |

## Inferências e limitações
- ✅ `GET /processo-admissibilidade/por-relator` está marcado `[Obsolete]` e só exige autenticação; a política `jad.ListarProcessosPorRelator` está definida, mas nenhum controller a usa.
- Códigos HTTP: `HandleDomainException`, `HandleInvalidSciOperationException`, `HandleValidationException` e `HandleAuthenticationFailedException` mapeiam exceções (não detalhei os códigos).
- Swagger exposto na raiz (`RoutePrefix = ""`).

## Relacionamentos
- [[01-Sistemas/SCI/Backend/06-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança e autorização]] · [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]]

## Pendências e próximo passo
- Documentar payloads e códigos de resposta dos endpoints críticos.
