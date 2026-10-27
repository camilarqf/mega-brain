---
type: persistence
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - persistencia
  - couchdb
  - mongodb
sources:
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/couchdb
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/mongodb
  - src/main/java/br/gov/df/peoplescheckapi/domain/IChallengeCache.java
  - src/main/java/br/gov/df/peoplescheckapi/domain/Challenge.java
---
# PeoplesCheck Serviço — banco e persistência

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Descrever os dois bancos, as coleções e as consultas. Endereços, usuários e senhas não são registrados.

## Evidências
- `CouchDbClient`, `NaturalPersonRepository`, `JuridicalPersonRepository`, mapeadores em `infrastructure/couchdb/mappers`.
- `ChallengeCacheDAO`, `MongoConfig`.

## Informações confirmadas
**CouchDB (somente leitura, cadastro de pessoas)**
| Banco/coleção | Consulta | Campos lidos |
|---|---|---|
| `chcpf_replica` | `POST /chcpf_replica/_find` com `{"selector":{"_id":{"$eq":"<cpf>"}},"limit":1}` | `_id`, `nomeContribuinte`, `nomeMae`, `dtNasc` (`yyyyMMdd`), `codSitCad` |
| `chcnpj_replica` | duas consultas `_find` por `_id`: o **CNPJ base** (8 primeiros dígitos) e o **CNPJ completo** | base: `_id`, `nomeEmpresarial`, `naturezaJuridica`; completo: `dataInicioAtividade`, `situacaoCadastral`, `nomeFantasia` |

- ✅ `CouchDbClient.find` monta a URL (`couchdb.uri` + caminho), autentica com Basic (cabeçalho montado à mão e também `CredentialsProvider`) e lê a resposta inteira como `String`.
- ✅ `HttClientFactory.getDefault`: pool com `couchdb.pool.maxTotal` = 100 e `maxPerRoute` = 50; **confia em qualquer certificado e ignora o nome do host** (`loadTrustMaterial` aceitando tudo e `NoopHostnameVerifier`).
- ✅ Os nomes das réplicas (`*_replica`) indicam cópia de uma base de origem (🔶; a origem e a sincronização não constam no repositório).

**MongoDB (leitura e escrita, desafios)**
| Coleção | Documento | Escrita |
|---|---|---|
| `challenges` | `_id` (UUID em texto), `personId` (CPF ou chave informada), `associatedPersonId` (CNPJ, opcional), `expirationDate` (data/hora da criação), `countTry` (inteiro, inicia em 0) | `insertOne` na abertura do desafio; `$inc countTry` a cada resposta errada; `deleteOne` e `deleteMany` na limpeza |

- ✅ O DAO usa a API de baixo nível (`MongoTemplate.getCollection`) e não o mapeamento de `@Document`; `MongoConfig` cria `MongoClient` e `MongoTemplate` a partir de `spring.data.mongodb.uri` e `spring.data.mongodb.database` (valores por perfil, omitidos).
- ✅ **O campo `expirationDate` é gravado com `new Date()`** (momento de criação), não com um vencimento futuro. A "expiração" real é o apagamento por `deleteOldChallenges` (`expirationDate <= data de referência`).
- ✅ Não há índices, TTL nem migrations no repositório.
- ✅ **Contagem de tentativas** (`countLastTryByPersonId` e `countLastTryByAssociatedPersonId`): somam `countTry` dos desafios da pessoa (ou da pessoa associada). O filtro monta um `Document` com a chave `expirationDate` **duas vezes** (`$gte` 24 h atrás e `$lt` agora); a segunda `append` substitui a primeira, de modo que só vale `expirationDate < agora`. A janela de 24 h portanto não é aplicada na consulta; vale a limpeza dos desafios com mais de 24 h. Ver [[01-Sistemas/PeoplesCheck/Servico/04-Regras-de-Negocio/PeoplesCheck-Servico-Regra-Limite-de-Tentativas|Limite de tentativas]].
- ✅ `countLastTryByPersonId` filtra `associatedPersonId = null`; `countLastTryByAssociatedPersonId` não filtra o `personId`.

## Inferências e limitações
- 🔴 ✅ O seletor do CouchDB é montado por **concatenação de texto** com o dado informado, sem escape (ver [[01-Sistemas/PeoplesCheck/Servico/09-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos técnicos]]).
- 🔶 `JuridicalPersonRepository.getJuridicalSubsidiaryPersonMapper` usa `docs[0]` sem checar vazio (exceção se o CNPJ completo não existir, embora a base exista).
- 🔶 `NaturalPersonMapper` e `JuridicalSubsidiaryPersonMapper` usam `Integer.parseInt` da situação (exceção se o campo vier nulo).
- 🔶 `CouchDBHealthCheck` cria um novo cliente HTTP (e um novo pool) a cada verificação, sem fechar.

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-CouchDB|Integração CouchDB]] · [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-MongoDB|Integração MongoDB]] · [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Modelo-de-Dominio|Modelo de domínio]]

## Pendências e próximo passo
- Confirmar origem das réplicas e se o MongoDB tem índice/TTL criado fora do repositório.
