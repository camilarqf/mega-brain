---
type: api
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - backend
  - api
  - endpoints
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/api
  - src/main/java/br/gov/df/cgdf/gerenciador/config/prometheus/PrometheusMetricsController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/config/ClientIdFilter.java
  - src/main/resources/application.properties
---
# Catálogo de endpoints

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Listar o contrato HTTP exposto pelos controllers (caminhos relativos à raiz do contexto; porta 8080).

## Evidências
Controllers em `api/` e `PrometheusMetricsController`. Regra comum: todo pedido, exceto `OPTIONS`, `*/healthcheck` e `*/prometheus`, exige o cabeçalho `x-client-id` (qualquer valor não vazio), senão responde `400` `{"message":"Header x-client-id obrigatório."}` (`ClientIdFilter`). Não há outra autenticação (ver [[01-Sistemas/Gerenciador-Portal/Backend/08-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|Segurança]]).

## Informações confirmadas
Legenda de parâmetros: `{x}` = variável de caminho; `?x` = parâmetro (query/form); `body` = JSON; `file` = multipart.

### `/login`
| Verbo | Caminho | Entrada | Saída |
|---|---|---|---|
| POST | `/login` | body `{login, senha}` | `200` `UsuarioDTO`; `401` para qualquer falha de autenticação no SSO (o handler ignora o status 400/503 da exceção); `403` sem permissão; `500` para token ausente/inválido |

### `/arquivo` (módulo [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Arquivos]])
| Verbo | Caminho | Entrada | Saída |
|---|---|---|---|
| POST | `/arquivo/salvar-arquivo/{usuarioLogado}/{codigoCategoria}/{ano}` | `file` | `Arquivo` (incompleto) ou `400` com a mensagem de erro |
| POST | `/arquivo/salvar-informacoes-arquivo` | body `Arquivo`; `?usuarioLogado`, `?idReferenciaEscolhida`, `?prefixoCategoria`, `?nomeOriginal` (opcional) | `HttpStatus` |
| POST | `/arquivo/ativar-arquivo`, `/desativar-arquivo`, `/excluir-arquivo` | `?id`, `?usuarioLogado` | `HttpStatus` |
| POST | `/arquivo/exclusao-multipla` | `?idArquivos` (lista), `?usuarioLogado` | `HttpStatus` |
| POST | `/arquivo/filtrar-arquivos` | body `Arquivo` (filtros) | lista de `Arquivo` |
| GET | `/arquivo/listar-ano`, `/listar-periodo`, `/listar-completos`, `/listar-incompletos`, `/listar-arquivos` | — | listas |
| GET | `/arquivo/listar-referencia` | `?idReferencia` | lista de `Referencia` |
| GET | `/arquivo/quantidade-arquivos-completos`, `/quantidade-arquivos-incompletos` | — | inteiro |
| GET | `/arquivo/recuperar-arquivo`, `/recuperar-arquivo-incompleto` | `?id` | `Arquivo` |

### `/imagem` (módulo [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Imagens-do-Portal|Imagens]])
| Verbo | Caminho | Entrada |
|---|---|---|
| POST | `/imagem/salvar/{usuarioLogado}/{codigoCategoria}` e `/imagem/salvar-sem-ordenar/{usuarioLogado}/{codigoCategoria}` | `file` |
| POST | `/imagem/salvar-imagem-background/{usuarioLogado}/{codImagemPainel}` | `file` |
| POST | `/imagem/ativar-imagem`, `/imagem/desativar-imagem` | `?id`, `?usuarioLogado` |
| PUT | `/imagem/salvar-imagem` | body `Imagem`; `?usuarioLogado` |
| PUT | `/imagem/ordenar-prioridades-imagens/{codigoCategoria}` | — |
| PUT | `/imagem/mover-prioridade-acima`, `/imagem/mover-prioridade-abaixo` | body `Imagem`; `?usuarioLogado` |
| DELETE | `/imagem/excluir-imagem` | `?id`, `?usuarioLogado` |
| DELETE | `/imagem/excluir-background` | `?idBackground`, `?idImagem`, `?usuarioLogado` |
| GET | `/imagem/listar-imagens-slideshow`, `/listar-imagens-setores`, `/listar-funcoes-paineis` | — |
| GET | `/imagem/recuperar-imagem` | `?id` |

