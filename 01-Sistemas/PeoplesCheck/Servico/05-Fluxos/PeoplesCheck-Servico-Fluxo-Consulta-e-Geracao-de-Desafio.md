---
type: flow
aliases:
  - "PeoplesCheck Serviço — fluxo de consulta e geração de desafio"
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
sources:
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/PeopleController.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/ValidationTypeResolver.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/ChallengeQuestionCreate.java
  - src/main/java/br/gov/df/peoplescheckapi/application/service/ChallengeQuestionMapper.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/mongodb/ChallengeCacheDAO.java
---
# PeoplesCheck Serviço — fluxo de consulta e geração de desafio

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Descrever, do pedido à resposta, o que ocorre em `GET /people/check?data=` e `GET /people/check/cnpj/{cnpj}?data=`.

## Evidências
- `PeopleController.check` (duas sobrecargas), `ValidationTypeResolver`, `ValidationFactory`, `ChallengeQuestionCreate`.

## Informações confirmadas
Atores: sistema consumidor (ex.: backend do `PARTICIPA-DF`), PeoplesCheck, CouchDB, MongoDB.

1. ✅ O consumidor envia `data` (CPF, ou CNPJ) com o cabeçalho de chave de API. O filtro rejeita chave inválida ([[01-Sistemas/PeoplesCheck/Servico/08-Seguranca/PeoplesCheck-Servico-Seguranca-e-Autorizacao|Segurança]]).
2. ✅ `ValidationTypeResolver` conta os dígitos de `data`: 11 → CPF; 14 → CNPJ; outro → serviço de desafio (que falha na pré-validação).
3. ✅ O serviço executa a cadeia: **pré-validação** (formato e dígitos verificadores) → **busca no CouchDB** e checagem da situação cadastral ([[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Elegibilidade-Cadastral|regra]]). Qualquer falha interrompe e responde **400** com o contrato de falha.
4. ✅ Em caso de sucesso, `ChallengeQuestionCreate` grava no MongoDB um `Challenge` (`personId` = `data` informado, `associatedPersonId` = CNPJ da rota, se houver; `countTry` = 0) e relê o documento pelo id gerado.
5. ✅ Para CPF, monta três passos com as perguntas e os itens mascarados ([[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Validacao-de-Pessoa|Validação de pessoa]]); para CNPJ avulso não há passos.
6. ✅ Responde **200** com `challengeContract` contendo `responseChallenge.id` e `steps`.
7. ➜ O consumidor apresenta as perguntas ao cidadão e segue para o [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Resposta-ao-Desafio|fluxo de resposta]].

Falhas:
| Situação | Resultado |
|---|---|
| dígitos inválidos ou tamanho diferente de 11/14 | 400 `invalidRequestContract` |
| CPF/CNPJ inexistente ou inapto | 400 `entityNotFoundContract` |
| CouchDB indisponível | exceção (`IOException`) não tratada → erro 5xx (🔶 resposta exata depende do tratador padrão do Spring) |
| falha na gravação no MongoDB | `insertChallenge` devolve `null` e o código seguinte lança `NullPointerException` → 5xx (✅ no código) |

## Inferências e limitações
- 🔶 Cada consulta bem-sucedida cria um novo desafio; consultas repetidas geram vários documentos (e o contador de tentativas soma todos).
- ❓ Se o consumidor trata o 5xx e o 400 de modo distinto.

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/06-API/PeoplesCheck-Servico-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco e persistência]]

## Pendências e próximo passo
- Nenhuma específica.
