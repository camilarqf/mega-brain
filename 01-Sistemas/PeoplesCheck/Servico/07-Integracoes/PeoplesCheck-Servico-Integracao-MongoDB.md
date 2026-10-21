---
type: integration
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
consumer: PeoplesCheck
provider: MongoDB
tags:
  - peoplescheck
  - integracao
  - mongodb
sources:
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/mongodb/ChallengeCacheDAO.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/mongodb/MongoConfig.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/IChallengeCache.java
---
# PeoplesCheck Serviço → MongoDB

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `PeoplesCheck` (`cgdf-peoples-check-api`) | `MongoDB` | driver Java do MongoDB (`MongoClient`, `MongoTemplate`) | coleção `challenges` | saída (leitura e escrita) |

## Evidências
- `ChallengeCacheDAO`, `MongoConfig`. Configuração (apenas nomes): `spring.data.mongodb.uri`, `spring.data.mongodb.database`, por perfil.

## Informações confirmadas
- ✅ Operações: `insertOne`, `find` por `_id` e por pessoa, `updateOne` com `$inc`, `deleteOne`, `deleteMany` (documento e consultas em [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco e persistência]]).
- ✅ Usado como cache de desafios e contador de tentativas; é a única persistência de escrita do serviço.
- ✅ Cliente criado uma vez (`MongoConfig`), com as configurações da string de conexão; sem opções explícitas de timeout.

## Falhas e dependências
- ✅ `insertChallenge` captura `MongoWriteException`, imprime a pilha e devolve `null`; o chamador usa o id e falha com `NullPointerException`.
- ✅ Demais operações propagam as exceções do driver → 5xx.
- ✅ Dependência síncrona de abertura e resposta de desafio e de `count-try`.
- 🔶 Sem health indicator específico no código do repositório.

## Inferências e limitações
- ❓ Dono, topologia (réplica/standalone), TLS e política de backup; ID `MongoDB` cadastrado no catálogo como serviço externo.
- 🔶 Sem índices nem TTL versionados: consultas por `personId`/`associatedPersonId` fazem varredura da coleção, a menos que existam índices criados fora do repositório.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-CouchDB|Integração CouchDB]] · [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]]

## Pendências e próximo passo
- Confirmar índices/TTL e ownership.
