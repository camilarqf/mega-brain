---
type: quality
aliases:
  - "PeoplesCheck Serviço — testes e cobertura"
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: parcial
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
sources:
  - src/test/java/br/gov/df/peoplescheckapi
  - pom.xml
  - .docker/Dockerfile
---
# PeoplesCheck Serviço — testes e cobertura

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar a estratégia e o inventário de testes. Os testes **não foram executados** nesta análise.

## Evidências
- 11 classes em `src/test/java` com 38 métodos `@Test` (contagem por leitura).

## Informações confirmadas
| Classe | `@Test` | Alvo |
|---|---|---|
| `PeoplescheckapiApplicationTests` | 1 | carga do contexto Spring |
| `ChallengeCacheTests` | 6 | cache de desafios |
| `NaturalPersonChallengeAnswerValidateTest` | 3 | resposta ao desafio (Mockito) |
| `NaturalPersonValidationServiceTests` | 1 | serviço de validação de CPF |
| `ValidationFactoryTests` | 3 | fábrica de serviços |
| `ValidationTypeResolverTests` | 3 | resolução por tamanho |
| `ChallengeTimeExpiredValidationTest` | 3 | limite de tentativas |
| `JuridicalPersonPreValidateTests` | 7 | pré-validação de CNPJ |
| `NaturalPersonPreValidateTests` | 7 | pré-validação de CPF |
| `ApiKeyControllerTests` | 3 | chave de API (RestAssured) |
| `CouchDbClientTests` | 1 | cliente CouchDB (mocks) |

- ✅ Regras cobertas por teste: dígitos verificadores de CPF e CNPJ, escolha do serviço por tamanho, limite de 3 tentativas, comparação das respostas.
- ✅ Sem plugin de cobertura (JaCoCo) nem configuração do Surefire no `pom.xml`: não há medição de cobertura.
- ✅ O `Dockerfile` compila com `-Dmaven.test.skip=true`: os testes não são executados no build da imagem.

## Inferências e limitações
- 🔶 Várias classes usam `@SpringBootTest` com `@Mock`: sobem o contexto completo (dependem de propriedades de MongoDB/CouchDB) e misturam mocks do Mockito sem extensão própria; podem falhar sem a infraestrutura.
- 🔶 `ApiKeyControllerTests` chama `localhost` com RestAssured sem iniciar a aplicação (sem `@SpringBootTest` com porta) e contém uma chave de API de exemplo no código.
- ❓ Não há testes de: `JobsController`, `ChallengeController`, `PeopleController`, `JuridicalPersonRepository`, `NaturalPersonRepository`, `ChallengeQuestionCreate`, `ChallengeCacheDAO` (apenas `ChallengeCacheTests`; conteúdo não verificado), nem testes de concorrência.
- ❓ Resultado da execução e cobertura percentual.

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/09-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Limite-de-Tentativas|Limite de tentativas]]

## Pendências e próximo passo
- Executar `mvnw test` num ambiente com as dependências e registrar o resultado.
