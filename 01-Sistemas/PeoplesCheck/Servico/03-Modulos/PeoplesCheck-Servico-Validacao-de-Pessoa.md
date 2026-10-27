---
type: module
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - modulo
  - validacao
sources:
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/PeopleController.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/NaturalPersonValidationService.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/JuridicalPersonValidationService.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/NaturalPersonPreValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/JuridicalPersonPreValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/NaturalPersonEntityValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/JuridicalPersonEntityValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/ChallengeQuestionCreate.java
---
# PeoplesCheck Serviço — validação de pessoa

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Conferir um CPF ou CNPJ (formato, dígitos verificadores e situação cadastral) e abrir um desafio de identidade.

## Evidências
- `PeopleController` (`GET /people/check` e `GET /people/check/cnpj/{cnpj}`), serviços de validação e etapas em `sources`.

## Informações confirmadas
- ✅ **CPF** (`NaturalPersonValidationService`): etapas `NaturalPersonPreValidate` (limpa não dígitos, exige 11, rejeita sequência de dígitos iguais, confere os dois dígitos verificadores) → `NaturalPersonEntityValidate` (busca no CouchDB; aceita só situação regular).
- ✅ **CNPJ** (`JuridicalPersonValidationService`): `JuridicalPersonPreValidate` (14 dígitos e dígitos verificadores; **não** rejeita sequências iguais) → `JuridicalPersonEntityValidate` (busca no CouchDB; aceita se `isAble()`).
- ✅ Falhas: dígitos inválidos → `InvalidRequestContract`; pessoa inexistente ou irregular → `EntityNotFoundContract` ("O CPF informado é inválido para cadastro" / "O CNPJ informado é inválido para cadastro"). Ambas respondem HTTP 400.
- ✅ **Vínculo CPF–CNPJ:** `GET /people/check/cnpj/{cnpj}?data=<cpf>` executa a mesma validação do CPF e grava o CNPJ no desafio como `associatedPersonId`. O CNPJ da rota **não é validado** neste momento; é conferido apenas na resposta ao desafio ([[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Resposta-ao-Desafio|Fluxo de resposta]]).
- ✅ **Abertura do desafio** (`ChallengeQuestionCreate.createChallengeContract`): se o resultado é `ChallengeContract` (sucesso), grava um `Challenge` no MongoDB e devolve `ResponseChallengeContract` com o id e, **somente para CPF**, três passos (`steps`). Para CNPJ avulso o retorno traz o id sem passos.
- ✅ Perguntas (configuradas em `pf.challenge.question.*`): "Qual o seu primeiro nome ?", "Qual o primeiro nome da sua mae ?", "Qual sua data de nascimento ?"; o item mostra o primeiro nome com `_` no lugar de cada letra e a data como `__/__/____`.
- ✅ Se a entrada não tem 11 nem 14 dígitos, o resolvedor escolhe o serviço de desafio; como a entrada é texto, a primeira etapa é `NaturalPersonPreValidate` e falha (400 `invalidRequestContract`).

## Inferências e limitações
- 🔴 ✅ **Vazamento de tamanho:** o mascaramento preserva o número de letras do primeiro nome da pessoa e do primeiro nome da mãe, antes de qualquer prova de identidade. O endpoint só exige chave de API, mas o dado é devolvido ao chamador (o backend consumidor), que pode repassar ao cidadão.
- 🔶 `GET /people/check/cnpj/{cnpj}` não impede associar qualquer CNPJ; a verificação ocorre apenas na resposta.
- 🔶 O `PeopleController` recebe `IChallengeQuestionMapper` no construtor e não o usa.
- Regras: [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Elegibilidade-Cadastral|Elegibilidade cadastral]].

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Consulta-e-Geracao-de-Desafio|Fluxo de consulta e geração de desafio]] · [[01-Sistemas/PeoplesCheck/Servico/06-API/PeoplesCheck-Servico-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]] · [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Arquitetura|Arquitetura]]

## Pendências e próximo passo
- Confirmar com o consumidor (PARTICIPA-DF) como o resultado de CNPJ sem passos é usado.
