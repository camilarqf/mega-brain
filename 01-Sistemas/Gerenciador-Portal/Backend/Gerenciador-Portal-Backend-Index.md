---
type: index
aliases:
  - "Gerenciador-Portal — Backend (índice)"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
---
# Gerenciador-Portal — Backend (índice)

Sistema: [[01-Sistemas/Gerenciador-Portal/Gerenciador-Portal-Index|Gerenciador-Portal]] · [[01-Sistemas/Gerenciador-Portal/Gerenciador-Portal-Repositorios|Repositórios]]

> MOC do **gerenciador-portal-backend** (commit `14b185f`). Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ API REST em Spring Boot 1.5 (Java 8) que administra o conteúdo do Portal da Transparência: arquivos/relatórios por categoria e período, imagens (slideshow e painéis), textos das consultas, palavras-chave, órgãos da LAI, lista de medida protetiva (com expiração de cache via RabbitMQ) e consulta de cargas. Persiste em SQL Server e MongoDB, guarda arquivos no MinIO e autentica o operador pelo SSO (Keycloak). A API não valida token nas demais rotas.
Evidência: `pom.xml`, `api/*`, `services/*`, `config/*`.

## Mapa

### 01 — Visão geral
- [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]] · [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]] · [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Deploy-e-Pipeline|Deploy-e-Pipeline]]

### 02 — Domínio e persistência
- [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Banco-e-Persistencia|Banco-e-Persistencia]]

### 03 — Módulos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Arquivos-e-Relatorios]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Imagens-do-Portal|Imagens-do-Portal]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Conteudo-do-Portal|Conteudo-do-Portal]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Medida-Protetiva]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Cargas|Cargas]]

### 04 — Fluxos
- [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Login-e-Autorizacao|Login-e-Autorizacao]] · [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Cadastro-de-Arquivo|Cadastro-de-Arquivo]] · [[01-Sistemas/Gerenciador-Portal/Backend/05-Fluxos/Gerenciador-Portal-Backend-Fluxo-Expirar-Cache-Medida-Protetiva|Expirar-Cache-Medida-Protetiva]]

### 05 a 08 — API, segurança, integrações, qualidade
- [[01-Sistemas/Gerenciador-Portal/Backend/06-API/Gerenciador-Portal-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] · [[01-Sistemas/Gerenciador-Portal/Backend/08-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracoes-Externas|Integracoes-Externas]]: [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MinIO-S3|MinIO/S3]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SSO-Keycloak|SSO]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-RabbitMQ-Expirar-Cache|RabbitMQ]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MongoDB|MongoDB]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SQL-Server|SQL Server]]
- [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

### 99 — Controle
- [[01-Sistemas/Gerenciador-Portal/Backend/99-Controle/Gerenciador-Portal-Backend-Registro-de-Analise|Registro-de-Analise]] — lotes e próximo passo
- [[01-Sistemas/Gerenciador-Portal/Backend/99-Controle/Gerenciador-Portal-Backend-Pendencias|Pendencias]] — dúvidas a confirmar

## Principais riscos (resumo de [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Debitos-Tecnicos]])
1. 🔴 Credenciais versionadas nos `application-*.properties` (banco, MongoDB, RabbitMQ).
2. 🔴 API de escrita sem validação de identidade (basta `x-client-id`); CORS `*`; usuário de desenvolvimento em `prod`.
3. 🔴 Injeção de SQL em cargas, busca de servidores, medida protetiva e filtros de arquivos.
4. 🔴 Spring Data REST sem restrição pode expor os repositórios (a confirmar).
5. 🟠 Exclusão não remove o objeto do MinIO; armazenamento duplo (disco × S3).

## Números rápidos (commit `14b185f`)
| Item | Quantidade |
|---|---|
| Controllers | 10 (mais `PrometheusMetricsController`) |
| Entidades JPA / documentos Mongo | 11 / 1 |
| Integrações com nota canônica | 5 |
| Testes versionados | 3 (em 2 classes) |
