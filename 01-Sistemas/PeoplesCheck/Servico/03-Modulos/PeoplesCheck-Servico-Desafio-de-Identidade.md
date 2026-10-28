---
type: module
aliases:
  - "PeoplesCheck Serviço — desafio de identidade"
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
sources:
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/ChallengeController.java
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/JobsController.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/NaturalPersonChallengeValidationService.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/ChallengeTimeExpiredValidation.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/NaturalPersonChallengeAnswerValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/mongodb/ChallengeCacheDAO.java
  - .jenkins-pipelines/Jenkinsfile.jobs
---
# PeoplesCheck Serviço — desafio de identidade

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Gerenciar o desafio: receber a resposta, contar tentativas, devolver os dados principais quando correta e limpar desafios antigos.

## Evidências
- `ChallengeController`, `JobsController`, serviço e etapas em `sources`, `ChallengeCacheDAO`.

## Informações confirmadas
- ✅ **Resposta:** `POST /challenge/check` com `challenge.id` e `challenge.keys` (primeiro nome, primeiro nome da mãe, data `dd/MM/yyyy`). Etapas: `ChallengeTimeExpiredValidation` (limite de tentativas) → `NaturalPersonChallengeAnswerValidate` (compara com o cadastro). Detalhe em [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Resposta-ao-Desafio|Fluxo de resposta]].
- ✅ **Sucesso:** `ValidAnswerContract` (`challengeSolvedContract`) devolve `challenge.keys` com os dados principais: para pessoa física [nome completo, data `dd/MM/yyyy`, nome da mãe, CPF]; se há CNPJ associado e ele é apto, no lugar disso [razão social, nome fantasia, natureza jurídica, CNPJ (inserido no índice 3)].
- ✅ **Contagem de tentativas:** `GET /challenge/count-try?data=` devolve a soma de tentativas erradas (CPF → por pessoa; CNPJ → por pessoa associada; outro tamanho → 404). Regra em [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Limite-de-Tentativas|Limite de tentativas]].
- ✅ **Administração do cache** (todos exigem chave de API): `POST /challenge` (cria, 201 sem corpo), `GET /challenge?id=` (lê ou 404), `DELETE /challenge?id=` (apaga ou 404), `DELETE /challenge/old?data=yyyy-MM-dd` (apaga os criados até a data).
- ✅ **Limpeza:** `DELETE /jobs/limpar-base-desafio` apaga os desafios com mais de 24 h e registra em log. O pipeline `Jenkinsfile.jobs` chama `DELETE {url}/jobs/{jobName}` com a chave de API, e o usuário informou em 2026-10-19 que o agendamento é feito pelo Jenkins (✅; frequência e `jobName` ❓).
- ✅ O desafio **não é consumido** após uma resposta correta: continua válido até a limpeza.

## Inferências e limitações
- 🔴 ✅ Sem a limpeza, o contador de tentativas nunca zera ([[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco e persistência]]); a regra de 24 h depende do agendamento externo.
- 🔶 `JuridicalPersonChallengeAnswerValidate`, `ChallengeValidate`, `IChallengeValidationService` para PJ e `findAllChallenge` não são usados por nenhum fluxo (código sem uso aparente); o desafio por CNPJ avulso não tem pergunta/resposta implementada.
- 🔶 `POST /challenge` aceita o corpo `Challenge` mas só usa `personId` e `associatedPersonId`; o id gerado não é devolvido ao chamador.
- 🔶 `keys` com menos de três itens causa `IndexOutOfBoundsException` (sem validação).

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Validacao-de-Pessoa|Validação de pessoa]] · [[01-Sistemas/PeoplesCheck/Servico/06-API/PeoplesCheck-Servico-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Comparacao-de-Respostas|Comparação de respostas]] · [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-MongoDB|Integração MongoDB]]

## Pendências e próximo passo
- Confirmar agenda do job de limpeza e se o desafio de CNPJ avulso é usado por algum consumidor.
