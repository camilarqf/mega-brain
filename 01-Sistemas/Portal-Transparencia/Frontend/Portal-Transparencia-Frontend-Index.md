---
type: index
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
tags:
  - portal-transparencia
  - moc
  - frontend
---

# Portal-Transparencia — Frontend (índice)

Sistema: [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Index|Portal-Transparencia]] · [[01-Sistemas/Portal-Transparencia/Portal-Transparencia-Repositorios|Repositórios]] · Backend: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]]

> MOC do **portal-transparencia-frontend** (pasta local `PT2016_FrontEnd`). Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ SPA AngularJS 1.4 ("Portal 2016", título "Portal da Transparência") que consome a API REST do Backend e exibe consultas públicas de despesas, receitas, servidores, licitações e contratos, convênios, patrimônio, orçamento e prestação de contas, com exportação PDF/CSV, painéis gráficos e busca unificada. Sem login. Servida como arquivos estáticos (nginx).
Evidência: `package.json`, `bower.json`, `src/app/index.module.js`, `index.route.js`, `Dockerfile`, `nginx.conf`.

## Mapa

### 01 — Visão geral
- [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Arquitetura-AngularJS|Arquitetura-AngularJS]] · [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Build-e-Perfis-de-Ambiente|Build-e-Perfis-de-Ambiente]]

### 03 — Módulos de tela
- [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Despesas|Despesas]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Receitas|Receitas]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Servidores|Servidores]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Orcamento|Orçamento]]
- [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Licitacoes-e-Contratos|Licitações-e-Contratos]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Convenios|Convênios]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Patrimonio|Patrimônio]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Prestacao-de-Contas|Prestando-Contas]]
- [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Super-Busca|Super-Busca]] · [[01-Sistemas/Portal-Transparencia/Frontend/03-Modulos/Portal-Transparencia-Frontend-Modulo-Paginas-Institucionais-e-Navegacao|Páginas-Institucionais-e-Navegação]]

### 04 — API e integrações
- [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API do Backend]] · [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Catalogo-de-Chamadas-a-API|Catálogo de chamadas]] · [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas|Integrações externas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

### 05/06 — Segurança e qualidade
- [[01-Sistemas/Portal-Transparencia/Frontend/05-Seguranca/Portal-Transparencia-Frontend-Seguranca-e-Privacidade|Segurança-e-Privacidade]] · [[01-Sistemas/Portal-Transparencia/Frontend/06-Qualidade/Portal-Transparencia-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/Portal-Transparencia/Frontend/06-Qualidade/Portal-Transparencia-Frontend-Debitos-Tecnicos|Débitos-Técnicos]]

### 99 — Controle
- [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Registro-de-Analise|Registro-de-Análise]] · [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]]

## Evidências
Repositório `portal-transparencia-frontend`, branch `master`, commit `dca3e933` (2026-10-21). Endereço do remoto omitido.

## Informações confirmadas
- 103 rotas (`$routeProvider`), 11 rotas só-rótulo; 359 chamadas HTTP extraídas dos serviços (350 `GET`, 9 `POST`) mais 61 exportações PDF/CSV.
- Sem autenticação; cabeçalho `x-client-id` aleatório nas chamadas à API.
- 28 specs Karma e 1 e2e; não executados.
- Chamadas do frontend sem rota correspondente no Backend: ver [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Integracao-API-Backend|Integração com a API]].

## Inferências e limitações
- Cobertura `parcial`: leitura estática; templates, SCSS e lógica interna dos controllers por amostragem; DTOs não comparados campo a campo; build e testes não executados.
- Não há notas de fluxo nem de regra de negócio do frontend: as regras estão no Backend.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Registro-de-Analise|Registro de análise]] (próximo passo exato).
