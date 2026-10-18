---
type: api
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - backend
  - api
  - endpoints
  - acesso
sources:
  - src/OuvDF.Api/Controllers
  - src/OuvDF.Api/Startup.cs
  - src/OuvDF.Api/Filters/LogAudit.cs
---

# Catálogo de endpoints (visão geral, Shared e raiz)

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Partes: [[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Endpoints-Ouvidoria|Endpoints-Ouvidoria]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Endpoints-SIC|Endpoints-SIC]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/06-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Objetivo
Catalogar todos os endpoints HTTP da API (verbo, rota, acesso declarado, marcas e tipo de entrada) e destacar os pontos de atenção de acesso. A lista foi **extraída dos controllers por script** (atributos `[Http*]`, `[Route]`, `[Authorize]`, `[AllowAnonymous]`, `[LogAudit]`, `[RequestSizeLimit]`), ignorando trechos comentados, e conferida contra a contagem de `[Http*]` do código (262 = 262).

## Evidências
`src/OuvDF.Api/Controllers/**`, commit `4901ad5`. A coluna **Acesso** reflete só o que está **declarado** nos atributos da classe e da ação; não inclui regras de autenticação que o SDK (`UseCgdfSecurity`, `AddJwtSecurity`) possa impor globalmente (❓ não lido).

## Informações confirmadas

### Números
- ✅ **262 endpoints**: 180 `POST` e 82 `GET`; nenhum `PUT`, `DELETE` ou `PATCH` (estilo RPC: consultas e comandos por `POST`).
- ✅ 84 endpoints com `[LogAudit]` e 20 com `[RequestSizeLimit(40_000_000)]` (uploads de até 40 MB).
- ✅ 12 endpoints de `Dashboard` estão **comentados** no código (não contados).

### Matriz de acesso declarado

| Área | Total | anônimo | sem atributo | autenticado | OperadorSO | OperadorSIC | OperadorSO,OperadorSIC | OperadorWS |
|---|---|---|---|---|---|---|---|---|
| Ouvidoria | 108 | 33 | 0 | 36 | 35 | 0 | 0 | 4 |
| SIC | 62 | 2 | 10 | 32 | 0 | 18 | 0 | 0 |
| Shared e raiz | 92 | 21 | 15 | 32 | 18 | 1 | 3 | 2 |
| **Total** | **262** | **56** | **25** | **100** | **53** | **19** | **3** | **6** |

Legenda: **anônimo** = `[AllowAnonymous]` na ação ou na classe; **sem atributo** = nem `[Authorize]` nem `[AllowAnonymous]` na classe ou na ação; **autenticado** = `[Authorize]` sem papel; **OperadorSO / OperadorSIC / OperadorWS** = `[Authorize(Roles=…)]`. Marcas: `audit` = `[LogAudit]`; `40MB` = limite de tamanho do corpo.

### Pontos de atenção de acesso
**Endpoints sem nenhum atributo de autorização (25)**, que ficam abertos se não houver autenticação global (❓ SDK):
- `UnidadeController` (9): `POST unidade/so` (grava unidade SO), `unidade/sic/ativar`, `unidade/sic/desativar`, listagens e consultas por id.
- `NotificacaoController` do SIC (4): registrar omissão de resposta, omissão CGDF, resposta preliminar e decisão.
- `JobController` (2): `GET jobs/{jobName}` e `GET jobs/v2/{jobName}`.
- `ConfigurationController` (2): `GET configuration/cors-origins` e `configuration/front-end-urls`.
- SIC: `arquivo/download`, `arquivo/validar`, `assunto` (3), `situacao/situacao-resposta`.
- Shared: `necessidade-especial`, `security/is-auth`.

