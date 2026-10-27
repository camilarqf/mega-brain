---
type: quality
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - testes
sources:
  - src/test/java
---
# IBS Backend — testes e cobertura

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Registrar o que existe de testes automatizados e o resultado da execução local.

## Evidências
- `./mvnw test` executado em 2026-10-18 no commit `cf0959a` (perfil `dev`, sem `SPRING_DATASOURCE_URL`): **157 testes, 152 passando, 5 com erro**.

## Informações confirmadas
| Área | Classes (testes) |
|---|---|
| API | `LoginControllerTest` (5), `UsuarioControllerTest` (6) |
| Aplicação | `AutenticarUsuarioHandlerTest` (14), `MontarClaimsHandlerTest` (5), `FonteAutenticacaoCacheServiceTest` (16), `ObterFontesPorSufixoHandlerTest` (4), `ResolverFontesPorOrgaoHandlerTest` (10), `SpringMediatorTest` (4), `BuscarUsuariosQueryTest` (4), `ObterUsuarioHandlerTest` (2), `ObterUsuarioQueryTest` (2) |
| Domínio | `FonteAutenticacaoTest` (7), `ServidorAutenticacaoTest` (6), `LoginContextualizadoTest` (7), `LoginUsuarioTest` (4), `SufixoLoginTest` (5), `ContextoPesquisaTest` (1), `SiglaUnidadeTest` (6), `TextoInstitucionalTest` (3), `UnidadesInstitucionaisTest` (3) |
| Infra | `LdapBindServiceTest` (11), `UsuarioRepositoryTest` (9), `IdentidadeInstitucionalRepositoryTest` (6), `FonteAutenticacaoRepositoryImplTest` (6), `IdentidadeInstitucionalServiceTest` (4), `UnidadeInstitucionalRepositoryTest` (4), `FonteAutenticacaoMapperTest` (1) |
| Contexto | `IdentityBrokerServiceApplicationTests` (1; exclui o datasource e mocka `JdbcTemplate`) |
| Suporte | `LdapBindServiceFake`, `FonteAutenticacaoStub` |

**Falhas observadas (5):**
- ✅ `UsuarioControllerTest` — 4 testes com `ClassCastException`: o teste usa o caminho `/usuarios/busca`, mas a rota real é `/usuarios/buscar`; `/usuarios/busca` casa com `/usuarios/{idUsuario}` e o mock devolve o tipo errado.
- ✅ `ResolverFontesPorOrgaoIntegrationTest` — depende de banco real (`CannotCreateTransactionException` sem datasource); lê `ibs.integration.login` por propriedade de sistema.

## Inferências e limitações
- Não há medição de cobertura (nenhum plugin JaCoCo no `pom.xml`); a avaliação é por inventário.
- 🔶 O `Dockerfile` roda `mvn package -DskipTests`; não verificado se o pipeline Jenkins executa testes.
- Conteúdo dos testes lido apenas por nomes de métodos e amostras.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/09-Qualidade/IBS-Backend-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Pendências e próximo passo
- Corrigir a rota no `UsuarioControllerTest` e isolar o teste de integração (perfil/Tag) — ver débitos.
