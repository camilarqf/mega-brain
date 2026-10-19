---
type: index
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
created: 2026-10-19
updated: 2026-10-19
tags:
  - sci
  - moc
  - backend
---

# SCI — Backend (índice)

Sistema: [[01-Sistemas/SCI/SCI-Index|SCI]] · [[01-Sistemas/SCI/SCI-Repositorios|Repositórios]] · [[01-Sistemas/SCI/SCI-Contexto-do-Sistema|Contexto do sistema]]

> MOC da base técnica do **sci-backend**. Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ API REST em ASP.NET Core (.NET 10) para gestão de **denúncias, demandas, processos de admissibilidade e processos investigativos preliminares (PIP)**, com CQRS, eventos de domínio gravados em um event store, mensageria RabbitMQ com o `PARTICIPA-DF` e geração de documentos assinados (nota técnica, minuta, relatório).
Evidência: `src/SCI.Api/Program.cs`, `src/SCI.Domain/*`.

## Mapa

### 01 — Visão geral
- [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Arquitetura-CQRS-e-Event-Sourcing|Arquitetura-CQRS-e-Event-Sourcing]] · [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Glossario|Glossario]]

### 02 — Domínio
- [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Enums-e-Estados]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Banco-e-Migrations|Banco-e-Migrations]]

### 03 — Módulos
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Denuncia-e-Demanda]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Processo-de-Admissibilidade]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Encaminhamento|Encaminhamento]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]]
- [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Documentos-e-Assinaturas|Documentos-e-Assinaturas]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Unidade-e-Configuracao|Unidade-e-Configuracao]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Identidade-e-Permissoes|Identidade-e-Permissoes]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Cadastros-de-Apoio|Cadastros-de-Apoio]]

### 04 — Fluxos
- [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo-Denuncia-ate-Admissibilidade]] · [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Ciclo-do-PIP|Fluxo-Ciclo-do-PIP]] · [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]]

### 05 a 08 — API, segurança, integrações, qualidade
- [[01-Sistemas/SCI/Backend/05-API/SCI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] · [[01-Sistemas/SCI/Backend/06-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integracoes-Externas]]
- [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

### 99 — Controle
- [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Registro-de-Analise|Registro-de-Analise]] — commit analisado, cobertura por lote
- [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendencias]] — dúvidas a confirmar com o time

## Principais riscos (resumo de [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Debitos-Tecnicos]])
1. 🔴 Bypass de autenticação por lista fixa de CPFs e senha fixa no código.
2. 🔴 Segredos (JWT, BCadastro) versionados em `appsettings*.json`.
3. 🟡 `POST /support/generate-database` anônimo e destrutivo; segundo o usuário só funciona em dev e local (barrado por feature flag).
4. 🟠 `DELETE /unidade/{id}` sem política; download de arquivo com validação mínima.

## Números rápidos (commit `8e3c8648`)
| Item | Quantidade |
|---|---|
| Controllers REST / atributos HTTP | 33 / 142 |
| Arquivos `.cs` por projeto (principais) | Domain 332 · Projections 266 · Api 209 · Application 179 · Data 122 |
| Tabelas mapeadas (EF) / scripts SQL | 58 mappings (Default) + `TB_EVENTO` / 28 |
| Eventos de integração | 3 (`denuncia-registrada`, `denuncia-aceita`, `denuncia-recusada`) |
| Métodos de teste | 7 |

## Política desta base
- Não contém valores de configuração, segredos, CPFs, senhas, endereços de infraestrutura nem dados reais.
- A POC de login por SSO (não commitada) está **fora do escopo** por decisão do usuário.
