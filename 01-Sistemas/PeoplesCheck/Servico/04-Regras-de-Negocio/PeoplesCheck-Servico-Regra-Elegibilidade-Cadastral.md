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
  - situacao-cadastral
sources:
  - src/main/java/br/gov/df/peoplescheckapi/domain/NaturalPerson.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/JuridicalPerson.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/NaturalPersonPreValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/JuridicalPersonPreValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/NaturalPersonEntityValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/JuridicalPersonEntityValidate.java
---
# PeoplesCheck Serviço — regra: elegibilidade cadastral

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar quais documentos o serviço aceita para abrir um desafio.

## Evidências
- Métodos `isRegular()` (`NaturalPerson`) e `isAble()` (`JuridicalPerson`); etapas de pré-validação e de entidade.

## Informações confirmadas
- ✅ **CPF:** é aceito somente se (a) tem 11 dígitos após remover não dígitos, (b) não tem todos os dígitos iguais, (c) os dois dígitos verificadores conferem (módulo 11) e (d) a pessoa existe na réplica de CPF com situação **0 (`REGULAR`)**. Qualquer outra situação (suspensa, falecida, pendente, cancelada por multiplicidade, nula, cancelada de ofício) é recusada.
- ✅ **CNPJ:** é aceito somente se (a) tem 14 dígitos, (b) os dois dígitos verificadores conferem e (c) a empresa existe na réplica de CNPJ com situação diferente de **8 (`CANCELED`)** e de **1 (`NULL`)**. Situações 2 a 5 (ativa, suspensa, inapta, ativa não regular) são aceitas, assim como valores não listados no enum.
- ✅ Resultado de recusa: HTTP 400 com `invalidRequestContract` (formato/dígitos) ou `entityNotFoundContract` (inexistente/inelegível, com mensagem "O CPF/CNPJ informado é inválido para cadastro").
- ✅ O mesmo critério (`isRegular` / `isAble`) é reaplicado na resposta ao desafio ([[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Resposta-ao-Desafio|Fluxo de resposta]]).

## Inferências e limitações
- ✅ As regras de negócio do serviço vieram da Ouvidoria, dona do negócio do `PARTICIPA-DF` (informado pelo usuário em 2026-10-19).
- 🔶 A diferença de rigor entre PF (só regular) e PJ (quase tudo exceto cancelada/nula) pode ser intencional; ❓ o motivo específico de aceitar CNPJ suspenso/inapto não foi informado.
- 🔶 A mensagem "inválido para cadastro" indica que o serviço serve ao cadastro de cidadão/empresa no consumidor.
- Testes da pré-validação existem (7 casos de CPF e 7 de CNPJ; não executados).

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Modelo-de-Dominio|Modelo de domínio]] · [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Validacao-de-Pessoa|Validação de pessoa]]

## Pendências e próximo passo
- Confirmar com o dono se aceitar CNPJ suspenso/inapto é intencional.
