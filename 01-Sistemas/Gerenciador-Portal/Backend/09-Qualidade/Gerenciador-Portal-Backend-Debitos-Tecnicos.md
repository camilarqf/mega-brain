---
type: technical-debt
aliases:
  - "Débitos técnicos e riscos"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador
  - src/main/resources
  - pom.xml
  - .docker/Dockerfile
---
# Débitos técnicos e riscos

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

> Fatos (✅, verificados no código) separados das **recomendações**. Nenhuma exploração foi testada. Valores de credenciais não são registrados.

## Objetivo
Listar os débitos e riscos do backend, com severidade (🔴 alto, 🟠 médio, 🟡 baixo) e onde estão.

## Evidências
Leitura estática do commit `14b185f`. Referências: [[01-Sistemas/Gerenciador-Portal/Backend/08-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|Segurança]], módulos em `03-Modulos`.

## Informações confirmadas
| # | Sev. | Fato (✅) | Onde |
|---|---|---|---|
| 1 | 🔴 | Credenciais (banco, MongoDB, RabbitMQ e senha do usuário de desenvolvimento) estão **em texto nos `application-*.properties` versionados**, inclusive de produção e comentadas em `dev`/`PersistenceConfiguration`; vão no histórico do Git. | `src/main/resources`, `config/PersistenceConfiguration.java` |
| 2 | 🔴 | A API de escrita não valida identidade: qualquer `x-client-id` não vazio dá acesso a upload, exclusão e cadastro; o autor (`usuarioLogado`) vem do cliente; CORS `*`. | `ClientIdFilter`, `CorsFilter`, controllers |
| 3 | 🔴 | Login de desenvolvimento (`dev.usuario.*`) habilitado em todos os perfis, inclusive `prod`; contorna o SSO. | `LoginService` |
| 4 | 🔴 | **Injeção de SQL** (concatenação de texto livre): `CargaService` (4 filtros), `ServidorDAO` (`nomeServidor`), `ServidorMedidaProtetivaDAO` (`identificador`), `ArquivoDAO` (nome, descrição, data de referência). Inteiros concatenados em `ImagemDAO`/`CategoriaService`. | ver módulos |
| 5 | 🔴 | **Spring Data REST** no classpath sem `exported=false`; 🔶 pode expor CRUD dos repositórios (inclusive `Log` e `ServidorMedidaProtetiva`). Não testado em execução. | `pom.xml`, `repository/*` |
| 6 | 🟠 | A exclusão de arquivo/imagem não remove o objeto do MinIO (apaga no disco local) e responde `400` depois de já apagar a linha; `exclusao-multipla` ignora falhas. | `CommonService.deletarArquivo` |
| 7 | 🟠 | `salvar-sem-ordenar` grava a imagem no disco local (não no MinIO); dois caminhos de armazenamento. | `ImagemService` |
| 8 | 🟠 | Upload no MinIO antes do `INSERT`; sem compensação (objetos órfãos). | `ArquivoService`, `ImagemService` |
| 9 | 🟠 | JWT decodificado sem verificar assinatura; SSO e MinIO via `http`; token do SSO não é emitido ao cliente. | `JwtService`, `application-*.properties` |
| 10 | 🟠 | `deletarServidorMedidaProtetiva` não retorna quando o registro não existe (falha ao apagar `null`); `expirarCache` com `&&` na guarda de URL; `expirar-cache` responde `200` mesmo em falha. | `ServidorMedidaProtetivaService` |
| 11 | 🟠 | `AutenticacaoException` sempre vira `401` (ignora 400/503 definidos em `SsoAuthClient`); erros de token viram `500`. | `ResourceExceptionHandler` |
| 12 | 🟠 | Spring Boot 1.5.8 e Java 8 sem suporte; versões antigas de `jackson-databind`, `httpclient` e `commons-fileupload` fixadas manualmente (CVEs não verificadas). | `pom.xml` |
| 13 | 🟠 | Testes ignorados no build da imagem; 3 testes versionados; sem cobertura medida. | `.docker/Dockerfile` |
| 14 | 🟡 | `spring.jpa.show-sql=true`, Hikari `TRACE` e logs `DEBUG` do AWS SDK podem poluir/expor dados nos logs. | `application*.properties` |
| 15 | 🟡 | `/healthcheck` público revela nomes de buckets e mensagens do S3. | `Healthcheck` |
| 16 | 🟡 | Configuração morta: `access.token`, `url.servidor.api.sigrh`, `url.portal.verificar.sutcs`, `storage.public-url`; `PersistenceConfiguration` comentada; `@EnableScheduling` sem tarefas; `javax.mail` e `springloaded` sem uso identificado. | várias |
| 17 | 🟡 | `printStackTrace` em vez de log e `Optional.get()` sem verificação (`mover-prioridade-*`); upload de categoria inválida gera `Imagem` nula. | `ImagemService`, `ServidorMedidaProtetivaService` |
| 18 | 🟡 | Staging sem os secrets `STORAGE_*` no pipeline (a aplicação não inicia sem credenciais). | `.jenkins-pipelines/deployment.params.yml` |

## Falhas e dependências
Os itens 1 a 5 mexem com dados pessoais (CPF, nome em medida protetiva) e com credenciais de infraestrutura compartilhada; ver [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Medida protetiva]].

## Inferências e limitações (recomendações, 🔶 não implementadas)
- Rotacionar e retirar as credenciais do repositório (usar secrets, como já ocorre com `SSO_CLIENT_SECRET` e `STORAGE_*`); limpar o histórico se aplicável.
- Proteger a API com autenticação real (validar o token do SSO e a assinatura); derivar `usuarioLogado` do token; restringir CORS.
- Parametrizar todas as consultas (`JdbcTemplate` com `?`/`NamedParameterJdbcTemplate`).
- Anotar os repositórios com `@RepositoryRestResource(exported = false)` ou remover `spring-boot-starter-data-rest` se não for usado.
- Unificar o armazenamento em S3 (inclusive exclusão) e inverter a ordem ou compensar upload × banco.
- Remover o login de desenvolvimento dos perfis de produção e a configuração morta.
- Atualizar Spring Boot/Java e habilitar testes no build.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Testes-e-Cobertura|Testes]] · [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Débitos do Portal-Transparencia]] (para comparação)

## Pendências e próximo passo
- Priorizar com o time os itens 1 a 5; confirmar o item 5 em execução.