**Anônimos que gravam dados:** `POST servico-ouvidoria/manifestacao` e `…/integrada`, `POST pessoa-fisica`, `pessoa-fisica/por-operador`, `pessoa-juridica`, `…/desbloquear-dados-inconsistentes` (PF e PJ), `usuario/recuperar-senha`, `usuario/concluir-recuperacao-senha` e **`operador-so/operador-ws`** (cria operador de serviço).

**Anônimos que consultam:** `manifestacao/resumo`, `security/token-retrieve/{sessionId}`, `security/check`, `check-cpf-vinculado-pj`, `count-try`, `challenge`, `politica/vigente`, `pessoa-*/existe`, `validar-cnpj`, cadastros públicos (assuntos, classificações, coleções, regiões administrativas, tipos de entrada, formulário por assunto, unidades), os `metro/*`, `servicos/*` e `ia/*`.

**Duplicidade de rota:** em `ServicoOuvidoria/IntegracaoController` há duas ações `GET v1/manifestacao` (`Create` e `ConsultarManifestacaoPorId`), o que tende a gerar `AmbiguousMatchException` para essa rota (🔶 não executado). Além disso, uma delas é `GET` com `[FromBody]`.

### Convenções observadas
- ✅ Rotas em minúsculas com hífen; prefixos `servico-ouvidoria/…`, `acesso-informacao/…`, `v1/…` (integração por `OperadorWS`), sem prefixo para Shared (`usuario`, `operador-so`, `pessoa-fisica`, `unidade`).
- ✅ `User.Id()` fornece o `UsuarioRegistrador`/`Operador` dos comandos; respostas de comando passam por `OuvDFBaseController.ProcessCommand` (`200` com `Response` ou `400` com `Notifications`/`ExceptionDetails`); `428` via `PreconditionRequiredObjectResult` em casos específicos.
- ✅ Erros não tratados: `UseGlobalExceptionHandler` devolve `500`.
- ✅ Saúde: `GET /healthcheck` (mapeado no `Startup`, fora dos controllers) e hub SignalR `/notification-auth`.

## Inferências e limitações
- 🔶 `GET` com corpo (`[FromBody]`) é pouco compatível com proxies e clientes; `GET v1/manifestacao` o usa.
- 🔶 `ConfigurationController` expõe a lista de origens CORS e URLs de frontend a quem chamar (informação de infraestrutura).
- ❓ Contratos (campos e códigos de erro) de cada comando não estão aqui: a coluna **Entrada** só indica o tipo C# do corpo.
- ❓ Códigos HTTP além de `200/400/401/428/500` não foram levantados.

## Shared e raiz (92 endpoints)

### Configuration (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `configuration/cors-origins` | sem atributo |  |  |
| GET | `configuration/front-end-urls` | sem atributo |  |  |

### Integracao (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `v1/usuario/pessoa-fisica/por-cpf` | OperadorWS |  |  |
| POST | `v1/usuario/pessoa-fisica` | OperadorWS | audit | `GravarCidadao` |

### Job (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `jobs/v2/{jobName}` | sem atributo |  |  |
| GET | `jobs/{jobName}` | sem atributo |  |  |

### NecessidadeEspecial (1)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `necessidade-especial` | sem atributo |  |  |

### OperadorSIC (11)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `operador-sic/consultar-permissoes` | autenticado |  |  |
| GET | `operador-sic/operador-existe` | autenticado |  |  |
| GET | `operador-sic/unidades` | autenticado |  |  |
| POST | `operador-sic` | autenticado |  | `ConsultarOperadoresSIC` |
| POST | `operador-sic/alterar-unidade-atual` | autenticado | audit | `AlterarUnidadeAtual` |
| POST | `operador-sic/ativar` | autenticado | audit | `AtivarOperadorSIC` |
| POST | `operador-sic/atualizar` | autenticado | audit | `GravarOperadorSIC` |
| POST | `operador-sic/cadastrar` | autenticado | audit | `GravarOperadorSIC` |
| POST | `operador-sic/consultar-por-cpf` | autenticado |  | `ConsultarOperadorSicPorCPF` |
| POST | `operador-sic/consultar-por-id` | autenticado |  | `ConsultarOperadorSICPorId` |
| POST | `operador-sic/desativar` | autenticado | audit | `DesativarOperadorSIC` |

