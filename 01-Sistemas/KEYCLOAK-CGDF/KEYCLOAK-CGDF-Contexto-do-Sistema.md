---
type: system
system: KEYCLOAK-CGDF
repository: keycloak
status: pendente
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - keycloak-cgdf
  - contexto
sources:
  - README.md
  - providers/pom.xml
  - .docker/Dockerfile
---
# KEYCLOAK-CGDF — contexto do sistema

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Index|KEYCLOAK-CGDF]]

## Objetivo
✅ Fornecer uma instância de Keycloak da CGDF que emite os tokens OIDC. O repositório empacota a imagem (Keycloak + driver MSSQL), uma extensão Java (SPI) e um tema de login.

## Evidências
- `README.md`: "Extensao Java pura para Keycloak 26.3.2. O provider autentica usuarios no IBS durante o fluxo Direct Grant e deixa o Keycloak como emissor do token."
- `.docker/Dockerfile`, `.jenkins-pipelines/*`: build e deploy por ambiente (Staging, Sandbox, Produção).
- `providers/src/main/java/br/gov/df/cg/ibs/keycloak/*`: authenticator, client, config e mapper.

## Informações confirmadas
- ✅ O repositório contém três partes: SPI `providers/`, empacotamento `.docker/` + `.jenkins-pipelines/` e tema `integra-login/`.
- ✅ A extensão autentica no **IBS** (Direct Grant) e injeta claims corporativas no token (detalhes em [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]]).
- ✅ Os ambientes e o banco (MSSQL) vêm dos arquivos de pipeline e do Dockerfile (valores omitidos).

## Inferências e limitações
- 🔶 Informado pelo usuário em 2026-10-18 (sem evidência no código): este é o Keycloak consumido pelo `SICI`, que **não** usa o componente IBS; o SICI usa o Keycloak integrado ao **AD**.
- ❓ A federação com o AD e a configuração de realms, clients e fluxos não estão neste repositório.
- ❓ Os consumidores do fluxo IBS (Direct Grant) não foram identificados.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Repositorios|Repositórios]] · [[Mapa-de-Integracoes|Mapa de integrações]]
- Consumidor conhecido (informado): [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas|Integrações externas do SICI Backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]].
