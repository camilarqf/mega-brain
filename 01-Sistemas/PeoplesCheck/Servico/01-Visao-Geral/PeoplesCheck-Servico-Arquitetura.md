---
type: architecture
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - arquitetura
sources:
  - src/main/java/br/gov/df/peoplescheckapi/PeoplescheckapiApplication.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/ValidationFactory.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/abstractions/ValidationServiceBase.java
  - src/main/java/br/gov/df/peoplescheckapi/api/httpResponse/ValidationContractHttpResponse.java
---
# PeoplesCheck Serviço — arquitetura

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Descrever as camadas e o padrão de validação em etapas.

## Evidências
- Pacotes sob `br.gov.df.peoplescheckapi`: `api`, `application`, `domain`, `infrastructure`.
- Classes `ValidationFactory`, `ValidationServiceBase`, `ValidationTypeResolver`, `ValidationContractHttpResponse`.

## Informações confirmadas
| Camada | Conteúdo |
|---|---|
| `api` | controllers (`PeopleController`, `ChallengeController`, `JobsController`), segurança (filtro de API key), health check, tradução de contrato em HTTP |
| `application` | serviços de validação por tipo, etapas (`stepValidations`), contratos de resultado (`contracts`), criação e mapeamento das perguntas |
| `domain` | entidades (`NaturalPerson`, `JuridicalPerson`, `Challenge`), enums de situação, interfaces `IRepository` e `IChallengeCache` |
| `infrastructure` | `couchdb` (cliente HTTP, repositórios, mapeadores) e `mongodb` (DAO e configuração) |

- ✅ **Escolha do serviço por tipo de dado:** `ValidationTypeResolver.resolvesByData` conta os dígitos da entrada: 11 → `NATURAL_PERSON`, 14 → `JURIDICAL_PERSON`, outro → `CHALLENGE`. `ValidationFactory.getByType` devolve o serviço correspondente.
- ✅ **Cadeia de etapas (pipeline):** cada serviço (`NaturalPersonValidationService`, `JuridicalPersonValidationService`, `NaturalPersonChallengeValidationService`) registra etapas com `addValidation` e `ValidationServiceBase.processValidation` as executa em ordem; a primeira que devolve um `IFaultValidationContract` interrompe a cadeia.
- ✅ **Contratos de resultado:** o retorno é um objeto de contrato (sucesso: `ChallengeContract`, `ResponseChallengeContract`, `ValidAnswerContract`, `ValidRequestContract`; falha: `InvalidRequestContract`, `EntityNotFoundContract`, `InvalidAnswerContract`, `LimitExceeded`). `ValidationContractHttpResponse` traduz: sucesso → HTTP 200; qualquer falha → HTTP 400.
- ✅ Injeção por construtor com interfaces (`IRepository<T>`, `IChallengeCache`); os repositórios usam CouchDB e o cache de desafios usa MongoDB.
- ✅ `PeoplescheckapiApplication` exclui `SecurityAutoConfiguration` e `UserDetailsServiceAutoConfiguration`; a segurança é montada à mão em `SecurityConfig` ([[01-Sistemas/PeoplesCheck/Servico/06-Seguranca/PeoplesCheck-Servico-Seguranca-e-Autorizacao|Segurança]]).

## Inferências e limitações
- 🔴 ✅ **Estado compartilhado em serviços singleton:** `ValidationServiceBase` guarda a lista de etapas (`_validations`, um `CopyOnWriteArrayList`) como campo de instância e cada `validate` chama `addValidation` e, no fim, `clear()`. Os serviços são beans singleton do Spring; requisições simultâneas misturam e apagam as etapas umas das outras. Ver [[01-Sistemas/PeoplesCheck/Servico/08-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos técnicos]].
- 🔶 A interface `IValidationService` serve a etapas e a serviços ao mesmo tempo, o que obscurece a cadeia.

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Validacao-de-Pessoa|Validação de pessoa]] · [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]] · [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Modelo-de-Dominio|Modelo de domínio]]

## Pendências e próximo passo
- Nenhuma além da correção dos débitos.
