---
type: index
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - moc
  - backend
---
# IBS — Backend (índice)

Sistema: [[01-Sistemas/IBS/IBS-Index|IBS]] · [[01-Sistemas/IBS/IBS-Repositorios|Repositórios]] · [[01-Sistemas/IBS/IBS-Contexto-do-Sistema|Contexto]]

> Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ Repositório `identity-broker-service`: API Spring Boot que autentica usuários por bind LDAP e devolve claims do SIP. Evidência: `pom.xml`, `IdentityBrokerServiceApplication`, `LoginController`.

## Mapa

### 01 — Visão geral
- [[01-Sistemas/IBS/Backend/01-Visao-Geral/IBS-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/IBS/Backend/01-Visao-Geral/IBS-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]] · [[01-Sistemas/IBS/Backend/01-Visao-Geral/IBS-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

### 02 — Domínio e persistência
- [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Modelo-de-Claims|Modelo-de-Claims]] · [[01-Sistemas/IBS/Backend/02-Dominio/IBS-Backend-Banco-SIP|Banco-SIP]]

### 03 — Módulos e regras de negócio
- [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Autenticacao-de-Usuario|Autenticacao-de-Usuario]] · [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Fontes-de-Autenticacao|Fontes-de-Autenticacao]] · [[01-Sistemas/IBS/Backend/03-Modulos/IBS-Backend-Consulta-de-Usuarios|Consulta-de-Usuarios]]
- [[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Ordem-de-Tentativa-LDAP|Regra-Ordem-de-Tentativa-LDAP]] · [[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Vinculo-Ativo-e-Matricula|Regra-Vinculo-Ativo-e-Matricula]] · [[01-Sistemas/IBS/Backend/04-Regras-de-Negocio/IBS-Backend-Regra-Mapeamento-de-Erros-HTTP|Regra-Mapeamento-de-Erros-HTTP]]

### 04 a 08 — Fluxo, API, segurança, integrações, qualidade
- [[01-Sistemas/IBS/Backend/05-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]] · [[01-Sistemas/IBS/Backend/06-API/IBS-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] · [[01-Sistemas/IBS/Backend/08-Seguranca/IBS-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]
- [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-AD-LDAP|Integracao-AD-LDAP]] · [[01-Sistemas/IBS/Backend/07-Integracoes/IBS-Backend-Integracao-SIP-SQLServer|Integracao-SIP-SQLServer]]
- [[01-Sistemas/IBS/Backend/09-Qualidade/IBS-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/IBS/Backend/09-Qualidade/IBS-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

### 99 — Controle
- [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Registro-de-Analise|Registro-de-Analise]] · [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Pendencias|Pendencias]]

## Principais pontos de atenção (resumo de [[01-Sistemas/IBS/Backend/09-Qualidade/IBS-Backend-Debitos-Tecnicos|Debitos-Tecnicos]])
1. Nenhuma rota tem controle de acesso; o `X-IBS-Secret` enviado pelo Keycloak não é validado.
2. LDAP em `ldap://` e várias tentativas de bind por senha errada.
3. Cache de fonte recente sem limite; erros de banco e "órgão sem fonte" viram 500.

## Inferências e limitações
- Cobertura parcial: lotes 0 a 4 concluídos; `Consulta-de-Usuarios`, `Seguranca` e `Testes` com cobertura parcial (SQL e testes lidos por amostra).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Registro-de-Analise|Registro de análise]].
