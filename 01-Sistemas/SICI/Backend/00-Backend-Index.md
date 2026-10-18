---
type: index
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
created: 2026-10-16
updated: 2026-10-18
tags:
  - sici
  - moc
  - backend
---

# SICI — Backend (índice)

Sistema: [[01-Sistemas/SICI/SICI-Index|SICI]] · [[01-Sistemas/SICI/Repositorios|Repositórios]] · [[01-Sistemas/SICI/Contexto-do-Sistema|Contexto do sistema]]

> Mapa de conteúdo (MOC) da base de conhecimento técnica do **sici-backend**.
> Legenda usada nas notas: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ API REST em Java 21 / Spring Boot 3.3 que apoia o ciclo de **ações de controle interno** (auditoria, consultoria, inspeção): planejamento (POAC, ação de controle), emissão de **Ordens de Serviço (OS)** em vários modelos, e **assinatura eletrônica** com numeração oficial, QR Code e código verificador.
Evidência: `pom.xml`, pacote `br.gov.df.cg.sici`, `domain/enums/EModeloOrdemServico`, `application/usecase/assinatura/AssinarOrdemServico`.

## Mapa

### 01 — Visão geral
- [[01-Sistemas/SICI/Backend/01-Visao-Geral/Stack-e-Dependencias|Stack-e-Dependencias]]
- [[01-Sistemas/SICI/Backend/01-Visao-Geral/Arquitetura-Hexagonal|Arquitetura-Hexagonal]]
- [[01-Sistemas/SICI/Backend/01-Visao-Geral/Perfis-e-Ambientes|Perfis-e-Ambientes]]
- [[01-Sistemas/SICI/Backend/01-Visao-Geral/Glossario|Glossario]]

### 02 — Domínio
- [[01-Sistemas/SICI/Backend/02-Dominio/Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/SICI/Backend/02-Dominio/Enums-e-Estados|Enums-e-Estados]] · [[01-Sistemas/SICI/Backend/02-Dominio/Banco-e-Migrations|Banco-e-Migrations]]

### 03 — Módulos
- [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Acao-de-Controle]] · [[01-Sistemas/SICI/Backend/03-Modulos/POAC|POAC]] · [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem-de-Servico]] · [[01-Sistemas/SICI/Backend/03-Modulos/Prorrogacao-e-Cancelamento|Prorrogacao-e-Cancelamento]]
- [[01-Sistemas/SICI/Backend/03-Modulos/OS-Generica|OS-Generica]] · [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura-Digital]] · [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI-e-Substitutos]]
- [[01-Sistemas/SICI/Backend/03-Modulos/Auditores-Coordenadores-Perfis|Auditores-Coordenadores-Perfis]] · [[01-Sistemas/SICI/Backend/03-Modulos/Cadastros-Auxiliares|Cadastros-Auxiliares]]

### 04 — Fluxos
- [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Ciclo-de-Vida-OS|Fluxo-Ciclo-de-Vida-OS]] · [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]] · [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Autenticacao|Fluxo-Autenticacao]]

### 05 a 08 — API, segurança, integrações, qualidade
- [[01-Sistemas/SICI/Backend/05-API/Catalogo-de-Endpoints|Catalogo-de-Endpoints]] · [[01-Sistemas/SICI/Backend/06-Seguranca/Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/SICI/Backend/07-Integracoes/Integracoes-Externas|Integracoes-Externas]]
- [[01-Sistemas/SICI/Backend/08-Qualidade/Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Debitos-Tecnicos]]

### 99 — Controle
- [[01-Sistemas/SICI/Backend/99-Controle/Registro-de-Analise|Registro-de-Analise]] — commit analisado, cobertura por lote
- [[01-Sistemas/SICI/Backend/99-Controle/Pendencias|Pendencias]] — dúvidas a confirmar com o time

## Principais riscos (resumo de [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Debitos-Tecnicos]])
1. 🔴 Qualquer auditor autenticado pode se cadastrar como SUBCI/substituto e assinar OS oficiais.
2. 🔴 Segredos versionados no repositório.
3. 🔴 Numeração oficial sujeita a duplicidade (sem lock nem unique).
4. 🔴 OS pode virar ASSINADA sem assinatura via mudança de status.

## Números rápidos (commit `1871e32`)
| Item | Quantidade |
|---|---|
| Classes Java (main) | 425 (api 25 · application 185 · domain 92 · infrastructure 122) |
| Controllers REST / endpoints | 19 / 61 (14 com role, 1 público, 46 só autenticados) |
| Migrations Flyway | 57 (V1–V57) |
| Templates Thymeleaf (PDF de OS) | 8 |
| Classes de teste / `@Test` | 31 / 64 (última execução local: 62 rodados, 11 falharam) |

## Política desta base
- Não contém valores de configuração, segredos, usuários privilegiados, endereços de infraestrutura, conteúdo de seeders nem dados reais.