### Conteúdo e apoio
| Verbo | Caminho | Entrada | Módulo |
|---|---|---|---|
| GET | `/categoria/listar-categorias` | — | [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Arquivos]] |
| GET | `/carga/listar-cargas` | `?dataCarga`, `?statusCarga`, `?esquemaCarga`, `?tabelaCarga` (opcionais) | [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Cargas|Cargas]] |
| GET | `/carga/listar-status`, `/listar-esquema`, `/listar-quantidade-status` | — | Cargas |
| POST | `/palavra/salvar` · `/palavra/editar` · `/palavra/excluir` | body `PalavraChaveDTO` / `PalavraChave` | [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Conteúdo do portal]] |
| GET | `/palavra/listar` | — | Conteúdo |
| GET | `/textos-consultas` | `?idCategoria`, `?idSubCategoria` | Conteúdo |
| PUT | `/textos-consultas` | body `TextoConsultaPortal` | Conteúdo |
| GET | `/textos-consultas/categorias` · `/sub-categorias` | `?idCategoria` (sub-categorias) | Conteúdo |
| POST/GET/PUT | `/orgao` | body `OrgaoLAI` (POST/PUT) | Conteúdo |
| DELETE | `/orgao` | `?id` | Conteúdo |

### Medida protetiva e busca de servidores
| Verbo | Caminho | Entrada |
|---|---|---|
| GET | `/servidores/remuneracao`, `/por-orgao`, `/despesas`, `/cadastro-expulsoes`, `/conselheiros` | `?nomeServidor` |
| GET | `/servidores-medida-protetiva/listar` | — |
| GET | `/servidores-medida-protetiva` | `?identificador` |
| GET | `/servidores-medida-protetiva/{remuneracao,por-orgao,despesas,cadastro-expulsoes,conselheiros,conselhos}` | — |
| POST | mesmos seis caminhos acima | body `{identificador, nome}`; `?usuarioAutenticado` |
| DELETE | `/servidores-medida-protetiva/{id}` | `?usuarioAutenticado` |
| GET | `/servidores-medida-protetiva/expirar-cache` | — |

Ver [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Módulo de medida protetiva]].

### Operação
| Verbo | Caminho | Observação |
|---|---|---|
| GET | `/healthcheck` | Actuator (`endpoints.health.id=healthcheck`); inclui o indicador `minio` (HEAD nos dois buckets) com `UP`/`DOWN` e nomes dos buckets; sem `x-client-id` |
| GET | `/prometheus` | métricas Prometheus; sem `x-client-id` |

## Falhas e dependências
- ✅ Erros: `ResourceExceptionHandler` converte `ObjectNotFoundException` (404), parâmetro ausente (400), falha de conexão JDBC (504), `AcessoNegadoException` (403), `AutenticacaoException` (sempre 401), `IndexOutOfBoundsException` (204) e várias exceções de dados/SQL (500) etc. no formato `StandardError`; várias rotas ainda respondem só `HttpStatus` no corpo.
- ✅ **Spring Data REST** (`spring-boot-starter-data-rest`) está no classpath e nenhum repositório tem `@RepositoryRestResource(exported = false)`. 🔶 Por padrão, isso exporia os repositórios JPA/Mongo como recursos REST (CRUD), **além** dos controllers acima; não testado em execução.
- ✅ Parâmetros sem anotação (`String usuarioAutenticado`, `String nomeServidor`, `String identificador`) são ligados por nome pelo Spring.

## Inferências e limitações
- 🔶 `usuarioLogado` na URL/parâmetro é preenchido pelo cliente e usado só para auditoria.
- ❓ Códigos de resposta de sucesso/erro por rota não foram testados em execução.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Arquitetura-em-Camadas|Arquitetura]] · [[Mapa-de-Integracoes|Mapa de integrações]] · Consumidor: [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas do Frontend]]

## Pendências e próximo passo
- Confirmar em execução se o Spring Data REST expõe os repositórios (pendência no registro).
