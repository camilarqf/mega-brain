---
type: index
aliases:
  - "SICI — Frontend (índice)"
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
---

# SICI — Frontend (índice)

Sistema: [[01-Sistemas/SICI/SICI-Index|SICI]] · [[01-Sistemas/SICI/SICI-Repositorios|Repositórios]] · Backend: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]]

> Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ SPA Angular (`sici-frontend`) do SICI: autenticação, ações de controle, ordens de serviço (OS), OS genéricas, assinatura e validação de assinatura, e gestão de SUBCI e perfis de auditores. Consome o `sici-backend`.

## Notas (links)
**Visão geral**
- [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Stack-e-Dependencias|Stack-e-Dependencias]]
- [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]]
- [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Perfis-e-Ambientes|Perfis-e-Ambientes]]
- [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]]

**Módulos**
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Acao-de-Controle|Acao-de-Controle]]
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]]
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-OS-Generica|OS-Generica]]
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Gestao-SUBCI-e-Perfis|Gestao-SUBCI-e-Perfis]]
- [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]]

**Fluxos**
- [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Autenticacao|Fluxo-Autenticacao]]
- [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Ciclo-de-Vida-OS|Fluxo-Ciclo-de-Vida-OS]]
- [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]]

**API e integrações**
- [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]]
- [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Integracoes|Integracoes]] · [[Mapa-de-Integracoes|Mapa de integrações]]

**Segurança e qualidade**
- [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]
- [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]]
- [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]]

**Controle**
- [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Registro-de-Analise|Registro-de-Analise]] · [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendencias]]

## Evidências
Repositório `sici-frontend`, branch `master`, commit `418642f` (2026-09-29). Endereço do remoto omitido.

## Inferências e limitações
- Cobertura `parcial`: templates HTML, SCSS, `ordem-servico-cadastrar`/`atualizar` (lidos por trechos), `acao-controle-visualizar`/`atualizar` e DTOs não foram lidos linha a linha. `ng build` passou; `ng test` não compila (código do Keycloak); a aplicação não foi executada.
- Achados principais (a confirmar em execução): URLs sem barra, envio de OS em duplicidade, validação pública que chama endpoint autenticado e restrições de perfil só no cliente; ver [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]].
- A validade das notas depende do commit analisado; para atualizar, usar `atualizar-documentacao`.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Registro-de-Analise|Registro-de-Analise]] (próximo passo exato).
