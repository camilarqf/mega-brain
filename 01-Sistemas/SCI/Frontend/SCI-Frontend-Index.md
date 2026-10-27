---
type: index
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - sci
  - moc
  - frontend
---

# SCI — Frontend (índice)

Sistema: [[01-Sistemas/SCI/SCI-Index|SCI]] · [[01-Sistemas/SCI/SCI-Repositorios|Repositórios]] · [[01-Sistemas/SCI/SCI-Contexto-do-Sistema|Contexto do sistema]] · Backend: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

> Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ SPA Angular 18 (`sci-frontend`, pacote `sci-novo`) do SCI: denúncias, demandas, processo de admissibilidade (JAD), PIP, encaminhamentos, administração, painel de gestão e validação pública de assinatura. Consome o `sci-backend` por HTTP/JSON com token Bearer.

## Notas (links)
**Visão geral**
- [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Arquitetura|Arquitetura]] · [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Perfis-e-Ambientes|Perfis-e-Ambientes]] · [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Rotas-e-Telas|Rotas-e-Telas]]

**Módulos**
- [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Denuncia-e-Demanda|Denuncia-e-Demanda]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-JAD-Admissibilidade|JAD-Admissibilidade]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-PIP|PIP]]
- [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Encaminhamento-e-Gerenciador|Encaminhamento-e-Gerenciador]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Administracao-e-Gestao|Administracao-e-Gestao]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Assinatura-e-Validacao|Assinatura-e-Validacao]]

**Fluxos**
- [[01-Sistemas/SCI/Frontend/05-Fluxos/SCI-Frontend-Fluxo-Autenticacao|Fluxo-Autenticacao]] · [[01-Sistemas/SCI/Frontend/05-Fluxos/SCI-Frontend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo-Denuncia-ate-Admissibilidade]] · [[01-Sistemas/SCI/Frontend/05-Fluxos/SCI-Frontend-Fluxo-Ciclo-do-PIP|Fluxo-Ciclo-do-PIP]]

**API e integrações**
- [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas-de-API]] · [[01-Sistemas/SCI/Frontend/07-Integracoes/SCI-Frontend-Integracoes|Integracoes]] · [[Mapa-de-Integracoes|Mapa de integrações]]

**Segurança e qualidade**
- [[01-Sistemas/SCI/Frontend/08-Seguranca/SCI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]] · [[01-Sistemas/SCI/Frontend/09-Qualidade/SCI-Frontend-Testes-e-Cobertura|Testes-e-Cobertura]] · [[01-Sistemas/SCI/Frontend/09-Qualidade/SCI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]]

**Controle**
- [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Registro-de-Analise|Registro-de-Analise]] · [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendencias]]

## Evidências
Repositório `sci-frontend`, branch `master`, commit `5e20fda` (último commit de 2026-10-08; 845 commits desde 2024-03-20). Endereço do remoto omitido.

## Informações confirmadas
- 25 serviços HTTP, 144 combinações verbo + caminho; 136 existem no `sci-backend` analisado e **8 não**, 3 delas usadas em telas (denúncia por id, download de anexo da denúncia, processos da pessoa).
- 11 perfis de negócio; autorização no cliente por `data.role` e menu. Rotas `denuncias` e `encaminhados` sem `data.role`.
- Nenhum teste automatizado.

## Inferências e limitações
- Cobertura `parcial`: leitura estática; templates HTML, SCSS, a maior parte dos formulários e os componentes de análise/revisão por amostragem; DTOs não comparados campo a campo; `ng build`/`ng test` e a aplicação **não** foram executados.
- A validade das notas depende do commit analisado; para atualizar, usar `atualizar-documentacao`.
- Ponto de atenção principal: contrato cliente–servidor desalinhado (ver [[01-Sistemas/SCI/Frontend/09-Qualidade/SCI-Frontend-Debitos-Tecnicos|Débitos técnicos]]).

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Registro-de-Analise|Registro de análise]] (próximo passo exato).
