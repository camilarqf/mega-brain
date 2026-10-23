---
type: index
system: PARTICIPA-DF
repository: participa-df-backend
status: pendente
coverage: parcial
analyzed_commit: 820666cb28ee23b239e5ad033034c3e8413a10ed
created: 2026-10-18
updated: 2026-10-23
tags:
  - participa-df
  - moc
  - backend
---

# PARTICIPA-DF — Backend (índice)

Sistema: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|PARTICIPA-DF]] · [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositórios]]

> Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ API ASP.NET Core em .NET 5 (`OuvDF.Api`) que referencia os projetos `OuvDF.ServicoOuvidoria`, `OuvDF.ServicoInformacaoCidadao` e `OuvDF.Shared`.
Evidência: `src/OuvDF.sln`, `src/OuvDF.Api/OuvDF.Api.csproj` (ProjectReference), `src/OuvDF.Api/Controllers/`.

## Mapa
Lotes 0 a 8 concluídos (análise inicial completa; cobertura parcial). Contexto de negócio: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Contexto-do-Sistema|Contexto do sistema]].

### 01 — Visão geral
- [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]] · [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]] · [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Glossario|Glossario]]
- [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]] · [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Workflows-e-Consumidores|Workflows-e-Consumidores]]

### 02 — Domínio
- [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]] · [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Banco-e-Mapeamentos|Banco-e-Mapeamentos]]

### 03 — Módulos
- Identidade: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Bloqueio-de-Usuario|Bloqueio-de-Usuario]]
- Ouvidoria: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Manifestacao|Manifestacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Regras-de-Prazo-e-Prorrogacao|Regras-de-Prazo-e-Prorrogacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Reclassificacao-e-Invalidacao|Reclassificacao-e-Invalidacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Atribuicao-e-Bloqueio-Externo|Atribuicao-e-Bloqueio-Externo]]

- SIC: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Pedido-e-Recurso|Pedido-e-Recurso]] · [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Regras-de-Prazo-do-SIC|Regras-de-Prazo-do-SIC]]

### 04 — Fluxos
- SIC: [[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Pedido|Fluxo-Registro-de-Pedido]] · [[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Recursos-e-Instancias|Fluxo-Recursos-e-Instancias]] · [[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Omissao-de-Resposta|Fluxo-Omissao-de-Resposta]]
- [[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Registro-de-Manifestacao|Fluxo-Registro-de-Manifestacao]] · [[01-Sistemas/PARTICIPA-DF/Backend/04-Fluxos/PARTICIPA-DF-Backend-Fluxo-Tramitacao-e-Resposta|Fluxo-Tramitacao-e-Resposta]]

### 05 — API
- [[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (visão geral, matriz de acesso, Shared e raiz) · [[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Endpoints-Ouvidoria|Endpoints-Ouvidoria]] · [[01-Sistemas/PARTICIPA-DF/Backend/05-API/PARTICIPA-DF-Backend-Endpoints-SIC|Endpoints-SIC]]

### 06 — Segurança
- [[01-Sistemas/PARTICIPA-DF/Backend/06-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

### 07 — Integrações
- [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integracoes-Externas]]: Iza, MailService, PeoplesCheck, SEI, serviço de PDF, RabbitMQ (eventos de denúncia), armazenamento S3, geocodificação, Loki, New Relic e API `v1`. Mapa: [[Mapa-de-Integracoes|Mapa de integrações]].

### 08 — Qualidade
- [[01-Sistemas/PARTICIPA-DF/Backend/08-Qualidade/PARTICIPA-DF-Backend-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/PARTICIPA-DF/Backend/08-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

### 99 — Controle
- [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Registro-de-Analise|Registro-de-Analise]]: plano de lotes, cobertura e próximo passo
- [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendencias]]: dúvidas a confirmar com o time

## Principais riscos (resumo de [[01-Sistemas/PARTICIPA-DF/Backend/08-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Debitos-Tecnicos]])
1. 🔴 Segredos preenchidos em arquivos versionados (`appsettings*.json`, testes). 🔶 Atualização 2026-10-23: segredos de aplicação e a licença do New Relic saíram dos arquivos versionados e passaram a Swarm Secrets (`820666c`), mas continuam no histórico do git e os `appsettings` de teste não mudaram (A1/A1.1).
2. 🔴 25 endpoints sem autorização declarada e vários anônimos que gravam (`operador-ws`, unidades, notificações, `jobs`).
3. 🔴 Possível SSRF em `servicos/siturb` e `servicos/ra`; TLS desligado no PeoplesCheck.
4. 🔴 Logout sem efeito comprovado (verificação de token cancelado não ligada).
5. 🔴 Relato do cidadão em logs e enviado ao Iza (LGPD).
6. 🔴 .NET 5 sem suporte.
7. 🟠 Integração de denúncias com o S3 sem testes e com limpeza do bucket sem tratamento de falha (F1 a F5, 2026-10-23).

## Números rápidos (commit `4901ad5`, arquivos `.cs` fora de `bin/obj`; não refeitos na atualização de 2026-10-23)
| Item | Quantidade |
|---|---|
| `ServicoOuvidoria` / `ServicoInformacaoCidadao` / `Shared` / `Api` | 452 / 399 / 357 / 68 |
| Controllers em `Controllers/ServicoOuvidoria` / `ServicoInformacaoCidadao` / `Shared` (+ `Shared/v2`) | 22 / 10 / 13 (+ 1) |
| Jobs registrados no `Startup` | 10 |
| Projetos de teste / `.cs` em `IntegrationTests` | 6 / 151 |
