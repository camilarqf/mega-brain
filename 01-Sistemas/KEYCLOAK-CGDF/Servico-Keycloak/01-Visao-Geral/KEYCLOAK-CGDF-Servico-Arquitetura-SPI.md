---
type: architecture
aliases:
  - "Arquitetura da extensão (SPI)"
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: completa
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
sources:
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticator.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticatorFactory.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsApiClient.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsRestClient.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/config/IbsConfig.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/config/IbsConfigResolver.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/mapper/IbsClaimsProtocolMapper.java
  - providers/src/main/resources/META-INF/services/org.keycloak.authentication.AuthenticatorFactory
  - providers/src/main/resources/META-INF/services/org.keycloak.protocol.ProtocolMapper
---
# Arquitetura da extensão (SPI)

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]]

## Objetivo
Descrever as classes do módulo `providers/` (pacote `br.gov.df.cg.ibs.keycloak`) e como o Keycloak as carrega.

## Evidências
- Arquivos listados em `sources`; registro por `ServiceLoader` nos dois arquivos de `META-INF/services`.

## Informações confirmadas
Duas extensões são registradas no Keycloak:

| Extensão | Classe | Provider ID | SPI Keycloak |
|---|---|---|---|
| Authenticator Direct Grant | `IbsAuthenticatorFactory` (cria `IbsAuthenticator`) | `ibs-authenticator` | `AuthenticatorFactory` |
| Protocol mapper OIDC | `IbsClaimsProtocolMapper` | `ibs-claims-protocol-mapper` | `ProtocolMapper` |

Classes de apoio (sem registro próprio):

| Pacote   | Classe                                 | Papel                                                                                   |
| -------- | -------------------------------------- | --------------------------------------------------------------------------------------- |
| `client` | `IbsApiClient`                         | Cliente HTTP (`java.net.http.HttpClient`) do `POST {base}/auth`                         |
| `client` | `IbsRestClient`                        | Fachada sobre `IbsApiClient` que recebe `IbsConfig`; `autenticar(...)`                  |
| `client` | `IbsLoginRequest` / `IbsLoginResponse` | Records do contrato JSON (`login`, `senha`, `idOrgao`) e da resposta (claims, unidades) |
| `config` | `IbsConfig`                            | Resolve URL, timeout e segredo (mapa → propriedade de sistema → variável de ambiente)   |
| `config` | `IbsConfigResolver`                    | Lê a configuração da execução (`AuthenticatorConfigModel`) no contexto do fluxo         |

Dependências entre classes: `IbsAuthenticator` → `IbsConfigResolver` → `IbsConfig`; `IbsAuthenticator` → `IbsApiClient` (via `Function<IbsClientSettings, IbsApiClient>` injetável para teste) → records `IbsLoginRequest`/`IbsLoginResponse`. `IbsClaimsProtocolMapper` não depende do cliente: lê atributos do usuário e notas da sessão.

Escolhas de projeto visíveis no código:
- `IbsAuthenticator` estende `AbstractDirectGrantAuthenticator` e usa `failureChallenge` com `errorResponse` (README, troubleshooting).
- `requiresUser()` = `false` e `configuredFor` = `true`; `getRequirementChoices` = `REQUIRED`/`DISABLED` (`IbsAuthenticatorFactory.REQUIREMENT_CHOICES`).
- O mapper expõe os toggles "Add to access token / ID token / userinfo" via `OIDCAttributeMapperHelper.addIncludeInTokensConfig`.

## Inferências e limitações
- 🔶 `IbsAuthenticator` repete os metadados de `IbsAuthenticatorFactory` (id, tipo, ajuda, propriedades); há duplicação de definição, sem impacto funcional aparente.
- ✅ `IbsRestClient` não é referenciado por nenhuma outra classe do repositório (busca por `IbsRestClient` em `providers/src`): `IbsAuthenticator` usa `IbsApiClient` direto, e `IbsRestClientTest` (apesar do nome) testa `IbsApiClient`. A classe parece código morto.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Nenhuma específica.
