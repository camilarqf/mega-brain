---
type: index
aliases:
  - "PARTICIPA-DF — Frontend Ouvidoria (índice)"
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
---

# PARTICIPA-DF — Frontend Ouvidoria (índice)

Sistema: [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Index|PARTICIPA-DF]] · [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositórios]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Outro front-end: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]]

> Legenda: ✅ confirmado no código · 🔶 inferência · ❓ não identificado.

## O que é
✅ SPA **AngularJS 1.x** (módulo `Ouv-DF`, título "OUV-DF Sistema de Ouvidoria do Distrito Federal") com build Gulp, usada pelos **operadores das unidades de ouvidoria**: caixa de entrada de manifestações, detalhamento e tratamento (respostas, trâmite, reclassificação, prorrogação, invalidação), registro de manifestação em nome do cidadão, cadastro de conta do manifestante por operador, área gerencial (assuntos, usuários, unidades, perfis, formulários, prazos, bloqueio de usuário) e painéis de produtividade. Consome o `participa-df-backend`.

🔶 **Nome do componente.** O README do repositório o descreve como "Frontend AngularJS do módulo de Ouvidoria do Participa DF". `Frontend-Ouvidoria` é rótulo desta análise (não nome oficial). 🔶 Seria o `SistemaOuvDF` para onde o [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Frontend Cidadão]] redireciona; a correspondência não está confirmada (ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]]).

## Notas (links)
**Visão geral**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Stack-e-Dependencias|Stack-e-Dependencias]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Arquitetura|Arquitetura]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Perfis-e-Ambientes|Perfis-e-Ambientes]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Rotas-e-Telas|Rotas-e-Telas]]

**Segurança e fluxos**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/08-Seguranca/PARTICIPA-DF-Frontend-Ouvidoria-Seguranca-e-Sessao|Seguranca-e-Sessao]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Autenticacao|Fluxo-Autenticacao]]

**Fluxos**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Caixa-de-Entrada-e-Detalhamento|Fluxo-Caixa-de-Entrada-e-Detalhamento]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Registro-por-Operador|Fluxo-Registro-por-Operador]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Prorrogacao-de-Prazo|Fluxo-Prorrogacao-de-Prazo]]

**Módulos**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Gerencial|Modulo-Gerencial]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Dashboards-e-Relatorios|Modulo-Dashboards-e-Relatorios]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/03-Modulos/PARTICIPA-DF-Frontend-Ouvidoria-Modulo-Conta-por-Operador|Modulo-Conta-por-Operador]]

**API e integrações**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Chamadas-de-API|Chamadas-de-API]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Integracoes-Externas|Integracoes-Externas]]

**Qualidade**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Testes-e-Cobertura|Testes-e-Cobertura]]
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Debitos-Tecnicos]]

**Controle**
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Registro-de-Analise|Registro-de-Analise]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendencias]]

## Evidências
Repositório `participa-df-ouv-frontend`, branch `master`, commit `9d8ecdb` (2026-09-09; 197 commits desde 2021-11-07). Endereço do remoto omitido.

## Inferências e limitações
- Cobertura `parcial`; ver o registro de análise.
- A validade das notas depende do commit analisado; para atualizar, usar `atualizar-documentacao`.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Registro-de-Analise|Registro-de-Analise]] (próximo passo exato).
