---
type: flow
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - fluxo
  - desafio
sources:
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/ChallengeController.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/NaturalPersonChallengeValidationService.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/ChallengeTimeExpiredValidation.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/stepValidations/NaturalPersonChallengeAnswerValidate.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/util/StringUtil.java
---
# PeoplesCheck Serviço — fluxo de resposta ao desafio

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Descrever `POST /challenge/check`, que confere as respostas e devolve os dados principais.

## Evidências
- `ChallengeController.check`, `NaturalPersonChallengeValidationService`, `ChallengeTimeExpiredValidation`, `NaturalPersonChallengeAnswerValidate`.

## Informações confirmadas
1. ✅ O consumidor envia `{"challenge": {"id": "<uuid>", "keys": ["<primeiro nome>", "<primeiro nome da mãe>", "<dd/MM/yyyy>"]}}`.
2. ✅ O controller sempre escolhe o serviço de desafio (`ValidationTypeResolver.resolvesByData("")` → `CHALLENGE`). Como a entrada não é texto, não há pré-validação de CPF.
3. ✅ **Etapa 1 (`ChallengeTimeExpiredValidation`):** lê o total de tentativas da pessoa do desafio. Se o desafio não existe → `InvalidAnswerContract`; se há 3 ou mais → `LimitExceeded`; senão segue ([[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Limite-de-Tentativas|Limite de tentativas]]).
4. ✅ **Etapa 2 (`NaturalPersonChallengeAnswerValidate`):** relê o desafio e o cadastro do CPF (`personId`):
   - pessoa inexistente ou irregular → `EntityNotFoundContract` ("A resposta para o desafio está incorreta");
   - qualquer resposta divergente ([[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Comparacao-de-Respostas|regra de comparação]]) → incrementa `countTry` (+1) e devolve `InvalidAnswerContract`;
   - tudo correto e **com CNPJ associado apto** → devolve os dados da empresa;
   - tudo correto e sem CNPJ, ou com CNPJ inexistente/inapto → devolve os dados da pessoa física.
5. ✅ Resposta: sucesso **200** `challengeSolvedContract` com `challenge.keys`; falhas **400**.

| Entrada | Saída | HTTP |
|---|---|---|
| desafio inexistente | `invalidAnswerContract` | 400 |
| 3 tentativas erradas acumuladas | `limitedExceeded` | 400 |
| resposta errada | `invalidAnswerContract` (+1 tentativa) | 400 |
| CPF irregular/inexistente | `entityNotFoundContract` | 400 |
| resposta correta | `challengeSolvedContract` | 200 |

## Inferências e limitações
- 🔴 ✅ Um CNPJ associado inexistente ou inapto **não gera erro**: o serviço devolve silenciosamente os dados da pessoa física, e o consumidor pode confundir o resultado com o vínculo validado (a diferença é a quantidade e a ordem de `keys`: PF tem [nome, data, mãe, CPF] e PJ [razão social, fantasia, natureza, CNPJ]).
- 🔶 O desafio não é invalidado após o sucesso: a mesma `id` pode ser reutilizada para obter novamente os dados (até a limpeza).
- 🔶 `keys` com menos de três itens → exceção não tratada (5xx).
- 🔶 Duas requisições simultâneas passam pela etapa 1 antes do incremento (verificação e escrita não são atômicas), então o limite de 3 pode ser excedido em paralelo; combina com o estado compartilhado descrito em [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Arquitetura|Arquitetura]].

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Consulta-e-Geracao-de-Desafio|Fluxo de consulta]] · [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]] · [[01-Sistemas/PeoplesCheck/Servico/09-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Confirmar como o consumidor distingue resposta de PF e de PJ.
