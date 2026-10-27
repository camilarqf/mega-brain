---
type: domain
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: completa
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - keycloak-cgdf
  - claims
  - token
  - dominio
sources:
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsLoginResponse.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticator.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/mapper/IbsClaimsProtocolMapper.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/mapper/IbsClaimsMapperTest.java
---
# Modelo de claims (IBS → usuário Keycloak → token)

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Arquitetura-SPI|Arquitetura-SPI]]

## Objetivo
Mapear cada dado devolvido pelo IBS até o atributo do usuário, a nota de sessão e a claim do token. Não contém dados reais.

## Evidências
- `IbsLoginResponse` (records `Claims`, `Unidade`), `IbsAuthenticator.updateUser/setUserSessionNotes`, `IbsClaimsProtocolMapper.addClaims`, `IbsClaimsMapperTest`.

## Informações confirmadas
| Campo do IBS                                                   | Atributo do usuário                     | Nota de sessão          | Claim no token                             | Observação                                                       |
| -------------------------------------------------------------- | --------------------------------------- | ----------------------- | ------------------------------------------ | ---------------------------------------------------------------- |
| `idUsuario`                                                    | `idUsuario` (e **username** do usuário) | `idUsuario`, `username` | `preferred_username` (= username)          | Obrigatório; não vai como claim própria                          |
| `login`                                                        | `login` (ou o `username` informado)     | `login`                 | `login`                                    |                                                                  |
| `autenticado`                                                  | `autenticado`                           | `autenticado`           | `autenticado` (booleano)                   |                                                                  |
| `idOrgao` (inteiro)                                            | `idOrgao`                               | `idOrgao`               | `idOrgao` (inteiro; texto se não numérico) | Sem valor no IBS, usa o `idOrgao` do formulário                  |
| `siglaOrgao`                                                   | `siglaOrgao`                            | `siglaOrgao`            | `siglaOrgao`                               |                                                                  |
| `nomeOrgao`                                                    | `nomeOrgao`                             | `nomeOrgao`             | `nomeOrgao`                                |                                                                  |
| `nomePessoa`                                                   | `nomePessoa`; também `firstName`        | `nomePessoa`            | `nomePessoa`                               | `firstName` cai para o `username` informado; `lastName` fixo `-` |
| `nomeSocial`                                                   | `nomeSocial`                            | `nomeSocial`            | `nomeSocial`                               |                                                                  |
| `matricula`                                                    | `matricula`                             | `matricula`             | `matricula`                                | Valor aparado (`trim`)                                           |
| `unidades[]` (`idUnidade`, `siglaUnidade`, `descricaoUnidade`) | `unidades` (string JSON)                | `unidades`              | `unidades` (array JSON real)               | Só se não vazio                                                  |
| `correlationKey`                                               | `correlationKey`                        | `correlationKey`        | **não** vai ao token                       |                                                                  |

Regras do mapper (`IbsClaimsProtocolMapper`):
- Para cada nome, lê primeiro o atributo do usuário e, se vazio, a nota de sessão.
- Define `preferred_username` com o username do usuário.
- Falha ao desserializar `unidades` gera aviso no log e a claim é omitida.
- Teste `naoAdicionaClaimsRemovidas`: o token não recebe `dominioOrigem`, `correlationId`, `correlationKey`, `sub`, `email`, `perfil`, `status`.

**Histórico (conforme mensagens de commit; diffs não lidos):**
- 2026-07-09 (`33cde3e`): username interno = hash de login, matrícula e órgão. Substituído em 2026-07-17 (`5c4fe98`) pelo `idUsuario` do IBS.
- 2026-08-14 (`46f5747`): `idUnidade` adicionado às unidades.

## Inferências e limitações
- 🔶 O significado de negócio de cada campo (órgão, unidade, matrícula) vem só dos nomes; o IBS não está neste repositório.
- 🔶 Que `idUsuario` seja "o hash gerado pelo processo ETL na origem" é afirmação do README, não verificável aqui.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Username-Interno-IdUsuario|Regra-Username-Interno-IdUsuario]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Confirmar com o time do IBS o contrato oficial (campos opcionais e tipos).
