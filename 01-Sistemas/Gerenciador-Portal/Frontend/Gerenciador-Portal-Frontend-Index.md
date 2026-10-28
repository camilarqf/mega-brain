---
type: index
aliases:
  - "Gerenciador-Portal — Frontend (índice)"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
---
# Gerenciador-Portal — Frontend (índice)

Sistema: [[01-Sistemas/Gerenciador-Portal/Gerenciador-Portal-Index|Gerenciador-Portal]] · [[01-Sistemas/Gerenciador-Portal/Gerenciador-Portal-Repositorios|Repositórios]] · Backend: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

> MOC do **gerenciador-portal-frontend** (commit `d6a737a`). Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ SPA AngularJS 1.6 (módulo `gerenciadorPortal`) com login e telas administrativas que consomem a API do [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|backend do Gerenciador]]: arquivos/relatórios, imagens do portal, cargas, palavras-chave, órgãos da LAI e medida protetiva (a tela de textos das consultas existe na rota, mas está fora do menu). Sem guarda de rota nem token: o login só grava o usuário no `localStorage`.
Evidência: `package.json`, `bower.json`, `src/app/index.module.js`, `src/app/index.route.js`, `src/app/components/*`.

## Mapa

### 01 — Visão geral
- [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Arquitetura-AngularJS|Arquitetura-AngularJS]] · [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Build-e-Perfis-de-Ambiente|Build-e-Perfis-de-Ambiente]]

### 03 — Módulos de tela
- [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Arquivos|Arquivos]] · [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Imagens|Imagens]] · [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Cargas|Cargas]] · [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Palavras-Chave|Palavras-chave]]
- [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Orgaos-LAI|Órgãos LAI]] · [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Medida-Protetiva|Medida protetiva]] · [[01-Sistemas/Gerenciador-Portal/Frontend/03-Modulos/Gerenciador-Portal-Frontend-Modulo-Textos-do-Portal|Textos do portal]] (fora do menu)

### 04 — Fluxos
- [[01-Sistemas/Gerenciador-Portal/Frontend/05-Fluxos/Gerenciador-Portal-Frontend-Fluxo-Login-e-Sessao|Login e sessão]]

### 05 — API e integrações
- [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Integracao-API-Backend|Integração com o Backend]] · [[01-Sistemas/Gerenciador-Portal/Frontend/07-Integracoes/Gerenciador-Portal-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

### 06/07 — Segurança e qualidade
- [[01-Sistemas/Gerenciador-Portal/Frontend/08-Seguranca/Gerenciador-Portal-Frontend-Seguranca-e-Sessao|Segurança-e-Sessão]] · [[01-Sistemas/Gerenciador-Portal/Frontend/09-Qualidade/Gerenciador-Portal-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/Gerenciador-Portal/Frontend/09-Qualidade/Gerenciador-Portal-Frontend-Debitos-Tecnicos|Débitos-Técnicos]]

### 99 — Controle
- [[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Registro-de-Analise|Registro-de-Análise]] · [[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Pendencias|Pendências]]

## Pendências e próximo passo
- Lotes 0 a 3 concluídos (cobertura parcial: HTML das telas lido só em trechos). Próximo passo exato no [[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Registro-de-Analise|Registro de análise]].
