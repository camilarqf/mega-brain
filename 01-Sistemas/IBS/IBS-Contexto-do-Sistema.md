---
type: system
system: IBS
repository: identity-broker-service
status: confirmado
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - contexto
sources:
  - README.md
  - src/main/java/br/gov/df/cg/ibs/api/auth/LoginController.java
  - src/main/java/br/gov/df/cg/ibs/application/autenticacao/services/AutenticacaoService.java
---
# IBS — contexto do sistema

Voltar: [[01-Sistemas/IBS/IBS-Index|IBS]]

## Objetivo
✅ O IBS recebe login, senha e identificador do órgão (`POST /auth`), valida a credencial no Active Directory por bind LDAP com o próprio usuário e devolve claims institucionais montadas a partir do banco SIP. Não emite token: o Keycloak continua sendo a autoridade de sessão e de tokens (declarado no `README.md`; o código não emite JWT).

## Evidências
- `README.md` (responsabilidades e não responsabilidades); `LoginController`, `AutenticacaoService`, `ClaimsService`, `LdapBindService`.
- Informado pelo usuário em 2026-10-18: este repositório é o serviço chamado pelo Keycloak (`KEYCLOAK-CGDF`).

## Informações confirmadas
- ✅ Atores técnicos: Keycloak (consumidor de `POST /auth`), servidores AD/LDAP (validação de credencial) e SQL Server `DB_SIP` (vínculo, unidades e roteamento).
- ✅ Além de `/auth`, expõe consulta de usuários (`/usuarios/buscar`, `/usuarios/{idUsuario}`) e `/healthcheck`.
- ✅ Visão técnica: [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo de autenticação]], [[01-Sistemas/IBS/Backend/06-API/IBS-Backend-Catalogo-de-Endpoints|Endpoints]], [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-AD-LDAP|AD/LDAP]] e [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-SIP-SQLServer|SIP]].

## Inferências e limitações
- 🔶 O `README.md` descreve responsabilidades "futuras" (ex.: OIDC, consulta a fontes corporativas); o código analisado não expõe endpoints OIDC.
- ❓ Dono do serviço, SLA e outros consumidores além do Keycloak não identificados.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/IBS-Backend-Index|IBS Backend]] · [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Index|KEYCLOAK-CGDF]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Os atores de negócio (quem usa o login) dependem de confirmar consumidores e dono do serviço.
