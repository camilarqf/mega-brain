---
type: index
aliases:
  - "Autenticação e identidade"
status: pendente
updated: 2026-10-28
tags:
  - autenticacao
---
# Autenticação e identidade

Voltar: [[Home]] · [[Mapa-de-Integracoes|Mapa de integrações]]

Tema transversal: como os sistemas autenticam usuários. Os fatos e a confirmação de cada relação vêm do [[Mapa-de-Integracoes|Mapa de integrações]]; aqui só se reúnem os caminhos.

## Visão geral
- ✅ O `KEYCLOAK-CGDF` autentica por Direct Grant chamando o `IBS` (`/auth`), que faz bind LDAP no `AD-LDAP` e lê vínculos e claims no `SIP-SQLServer`.
- ✅ O backend do `SICI` valida JWT do `Keycloak` (OIDC/JWKS) e chama o token endpoint e o userinfo. 🔶 A instância é a do `KEYCLOAK-CGDF`, autenticando no AD sem o IBS (informado pelo usuário).
- ✅ O backend do `Gerenciador-Portal` obtém token no `Keycloak` (`grant_type=password`). 🔶 A instância é a do `KEYCLOAK-CGDF`.
- ✅ O backend do `SCI` autentica usuários chamando o `PARTICIPA-DF`.
- 🔶 Os frontends do `PARTICIPA-DF` fazem login assistido por `sessionId`; o emissor não foi identificado.

## Por sistema
- **KEYCLOAK-CGDF:** [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo Direct Grant]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integração Keycloak → IBS]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/06-API/KEYCLOAK-CGDF-Servico-Contrato-Token-Endpoint|Contrato do token endpoint]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Claims]]
- **IBS:** [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo de autenticação]] · [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-AD-LDAP|IBS → AD]] · [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-SIP-SQLServer|IBS → SIP]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Claims|Claims]]
- **SICI:** [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Autenticacao|Backend]] · [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Autenticacao|Frontend]] · [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas|Integrações externas]]
- **Gerenciador-Portal:** [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Login-e-Autorizacao|Login e autorização]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SSO-Keycloak|Gerenciador → SSO]]
- **SCI:** [[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Autenticacao|Backend]] · [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Autenticacao|SCI → PARTICIPA-DF]] · [[01-Sistemas/SCI/Frontend/05-Fluxos/SCI-Frontend-Fluxo-Autenticacao|Frontend]]
- **PARTICIPA-DF:** [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Backend]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Autenticacao|Cidadão]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Autenticacao|Ouvidoria]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Autenticacao|SIC]]

## Todas as notas com a tag `autenticacao`
```base
filters:
  and:
    - file.hasTag("autenticacao")
views:
  - type: table
    name: Autenticação
    groupBy:
      property: system
      direction: ASC
    order:
      - file.name
      - type
      - status
```

## Hipóteses
Ver a seção "Relações não confirmadas" do [[Mapa-de-Integracoes|Mapa de integrações]].
