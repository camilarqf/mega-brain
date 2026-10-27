---
type: index
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
tags:
  - portal-transparencia
  - moc
  - backend
---

# Portal-Transparencia — Backend (índice)

Sistema: [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Index|Portal-Transparencia]] · [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Repositorios|Repositórios]]

> MOC da base técnica do **portal-transparencia-backend** (pasta local `PT2016_BackEnd`). Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ API REST em Spring Boot 1.3 (Java 8) que serve as consultas do Portal da Transparência: despesa, receita, servidores e remuneração, licitações e contratos, convênios, patrimônio e prestação de contas, com exportação em PDF/CSV, sobre SQL Server por consultas em templates Velocity. Oculta registros de pessoas com medida protetiva e não tem autenticação (consulta pública).
Evidência: `pom.xml`, `Application.java`, `api/*`, `resources/sql/*`.

## Mapa

### 01 — Visão geral
- [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]] · [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

### 02 — Domínio e persistência
- [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco-e-Migrations]]

### 03 — Módulos
- [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]]
- Por área funcional (lote 7; Despesa detalhada no lote 8: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Despesa-Consultas-e-Calculos|Despesa: consultas e cálculos]]): [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Despesa|Despesa]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Receita|Receita]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Servidores-e-Remuneracao|Servidores-e-Remuneracao]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Licitacoes-e-Contratos|Licitacoes-e-Contratos]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Convenios|Convenios]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Patrimonio|Patrimonio]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Prestacao-de-Contas|Prestacao-de-Contas]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Orcamento-e-Documentos-Publicados|Orcamento-e-Documentos-Publicados]] · [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Modulo-Apoio-e-Atualizacao-de-Dados|Apoio-e-Atualizacao-de-Dados]]

### 04 — Fluxos
- [[01-Sistemas/Portal-Transparencia/Backend/05-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Fluxo-Invalidacao-de-Cache-de-Mascarados]]

### 05 a 08 — API, segurança, integrações, qualidade
- Segurança aprofundada (lote 8): [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão de injeção de SQL]] · [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]]
- Atualização `e98fcc38` (storage MinIO): [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]] · [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] · [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]
- [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] · [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]]
- [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

### 99 — Controle
- [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Registro-de-Analise|Registro-de-Analise]] — commit analisado, cobertura por lote
- [[01-Sistemas/Portal-Transparencia/Backend/99-Controle/Portal-Transparencia-Backend-Pendencias|Pendencias]] — dúvidas a confirmar com o time

## Principais riscos (resumo de [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]])
1. 🔴 Credenciais do banco e da conta Google versionadas no código; certificado `.p12` no repositório e na imagem.
2. 🔴 Nenhuma autenticação; endpoints operacionais e `/integracao/*` abertos; CORS `*`.
3. 🔴 Injeção de SQL: 860 referências de texto bruto em 103 arquivos SQL e 5 rotas POST com fluxo direto ao SQL (confirmado por análise estática; exploração não testada).
4. 🔴 `/integracao/*` devolve CPF de servidores sem autenticação; programas sociais devolvem NIS/CPF sem máscara.
5. 🟡 Módulo de storage novo (`/storage/*`): dependência `io.minio` sem uso, host interno exposto e chaves ausentes em `dev`/`test`.
6. 🟠 Spring Boot 1.3 e Java 8 sem suporte; testes pulados no build da imagem.

## Números rápidos (commit `e98fcc38`)
| Item | Quantidade |
|---|---|
| Controllers com rota ativa / rotas | 70 / 559 (545 GET, 9 POST, 5 sem verbo) |
| Arquivos `.java` em `main` (`api` / `servico` / `modelo`) | 75 / 67 / 122 |
| Arquivos de consulta (`resources/sql`) | 547 |
| Entidades JPA | 6 |
| Classes de teste / `@Test` (versionados) | 14 / 139 |
| Métodos `@Mascaravel` | 30 |

## Política desta base
- Não contém valores de configuração, segredos, credenciais, hosts nem dados reais.
- Arquivos não versionados do repositório (relatórios `RELATORIO_*_LEGADO.md`, `logback-spring.xml`, testes de pesquisa) estão **fora do escopo** por decisão do usuário.
