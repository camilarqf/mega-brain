---
type: business-rule
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - regra
  - tentativas
sources:
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/ChallengeTimeExpiredValidation.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/mongodb/ChallengeCacheDAO.java
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/JobsController.java
  - src/test/java/br/gov/df/peoplescheckapi/unitTests/applicationTests/stepValidationsTests/ChallengeTimeExpiredValidationTest.java
---
# PeoplesCheck Serviço — regra: limite de tentativas

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar o limite de respostas erradas por pessoa.

## Evidências
- `ChallengeTimeExpiredValidation` (`MAX_TRIES = 3`), `ChallengeCacheDAO.countLastTrys`, `countLastTryByPersonId`, `countLastTryByAssociatedPersonId`, `updateChallengeCountTry`.
- Teste `ChallengeTimeExpiredValidationTest` (3 casos; não executado).

## Informações confirmadas
- ✅ **Condição → efeito:** se a soma de tentativas erradas da pessoa é **3 ou mais**, a resposta ao desafio é recusada com `limitedExceeded` ("Limite de tentativas em 24 horas excedido") sem comparar as respostas.
- ✅ **Chave da contagem:** se o desafio tem CNPJ associado, soma-se por `associatedPersonId`; senão, por `personId` (considerando só desafios sem `associatedPersonId`).
- ✅ **Incremento:** +1 em `countTry` do desafio a cada resposta divergente. Respostas corretas não zeram nem alteram o contador.
- ✅ **Janela de 24 h:** a mensagem diz "24 horas"; a consulta não aplica o filtro de data (duplicidade da chave `expirationDate` no filtro, a segunda substitui a primeira — ver [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco e persistência]]). O efeito de 24 h vem de `DELETE /jobs/limpar-base-desafio`, que apaga os desafios criados há mais de 24 h.
- ✅ `GET /challenge/count-try?data=` expõe a mesma contagem ao consumidor (CPF → por pessoa; CNPJ → por associado).
- ✅ Desafio inexistente → `InvalidAnswerContract` (não `LimitExceeded`).

## Inferências e limitações
- 🔶 Se o job de limpeza não roda, o bloqueio deixa de expirar. O agendamento é feito pelo Jenkins (informado pelo usuário em 2026-10-19); frequência ❓.
- 🔶 A contagem por CPF ignora desafios com CNPJ associado e vice-versa (o limite de PF e o de PJ são independentes).
- 🔶 Contagem e incremento não são atômicos (corrida entre requisições simultâneas).
- ✅ Origem: a regra veio da Ouvidoria, dona do negócio do `PARTICIPA-DF` (informado pelo usuário em 2026-10-19; o documento do requisito não consta no repositório nem no vault).

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Resposta-ao-Desafio|Fluxo de resposta]] · [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]]

## Pendências e próximo passo
- Confirmar o requisito original e a agenda do job.
