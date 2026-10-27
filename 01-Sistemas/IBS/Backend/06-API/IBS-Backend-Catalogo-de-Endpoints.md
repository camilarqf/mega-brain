---
type: api
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - api
  - endpoints
sources:
  - src/main/java/br/gov/df/cg/ibs/api/auth/LoginController.java
  - src/main/java/br/gov/df/cg/ibs/api/auth/AutenticarUsuarioRequest.java
  - src/main/java/br/gov/df/cg/ibs/api/auth/AutenticarUsuarioResponse.java
  - src/main/java/br/gov/df/cg/ibs/api/usuarios/UsuarioController.java
  - src/main/java/br/gov/df/cg/ibs/api/health/HealthController.java
  - src/main/java/br/gov/df/cg/ibs/api/exceptions/GlobalExceptionHandler.java
  - src/main/java/br/gov/df/cg/ibs/application/usuario/usecases/buscarusuarios/BuscarUsuariosQuery.java
---
# IBS Backend — catálogo de endpoints

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Documentar o contrato HTTP exposto, extraído do código (não do OpenAPI publicado, que não foi consultado).

## Evidências
- Controllers, DTOs, `GlobalExceptionHandler` e queries listados em `sources`. Nenhuma rota exige autenticação (ver [[01-Sistemas/IBS/Backend/08-Seguranca/IBS-Backend-Seguranca-e-Autorizacao|Segurança]]).

## Informações confirmadas
| Método e rota | Finalidade | Controller |
|---|---|---|
| `POST /auth` | Autenticar por LDAP e devolver claims | `LoginController` |
| `GET /usuarios/buscar` | Buscar usuários com filtros e paginação | `UsuarioController` |
| `GET /usuarios/{idUsuario}` | Consultar um usuário com unidades | `UsuarioController` |
| `GET /healthcheck` | Readiness (`readinessState` + `db`) | `HealthController` |
| `/actuator/*` | `health`, `info`, `metrics`, `prometheus` | Actuator |

### `POST /auth`
- **Request JSON:** `login` (obrigatório, mín. 3 caracteres, sem `@`), `senha` (obrigatória), `idOrgao` (inteiro obrigatório). Header opcional `X-Correlation-Key` (deve ser um UUID; ausente ou em branco → o serviço gera um).
- **Response 200:** `autenticado` (sempre `true`), `correlationKey` e `claims` { `login`, `idUsuario`, `idOrgao`, `siglaOrgao`, `nomeOrgao`, `nomePessoa`, `nomeSocial`, `matricula`, `unidades[]` { `idUnidade`, `siglaUnidade`, `descricaoUnidade` } }. Não há token.
- **Erros** (body `{"message": "..."}`):

| HTTP | Causa |
|---|---|
| 400 | Falha de validação do body (primeira mensagem), `IllegalArgumentException` (ex.: login com `@`, `X-Correlation-Key` que não é UUID) |
| 401 | `CREDENCIAL_INVALIDA` ou `USUARIO_SEM_VINCULO_NO_ORGAO` |
| 409 | `USUARIO_SEM_MATRICULA` |
| 503 | `SERVICO_INDISPONIVEL` e `FONTE_NAO_ENCONTRADA` quando lançados como `AutenticacaoException` (ramo `default`) |

### `GET /usuarios/buscar`
- **Query:** `nome`, `login`, `matricula`, `orgao`, `page` (padrão 0), `size` (padrão 20, 1 a 100). Exige ao menos um filtro, senão 400 "Informe ao menos um filtro para buscar usuários."
- **Response 200:** `content[]` (`idUsuario`, `login`, `matricula`, `idOrgao`, `siglaOrgao`, `nomeOrgao`, `nomeUsuario`, `nomeSocial`, `idUnidade`, `siglaUnidade`), `page`, `size`, `totalElements`, `totalPages`.
- Regras de filtro em [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Consulta-de-Usuarios|Consulta de usuários]].

### `GET /usuarios/{idUsuario}`
- **200:** `idUsuario`, `nomeUsuario`, `nomeSocial`, `login`, `matricula`, `idOrgao`, `siglaOrgao`, `nomeOrgao`, `unidades[]`. **404** "Usuário não encontrado."

### `GET /healthcheck`
- 200 com o descritor de saúde do grupo `readiness` quando `UP`; 503 com o descritor nos demais casos. Usado pelo healthcheck do Dockerfile e pelo `integration_definition` do pipeline.

## Inferências e limitações
- ✅ (por leitura do código) Exceções sem handler caem no tratamento padrão do Spring (500): `FonteAutenticacaoException`/`FonteAutenticacaoNaoEncontradaException` (órgão sem fonte), `IdentidadeInstitucionalIndisponivelException`, `MediatorException` e erros de acesso a dados. Portanto, na prática, "órgão sem fonte" resulta em 500, e o ramo `FONTE_NAO_ENCONTRADA` → 503 só ocorre se a lista de fontes chegar vazia a `AutenticacaoService.autenticar`. Não foi executado.
- 🔶 Springdoc está presente sem configuração própria; pelos padrões do springdoc, o OpenAPI e o Swagger UI ficam em `/v3/api-docs` e `/swagger-ui.html`. Não verificado em execução.
- 🔶 `idOrgao` enviado como texto numérico (como faz o cliente do Keycloak) depende da coerção padrão do Jackson; não testado.
- Contrato do lado consumidor: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integração Keycloak → IBS]].

## Relacionamentos
- [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]] · [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo de autenticação]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Claims|Modelo de claims]]

## Pendências e próximo passo
- Confirmar em ambiente o OpenAPI publicado e a coerção de `idOrgao`.
