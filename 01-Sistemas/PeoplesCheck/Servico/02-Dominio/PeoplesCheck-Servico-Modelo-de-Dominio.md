---
type: domain
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - dominio
  - enums
sources:
  - src/main/java/br/gov/df/peoplescheckapi/domain/NaturalPerson.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/JuridicalPerson.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/NaturalPersonStatus.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/JuridicalPersonStatus.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/Challenge.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/ChallengeKeys.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/Step.java
  - src/main/java/br/gov/df/peoplescheckapi/application/contracts
---
# PeoplesCheck Serviço — modelo de domínio

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Descrever entidades, enums, estados e contratos de resultado.

## Evidências
- Pacote `domain` e pacote `application.contracts` (ver `sources`).

## Informações confirmadas
**Entidades (leitura do CouchDB)**
| Entidade | Campos | Observações |
|---|---|---|
| `NaturalPerson` | `id` (CPF), `name`, `mothersName`, `dateOfBirth` (`yyyyMMdd`), `status` | `isRegular()` = `status == 0`; `getFormateData()` devolve `dd/MM/yyyy` (ou `null` se a data não faz parse); `getFirstName()` e `getMothersFirtName()` pegam a primeira palavra; `getDadosPrincipais()` = [nome, data formatada, nome da mãe, CPF] |
| `JuridicalPerson` | `id` (CNPJ), `name` (razão social), `nomeFantasia`, `naturezaJuridica`, `activityStartDate`, `status` | `isAble()` = situação diferente de `CANCELED` e de `NULL`; `getDadosPrincipais()` = [razão social, nome fantasia, natureza jurídica] |

**Estado do desafio (MongoDB)**
| Entidade | Campos | Observações |
|---|---|---|
| `Challenge` | `id` (UUID), `solution`, `expirationDate`, `personId`, `associatedPersonId`, `countTry`, `steps` | coleção `challenges`; `solution` não é preenchido pelo código lido; `expirationDate` é, na prática, a data de **criação** (ver [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco e persistência]]) |
| `Step` | `description`, `item` | `item` é a palavra inicial mascarada: cada caractere vira `_` |
| `ResponseChallenge` | `id`, `steps` | o que o cliente recebe ao abrir o desafio |
| `ChallengeKeysDTO` / `ChallengeKeys` | `challenge.id`, `challenge.keys[]` | entrada da resposta: `keys[0]` primeiro nome, `keys[1]` primeiro nome da mãe, `keys[2]` data `dd/MM/yyyy` |

**Enums de situação cadastral**
| `NaturalPersonStatus` | valor | | `JuridicalPersonStatus` | valor |
|---|---|---|---|---|
| `REGULAR` | 0 | | `NULL` | 1 |
| `SUSPENDED` | 2 | | `ACTIVE` | 2 |
| `DECEASED` | 3 | | `SUSPENDED` | 3 |
| `PENDING` | 4 | | `UNFIT` | 4 |
| `CANCELED_BY_MULTIPLICITY` | 5 | | `ACTIV_NOT_REGULAR` | 5 |
| `NULL` | 8 | | `CANCELED` | 8 |
| `OFFICIALLY_CANCELED` | 9 | | | |

- ✅ Os códigos seguem a situação cadastral da Receita Federal (🔶 pela correspondência dos valores; a fonte não é citada no código).

**Contratos de resultado** (pacote `application.contracts`)
| Contrato | Tipo | `type` no JSON | HTTP |
|---|---|---|---|
| `ChallengeContract` | sucesso (interno: carrega `naturalPerson`/`juridicalPerson`) | — | 200 |
| `ResponseChallengeContract` | sucesso | `challengeContract` | 200 |
| `ValidAnswerContract` | sucesso | `challengeSolvedContract` | 200 |
| `ValidRequestContract` | sucesso (etapa) | — | 200 |
| `InvalidRequestContract` | falha | `invalidRequestContract` ("O Dado informado é inválido") | 400 |
| `EntityNotFoundContract` | falha | `entityNotFoundContract` (mensagem variável) | 400 |
| `InvalidAnswerContract` | falha | `invalidAnswerContract` ("Resposta inválida") | 400 |
| `LimitExceeded` | falha | `limitedExceeded` ("Limite de tentativas em 24 horas excedido") | 400 |

## Inferências e limitações
- 🔶 `IValidationContract` declara constantes (`type`, `message`, `content` como campos de interface, sempre `null`) sem uso; os contratos concretos definem seus próprios campos.
- 🔶 O nome `limitedExceeded` é gramaticalmente incorreto, mas faz parte do contrato HTTP consumido; alterar exige coordenação com os clientes.
- Dados pessoais (nome, mãe, nascimento, CPF) transitam por estas entidades; ver [[01-Sistemas/PeoplesCheck/Servico/08-Seguranca/PeoplesCheck-Servico-Seguranca-e-Autorizacao|Segurança]].

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Validacao-de-Pessoa|Validação de pessoa]] · [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]] · [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Elegibilidade-Cadastral|Elegibilidade cadastral]]

## Pendências e próximo passo
- Confirmar a fonte oficial dos códigos de situação cadastral.
