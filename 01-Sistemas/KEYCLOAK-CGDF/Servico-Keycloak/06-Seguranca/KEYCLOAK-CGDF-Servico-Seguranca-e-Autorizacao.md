---
type: security
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - keycloak-cgdf
  - seguranca
  - autenticacao
sources:
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticator.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsApiClient.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/config/IbsConfig.java
  - .docker/inject-docker-secrets-entrypoint.sh
  - .jenkins-pipelines/deployment.params.yml
---
# Segurança e autorização

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Qualidade/KEYCLOAK-CGDF-Servico-Debitos-Tecnicos|Debitos-Tecnicos]]

## Objetivo
Registrar controles de autenticação, tratamento de segredos e dados pessoais no repositório. Sem valores de segredos.

## Evidências
- Arquivos em `sources`; teste `mensagensDeErroNuncaIncluemPassword` (`IbsRestClientTest`).

## Informações confirmadas
**Autenticação**
- ✅ A senha é validada pelo IBS, não pelo Keycloak; o Keycloak não armazena credencial (nenhum `setCredential`/senha no código do SPI) e o usuário local é criado sem senha.
- ✅ O fluxo aceita `REQUIRED` ou `DISABLED` (`IbsAuthenticatorFactory`); `requiresUser()=false`.
- ✅ Falha de autenticação devolve 401 `invalid_grant`; falha técnica devolve 500 `server_error` sem detalhes internos.

**Segredos**
- ✅ Segredo compartilhado com o IBS: propriedade `ibs.shared-secret` (tipo `PASSWORD` no Admin Console), enviada no cabeçalho `X-IBS-Secret` quando não vazia; o log só informa se está configurado.
- ✅ A senha do usuário não é logada; mensagens de erro do cliente não a incluem (teste `mensagensDeErroNuncaIncluemPassword`).
- ✅ Banco e credenciais de administrador entram por secrets Swarm (`KC_DB_URL`, `KEYCLOAK_ADMIN`, `KEYCLOAK_ADMIN_PASSWORD`); o entrypoint os exporta como variáveis de ambiente e imprime só os nomes.

**Dados pessoais**
- ✅ Logs do SPI registram `login`, `idOrgao`, `correlationKey` e username interno (hash). Não registram senha.
- ✅ Atributos do usuário guardam nome, nome social e matrícula (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]]); esses dados vão ao token conforme o mapper associado ao client.

**Usuários locais**
- ✅ Todo usuário criado fica `enabled`, e-mail verificado e sem required actions ([[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/03-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Normalizacao-do-Usuario|Regra-Normalizacao-do-Usuario]]).

## Inferências e limitações
- 🔶 O README mostra exemplo de `ibsBaseUrl` com `http://`; o protocolo real por ambiente não está no repositório (❓ se o tráfego ao IBS usa TLS).
- 🔶 `X-IBS-Secret` é opcional no código: sem a propriedade, a chamada segue sem segredo.
- ❓ Políticas de brute force, bloqueio e MFA do realm não estão no repositório.
- ❓ Autorização por client/escopo (quem pode usar o Direct Grant) depende da configuração do realm, ausente aqui.
- O arquivo `.idea/` está versionado (ver débitos); não foi verificado se contém dados sensíveis.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]]

## Pendências e próximo passo
- Confirmar TLS e rede entre Keycloak e IBS; ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]].