### OperadorSO (9)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `operador-so/consultar-permissoes` | OperadorSO |  |  |
| GET | `operador-so/consultar-por-unidade` | OperadorSO |  |  |
| GET | `operador-so/existe` | OperadorSO |  |  |
| GET | `operador-so/unidades` | OperadorSO |  |  |
| POST | `operador-so` | OperadorSO | audit | `GravarOperadorSo` |
| POST | `operador-so/alterar-unidade` | OperadorSO | audit | `AlterarUnidadePadrao` |
| POST | `operador-so/id` | OperadorSO |  | `ConsultarOperadorSO` |
| POST | `operador-so/listar` | OperadorSO |  | `ConsultarOperadoresSO` |
| POST | `operador-so/operador-ws` | anônimo | audit | `GravarOperadorWS` |

### PerfilSIC (5)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `acesso-informacao/perfil-sic/ativos` | autenticado |  |  |
| GET | `acesso-informacao/perfil-sic/funcionalidade` | autenticado |  |  |
| POST | `acesso-informacao/perfil-sic` | autenticado | audit | `GravarPerfilSIC` |
| POST | `acesso-informacao/perfil-sic/get-perfil-por-id` | autenticado |  | `ConsultarPerfilSICPorId` |
| POST | `acesso-informacao/perfil-sic/get-perfis` | autenticado |  | `ConsultarPerfisSIC` |

### PerfilSo (5)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `perfil-so/ativos` | OperadorSO |  |  |
| GET | `perfil-so/funcionalidade` | OperadorSO |  |  |
| POST | `perfil-so` | OperadorSO | audit | `GravarPerfilSO` |
| POST | `perfil-so/id` | OperadorSO |  | `CommandIDSensitive<long>` |
| POST | `perfil-so/listar` | OperadorSO |  | `ConsultarPerfisSO` |

### PessoaFisica (7)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| POST | `pessoa-fisica` | anônimo | audit | `CadastrarPessoaFisica` |
| POST | `pessoa-fisica/atualizar` | autenticado | audit | `AtualizarPessoaFisica` |
| POST | `pessoa-fisica/atualizar/por-operador` | autenticado | audit | `AtualizarPessoaFisica` |
| POST | `pessoa-fisica/desbloquear-dados-inconsistentes` | anônimo |  | `DesbloquearPessoaFisicaDadosInconsistentes` |
| POST | `pessoa-fisica/existe` | anônimo |  | `ConsultarExistenciaPessoaFisica` |
| POST | `pessoa-fisica/por-cpf` | autenticado |  | `ConsultarUsuario` |
| POST | `pessoa-fisica/por-operador` | anônimo | audit | `CadastrarPessoaFisica` |

### PessoaJuridica (12)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `pessoa-juridica/historico-responsavel` | autenticado |  |  |
| GET | `pessoa-juridica/por-cnpj` | autenticado |  |  |
| GET | `pessoa-juridica/tipo-entidade` | anônimo |  |  |
| GET | `pessoa-juridica/usuario/pessoa-juridica/validar-cnpj` | anônimo |  |  |
| POST | `pessoa-juridica` | anônimo | audit | `CadastrarPessoaJuridica` |
| POST | `pessoa-juridica/atualizar` | autenticado | audit | `AtualizarPessoaJuridica` |
| POST | `pessoa-juridica/atualizar-responsavel` | autenticado | audit | `AtualizarResponsavelPessoaJuridica` |
| POST | `pessoa-juridica/atualizar/por-operador` | OperadorSO,OperadorSIC | audit | `AtualizarPessoaJuridica` |
| POST | `pessoa-juridica/desbloquear-dados-inconsistentes` | anônimo |  | `DesbloquearPessoaJuridicaDadosInconsistentes` |
| POST | `pessoa-juridica/existe` | anônimo |  | `ConsultarExistenciaPessoaJuridica` |
| POST | `pessoa-juridica/historico-responsavel-por-operador` | autenticado |  | `ConsultarHistoricoResponsaveisPJ` |
| POST | `pessoa-juridica/por-operador` | OperadorSO,OperadorSIC | audit | `CadastrarPessoaJuridica` |

