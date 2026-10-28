---
type: business-rule
aliases:
  - "PeoplesCheck Serviço — regra: comparação das respostas do desafio"
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
sources:
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/NaturalPersonChallengeAnswerValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/util/StringUtil.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/NaturalPerson.java
  - src/test/java/br/gov/df/peoplescheckapi/unitTests/applicationTests/NaturalPersonChallengeAnswerValidateTest.java
---
# PeoplesCheck Serviço — regra: comparação das respostas do desafio

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar como cada resposta é comparada ao cadastro.

## Evidências
- `NaturalPersonChallengeAnswerValidate.isAnswerInvalid`, `StringUtil.comparaComNormalizacao`, `NaturalPerson.getFormateData`.
- Teste `NaturalPersonChallengeAnswerValidateTest` (3 casos; não executado).

## Informações confirmadas
| Resposta | Posição em `keys` | Comparação |
|---|---|---|
| Primeiro nome | 0 | igual ao primeiro nome do cadastro, **sem acentos e sem diferença de maiúsculas** (`Normalizer NFD`, remove não ASCII, minúsculas) |
| Primeiro nome da mãe | 1 | igual ao primeiro nome da mãe no cadastro, com a mesma normalização |
| Data de nascimento | 2 | texto **idêntico** a `dd/MM/yyyy` (a data do cadastro `yyyyMMdd` é reformatada) |

- ✅ Basta uma divergência para a resposta ser inválida (as três precisam conferir).
- ✅ "Primeiro nome" é a primeira palavra separada por espaço.
- ✅ Efeito da divergência: `countTry` do desafio +1 ([[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Limite-de-Tentativas|Limite de tentativas]]).

## Inferências e limitações
- 🔶 `StringUtil.normalizar` remove caracteres não ASCII (inclusive os que não são acento, como `ç` vira `c` mas letras não latinas desaparecem). Nomes com apóstrofo ou hífen no primeiro token são comparados literalmente.
- 🔶 Entradas com espaços extras ou com `null` em `keys` geram exceção (`trim` não é aplicado; `normalizar(null)` falha).
- 🔶 Se `getFormateData()` falha o parse, devolve `null` e a comparação lança `NullPointerException`.

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Resposta-ao-Desafio|Fluxo de resposta]] · [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]]

## Pendências e próximo passo
- Nenhuma específica.
