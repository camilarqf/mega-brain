---
type: integration
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
consumer: IBS
provider: AD-LDAP
tags:
  - ibs
  - integracao
  - ldap
  - active-directory
sources:
  - src/main/java/br/gov/df/cg/ibs/infra/ldap/LdapBindService.java
  - src/main/java/br/gov/df/cg/ibs/application/autenticacao/services/AutenticacaoService.java
  - src/test/java/br/gov/df/cg/ibs/infra/ldap/LdapBindServiceTest.java
---
# Integração IBS → AD (LDAP)

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `IBS` (`identity-broker-service`) | `AD-LDAP` | JNDI (`com.sun.jndi.ldap.LdapCtxFactory`), bind simples | bind com `login + sufixo` (UPN) ou `login` (displayName) e a senha do usuário | saída |

## Evidências
- `LdapBindService.montarAmbiente`, `autenticarNoServidor`, `montarBindDn`; testes `LdapBindServiceTest` (11 cenários, com `criarContexto` substituível).

## Informações confirmadas
- ✅ URL `ldap://<endereco>:<porta>` (endereços e portas vêm de `vw_autenticacao_sip`; não há `ldaps` nem StartTLS no código). `SECURITY_AUTHENTICATION=simple`.
- ✅ Só **valida a credencial**: abre o contexto e fecha; não faz busca de atributos (o `contexto_pesquisa` aparece apenas no log).
- ✅ Timeouts `com.sun.jndi.ldap.connect.timeout` e `read.timeout` = `ibs.ldap.timeout-ms` (3000 ms).
- ✅ Classificação: `AuthenticationException` → credencial inválida (código `data xxx` extraído da mensagem, minúsculo); `CommunicationException` → `TIMEOUT` se a causa for `SocketTimeoutException`, senão `CONN_REFUSED`; outras `NamingException` → `TIMEOUT` ou `UNAVAILABLE`.
- ✅ Logs com `correlationKey`, fonte, endereço, porta e latência; a senha não é registrada. O log de rejeição inclui a mensagem da exceção JNDI.
- ✅ Dependência síncrona do login: sem AD acessível para o órgão, `POST /auth` responde 503.

## Inferências e limitações
- 🔶 Tráfego `ldap://` sem TLS no código: a senha trafega em texto claro até o AD, a menos que a rede ou o AD imponham outra proteção (não verificado).
- ❓ Hosts, versões do AD, dono e SLA dos ADs não estão no repositório.
- Regras de repetição entre servidores: [[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Ordem-de-Tentativa-LDAP|Ordem de tentativa]].

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo]] · [[01-Sistemas/IBS/Backend/08-Seguranca/IBS-Backend-Seguranca-e-Autorizacao|Segurança]]

## Pendências e próximo passo
- Confirmar se o transporte é protegido por outro meio (rede, VPN) e quem é o dono dos ADs.