### Politica (2)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `politica/vigente` | anônimo |  |  |
| POST | `politica/aceitar-vigente` | autenticado | audit | `AceitarPolitica` |

### Security (9)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `security/check` | anônimo |  |  |
| GET | `security/check-cpf-vinculado-pj` | anônimo |  |  |
| GET | `security/count-try` | anônimo |  |  |
| GET | `security/is-auth` | sem atributo |  |  |
| GET | `security/logout` | autenticado |  |  |
| GET | `security/token-retrieve/{sessionId}` | anônimo |  |  |
| POST | `security/auth` | anônimo |  | `AutenticarUsuario` |
| POST | `security/challenge` | anônimo |  |  |
| POST | `security/notify` | autenticado |  | `NotificarAutenticacao` |

### Unidade (11)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `unidade/so/tipo-unidade` | sem atributo |  |  |
| GET | `unidade/subordinadasSIC` | OperadorSIC |  |  |
| GET | `unidade/subordinadasSO` | OperadorSO |  |  |
| POST | `unidade/ouvidorias-ativas` | sem atributo |  | `ConsultarUnidadesOuvidoriasAtivas` |
| POST | `unidade/sic/ativar` | sem atributo | audit | `AtivarUnidadeSIC` |
| POST | `unidade/sic/desativar` | sem atributo | audit | `DesativarUnidadeSIC` |
| POST | `unidade/sic/id` | sem atributo |  | `CommandIDSensitive<string>` |
| POST | `unidade/sic/listar` | sem atributo |  | `ConsultarUnidadesSIC` |
| POST | `unidade/so` | sem atributo | audit | `GravarUnidadeSO` |
| POST | `unidade/so/id` | sem atributo |  | `CommandIDSensitive<string>` |
| POST | `unidade/so/listar` | sem atributo |  | `ConsultarUnidadesSO` |

### Usuario (14)

| Verbo | Rota | Acesso | Marcas | Entrada |
|---|---|---|---|---|
| GET | `usuario` | anônimo |  | `bool` |
| GET | `usuario/detalhar` | autenticado |  |  |
| GET | `usuario/motivacao-bloqueio-usuario` | autenticado |  |  |
| GET | `usuario/por-login` | OperadorSO |  |  |
| GET | `usuario/por-nome` | OperadorSO |  |  |
| GET | `usuario/profile` | autenticado |  |  |
| POST | `usuario/alterar-senha` | autenticado | audit | `AlterarSenha` |
| POST | `usuario/bloquear` | OperadorSO | audit | `BloquearUsuario` |
| POST | `usuario/concluir-recuperacao-senha` | anônimo | audit | `ConcluirRecuperacaoSenha` |
| POST | `usuario/desbloquear` | OperadorSO | audit | `DesbloquearUsuario` |
| POST | `usuario/excluir-conta` | autenticado | audit | `SolicitarExclusaoContaUsuario` |
| POST | `usuario/id` | OperadorSO,OperadorSIC |  | `ConsultarUsuario` |
| POST | `usuario/recuperar-senha` | anônimo |  | `RecuperarSenha` |
| GET | `v2/usuario` | anônimo |  | `bool` |

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]] · [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]]

## Pendências e próximo passo
- Confirmar no SDK se há autenticação global; se não, os 25 endpoints sem atributo são risco de acesso (lote 8).
- Descrever contratos de entrada e saída das operações principais quando houver amostras de payload ou testes.
