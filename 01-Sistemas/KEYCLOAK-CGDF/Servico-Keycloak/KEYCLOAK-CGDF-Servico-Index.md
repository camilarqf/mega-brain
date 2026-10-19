---
type: index
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - keycloak-cgdf
  - moc
  - servico
---
# KEYCLOAK-CGDF — Serviço Keycloak (índice)

Sistema: [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Index|KEYCLOAK-CGDF]] · [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Repositorios|Repositórios]] · [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Contexto-do-Sistema|Contexto]]

> Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ Repositório `keycloak`: imagem Docker do Keycloak com extensão Java (SPI de autenticação via IBS e protocol mapper de claims) e tema de login. Evidência: `README.md`, `providers/pom.xml`, `.docker/Dockerfile`, `integra-login/login/theme.properties`.

## Mapa

### 01 — Visão geral
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Arquitetura-SPI|Arquitetura-SPI]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Build-e-Deploy|Build-e-Deploy]]

### 02 — Domínio
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]]

### 03 — Módulos e regras de negócio
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/03-Modulos/KEYCLOAK-CGDF-Servico-Tema-Integra-Login|Tema-Integra-Login]]
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/03-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Username-Interno-IdUsuario|Regra-Username-Interno-IdUsuario]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/03-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Validacao-do-Formulario|Regra-Validacao-do-Formulario]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/03-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Normalizacao-do-Usuario|Regra-Normalizacao-do-Usuario]]

### 04 a 08 — Fluxo, API, segurança, integrações, qualidade
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-API/KEYCLOAK-CGDF-Servico-Contrato-Token-Endpoint|Contrato-Token-Endpoint]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/06-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]]
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Qualidade/KEYCLOAK-CGDF-Servico-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Qualidade/KEYCLOAK-CGDF-Servico-Debitos-Tecnicos|Debitos-Tecnicos]]

### 99 — Controle
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Registro-de-Analise|Registro-de-Analise]] · [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendencias]]

## Principais pontos de atenção (resumo de [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Qualidade/KEYCLOAK-CGDF-Servico-Debitos-Tecnicos|Debitos-Tecnicos]])
1. README diz que o 403 do IBS vira `invalid_grant`; o código o trata como `server_error`.
2. Runtime `keycloak:25.0.2` vs. compilação 26.3.2 e README.
3. O tema `integra-login` não é copiado pelo Dockerfile.

## Inferências e limitações
- Realms, clients, federação com o AD e o IBS em si não estão no repositório. Cobertura parcial: tema só por inventário.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Registro-de-Analise|Registro de análise]].
