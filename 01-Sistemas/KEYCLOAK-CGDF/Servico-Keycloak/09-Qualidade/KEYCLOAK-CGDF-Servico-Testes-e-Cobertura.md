---
type: quality
aliases:
  - "Testes e cobertura"
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
sources:
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticatorTest.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/client/IbsRestClientTest.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/mapper/IbsClaimsMapperTest.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/provider/ServiceLoaderFilesTest.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/manual/IbsManualLoginRunner.java
---
# Testes e cobertura

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]]

## Objetivo
Inventariar os testes automatizados. ✅ Executados em 2026-10-18 com `mvn -B test` em `providers/` (commit `1755591`, sem alterações locais): **20 testes, 0 falhas, 0 erros, 0 ignorados** (relatórios do surefire: Authenticator 7, RestClient 7, ClaimsMapper 4, ServiceLoaderFiles 2). A saída mostra stack traces e avisos de SLF4J/JBoss LogManager; os traces vêm dos cenários de erro técnico e não indicam falha.

## Evidências
- Arquivos em `sources` (JUnit 5, Mockito, WireMock).

## Informações confirmadas
| Classe | Testes | O que cobre |
|---|---|---|
| `IbsAuthenticatorTest` | 7 | sucesso (usuário, notas, `success()`), criação de usuário, username = `idUsuario`, `idUsuario` ausente, credencial inválida, campo ausente, erro técnico |
| `IbsRestClientTest` | 7 | cliente `IbsApiClient` com WireMock: 200, barra final da URL, 401 com mensagem, 403 e 404 como erro técnico, timeout, mensagens sem senha |
| `IbsClaimsMapperTest` | 4 | claims corporativas, `unidades` como array, claims que não devem aparecer, toggles OIDC |
| `ServiceLoaderFilesTest` | 2 | `META-INF/services` sem BOM UTF-8 e registro do mapper |
| `IbsManualLoginRunner` | — | execução manual do cliente contra um IBS real (`mvn test-compile exec:java`) |

Total: 20 métodos de teste automatizados.

## Inferências e limitações
- ✅ Sem cobertura: `IbsConfig`/`IbsConfigResolver` (precedência de fontes e erros de valor), `idOrgao` não numérico, 401 com corpo inválido, normalização de usuário existente, `IbsAuthenticatorFactory`.
- ✅ O `Dockerfile` compila com `-DskipTests`; não há evidência no repositório de execução dos testes no pipeline (❓ Jenkins externo).
- Não há medição de cobertura (nenhum plugin JaCoCo no `pom.xml`).

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/09-Qualidade/KEYCLOAK-CGDF-Servico-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Sem pendência de execução. Falta apenas medir cobertura (sem JaCoCo).
