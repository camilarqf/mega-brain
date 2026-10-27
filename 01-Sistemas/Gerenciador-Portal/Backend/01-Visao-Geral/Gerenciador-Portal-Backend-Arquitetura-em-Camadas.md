---
type: architecture
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
  - arquitetura
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador
---
# Arquitetura em camadas

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Descrever a estrutura de pacotes e as responsabilidades de cada camada (pacote raiz `br.gov.df.cgdf.gerenciador`).

## Evidências
Estrutura de `src/main/java/br/gov/df/cgdf/gerenciador` (102 arquivos de código no total, contando recursos): `api`, `services`, `services/auth`, `dao`, `repository`, `model`, `dto`, `enums`, `exceptions`, `handler`, `interfaces`, `util`, `config`, `config/prometheus`, `comum`.

## Informações confirmadas
| Camada (pacote) | Papel (✅) | Exemplos |
|---|---|---|
| `api` | 10 `@RestController` finos; delegam ao serviço e devolvem entidades/`HttpStatus` | `ArquivoController`, `ImagemController`, `ServidoresMedidaProtetivaController` |
| `services` | regra de negócio e orquestração; gravam log de auditoria | `ArquivoService`, `ImagemService`, `ServidorMedidaProtetivaService`, `StorageService` |
| `services/auth` | login por SSO, decodificação do JWT e autorização por órgão/unidade | `LoginService`, `SsoAuthClient`, `JwtService`, `AutorizacaoService` |
| `dao` | SQL escrito à mão com `JdbcTemplate` (consultas de leitura e filtros) | `ArquivoDAO`, `ImagemDAO`, `ServidorDAO` |
| `repository` | Spring Data JPA (SQL Server) e `MongoRepository` (`PalavrasRepository`) | `ArquivosRepository`, `ImagensRepository` |
| `model` | entidades JPA, um documento Mongo (`PalavraChave`) e tipos auxiliares | `Arquivo`, `Imagem`, `ServidorMedidaProtetiva` |
| `dto` / `enums` | objetos de entrada/saída e enums de medida protetiva | `UsuarioDTO`, `ConsultasMedidaProtetivaEnum` |
| `config` | CORS, filtro `x-client-id`, S3, Mongo, Prometheus | `ClientIdFilter`, `CorsFilter`, `S3Config` |
| `handler` | `@ControllerAdvice` com 13 handlers de exceção e payload `StandardError` | `ResourceExceptionHandler` |
| `comum` | indicador de saúde do MinIO (`@Component("minio")`) | `Healthcheck` |

- ✅ Dois acessos ao SQL Server convivem: JPA (CRUD das entidades) e `JdbcTemplate` (filtros/listagens). Para os mesmos dados, `ArquivosRepository` e `ArquivoDAO` coexistem.
- ✅ Toda alteração de arquivo/imagem/medida protetiva grava um registro em `arquivo.LOG_ARQUIVOS` (`LogService`, objeto serializado com Gson).
- ✅ Upload vai para o MinIO (`StorageService`), mas a exclusão usa o sistema de arquivos local (`CommonService`): ver [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Arquivos e relatórios]].
- ✅ `PersistenceConfiguration` está **inteiramente comentada** (configuração antiga de JPA/DataSource); o `DataSource` vem da autoconfiguração (Hikari, `spring.datasource.*`).
- ✅ Não há camada de segurança do Spring (sem starter): a proteção é o filtro `x-client-id` e o login.

## Inferências e limitações
- 🔶 Arquitetura em camadas simples, sem portas/adaptadores; regras de negócio e transações vivem nos serviços, e vários métodos devolvem `HttpStatus` em vez de lançar exceções.
- ❓ `@EnableScheduling` está ativo, mas não há tarefas agendadas no código principal.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Stack-e-Dependencias|Stack]] · [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Modelo-de-Dominio|Modelo de domínio]] · [[01-Sistemas/Gerenciador-Portal/Backend/06-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Gerenciador-Portal/Backend/99-Controle/Gerenciador-Portal-Backend-Pendencias|Pendências]].
